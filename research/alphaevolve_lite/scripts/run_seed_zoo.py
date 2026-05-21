"""Render and evaluate deterministic Phase 4 seed-zoo parent candidates."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


def _ensure_repo_import() -> None:
    repo_root = Path(__file__).resolve().parents[3]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))


_ensure_repo_import()

from research.alphaevolve_lite.artifact_io import write_json  # noqa: E402
from research.alphaevolve_lite.seed_zoo import (  # noqa: E402
    SEED_ZOO_SCHEMA_VERSION,
    seed_zoo_rows_from_summaries,
    write_seed_zoo_programs,
    write_seed_zoo_results,
)
from research.alphaevolve_lite.splits import (  # noqa: E402
    DEFAULT_ANALYSIS_END_DATE,
    DEFAULT_ANALYSIS_START_DATE,
    DEFAULT_OUT_SAMPLE_START_DATE,
)
from research.alphaevolve_lite.paths import utc_now_iso, write_text  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run deterministic seed-zoo sample evaluations.")
    parser.add_argument("--csv-path", required=True)
    parser.add_argument(
        "--out-dir",
        default="artifacts/phase4_alphaevolve/seed_zoo_is_os_20260521",
    )
    parser.add_argument("--db-path", default="artifacts/phase4_alphaevolve/program_database.sqlite")
    parser.add_argument(
        "--seed-ids",
        default="all",
        help="Comma-separated seed ids, or all.",
    )
    parser.add_argument(
        "--benchmark-summary",
        default="",
        help="Optional evaluator_summary.json used for aggregate deltas and remote equivalence diagnostics.",
    )
    parser.add_argument(
        "--remote-sample-eval-script",
        default="research/alphaevolve_lite/scripts/remote_sample_eval.py",
    )
    parser.add_argument("--start-date", default=DEFAULT_ANALYSIS_START_DATE)
    parser.add_argument("--end-date", default=DEFAULT_ANALYSIS_END_DATE)
    parser.add_argument("--out-sample-start", default=DEFAULT_OUT_SAMPLE_START_DATE)
    parser.add_argument("--chunksize", type=int, default=1_000_000)
    parser.add_argument("--max-input-rows", type=int)
    parser.add_argument("--top-n", type=int, default=500)
    parser.add_argument("--total-cost-bps", type=float, default=2.5)
    parser.add_argument("--cost-grid-bps", default="0,1,2.5,5,10")
    parser.add_argument("--null-seeds", type=int, default=5)
    parser.add_argument("--turnover-penalty", type=float, default=0.25)
    parser.add_argument("--missing-weight-penalty", type=float, default=5.0)
    parser.add_argument("--min-portfolio-days", type=int, default=252)
    parser.add_argument("--min-portfolio-day-coverage", type=float, default=0.80)
    parser.add_argument(
        "--render-only",
        action="store_true",
        help="Only write seed-zoo programs and commands; do not run sample evaluation.",
    )
    parser.add_argument(
        "--continue-on-error",
        action="store_true",
        help="Continue evaluating remaining seeds if one subprocess fails.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    seed_ids = _parse_seed_ids(args.seed_ids)
    manifest = write_seed_zoo_programs(out_dir, seed_ids=seed_ids)
    commands = _build_eval_commands(args, manifest)
    _write_command_artifacts(out_dir, commands)

    run_manifest: dict[str, Any] = {
        "schema_version": SEED_ZOO_SCHEMA_VERSION,
        "stage": "seed_zoo_sample_eval",
        "created_at": utc_now_iso(),
        "out_dir": str(out_dir),
        "csv_path": args.csv_path,
        "db_path": args.db_path,
        "benchmark_summary": args.benchmark_summary,
        "render_only": bool(args.render_only),
        "seed_ids": [row["seed_id"] for row in manifest["programs"]],
        "command_count": len(commands),
    }

    if args.render_only:
        run_manifest["status"] = "rendered"
        write_json(out_dir / "seed_zoo_run_manifest.json", run_manifest)
        print(json.dumps({"status": "rendered", "out_dir": str(out_dir)}, sort_keys=True))
        return 0

    summaries = []
    run_results = []
    for command_record in commands:
        eval_out_dir = Path(command_record["out_dir"])
        eval_out_dir.mkdir(parents=True, exist_ok=True)
        result = subprocess.run(
            command_record["argv"],
            text=True,
            capture_output=True,
            check=False,
        )
        write_text(eval_out_dir / "seed_zoo_subprocess_stdout.txt", result.stdout)
        write_text(eval_out_dir / "seed_zoo_subprocess_stderr.txt", result.stderr)
        run_result = {
            "seed_id": command_record["seed_id"],
            "program_id": command_record["program_id"],
            "out_dir": str(eval_out_dir),
            "returncode": int(result.returncode),
        }
        summary_path = eval_out_dir / "evaluator_summary.json"
        if summary_path.exists():
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            summaries.append(summary)
            run_result["decision"] = summary.get("decision")
            run_result["failure_reason"] = summary.get("failure_reason")
        elif result.returncode != 0:
            run_result["decision"] = "missing_summary"
            run_result["failure_reason"] = result.stderr.strip()[:1000]
        run_results.append(run_result)
        if result.returncode != 0 and not args.continue_on_error:
            run_manifest["status"] = "error"
            run_manifest["run_results"] = run_results
            write_json(out_dir / "seed_zoo_run_manifest.json", run_manifest)
            print(
                json.dumps(
                    {
                        "status": "error",
                        "failed_seed_id": command_record["seed_id"],
                        "out_dir": str(out_dir),
                    },
                    sort_keys=True,
                ),
                file=sys.stderr,
            )
            return result.returncode or 1

    benchmark_summary = _read_optional_json(args.benchmark_summary)
    write_seed_zoo_results(out_dir, summaries, benchmark_summary=benchmark_summary)
    run_manifest["status"] = "ok"
    run_manifest["run_results"] = run_results
    run_manifest["candidate_rows"] = [
        row for row in seed_zoo_rows_from_summaries(summaries, benchmark_summary=benchmark_summary)
        if row["parent_candidate_tier"] == "candidate"
    ]
    write_json(out_dir / "seed_zoo_run_manifest.json", run_manifest)
    print(
        json.dumps(
            {
                "status": "ok",
                "out_dir": str(out_dir),
                "program_count": len(summaries),
                "candidate_count": len(run_manifest["candidate_rows"]),
            },
            sort_keys=True,
        )
    )
    return 0


def _build_eval_commands(args: argparse.Namespace, manifest: dict[str, Any]) -> list[dict[str, Any]]:
    commands = []
    script = Path(args.remote_sample_eval_script)
    for row in manifest["programs"]:
        eval_out_dir = Path(args.out_dir) / "evaluations" / str(row["seed_id"])
        argv = [
            sys.executable,
            str(script),
            "--csv-path",
            args.csv_path,
            "--program-path",
            row["program_path"],
            "--out-dir",
            str(eval_out_dir),
            "--db-path",
            args.db_path,
            "--program-id",
            row["program_id"],
            "--program-kind",
            "seed",
            "--strategy-family",
            "daily_stock_seed_zoo",
            "--start-date",
            args.start_date,
            "--end-date",
            args.end_date,
            "--out-sample-start",
            args.out_sample_start,
            "--chunksize",
            str(args.chunksize),
            "--top-n",
            str(args.top_n),
            "--total-cost-bps",
            str(args.total_cost_bps),
            "--cost-grid-bps",
            args.cost_grid_bps,
            "--null-seeds",
            str(args.null_seeds),
            "--turnover-penalty",
            str(args.turnover_penalty),
            "--missing-weight-penalty",
            str(args.missing_weight_penalty),
            "--min-portfolio-days",
            str(args.min_portfolio_days),
            "--min-portfolio-day-coverage",
            str(args.min_portfolio_day_coverage),
            "--run-id",
            f"seed_zoo-{row['seed_id']}-{utc_now_iso().replace(':', '').replace('-', '')}",
        ]
        if args.max_input_rows is not None:
            argv.extend(["--max-input-rows", str(args.max_input_rows)])
        if args.benchmark_summary:
            argv.extend(["--reference-summary", args.benchmark_summary])
        commands.append(
            {
                "seed_id": row["seed_id"],
                "program_id": row["program_id"],
                "out_dir": str(eval_out_dir),
                "argv": argv,
            }
        )
    return commands


def _write_command_artifacts(out_dir: Path, commands: list[dict[str, Any]]) -> None:
    write_json(out_dir / "seed_zoo_commands.json", commands)
    lines = ["#!/usr/bin/env bash", "set -euo pipefail", ""]
    for command in commands:
        lines.append(_shell_join(command["argv"]))
    write_text(out_dir / "seed_zoo_commands.sh", "\n\n".join(lines) + "\n")


def _shell_join(parts: list[str]) -> str:
    return " ".join("'" + str(part).replace("'", "'\"'\"'") + "'" for part in parts)


def _parse_seed_ids(raw: str) -> list[str] | None:
    values = [item.strip() for item in raw.split(",") if item.strip()]
    if not values or values == ["all"]:
        return None
    return values


def _read_optional_json(path: str) -> dict[str, Any] | None:
    if not path:
        return None
    return json.loads(Path(path).read_text(encoding="utf-8"))


if __name__ == "__main__":
    raise SystemExit(main())
