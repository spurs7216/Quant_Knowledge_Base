"""Artifact and summary helpers for controller-static child batches."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .artifact_io import clean_json, write_json


SAMPLE_EVAL_ELIGIBILITY_VERSION = "sample_eval_candidate_eligibility_v1"
KNOWN_BAD_ATTEMPT017_SIGNAL_FAMILIES = {
    "bounded_tanh_dampening",
    "clipped_magnitude_dampening",
}


def _as_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def write_messages(path: Path, title: str, messages: dict[str, str]) -> None:
    """Write prompt messages as paired JSON and Markdown artifacts."""

    write_json(path.with_suffix(".json"), messages)
    path.with_suffix(".md").write_text(
        "\n".join(
            [
                f"# {title}",
                "",
                "## System",
                "",
                "```text",
                messages["system"],
                "```",
                "",
                "## User",
                "",
                "```text",
                messages["user"],
                "```",
                "",
            ]
        ),
        encoding="utf-8",
    )


def sample_eval_eligibility(attempt: dict[str, Any]) -> dict[str, Any]:
    """Return deterministic sample-eval eligibility for one controller attempt.

    This is not a promotion decision. It prevents controller-static passes from
    being mistaken for data-backed evaluation candidates when they are off-target,
    known-bad focused-repair families, or absorbed before final weights.
    """

    reasons: list[str] = []
    if attempt.get("decision") != "pass":
        reasons.append("not_controller_pass")
    if not attempt.get("child_program_path"):
        reasons.append("no_child_program")
    if attempt.get("target_intent_match") is not True:
        reasons.append("target_intent_not_matched")

    patch_intent = str(attempt.get("patch_intent") or "")
    target_surface = str(attempt.get("target_surface") or "")
    if target_surface == "signal" and patch_intent in KNOWN_BAD_ATTEMPT017_SIGNAL_FAMILIES:
        reasons.append("known_bad_attempt017_signal_dampening_family")

    delta = attempt.get("behavior_delta_metrics", {}) or {}
    weight_delta = _as_float(delta.get("weight_max_abs_delta"))
    weight_changed_fraction = _as_float(delta.get("weight_changed_fraction"))
    if (weight_delta or 0.0) <= 1e-12 and (weight_changed_fraction or 0.0) <= 0.0:
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

    return {
        "sample_eval_eligibility_version": SAMPLE_EVAL_ELIGIBILITY_VERSION,
        "sample_eval_eligible": not reasons,
        "sample_eval_eligibility_reasons": reasons,
    }


def summarize_attempts(attempts: list[dict[str, Any]]) -> dict[str, Any]:
    """Compute controller batch summary metrics from attempt records."""

    total = len(attempts)

    def final_rate(gate: str) -> float:
        if total == 0:
            return 0.0
        return sum(1 for item in attempts if item.get("hard_gates", {}).get(gate)) / total

    def initial_rate(gate: str) -> float:
        if total == 0:
            return 0.0
        return sum(
            1
            for item in attempts
            if item.get("initial_hard_gates", item.get("hard_gates", {})).get(gate)
        ) / total

    def as_float(value: Any) -> float:
        if value is None:
            return 0.0
        return float(value)

    passed = [item for item in attempts if item.get("decision") == "pass"]
    repair_attempts = [item for item in attempts if item.get("repair_attempted")]
    repair_successes = [item for item in repair_attempts if item.get("repair_succeeded")]
    empty_retries = [item for item in attempts if item.get("empty_retry_count", 0) > 0]
    empty_retry_successes = [item for item in empty_retries if item.get("empty_retry_succeeded")]
    duplicate_retries = [item for item in attempts if item.get("duplicate_retry_attempted")]
    duplicate_retry_successes = [item for item in duplicate_retries if item.get("duplicate_retry_succeeded")]
    map_cells = {
        item.get("map_cell_key")
        for item in attempts
        if item.get("decision") == "pass" and item.get("map_cell_key")
    }
    target_intent_matches = [
        item for item in passed if item.get("target_intent_match") is not False
    ]
    sample_eval_eligible = [
        item for item in attempts if sample_eval_eligibility(item)["sample_eval_eligible"]
    ]
    reasoning_only_empty = [
        item
        for item in attempts
        if item.get("initial_response_content_length", 0) == 0
        and item.get("initial_response_reasoning_length", 0) > 0
    ]
    controller_search_scores = [as_float(item.get("controller_search_score")) for item in attempts]
    lazy_penalty_scores = [as_float(item.get("lazy_penalty_score")) for item in attempts]
    return {
        "attempt_count": total,
        "pass_count": len(passed),
        "controller_search_score_sum": sum(controller_search_scores),
        "controller_search_score_mean": (
            sum(controller_search_scores) / len(controller_search_scores) if controller_search_scores else 0.0
        ),
        "controller_search_score_best": max(controller_search_scores or [0.0]),
        "lazy_penalty_score_sum": sum(lazy_penalty_scores),
        "lazy_penalty_attempt_count": sum(1 for score in lazy_penalty_scores if score < 0.0),
        "raw_parse_pass_rate": initial_rate("parse_search_replace"),
        "repair_attempt_rate": len(repair_attempts) / total if total else 0.0,
        "repair_success_rate": len(repair_successes) / len(repair_attempts) if repair_attempts else 0.0,
        "empty_retry_rate": len(empty_retries) / total if total else 0.0,
        "empty_retry_success_rate": len(empty_retry_successes) / len(empty_retries) if empty_retries else 0.0,
        "reasoning_only_empty_count": len(reasoning_only_empty),
        "max_initial_response_reasoning_length": max(
            [int(item.get("initial_response_reasoning_length", 0)) for item in attempts] or [0]
        ),
        "exact_search_match_rate": final_rate("exact_search_match"),
        "evolve_block_safe_rate": final_rate("evolve_block_safe"),
        "apply_pass_rate": final_rate("apply_patch"),
        "compile_pass_rate": final_rate("compile_pass"),
        "vector_smoke_pass_rate": final_rate("vector_smoke_pass"),
        "portfolio_semantic_pass_rate": final_rate("portfolio_semantic_pass"),
        "behavior_delta_pass_rate": final_rate("behavior_delta_pass"),
        "unique_child_pass_rate": final_rate("unique_child"),
        "target_intent_match_rate": (
            len(target_intent_matches) / len(passed) if passed else 0.0
        ),
        "target_intent_mismatch_pass_count": len(passed) - len(target_intent_matches),
        "sample_eval_eligibility_version": SAMPLE_EVAL_ELIGIBILITY_VERSION,
        "sample_eval_candidate_count": len(sample_eval_eligible),
        "sample_eval_candidate_attempts": [item.get("attempt") for item in sample_eval_eligible],
        "sample_eval_candidate_program_ids": [item.get("program_id") for item in sample_eval_eligible],
        "db_insert_pass_rate": sum(1 for item in attempts if item.get("db_inserted")) / total if total else 0.0,
        "duplicate_child_count": sum(1 for item in attempts if item.get("failure_category") == "duplicate_child"),
        "duplicate_patch_fingerprint_count": sum(
            1 for item in attempts if item.get("failure_category") == "duplicate_patch_fingerprint"
        ),
        "near_duplicate_patch_count": sum(
            1 for item in attempts if item.get("failure_category") == "near_duplicate_patch"
        ),
        "behavioral_noop_count": sum(
            1 for item in attempts if item.get("failure_category") == "behavioral_noop"
        ),
        "duplicate_retry_attempt_rate": len(duplicate_retries) / total if total else 0.0,
        "duplicate_retry_success_rate": (
            len(duplicate_retry_successes) / len(duplicate_retries) if duplicate_retries else 0.0
        ),
        "map_cell_count": len(map_cells),
        "map_cell_duplicate_count": sum(1 for item in attempts if item.get("map_cell_already_occupied")),
        "failure_categories": {
            str(category): sum(1 for item in attempts if item.get("failure_category") == category)
            for category in sorted({item.get("failure_category") for item in attempts if item.get("failure_category")})
        },
    }


def write_summary_markdown(path: Path, summary: dict[str, Any]) -> None:
    """Write the human-readable controller batch summary artifact."""

    lines = [
        "# Controller Batch Summary",
        "",
        f"- attempt_count: `{summary['attempt_count']}`",
        f"- pass_count: `{summary['pass_count']}`",
        f"- controller_search_score_sum: `{summary['controller_search_score_sum']}`",
        f"- controller_search_score_mean: `{summary['controller_search_score_mean']}`",
        f"- controller_search_score_best: `{summary['controller_search_score_best']}`",
        f"- lazy_penalty_score_sum: `{summary['lazy_penalty_score_sum']}`",
        f"- lazy_penalty_attempt_count: `{summary['lazy_penalty_attempt_count']}`",
        f"- raw_parse_pass_rate: `{summary['raw_parse_pass_rate']}`",
        f"- repair_attempt_rate: `{summary['repair_attempt_rate']}`",
        f"- repair_success_rate: `{summary['repair_success_rate']}`",
        f"- empty_retry_rate: `{summary['empty_retry_rate']}`",
        f"- empty_retry_success_rate: `{summary['empty_retry_success_rate']}`",
        f"- reasoning_only_empty_count: `{summary['reasoning_only_empty_count']}`",
        f"- max_initial_response_reasoning_length: `{summary['max_initial_response_reasoning_length']}`",
        f"- exact_search_match_rate: `{summary['exact_search_match_rate']}`",
        f"- evolve_block_safe_rate: `{summary['evolve_block_safe_rate']}`",
        f"- apply_pass_rate: `{summary['apply_pass_rate']}`",
        f"- compile_pass_rate: `{summary['compile_pass_rate']}`",
        f"- vector_smoke_pass_rate: `{summary['vector_smoke_pass_rate']}`",
        f"- portfolio_semantic_pass_rate: `{summary['portfolio_semantic_pass_rate']}`",
        f"- behavior_delta_pass_rate: `{summary['behavior_delta_pass_rate']}`",
        f"- unique_child_pass_rate: `{summary['unique_child_pass_rate']}`",
        f"- target_intent_match_rate: `{summary['target_intent_match_rate']}`",
        f"- target_intent_mismatch_pass_count: `{summary['target_intent_mismatch_pass_count']}`",
        f"- sample_eval_eligibility_version: `{summary['sample_eval_eligibility_version']}`",
        f"- sample_eval_candidate_count: `{summary['sample_eval_candidate_count']}`",
        f"- sample_eval_candidate_attempts: `{summary['sample_eval_candidate_attempts']}`",
        f"- sample_eval_candidate_program_ids: `{summary['sample_eval_candidate_program_ids']}`",
        f"- duplicate_child_count: `{summary['duplicate_child_count']}`",
        f"- duplicate_patch_fingerprint_count: `{summary['duplicate_patch_fingerprint_count']}`",
        f"- near_duplicate_patch_count: `{summary['near_duplicate_patch_count']}`",
        f"- behavioral_noop_count: `{summary['behavioral_noop_count']}`",
        f"- duplicate_retry_attempt_rate: `{summary['duplicate_retry_attempt_rate']}`",
        f"- duplicate_retry_success_rate: `{summary['duplicate_retry_success_rate']}`",
        f"- map_cell_count: `{summary['map_cell_count']}`",
        f"- map_cell_duplicate_count: `{summary['map_cell_duplicate_count']}`",
        f"- db_insert_pass_rate: `{summary['db_insert_pass_rate']}`",
    ]
    if "surface_schedule" in summary:
        lines.extend(
            [
                f"- surface_schedule: `{summary.get('surface_schedule')}`",
                f"- prior_summary_paths: `{summary.get('prior_summary_paths', [])}`",
                f"- prior_attempt_count: `{summary.get('prior_attempt_count', 0)}`",
                f"- prior_pass_count: `{summary.get('prior_pass_count', 0)}`",
                f"- prior_seen_child_hash_count: `{summary.get('prior_seen_child_hash_count', 0)}`",
                f"- population_policy_version: `{summary.get('population_policy_version')}`",
                f"- prompt_fitness_policy_version: `{summary.get('prompt_fitness_policy_version')}`",
                f"- near_duplicate_threshold: `{summary.get('near_duplicate_threshold')}`",
                f"- prompt_card_score_sums: `{summary.get('prompt_card_score_sums', {})}`",
                f"- prompt_card_lazy_penalty_sums: `{summary.get('prompt_card_lazy_penalty_sums', {})}`",
                f"- prompt_card_reroute_policy: `{summary.get('prompt_card_reroute_policy', {})}`",
            ]
        )
    if "reasoning_memory_enabled" in summary:
        lines.extend(
            [
                f"- reasoning_memory_enabled: `{summary['reasoning_memory_enabled']}`",
                f"- reasoning_memory_item_count: `{summary.get('reasoning_memory_item_count')}`",
                f"- retrieved_reasoning_memory_ids: `{summary.get('retrieved_reasoning_memory_ids')}`",
                f"- reasoning_memory_update_json: `{summary.get('reasoning_memory_update_json')}`",
                f"- reasoning_memory_update_log: `{summary.get('reasoning_memory_update_log')}`",
            ]
        )
    if "skill_library_enabled" in summary:
        lines.extend(
            [
                f"- skill_library_enabled: `{summary['skill_library_enabled']}`",
                f"- skill_library_item_count: `{summary.get('skill_library_item_count')}`",
                f"- retrieved_skill_ids: `{summary.get('retrieved_skill_ids')}`",
                f"- skill_update_json: `{summary.get('skill_update_json')}`",
                f"- skill_update_log: `{summary.get('skill_update_log')}`",
            ]
        )
    if "evaluator_diagnostic_report_json" in summary:
        lines.extend(
            [
                f"- evaluator_diagnostic_report_json: `{summary.get('evaluator_diagnostic_report_json')}`",
                f"- controller_diagnostic_report_json: `{summary.get('controller_diagnostic_report_json')}`",
            ]
        )
    lines.extend(["", "## Failure Categories", ""])
    if summary["failure_categories"]:
        for category, count in summary["failure_categories"].items():
            lines.append(f"- {category}: `{count}`")
    else:
        lines.append("- none")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


__all__ = [
    "SAMPLE_EVAL_ELIGIBILITY_VERSION",
    "clean_json",
    "sample_eval_eligibility",
    "summarize_attempts",
    "write_json",
    "write_messages",
    "write_summary_markdown",
]
