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


DEFAULT_SEED_PROGRAM_ID = "PROG-20260430-000000"
DEFAULT_SEED_PROGRAM_PATH = Path("research/alphaevolve_lite/seeds/kalman_reversal_seed.py")


def _ensure_repo_import() -> None:
    repo_root = Path(__file__).resolve().parents[3]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))


_ensure_repo_import()

from research.alphaevolve_lite.splits import (  # noqa: E402
    DEFAULT_ANALYSIS_END_DATE,
    DEFAULT_ANALYSIS_START_DATE,
    DEFAULT_OUT_SAMPLE_START_DATE,
    IS_OS_SPLIT_ID,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Remote sample-evaluate a Phase 4 strategy program.")
    parser.add_argument("--csv-path", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--program-path", default="research/alphaevolve_lite/seeds/kalman_reversal_seed.py")
    parser.add_argument("--db-path", default="")
    parser.add_argument(
        "--reference-summary",
        default="",
        help="Optional seed/parent evaluator_summary.json used to flag metric-equivalent children.",
    )
    parser.add_argument(
        "--prior-sample-summary",
        action="append",
        default=[],
        help=(
            "Prior child evaluator_summary.json used to flag sample-metric replay against siblings. "
            "May be repeated."
        ),
    )
    parser.add_argument(
        "--reference-equivalence-tolerance",
        type=float,
        default=1e-9,
        help="Absolute tolerance for optional search-sample metric equivalence to the reference summary.",
    )
    parser.add_argument(
        "--start-date",
        default=DEFAULT_ANALYSIS_START_DATE,
        help="Inclusive analysis-window start. The active Phase 4 IS/OS window starts in 2011.",
    )
    parser.add_argument(
        "--end-date",
        default=DEFAULT_ANALYSIS_END_DATE,
        help="Inclusive analysis-window end. The active Phase 4 window ends with available 2025 data.",
    )
    parser.add_argument(
        "--out-sample-start",
        default=DEFAULT_OUT_SAMPLE_START_DATE,
        help="First calendar date assigned to the out-of-sample split.",
    )
    parser.add_argument("--chunksize", type=int, default=1_000_000)
    parser.add_argument("--max-input-rows", type=int)
    parser.add_argument("--top-n", type=int, default=500)
    parser.add_argument("--total-cost-bps", type=float, default=2.5)
    parser.add_argument("--cost-grid-bps", default="0,1,2.5,5,10")
    parser.add_argument("--null-seeds", type=int, default=5)
    parser.add_argument("--turnover-penalty", type=float, default=0.25)
    parser.add_argument("--missing-weight-penalty", type=float, default=5.0)
    parser.add_argument(
        "--program-kind",
        choices=["auto", "seed", "child"],
        default="auto",
        help=(
            "How to record the evaluated program. auto preserves legacy behavior: the canonical seed path "
            "is a seed, other paths are children. Use seed for deterministic seed-zoo parents."
        ),
    )
    parser.add_argument(
        "--strategy-family",
        default="",
        help="Optional strategy-family descriptor. Defaults to STRATEGY_FAMILY in the program module.",
    )
    parser.add_argument(
        "--min-portfolio-days",
        type=int,
        default=252,
        help="Minimum active portfolio days required when the visible sample is long enough.",
    )
    parser.add_argument(
        "--min-portfolio-day-coverage",
        type=float,
        default=0.80,
        help="Minimum fraction of visible rolling-universe days with an active portfolio.",
    )
    parser.add_argument("--program-id", default=DEFAULT_SEED_PROGRAM_ID)
    parser.add_argument(
        "--parent-program-id",
        default="",
        help=(
            "Parent program id for child sample evaluation. If omitted for a child, "
            "the reference-summary program_id is used when available."
        ),
    )
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

    from research.alphaevolve_lite.reproducibility import capture_git_reproducibility

    return capture_git_reproducibility(out_dir)


def write_lines(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def is_seed_program_path(resolved_program_path: Path) -> bool:
    """Return whether the evaluated program is the canonical generation-zero seed."""

    try:
        return resolved_program_path.resolve() == (Path.cwd() / DEFAULT_SEED_PROGRAM_PATH).resolve()
    except Exception:
        return str(resolved_program_path).replace("\\", "/").endswith(DEFAULT_SEED_PROGRAM_PATH.as_posix())


def child_parent_program_id(args: argparse.Namespace, reference_summary: dict[str, Any]) -> str:
    """Resolve child parent lineage for sample-evaluation database records."""

    if args.parent_program_id:
        return str(args.parent_program_id)
    reference_program_id = reference_summary.get("program_id") if isinstance(reference_summary, dict) else None
    if reference_program_id:
        return str(reference_program_id)
    return DEFAULT_SEED_PROGRAM_ID


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
    from research.alphaevolve_lite.reproducibility import capture_program_snapshot
    from research.alphaevolve_lite.sample_eval_baselines import (
        build_baseline_records,
        flatten_baseline_rows,
        summarize_baselines,
    )
    from research.alphaevolve_lite.sample_eval_metrics import (
        build_forward_returns_from_source,
        compare_search_sample_to_reference,
        compare_search_sample_to_references,
        cost_sensitivity_rows,
        is_os_degradation_metrics,
        portfolio_from_weights,
        portfolio_day_coverage_diagnostics,
        scorecard_from_metrics,
        split_metrics,
    )
    from research.alphaevolve_lite.splits import build_is_os_splits, write_split_manifest
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
    if args.reference_equivalence_tolerance < 0.0:
        print("--reference-equivalence-tolerance must be nonnegative", file=sys.stderr)
        return 2
    if args.min_portfolio_days < 1:
        print("--min-portfolio-days must be positive", file=sys.stderr)
        return 2
    if not 0.0 < args.min_portfolio_day_coverage <= 1.0:
        print("--min-portfolio-day-coverage must be in (0, 1]", file=sys.stderr)
        return 2
    git_status = write_git_status_artifacts(out_dir)
    reference_summary = {}
    if args.reference_summary:
        reference_path = Path(args.reference_summary)
        if not reference_path.exists():
            print(f"reference summary does not exist: {reference_path}", file=sys.stderr)
            return 2
        reference_summary = json.loads(reference_path.read_text(encoding="utf-8"))
    prior_sample_summaries: list[dict[str, Any]] = []
    for raw_path in args.prior_sample_summary:
        prior_path = Path(raw_path)
        if not prior_path.exists():
            print(f"prior sample summary does not exist: {prior_path}", file=sys.stderr)
            return 2
        prior_sample_summaries.append(json.loads(prior_path.read_text(encoding="utf-8")))

    diagnostics: list[dict[str, Any]] = []
    decision = "reject"
    failure_reason = None

    try:
        strategy_module, resolved_program_path = load_strategy_module(args.program_path)
        program_snapshot = capture_program_snapshot(resolved_program_path, out_dir)
        canonical_seed_path = is_seed_program_path(resolved_program_path)
        if args.program_kind == "seed":
            is_seed_program = True
        elif args.program_kind == "child":
            is_seed_program = False
        else:
            is_seed_program = canonical_seed_path
        if is_seed_program and args.parent_program_id:
            raise RuntimeError("seed sample evaluation must not set --parent-program-id")
        if not is_seed_program and args.program_id == DEFAULT_SEED_PROGRAM_ID:
            raise RuntimeError(
                "child sample evaluation requires --program-id; refusing to record a child under the seed id"
            )
        resolved_parent_program_id = None if is_seed_program else child_parent_program_id(args, reference_summary)
        strategy_family = (
            args.strategy_family
            or str(getattr(strategy_module, "STRATEGY_FAMILY", "") or "kalman_innovation_reversal")
        )
        strategy_id = str(getattr(strategy_module, "STRATEGY_ID", resolved_program_path.stem))
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

        splits = build_is_os_splits(eligible[CONTRACT.date], out_sample_start=args.out_sample_start)
        membership, universe_summary = build_monthly_rolling_universe(eligible, top_n=args.top_n)
        universe_panel = apply_monthly_universe(eligible, membership)
        if universe_panel.empty:
            raise RuntimeError("rolling universe produced no sample rows")

        eval_panel = build_forward_returns_from_source(universe_panel, eligible, CONTRACT)
        strategy_params = dict(strategy_module.DEFAULT_PARAMS)
        signal = strategy_module.compute_signal(eval_panel, strategy_params)
        ranked = strategy_module.rank_or_transform_signal(signal, eval_panel, strategy_params)
        raw_weights = strategy_module.construct_portfolio(ranked, eval_panel, strategy_params)
        weights = strategy_module.apply_risk_controls(raw_weights, eval_panel, strategy_params)
        full_portfolio, positions = portfolio_from_weights(eval_panel, weights, args.total_cost_bps, CONTRACT)
        analysis_end = splits[-1].end
        portfolio = full_portfolio.loc[full_portfolio["DlyCalDt"] <= analysis_end].copy()
        positions = positions.loc[positions[CONTRACT.date] <= analysis_end].copy()
        if portfolio.empty:
            raise RuntimeError("seed produced no nonzero portfolio returns")

        visible_splits = [split for split in splits if split.name in {"in_sample", "out_sample"}]
        portfolio_coverage = portfolio_day_coverage_diagnostics(
            portfolio,
            universe_panel,
            CONTRACT,
            analysis_end=analysis_end,
            min_portfolio_days=args.min_portfolio_days,
            min_portfolio_day_coverage=args.min_portfolio_day_coverage,
        )
        diagnostics.extend(
            {"check": key, "status": "info", "value": value}
            for key, value in portfolio_coverage.items()
        )
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
        metrics["is_os_degradation"] = is_os_degradation_metrics(
            metrics["in_sample"],
            metrics["out_sample"],
        )

        baseline_records = build_baseline_records(
            panel=eval_panel,
            reference_weights=weights,
            contract=CONTRACT,
            analysis_end=analysis_end,
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
        reference_comparison = compare_search_sample_to_reference(
            metrics,
            reference_summary,
            tolerance=args.reference_equivalence_tolerance,
        )
        prior_sample_comparison = compare_search_sample_to_references(
            metrics,
            prior_sample_summaries,
            tolerance=args.reference_equivalence_tolerance,
        )

        hard_gates = {
            "daily_stock_contract_v1_columns_present": True,
            "rolling_universe_nonempty": bool(len(membership)),
            "portfolio_nonempty": bool(len(portfolio)),
            "portfolio_min_active_days": bool(portfolio_coverage["portfolio_min_days_pass"]),
            "portfolio_day_coverage_within_sample_tolerance": bool(
                portfolio_coverage["portfolio_day_coverage_pass"]
            ),
            "max_weight_reported": "max_weight" in metrics["search_sample"],
            "test_metrics_locked": True,
            "missing_held_weight_within_sample_tolerance": metrics["search_sample"]["max_missing_held_weight"] <= 0.05,
            "duplicate_diagnostics_written": (out_dir / "duplicate_diagnostics.csv").exists(),
            "git_status_recorded": (out_dir / "git_status.txt").exists(),
            "git_worktree_clean": not bool(git_status.get("git_dirty")),
            "git_head_matches_origin_main": bool(git_status.get("git_head_matches_origin_main")),
            "code_snapshot_recorded": (out_dir / str(program_snapshot["program_snapshot_path"])).exists(),
            "forward_return_source_contract_recorded": True,
            "null_baselines_written": (out_dir / "null_baselines.csv").exists(),
            "turnover_aware_score_reported": "turnover_aware_score" in metrics["search_sample"],
            "exposure_diagnostics_reported": "mean_gross_exposure" in metrics["search_sample"],
        }
        if reference_summary:
            hard_gates["not_metric_equivalent_to_reference"] = not bool(
                reference_comparison["metric_equivalent_to_reference"]
            )
        if prior_sample_summaries:
            hard_gates["not_metric_equivalent_to_prior_sample"] = not bool(
                prior_sample_comparison["metric_equivalent_to_any_reference"]
            )
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
            split_id=IS_OS_SPLIT_ID,
            split_policy="fixed_calendar_is_os",
        )
        portfolio.to_csv(out_dir / "returns_by_split.csv", index=False)
        positions.head(5000).to_csv(out_dir / "positions_sample.csv", index=False)
        scorecard.to_csv(out_dir / "scorecard.csv", index=False)
        pd.DataFrame(cost_rows).to_csv(out_dir / "cost_sensitivity.csv", index=False)
        pd.DataFrame(diagnostics).to_csv(out_dir / "diagnostics.csv", index=False)

        manifest = {
            "run_id": run_id,
            "program_id": args.program_id,
            "parent_program_id": resolved_parent_program_id,
            "stage": "remote_sample_eval",
            "program_kind": "seed" if is_seed_program else "child",
            "strategy_family": strategy_family,
            "strategy_id": strategy_id,
            "program_path": str(resolved_program_path),
            **program_snapshot,
            "reference_summary_path": args.reference_summary,
            "prior_sample_summary_paths": args.prior_sample_summary,
            "reference_equivalence_tolerance": args.reference_equivalence_tolerance,
            "csv_path": args.csv_path,
            "start_date": args.start_date,
            "end_date": args.end_date,
            "out_sample_start": args.out_sample_start,
            "split_id": IS_OS_SPLIT_ID,
            "top_n": args.top_n,
            "total_cost_bps": args.total_cost_bps,
            "cost_grid_bps": costs,
            "null_seeds": args.null_seeds,
            "turnover_penalty": args.turnover_penalty,
            "missing_weight_penalty": args.missing_weight_penalty,
            "min_portfolio_days": args.min_portfolio_days,
            "min_portfolio_day_coverage": args.min_portfolio_day_coverage,
            "portfolio_coverage": portfolio_coverage,
            "daily_stock_contract": CONTRACT.contract_id,
            "signal_panel_source": "rolling_top500_universe_panel",
            "forward_return_source": "eligible_static_panel",
            "forward_return_contract": "signal_universe_t_return_source_eligible_t_plus_1_v1",
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
                "parent_program_id": resolved_parent_program_id,
                "metrics": metrics,
                "baseline_summary": baseline_summary,
                "sample_coverage": portfolio_coverage,
                "reference_comparison": reference_comparison,
                "prior_sample_comparison": prior_sample_comparison,
            },
        )
        write_json(
            out_dir / "evaluator_summary.json",
            {
                "schema_version": "phase4_evaluator_summary_v1",
                "program_id": args.program_id,
                "parent_program_id": resolved_parent_program_id,
                "stage": "remote_sample_eval",
                "decision": decision,
                "failure_reason": failure_reason,
                "hard_gates": hard_gates,
                "metrics": metrics,
                "baseline_summary": baseline_summary,
                "sample_coverage": portfolio_coverage,
                "reference_comparison": reference_comparison,
                "prior_sample_comparison": prior_sample_comparison,
                "descriptors": {
                    "daily_stock_contract": CONTRACT.contract_id,
                    "strategy_family": strategy_family,
                    "strategy_id": strategy_id,
                    "program_path": str(resolved_program_path),
                    "program_snapshot_path": program_snapshot["program_snapshot_path"],
                    "program_sha256": program_snapshot["program_sha256"],
                    "parent_program_id": resolved_parent_program_id,
                    "prior_sample_equivalent_program_ids": prior_sample_comparison[
                        "equivalent_reference_program_ids"
                    ],
                    "universe_policy": UNIVERSE_POLICY_ID,
                    "split_id": IS_OS_SPLIT_ID,
                    "out_sample_start": args.out_sample_start,
                    "signal_panel_source": "rolling_top500_universe_panel",
                    "forward_return_source": "eligible_static_panel",
                    "forward_return_contract": "signal_universe_t_return_source_eligible_t_plus_1_v1",
                    "data_scope": "daily_stock_only",
                    "portfolio_day_coverage": portfolio_coverage["portfolio_day_coverage"],
                    "mean_gross_exposure": metrics["search_sample"].get("mean_gross_exposure"),
                    "max_gross_exposure": metrics["search_sample"].get("max_gross_exposure"),
                    "max_abs_net_exposure": metrics["search_sample"].get("max_abs_net_exposure"),
                    "git_dirty": git_status["git_dirty"],
                    "git_commit": git_status["git_commit"],
                    "git_origin_main_commit": git_status["git_origin_main_commit"],
                    "git_head_matches_origin_main": git_status["git_head_matches_origin_main"],
                },
                "next_prompt_hint": "If sample_pass, compare IS and OS behavior against seed, null baselines, and sibling children before promotion. Do not treat OS as a pristine final test after repeated use.",
                "artifact_paths": {
                    "scorecard": "scorecard.csv",
                    "diagnostics": "diagnostics.csv",
                    "cost_sensitivity": "cost_sensitivity.csv",
                    "duplicate_diagnostics": "duplicate_diagnostics.csv",
                    "null_baselines": "null_baselines.csv",
                    "baseline_summary": "baseline_summary.json",
                    "git_status": "git_status.txt",
                    "git_diff_stat": "git_diff_stat.txt",
                    "program_snapshot": program_snapshot["program_snapshot_path"],
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
                f"- parent_program_id: `{resolved_parent_program_id}`",
                f"- daily_stock_contract: `{CONTRACT.contract_id}`",
                f"- rows_after_static_eligibility: `{eligibility_diag.get('rows_after_static_eligibility')}`",
                f"- universe_rows: `{len(universe_panel)}`",
                f"- portfolio_days: `{len(portfolio)}`",
                f"- split_id: `{IS_OS_SPLIT_ID}`",
                "- signal_panel_source: `rolling_top500_universe_panel`",
                "- forward_return_source: `eligible_static_panel`",
                "- forward_return_contract: `signal_universe_t_return_source_eligible_t_plus_1_v1`",
                f"- in_sample_range: `{splits[0].start.date().isoformat()} to {splits[0].end.date().isoformat()}`",
                f"- out_sample_range: `{splits[1].start.date().isoformat()} to {splits[1].end.date().isoformat()}`",
                f"- visible_universe_days: `{portfolio_coverage['visible_universe_days']}`",
                f"- portfolio_day_coverage: `{portfolio_coverage['portfolio_day_coverage']}`",
                f"- min_required_portfolio_days: `{portfolio_coverage['min_required_portfolio_days']}`",
                f"- reference_metric_equivalent: `{reference_comparison['metric_equivalent_to_reference']}`",
                f"- reference_max_abs_metric_delta: `{reference_comparison['max_abs_metric_delta']}`",
                f"- prior_sample_metric_equivalent: `{prior_sample_comparison['metric_equivalent_to_any_reference']}`",
                (
                    "- prior_sample_equivalent_program_ids: `"
                    f"{prior_sample_comparison['equivalent_reference_program_ids']}`"
                ),
                f"- is_sharpe: `{metrics['in_sample']['sharpe']}`",
                f"- is_turnover: `{metrics['in_sample']['turnover']}`",
                f"- os_sharpe: `{metrics['out_sample']['sharpe']}`",
                f"- os_turnover: `{metrics['out_sample']['turnover']}`",
                f"- is_to_os_sharpe_degradation: `{metrics['is_os_degradation']['is_to_os_sharpe_degradation']}`",
                f"- search_sample_sharpe: `{metrics['search_sample']['sharpe']}`",
                f"- turnover_aware_score: `{metrics['search_sample']['turnover_aware_score']}`",
                f"- max_weight: `{metrics['search_sample']['max_weight']}`",
                f"- mean_gross_exposure: `{metrics['search_sample']['mean_gross_exposure']}`",
                f"- max_gross_exposure: `{metrics['search_sample']['max_gross_exposure']}`",
                f"- max_abs_net_exposure: `{metrics['search_sample']['max_abs_net_exposure']}`",
                f"- max_missing_held_weight: `{metrics['search_sample']['max_missing_held_weight']}`",
                f"- duplicate_groups_with_conflicts: `{duplicate_summary['duplicate_groups_with_conflicts']}`",
                f"- git_dirty: `{git_status['git_dirty']}`",
                f"- git_head_matches_origin_main: `{git_status['git_head_matches_origin_main']}`",
                f"- program_sha256: `{program_snapshot['program_sha256']}`",
            ],
        )

        if args.db_path:
            init_db(args.db_path)
            insert_program_record(
                args.db_path,
                {
                    "program_id": args.program_id,
                    "parent_id": resolved_parent_program_id,
                    "root_id": "CAND-20260423-001",
                    "branch_id": "BRANCH-CAND-20260423-001-001",
                    "generation": 0 if is_seed_program else 1,
                    "island": "daily_stock_signal",
                    "mutation_surface": "seed_zoo" if is_seed_program and not canonical_seed_path else (
                        "seed" if is_seed_program else "child_program"
                    ),
                    "data_scope": "daily_stock_only",
                    "status": "seed_sample_evaluated" if is_seed_program else "child_sample_evaluated",
                    "program_path": str(resolved_program_path),
                    "evaluator_summary_path": str(out_dir / "evaluator_summary.json"),
                    "metrics": metrics,
                    "descriptors": {
                        "daily_stock_contract": CONTRACT.contract_id,
                        "strategy_family": strategy_family,
                        "strategy_id": strategy_id,
                        "program_path": str(resolved_program_path),
                        "program_snapshot_path": program_snapshot["program_snapshot_path"],
                        "program_sha256": program_snapshot["program_sha256"],
                        "parent_program_id": resolved_parent_program_id,
                        "prior_sample_equivalent_program_ids": prior_sample_comparison[
                            "equivalent_reference_program_ids"
                        ],
                        "portfolio_coverage": portfolio_coverage,
                        "split_id": IS_OS_SPLIT_ID,
                        "out_sample_start": args.out_sample_start,
                        "signal_panel_source": "rolling_top500_universe_panel",
                        "forward_return_source": "eligible_static_panel",
                        "forward_return_contract": "signal_universe_t_return_source_eligible_t_plus_1_v1",
                        "mean_gross_exposure": metrics["search_sample"].get("mean_gross_exposure"),
                        "max_gross_exposure": metrics["search_sample"].get("max_gross_exposure"),
                        "max_abs_net_exposure": metrics["search_sample"].get("max_abs_net_exposure"),
                        "git_commit": git_status["git_commit"],
                        "git_origin_main_commit": git_status["git_origin_main_commit"],
                        "git_head_matches_origin_main": git_status["git_head_matches_origin_main"],
                    },
                    "hard_gates": hard_gates,
                    "validation_exposure": {
                        "remote_sample_eval": True,
                        "remote_full_validation": False,
                        "split_id": IS_OS_SPLIT_ID,
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
                "parent_program_id": None,
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
