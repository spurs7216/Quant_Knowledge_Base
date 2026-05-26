"""Run deterministic bridge-policy follow-up for daily-stock expressions.

This runner promotes the bridge from an episode side diagnostic into an
explicit evaluation contract.  It does not call Qwen, does not promote a
strategy, and does not use a final test set.  Its job is to answer one narrow
question: does a child expression only look interesting because a slower
portfolio bridge changes the cost/turnover economics, and if so does it beat
the parent under that same bridge contract?
"""

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


DEFAULT_PARENT_SEED_ID = "expr_smoothed_rev"
DEFAULT_CHILD_EXPRESSION_ID = "expr_smoothed_rev_liq_bridge_20260526"
DEFAULT_CHILD_TITLE = "Smoothed liquid reversal bridge candidate"
DEFAULT_CHILD_THESIS = (
    "A smoothed residual reversal signal may survive costs better when liquidity "
    "confidence is explicit and the evaluator uses a slower bridge."
)
DEFAULT_CHILD_EXPRESSION = (
    "rank(-rolling_mean(rolling_sum(excess_ret, 5), 3)) * "
    "rank(log1p_abs(dollar_volume))"
)
DEFAULT_CHILD_MECHANISM = "smoothed reversal gated by dollar-volume confidence"
DEFAULT_CHILD_EXPECTED_EFFECT = (
    "Retain broad reversal coverage while reducing cost fragility under 5-day "
    "rebalance or signal-decay bridge policies."
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
    parser.add_argument(
        "--bridge-variant-grid",
        default="daily,rebalance_5,signal_decay_5",
        help="Comma-separated bridge contracts to compare parent and child under.",
    )
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
    parser.add_argument("--parent-seed-id", default=DEFAULT_PARENT_SEED_ID)
    parser.add_argument("--child-expression-id", default=DEFAULT_CHILD_EXPRESSION_ID)
    parser.add_argument("--child-title", default=DEFAULT_CHILD_TITLE)
    parser.add_argument("--child-thesis", default=DEFAULT_CHILD_THESIS)
    parser.add_argument("--child-expression", default=DEFAULT_CHILD_EXPRESSION)
    parser.add_argument("--child-mechanism", default=DEFAULT_CHILD_MECHANISM)
    parser.add_argument("--child-expected-effect", default=DEFAULT_CHILD_EXPECTED_EFFECT)
    parser.add_argument("--pass-margin", type=float, default=0.0)
    parser.add_argument("--run-id", default="")
    return parser.parse_args()


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def main() -> int:
    import pandas as pd

    from research.alphaevolve_lite.artifact_io import write_json
    from research.alphaevolve_lite.daily_stock_contract import CONTRACT, eligibility_query_description
    from research.alphaevolve_lite.daily_stock_loader import (
        apply_duplicate_policy,
        apply_static_eligibility,
        load_daily_stock_window,
    )
    from research.alphaevolve_lite.expression_bridge_variants import (
        bridge_variant_names,
        parse_bridge_variant_grid,
    )
    from research.alphaevolve_lite.expression_eval_records import (
        expression_success_flags,
    )
    from research.alphaevolve_lite.expression_evolution import (
        DEFAULT_EXPRESSION_SEEDS,
        ExpressionEvaluationConfig,
        ExpressionSpec,
        expression_interface_markdown,
        expression_seed_library_rows,
    )
    from research.alphaevolve_lite.reproducibility import capture_git_reproducibility
    from research.alphaevolve_lite.sample_eval_metrics import build_forward_returns_from_source
    from research.alphaevolve_lite.splits import IS_OS_SPLIT_ID, build_is_os_splits, write_split_manifest
    from research.alphaevolve_lite.universe import (
        UNIVERSE_POLICY_ID,
        apply_monthly_universe,
        build_monthly_rolling_universe,
        write_universe_artifacts,
    )

    args = parse_args()
    try:
        _validate_args(args)
        costs = _parse_float_list(args.cost_grid_bps, "--cost-grid-bps")
        bridge_variants = parse_bridge_variant_grid(args.bridge_variant_grid)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 2

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    run_id = args.run_id or (
        f"expression_bridge_followup-"
        f"{utc_now_iso().replace(':', '').replace('-', '')}-{uuid.uuid4().hex[:8]}"
    )
    git_status = capture_git_reproducibility(out_dir)

    seed_by_id = {seed.expression_id: seed for seed in DEFAULT_EXPRESSION_SEEDS}
    if args.parent_seed_id not in seed_by_id:
        print(f"unknown parent seed id: {args.parent_seed_id}", file=sys.stderr)
        return 2
    parent = seed_by_id[args.parent_seed_id]
    child = ExpressionSpec(
        expression_id=args.child_expression_id,
        title=args.child_title,
        thesis=args.child_thesis,
        expression=args.child_expression,
        mechanism=args.child_mechanism,
        expected_effect=args.child_expected_effect,
        tags=("bridge_policy_followup", "reversal", "liquidity", "cost_conversion"),
    )
    specs = [parent, child]
    config = ExpressionEvaluationConfig(
        long_quantile=args.long_quantile,
        short_quantile=args.short_quantile,
        gross_exposure=args.gross_exposure,
        max_weight=args.max_weight,
        min_names_per_side=args.min_names_per_side,
        min_group_count=args.min_group_count,
        max_window=args.max_window,
    )

    write_json(out_dir / "expression_seed_library.json", expression_seed_library_rows([parent]))
    write_json(out_dir / "expression_bridge_followup_candidate.json", _candidate_record(parent, child))
    (out_dir / "expression_interface.md").write_text(expression_interface_markdown(), encoding="utf-8")

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
            raise RuntimeError("rolling universe produced no bridge-followup rows")
        eval_panel = build_forward_returns_from_source(universe_panel, eligible, CONTRACT)
        analysis_end = splits[-1].end

        artifact_paths = {
            "expression_interface": str(out_dir / "expression_interface.md"),
            "expression_seed_library": str(out_dir / "expression_seed_library.json"),
            "expression_bridge_followup_candidate": str(
                out_dir / "expression_bridge_followup_candidate.json"
            ),
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

        results: list[dict[str, Any]] = []
        cost_rows: list[dict[str, Any]] = []
        for spec in specs:
            record_type = "parent_baseline" if spec.expression_id == parent.expression_id else "bridge_child"
            spec_results, spec_cost_rows = _evaluate_spec_under_bridges(
                spec,
                record_type=record_type,
                parent_expression_id=parent.expression_id if record_type == "bridge_child" else None,
                eval_panel=eval_panel,
                universe_panel=universe_panel,
                splits=splits,
                analysis_end=analysis_end,
                costs=costs,
                args=args,
                config=config,
                bridge_variants=bridge_variants,
            )
            results.extend(spec_results)
            cost_rows.extend(spec_cost_rows)

        parent_by_bridge = {
            result["bridge_variant"]: result
            for result in results
            if result.get("record_type") == "parent_baseline"
        }
        for result in results:
            if result.get("record_type") == "bridge_child":
                parent_result = parent_by_bridge.get(str(result.get("bridge_variant")))
                result["success_flags"] = expression_success_flags(
                    result,
                    parent_result=parent_result,
                    root_result=parent_result,
                    pass_margin=args.pass_margin,
                )
            else:
                result["success_flags"] = {}

        comparison_rows = _comparison_rows(results)
        rankings_df = pd.DataFrame(_ranking_rows(results))
        if not rankings_df.empty:
            rankings_df = rankings_df.sort_values(
                ["bridge_variant", "record_type", "search_turnover_aware_score"],
                ascending=[True, True, False],
                na_position="last",
            )
        scorecard = _scorecard_rows(results)
        rankings_df.to_csv(out_dir / "expression_bridge_followup_rankings.csv", index=False)
        pd.DataFrame(scorecard).to_csv(out_dir / "expression_bridge_followup_scorecard.csv", index=False)
        pd.DataFrame(comparison_rows).to_csv(
            out_dir / "expression_bridge_followup_comparison.csv",
            index=False,
        )
        pd.DataFrame(cost_rows).to_csv(
            out_dir / "expression_bridge_followup_cost_sensitivity.csv",
            index=False,
        )

        promising = [
            row["bridge_variant"]
            for row in comparison_rows
            if row.get("bridge_contract_followup_pass") is True
        ]
        summary = {
            "run_id": run_id,
            "status": "ok",
            "contract_id": CONTRACT.contract_id,
            "universe_policy": UNIVERSE_POLICY_ID,
            "split_id": IS_OS_SPLIT_ID,
            "eligibility_query": eligibility_query_description(CONTRACT),
            "config": vars(args),
            "expression_config": {
                **vars(config),
                "bridge_variants": bridge_variant_names(bridge_variants),
            },
            "git_status": git_status,
            "diagnostics": diagnostics,
            "artifact_paths": {
                **artifact_paths,
                "expression_bridge_followup_summary": str(
                    out_dir / "expression_bridge_followup_summary.json"
                ),
                "expression_bridge_followup_rankings": str(
                    out_dir / "expression_bridge_followup_rankings.csv"
                ),
                "expression_bridge_followup_scorecard": str(
                    out_dir / "expression_bridge_followup_scorecard.csv"
                ),
                "expression_bridge_followup_comparison": str(
                    out_dir / "expression_bridge_followup_comparison.csv"
                ),
                "expression_bridge_followup_cost_sensitivity": str(
                    out_dir / "expression_bridge_followup_cost_sensitivity.csv"
                ),
            },
            "result_counts": _result_counts(results),
            "parent": _spec_record(parent),
            "child": _spec_record(child),
            "promising_bridge_variants": promising,
            "decision_contract": {
                "promotion_allowed_from_this_run": False,
                "full_validation_allowed_from_this_run": False,
                "final_test_used": False,
                "development_os_used_for_feedback": True,
                "review_rule": (
                    "A bridge follow-up pass is evidence to consider an explicit "
                    "bridge-aware strategy candidate, not a promotion."
                ),
            },
            "comparison_rows": comparison_rows,
            "results": results,
        }
        write_json(out_dir / "expression_bridge_followup_summary.json", summary)
        print(
            write_json(
                out_dir / "run_result.json",
                {
                    "status": "ok",
                    "run_id": run_id,
                    "out_dir": str(out_dir),
                    "result_count": len(results),
                    "comparison_count": len(comparison_rows),
                    "promising_bridge_variant_count": len(promising),
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
        write_json(out_dir / "expression_bridge_followup_summary.json", summary)
        print(str(exc), file=sys.stderr)
        return 1


def _evaluate_spec_under_bridges(
    spec: Any,
    *,
    record_type: str,
    parent_expression_id: str | None,
    eval_panel: Any,
    universe_panel: Any,
    splits: Any,
    analysis_end: Any,
    costs: list[float],
    args: argparse.Namespace,
    config: Any,
    bridge_variants: Any,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    from research.alphaevolve_lite.daily_stock_contract import CONTRACT
    from research.alphaevolve_lite.expression_bridge_variants import apply_bridge_variant
    from research.alphaevolve_lite.expression_eval_records import (
        expression_sample_hard_gates,
        status_from_metrics,
    )
    from research.alphaevolve_lite.expression_evolution import (
        construct_expression_portfolio,
        evaluate_expression_signal,
    )
    from research.alphaevolve_lite.sample_eval_metrics import (
        cost_sensitivity_rows,
        is_os_degradation_metrics,
        portfolio_day_coverage_diagnostics,
        portfolio_from_weights,
        split_metrics,
    )

    results: list[dict[str, Any]] = []
    cost_rows: list[dict[str, Any]] = []
    signal = evaluate_expression_signal(spec, eval_panel, config=config, contract=CONTRACT)
    target_weights = construct_expression_portfolio(signal, eval_panel, config=config, contract=CONTRACT)
    signal_non_null_ratio = float(signal.notna().mean())

    for variant in bridge_variants:
        result: dict[str, Any] = {
            "expression_id": spec.expression_id,
            "record_type": record_type,
            "root_expression_id": parent_expression_id or spec.expression_id,
            "parent_expression_id": parent_expression_id,
            "turn": None,
            "title": spec.title,
            "thesis": spec.thesis,
            "expression": spec.expression,
            "mechanism": spec.mechanism,
            "expected_effect": spec.expected_effect,
            "tags": list(spec.tags),
            "bridge_variant": variant.name,
            "status": "expression_error",
            "failure_reason": None,
            "metrics": {},
            "portfolio_coverage": {},
            "hard_gates": {},
            "signal_non_null_ratio": signal_non_null_ratio,
        }
        try:
            weights = apply_bridge_variant(
                target_weights,
                eval_panel,
                variant=variant,
                config=config,
                contract=CONTRACT,
            )
            full_portfolio, positions = portfolio_from_weights(
                eval_panel,
                weights,
                args.total_cost_bps,
                CONTRACT,
            )
            portfolio = full_portfolio.loc[full_portfolio["DlyCalDt"] <= analysis_end].copy()
            positions = positions.loc[positions[CONTRACT.date] <= analysis_end].copy()
            if portfolio.empty:
                raise RuntimeError("expression bridge produced no nonzero portfolio returns")
            coverage = portfolio_day_coverage_diagnostics(
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
                for split in splits
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
            result["portfolio_coverage"] = coverage
            result["position_rows"] = int(len(positions))
            result["status"] = status_from_metrics(
                metrics,
                coverage,
                max_weight=args.max_weight,
                max_abs_net_exposure=args.max_abs_net_exposure,
                max_missing_held_weight=args.max_missing_held_weight,
            )
            result["hard_gates"] = expression_sample_hard_gates(
                metrics,
                coverage,
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
                cost_rows.append(
                    {
                        "expression_id": spec.expression_id,
                        "record_type": record_type,
                        "parent_expression_id": parent_expression_id,
                        "bridge_variant": variant.name,
                        **row,
                    }
                )
        except Exception as exc:
            result["failure_reason"] = str(exc)
        results.append(result)
    return results, cost_rows


def _comparison_rows(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    parent_by_bridge = {
        str(result.get("bridge_variant")): result
        for result in results
        if result.get("record_type") == "parent_baseline"
    }
    child_results = [result for result in results if result.get("record_type") == "bridge_child"]
    rows: list[dict[str, Any]] = []
    for child in child_results:
        bridge = str(child.get("bridge_variant"))
        parent = parent_by_bridge.get(bridge, {})
        flags = child.get("success_flags") or {}
        row = {
            "bridge_variant": bridge,
            "parent_expression_id": parent.get("expression_id"),
            "child_expression_id": child.get("expression_id"),
            "parent_status": parent.get("status"),
            "child_status": child.get("status"),
            "child_expression": child.get("expression"),
            "bridge_contract_followup_pass": bool(flags.get("economically_interesting")),
        }
        for split in ("search_sample", "in_sample", "out_sample"):
            for metric in (
                "sharpe",
                "turnover",
                "turnover_aware_score",
                "max_missing_held_weight",
                "max_weight",
                "max_abs_net_exposure",
            ):
                parent_value = _metric(parent, split, metric)
                child_value = _metric(child, split, metric)
                row[f"parent_{split}_{metric}"] = parent_value
                row[f"child_{split}_{metric}"] = child_value
                row[f"child_minus_parent_{split}_{metric}"] = (
                    child_value - parent_value
                    if child_value is not None and parent_value is not None
                    else None
                )
        row.update({f"flag_{key}": value for key, value in flags.items()})
        rows.append(row)
    return rows


def _ranking_rows(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    from research.alphaevolve_lite.expression_eval_records import ranking_row

    rows: list[dict[str, Any]] = []
    for result in results:
        row = ranking_row(result)
        row["bridge_variant"] = result.get("bridge_variant")
        row["root_expression_id"] = result.get("root_expression_id")
        rows.append(row)
    return rows


def _scorecard_rows(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for result in results:
        for split_name, metrics in (result.get("metrics") or {}).items():
            if not isinstance(metrics, dict):
                continue
            for metric, value in metrics.items():
                rows.append(
                    {
                        "expression_id": result.get("expression_id"),
                        "record_type": result.get("record_type"),
                        "parent_expression_id": result.get("parent_expression_id"),
                        "bridge_variant": result.get("bridge_variant"),
                        "status": result.get("status"),
                        "split": split_name,
                        "metric": metric,
                        "value": value,
                    }
                )
    return rows


def _candidate_record(parent: Any, child: Any) -> dict[str, Any]:
    return {
        "schema_version": "expression_bridge_followup_candidate_v1",
        "parent": _spec_record(parent),
        "child": _spec_record(child),
        "interpretation": (
            "Evaluate child and parent under identical bridge contracts. "
            "Positive bridge evidence can justify a reviewed bridge-aware strategy "
            "conversion, but cannot promote the expression by itself."
        ),
    }


def _spec_record(spec: Any) -> dict[str, Any]:
    return {
        "expression_id": spec.expression_id,
        "title": spec.title,
        "thesis": spec.thesis,
        "expression": spec.expression,
        "mechanism": spec.mechanism,
        "expected_effect": spec.expected_effect,
        "tags": list(spec.tags),
    }


def _metric(result: dict[str, Any], split: str, metric: str) -> float | None:
    from research.alphaevolve_lite.expression_eval_records import finite_or_none

    return finite_or_none(((result.get("metrics") or {}).get(split) or {}).get(metric))


def _result_counts(results: list[dict[str, Any]]) -> dict[str, int]:
    statuses = [str(result.get("status")) for result in results]
    return {
        "result_count": len(results),
        "parent_baseline_count": sum(result.get("record_type") == "parent_baseline" for result in results),
        "bridge_child_count": sum(result.get("record_type") == "bridge_child" for result in results),
        "sample_pass": statuses.count("expression_sample_pass"),
        "sample_review": statuses.count("expression_sample_review"),
        "expression_error": statuses.count("expression_error"),
    }


def _parse_float_list(value: str, flag_name: str) -> list[float]:
    items = [item.strip() for item in value.split(",") if item.strip()]
    if not items:
        raise ValueError(f"{flag_name} must include at least one numeric value")
    return [float(item) for item in items]


def _validate_args(args: argparse.Namespace) -> None:
    if args.min_portfolio_days < 1:
        raise ValueError("--min-portfolio-days must be positive")
    if not 0.0 < args.min_portfolio_day_coverage <= 1.0:
        raise ValueError("--min-portfolio-day-coverage must be in (0, 1]")
    if not args.child_expression.strip():
        raise ValueError("--child-expression must be non-empty")
    if not args.child_expression_id.strip():
        raise ValueError("--child-expression-id must be non-empty")


if __name__ == "__main__":
    raise SystemExit(main())
