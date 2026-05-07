"""Run a compact remote sample evaluation for the Kalman reversal seed."""

from __future__ import annotations

import argparse
import importlib.util
import json
import platform
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _ensure_repo_import() -> None:
    repo_root = Path(__file__).resolve().parents[3]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Remote sample-evaluate a Phase 4 strategy program.")
    parser.add_argument("--csv-path", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--program-path", default="research/alphaevolve_lite/seeds/kalman_reversal_seed.py")
    parser.add_argument("--db-path", default="")
    parser.add_argument("--start-date", default="2018-01-01")
    parser.add_argument("--end-date", default="2020-12-31")
    parser.add_argument("--chunksize", type=int, default=1_000_000)
    parser.add_argument("--max-input-rows", type=int)
    parser.add_argument("--top-n", type=int, default=500)
    parser.add_argument("--total-cost-bps", type=float, default=2.5)
    parser.add_argument("--cost-grid-bps", default="0,1,2.5,5")
    parser.add_argument("--null-seeds", type=int, default=5)
    parser.add_argument("--turnover-penalty", type=float, default=0.25)
    parser.add_argument("--missing-weight-penalty", type=float, default=5.0)
    parser.add_argument("--program-id", default="PROG-20260430-000000")
    parser.add_argument("--run-id", default="")
    return parser.parse_args()


def load_strategy_module(program_path: str):
    path = Path(program_path)
    if not path.is_absolute():
        path = Path.cwd() / path
    if not path.exists():
        raise FileNotFoundError(f"strategy program path does not exist: {path}")
    module_name = f"alphaevolve_eval_program_{uuid.uuid4().hex}"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import strategy program from {path}")
    module = importlib.util.module_from_spec(spec)
    old_dont_write_bytecode = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = old_dont_write_bytecode
    required = [
        "DEFAULT_PARAMS",
        "compute_signal",
        "rank_or_transform_signal",
        "construct_portfolio",
        "apply_risk_controls",
    ]
    missing = [name for name in required if not hasattr(module, name)]
    if missing:
        raise RuntimeError(f"strategy program missing required names: {missing}")
    return module, path


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def git_value(args: list[str]) -> str:
    try:
        out = subprocess.check_output(["git", *args], stderr=subprocess.DEVNULL)
        return out.decode("utf-8", errors="replace").strip()
    except Exception:
        return "unknown"


def write_git_status_artifacts(out_dir: Path) -> dict[str, Any]:
    """Record dirty-tree details for remote reproducibility review."""

    status = git_value(["status", "--short"])
    diff_stat = git_value(["diff", "--stat"])
    branch = git_value(["rev-parse", "--abbrev-ref", "HEAD"])
    commit = git_value(["rev-parse", "HEAD"])
    (out_dir / "git_status.txt").write_text(status + ("\n" if status else ""), encoding="utf-8")
    (out_dir / "git_diff_stat.txt").write_text(diff_stat + ("\n" if diff_stat else ""), encoding="utf-8")
    return {
        "git_commit": commit,
        "git_branch": branch,
        "git_dirty": bool(status),
        "git_status_path": "git_status.txt",
        "git_diff_stat_path": "git_diff_stat.txt",
    }


def write_lines(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def duplicate_diagnostics(frame, contract, max_rows: int = 200):
    import pandas as pd

    keys = [contract.security_id, contract.date]
    if frame.empty or not frame.duplicated(keys, keep=False).any():
        return pd.DataFrame(
            columns=[
                contract.security_id,
                contract.date,
                "duplicate_rows",
                "conflicting_columns",
            ]
        ), {
            "duplicate_groups": 0,
            "duplicate_rows": 0,
            "duplicate_groups_with_conflicts": 0,
            "duplicate_conflict_columns": "",
        }

    dup = frame.loc[frame.duplicated(keys, keep=False)].sort_values(keys).copy()
    rows = []
    conflict_columns: set[str] = set()
    for (permno, date), group in dup.groupby(keys, sort=True):
        conflicts = [
            col
            for col in contract.required_columns
            if col in group.columns and group[col].astype(str).fillna("<NA>").nunique(dropna=False) > 1
        ]
        conflict_columns.update(conflicts)
        rows.append(
            {
                contract.security_id: int(permno) if pd.notna(permno) else "",
                contract.date: pd.Timestamp(date).date().isoformat() if pd.notna(date) else "",
                "duplicate_rows": int(len(group)),
                "conflicting_columns": "|".join(conflicts),
            }
        )
    detail = pd.DataFrame(rows)
    summary = {
        "duplicate_groups": int(len(detail)),
        "duplicate_rows": int(len(dup)),
        "duplicate_groups_with_conflicts": int(detail["conflicting_columns"].ne("").sum()) if len(detail) else 0,
        "duplicate_conflict_columns": "|".join(sorted(conflict_columns)),
    }
    return detail.head(max_rows), summary


def main() -> int:
    _ensure_repo_import()
    import pandas as pd

    from research.alphaevolve_lite.artifact_io import clean_json, write_json
    from research.alphaevolve_lite.daily_stock_contract import CONTRACT, eligibility_query_description
    from research.alphaevolve_lite.daily_stock_loader import (
        apply_duplicate_policy,
        apply_static_eligibility,
        load_daily_stock_window,
    )
    from research.alphaevolve_lite.program_database import init_db, insert_program_record
    from research.alphaevolve_lite.sample_eval_baselines import (
        build_baseline_records,
        flatten_baseline_rows,
        summarize_baselines,
    )
    from research.alphaevolve_lite.sample_eval_metrics import (
        build_forward_returns,
        cost_sensitivity_rows,
        portfolio_from_weights,
        scorecard_from_metrics,
        split_metrics,
    )
    from research.alphaevolve_lite.splits import build_chronological_splits, write_split_manifest
    from research.alphaevolve_lite.universe import (
        UNIVERSE_POLICY_ID,
        apply_monthly_universe,
        build_monthly_rolling_universe,
        write_universe_artifacts,
    )

    args = parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    run_id = args.run_id or f"remote_sample_eval-{utc_now_iso().replace(':', '').replace('-', '')}-{uuid.uuid4().hex[:8]}"
    costs = [float(item.strip()) for item in args.cost_grid_bps.split(",") if item.strip()]
    if args.null_seeds < 0:
        print("--null-seeds must be nonnegative", file=sys.stderr)
        return 2
    git_status = write_git_status_artifacts(out_dir)

    diagnostics: list[dict[str, Any]] = []
    decision = "reject"
    failure_reason = None

    try:
        strategy_module, resolved_program_path = load_strategy_module(args.program_path)
        raw, load_diag = load_daily_stock_window(
            args.csv_path,
            start_date=args.start_date,
            end_date=args.end_date,
            chunksize=args.chunksize,
            max_input_rows=args.max_input_rows,
        )
        diagnostics.extend({"check": key, "status": "info", "value": value} for key, value in load_diag.items())
        duplicate_detail, duplicate_summary = duplicate_diagnostics(raw, CONTRACT)
        duplicate_detail.to_csv(out_dir / "duplicate_diagnostics.csv", index=False)
        diagnostics.extend(
            {"check": key, "status": "info", "value": value}
            for key, value in duplicate_summary.items()
        )
        deduped, dup_diag = apply_duplicate_policy(raw)
        diagnostics.extend({"check": key, "status": "info", "value": value} for key, value in dup_diag.items())
        eligible, eligibility_diag = apply_static_eligibility(deduped)
        diagnostics.extend({"check": key, "status": "info", "value": value} for key, value in eligibility_diag.items())

        if eligible.empty:
            raise RuntimeError("no eligible rows after daily_stock_contract_v1 filters")

        splits = build_chronological_splits(eligible[CONTRACT.date])
        membership, universe_summary = build_monthly_rolling_universe(eligible, top_n=args.top_n)
        universe_panel = apply_monthly_universe(eligible, membership)
        if universe_panel.empty:
            raise RuntimeError("rolling universe produced no sample rows")

        eval_panel = build_forward_returns(universe_panel, CONTRACT)
        strategy_params = dict(strategy_module.DEFAULT_PARAMS)
        signal = strategy_module.compute_signal(eval_panel, strategy_params)
        ranked = strategy_module.rank_or_transform_signal(signal, eval_panel, strategy_params)
        raw_weights = strategy_module.construct_portfolio(ranked, eval_panel, strategy_params)
        weights = strategy_module.apply_risk_controls(raw_weights, eval_panel, strategy_params)
        full_portfolio, positions = portfolio_from_weights(eval_panel, weights, args.total_cost_bps, CONTRACT)
        validation_end = splits[1].end
        portfolio = full_portfolio.loc[full_portfolio["DlyCalDt"] <= validation_end].copy()
        positions = positions.loc[positions[CONTRACT.date] <= validation_end].copy()
        if portfolio.empty:
            raise RuntimeError("seed produced no nonzero portfolio returns")

        visible_splits = [split for split in splits if split.name in {"train", "validation"}]
        metrics = {
            split.name: split_metrics(
                portfolio,
                split.name,
                split.start,
                split.end,
                turnover_penalty=args.turnover_penalty,
                missing_weight_penalty=args.missing_weight_penalty,
            )
            for split in visible_splits
        }
        metrics["search_sample"] = split_metrics(
            portfolio,
            "search_sample",
            portfolio["DlyCalDt"].min(),
            portfolio["DlyCalDt"].max(),
            turnover_penalty=args.turnover_penalty,
            missing_weight_penalty=args.missing_weight_penalty,
        )

        baseline_records = build_baseline_records(
            panel=eval_panel,
            reference_weights=weights,
            contract=CONTRACT,
            validation_end=validation_end,
            total_cost_bps=args.total_cost_bps,
            visible_splits=visible_splits,
            null_seeds=args.null_seeds,
            turnover_penalty=args.turnover_penalty,
            missing_weight_penalty=args.missing_weight_penalty,
        )
        baseline_rows = flatten_baseline_rows(baseline_records)
        baseline_rows.to_csv(out_dir / "null_baselines.csv", index=False)
        baseline_summary = summarize_baselines(baseline_rows, metrics)
        write_json(out_dir / "baseline_summary.json", baseline_summary)

        hard_gates = {
            "daily_stock_contract_v1_columns_present": True,
            "rolling_universe_nonempty": bool(len(membership)),
            "portfolio_nonempty": bool(len(portfolio)),
            "max_weight_reported": "max_weight" in metrics["search_sample"],
            "test_metrics_locked": True,
            "missing_held_weight_within_sample_tolerance": metrics["search_sample"]["max_missing_held_weight"] <= 0.05,
            "duplicate_diagnostics_written": (out_dir / "duplicate_diagnostics.csv").exists(),
            "git_status_recorded": (out_dir / "git_status.txt").exists(),
            "null_baselines_written": (out_dir / "null_baselines.csv").exists(),
            "turnover_aware_score_reported": "turnover_aware_score" in metrics["search_sample"],
        }
        decision = "sample_pass" if all(hard_gates.values()) else "sample_review"

        scorecard = scorecard_from_metrics(args.program_id, metrics, visible_splits)
        cost_rows = cost_sensitivity_rows(
            portfolio,
            costs,
            turnover_penalty=args.turnover_penalty,
            missing_weight_penalty=args.missing_weight_penalty,
        )

        write_universe_artifacts(out_dir, membership, universe_summary)
        write_split_manifest(
            out_dir / "split_manifest.yaml",
            splits=splits,
            calendar_count=int(eligible[CONTRACT.date].nunique()),
            universe_policy=UNIVERSE_POLICY_ID,
            duplicate_policy=dup_diag,
        )
        portfolio.to_csv(out_dir / "returns_by_split.csv", index=False)
        positions.head(5000).to_csv(out_dir / "positions_sample.csv", index=False)
        scorecard.to_csv(out_dir / "scorecard.csv", index=False)
        pd.DataFrame(cost_rows).to_csv(out_dir / "cost_sensitivity.csv", index=False)
        pd.DataFrame(diagnostics).to_csv(out_dir / "diagnostics.csv", index=False)

        manifest = {
            "run_id": run_id,
            "program_id": args.program_id,
            "stage": "remote_sample_eval",
            "program_path": str(resolved_program_path),
            "csv_path": args.csv_path,
            "start_date": args.start_date,
            "end_date": args.end_date,
            "top_n": args.top_n,
            "total_cost_bps": args.total_cost_bps,
            "cost_grid_bps": costs,
            "null_seeds": args.null_seeds,
            "turnover_penalty": args.turnover_penalty,
            "missing_weight_penalty": args.missing_weight_penalty,
            "daily_stock_contract": CONTRACT.contract_id,
            "universe_policy": UNIVERSE_POLICY_ID,
            "eligibility_filters": eligibility_query_description(),
            **git_status,
            "python": sys.version,
            "platform": platform.platform(),
            "created_at": utc_now_iso(),
        }
        write_json(
            out_dir / "metrics.json",
            {
                "program_id": args.program_id,
                "metrics": metrics,
                "baseline_summary": baseline_summary,
            },
        )
        write_json(
            out_dir / "evaluator_summary.json",
            {
                "schema_version": "phase4_evaluator_summary_v1",
                "program_id": args.program_id,
                "stage": "remote_sample_eval",
                "decision": decision,
                "failure_reason": failure_reason,
                "hard_gates": hard_gates,
                "metrics": metrics,
                "baseline_summary": baseline_summary,
                "descriptors": {
                    "daily_stock_contract": CONTRACT.contract_id,
                    "strategy_family": "kalman_innovation_reversal",
                    "program_path": str(resolved_program_path),
                    "universe_policy": UNIVERSE_POLICY_ID,
                    "data_scope": "daily_stock_only",
                    "git_dirty": git_status["git_dirty"],
                },
                "next_prompt_hint": "If sample_pass, compare against seed, null baselines, and sibling children before any stage-0/full validation. Do not use test metrics for prompt sampling.",
                "artifact_paths": {
                    "scorecard": "scorecard.csv",
                    "diagnostics": "diagnostics.csv",
                    "cost_sensitivity": "cost_sensitivity.csv",
                    "duplicate_diagnostics": "duplicate_diagnostics.csv",
                    "null_baselines": "null_baselines.csv",
                    "baseline_summary": "baseline_summary.json",
                    "git_status": "git_status.txt",
                    "universe_summary": "universe_summary.csv",
                    "split_manifest": "split_manifest.yaml",
                },
            },
        )
        write_json(out_dir / "run_manifest.json", manifest)
        write_lines(
            out_dir / "run_manifest.yaml",
            [f"{key}: {value}" for key, value in clean_json(manifest).items()],
        )
        write_lines(
            out_dir / "failure_report.md",
            [
                "# Failure Report",
                "",
                "## Failure Category",
                "",
                "none" if decision == "sample_pass" else "sample_review",
                "",
                "## Exact Gate That Failed",
                "",
                "none" if decision == "sample_pass" else "review evaluator_summary.json hard_gates",
            ],
        )
        write_lines(
            out_dir / "review.md",
            [
                "# Remote Sample Eval Review",
                "",
                f"- decision: `{decision}`",
                f"- program_id: `{args.program_id}`",
                f"- daily_stock_contract: `{CONTRACT.contract_id}`",
                f"- rows_after_static_eligibility: `{eligibility_diag.get('rows_after_static_eligibility')}`",
                f"- universe_rows: `{len(universe_panel)}`",
                f"- portfolio_days: `{len(portfolio)}`",
                f"- search_sample_sharpe: `{metrics['search_sample']['sharpe']}`",
                f"- turnover_aware_score: `{metrics['search_sample']['turnover_aware_score']}`",
                f"- max_weight: `{metrics['search_sample']['max_weight']}`",
                f"- max_missing_held_weight: `{metrics['search_sample']['max_missing_held_weight']}`",
                f"- duplicate_groups_with_conflicts: `{duplicate_summary['duplicate_groups_with_conflicts']}`",
                f"- git_dirty: `{git_status['git_dirty']}`",
            ],
        )

        if args.db_path:
            default_seed_path = Path("research/alphaevolve_lite/seeds/kalman_reversal_seed.py")
            try:
                is_seed_program = resolved_program_path.resolve() == (Path.cwd() / default_seed_path).resolve()
            except Exception:
                is_seed_program = str(resolved_program_path).replace("\\", "/").endswith(default_seed_path.as_posix())
            init_db(args.db_path)
            insert_program_record(
                args.db_path,
                {
                    "program_id": args.program_id,
                    "parent_id": None if is_seed_program else "PROG-20260430-000000",
                    "root_id": "CAND-20260423-001",
                    "branch_id": "BRANCH-CAND-20260423-001-001",
                    "generation": 0 if is_seed_program else 1,
                    "island": "daily_stock_signal",
                    "mutation_surface": "seed" if is_seed_program else "child_program",
                    "data_scope": "daily_stock_only",
                    "status": "seed_sample_evaluated" if is_seed_program else "child_sample_evaluated",
                    "program_path": str(resolved_program_path),
                    "evaluator_summary_path": str(out_dir / "evaluator_summary.json"),
                    "metrics": metrics,
                    "descriptors": {
                        "daily_stock_contract": CONTRACT.contract_id,
                        "program_path": str(resolved_program_path),
                    },
                    "hard_gates": hard_gates,
                    "validation_exposure": {
                        "remote_sample_eval": True,
                        "remote_full_validation": False,
                        "test_set_used": False,
                    },
                    "failure_reason": failure_reason,
                },
            )

        print(json.dumps({"status": "ok", "decision": decision, "out_dir": str(out_dir)}, sort_keys=True))
        return 0
    except Exception as exc:
        failure_reason = str(exc)
        write_json(
            out_dir / "evaluator_summary.json",
            {
                "schema_version": "phase4_evaluator_summary_v1",
                "program_id": args.program_id,
                "stage": "remote_sample_eval",
                "decision": "reject",
                "failure_reason": failure_reason,
                "hard_gates": {"remote_sample_eval_completed": False},
                "metrics": {},
                "descriptors": {"daily_stock_contract": CONTRACT.contract_id},
                "next_prompt_hint": "Fix the non-evolvable loader/evaluator issue before child generation.",
                "artifact_paths": {},
            },
        )
        write_lines(
            out_dir / "failure_report.md",
            [
                "# Failure Report",
                "",
                "## Failure Category",
                "",
                "remote_sample_eval_error",
                "",
                "## Exact Gate That Failed",
                "",
                failure_reason,
            ],
        )
        print(json.dumps({"status": "error", "error": failure_reason, "out_dir": str(out_dir)}, sort_keys=True), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
