"""Generation-zero Kalman innovation reversal seed program."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from research.alphaevolve_lite.daily_stock_contract import CONTRACT


DEFAULT_PARAMS: dict[str, float | int] = {
    "kalman_q": 1e-5,
    "kalman_r": 1e-3,
    "vol_lookback": 20,
    "min_history": 40,
    "long_quantile": 0.9,
    "short_quantile": 0.1,
    "gross_exposure": 1.0,
    "max_weight": 0.02,
}


def _kalman_innovation_reversal(values: np.ndarray, q: float, r: float) -> np.ndarray:
    """Causal scalar local-level Kalman innovation signal."""

    state = 0.0
    variance = 1.0
    out = np.full(len(values), np.nan, dtype=float)
    for i, observation in enumerate(values):
        if not np.isfinite(observation):
            variance += q
            continue
        prior_state = state
        prior_variance = variance + q
        innovation = observation - prior_state
        innovation_variance = prior_variance + r
        if innovation_variance <= 0.0 or not np.isfinite(innovation_variance):
            variance = prior_variance
            continue
        gain = prior_variance / innovation_variance
        state = prior_state + gain * innovation
        variance = max((1.0 - gain) * prior_variance, 1e-12)
        out[i] = -innovation / float(np.sqrt(innovation_variance))
    return out


def compute_signal(panel: pd.DataFrame, params: dict[str, Any] | None = None) -> pd.Series:
    """Compute a causal Kalman innovation reversal signal."""

    cfg = {**DEFAULT_PARAMS, **(params or {})}
    data = panel.sort_values([CONTRACT.security_id, CONTRACT.date]).copy()
    excess = (
        pd.to_numeric(data[CONTRACT.ex_dividend_return], errors="coerce")
        - pd.to_numeric(data[CONTRACT.benchmark_return_primary], errors="coerce")
    )
    data["_excess_return"] = excess

    # EVOLVE-BLOCK-START: signal
    q = float(cfg["kalman_q"])
    r = float(cfg["kalman_r"])
    min_history = int(cfg["min_history"])
    vol_lookback = int(cfg["vol_lookback"])

    pieces: list[pd.Series] = []
    for _, group in data.groupby(CONTRACT.security_id, sort=False):
        values = group["_excess_return"].to_numpy(dtype=float)
        raw_signal = _kalman_innovation_reversal(values, q=q, r=r)
        signal = pd.Series(raw_signal, index=group.index, dtype=float)
        history = pd.Series(values, index=group.index).notna().groupby(group[CONTRACT.security_id]).cumsum()
        rolling_vol = (
            pd.Series(values, index=group.index)
            .rolling(vol_lookback, min_periods=max(5, vol_lookback // 2))
            .std()
            .replace(0.0, np.nan)
        )
        signal = signal / rolling_vol.clip(lower=1e-4)
        signal = signal.where(history >= min_history)
        pieces.append(signal)
    # EVOLVE-BLOCK-END

    if not pieces:
        return pd.Series(index=panel.index, dtype=float, name="signal")
    combined = pd.concat(pieces).reindex(data.index)
    return combined.reindex(panel.index).rename("signal")


def rank_or_transform_signal(
    signal: pd.Series,
    panel: pd.DataFrame,
    params: dict[str, Any] | None = None,
) -> pd.Series:
    """Cross-sectionally standardize the signal inside each date."""

    _ = params
    data = panel[[CONTRACT.date]].copy()
    data["signal"] = signal

    # EVOLVE-BLOCK-START: ranking
    def transform(group: pd.DataFrame) -> pd.Series:
        s = group["signal"].replace([np.inf, -np.inf], np.nan)
        if s.notna().sum() < 10:
            return pd.Series(np.nan, index=group.index)
        lo = s.quantile(0.01)
        hi = s.quantile(0.99)
        clipped = s.clip(lower=lo, upper=hi)
        demeaned = clipped - clipped.mean()
        scale = demeaned.std(ddof=0)
        if not np.isfinite(scale) or scale <= 0.0:
            return pd.Series(np.nan, index=group.index)
        return demeaned / scale

    ranked = data.groupby(CONTRACT.date, group_keys=False).apply(transform)
    # EVOLVE-BLOCK-END

    return ranked.reindex(panel.index).rename("ranked_signal")


def construct_portfolio(
    signal: pd.Series,
    panel: pd.DataFrame,
    params: dict[str, Any] | None = None,
) -> pd.Series:
    """Construct daily long/short target weights from ranked signal."""

    cfg = {**DEFAULT_PARAMS, **(params or {})}
    data = panel[[CONTRACT.date, CONTRACT.security_id]].copy()
    data["signal"] = signal

    # EVOLVE-BLOCK-START: portfolio
    long_q = float(cfg["long_quantile"])
    short_q = float(cfg["short_quantile"])
    gross = float(cfg["gross_exposure"])

    weights = pd.Series(0.0, index=panel.index, dtype=float, name="weight")
    for _, group in data.groupby(CONTRACT.date, sort=True):
        valid = group.dropna(subset=["signal"])
        if len(valid) < 20:
            continue
        long_cut = valid["signal"].quantile(long_q)
        short_cut = valid["signal"].quantile(short_q)
        longs = valid.index[valid["signal"] >= long_cut]
        shorts = valid.index[valid["signal"] <= short_cut]
        if len(longs) == 0 or len(shorts) == 0:
            continue
        weights.loc[longs] = 0.5 * gross / len(longs)
        weights.loc[shorts] = -0.5 * gross / len(shorts)
    # EVOLVE-BLOCK-END

    return weights


def apply_risk_controls(
    weights: pd.Series,
    panel: pd.DataFrame,
    params: dict[str, Any] | None = None,
) -> pd.Series:
    """Cap single-name weights and rebalance each side separately."""

    cfg = {**DEFAULT_PARAMS, **(params or {})}
    data = panel[[CONTRACT.date]].copy()
    data["weight"] = weights.fillna(0.0)

    # EVOLVE-BLOCK-START: risk
    max_weight = float(cfg["max_weight"])
    controlled = pd.Series(0.0, index=weights.index, dtype=float, name="weight")
    for _, group in data.groupby(CONTRACT.date, sort=True):
        w = group["weight"].clip(lower=-max_weight, upper=max_weight)
        long_sum = w[w > 0].sum()
        short_sum = -w[w < 0].sum()
        if long_sum > 0:
            w.loc[w > 0] *= 0.5 / long_sum
        if short_sum > 0:
            w.loc[w < 0] *= 0.5 / short_sum
        controlled.loc[group.index] = w.clip(lower=-max_weight, upper=max_weight)
    # EVOLVE-BLOCK-END

    return controlled


def evaluate(eval_inputs: dict[str, Any]) -> dict[str, float]:
    """Small in-memory evaluation hook used by controller smoke tests."""

    panel = eval_inputs["panel"]
    params = {**DEFAULT_PARAMS, **eval_inputs.get("params", {})}
    signal = compute_signal(panel, params)
    ranked = rank_or_transform_signal(signal, panel, params)
    weights = construct_portfolio(ranked, panel, params)
    weights = apply_risk_controls(weights, panel, params)
    out = {
        "mean_abs_weight": float(weights.abs().mean()) if len(weights) else float("nan"),
        "max_weight": float(weights.abs().max()) if len(weights) else float("nan"),
        "nonzero_weight_count": float(weights.ne(0.0).sum()),
    }
    if "fwd_ret" in panel.columns:
        pnl = weights * pd.to_numeric(panel["fwd_ret"], errors="coerce")
        daily = pnl.groupby(panel[CONTRACT.date]).sum()
        vol = daily.std(ddof=1)
        out["mean_daily_return"] = float(daily.mean()) if len(daily) else float("nan")
        out["daily_sharpe"] = float(daily.mean() / vol * np.sqrt(252.0)) if vol and vol > 0 else float("nan")
    return out
