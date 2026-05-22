"""Prepare or run a small multi-parent cost-aware controller batch."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def _ensure_repo_import() -> None:
    repo_root = Path(__file__).resolve().parents[3]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))


_ensure_repo_import()

from research.alphaevolve_lite.artifact_io import write_json  # noqa: E402
from research.alphaevolve_lite.parent_zoo import (  # noqa: E402
    DEFAULT_ATTEMPT017_PROGRAM_ID,
    DEFAULT_PARENT_ZOO_ROOT_IDS,
    PARENT_ZOO_SCHEMA_VERSION,
    write_parent_zoo_plan,
)
from research.alphaevolve_lite.paths import utc_now_iso, write_text  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run parent-zoo cost-aware controller batches.")
    parser.add_argument(
        "--out-dir",
        default="artifacts/phase4_alphaevolve/parent_zoo_cost_aware_20260522",
    )
    parser.add_argument(
        "--roots",
        default=",".join(DEFAULT_PARENT_ZOO_ROOT_IDS),
        help="Comma-separated parent-zoo root ids, or all.",
    )
    parser.add_argument("--db-path", default="artifacts/phase4_alphaevolve/program_database.sqlite")
    parser.add_argument(
        "--controller-script",
        default="research/alphaevolve_lite/scripts/run_child_batch.py",
    )
    parser.add_argument("--program-id-prefix", default="PROG-20260522-PZOO")
    parser.add_argument(
        "--mechanism-card-path",
        default="",
        help="Optional mechanism_cards.json. If omitted, hand-authored parent-zoo cards are written.",
    )
    parser.add_argument(
        "--incumbent-summary",
        default=(
            "artifacts/phase4_alphaevolve/"
            "remote_sample_eval_attempt017_is_os_forward_repair_20260519/evaluator_summary.json"
        ),
    )
    parser.add_argument("--prior-summary", action="append", default=[])
    parser.add_argument("--attempts-per-root", type=int)
    parser.add_argument("--model-role", default="fast_generator")
    parser.add_argument("--temperature-grid", default="0.0,0.2,0.5")
    parser.add_argument("--max-tokens", type=int, default=8192)
    parser.add_argument(
        "--render-only",
        action="store_true",
        help="Write parent-zoo programs, cards, and commands without launching Qwen.",
    )
    parser.add_argument(
        "--continue-on-error",
        action="store_true",
        help="Continue remaining roots after one controller subprocess fails.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.attempts_per_root is not None and args.attempts_per_root <= 0:
        print("--attempts-per-root must be positive", file=sys.stderr)
        return 2
    if args.max_tokens <= 0:
        print("--max-tokens must be positive", file=sys.stderr)
        return 2

    out_dir = Path(args.out_dir)
    root_ids = _parse_root_ids(args.roots)
    plan = write_parent_zoo_plan(
        out_dir,
        root_ids=root_ids,
        db_path=args.db_path,
        controller_script=args.controller_script,
        program_id_prefix=args.program_id_prefix,
        attempts_per_root=args.attempts_per_root,
        mechanism_card_path=args.mechanism_card_path or None,
        prior_summary_paths=args.prior_summary,
        model_role=args.model_role,
        temperature_grid=args.temperature_grid,
        max_tokens=args.max_tokens,
        incumbent_summary_path=args.incumbent_summary,
    )
    commands = plan["commands"]
    run_manifest = {
        "schema_version": PARENT_ZOO_SCHEMA_VERSION,
        "stage": "parent_zoo_cost_aware_controller_batch",
        "created_at": utc_now_iso(),
        "out_dir": str(out_dir),
        "root_ids": [root["root_id"] for root in plan["manifest"]["roots"]],
        "command_count": len(commands),
        "render_only": bool(args.render_only),
        "incumbent_program_id": DEFAULT_ATTEMPT017_PROGRAM_ID,
        "incumbent_summary": args.incumbent_summary,
    }

    if args.render_only:
        run_manifest["status"] = "rendered"
        write_json(out_dir / "parent_zoo_run_manifest.json", run_manifest)
        print(json.dumps({"status": "rendered", "out_dir": str(out_dir)}, sort_keys=True))
        return 0

    run_results = []
    for command in commands:
        controller_out_dir = Path(command["out_dir"])
        controller_out_dir.mkdir(parents=True, exist_ok=True)
        result = subprocess.run(command["argv"], text=True, capture_output=True, check=False)
        write_text(controller_out_dir / "parent_zoo_subprocess_stdout.txt", result.stdout)
        write_text(controller_out_dir / "parent_zoo_subprocess_stderr.txt", result.stderr)
        run_result = {
            "root_id": command["root_id"],
            "program_id": command["program_id"],
            "out_dir": str(controller_out_dir),
            "returncode": int(result.returncode),
        }
        summary_path = controller_out_dir / "summary.json"
        if summary_path.exists():
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            run_result["decision"] = "summary_written"
            run_result["pass_count"] = summary.get("summary", {}).get("pass_count")
            run_result["sample_eval_candidate_count"] = summary.get("summary", {}).get(
                "sample_eval_candidate_count"
            )
        elif result.returncode != 0:
            run_result["decision"] = "missing_summary"
            run_result["failure_reason"] = result.stderr.strip()[:1000]
        run_results.append(run_result)
        if result.returncode != 0 and not args.continue_on_error:
            run_manifest["status"] = "error"
            run_manifest["run_results"] = run_results
            write_json(out_dir / "parent_zoo_run_manifest.json", run_manifest)
            print(
                json.dumps(
                    {
                        "status": "error",
                        "failed_root_id": command["root_id"],
                        "out_dir": str(out_dir),
                    },
                    sort_keys=True,
                ),
                file=sys.stderr,
            )
            return result.returncode or 1

    run_manifest["status"] = "ok"
    run_manifest["run_results"] = run_results
    write_json(out_dir / "parent_zoo_run_manifest.json", run_manifest)
    print(
        json.dumps(
            {
                "status": "ok",
                "out_dir": str(out_dir),
                "root_count": len(commands),
                "sample_eval_candidate_count": sum(
                    int(item.get("sample_eval_candidate_count") or 0) for item in run_results
                ),
            },
            sort_keys=True,
        )
    )
    return 0


def _parse_root_ids(raw: str) -> list[str] | None:
    values = [item.strip() for item in raw.split(",") if item.strip()]
    if not values or values == ["all"]:
        return None
    return values


if __name__ == "__main__":
    raise SystemExit(main())
