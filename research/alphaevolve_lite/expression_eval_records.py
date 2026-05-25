"""Shared record rendering for daily-stock expression evaluation artifacts."""

from __future__ import annotations

import math
from typing import Any


def finite_or_none(value: Any) -> float | None:
    """Return a finite float or ``None`` for artifact-safe gate checks."""

    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def ranking_row(result: dict[str, Any]) -> dict[str, Any]:
    """Render one compact row for expression ranking CSVs."""

    metrics = result.get("metrics", {})
    search = metrics.get("search_sample", {})
    in_sample = metrics.get("in_sample", {})
    out_sample = metrics.get("out_sample", {})
    coverage = result.get("portfolio_coverage", {})
    return {
        "expression_id": result.get("expression_id"),
        "record_type": result.get("record_type"),
        "parent_expression_id": result.get("parent_expression_id"),
        "turn": result.get("turn"),
        "title": result.get("title"),
        "status": result.get("status"),
        "failure_reason": result.get("failure_reason"),
        "near_duplicate": result.get("near_duplicate"),
        "similarity_to_parent": result.get("similarity_to_parent"),
        "max_similarity_to_prior": result.get("max_similarity_to_prior"),
        "search_sharpe": search.get("sharpe"),
        "search_turnover": search.get("turnover"),
        "search_turnover_aware_score": search.get("turnover_aware_score"),
        "search_max_missing_held_weight": search.get("max_missing_held_weight"),
        "search_max_weight": search.get("max_weight"),
        "search_max_abs_net_exposure": search.get("max_abs_net_exposure"),
        "in_sample_sharpe": in_sample.get("sharpe"),
        "in_sample_turnover_aware_score": in_sample.get("turnover_aware_score"),
        "out_sample_sharpe": out_sample.get("sharpe"),
        "out_sample_turnover_aware_score": out_sample.get("turnover_aware_score"),
        "portfolio_days": coverage.get("portfolio_days"),
        "portfolio_day_coverage": coverage.get("portfolio_day_coverage"),
        "portfolio_coverage_pass": coverage.get("portfolio_coverage_pass"),
    }


def scorecard_rows(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Flatten split metrics into a long scorecard table."""

    rows: list[dict[str, Any]] = []
    for result in results:
        for split_name, metrics in result.get("metrics", {}).items():
            if not isinstance(metrics, dict):
                continue
            for metric, value in metrics.items():
                rows.append(
                    {
                        "expression_id": result.get("expression_id"),
                        "parent_expression_id": result.get("parent_expression_id"),
                        "turn": result.get("turn"),
                        "title": result.get("title"),
                        "status": result.get("status"),
                        "split": split_name,
                        "metric": metric,
                        "value": value,
                    }
                )
    return rows


def expression_sample_hard_gates(
    metrics: dict[str, dict[str, float]],
    portfolio_coverage: dict[str, Any],
    *,
    max_weight: float,
    max_abs_net_exposure: float,
    max_missing_held_weight: float,
) -> dict[str, bool]:
    """Return the mechanical gates that define expression sample-pass status."""

    search = metrics.get("search_sample", {})
    observed_max_weight = finite_or_none(search.get("max_weight"))
    observed_net = finite_or_none(search.get("max_abs_net_exposure"))
    observed_missing = finite_or_none(search.get("max_missing_held_weight"))
    return {
        "portfolio_coverage_pass": bool(portfolio_coverage.get("portfolio_coverage_pass")),
        "max_weight_within_expression_limit": bool(
            observed_max_weight is not None and observed_max_weight <= max_weight + 1.0e-12
        ),
        "max_abs_net_exposure_within_expression_limit": bool(
            observed_net is not None and observed_net <= max_abs_net_exposure + 1.0e-12
        ),
        "missing_held_weight_within_sample_tolerance": bool(
            observed_missing is not None
            and observed_missing <= max_missing_held_weight + 1.0e-12
        ),
        "turnover_aware_score_reported": finite_or_none(search.get("turnover_aware_score")) is not None,
    }


def status_from_metrics(
    metrics: dict[str, dict[str, float]],
    portfolio_coverage: dict[str, Any],
    *,
    max_weight: float,
    max_abs_net_exposure: float,
    max_missing_held_weight: float,
) -> str:
    """Return the reviewed expression sample status for a metric bundle."""

    hard_gates = expression_sample_hard_gates(
        metrics,
        portfolio_coverage,
        max_weight=max_weight,
        max_abs_net_exposure=max_abs_net_exposure,
        max_missing_held_weight=max_missing_held_weight,
    )
    return "expression_sample_pass" if all(hard_gates.values()) else "expression_sample_review"


__all__ = [
    "expression_sample_hard_gates",
    "finite_or_none",
    "ranking_row",
    "scorecard_rows",
    "status_from_metrics",
]
