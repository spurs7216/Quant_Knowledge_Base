"""Run a small remote Qwen child-generation controller dry run."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


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
    parser.add_argument("--max-tokens", type=int, default=4096)
    parser.add_argument("--empty-retry-attempts", type=int, default=1)
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
        f"- db_insert_pass_rate: `{summary['db_insert_pass_rate']}`",
        "",
        "## Failure Categories",
        "",
    ]
    if summary["failure_categories"]:
        for category, count in summary["failure_categories"].items():
            lines.append(f"- {category}: `{count}`")
    else:
        lines.append("- none")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    _ensure_repo_import()
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
    temperatures = [float(item.strip()) for item in args.temperature_grid.split(",") if item.strip()]
    if not temperatures:
        temperatures = [0.2]
    if args.db_path:
        init_db(args.db_path)

    attempt_records: list[dict[str, Any]] = []
    seen_child_hashes: dict[str, str] = {}
    accepted_patches_by_surface: dict[str, list[str]] = {}
    for attempt in range(args.attempts):
        attempt_dir = out_dir / f"attempt_{attempt:03d}"
        attempt_dir.mkdir(parents=True, exist_ok=True)
        temperature = temperatures[attempt % len(temperatures)]
        target_surface = choose_target_surface(attempt)
        messages = build_child_generation_prompt(
            parent_code=parent_text,
            evaluator_summary=evaluator_summary,
            attempt_index=attempt,
            target_surface=target_surface,
            previous_accepted_patches=accepted_patches_by_surface.get(target_surface, [])[-3:],
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

        result = run_micro_filter(parent_text, generated_text, target_surface=target_surface)
        initial_result_record = result.to_record()
        write_json(attempt_dir / "micro_filter_initial_result.json", initial_result_record)
        repair_attempted = False
        repair_succeeded = False
        repair_record: dict[str, Any] | None = None
        final_diff_text = generated_text

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
            write_messages(attempt_dir / "repair_prompt", "Patch Repair Prompt", repair_messages)
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
            (attempt_dir / "repair_output.txt").write_text(repair_text, encoding="utf-8")
            write_json(attempt_dir / "repair_response.json", repair_record)
            repair_result = run_micro_filter(parent_text, repair_text, target_surface=target_surface)
            write_json(attempt_dir / "repair_micro_filter_result.json", repair_result.to_record())
            if repair_result.decision == "pass":
                result = repair_result
                repair_succeeded = True
                final_diff_text = repair_text

        child_hash = None
        duplicate_of_program_id = None
        if result.child_text is not None:
            child_hash = hashlib.sha256(result.child_text.encode("utf-8")).hexdigest()
        if result.decision == "pass":
            result.hard_gates["unique_child"] = True
            if child_hash in seen_child_hashes:
                duplicate_of_program_id = seen_child_hashes[child_hash]
                result.decision = "reject"
                result.failure_category = "duplicate_child"
                result.failure_reason = f"duplicate child program hash already seen for {duplicate_of_program_id}"
                result.hard_gates["unique_child"] = False
            elif child_hash is not None:
                seen_child_hashes[child_hash] = f"{args.program_id_prefix}-{attempt:04d}"
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
                        "diff_path": str(attempt_dir / ("repair_output.txt" if repair_succeeded else "raw_output.txt")),
                        "prompt_path": str(attempt_dir / "prompt.json"),
                        "evaluator_summary_path": None,
                        "metrics": result.vector_smoke_metrics,
                        "descriptors": {
                            "model_role": args.model_role,
                            "temperature": temperature,
                            "target_surface": target_surface,
                            "child_sha256": child_hash,
                            "duplicate_of_program_id": duplicate_of_program_id,
                            "repair_attempted": repair_attempted,
                            "repair_succeeded": repair_succeeded,
                            "empty_retry_count": empty_retry_count,
                            "empty_retry_succeeded": empty_retry_succeeded,
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
                "repair_response_path": str(attempt_dir / "repair_response.json") if repair_attempted else None,
                "final_diff_path": str(attempt_dir / ("repair_output.txt" if repair_succeeded else "raw_output.txt")),
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
        }
    )
    write_json(out_dir / "summary.json", {"summary": summary, "attempts": attempt_records})
    write_summary_markdown(out_dir / "summary.md", summary)
    print(json.dumps({"status": "ok", "out_dir": str(out_dir), "summary": summary}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
