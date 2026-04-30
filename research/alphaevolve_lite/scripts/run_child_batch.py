"""Run a small remote Qwen child-generation controller dry run."""

from __future__ import annotations

import argparse
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
    parser.add_argument("--program-id-prefix", default="PROG-20260430-CHILD")
    parser.add_argument("--mock-patch-mode", choices=["none", "sign_flip", "no_valid_patch"], default="none")
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


def mock_patch(parent_text: str, mode: str) -> str:
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
    raise RuntimeError(f"unknown mock patch mode: {mode}")


def summarize_attempts(attempts: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(attempts)

    def rate(gate: str) -> float:
        if total == 0:
            return 0.0
        return sum(1 for item in attempts if item.get("hard_gates", {}).get(gate)) / total

    passed = [item for item in attempts if item.get("decision") == "pass"]
    return {
        "attempt_count": total,
        "pass_count": len(passed),
        "raw_parse_pass_rate": rate("parse_search_replace"),
        "repair_attempt_rate": 0.0,
        "repair_success_rate": 0.0,
        "exact_search_match_rate": rate("exact_search_match"),
        "evolve_block_safe_rate": rate("evolve_block_safe"),
        "apply_pass_rate": rate("apply_patch"),
        "compile_pass_rate": rate("compile_pass"),
        "vector_smoke_pass_rate": rate("vector_smoke_pass"),
        "db_insert_pass_rate": sum(1 for item in attempts if item.get("db_inserted")) / total if total else 0.0,
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
        f"- exact_search_match_rate: `{summary['exact_search_match_rate']}`",
        f"- evolve_block_safe_rate: `{summary['evolve_block_safe_rate']}`",
        f"- apply_pass_rate: `{summary['apply_pass_rate']}`",
        f"- compile_pass_rate: `{summary['compile_pass_rate']}`",
        f"- vector_smoke_pass_rate: `{summary['vector_smoke_pass_rate']}`",
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
    for attempt in range(args.attempts):
        attempt_dir = out_dir / f"attempt_{attempt:03d}"
        attempt_dir.mkdir(parents=True, exist_ok=True)
        temperature = temperatures[attempt % len(temperatures)]
        messages = build_child_generation_prompt(
            parent_code=parent_text,
            evaluator_summary=evaluator_summary,
            attempt_index=attempt,
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
            generated_text = mock_patch(parent_text, args.mock_patch_mode)
            response_record = {
                "role": "mock",
                "served_model_name": "mock",
                "temperature": temperature,
                "content": generated_text,
            }

        (attempt_dir / "raw_output.txt").write_text(generated_text, encoding="utf-8")
        write_json(attempt_dir / "model_response.json", response_record)

        result = run_micro_filter(parent_text, generated_text)
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
                        "diff_path": str(attempt_dir / "raw_output.txt"),
                        "prompt_path": str(attempt_dir / "prompt.json"),
                        "evaluator_summary_path": None,
                        "metrics": result.vector_smoke_metrics,
                        "descriptors": {
                            "model_role": args.model_role,
                            "temperature": temperature,
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
                "temperature": temperature,
                "db_inserted": db_inserted,
                "child_program_path": str(child_path) if child_path else None,
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
