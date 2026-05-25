"""Evaluate the daily-stock expression seed catalog on the remote data machine."""

from __future__ import annotations

import argparse
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _ensure_repo_import() -> None:
    repo_root = Path(__file__).resolve().parents[3]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))


_ensure_repo_import()

from research.alphaevolve_lite.splits import (  # noqa: E402
    DEFAULT_ANALYSIS_END_DATE,
    DEFAULT_ANALYSIS_START_DATE,
    DEFAULT_OUT_SAMPLE_START_DATE,
)
from research.alphaevolve_lite.expression_eval_records import (  # noqa: E402
    expression_sample_hard_gates as _expression_sample_hard_gates,
    ranking_row as _ranking_row,
    scorecard_rows as _scorecard_rows,
    status_from_metrics as _status_from_metrics,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv-path", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument(
        "--start-date",
        default=DEFAULT_ANALYSIS_START_DATE,
        help="Inclusive analysis-window start. Active Phase 4 starts in 2011.",
    )
    parser.add_argument(
        "--end-date",
        default=DEFAULT_ANALYSIS_END_DATE,
        help="Inclusive analysis-window end. Active Phase 4 ends with available 2025 data.",
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
    parser.add_argument("--turnover-penalty", type=float, default=0.25)
    parser.add_argument("--missing-weight-penalty", type=float, default=5.0)
    parser.add_argument("--long-quantile", type=float, default=0.9)
    parser.add_argument("--short-quantile", type=float, default=0.1)
    parser.add_argument("--gross-exposure", type=float, default=1.0)
    parser.add_argument("--max-weight", type=float, default=0.02)
    parser.add_argument("--min-names-per-side", type=int, default=5)
    parser.add_argument("--min-group-count", type=int, default=5)
    parser.add_argument("--max-window", type=int, default=252)
    parser.add_argument("--max-abs-net-exposure", type=float, default=1.0e-9)
    parser.add_argument("--max-missing-held-weight", type=float, default=0.05)
    parser.add_argument("--min-portfolio-days", type=int, default=252)
    parser.add_argument("--min-portfolio-day-coverage", type=float, default=0.80)
    parser.add_argument(
        "--seed-id",
        action="append",
        default=[],
        help="Evaluate only these expression seed ids. May be repeated.",
    )
    parser.add_argument("--seed-limit", type=int, default=0)
    parser.add_argument("--run-id", default="")
    return parser.parse_args()


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _select_seeds(seed_ids: list[str], seed_limit: int):
    from research.alphaevolve_lite.expression_evolution import DEFAULT_EXPRESSION_SEEDS

    seeds = list(DEFAULT_EXPRESSION_SEEDS)
    if seed_ids:
        wanted = set(seed_ids)
        missing = sorted(wanted - {seed.expression_id for seed in seeds})
        if missing:
            raise ValueError(f"unknown expression seed ids: {missing}")
        seeds = [seed for seed in seeds if seed.expression_id in wanted]
    if seed_limit:
        if seed_limit < 1:
            raise ValueError("--seed-limit must be positive when supplied")
        seeds = seeds[:seed_limit]
    return seeds


def main() -> int:
    import pandas as pd

    from research.alphaevolve_lite.artifact_io import write_json
    from research.alphaevolve_lite.daily_stock_contract import CONTRACT, eligibility_query_description
    from research.alphaevolve_lite.daily_stock_loader import (
        apply_duplicate_policy,
        apply_static_eligibility,
        load_daily_stock_window,
    )
    from research.alphaevolve_lite.expression_evolution import (
        ExpressionEvaluationConfig,
        evaluate_expression_signal,
        construct_expression_portfolio,
        expression_interface_markdown,
        expression_seed_library_rows,
    )
    from research.alphaevolve_lite.reproducibility import capture_git_reproducibility
    from research.alphaevolve_lite.sample_eval_metrics import (
        build_forward_returns_from_source,
        cost_sensitivity_rows,
        is_os_degradation_metrics,
        portfolio_day_coverage_diagnostics,
        portfolio_from_weights,
        split_metrics,
    )
    from research.alphaevolve_lite.splits import IS_OS_SPLIT_ID, build_is_os_splits, write_split_manifest
    from research.alphaevolve_lite.universe import (
        UNIVERSE_POLICY_ID,
        apply_monthly_universe,
        build_monthly_rolling_universe,
        write_universe_artifacts,
    )

    args = parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    run_id = args.run_id or f"expression_seed_zoo-{utc_now_iso().replace(':', '').replace('-', '')}-{uuid.uuid4().hex[:8]}"
    costs = [float(item.strip()) for item in args.cost_grid_bps.split(",") if item.strip()]
    if not costs:
        print("--cost-grid-bps must include at least one numeric cost", file=sys.stderr)
        return 2
    if args.min_portfolio_days < 1:
        print("--min-portfolio-days must be positive", file=sys.stderr)
        return 2
    if not 0.0 < args.min_portfolio_day_coverage <= 1.0:
        print("--min-portfolio-day-coverage must be in (0, 1]", file=sys.stderr)
        return 2

    seeds = _select_seeds(args.seed_id, args.seed_limit)
    config = ExpressionEvaluationConfig(
        long_quantile=args.long_quantile,
        short_quantile=args.short_quantile,
        gross_exposure=args.gross_exposure,
        max_weight=args.max_weight,
        min_names_per_side=args.min_names_per_side,
        min_group_count=args.min_group_count,
        max_window=args.max_window,
    )

    git_status = capture_git_reproducibility(out_dir)
    (out_dir / "expression_interface.md").write_text(
        expression_interface_markdown(),
        encoding="utf-8",
    )
    write_json(out_dir / "expression_seed_library.json", expression_seed_library_rows(seeds))

    diagnostics: list[dict[str, Any]] = []
    try:
        raw, load_diag = load_daily_stock_window(
            args.csv_path,
            start_date=args.start_date,
            end_date=args.end_date,
            chunksize=args.chunksize,
            max_input_rows=args.max_input_rows,
        )
        diagnostics.extend({"check": key, "status": "info", "value": value} for key, value in load_diag.items())
        deduped, dup_diag = apply_duplicate_policy(raw)
        diagnostics.extend({"check": key, "status": "info", "value": value} for key, value in dup_diag.items())
        eligible, eligibility_diag = apply_static_eligibility(deduped)
        diagnostics.extend(
            {"check": key, "status": "info", "value": value} for key, value in eligibility_diag.items()
        )
        if eligible.empty:
            raise RuntimeError("no eligible rows after daily_stock_contract_v1 filters")

        splits = build_is_os_splits(eligible[CONTRACT.date], out_sample_start=args.out_sample_start)
        membership, universe_summary = build_monthly_rolling_universe(eligible, top_n=args.top_n)
        universe_panel = apply_monthly_universe(eligible, membership)
        if universe_panel.empty:
            raise RuntimeError("rolling universe produced no expression-evaluation rows")
        eval_panel = build_forward_returns_from_source(universe_panel, eligible, CONTRACT)
        analysis_end = splits[-1].end

        artifact_paths = {
            "expression_interface": str(out_dir / "expression_interface.md"),
            "expression_seed_library": str(out_dir / "expression_seed_library.json"),
            "split_manifest": str(out_dir / "split_manifest.yaml"),
        }
        artifact_paths.update(write_universe_artifacts(out_dir, membership, universe_summary))
        write_split_manifest(
            out_dir / "split_manifest.yaml",
            splits=splits,
            calendar_count=int(eligible[CONTRACT.date].dropna().nunique()),
            universe_policy=UNIVERSE_POLICY_ID,
            duplicate_policy=dup_diag,
            split_id=IS_OS_SPLIT_ID,
        )

        visible_splits = [split for split in splits if split.name in {"in_sample", "out_sample"}]
        results: list[dict[str, Any]] = []
        cost_rows: list[dict[str, Any]] = []

        for seed in seeds:
            result: dict[str, Any] = {
                "expression_id": seed.expression_id,
                "title": seed.title,
                "thesis": seed.thesis,
                "expression": seed.expression,
                "mechanism": seed.mechanism,
                "expected_effect": seed.expected_effect,
                "tags": list(seed.tags),
                "status": "expression_error",
                "failure_reason": None,
                "metrics": {},
                "portfolio_coverage": {},
                "hard_gates": {},
            }
            try:
                signal = evaluate_expression_signal(seed, eval_panel, config=config, contract=CONTRACT)
                weights = construct_expression_portfolio(signal, eval_panel, config=config, contract=CONTRACT)
                full_portfolio, positions = portfolio_from_weights(
                    eval_panel,
                    weights,
                    args.total_cost_bps,
                    CONTRACT,
                )
                portfolio = full_portfolio.loc[full_portfolio["DlyCalDt"] <= analysis_end].copy()
                positions = positions.loc[positions[CONTRACT.date] <= analysis_end].copy()
                if portfolio.empty:
                    raise RuntimeError("expression produced no nonzero portfolio returns")
                portfolio_coverage = portfolio_day_coverage_diagnostics(
                    portfolio,
                    universe_panel,
                    CONTRACT,
                    analysis_end=analysis_end,
                    min_portfolio_days=args.min_portfolio_days,
                    min_portfolio_day_coverage=args.min_portfolio_day_coverage,
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
                result["metrics"] = metrics
                result["portfolio_coverage"] = portfolio_coverage
                result["position_rows"] = int(len(positions))
                result["signal_non_null_ratio"] = float(signal.notna().mean())
                result["status"] = _status_from_metrics(
                    metrics,
                    portfolio_coverage,
                    max_weight=args.max_weight,
                    max_abs_net_exposure=args.max_abs_net_exposure,
                    max_missing_held_weight=args.max_missing_held_weight,
                )
                result["hard_gates"] = _expression_sample_hard_gates(
                    metrics,
                    portfolio_coverage,
                    max_weight=args.max_weight,
                    max_abs_net_exposure=args.max_abs_net_exposure,
                    max_missing_held_weight=args.max_missing_held_weight,
                )
                for row in cost_sensitivity_rows(
                    portfolio,
                    costs,
                    turnover_penalty=args.turnover_penalty,
                    missing_weight_penalty=args.missing_weight_penalty,
                ):
                    cost_rows.append({"expression_id": seed.expression_id, **row})
            except Exception as exc:  # pragma: no cover - remote artifact path.
                result["failure_reason"] = str(exc)
            results.append(result)

        rankings = [_ranking_row(result) for result in results]
        rankings_df = pd.DataFrame(rankings)
        if not rankings_df.empty and "search_turnover_aware_score" in rankings_df:
            rankings_df["_status_rank"] = rankings_df["status"].map(
                {
                    "expression_sample_pass": 0,
                    "expression_sample_review": 1,
                    "expression_error": 2,
                }
            ).fillna(3)
            rankings_df = rankings_df.sort_values(
                ["_status_rank", "search_turnover_aware_score", "out_sample_sharpe"],
                ascending=[True, False, False],
                na_position="last",
            ).drop(columns=["_status_rank"])
        rankings_df.to_csv(out_dir / "expression_rankings.csv", index=False)
        pd.DataFrame(_scorecard_rows(results)).to_csv(out_dir / "expression_scorecard.csv", index=False)
        pd.DataFrame(cost_rows).to_csv(out_dir / "expression_cost_sensitivity.csv", index=False)

        summary = {
            "run_id": run_id,
            "status": "ok",
            "contract_id": CONTRACT.contract_id,
            "universe_policy": UNIVERSE_POLICY_ID,
            "split_id": IS_OS_SPLIT_ID,
            "eligibility_query": eligibility_query_description(CONTRACT),
            "config": vars(args),
            "expression_config": vars(config),
            "git_status": git_status,
            "diagnostics": diagnostics,
            "artifact_paths": {
                **artifact_paths,
                "expression_rankings": str(out_dir / "expression_rankings.csv"),
                "expression_scorecard": str(out_dir / "expression_scorecard.csv"),
                "expression_cost_sensitivity": str(out_dir / "expression_cost_sensitivity.csv"),
                "expression_evaluator_summary": str(out_dir / "expression_evaluator_summary.json"),
            },
            "result_counts": {
                "seed_count": len(results),
                "sample_pass": sum(result.get("status") == "expression_sample_pass" for result in results),
                "sample_review": sum(result.get("status") == "expression_sample_review" for result in results),
                "error": sum(result.get("status") == "expression_error" for result in results),
            },
            "results": results,
        }
        write_json(out_dir / "expression_evaluator_summary.json", summary)
        print(
            write_json(
                out_dir / "run_result.json",
                {
                    "status": "ok",
                    "run_id": run_id,
                    "out_dir": str(out_dir),
                    "seed_count": len(results),
                    "sample_pass": summary["result_counts"]["sample_pass"],
                    "sample_review": summary["result_counts"]["sample_review"],
                    "error": summary["result_counts"]["error"],
                },
            ).read_text(encoding="utf-8"),
        )
        return 0
    except Exception as exc:
        summary = {
            "run_id": run_id,
            "status": "error",
            "failure_reason": str(exc),
            "contract_id": CONTRACT.contract_id,
            "git_status": git_status,
            "diagnostics": diagnostics,
        }
        write_json(out_dir / "expression_evaluator_summary.json", summary)
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
