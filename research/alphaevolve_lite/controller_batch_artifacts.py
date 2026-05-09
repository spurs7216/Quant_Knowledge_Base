"""Artifact and summary helpers for controller-static child batches."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .artifact_io import clean_json, write_json


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
        "unique_child_pass_rate": final_rate("unique_child"),
        "db_insert_pass_rate": sum(1 for item in attempts if item.get("db_inserted")) / total if total else 0.0,
        "duplicate_child_count": sum(1 for item in attempts if item.get("failure_category") == "duplicate_child"),
        "duplicate_patch_fingerprint_count": sum(
            1 for item in attempts if item.get("failure_category") == "duplicate_patch_fingerprint"
        ),
        "near_duplicate_patch_count": sum(
            1 for item in attempts if item.get("failure_category") == "near_duplicate_patch"
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
        f"- unique_child_pass_rate: `{summary['unique_child_pass_rate']}`",
        f"- duplicate_child_count: `{summary['duplicate_child_count']}`",
        f"- duplicate_patch_fingerprint_count: `{summary['duplicate_patch_fingerprint_count']}`",
        f"- near_duplicate_patch_count: `{summary['near_duplicate_patch_count']}`",
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
    "clean_json",
    "summarize_attempts",
    "write_json",
    "write_messages",
    "write_summary_markdown",
]
