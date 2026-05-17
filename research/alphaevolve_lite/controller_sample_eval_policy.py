"""Controller-to-sample-eval eligibility policy.

This module owns the decision "is a controller-static child worth one
expensive sample evaluation?"  It is deliberately stricter than controller
pass/fail: a child can be controller-safe and still be a poor use of remote
market-data evaluation budget.
"""

from __future__ import annotations

import math
from typing import Any

from .controller_execution_effect import has_final_weight_effect


SAMPLE_EVAL_ELIGIBILITY_VERSION = "sample_eval_candidate_eligibility_v2"

MAP_CELL_ELITE_SCORE_MARGIN = 1e-9
MAP_CELL_ELITE_BEHAVIOR_DELTA_MIN = 0.01

BEHAVIOR_DELTA_COMPARE_FIELDS = (
    "weight_max_abs_delta",
    "weight_changed_fraction",
    "ranked_signal_max_abs_delta",
    "ranked_signal_mean_abs_delta",
    "signal_max_abs_delta",
    "signal_mean_abs_delta",
    "max_abs_gross_exposure_delta",
    "mean_abs_gross_exposure_delta",
    "active_position_jaccard",
)


def sample_eval_eligibility(attempt: dict[str, Any]) -> dict[str, Any]:
    """Return deterministic sample-eval eligibility for one controller attempt.

    This is not a promotion decision. It prevents controller-static passes from
    being mistaken for data-backed evaluation candidates when they are off-target,
    absorbed before final weights, or already in an occupied MAP cell
    without evidence that they beat and differ from the cell elite.
    """

    reasons: list[str] = []
    if attempt.get("decision") != "pass":
        reasons.append("not_controller_pass")
    if not attempt.get("child_program_path"):
        reasons.append("no_child_program")
    if attempt.get("target_intent_match") is not True:
        reasons.append("target_intent_not_matched")

    delta = attempt.get("behavior_delta_metrics", {}) or {}
    if not has_final_weight_effect(delta):
        reasons.append("no_final_weight_delta")

    metrics = attempt.get("vector_smoke_metrics", {}) or {}
    active_days = _as_float(metrics.get("active_day_count"))
    min_long_count = _as_float(metrics.get("min_long_count_active_day"))
    min_short_count = _as_float(metrics.get("min_short_count_active_day"))
    if active_days is not None and active_days < 20.0:
        reasons.append("too_few_controller_active_days")
    if min_long_count is not None and min_long_count < 3.0:
        reasons.append("thin_controller_long_book")
    if min_short_count is not None and min_short_count < 3.0:
        reasons.append("thin_controller_short_book")

    if attempt.get("hard_gates", {}).get("no_forward_return_replacement") is False:
        reasons.append("forward_return_field_used")

    if attempt.get("map_cell_already_occupied") is True:
        reasons.extend(_occupied_map_cell_reasons(attempt))

    return {
        "sample_eval_eligibility_version": SAMPLE_EVAL_ELIGIBILITY_VERSION,
        "sample_eval_eligible": not reasons,
        "sample_eval_eligibility_reasons": reasons,
    }


def compare_to_map_cell_elite(
    attempt: dict[str, Any],
    elite_attempt: dict[str, Any] | None,
) -> dict[str, Any]:
    """Compare a controller pass with the existing MAP-cell elite record."""

    if not elite_attempt:
        return {
            "map_cell_elite_comparison_version": SAMPLE_EVAL_ELIGIBILITY_VERSION,
            "map_cell_elite_controller_search_score": None,
            "map_cell_elite_behavior_delta_max_abs_diff": None,
            "map_cell_elite_behavior_delta_compared_keys": [],
            "map_cell_elite_controller_score_beaten": False,
            "map_cell_elite_behavior_distinct": False,
        }

    attempt_score = _as_float(attempt.get("controller_search_score"))
    elite_score = _as_float(elite_attempt.get("controller_search_score"))
    score_beaten = (
        attempt_score is not None
        and elite_score is not None
        and attempt_score > elite_score + MAP_CELL_ELITE_SCORE_MARGIN
    )

    max_abs_diff = 0.0
    compared_keys: list[str] = []
    attempt_delta = attempt.get("behavior_delta_metrics", {}) or {}
    elite_delta = elite_attempt.get("behavior_delta_metrics", {}) or {}
    for key in BEHAVIOR_DELTA_COMPARE_FIELDS:
        current = _as_float(attempt_delta.get(key))
        elite = _as_float(elite_delta.get(key))
        if current is None or elite is None:
            continue
        compared_keys.append(key)
        max_abs_diff = max(max_abs_diff, abs(current - elite))
    behavior_distinct = bool(compared_keys) and max_abs_diff >= MAP_CELL_ELITE_BEHAVIOR_DELTA_MIN

    return {
        "map_cell_elite_comparison_version": SAMPLE_EVAL_ELIGIBILITY_VERSION,
        "map_cell_elite_program_id": elite_attempt.get("program_id"),
        "map_cell_elite_child_sha256": elite_attempt.get("child_sha256"),
        "map_cell_elite_patch_fingerprint": elite_attempt.get("patch_fingerprint"),
        "map_cell_elite_controller_search_score": elite_score,
        "map_cell_elite_behavior_delta_max_abs_diff": float(max_abs_diff) if compared_keys else None,
        "map_cell_elite_behavior_delta_compared_keys": compared_keys,
        "map_cell_elite_controller_score_beaten": bool(score_beaten),
        "map_cell_elite_behavior_distinct": bool(behavior_distinct),
    }


def controller_quality_score(attempt: dict[str, Any]) -> float:
    """Return a controller-local quality score used to choose MAP-cell elites."""

    score = _as_float(attempt.get("controller_search_score"))
    if score is not None:
        return score
    if attempt.get("decision") != "pass":
        return float("-inf")
    # Backward-compatible fallback for old summaries that predate score capture.
    penalty = 0.0
    if attempt.get("target_intent_match") is False:
        penalty -= 0.25
    if attempt.get("map_cell_already_occupied"):
        penalty -= 0.10
    return 1.0 + penalty


def _occupied_map_cell_reasons(attempt: dict[str, Any]) -> list[str]:
    elite_score = _as_float(attempt.get("map_cell_elite_controller_search_score"))
    behavior_diff = _as_float(attempt.get("map_cell_elite_behavior_delta_max_abs_diff"))
    if elite_score is None or behavior_diff is None:
        return ["occupied_map_cell_without_elite_comparison"]
    reasons: list[str] = []
    if attempt.get("map_cell_elite_controller_score_beaten") is not True:
        reasons.append("occupied_map_cell_does_not_beat_elite")
    if attempt.get("map_cell_elite_behavior_distinct") is not True:
        reasons.append("occupied_map_cell_not_behaviorally_distinct_from_elite")
    return reasons


def _as_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(result):
        return None
    return result


__all__ = [
    "SAMPLE_EVAL_ELIGIBILITY_VERSION",
    "compare_to_map_cell_elite",
    "controller_quality_score",
    "sample_eval_eligibility",
]
