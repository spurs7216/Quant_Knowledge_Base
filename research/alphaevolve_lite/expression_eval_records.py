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
    success_flags = result.get("success_flags", {})
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
        "beats_parent_turnover_aware": success_flags.get("beats_parent_turnover_aware"),
        "beats_root_turnover_aware": success_flags.get("beats_root_turnover_aware"),
        "positive_search_after_cost": success_flags.get("positive_search_after_cost"),
        "positive_in_sample_after_cost": success_flags.get("positive_in_sample_after_cost"),
        "positive_out_sample_after_cost": success_flags.get("positive_out_sample_after_cost"),
        "positive_in_sample_sharpe": success_flags.get("positive_in_sample_sharpe"),
        "positive_out_sample_sharpe": success_flags.get("positive_out_sample_sharpe"),
        "broad_coverage": success_flags.get("broad_coverage"),
        "not_sparse": success_flags.get("not_sparse"),
        "not_near_duplicate": success_flags.get("not_near_duplicate"),
        "pass_at_t_basic": success_flags.get("pass_at_t_basic"),
        "economically_interesting": success_flags.get("economically_interesting"),
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


def expression_success_flags(
    result: dict[str, Any],
    *,
    parent_result: dict[str, Any] | None = None,
    root_result: dict[str, Any] | None = None,
    pass_margin: float = 0.0,
    broad_coverage_threshold: float = 0.80,
) -> dict[str, bool]:
    """Return explicit success flags so pass@T is not a vague parent-beat claim."""

    search_score = _metric(result, "search_sample", "turnover_aware_score")
    parent_score = _metric(parent_result, "search_sample", "turnover_aware_score")
    root_score = _metric(root_result, "search_sample", "turnover_aware_score")
    in_sample_score = _metric(result, "in_sample", "turnover_aware_score")
    out_sample_score = _metric(result, "out_sample", "turnover_aware_score")
    in_sample_sharpe = _metric(result, "in_sample", "sharpe")
    out_sample_sharpe = _metric(result, "out_sample", "sharpe")
    coverage = finite_or_none((result.get("portfolio_coverage") or {}).get("portfolio_day_coverage"))
    sample_pass = result.get("status") == "expression_sample_pass"
    broad_coverage = coverage is not None and coverage >= broad_coverage_threshold
    flags = {
        "sample_pass": bool(sample_pass),
        "beats_parent_turnover_aware": _gt_with_margin(search_score, parent_score, pass_margin),
        "beats_root_turnover_aware": _gt_with_margin(search_score, root_score, pass_margin),
        "positive_search_after_cost": bool(search_score is not None and search_score > 0.0),
        "positive_in_sample_after_cost": bool(in_sample_score is not None and in_sample_score > 0.0),
        "positive_out_sample_after_cost": bool(out_sample_score is not None and out_sample_score > 0.0),
        "positive_in_sample_sharpe": bool(in_sample_sharpe is not None and in_sample_sharpe > 0.0),
        "positive_out_sample_sharpe": bool(out_sample_sharpe is not None and out_sample_sharpe > 0.0),
        "broad_coverage": bool(broad_coverage),
        "not_sparse": bool(broad_coverage and sample_pass),
        "not_near_duplicate": not bool(result.get("near_duplicate")),
    }
    flags["pass_at_t_basic"] = bool(
        sample_pass
        and flags["beats_parent_turnover_aware"]
        and flags["positive_search_after_cost"]
        and flags["broad_coverage"]
        and flags["not_near_duplicate"]
    )
    flags["economically_interesting"] = bool(
        flags["pass_at_t_basic"]
        and flags["beats_root_turnover_aware"]
        and flags["positive_in_sample_after_cost"]
        and flags["positive_out_sample_after_cost"]
        and flags["positive_in_sample_sharpe"]
        and flags["positive_out_sample_sharpe"]
    )
    return flags


def success_flag_rows(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Flatten expression success flags for review artifacts."""

    rows: list[dict[str, Any]] = []
    for result in results:
        row = {
            "expression_id": result.get("expression_id"),
            "record_type": result.get("record_type"),
            "root_expression_id": result.get("root_expression_id"),
            "parent_expression_id": result.get("parent_expression_id"),
            "turn": result.get("turn"),
            "status": result.get("status"),
        }
        row.update(result.get("success_flags") or {})
        rows.append(row)
    return rows


def _metric(result: dict[str, Any] | None, split: str, metric: str) -> float | None:
    if not result:
        return None
    return finite_or_none(((result.get("metrics") or {}).get(split) or {}).get(metric))


def _gt_with_margin(value: float | None, reference: float | None, margin: float) -> bool:
    return bool(value is not None and reference is not None and value > reference + margin)


__all__ = [
    "expression_sample_hard_gates",
    "expression_success_flags",
    "finite_or_none",
    "ranking_row",
    "scorecard_rows",
    "status_from_metrics",
    "success_flag_rows",
]
