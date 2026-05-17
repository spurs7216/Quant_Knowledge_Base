"""Patch filtering and one-shot repair for controller-static child batches."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .controller_batch_artifacts import write_json, write_messages
from .controller_batch_mocks import mock_repair_patch
from .micro_filter import run_micro_filter
from .model_router import chat_completion
from .prompt_builder import build_patch_repair_prompt


REPAIRABLE_FAILURE_CATEGORIES = {
    "malformed_search_replace",
    "exact_search_not_found",
    "outside_evolve_block",
    "evolve_marker_error",
    "vector_smoke_failed",
    "portfolio_semantic_failed",
    "execution_effect_failed",
}


@dataclass(frozen=True)
class PatchFilterConfig:
    """Shared patch-filter settings for one controller batch."""

    parent_text: str
    no_repair: bool
    mock_patch_mode: str
    max_tokens: int


def filter_patch_with_optional_repair(
    *,
    config: PatchFilterConfig,
    attempt_dir: Path,
    generated_text: str,
    raw_output_path: Path,
    target_surface: str,
    attempt: int,
    artifact_prefix: str = "",
) -> dict[str, Any]:
    """Run micro-filter checks and optionally one bounded critic repair."""

    result = run_micro_filter(config.parent_text, generated_text, target_surface=target_surface)
    initial_result_record = result.to_record()
    write_json(attempt_dir / f"{artifact_prefix}micro_filter_initial_result.json", initial_result_record)

    repair_attempted = False
    repair_succeeded = False
    repair_record: dict[str, Any] | None = None
    final_diff_text = generated_text
    final_diff_path = raw_output_path
    repair_response_path: Path | None = None

    if (
        not config.no_repair
        and result.decision != "pass"
        and result.failure_category in REPAIRABLE_FAILURE_CATEGORIES
    ):
        repair_attempted = True
        repair_messages = build_patch_repair_prompt(
            parent_code=config.parent_text,
            unsafe_patch=generated_text,
            failure_reason=result.failure_reason or result.failure_category or "unknown",
            attempt_index=attempt,
            target_surface=target_surface,
        )
        write_messages(attempt_dir / f"{artifact_prefix}repair_prompt", "Patch Repair Prompt", repair_messages)
        if config.mock_patch_mode == "none":
            repair_record = chat_completion(
                role="critic_repair",
                system_prompt=repair_messages["system"],
                user_prompt=repair_messages["user"],
                temperature=0.0,
                max_tokens=config.max_tokens,
                verify=True,
            )
            repair_text = repair_record["content"]
        else:
            repair_text = mock_repair_patch(config.parent_text, config.mock_patch_mode)
            repair_record = {
                "role": "mock_repair",
                "served_model_name": "mock",
                "temperature": 0.0,
                "content": repair_text,
            }
        repair_output_path = attempt_dir / f"{artifact_prefix}repair_output.txt"
        repair_response_path = attempt_dir / f"{artifact_prefix}repair_response.json"
        repair_output_path.write_text(repair_text, encoding="utf-8")
        write_json(repair_response_path, repair_record)
        repair_result = run_micro_filter(config.parent_text, repair_text, target_surface=target_surface)
        write_json(
            attempt_dir / f"{artifact_prefix}repair_micro_filter_result.json",
            repair_result.to_record(),
        )
        if repair_result.decision == "pass":
            result = repair_result
            repair_succeeded = True
            final_diff_text = repair_text
            final_diff_path = repair_output_path

    return {
        "result": result,
        "initial_result_record": initial_result_record,
        "repair_attempted": repair_attempted,
        "repair_succeeded": repair_succeeded,
        "repair_response_path": repair_response_path,
        "final_diff_text": final_diff_text,
        "final_diff_path": final_diff_path,
        "repair_record": repair_record,
    }


__all__ = [
    "PatchFilterConfig",
    "REPAIRABLE_FAILURE_CATEGORIES",
    "filter_patch_with_optional_repair",
]
