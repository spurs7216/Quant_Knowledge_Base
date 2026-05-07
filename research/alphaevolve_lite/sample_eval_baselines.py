"""Null-control baselines for remote sample evaluation."""

from __future__ import annotations

from typing import Any

from .sample_eval_metrics import portfolio_from_weights, split_metrics


def random_baseline_weights(panel: Any, reference_weights: Any, contract: Any, seed: int) -> Any:
    """Randomize held names while preserving the reference long/short counts by date."""

    import numpy as np
    import pandas as pd

    rng = np.random.default_rng(seed)
    weights = pd.Series(0.0, index=panel.index, dtype=float)
    reference = reference_weights.reindex(panel.index).fillna(0.0)
    for _, group in panel.groupby(contract.date, sort=True):
        ref = reference.loc[group.index]
        n_long = int((ref > 0.0).sum())
        n_short = int((ref < 0.0).sum())
        needed = n_long + n_short
        if n_long == 0 or n_short == 0 or len(group) < needed:
            continue
        chosen = rng.choice(group.index.to_numpy(), size=needed, replace=False)
        long_idx = chosen[:n_long]
        short_idx = chosen[n_long:]
        weights.loc[long_idx] = 0.5 / n_long
        weights.loc[short_idx] = -0.5 / n_short
    return weights.rename("random_weight")


def baseline_metrics_for_weights(
    *,
    label: str,
    panel: Any,
    weights: Any,
    contract: Any,
    validation_end: Any,
    total_cost_bps: float,
    visible_splits: Any,
    turnover_penalty: float,
    missing_weight_penalty: float,
) -> dict[str, Any]:
    portfolio, _ = portfolio_from_weights(panel, weights, total_cost_bps, contract)
    portfolio = portfolio.loc[portfolio["DlyCalDt"] <= validation_end].copy()
    metrics = {
        split.name: split_metrics(
            portfolio,
            split.name,
            split.start,
            split.end,
            turnover_penalty=turnover_penalty,
            missing_weight_penalty=missing_weight_penalty,
        )
        for split in visible_splits
    }
    if portfolio.empty:
        metrics["search_sample"] = split_metrics(
            portfolio,
            "search_sample",
            validation_end,
            validation_end,
            turnover_penalty=turnover_penalty,
            missing_weight_penalty=missing_weight_penalty,
        )
    else:
        metrics["search_sample"] = split_metrics(
            portfolio,
            "search_sample",
            portfolio["DlyCalDt"].min(),
            portfolio["DlyCalDt"].max(),
            turnover_penalty=turnover_penalty,
            missing_weight_penalty=missing_weight_penalty,
        )
    return {"label": label, "metrics": metrics}


def build_baseline_records(
    *,
    panel: Any,
    reference_weights: Any,
    contract: Any,
    validation_end: Any,
    total_cost_bps: float,
    visible_splits: Any,
    null_seeds: int,
    turnover_penalty: float,
    missing_weight_penalty: float,
) -> list[dict[str, Any]]:
    """Build sign-flip and matched-random baseline records."""

    records = [
        baseline_metrics_for_weights(
            label="sign_flip",
            panel=panel,
            weights=-reference_weights,
            contract=contract,
            validation_end=validation_end,
            total_cost_bps=total_cost_bps,
            visible_splits=visible_splits,
            turnover_penalty=turnover_penalty,
            missing_weight_penalty=missing_weight_penalty,
        )
    ]
    for seed in range(null_seeds):
        random_weights = random_baseline_weights(panel, reference_weights, contract, seed)
        records.append(
            baseline_metrics_for_weights(
                label=f"random_{seed}",
                panel=panel,
                weights=random_weights,
                contract=contract,
                validation_end=validation_end,
                total_cost_bps=total_cost_bps,
                visible_splits=visible_splits,
                turnover_penalty=turnover_penalty,
                missing_weight_penalty=missing_weight_penalty,
            )
        )
    return records


def flatten_baseline_rows(records: list[dict[str, Any]]) -> Any:
    import pandas as pd

    rows = []
    for record in records:
        for split, metrics in record["metrics"].items():
            for metric, value in metrics.items():
                rows.append(
                    {
                        "baseline": record["label"],
                        "split": split,
                        "metric": metric,
                        "value": value,
                    }
                )
    return pd.DataFrame(rows)


def summarize_baselines(baseline_rows: Any, seed_metrics: dict[str, dict[str, float]]) -> dict[str, Any]:
    if baseline_rows.empty:
        return {}
    summary: dict[str, Any] = {}
    for metric in ["sharpe", "annualized_return", "turnover", "turnover_aware_score"]:
        part = baseline_rows[
            (baseline_rows["split"] == "search_sample")
            & (baseline_rows["metric"] == metric)
            & (baseline_rows["baseline"].str.startswith("random_"))
        ]["value"].dropna()
        if len(part):
            summary[f"random_search_sample_{metric}"] = {
                "count": int(len(part)),
                "mean": float(part.mean()),
                "median": float(part.median()),
                "min": float(part.min()),
                "max": float(part.max()),
                "seed_value": seed_metrics["search_sample"].get(metric),
            }
    sign_flip = baseline_rows[
        (baseline_rows["split"] == "search_sample")
        & (baseline_rows["baseline"] == "sign_flip")
        & (baseline_rows["metric"].isin(["sharpe", "annualized_return", "turnover_aware_score"]))
    ]
    if not sign_flip.empty:
        summary["sign_flip_search_sample"] = {
            str(row["metric"]): float(row["value"]) for _, row in sign_flip.iterrows()
        }
    return summary


__all__ = [
    "baseline_metrics_for_weights",
    "build_baseline_records",
    "flatten_baseline_rows",
    "random_baseline_weights",
    "summarize_baselines",
]
