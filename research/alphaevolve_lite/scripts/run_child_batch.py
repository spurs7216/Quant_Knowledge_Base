"""Run a small remote Qwen child-generation controller dry run."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


DEFAULT_MAX_COMPLETION_TOKENS = 8192


def _ensure_repo_import() -> None:
    repo_root = Path(__file__).resolve().parents[3]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run controller-static child generation attempts.")
    parser.add_argument(
        "--program-path",
        default="research/alphaevolve_lite/seeds/kalman_reversal_seed.py",
    )
    parser.add_argument("--evaluator-summary", default="")
    parser.add_argument("--out-dir", default="artifacts/phase4_alphaevolve/controller_batch_001")
    parser.add_argument("--db-path", default="")
    parser.add_argument("--attempts", type=int, default=5)
    parser.add_argument("--model-role", default="fast_generator")
    parser.add_argument("--temperature-grid", default="0.0,0.2,0.5")
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=DEFAULT_MAX_COMPLETION_TOKENS,
        help=(
            "Maximum completion tokens requested from vLLM. The remote server's "
            "max-model-len must exceed prompt tokens plus this value."
        ),
    )
    parser.add_argument("--empty-retry-attempts", type=int, default=1)
    parser.add_argument(
        "--duplicate-retry-attempts",
        type=int,
        default=1,
        help="Retry once when a controller-pass child duplicates an earlier child or patch fingerprint.",
    )
    parser.add_argument(
        "--memory-path",
        default="artifacts/phase4_alphaevolve/reasoning_memory/memory_items.jsonl",
        help="JSONL reasoning-memory bank used for prompt cards.",
    )
    parser.add_argument("--memory-card-limit", type=int, default=3)
    parser.add_argument("--disable-reasoning-memory", action="store_true")
    parser.add_argument("--diagnostic-card-limit", type=int, default=4)
    parser.add_argument(
        "--skill-library-path",
        default="artifacts/phase4_alphaevolve/skill_library/skill_items.jsonl",
        help="JSONL explicit skill library used for prompt skill cards.",
    )
    parser.add_argument("--skill-card-limit", type=int, default=3)
    parser.add_argument("--disable-skill-library", action="store_true")
    parser.add_argument("--program-id-prefix", default="PROG-20260430-CHILD")
    parser.add_argument(
        "--mock-patch-mode",
        choices=["none", "sign_flip", "marker_oversize", "portfolio_long_only", "no_valid_patch"],
        default="none",
    )
    parser.add_argument("--no-repair", action="store_true", help="Disable one-shot critic repair.")
    return parser.parse_args()


def clean_json(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {str(k): clean_json(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [clean_json(v) for v in obj]
    if isinstance(obj, float):
        if obj != obj or obj in {float("inf"), float("-inf")}:
            return None
    return obj


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(clean_json(payload), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_messages(path: Path, title: str, messages: dict[str, str]) -> None:
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


def mock_patch(parent_text: str, mode: str, target_surface: str = "signal") -> str:
    if mode == "no_valid_patch":
        return "NO_VALID_PATCH"
    if mode == "sign_flip":
        search = "        signal = signal / rolling_vol.clip(lower=1e-4)\n"
        if search not in parent_text:
            raise RuntimeError("mock sign_flip SEARCH text not found")
        return (
            "<<<<<<< SEARCH\n"
            f"{search}"
            "=======\n"
            "        signal = -signal / rolling_vol.clip(lower=1e-4)\n"
            ">>>>>>> REPLACE\n"
        )
    if mode == "marker_oversize":
        search = (
            "    # EVOLVE-BLOCK-START: signal\n"
            "    q = float(cfg[\"kalman_q\"])\n"
            "    r = float(cfg[\"kalman_r\"])\n"
            "    min_history = int(cfg[\"min_history\"])\n"
        )
        if search not in parent_text:
            raise RuntimeError("mock marker_oversize SEARCH text not found")
        replace = search + "    # mock oversized patch touched marker lines\n"
        return f"<<<<<<< SEARCH\n{search}=======\n{replace}>>>>>>> REPLACE\n"
    if mode == "portfolio_long_only":
        search = (
            "        weights.loc[longs] = 0.5 * gross / len(longs)\n"
            "        weights.loc[shorts] = -0.5 * gross / len(shorts)\n"
        )
        if search not in parent_text:
            raise RuntimeError("mock portfolio_long_only SEARCH text not found")
        return (
            "<<<<<<< SEARCH\n"
            f"{search}"
            "=======\n"
            "        weights.loc[longs] = 0.5 * gross * valid.loc[longs, \"signal\"] / valid.loc[longs, \"signal\"].sum()\n"
            "        weights.loc[shorts] = -0.5 * gross * valid.loc[shorts, \"signal\"] / valid.loc[shorts, \"signal\"].abs().sum()\n"
            ">>>>>>> REPLACE\n"
        )
    raise RuntimeError(f"unknown mock patch mode: {mode}")


def mock_repair_patch(parent_text: str, mode: str) -> str:
    if mode == "marker_oversize":
        return mock_patch(parent_text, "sign_flip")
    return "NO_VALID_PATCH"


REPAIRABLE_FAILURE_CATEGORIES = {
    "malformed_search_replace",
    "exact_search_not_found",
    "outside_evolve_block",
    "evolve_marker_error",
    "vector_smoke_failed",
    "portfolio_semantic_failed",
}


def summarize_attempts(attempts: list[dict[str, Any]]) -> dict[str, Any]:
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
    return {
        "attempt_count": total,
        "pass_count": len(passed),
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
    lines = [
        "# Controller Batch Summary",
        "",
        f"- attempt_count: `{summary['attempt_count']}`",
        f"- pass_count: `{summary['pass_count']}`",
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
        f"- duplicate_retry_attempt_rate: `{summary['duplicate_retry_attempt_rate']}`",
        f"- duplicate_retry_success_rate: `{summary['duplicate_retry_success_rate']}`",
        f"- map_cell_count: `{summary['map_cell_count']}`",
        f"- map_cell_duplicate_count: `{summary['map_cell_duplicate_count']}`",
        f"- db_insert_pass_rate: `{summary['db_insert_pass_rate']}`",
    ]
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


def main() -> int:
    _ensure_repo_import()
    from research.alphaevolve_lite.diversity import (
        choose_diversity_target,
        patch_diversity_descriptor,
    )
    from research.alphaevolve_lite.diagnostic_analyzer import (
        build_controller_diagnostic_report,
        build_evaluator_diagnostic_report,
        render_diagnostic_cards,
        retrieve_diagnostic_cards,
        write_diagnostic_report,
    )
    from research.alphaevolve_lite.micro_filter import run_micro_filter
    from research.alphaevolve_lite.model_router import chat_completion
    from research.alphaevolve_lite.program_database import init_db, insert_program_record
    from research.alphaevolve_lite.prompt_builder import (
        build_child_generation_prompt,
        build_patch_repair_prompt,
        choose_target_surface,
        load_json_if_exists,
        write_prompt_artifact,
    )
    from research.alphaevolve_lite.reasoning_memory import (
        append_memory_update,
        bootstrap_default_memory_bank,
        build_controller_batch_memory_update,
        render_memory_cards,
        retrieve_memory_items,
        write_memory_update,
    )
    from research.alphaevolve_lite.skill_library import (
        append_skill_update,
        bootstrap_default_skill_library,
        build_controller_batch_skill_update,
        render_skill_cards,
        retrieve_skill_items,
        write_skill_update,
    )

    args = parse_args()
    if args.attempts <= 0:
        print("--attempts must be positive", file=sys.stderr)
        return 2

    program_path = Path(args.program_path)
    if not program_path.exists():
        print(f"program path does not exist: {program_path}", file=sys.stderr)
        return 2
    parent_text = program_path.read_text(encoding="utf-8")
    evaluator_summary = load_json_if_exists(args.evaluator_summary)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    evaluator_diagnostic_report = build_evaluator_diagnostic_report(
        evaluator_summary,
        source_path=args.evaluator_summary or None,
    )
    evaluator_diagnostic_paths = write_diagnostic_report(
        out_dir,
        "evaluator_diagnostic_report",
        evaluator_diagnostic_report,
    )
    temperatures = [float(item.strip()) for item in args.temperature_grid.split(",") if item.strip()]
    if not temperatures:
        temperatures = [0.2]
    if args.db_path:
        init_db(args.db_path)
    memory_path = None if args.disable_reasoning_memory else Path(args.memory_path)
    reasoning_memory_items: list[dict[str, Any]] = []
    retrieved_memory_ids_seen: set[str] = set()
    if memory_path is not None:
        reasoning_memory_items = bootstrap_default_memory_bank(memory_path)
        write_json(
            out_dir / "reasoning_memory_loaded.json",
            {
                "memory_path": str(memory_path),
                "memory_item_count": len(reasoning_memory_items),
                "active_memory_item_count": sum(
                    1 for item in reasoning_memory_items if item.get("status") == "active"
                ),
                "memory_item_ids": [item.get("memory_item_id") for item in reasoning_memory_items],
            },
        )
    skill_library_path = None if args.disable_skill_library else Path(args.skill_library_path)
    skill_items: list[dict[str, Any]] = []
    retrieved_skill_ids_seen: set[str] = set()
    if skill_library_path is not None:
        skill_items = bootstrap_default_skill_library(skill_library_path)
        write_json(
            out_dir / "skill_library_loaded.json",
            {
                "skill_library_path": str(skill_library_path),
                "skill_item_count": len(skill_items),
                "active_skill_item_count": sum(1 for item in skill_items if item.get("status") == "active"),
                "skill_ids": [item.get("skill_id") for item in skill_items],
            },
        )

    def filter_patch_with_optional_repair(
        *,
        attempt_dir: Path,
        generated_text: str,
        raw_output_path: Path,
        target_surface: str,
        attempt: int,
        artifact_prefix: str = "",
    ) -> dict[str, Any]:
        result = run_micro_filter(parent_text, generated_text, target_surface=target_surface)
        initial_result_record = result.to_record()
        write_json(attempt_dir / f"{artifact_prefix}micro_filter_initial_result.json", initial_result_record)

        repair_attempted = False
        repair_succeeded = False
        repair_record: dict[str, Any] | None = None
        final_diff_text = generated_text
        final_diff_path = raw_output_path
        repair_response_path: Path | None = None

        if (
            not args.no_repair
            and result.decision != "pass"
            and result.failure_category in REPAIRABLE_FAILURE_CATEGORIES
        ):
            repair_attempted = True
            repair_messages = build_patch_repair_prompt(
                parent_code=parent_text,
                unsafe_patch=generated_text,
                failure_reason=result.failure_reason or result.failure_category or "unknown",
                attempt_index=attempt,
                target_surface=target_surface,
            )
            write_messages(attempt_dir / f"{artifact_prefix}repair_prompt", "Patch Repair Prompt", repair_messages)
            if args.mock_patch_mode == "none":
                repair_record = chat_completion(
                    role="critic_repair",
                    system_prompt=repair_messages["system"],
                    user_prompt=repair_messages["user"],
                    temperature=0.0,
                    max_tokens=args.max_tokens,
                    verify=True,
                )
                repair_text = repair_record["content"]
            else:
                repair_text = mock_repair_patch(parent_text, args.mock_patch_mode)
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
            repair_result = run_micro_filter(parent_text, repair_text, target_surface=target_surface)
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

    def describe_pass_candidate(
        *,
        result: Any,
        final_diff_text: str,
        target_surface: str,
    ) -> dict[str, Any]:
        child_hash = None
        if result.child_text is not None:
            child_hash = hashlib.sha256(result.child_text.encode("utf-8")).hexdigest()
        if result.decision != "pass":
            return {
                "child_hash": child_hash,
                "diversity_descriptor": {},
                "patch_fingerprint": None,
                "map_cell_key": None,
            }
        diversity_descriptor = patch_diversity_descriptor(
            final_diff_text,
            target_surface,
            result.vector_smoke_metrics,
        )
        return {
            "child_hash": child_hash,
            "diversity_descriptor": diversity_descriptor,
            "patch_fingerprint": diversity_descriptor.get("patch_fingerprint"),
            "map_cell_key": diversity_descriptor.get("map_cell_key"),
        }

    attempt_records: list[dict[str, Any]] = []
    seen_child_hashes: dict[str, str] = {}
    seen_patch_fingerprints: dict[str, str] = {}
    occupied_map_cells: dict[str, str] = {}
    occupied_target_labels_by_surface: dict[str, set[str]] = {}
    accepted_patches_by_surface: dict[str, list[str]] = {}
    for attempt in range(args.attempts):
        attempt_dir = out_dir / f"attempt_{attempt:03d}"
        attempt_dir.mkdir(parents=True, exist_ok=True)
        temperature = temperatures[attempt % len(temperatures)]
        target_surface = choose_target_surface(attempt)
        diversity_target = choose_diversity_target(
            target_surface,
            attempt,
            occupied_labels=occupied_target_labels_by_surface.get(target_surface, set()),
        )
        occupied_same_surface_cells = [
            cell for cell in sorted(occupied_map_cells) if f"surface={target_surface}" in cell
        ]
        memory_query = " ".join(
            [
                target_surface,
                diversity_target.cell_label if diversity_target else "",
                diversity_target.instruction if diversity_target else "",
            ]
        )
        retrieved_memory_items = retrieve_memory_items(
            reasoning_memory_items,
            source_stage="controller_static",
            target_surface=target_surface,
            data_stage="stage_0_daily_stock",
            query=memory_query,
            limit=max(0, args.memory_card_limit),
        )
        retrieved_memory_item_ids = [
            str(item.get("memory_item_id")) for item in retrieved_memory_items if item.get("memory_item_id")
        ]
        retrieved_memory_ids_seen.update(retrieved_memory_item_ids)
        reasoning_memory_text = render_memory_cards(retrieved_memory_items)
        diagnostic_cards = retrieve_diagnostic_cards(
            evaluator_diagnostic_report.get("diagnostic_cards", []),
            target_surface=target_surface,
            limit=max(0, args.diagnostic_card_limit),
        )
        diagnostic_text = render_diagnostic_cards(diagnostic_cards)
        diagnostic_card_ids = [
            str(card.get("diagnostic_id")) for card in diagnostic_cards if card.get("diagnostic_id")
        ]
        skill_query = " ".join(
            [
                memory_query,
                diagnostic_text,
                " ".join(diagnostic_card_ids),
            ]
        )
        retrieved_skill_items = retrieve_skill_items(
            skill_items,
            source_stage="controller_static",
            target_surface=target_surface,
            data_stage="stage_0_daily_stock",
            query=skill_query,
            limit=max(0, args.skill_card_limit),
        )
        retrieved_skill_ids = [
            str(item.get("skill_id")) for item in retrieved_skill_items if item.get("skill_id")
        ]
        retrieved_skill_ids_seen.update(retrieved_skill_ids)
        skill_text = render_skill_cards(retrieved_skill_items)
        messages = build_child_generation_prompt(
            parent_code=parent_text,
            evaluator_summary=evaluator_summary,
            attempt_index=attempt,
            target_surface=target_surface,
            previous_accepted_patches=accepted_patches_by_surface.get(target_surface, [])[-3:],
            diversity_target=diversity_target,
            occupied_map_cells=occupied_same_surface_cells,
            reasoning_memory_text=reasoning_memory_text,
            diagnostic_text=diagnostic_text,
            skill_text=skill_text,
        )
        write_prompt_artifact(attempt_dir, messages)

        response_record: dict[str, Any]
        if args.mock_patch_mode == "none":
            response_record = chat_completion(
                role=args.model_role,
                system_prompt=messages["system"],
                user_prompt=messages["user"],
                temperature=temperature,
                max_tokens=args.max_tokens,
                verify=True,
            )
            generated_text = response_record["content"]
        else:
            generated_text = mock_patch(parent_text, args.mock_patch_mode, target_surface=target_surface)
            response_record = {
                "role": "mock",
                "served_model_name": "mock",
                "temperature": temperature,
                "content": generated_text,
            }

        (attempt_dir / "raw_output.txt").write_text(generated_text, encoding="utf-8")
        write_json(attempt_dir / "model_response.json", response_record)
        initial_response_record = dict(response_record)

        empty_retry_count = 0
        empty_retry_succeeded = False
        while (
            args.mock_patch_mode == "none"
            and not generated_text.strip()
            and empty_retry_count < max(0, args.empty_retry_attempts)
        ):
            empty_retry_count += 1
            retry_messages = {
                "system": messages["system"]
                + "\nYou must put the SEARCH/REPLACE patch in message.content. Do not use reasoning output.",
                "user": messages["user"]
                + "\n\nPrevious response had empty final content. Retry once with only the final SEARCH/REPLACE patch in message.content.",
            }
            write_messages(attempt_dir / f"empty_retry_{empty_retry_count}_prompt", "Empty Output Retry Prompt", retry_messages)
            retry_record = chat_completion(
                role=args.model_role,
                system_prompt=retry_messages["system"],
                user_prompt=retry_messages["user"],
                temperature=0.0,
                max_tokens=args.max_tokens,
                verify=True,
            )
            retry_text = retry_record["content"]
            write_json(attempt_dir / f"empty_retry_{empty_retry_count}_response.json", retry_record)
            (attempt_dir / f"empty_retry_{empty_retry_count}_output.txt").write_text(retry_text, encoding="utf-8")
            if retry_text.strip():
                generated_text = retry_text
                response_record = retry_record
                empty_retry_succeeded = True
                (attempt_dir / "raw_output.txt").write_text(generated_text, encoding="utf-8")
                write_json(attempt_dir / "model_response.json", response_record)
                break

        filter_record = filter_patch_with_optional_repair(
            attempt_dir=attempt_dir,
            generated_text=generated_text,
            raw_output_path=attempt_dir / "raw_output.txt",
            target_surface=target_surface,
            attempt=attempt,
        )
        result = filter_record["result"]
        initial_result_record = filter_record["initial_result_record"]
        repair_attempted = bool(filter_record["repair_attempted"])
        repair_succeeded = bool(filter_record["repair_succeeded"])
        repair_response_path = filter_record["repair_response_path"]
        final_diff_text = str(filter_record["final_diff_text"])
        final_diff_path = Path(filter_record["final_diff_path"])

        child_hash = None
        duplicate_of_program_id = None
        duplicate_patch_fingerprint_of_program_id = None
        duplicate_retry_attempted = False
        duplicate_retry_succeeded = False
        duplicate_retry_count = 0
        duplicate_retry_reason = None
        diversity_descriptor: dict[str, Any] = {}
        patch_fingerprint = None
        map_cell_key_value = None
        map_cell_already_occupied = False
        map_cell_elite_program_id = None

        identity = describe_pass_candidate(
            result=result,
            final_diff_text=final_diff_text,
            target_surface=target_surface,
        )
        child_hash = identity["child_hash"]
        diversity_descriptor = identity["diversity_descriptor"]
        patch_fingerprint = identity["patch_fingerprint"]
        map_cell_key_value = identity["map_cell_key"]

        if result.decision == "pass":
            result.hard_gates["unique_child"] = True
            if child_hash in seen_child_hashes:
                duplicate_of_program_id = seen_child_hashes[child_hash]
                duplicate_retry_reason = f"duplicate child program hash already seen for {duplicate_of_program_id}"
            elif patch_fingerprint in seen_patch_fingerprints:
                duplicate_patch_fingerprint_of_program_id = seen_patch_fingerprints[str(patch_fingerprint)]
                duplicate_retry_reason = (
                    "duplicate normalized patch fingerprint already seen for "
                    f"{duplicate_patch_fingerprint_of_program_id}"
                )

            if duplicate_retry_reason and args.duplicate_retry_attempts > 0:
                duplicate_retry_attempted = True
                forbidden_patches = [final_diff_text] + accepted_patches_by_surface.get(target_surface, [])[-2:]
                for retry_index in range(1, max(0, args.duplicate_retry_attempts) + 1):
                    duplicate_retry_count += 1
                    retry_target = choose_diversity_target(
                        target_surface,
                        attempt + args.attempts + retry_index,
                        occupied_labels=occupied_target_labels_by_surface.get(target_surface, set()),
                    )
                    retry_memory_query = " ".join(
                        [
                            target_surface,
                            "duplicate retry",
                            duplicate_retry_reason or "",
                            retry_target.cell_label if retry_target else "",
                            retry_target.instruction if retry_target else "",
                        ]
                    )
                    retry_memory_items = retrieve_memory_items(
                        reasoning_memory_items,
                        source_stage="controller_static",
                        target_surface=target_surface,
                        data_stage="stage_0_daily_stock",
                        query=retry_memory_query,
                        limit=max(0, args.memory_card_limit),
                    )
                    retry_memory_ids = [
                        str(item.get("memory_item_id")) for item in retry_memory_items if item.get("memory_item_id")
                    ]
                    retrieved_memory_ids_seen.update(retry_memory_ids)
                    retry_diagnostic_cards = retrieve_diagnostic_cards(
                        evaluator_diagnostic_report.get("diagnostic_cards", []),
                        target_surface=target_surface,
                        limit=max(0, args.diagnostic_card_limit),
                    )
                    retry_diagnostic_text = render_diagnostic_cards(retry_diagnostic_cards)
                    retry_skill_items = retrieve_skill_items(
                        skill_items,
                        source_stage="controller_static",
                        target_surface=target_surface,
                        data_stage="stage_0_daily_stock",
                        query=retry_memory_query + " " + retry_diagnostic_text,
                        limit=max(0, args.skill_card_limit),
                    )
                    retry_skill_ids = [
                        str(item.get("skill_id")) for item in retry_skill_items if item.get("skill_id")
                    ]
                    retrieved_skill_ids_seen.update(retry_skill_ids)
                    retry_messages = build_child_generation_prompt(
                        parent_code=parent_text,
                        evaluator_summary=evaluator_summary,
                        attempt_index=attempt,
                        target_surface=target_surface,
                        previous_accepted_patches=accepted_patches_by_surface.get(target_surface, [])[-3:],
                        diversity_target=retry_target,
                        occupied_map_cells=occupied_same_surface_cells,
                        forbidden_patches=forbidden_patches,
                        duplicate_retry_reason=duplicate_retry_reason,
                        reasoning_memory_text=render_memory_cards(retry_memory_items),
                        diagnostic_text=retry_diagnostic_text,
                        skill_text=render_skill_cards(retry_skill_items),
                    )
                    write_messages(
                        attempt_dir / f"duplicate_retry_{retry_index}_prompt",
                        "Duplicate Retry Prompt",
                        retry_messages,
                    )
                    if args.mock_patch_mode == "none":
                        retry_response_record = chat_completion(
                            role=args.model_role,
                            system_prompt=retry_messages["system"],
                            user_prompt=retry_messages["user"],
                            temperature=max(0.5, temperature),
                            max_tokens=args.max_tokens,
                            verify=True,
                        )
                        retry_text = retry_response_record["content"]
                    else:
                        retry_text = mock_patch(parent_text, args.mock_patch_mode, target_surface=target_surface)
                        retry_response_record = {
                            "role": "mock_duplicate_retry",
                            "served_model_name": "mock",
                            "temperature": max(0.5, temperature),
                            "content": retry_text,
                        }
                    retry_output_path = attempt_dir / f"duplicate_retry_{retry_index}_output.txt"
                    retry_output_path.write_text(retry_text, encoding="utf-8")
                    write_json(attempt_dir / f"duplicate_retry_{retry_index}_response.json", retry_response_record)
                    retry_filter_record = filter_patch_with_optional_repair(
                        attempt_dir=attempt_dir,
                        generated_text=retry_text,
                        raw_output_path=retry_output_path,
                        target_surface=target_surface,
                        attempt=attempt,
                        artifact_prefix=f"duplicate_retry_{retry_index}_",
                    )
                    retry_result = retry_filter_record["result"]
                    retry_identity = describe_pass_candidate(
                        result=retry_result,
                        final_diff_text=str(retry_filter_record["final_diff_text"]),
                        target_surface=target_surface,
                    )
                    retry_child_hash = retry_identity["child_hash"]
                    retry_patch_fingerprint = retry_identity["patch_fingerprint"]
                    retry_duplicate_reason = None
                    if retry_result.decision == "pass" and retry_child_hash in seen_child_hashes:
                        retry_duplicate_reason = (
                            "duplicate child program hash already seen for "
                            f"{seen_child_hashes[retry_child_hash]}"
                        )
                    elif retry_result.decision == "pass" and retry_patch_fingerprint in seen_patch_fingerprints:
                        retry_duplicate_reason = (
                            "duplicate normalized patch fingerprint already seen for "
                            f"{seen_patch_fingerprints[str(retry_patch_fingerprint)]}"
                        )
                    write_json(
                        attempt_dir / f"duplicate_retry_{retry_index}_duplicate_check.json",
                        {
                            "decision": retry_result.decision,
                            "duplicate_reason": retry_duplicate_reason,
                            "child_sha256": retry_child_hash,
                            "patch_fingerprint": retry_patch_fingerprint,
                            "map_cell_key": retry_identity["map_cell_key"],
                        },
                    )
                    if retry_result.decision == "pass" and retry_duplicate_reason is None:
                        result = retry_result
                        response_record = retry_response_record
                        final_diff_text = str(retry_filter_record["final_diff_text"])
                        final_diff_path = Path(retry_filter_record["final_diff_path"])
                        repair_attempted = repair_attempted or bool(retry_filter_record["repair_attempted"])
                        repair_succeeded = repair_succeeded or bool(retry_filter_record["repair_succeeded"])
                        repair_response_path = retry_filter_record["repair_response_path"] or repair_response_path
                        child_hash = retry_child_hash
                        diversity_descriptor = retry_identity["diversity_descriptor"]
                        patch_fingerprint = retry_patch_fingerprint
                        map_cell_key_value = retry_identity["map_cell_key"]
                        duplicate_of_program_id = None
                        duplicate_patch_fingerprint_of_program_id = None
                        duplicate_retry_succeeded = True
                        duplicate_retry_reason = None
                        break

            if duplicate_retry_reason:
                if duplicate_of_program_id:
                    result.failure_category = "duplicate_child"
                else:
                    result.failure_category = "duplicate_patch_fingerprint"
                result.decision = "reject"
                result.failure_reason = duplicate_retry_reason
                result.hard_gates["unique_child"] = False
            elif child_hash is not None:
                result.hard_gates["unique_child"] = True
                program_id_for_seen = f"{args.program_id_prefix}-{attempt:04d}"
                seen_child_hashes[child_hash] = program_id_for_seen
                if patch_fingerprint is not None:
                    seen_patch_fingerprints[str(patch_fingerprint)] = program_id_for_seen
                if map_cell_key_value:
                    map_cell_already_occupied = map_cell_key_value in occupied_map_cells
                    map_cell_elite_program_id = occupied_map_cells.get(map_cell_key_value)
                    occupied_map_cells.setdefault(map_cell_key_value, program_id_for_seen)
                actual_target_label = f"{target_surface}:{diversity_descriptor.get('patch_intent', 'unknown')}"
                occupied_labels = occupied_target_labels_by_surface.setdefault(target_surface, set())
                occupied_labels.add(diversity_target.cell_label)
                occupied_labels.add(actual_target_label)
                accepted_patches_by_surface.setdefault(target_surface, []).append(final_diff_text)
        else:
            result.hard_gates["unique_child"] = False

        result_record = result.to_record()
        program_id = f"{args.program_id_prefix}-{attempt:04d}"
        child_path = None
        if result.decision == "pass" and result.child_text is not None:
            child_path = attempt_dir / "child_program.py"
            child_path.write_text(result.child_text, encoding="utf-8")

        db_inserted = False
        if args.db_path:
            try:
                insert_program_record(
                    args.db_path,
                    {
                        "program_id": program_id,
                        "parent_id": "PROG-20260430-000000",
                        "root_id": "CAND-20260423-001",
                        "branch_id": "BRANCH-CAND-20260423-001-001",
                        "generation": 1,
                        "island": "daily_stock_signal",
                        "mutation_surface": "controller_static_child_dry_run",
                        "data_scope": "daily_stock_only",
                        "status": "controller_static_pass" if result.decision == "pass" else "controller_static_reject",
                        "program_path": str(child_path) if child_path else str(program_path),
                        "diff_path": str(final_diff_path),
                        "prompt_path": str(attempt_dir / "prompt.json"),
                        "evaluator_summary_path": None,
                        "metrics": result.vector_smoke_metrics,
                        "descriptors": {
                            "model_role": args.model_role,
                            "temperature": temperature,
                            "target_surface": target_surface,
                            "child_sha256": child_hash,
                            "duplicate_of_program_id": duplicate_of_program_id,
                            "duplicate_patch_fingerprint_of_program_id": duplicate_patch_fingerprint_of_program_id,
                            "duplicate_retry_attempted": duplicate_retry_attempted,
                            "duplicate_retry_succeeded": duplicate_retry_succeeded,
                            "duplicate_retry_count": duplicate_retry_count,
                            "map_cell_key": map_cell_key_value,
                            "map_cell_already_occupied": map_cell_already_occupied,
                            "map_cell_elite_program_id": map_cell_elite_program_id,
                            **diversity_descriptor,
                            "repair_attempted": repair_attempted,
                            "repair_succeeded": repair_succeeded,
                            "empty_retry_count": empty_retry_count,
                            "empty_retry_succeeded": empty_retry_succeeded,
                            "diagnostic_card_ids": diagnostic_card_ids,
                            "reasoning_memory_item_ids": retrieved_memory_item_ids,
                            "skill_ids": retrieved_skill_ids,
                            "initial_failure_category": initial_result_record.get("failure_category"),
                            "dry_run_only": True,
                        },
                        "hard_gates": result.hard_gates,
                        "validation_exposure": {
                            "controller_static": True,
                            "remote_sample_eval": False,
                            "remote_full_validation": False,
                            "test_set_used": False,
                        },
                        "failure_reason": result.failure_reason,
                    },
                )
                db_inserted = True
            except Exception as exc:
                result_record["db_insert_error"] = str(exc)

        result_record.update(
            {
                "attempt": attempt,
                "program_id": program_id,
                "target_surface": target_surface,
                "temperature": temperature,
                "db_inserted": db_inserted,
                "child_program_path": str(child_path) if child_path else None,
                "child_sha256": child_hash,
                "duplicate_of_program_id": duplicate_of_program_id,
                "duplicate_patch_fingerprint_of_program_id": duplicate_patch_fingerprint_of_program_id,
                "duplicate_retry_attempted": duplicate_retry_attempted,
                "duplicate_retry_succeeded": duplicate_retry_succeeded,
                "duplicate_retry_count": duplicate_retry_count,
                "map_cell_key": map_cell_key_value,
                "map_cell_already_occupied": map_cell_already_occupied,
                "map_cell_elite_program_id": map_cell_elite_program_id,
                **diversity_descriptor,
                "initial_response_content_was_null": bool(initial_response_record.get("content_was_null", False)),
                "initial_response_content_length": len(str(initial_response_record.get("content", "") or "")),
                "initial_response_reasoning_length": int(initial_response_record.get("reasoning_length", 0) or 0),
                "final_response_content_was_null": bool(response_record.get("content_was_null", False)),
                "final_response_content_length": len(str(response_record.get("content", "") or "")),
                "final_response_reasoning_length": int(response_record.get("reasoning_length", 0) or 0),
                "initial_decision": initial_result_record.get("decision"),
                "initial_failure_category": initial_result_record.get("failure_category"),
                "initial_failure_reason": initial_result_record.get("failure_reason"),
                "initial_hard_gates": initial_result_record.get("hard_gates", {}),
                "repair_attempted": repair_attempted,
                "repair_succeeded": repair_succeeded,
                "empty_retry_count": empty_retry_count,
                "empty_retry_succeeded": empty_retry_succeeded,
                "repair_response_path": str(repair_response_path) if repair_response_path else None,
                "final_diff_path": str(final_diff_path),
                "diagnostic_card_ids": diagnostic_card_ids,
                "reasoning_memory_item_ids": retrieved_memory_item_ids,
                "reasoning_memory_path": str(memory_path) if memory_path else None,
                "skill_ids": retrieved_skill_ids,
                "skill_library_path": str(skill_library_path) if skill_library_path else None,
            }
        )
        write_json(attempt_dir / "micro_filter_result.json", result_record)
        attempt_records.append(result_record)

    summary = summarize_attempts(attempt_records)
    summary.update(
        {
            "program_path": str(program_path),
            "evaluator_summary": args.evaluator_summary,
            "model_role": args.model_role,
            "mock_patch_mode": args.mock_patch_mode,
            "remote_sample_eval_launched": False,
            "full_validation_launched": False,
            "reasoning_memory_enabled": memory_path is not None,
            "reasoning_memory_path": str(memory_path) if memory_path else None,
            "reasoning_memory_item_count": len(reasoning_memory_items),
            "retrieved_reasoning_memory_ids": sorted(retrieved_memory_ids_seen),
            "skill_library_enabled": skill_library_path is not None,
            "skill_library_path": str(skill_library_path) if skill_library_path else None,
            "skill_library_item_count": len(skill_items),
            "retrieved_skill_ids": sorted(retrieved_skill_ids_seen),
            "evaluator_diagnostic_report_json": evaluator_diagnostic_paths["json"],
            "evaluator_diagnostic_report_markdown": evaluator_diagnostic_paths["markdown"],
            "evaluator_diagnostic_card_ids": [
                card.get("diagnostic_id")
                for card in evaluator_diagnostic_report.get("diagnostic_cards", [])
            ],
        }
    )
    if memory_path is not None:
        memory_update = build_controller_batch_memory_update(
            source_run_id=out_dir.name,
            summary=summary,
            attempts=attempt_records,
            memory_path=memory_path,
            retrieved_memory_ids=sorted(retrieved_memory_ids_seen),
        )
        memory_update_paths = write_memory_update(out_dir, memory_update)
        memory_update_log = append_memory_update(memory_path.parent / "memory_updates.jsonl", memory_update)
        summary["reasoning_memory_update_json"] = memory_update_paths["json"]
        summary["reasoning_memory_update_markdown"] = memory_update_paths["markdown"]
        summary["reasoning_memory_update_log"] = memory_update_log
    controller_diagnostic_report = build_controller_diagnostic_report(
        summary=summary,
        attempts=attempt_records,
        source_path=out_dir / "summary.json",
    )
    controller_diagnostic_paths = write_diagnostic_report(
        out_dir,
        "controller_diagnostic_report",
        controller_diagnostic_report,
    )
    summary["controller_diagnostic_report_json"] = controller_diagnostic_paths["json"]
    summary["controller_diagnostic_report_markdown"] = controller_diagnostic_paths["markdown"]
    summary["controller_diagnostic_card_ids"] = [
        card.get("diagnostic_id") for card in controller_diagnostic_report.get("diagnostic_cards", [])
    ]
    if skill_library_path is not None:
        skill_update = build_controller_batch_skill_update(
            source_run_id=out_dir.name,
            summary=summary,
            attempts=attempt_records,
            skill_library_path=skill_library_path,
            retrieved_skill_ids=sorted(retrieved_skill_ids_seen),
        )
        skill_update_paths = write_skill_update(out_dir, skill_update)
        skill_update_log = append_skill_update(skill_library_path.parent / "skill_updates.jsonl", skill_update)
        summary["skill_update_json"] = skill_update_paths["json"]
        summary["skill_update_markdown"] = skill_update_paths["markdown"]
        summary["skill_update_log"] = skill_update_log
    write_json(out_dir / "summary.json", {"summary": summary, "attempts": attempt_records})
    write_summary_markdown(out_dir / "summary.md", summary)
    print(json.dumps({"status": "ok", "out_dir": str(out_dir), "summary": summary}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
