"""Population policy for daily-stock expression evolution episodes."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from .expression_eval_records import finite_or_none
from .expression_evolution import ExpressionSpec


EXPRESSION_POPULATION_SCHEMA_VERSION = "expression_population_v1"


@dataclass(frozen=True)
class ExpressionParentChoice:
    """One deterministic parent choice for a root expression and turn."""

    root_expression_id: str
    turn: int
    selected_expression_id: str
    selected_expression: str
    parent_sampling_mode: str
    selection_reason: str
    eligible_parent_count: int
    candidate_expression_ids: tuple[str, ...]

    def to_record(self) -> dict[str, Any]:
        return {
            "schema_version": EXPRESSION_POPULATION_SCHEMA_VERSION,
            "root_expression_id": self.root_expression_id,
            "turn": int(self.turn),
            "selected_expression_id": self.selected_expression_id,
            "selected_expression": self.selected_expression,
            "parent_sampling_mode": self.parent_sampling_mode,
            "selection_reason": self.selection_reason,
            "eligible_parent_count": int(self.eligible_parent_count),
            "candidate_expression_ids": list(self.candidate_expression_ids),
        }


def build_population_record(
    result: Mapping[str, Any],
    *,
    root_expression_id: str,
    generation: int,
    split_id: str,
    root_score: float | None,
    branch_child_index: int,
    run_id: str | None = None,
    historical: bool = False,
    source_path: str | None = None,
) -> dict[str, Any]:
    """Build the search-facing ledger row for an expression result."""

    descriptors = expression_descriptors(result)
    score = expression_selection_score(result, root_score=root_score)
    status = str(result.get("status") or "")
    record_type = str(result.get("record_type") or "")
    parent_eligible = bool(
        record_type == "child"
        and status == "expression_sample_pass"
        and score is not None
    )
    search_score = _metric(result, "search_sample", "turnover_aware_score")
    root_delta = None if search_score is None or root_score is None else search_score - root_score
    return {
        "schema_version": EXPRESSION_POPULATION_SCHEMA_VERSION,
        "run_id": run_id,
        "historical": bool(historical),
        "source_path": source_path,
        "expression_id": result.get("expression_id"),
        "record_type": result.get("record_type"),
        "root_expression_id": root_expression_id,
        "parent_expression_id": result.get("parent_expression_id"),
        "generation": int(generation),
        "turn": result.get("turn"),
        "title": result.get("title"),
        "thesis": result.get("thesis"),
        "status": status,
        "failure_reason": result.get("failure_reason"),
        "expression": result.get("expression"),
        "mechanism": result.get("mechanism"),
        "expected_effect": result.get("expected_effect"),
        "tags": list(result.get("tags") or []),
        "metrics": result.get("metrics") or {},
        "portfolio_coverage": result.get("portfolio_coverage") or {},
        "hard_gates": result.get("hard_gates") or {},
        "signal_non_null_ratio": result.get("signal_non_null_ratio"),
        "position_rows": result.get("position_rows"),
        "selection_score": score,
        "root_score": root_score,
        "root_turnover_aware_delta": root_delta,
        "parent_sampling_eligible": parent_eligible,
        "descriptors": descriptors,
        "map_cell_key": map_cell_key(descriptors),
        "near_duplicate": bool(result.get("near_duplicate")),
        "similarity_to_parent": result.get("similarity_to_parent"),
        "max_similarity_to_prior": result.get("max_similarity_to_prior"),
        "validation_exposure": {
            "split_id": split_id,
            "development_os_used_for_feedback": True,
            "final_test_used": False,
            "branch_child_index": int(branch_child_index),
        },
    }


def expression_descriptors(result: Mapping[str, Any]) -> dict[str, Any]:
    """Return MAP-style descriptors for expression population accounting."""

    expression = str(result.get("expression") or "")
    return {
        "mechanism_family": mechanism_family(expression),
        "operator_set": operator_set(expression),
        "horizon_bucket": horizon_bucket(expression),
        "turnover_bucket": turnover_bucket(_metric(result, "search_sample", "turnover")),
        "cost_fragility_bucket": cost_fragility_bucket(result),
        "stability_bucket": stability_bucket(result),
        "coverage_bucket": coverage_bucket(
            finite_or_none((result.get("portfolio_coverage") or {}).get("portfolio_day_coverage"))
        ),
        "duplicate_bucket": "near_duplicate" if result.get("near_duplicate") else "not_near_duplicate",
    }


def map_cell_key(descriptors: Mapping[str, Any]) -> str:
    """Return the active MAP cell key for expression search."""

    fields = [
        "mechanism_family",
        "horizon_bucket",
        "turnover_bucket",
        "cost_fragility_bucket",
        "stability_bucket",
    ]
    return "|".join(f"{field}={descriptors.get(field)}" for field in fields)


def expression_selection_score(
    result: Mapping[str, Any],
    *,
    root_score: float | None,
) -> float | None:
    """Return a deterministic parent-sampling score, not a promotion score."""

    status = str(result.get("status") or "")
    if status in {"model_parse_error", "expression_duplicate"}:
        return -10.0

    search_score = _metric(result, "search_sample", "turnover_aware_score")
    if search_score is None:
        return -5.0 if status == "expression_error" else None

    score = search_score
    if status == "expression_sample_pass":
        score += 0.20
    elif status == "expression_sample_review":
        score -= 0.75
    else:
        score -= 2.0

    is_sharpe = _metric(result, "in_sample", "sharpe")
    os_sharpe = _metric(result, "out_sample", "sharpe")
    if is_sharpe is not None and os_sharpe is not None:
        if is_sharpe > 0.0 and os_sharpe > 0.0:
            score += 0.20
        elif is_sharpe * os_sharpe < 0.0:
            score -= 0.15

    turnover = _metric(result, "search_sample", "turnover")
    if turnover is not None:
        if turnover > 0.80:
            score -= 0.20
        elif turnover < 0.35:
            score += 0.05

    missing = _metric(result, "search_sample", "max_missing_held_weight")
    if missing is not None and missing > 0.05:
        score -= 0.50

    if result.get("near_duplicate"):
        score -= 0.25

    if root_score is not None:
        score += max(-0.25, min(0.25, search_score - root_score))
    return float(score)


def select_expression_parent(
    *,
    root: ExpressionSpec,
    turn: int,
    specs_by_id: Mapping[str, ExpressionSpec],
    population_records: Sequence[Mapping[str, Any]],
    parent_sampling_mode: str,
) -> ExpressionParentChoice:
    """Choose the expression parent for a generation turn."""

    if turn <= 1 or parent_sampling_mode == "fixed_seed":
        return ExpressionParentChoice(
            root_expression_id=root.expression_id,
            turn=turn,
            selected_expression_id=root.expression_id,
            selected_expression=root.expression,
            parent_sampling_mode=parent_sampling_mode,
            selection_reason="seed_parent_for_first_turn_or_fixed_mode",
            eligible_parent_count=0,
            candidate_expression_ids=(),
        )

    eligible = [
        record
        for record in population_records
        if record.get("root_expression_id") == root.expression_id
        and record.get("expression_id") in specs_by_id
        and record.get("record_type") == "child"
        and record.get("parent_sampling_eligible") is True
        and finite_or_none(record.get("selection_score")) is not None
    ]
    if not eligible:
        return ExpressionParentChoice(
            root_expression_id=root.expression_id,
            turn=turn,
            selected_expression_id=root.expression_id,
            selected_expression=root.expression,
            parent_sampling_mode=parent_sampling_mode,
            selection_reason="fallback_to_seed_no_eligible_child_survivor",
            eligible_parent_count=0,
            candidate_expression_ids=(),
        )

    if parent_sampling_mode == "population_mixed" and turn % 2 == 1:
        selected = max(
            eligible,
            key=lambda item: (
                novelty_score(item),
                finite_or_none(item.get("selection_score")) or float("-inf"),
                str(item.get("expression_id")),
            ),
        )
        reason = "most_novel_eligible_child_survivor"
    else:
        selected = max(
            eligible,
            key=lambda item: (
                finite_or_none(item.get("selection_score")) or float("-inf"),
                novelty_score(item),
                str(item.get("expression_id")),
            ),
        )
        reason = "best_scored_eligible_child_survivor"

    expression_id = str(selected.get("expression_id"))
    spec = specs_by_id[expression_id]
    return ExpressionParentChoice(
        root_expression_id=root.expression_id,
        turn=turn,
        selected_expression_id=expression_id,
        selected_expression=spec.expression,
        parent_sampling_mode=parent_sampling_mode,
        selection_reason=reason,
        eligible_parent_count=len(eligible),
        candidate_expression_ids=tuple(str(item.get("expression_id")) for item in eligible),
    )


def branch_stop_loss_diagnostics(
    *,
    root_expression_id: str,
    root_score: float | None,
    population_records: Sequence[Mapping[str, Any]],
    min_child_count: int,
    improvement_margin: float,
) -> dict[str, Any]:
    """Return branch diagnostics that prevent endless single-branch repair."""

    child_records = [
        record
        for record in population_records
        if record.get("root_expression_id") == root_expression_id
        and record.get("record_type") == "child"
    ]
    scores = [
        score
        for score in (finite_or_none(record.get("selection_score")) for record in child_records)
        if score is not None
    ]
    root_deltas = [
        delta
        for delta in (finite_or_none(record.get("root_turnover_aware_delta")) for record in child_records)
        if delta is not None
    ]
    best_score = max(scores) if scores else None
    best_delta = max(root_deltas) if root_deltas else None
    should_pause = bool(
        len(child_records) >= min_child_count
        and (
            best_delta is None
            or best_delta <= improvement_margin
        )
    )
    return {
        "schema_version": EXPRESSION_POPULATION_SCHEMA_VERSION,
        "root_expression_id": root_expression_id,
        "child_count": len(child_records),
        "eligible_child_parent_count": sum(
            bool(record.get("parent_sampling_eligible")) for record in child_records
        ),
        "root_score": root_score,
        "best_child_selection_score": best_score,
        "best_child_turnover_aware_delta": best_delta,
        "min_child_count": int(min_child_count),
        "improvement_margin": float(improvement_margin),
        "pause_branch_for_population_review": should_pause,
    }


def novelty_score(record: Mapping[str, Any]) -> float:
    """Return novelty as one minus max known structural similarity."""

    similarities = [
        finite_or_none(record.get("similarity_to_parent")),
        finite_or_none(record.get("max_similarity_to_prior")),
    ]
    finite = [value for value in similarities if value is not None]
    if not finite:
        return 0.0
    return float(max(0.0, 1.0 - max(finite)))


def mechanism_family(expression: str) -> str:
    text = expression.lower()
    if "industry_neutralize" in text:
        return "neutralization"
    if "rolling_beta" in text or "benchmark_return" in text:
        return "beta_or_benchmark_residual"
    if "dollar_volume" in text or "volume" in text:
        return "liquidity_or_volume"
    if "market_cap" in text or "shares_outstanding" in text or "price" in text:
        return "capacity_or_size"
    if "rolling_std" in text or "vol" in text:
        return "volatility_conditioned"
    if "rolling_sum(excess_ret, 60" in text or "rolling_sum(excess_ret, 40" in text:
        return "momentum_or_regime"
    if "-rolling_sum" in text or "-excess_ret" in text:
        return "reversal"
    return "mixed_or_other"


def operator_set(expression: str) -> list[str]:
    return sorted(set(re.findall(r"([A-Za-z_][A-Za-z0-9_]*)\s*\(", expression)))


def horizon_bucket(expression: str) -> str:
    windows = [int(item) for item in re.findall(r",\s*([0-9]+)\s*\)", expression)]
    if not windows:
        return "cross_sectional_or_one_day"
    max_window = max(windows)
    if max_window <= 5:
        return "short_1_5"
    if max_window <= 20:
        return "medium_6_20"
    if max_window <= 60:
        return "intermediate_21_60"
    return "long_61_plus"


def turnover_bucket(turnover: float | None) -> str:
    if turnover is None:
        return "unknown"
    if turnover < 0.25:
        return "very_low"
    if turnover < 0.50:
        return "low"
    if turnover < 0.80:
        return "medium"
    if turnover < 1.20:
        return "high"
    return "extreme"


def cost_fragility_bucket(result: Mapping[str, Any]) -> str:
    score = _metric(result, "search_sample", "turnover_aware_score")
    sharpe = _metric(result, "search_sample", "sharpe")
    if score is None or sharpe is None:
        return "unknown"
    drag = sharpe - score
    if score > 0.0 and drag < 0.25:
        return "robust"
    if score > 0.0:
        return "moderate"
    if sharpe > 0.0 and score <= 0.0:
        return "fragile"
    return "broken_or_negative"


def stability_bucket(result: Mapping[str, Any]) -> str:
    is_sharpe = _metric(result, "in_sample", "sharpe")
    os_sharpe = _metric(result, "out_sample", "sharpe")
    if is_sharpe is None or os_sharpe is None:
        return "unknown"
    if is_sharpe > 0.0 and os_sharpe > 0.0:
        return "both_positive"
    if is_sharpe <= 0.0 and os_sharpe <= 0.0:
        return "both_nonpositive"
    if is_sharpe > 0.0 and os_sharpe <= 0.0:
        return "is_positive_os_negative"
    return "is_negative_os_positive"


def coverage_bucket(portfolio_day_coverage: float | None) -> str:
    if portfolio_day_coverage is None:
        return "unknown"
    if portfolio_day_coverage >= 0.95:
        return "broad"
    if portfolio_day_coverage >= 0.80:
        return "adequate"
    return "sparse"


def _metric(result: Mapping[str, Any], split: str, metric: str) -> float | None:
    return finite_or_none(
        ((result.get("metrics") or {}).get(split) or {}).get(metric)
    )


__all__ = [
    "EXPRESSION_POPULATION_SCHEMA_VERSION",
    "ExpressionParentChoice",
    "branch_stop_loss_diagnostics",
    "build_population_record",
    "expression_descriptors",
    "expression_selection_score",
    "map_cell_key",
    "select_expression_parent",
]
