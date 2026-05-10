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
    "mean_daily_long_count": float("nan"),
    "mean_daily_short_count": float("nan"),
    "mean_missing_held_weight": float("nan"),
    "max_missing_held_weight": float("nan"),
    "max_weight": float("nan"),
    "mean_gross_exposure": float("nan"),
    "max_gross_exposure": float("nan"),
    "mean_abs_net_exposure": float("nan"),
    "max_abs_net_exposure": float("nan"),
    "mean_long_exposure": float("nan"),
    "mean_short_exposure": float("nan"),
    "turnover_aware_score": float("nan"),
}


REFERENCE_COMPARISON_METRICS = [
    "annualized_return",
    "annualized_volatility",
    "sharpe",
    "gross_annualized_return",
    "gross_sharpe",
    "max_drawdown",
    "turnover",
    "hit_rate",
    "beta_to_vwretd",
    "mean_daily_n_names",
    "mean_daily_long_count",
    "mean_daily_short_count",
    "mean_missing_held_weight",
    "max_missing_held_weight",
    "max_weight",
    "mean_gross_exposure",
    "max_gross_exposure",
    "mean_abs_net_exposure",
    "max_abs_net_exposure",
    "mean_long_exposure",
    "mean_short_exposure",
    "turnover_aware_score",
]


def empty_split_metrics() -> dict[str, float]:
    """Return a fresh all-NaN split metric record."""

    return dict(EMPTY_SPLIT_METRICS)


def _finite_float(value: Any) -> float | None:
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(result):
        return None
    return result


def compare_search_sample_to_reference(
    metrics: dict[str, dict[str, float]],
    reference_summary: dict[str, Any],
    *,
    tolerance: float,
    metric_names: list[str] | None = None,
) -> dict[str, Any]:
    """Compare current search-sample metrics with a seed or parent summary.

    This is a diagnostic for child evaluation. It catches no-op or
    functionally neutral children whose code differs but whose sample evidence
    is indistinguishable from the reference under the reported metrics.
    """

    if tolerance < 0.0:
        raise ValueError("reference comparison tolerance must be nonnegative")

    current = metrics.get("search_sample", {})
    reference = (
        reference_summary.get("metrics", {}).get("search_sample", {})
        if isinstance(reference_summary, dict)
        else {}
    )
    fields = metric_names or REFERENCE_COMPARISON_METRICS
    rows: dict[str, dict[str, Any]] = {}
    comparable_count = 0
    max_abs_delta = 0.0
    all_equivalent = True

    for name in fields:
        current_value = _finite_float(current.get(name))
        reference_value = _finite_float(reference.get(name))
        if current_value is None or reference_value is None:
            delta = None
            comparable = False
            equivalent = True
        else:
            comparable_count += 1
            delta = float(current_value - reference_value)
            max_abs_delta = max(max_abs_delta, abs(delta))
            comparable = True
            equivalent = abs(delta) <= tolerance
        all_equivalent = all_equivalent and equivalent
        rows[name] = {
            "current": current_value,
            "reference": reference_value,
            "delta": delta,
            "comparable": bool(comparable),
            "equivalent": bool(equivalent),
        }

    return {
        "reference_available": bool(reference),
        "metric_equivalent_to_reference": bool(reference and comparable_count and all_equivalent),
        "comparable_metric_count": int(comparable_count),
        "max_abs_metric_delta": float(max_abs_delta),
        "tolerance": float(tolerance),
        "metrics": rows,
    }


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
    net_exposure = part["net_exposure"] if "net_exposure" in part else None
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
        "mean_daily_long_count": float(part["long_count"].mean()),
        "mean_daily_short_count": float(part["short_count"].mean()),
        "mean_missing_held_weight": float(part["missing_held_weight"].mean()),
        "max_missing_held_weight": max_missing,
        "max_weight": float(part["max_weight"].max()),
        "mean_gross_exposure": float(part["gross_exposure"].mean()),
        "max_gross_exposure": float(part["gross_exposure"].max()),
        "mean_abs_net_exposure": float(net_exposure.abs().mean()) if net_exposure is not None else float("nan"),
        "max_abs_net_exposure": float(net_exposure.abs().max()) if net_exposure is not None else float("nan"),
        "mean_long_exposure": float(part["long_exposure"].mean()),
        "mean_short_exposure": float(part["short_exposure"].mean()),
        "turnover_aware_score": turnover_aware_score(
            sharpe=sharpe,
            turnover=turnover,
            max_missing_held_weight=max_missing,
            turnover_penalty=turnover_penalty,
            missing_weight_penalty=missing_weight_penalty,
        ),
    }


def portfolio_day_coverage_diagnostics(
    portfolio: Any,
    panel: Any,
    contract: Any,
    *,
    validation_end: Any,
    min_portfolio_days: int,
    min_portfolio_day_coverage: float,
) -> dict[str, Any]:
    """Measure whether a sample portfolio is active on enough eligible days.

    The sample evaluator is allowed to review sparse ideas, but `sample_pass`
    should mean a daily-stock child traded across a broad search sample rather
    than producing a high Sharpe from a few surviving dates.
    """

    import numpy as np

    if min_portfolio_days < 1:
        raise ValueError("min_portfolio_days must be positive")
    if not 0.0 < min_portfolio_day_coverage <= 1.0:
        raise ValueError("min_portfolio_day_coverage must be in (0, 1]")

    visible_panel = panel.loc[panel[contract.date] <= validation_end]
    visible_universe_days = int(visible_panel[contract.date].dropna().nunique())
    if portfolio.empty or "DlyCalDt" not in portfolio.columns:
        portfolio_days = 0
    else:
        portfolio_days = int(portfolio["DlyCalDt"].dropna().nunique())

    if visible_universe_days:
        portfolio_day_coverage = float(portfolio_days / visible_universe_days)
        coverage_required_days = int(np.ceil(min_portfolio_day_coverage * visible_universe_days))
        min_required_portfolio_days = min(int(min_portfolio_days), coverage_required_days)
    else:
        portfolio_day_coverage = float("nan")
        min_required_portfolio_days = int(min_portfolio_days)

    min_days_pass = portfolio_days >= min_required_portfolio_days
    coverage_pass = bool(
        visible_universe_days
        and np.isfinite(portfolio_day_coverage)
        and portfolio_day_coverage >= min_portfolio_day_coverage
    )
    return {
        "portfolio_days": portfolio_days,
        "visible_universe_days": visible_universe_days,
        "portfolio_day_coverage": portfolio_day_coverage,
        "min_portfolio_days": int(min_portfolio_days),
        "min_portfolio_day_coverage": float(min_portfolio_day_coverage),
        "min_required_portfolio_days": int(min_required_portfolio_days),
        "portfolio_min_days_pass": bool(min_days_pass),
        "portfolio_day_coverage_pass": bool(coverage_pass),
        "portfolio_coverage_pass": bool(min_days_pass and coverage_pass),
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
                "long_count",
                "short_count",
                "missing_held_weight",
                "max_weight",
                "gross_exposure",
                "net_exposure",
                "long_exposure",
                "short_exposure",
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

        long_weights = group.loc[group["weight"] > 0.0, "weight"]
        short_weights = group.loc[group["weight"] < 0.0, "weight"]
        gross_exposure = float(group["weight"].abs().sum())
        net_exposure = float(group["weight"].sum())
        long_exposure = float(long_weights.sum())
        short_exposure = float(-short_weights.sum())
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
                "long_count": int((group["weight"] > 0.0).sum()),
                "short_count": int((group["weight"] < 0.0).sum()),
                "missing_held_weight": missing_held_weight,
                "max_weight": float(group["weight"].abs().max()),
                "gross_exposure": gross_exposure,
                "net_exposure": net_exposure,
                "long_exposure": long_exposure,
                "short_exposure": short_exposure,
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
    "compare_search_sample_to_reference",
    "cost_sensitivity_rows",
    "empty_split_metrics",
    "portfolio_day_coverage_diagnostics",
    "portfolio_from_weights",
    "scorecard_from_metrics",
    "split_metrics",
    "turnover_aware_score",
]
