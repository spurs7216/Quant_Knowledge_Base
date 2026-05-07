"""Portfolio accounting and metrics for remote sample evaluation."""

from __future__ import annotations

import math
from typing import Any


EMPTY_SPLIT_METRICS = {
    "annualized_return": float("nan"),
    "annualized_volatility": float("nan"),
    "sharpe": float("nan"),
    "gross_annualized_return": float("nan"),
    "gross_sharpe": float("nan"),
    "max_drawdown": float("nan"),
    "turnover": float("nan"),
    "hit_rate": float("nan"),
    "beta_to_vwretd": float("nan"),
    "mean_daily_n_names": float("nan"),
    "mean_missing_held_weight": float("nan"),
    "max_missing_held_weight": float("nan"),
    "max_weight": float("nan"),
    "turnover_aware_score": float("nan"),
}


def empty_split_metrics() -> dict[str, float]:
    """Return a fresh all-NaN split metric record."""

    return dict(EMPTY_SPLIT_METRICS)


def max_drawdown(returns: Any) -> float:
    wealth = (1.0 + returns.fillna(0.0)).cumprod()
    peak = wealth.cummax()
    drawdown = wealth / peak - 1.0
    return float(drawdown.min()) if len(drawdown) else float("nan")


def beta_to_market(returns: Any, market: Any) -> float:
    import numpy as np
    import pandas as pd

    joined = pd.concat([returns, market], axis=1).dropna()
    if len(joined) < 2:
        return float("nan")
    y = joined.iloc[:, 0].to_numpy(dtype=float)
    x = joined.iloc[:, 1].to_numpy(dtype=float)
    var_x = np.var(x, ddof=1)
    if var_x <= 0 or not np.isfinite(var_x):
        return float("nan")
    return float(np.cov(x, y, ddof=1)[0, 1] / var_x)


def turnover_aware_score(
    *,
    sharpe: float,
    turnover: float,
    max_missing_held_weight: float,
    turnover_penalty: float = 0.25,
    missing_weight_penalty: float = 5.0,
) -> float:
    values = [sharpe, turnover, max_missing_held_weight]
    if any(not math.isfinite(float(value)) for value in values):
        return float("nan")
    return float(sharpe - turnover_penalty * turnover - missing_weight_penalty * max_missing_held_weight)


def split_metrics(
    portfolio: Any,
    split_name: str,
    start: Any,
    end: Any,
    *,
    turnover_penalty: float = 0.25,
    missing_weight_penalty: float = 5.0,
) -> dict[str, float]:
    """Compute after-cost and diagnostic metrics for one chronological split."""

    import numpy as np

    if portfolio.empty:
        return empty_split_metrics()
    part = portfolio.loc[portfolio["DlyCalDt"].between(start, end)].copy()
    if part.empty:
        return empty_split_metrics()

    ann = 252.0
    rets = part.set_index("DlyCalDt")["net_return"]
    gross = part.set_index("DlyCalDt")["gross_return"]
    market = part.set_index("DlyCalDt")["vwretd"]
    vol = rets.std(ddof=1)
    gross_vol = gross.std(ddof=1)
    sharpe = float(rets.mean() / vol * math.sqrt(ann)) if vol and vol > 0 else float("nan")
    turnover = float(part["turnover"].mean())
    max_missing = float(part["missing_held_weight"].max())
    return {
        "annualized_return": float(rets.mean() * ann),
        "annualized_volatility": float(vol * math.sqrt(ann)) if np.isfinite(vol) else float("nan"),
        "sharpe": sharpe,
        "gross_annualized_return": float(gross.mean() * ann),
        "gross_sharpe": (
            float(gross.mean() / gross_vol * math.sqrt(ann))
            if gross_vol and gross_vol > 0
            else float("nan")
        ),
        "max_drawdown": max_drawdown(rets),
        "turnover": turnover,
        "hit_rate": float((rets > 0).mean()),
        "beta_to_vwretd": beta_to_market(rets, market),
        "mean_daily_n_names": float(part["n_names"].mean()),
        "mean_missing_held_weight": float(part["missing_held_weight"].mean()),
        "max_missing_held_weight": max_missing,
        "max_weight": float(part["max_weight"].max()),
        "turnover_aware_score": turnover_aware_score(
            sharpe=sharpe,
            turnover=turnover,
            max_missing_held_weight=max_missing,
            turnover_penalty=turnover_penalty,
            missing_weight_penalty=missing_weight_penalty,
        ),
    }


def build_forward_returns(panel: Any, contract: Any) -> Any:
    """Attach one-trading-day-forward returns under the frozen daily-stock contract."""

    import pandas as pd

    data = panel.sort_values([contract.security_id, contract.date]).copy()
    trading_dates = pd.Index(data[contract.date].drop_duplicates().sort_values())
    next_date_map = pd.Series(trading_dates[1:].to_numpy(), index=trading_dates[:-1])
    data["next_market_date"] = data[contract.date].map(next_date_map)
    grouped = data.groupby(contract.security_id, sort=False)
    data["fwd_ret"] = grouped[contract.ex_dividend_return].shift(-1)
    data["fwd_date"] = grouped[contract.date].shift(-1)
    data["fwd_vwretd"] = grouped[contract.benchmark_return_primary].shift(-1)
    data["one_day_forward"] = data["fwd_date"].eq(data["next_market_date"])
    return data


def portfolio_from_weights(panel: Any, weights: Any, total_cost_bps: float, contract: Any) -> tuple[Any, Any]:
    """Convert signal-date weights into next-day portfolio returns and held positions."""

    import pandas as pd

    data = panel[
        [contract.date, contract.security_id, "fwd_ret", "fwd_date", "fwd_vwretd", "one_day_forward"]
    ].copy()
    data["weight"] = weights.reindex(data.index).fillna(0.0)
    data = data.loc[data["weight"].ne(0.0)].copy()
    if data.empty:
        return pd.DataFrame(
            columns=[
                "DlyCalDt",
                "signal_date",
                "gross_return",
                "net_return",
                "turnover",
                "n_names",
                "missing_held_weight",
                "max_weight",
                "vwretd",
            ]
        ), data

    cost_rate = total_cost_bps / 10000.0
    rows: list[dict[str, Any]] = []
    prev_weights = None
    for signal_date, group in data.groupby(contract.date, sort=True):
        w = group.set_index(contract.security_id)["weight"]
        if prev_weights is None:
            turnover = float(w.abs().sum())
        else:
            combined = w.index.union(prev_weights.index)
            turnover = float(
                (
                    w.reindex(combined, fill_value=0.0)
                    - prev_weights.reindex(combined, fill_value=0.0)
                )
                .abs()
                .sum()
            )
        prev_weights = w

        valid = group["one_day_forward"].fillna(False) & group["fwd_ret"].notna()
        missing_held_weight = float(group.loc[~valid, "weight"].abs().sum())
        available = group.loc[valid].copy()
        if available.empty:
            gross_return = float("nan")
            next_date = group["fwd_date"].dropna().min()
            market_return = float("nan")
        else:
            gross_return = float((available["weight"] * available["fwd_ret"]).sum())
            next_date = available["fwd_date"].iloc[0]
            market_return = float(available["fwd_vwretd"].iloc[0])
        rows.append(
            {
                "DlyCalDt": pd.Timestamp(next_date) if pd.notna(next_date) else pd.NaT,
                "signal_date": pd.Timestamp(signal_date),
                "gross_return": gross_return,
                "net_return": gross_return - turnover * cost_rate if math.isfinite(gross_return) else float("nan"),
                "turnover": turnover,
                "n_names": int(len(group)),
                "missing_held_weight": missing_held_weight,
                "max_weight": float(group["weight"].abs().max()),
                "vwretd": market_return,
            }
        )
    portfolio = pd.DataFrame(rows).dropna(subset=["DlyCalDt"]).sort_values("DlyCalDt")
    return portfolio, data


def scorecard_from_metrics(program_id: str, metrics: dict[str, dict[str, float]], splits: Any) -> Any:
    import pandas as pd

    rows = []
    split_dates = {split.name: split for split in splits}
    for split_name, values in metrics.items():
        split = split_dates.get(split_name)
        for metric, value in values.items():
            rows.append(
                {
                    "program_id": program_id,
                    "split": split_name,
                    "start_date": split.start.date().isoformat() if split else "",
                    "end_date": split.end.date().isoformat() if split else "",
                    "metric": metric,
                    "value": value,
                }
            )
    return pd.DataFrame(rows)


def cost_sensitivity_rows(
    portfolio: Any,
    costs: list[float],
    *,
    turnover_penalty: float,
    missing_weight_penalty: float,
) -> list[dict[str, float]]:
    rows = []
    for cost in costs:
        cost_portfolio = portfolio.copy()
        cost_portfolio["net_return"] = (
            cost_portfolio["gross_return"] - cost_portfolio["turnover"] * (cost / 10000.0)
        )
        cost_metrics = split_metrics(
            cost_portfolio,
            "all",
            cost_portfolio["DlyCalDt"].min(),
            cost_portfolio["DlyCalDt"].max(),
            turnover_penalty=turnover_penalty,
            missing_weight_penalty=missing_weight_penalty,
        )
        rows.append(
            {
                "total_cost_bps": cost,
                "annualized_return": cost_metrics["annualized_return"],
                "sharpe": cost_metrics["sharpe"],
                "turnover": cost_metrics["turnover"],
                "turnover_aware_score": cost_metrics["turnover_aware_score"],
            }
        )
    return rows


__all__ = [
    "build_forward_returns",
    "cost_sensitivity_rows",
    "empty_split_metrics",
    "portfolio_from_weights",
    "scorecard_from_metrics",
    "split_metrics",
    "turnover_aware_score",
]
