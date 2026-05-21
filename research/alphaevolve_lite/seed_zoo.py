"""Deterministic daily-stock seed-zoo programs for Phase 4 parent discovery.

The seed zoo is deliberately separate from LLM child generation. It creates
auditable, hand-designed parent candidates so the AlphaEvolve loop is not
trapped around one fragile local parent.
"""

from __future__ import annotations

import csv
import math
import textwrap
from dataclasses import dataclass
from pathlib import Path
from string import Template
from typing import Any, Iterable

from .artifact_io import write_json
from .paths import sha256_file, utc_now_iso, write_text


SEED_ZOO_SCHEMA_VERSION = "phase4_seed_zoo_v1"
SEED_ZOO_PROGRAM_PREFIX = "PROG-20260521-SEEDZOO"


@dataclass(frozen=True)
class SeedZooSpec:
    """One deterministic parent candidate in the seed zoo."""

    seed_id: str
    program_id: str
    title: str
    thesis: str
    signal_template: str
    ranking_template: str
    params: dict[str, float | int]
    expected_effect: str


COMMON_PARAMS: dict[str, float | int] = {
    "lookback": 5,
    "min_history": 40,
    "vol_lookback": 20,
    "beta_lookback": 60,
    "momentum_lookback": 60,
    "momentum_weight": 0.25,
    "long_quantile": 0.9,
    "short_quantile": 0.1,
    "gross_exposure": 1.0,
    "max_weight": 0.02,
    "min_group_count": 10,
    "kalman_q": 1e-5,
    "kalman_r": 1e-3,
    "ewm_span": 10,
}


SIGNAL_TEMPLATES: dict[str, str] = {
    "one_day_excess_reversal": """
    min_history = int(cfg["min_history"])
    pieces: list[pd.Series] = []
    for _, group in data.groupby(CONTRACT.security_id, sort=False):
        excess = pd.to_numeric(group["_excess_return"], errors="coerce")
        history = excess.notna().cumsum()
        signal = -excess
        signal = signal.where(history >= min_history)
        pieces.append(signal.astype(float))
""",
    "five_day_excess_reversal": """
    lookback = int(cfg["lookback"])
    min_history = int(cfg["min_history"])
    pieces: list[pd.Series] = []
    for _, group in data.groupby(CONTRACT.security_id, sort=False):
        excess = pd.to_numeric(group["_excess_return"], errors="coerce")
        history = excess.notna().cumsum()
        reversal = -excess.rolling(lookback, min_periods=max(2, lookback // 2)).sum()
        signal = reversal.where(history >= min_history)
        pieces.append(signal.astype(float))
""",
    "vol_norm_five_day_reversal": """
    lookback = int(cfg["lookback"])
    min_history = int(cfg["min_history"])
    vol_lookback = int(cfg["vol_lookback"])
    pieces: list[pd.Series] = []
    for _, group in data.groupby(CONTRACT.security_id, sort=False):
        excess = pd.to_numeric(group["_excess_return"], errors="coerce")
        history = excess.notna().cumsum()
        reversal = -excess.rolling(lookback, min_periods=max(2, lookback // 2)).sum()
        vol = excess.rolling(vol_lookback, min_periods=max(5, vol_lookback // 2)).std()
        signal = reversal / vol.replace(0.0, np.nan).clip(lower=1e-4)
        signal = signal.where(history >= min_history)
        pieces.append(signal.astype(float))
""",
    "beta_residual_reversal": """
    min_history = int(cfg["min_history"])
    beta_lookback = int(cfg["beta_lookback"])
    vol_lookback = int(cfg["vol_lookback"])
    pieces: list[pd.Series] = []
    for _, group in data.groupby(CONTRACT.security_id, sort=False):
        excess = pd.to_numeric(group["_excess_return"], errors="coerce")
        market = pd.to_numeric(group["_market_return"], errors="coerce")
        history = excess.notna().cumsum()
        cov = excess.rolling(beta_lookback, min_periods=max(20, beta_lookback // 2)).cov(market)
        var = market.rolling(beta_lookback, min_periods=max(20, beta_lookback // 2)).var()
        beta = (cov / var.replace(0.0, np.nan)).clip(lower=-3.0, upper=3.0).fillna(1.0)
        residual = excess - beta * market
        vol = residual.rolling(vol_lookback, min_periods=max(5, vol_lookback // 2)).std()
        signal = -residual / vol.replace(0.0, np.nan).clip(lower=1e-4)
        signal = signal.where(history >= min_history)
        pieces.append(signal.astype(float))
""",
    "liquidity_confidence_reversal": """
    lookback = int(cfg["lookback"])
    min_history = int(cfg["min_history"])
    vol_lookback = int(cfg["vol_lookback"])
    pieces: list[pd.Series] = []
    for _, group in data.groupby(CONTRACT.security_id, sort=False):
        excess = pd.to_numeric(group["_excess_return"], errors="coerce")
        history = excess.notna().cumsum()
        reversal = -excess.rolling(lookback, min_periods=max(2, lookback // 2)).sum()
        vol = excess.rolling(vol_lookback, min_periods=max(5, vol_lookback // 2)).std()
        signal = reversal / vol.replace(0.0, np.nan).clip(lower=1e-4)
        signal = signal.where(history >= min_history)
        pieces.append(signal.astype(float))
    base_signal = pd.concat(pieces).reindex(data.index) if pieces else pd.Series(index=data.index, dtype=float)
    liquidity = np.log1p(pd.to_numeric(data[CONTRACT.dollar_volume], errors="coerce").abs())
    liquidity_pct = liquidity.groupby(data[CONTRACT.date]).rank(pct=True).clip(lower=0.05, upper=1.0)
    pieces = [(base_signal * (0.5 + liquidity_pct)).astype(float)]
""",
    "momentum_reversal_blend": """
    lookback = int(cfg["lookback"])
    min_history = int(cfg["min_history"])
    momentum_lookback = int(cfg["momentum_lookback"])
    momentum_weight = float(cfg["momentum_weight"])
    vol_lookback = int(cfg["vol_lookback"])
    pieces: list[pd.Series] = []
    for _, group in data.groupby(CONTRACT.security_id, sort=False):
        excess = pd.to_numeric(group["_excess_return"], errors="coerce")
        history = excess.notna().cumsum()
        reversal = -excess.rolling(lookback, min_periods=max(2, lookback // 2)).sum()
        medium_momentum = excess.rolling(momentum_lookback, min_periods=max(20, momentum_lookback // 2)).sum()
        blended = reversal + momentum_weight * medium_momentum
        vol = excess.rolling(vol_lookback, min_periods=max(5, vol_lookback // 2)).std()
        signal = blended / vol.replace(0.0, np.nan).clip(lower=1e-4)
        signal = signal.where(history >= min_history)
        pieces.append(signal.astype(float))
""",
    "kalman_innovation_reversal": """
    q = float(cfg["kalman_q"])
    r = float(cfg["kalman_r"])
    min_history = int(cfg["min_history"])
    vol_lookback = int(cfg["vol_lookback"])
    pieces: list[pd.Series] = []
    for _, group in data.groupby(CONTRACT.security_id, sort=False):
        values = group["_excess_return"].to_numpy(dtype=float)
        raw_signal = _kalman_innovation_reversal(values, q=q, r=r)
        signal = pd.Series(raw_signal, index=group.index, dtype=float)
        excess = pd.Series(values, index=group.index)
        history = excess.notna().cumsum()
        rolling_vol = excess.rolling(vol_lookback, min_periods=max(5, vol_lookback // 2)).std()
        signal = signal / rolling_vol.replace(0.0, np.nan).clip(lower=1e-4)
        signal = signal.where(history >= min_history)
        pieces.append(signal.astype(float))
""",
    "kalman_ewm_reversal": """
    q = float(cfg["kalman_q"])
    r = float(cfg["kalman_r"])
    min_history = int(cfg["min_history"])
    vol_lookback = int(cfg["vol_lookback"])
    ewm_span = int(cfg["ewm_span"])
    pieces: list[pd.Series] = []
    for _, group in data.groupby(CONTRACT.security_id, sort=False):
        values = group["_excess_return"].to_numpy(dtype=float)
        raw_signal = _kalman_innovation_reversal(values, q=q, r=r)
        signal = pd.Series(raw_signal, index=group.index, dtype=float)
        excess = pd.Series(values, index=group.index)
        history = excess.notna().cumsum()
        rolling_vol = excess.rolling(vol_lookback, min_periods=max(5, vol_lookback // 2)).std()
        signal = signal / rolling_vol.replace(0.0, np.nan).clip(lower=1e-4)
        signal = signal.where(history >= min_history)
        signal = signal.ewm(span=max(5, ewm_span), adjust=False).mean()
        pieces.append(signal.astype(float))
""",
}


RANKING_TEMPLATES: dict[str, str] = {
    "date_zscore": """
    def transform(group: pd.DataFrame) -> pd.Series:
        return _date_zscore(group["signal"], group.index)

    ranked = _apply_by_date(data, transform)
""",
    "industry_neutral_zscore": """
    min_group_count = int(cfg["min_group_count"])
    data[CONTRACT.industry_primary] = panel[CONTRACT.industry_primary]

    def transform(group: pd.DataFrame) -> pd.Series:
        out = pd.Series(np.nan, index=group.index, dtype=float)
        fallback = _date_zscore(group["signal"], group.index)
        for _, sub in group.groupby(CONTRACT.industry_primary, sort=False):
            if sub["signal"].notna().sum() >= min_group_count:
                out.loc[sub.index] = _date_zscore(sub["signal"], sub.index)
        return out.fillna(fallback)

    ranked = _apply_by_date(data, transform)
""",
    "size_bucket_zscore": """
    min_group_count = int(cfg["min_group_count"])
    data[CONTRACT.market_cap] = pd.to_numeric(panel[CONTRACT.market_cap], errors="coerce")

    def transform(group: pd.DataFrame) -> pd.Series:
        out = pd.Series(np.nan, index=group.index, dtype=float)
        fallback = _date_zscore(group["signal"], group.index)
        size_rank = group[CONTRACT.market_cap].rank(method="first")
        if size_rank.notna().sum() < min_group_count * 3:
            return fallback
        buckets = pd.qcut(size_rank, q=5, labels=False, duplicates="drop")
        for _, idx in buckets.groupby(buckets, sort=False).groups.items():
            sub_signal = group.loc[idx, "signal"]
            if sub_signal.notna().sum() >= min_group_count:
                out.loc[idx] = _date_zscore(sub_signal, idx)
        return out.fillna(fallback)

    ranked = _apply_by_date(data, transform)
""",
}


SEED_ZOO_SPECS: tuple[SeedZooSpec, ...] = (
    SeedZooSpec(
        seed_id="one_day_excess_reversal",
        program_id=f"{SEED_ZOO_PROGRAM_PREFIX}-0001",
        title="One-day excess reversal",
        thesis="Use the latest market-adjusted ex-dividend return as a short-horizon reversal parent.",
        signal_template="one_day_excess_reversal",
        ranking_template="date_zscore",
        params={"min_history": 20},
        expected_effect="tests whether attempt017 adds value beyond the simplest causal reversal parent",
    ),
    SeedZooSpec(
        seed_id="five_day_excess_reversal",
        program_id=f"{SEED_ZOO_PROGRAM_PREFIX}-0002",
        title="Five-day excess reversal",
        thesis="Use a short rolling excess-return sum to reduce one-day noise while preserving reversal.",
        signal_template="five_day_excess_reversal",
        ranking_template="date_zscore",
        params={"lookback": 5, "min_history": 30},
        expected_effect="tests whether a smoother deterministic reversal parent beats Kalman filtering",
    ),
    SeedZooSpec(
        seed_id="vol_norm_five_day_reversal",
        program_id=f"{SEED_ZOO_PROGRAM_PREFIX}-0003",
        title="Volatility-normalized five-day reversal",
        thesis="Normalize short-horizon reversal by rolling residual volatility before cross-sectional ranking.",
        signal_template="vol_norm_five_day_reversal",
        ranking_template="date_zscore",
        params={"lookback": 5, "vol_lookback": 20, "min_history": 40},
        expected_effect="tests whether scale control is the main driver behind attempt017",
    ),
    SeedZooSpec(
        seed_id="beta_residual_reversal",
        program_id=f"{SEED_ZOO_PROGRAM_PREFIX}-0004",
        title="Rolling beta-residual reversal",
        thesis="Remove a rolling market-beta component before taking reversal signals.",
        signal_template="beta_residual_reversal",
        ranking_template="date_zscore",
        params={"beta_lookback": 60, "vol_lookback": 20, "min_history": 80},
        expected_effect="tests whether market-residual construction beats simple vwretd subtraction",
    ),
    SeedZooSpec(
        seed_id="liquidity_confidence_reversal",
        program_id=f"{SEED_ZOO_PROGRAM_PREFIX}-0005",
        title="Liquidity-confidence reversal",
        thesis="Favor reversal signals in more liquid names using same-day dollar-volume percentile confidence.",
        signal_template="liquidity_confidence_reversal",
        ranking_template="date_zscore",
        params={"lookback": 5, "vol_lookback": 20, "min_history": 40},
        expected_effect="tests whether ex-ante tradability improves turnover-aware evidence",
    ),
    SeedZooSpec(
        seed_id="industry_neutral_reversal",
        program_id=f"{SEED_ZOO_PROGRAM_PREFIX}-0006",
        title="Industry-neutral reversal",
        thesis="Rank volatility-normalized reversal within SIC groups with date-level fallback.",
        signal_template="vol_norm_five_day_reversal",
        ranking_template="industry_neutral_zscore",
        params={"lookback": 5, "vol_lookback": 20, "min_history": 40, "min_group_count": 10},
        expected_effect="tests whether sector/industry shocks are hurting the reversal parent",
    ),
    SeedZooSpec(
        seed_id="size_bucket_reversal",
        program_id=f"{SEED_ZOO_PROGRAM_PREFIX}-0007",
        title="Size-bucket reversal",
        thesis="Rank volatility-normalized reversal inside daily market-cap buckets.",
        signal_template="vol_norm_five_day_reversal",
        ranking_template="size_bucket_zscore",
        params={"lookback": 5, "vol_lookback": 20, "min_history": 40, "min_group_count": 10},
        expected_effect="tests whether size effects dominate the cross-section",
    ),
    SeedZooSpec(
        seed_id="momentum_reversal_blend",
        program_id=f"{SEED_ZOO_PROGRAM_PREFIX}-0008",
        title="Momentum/reversal blend",
        thesis="Blend short-term reversal with a weaker medium-horizon momentum term.",
        signal_template="momentum_reversal_blend",
        ranking_template="date_zscore",
        params={"lookback": 5, "momentum_lookback": 60, "momentum_weight": 0.25, "min_history": 80},
        expected_effect="tests whether pure reversal is too myopic over the 2011-2025 window",
    ),
    SeedZooSpec(
        seed_id="kalman_reversal_base",
        program_id=f"{SEED_ZOO_PROGRAM_PREFIX}-0009",
        title="Kalman innovation reversal baseline",
        thesis="Render the canonical Kalman innovation reversal as a seed-zoo parent candidate.",
        signal_template="kalman_innovation_reversal",
        ranking_template="date_zscore",
        params={},
        expected_effect="anchors the zoo against the original generation-zero Kalman seed",
    ),
    SeedZooSpec(
        seed_id="kalman_ewm_reversal",
        program_id=f"{SEED_ZOO_PROGRAM_PREFIX}-0010",
        title="Kalman EWM reversal",
        thesis="Render the attempt017-style causal EWM smoothing mechanism as a deterministic parent.",
        signal_template="kalman_ewm_reversal",
        ranking_template="date_zscore",
        params={"ewm_span": 10},
        expected_effect="anchors the zoo against the current attempt017-style lead",
    ),
)


PROGRAM_TEMPLATE = Template(
    '''"""Deterministic Phase 4 seed-zoo program: $seed_id."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from research.alphaevolve_lite.daily_stock_contract import CONTRACT


STRATEGY_ID = "$seed_id"
STRATEGY_FAMILY = "daily_stock_seed_zoo"
STRATEGY_TITLE = "$title"
STRATEGY_THESIS = "$thesis"
EXPECTED_EFFECT = "$expected_effect"

DEFAULT_PARAMS: dict[str, float | int] = $params_repr


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


def _date_zscore(values: pd.Series, index: pd.Index) -> pd.Series:
    """Robust date-level z-score with winsorized tails."""

    s = values.replace([np.inf, -np.inf], np.nan)
    if s.notna().sum() < 10:
        return pd.Series(np.nan, index=index, dtype=float)
    lo = s.quantile(0.01)
    hi = s.quantile(0.99)
    clipped = s.clip(lower=lo, upper=hi)
    demeaned = clipped - clipped.mean()
    scale = demeaned.std(ddof=0)
    if not np.isfinite(scale) or scale <= 0.0:
        return pd.Series(np.nan, index=index, dtype=float)
    return (demeaned / scale).reindex(index)


def _apply_by_date(data: pd.DataFrame, transform) -> pd.Series:
    """Apply a date-level transform across pandas versions."""

    grouped = data.groupby(CONTRACT.date, group_keys=False)
    try:
        return grouped.apply(transform, include_groups=False)
    except TypeError:
        return grouped.apply(transform)


def compute_signal(panel: pd.DataFrame, params: dict[str, Any] | None = None) -> pd.Series:
    """Compute a causal daily-stock seed-zoo signal."""

    cfg = {**DEFAULT_PARAMS, **(params or {})}
    data = panel.sort_values([CONTRACT.security_id, CONTRACT.date]).copy()
    data["_excess_return"] = (
        pd.to_numeric(data[CONTRACT.ex_dividend_return], errors="coerce")
        - pd.to_numeric(data[CONTRACT.benchmark_return_primary], errors="coerce")
    )
    data["_market_return"] = pd.to_numeric(data[CONTRACT.benchmark_return_primary], errors="coerce")

    # EVOLVE-BLOCK-START: signal
$signal_body
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
    """Cross-sectionally transform the seed-zoo signal inside each date."""

    cfg = {**DEFAULT_PARAMS, **(params or {})}
    data = panel[[CONTRACT.date]].copy()
    data["signal"] = signal

    # EVOLVE-BLOCK-START: ranking
$ranking_body
    # EVOLVE-BLOCK-END

    return ranked.reindex(panel.index).rename("ranked_signal")


def construct_portfolio(
    signal: pd.Series,
    panel: pd.DataFrame,
    params: dict[str, Any] | None = None,
) -> pd.Series:
    """Construct daily equal-side long/short target weights from ranked signal."""

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
'''
)


def all_seed_zoo_specs() -> list[SeedZooSpec]:
    """Return the frozen seed-zoo spec list."""

    return list(SEED_ZOO_SPECS)


def select_seed_zoo_specs(seed_ids: Iterable[str] | None = None) -> list[SeedZooSpec]:
    """Select specs by id while preserving the frozen zoo order."""

    specs = all_seed_zoo_specs()
    if seed_ids is None:
        return specs
    wanted = {seed_id.strip() for seed_id in seed_ids if seed_id.strip()}
    if not wanted or wanted == {"all"}:
        return specs
    available = {spec.seed_id for spec in specs}
    missing = sorted(wanted - available)
    if missing:
        raise ValueError(f"unknown seed-zoo ids: {missing}; available={sorted(available)}")
    return [spec for spec in specs if spec.seed_id in wanted]


def render_seed_program(spec: SeedZooSpec) -> str:
    """Render one concrete executable parent program."""

    params = {**COMMON_PARAMS, **spec.params}
    signal_body = _indent_block(SIGNAL_TEMPLATES[spec.signal_template], spaces=4)
    ranking_body = _indent_block(RANKING_TEMPLATES[spec.ranking_template], spaces=4)
    return PROGRAM_TEMPLATE.substitute(
        seed_id=spec.seed_id,
        title=_escape_double_quotes(spec.title),
        thesis=_escape_double_quotes(spec.thesis),
        expected_effect=_escape_double_quotes(spec.expected_effect),
        params_repr=repr(params),
        signal_body=signal_body,
        ranking_body=ranking_body,
    )


def write_seed_zoo_programs(
    out_dir: str | Path,
    *,
    seed_ids: Iterable[str] | None = None,
) -> dict[str, Any]:
    """Write selected seed-zoo programs and a manifest."""

    root = Path(out_dir)
    program_dir = root / "programs"
    program_dir.mkdir(parents=True, exist_ok=True)
    specs = select_seed_zoo_specs(seed_ids)
    rows = []
    for spec in specs:
        program_path = program_dir / f"{spec.seed_id}.py"
        write_text(program_path, render_seed_program(spec))
        rows.append(
            {
                "seed_id": spec.seed_id,
                "program_id": spec.program_id,
                "title": spec.title,
                "thesis": spec.thesis,
                "expected_effect": spec.expected_effect,
                "program_path": str(program_path),
                "program_sha256": sha256_file(program_path),
                "signal_template": spec.signal_template,
                "ranking_template": spec.ranking_template,
                "params": {**COMMON_PARAMS, **spec.params},
            }
        )
    manifest = {
        "schema_version": SEED_ZOO_SCHEMA_VERSION,
        "created_at": utc_now_iso(),
        "program_count": len(rows),
        "programs": rows,
    }
    write_json(root / "seed_zoo_manifest.json", manifest)
    _write_seed_zoo_manifest_md(root / "seed_zoo_manifest.md", manifest)
    return manifest


def seed_zoo_rows_from_summaries(
    summaries: Iterable[dict[str, Any]],
    *,
    benchmark_summary: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Convert evaluator summaries into sortable seed-zoo result rows."""

    benchmark_metrics = (benchmark_summary or {}).get("metrics", {}).get("search_sample", {})
    benchmark_program_id = (benchmark_summary or {}).get("program_id")
    rows = []
    for summary in summaries:
        metrics = summary.get("metrics", {})
        search = metrics.get("search_sample", {})
        in_sample = metrics.get("in_sample", {})
        out_sample = metrics.get("out_sample", {})
        degradation = metrics.get("is_os_degradation", {})
        descriptors = summary.get("descriptors", {})
        turnover_score = _finite(search.get("turnover_aware_score"))
        is_sharpe = _finite(in_sample.get("sharpe"))
        os_sharpe = _finite(out_sample.get("sharpe"))
        degradation_value = _finite(degradation.get("is_to_os_sharpe_degradation"))
        admission_score = _seed_zoo_admission_score(
            turnover_score=turnover_score,
            is_sharpe=is_sharpe,
            os_sharpe=os_sharpe,
            is_to_os_sharpe_degradation=degradation_value,
            decision=str(summary.get("decision", "")),
        )
        row = {
            "program_id": summary.get("program_id"),
            "decision": summary.get("decision"),
            "strategy_id": descriptors.get("strategy_id"),
            "strategy_family": descriptors.get("strategy_family"),
            "program_path": descriptors.get("program_path"),
            "is_sharpe": is_sharpe,
            "os_sharpe": os_sharpe,
            "search_sample_sharpe": _finite(search.get("sharpe")),
            "search_sample_annualized_return": _finite(search.get("annualized_return")),
            "turnover": _finite(search.get("turnover")),
            "turnover_aware_score": turnover_score,
            "max_missing_held_weight": _finite(search.get("max_missing_held_weight")),
            "max_weight": _finite(search.get("max_weight")),
            "is_to_os_sharpe_degradation": degradation_value,
            "portfolio_day_coverage": descriptors.get("portfolio_day_coverage"),
            "admission_score": admission_score,
            "benchmark_program_id": benchmark_program_id,
            "benchmark_turnover_aware_delta": _delta(turnover_score, benchmark_metrics.get("turnover_aware_score")),
            "benchmark_search_sharpe_delta": _delta(search.get("sharpe"), benchmark_metrics.get("sharpe")),
        }
        row["parent_candidate_tier"] = _parent_candidate_tier(row)
        rows.append(row)
    rows.sort(
        key=lambda row: (
            row["parent_candidate_tier"] != "candidate",
            -_sort_float(row["admission_score"]),
            -_sort_float(row["turnover_aware_score"]),
            -_sort_float(row["os_sharpe"]),
            str(row["program_id"]),
        )
    )
    return rows


def write_seed_zoo_results(
    out_dir: str | Path,
    summaries: Iterable[dict[str, Any]],
    *,
    benchmark_summary: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Write aggregate seed-zoo ranking artifacts."""

    root = Path(out_dir)
    rows = seed_zoo_rows_from_summaries(summaries, benchmark_summary=benchmark_summary)
    result = {
        "schema_version": SEED_ZOO_SCHEMA_VERSION,
        "created_at": utc_now_iso(),
        "program_count": len(rows),
        "benchmark_program_id": (benchmark_summary or {}).get("program_id"),
        "rows": rows,
    }
    write_json(root / "seed_zoo_results.json", result)
    _write_csv(root / "seed_zoo_results.csv", rows)
    _write_seed_zoo_report(root / "seed_zoo_report.md", result)
    return result


def _seed_zoo_admission_score(
    *,
    turnover_score: float | None,
    is_sharpe: float | None,
    os_sharpe: float | None,
    is_to_os_sharpe_degradation: float | None,
    decision: str,
) -> float:
    """Rank parent candidates without pretending to prove alpha."""

    if turnover_score is None:
        return float("-inf")
    score = turnover_score
    if is_sharpe is not None and os_sharpe is not None:
        score += 0.10 * min(is_sharpe, os_sharpe)
    if is_to_os_sharpe_degradation is not None and is_to_os_sharpe_degradation > 0.0:
        score -= 0.25 * is_to_os_sharpe_degradation
    if os_sharpe is not None and os_sharpe < 0.0:
        score -= 0.50
    if decision != "sample_pass":
        score -= 0.25
    return float(score)


def _parent_candidate_tier(row: dict[str, Any]) -> str:
    score = _finite(row.get("turnover_aware_score"))
    os_sharpe = _finite(row.get("os_sharpe"))
    coverage = _finite(row.get("portfolio_day_coverage"))
    if (
        row.get("decision") == "sample_pass"
        and score is not None
        and score > 0.0
        and os_sharpe is not None
        and os_sharpe > 0.0
        and (coverage is None or coverage >= 0.80)
    ):
        return "candidate"
    return "review"


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _write_seed_zoo_manifest_md(path: Path, manifest: dict[str, Any]) -> None:
    lines = [
        "# Seed Zoo Manifest",
        "",
        f"- schema_version: `{manifest['schema_version']}`",
        f"- program_count: `{manifest['program_count']}`",
        "",
        "| Program | Title | Signal | Ranking | Expected effect |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in manifest["programs"]:
        lines.append(
            "| `{program_id}` | {title} | `{signal_template}` | `{ranking_template}` | {expected_effect} |".format(
                **row
            )
        )
    write_text(path, "\n".join(lines) + "\n")


def _write_seed_zoo_report(path: Path, result: dict[str, Any]) -> None:
    lines = [
        "# Seed Zoo Results",
        "",
        f"- schema_version: `{result['schema_version']}`",
        f"- program_count: `{result['program_count']}`",
        f"- benchmark_program_id: `{result.get('benchmark_program_id')}`",
        "",
        "| Tier | Program | Strategy | Decision | IS Sharpe | OS Sharpe | Search Sharpe | Turnover | Score | Admission |",
        "| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in result["rows"]:
        lines.append(
            "| {tier} | `{program}` | `{strategy}` | `{decision}` | {is_s} | {os_s} | {search_s} | {turnover} | {score} | {admission} |".format(
                tier=row.get("parent_candidate_tier"),
                program=row.get("program_id"),
                strategy=row.get("strategy_id"),
                decision=row.get("decision"),
                is_s=_format_number(row.get("is_sharpe")),
                os_s=_format_number(row.get("os_sharpe")),
                search_s=_format_number(row.get("search_sample_sharpe")),
                turnover=_format_number(row.get("turnover")),
                score=_format_number(row.get("turnover_aware_score")),
                admission=_format_number(row.get("admission_score")),
            )
        )
    lines.extend(
        [
            "",
            "Interpretation rule: this table ranks parent candidates for further AlphaEvolve search. "
            "It is not promotion or final validation.",
        ]
    )
    write_text(path, "\n".join(lines) + "\n")


def _escape_double_quotes(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def _indent_block(block: str, *, spaces: int) -> str:
    prefix = " " * spaces
    raw_lines = textwrap.dedent(block).strip("\n").splitlines()
    return "\n".join(prefix + line if line else "" for line in raw_lines)


def _finite(value: Any) -> float | None:
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    return result if math.isfinite(result) else None


def _delta(value: Any, benchmark: Any) -> float | None:
    left = _finite(value)
    right = _finite(benchmark)
    if left is None or right is None:
        return None
    return float(left - right)


def _sort_float(value: Any) -> float:
    result = _finite(value)
    return result if result is not None else float("-inf")


def _format_number(value: Any) -> str:
    result = _finite(value)
    return "" if result is None else f"{result:.4f}"


__all__ = [
    "SEED_ZOO_PROGRAM_PREFIX",
    "SEED_ZOO_SCHEMA_VERSION",
    "SEED_ZOO_SPECS",
    "SeedZooSpec",
    "all_seed_zoo_specs",
    "render_seed_program",
    "seed_zoo_rows_from_summaries",
    "select_seed_zoo_specs",
    "write_seed_zoo_programs",
    "write_seed_zoo_results",
]
