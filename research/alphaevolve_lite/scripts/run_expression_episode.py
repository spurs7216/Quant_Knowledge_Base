"""Run a remote Qwen daily-stock expression-evolution episode."""

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
        "--parent-seed-id",
        action="append",
        default=[],
        help="Expression seed id to use as an episode parent. May be repeated.",
    )
    parser.add_argument("--turns", type=int, default=3)
    parser.add_argument("--offspring-per-turn", type=int, default=3)
    parser.add_argument("--model-role", default="fast_generator")
    parser.add_argument("--temperature-grid", default="0.2,0.4,0.6")
    parser.add_argument("--max-tokens", type=int, default=8192)
    parser.add_argument("--verify-each-call", action="store_true")
    parser.add_argument("--near-duplicate-threshold", type=float, default=0.98)
    parser.add_argument("--pass-margin", type=float, default=0.0)
    parser.add_argument(
        "--parent-sampling-mode",
        choices=["fixed_seed", "population_best", "population_mixed"],
        default="population_mixed",
        help="How later turns choose expression parents within each root branch.",
    )
    parser.add_argument("--branch-stop-loss-min-children", type=int, default=4)
    parser.add_argument("--branch-stop-loss-margin", type=float, default=0.0)
    parser.add_argument(
        "--mock-response-json",
        default="",
        help="Local-test only: use this JSON response for every model call instead of Qwen.",
    )
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
    from research.alphaevolve_lite.expression_episode import (
        DEFAULT_EPISODE_PARENT_IDS,
        attempt_record_from_result,
        build_expression_episode_prompt,
        expression_novelty_diagnostics,
        parse_expression_proposals,
    )
    from research.alphaevolve_lite.expression_eval_records import (
        finite_or_none,
        ranking_row,
        scorecard_rows,
    )
    from research.alphaevolve_lite.expression_evolution import (
        DEFAULT_EXPRESSION_SEEDS,
        ExpressionEvaluationConfig,
        expression_interface_markdown,
        expression_seed_library_rows,
        score_expression_trajectory,
    )
    from research.alphaevolve_lite.expression_population import (
        branch_stop_loss_diagnostics,
        build_population_record,
        select_expression_parent,
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
    run_id = args.run_id or f"expression_episode-{utc_now_iso().replace(':', '').replace('-', '')}-{uuid.uuid4().hex[:8]}"
    costs = _parse_float_list(args.cost_grid_bps, "--cost-grid-bps")
    temperatures = _parse_float_list(args.temperature_grid, "--temperature-grid")
    _validate_args(args)

    seed_by_id = {seed.expression_id: seed for seed in DEFAULT_EXPRESSION_SEEDS}
    parent_ids = args.parent_seed_id or list(DEFAULT_EPISODE_PARENT_IDS)
    missing = sorted(set(parent_ids) - set(seed_by_id))
    if missing:
        print(f"unknown parent seed ids: {missing}", file=sys.stderr)
        return 2
    parents = [seed_by_id[parent_id] for parent_id in parent_ids]
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
    interface_markdown = expression_interface_markdown()
    (out_dir / "expression_interface.md").write_text(interface_markdown, encoding="utf-8")
    write_json(out_dir / "expression_seed_library.json", expression_seed_library_rows(DEFAULT_EXPRESSION_SEEDS))

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
        visible_splits = [split for split in splits if split.name in {"in_sample", "out_sample"}]

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

        parent_results: dict[str, dict[str, Any]] = {}
        result_by_id: dict[str, dict[str, Any]] = {}
        specs_by_id = dict(seed_by_id)
        root_scores: dict[str, float | None] = {}
        all_results: list[dict[str, Any]] = []
        child_results: list[dict[str, Any]] = []
        population_records: list[dict[str, Any]] = []
        parent_selection_records: list[dict[str, Any]] = []
        branch_child_counts = {parent.expression_id: 0 for parent in parents}
        cost_rows: list[dict[str, Any]] = []
        model_call_records: list[dict[str, Any]] = []

        for parent in parents:
            parent_result, parent_cost_rows = _evaluate_expression_spec(
                parent,
                eval_panel=eval_panel,
                universe_panel=universe_panel,
                splits=visible_splits,
                analysis_end=analysis_end,
                costs=costs,
                args=args,
                config=config,
                record_type="parent_baseline",
                root_expression_id=parent.expression_id,
            )
            parent_results[parent.expression_id] = parent_result
            result_by_id[parent.expression_id] = parent_result
            root_score = finite_or_none(
                parent_result.get("metrics", {}).get("search_sample", {}).get("turnover_aware_score")
            )
            root_scores[parent.expression_id] = root_score
            population_records.append(
                build_population_record(
                    parent_result,
                    root_expression_id=parent.expression_id,
                    generation=0,
                    split_id=IS_OS_SPLIT_ID,
                    root_score=root_score,
                    branch_child_index=0,
                )
            )
            all_results.append(parent_result)
            cost_rows.extend(parent_cost_rows)

        mock_content = (
            Path(args.mock_response_json).read_text(encoding="utf-8")
            if args.mock_response_json
            else None
        )

        for parent_index, root_parent in enumerate(parents):
            prior_expressions: list[str] = []
            feedback_rows: list[dict[str, Any]] = []
            for turn in range(1, args.turns + 1):
                parent_choice = select_expression_parent(
                    root=root_parent,
                    turn=turn,
                    specs_by_id=specs_by_id,
                    population_records=population_records,
                    parent_sampling_mode=args.parent_sampling_mode,
                )
                parent_selection_records.append(parent_choice.to_record())
                parent = specs_by_id[parent_choice.selected_expression_id]
                parent_result = result_by_id.get(parent.expression_id, parent_results[root_parent.expression_id])
                parent_ranking = ranking_row(parent_result)
                population_context = _population_context_for_root(
                    root_expression_id=root_parent.expression_id,
                    parent_choice=parent_choice.to_record(),
                    population_records=population_records,
                )
                temperature = temperatures[(turn + parent_index - 1) % len(temperatures)]
                system_prompt, user_prompt = build_expression_episode_prompt(
                    parent=parent,
                    root_parent=root_parent,
                    parent_ranking=parent_ranking,
                    population_context=population_context,
                    prior_feedback=feedback_rows,
                    turn=turn,
                    offspring_per_turn=args.offspring_per_turn,
                    interface_markdown=interface_markdown,
                )
                call_dir = out_dir / "model_calls" / (
                    f"{root_parent.expression_id}_turn_{turn:02d}_parent_{parent.expression_id}"
                )
                call_dir.mkdir(parents=True, exist_ok=True)
                (call_dir / "system_prompt.txt").write_text(system_prompt, encoding="utf-8")
                (call_dir / "user_prompt.md").write_text(user_prompt, encoding="utf-8")

                model_record: dict[str, Any] = {
                    "root_expression_id": root_parent.expression_id,
                    "parent_expression_id": parent.expression_id,
                    "turn": turn,
                    "parent_selection": parent_choice.to_record(),
                    "temperature": temperature,
                    "model_role": args.model_role,
                    "max_tokens": args.max_tokens,
                    "mock_response": bool(mock_content is not None),
                    "status": "ok",
                }
                try:
                    if mock_content is None:
                        from research.alphaevolve_lite.model_router import chat_completion

                        response = chat_completion(
                            role=args.model_role,
                            system_prompt=system_prompt,
                            user_prompt=user_prompt,
                            temperature=temperature,
                            max_tokens=args.max_tokens,
                            verify=args.verify_each_call or not model_call_records,
                        )
                        write_json(call_dir / "model_response.json", response)
                        response_content = str(response.get("content") or "")
                        model_record.update(
                            {
                                "content_was_null": bool(response.get("content_was_null")),
                                "reasoning_length": response.get("reasoning_length"),
                                "served_model_name": response.get("served_model_name"),
                            }
                        )
                    else:
                        response_content = mock_content
                        (call_dir / "model_response.json").write_text(response_content, encoding="utf-8")
                    proposals = parse_expression_proposals(response_content)[: args.offspring_per_turn]
                    if not proposals:
                        raise ValueError("model returned zero child proposals")
                except Exception as exc:
                    model_record["status"] = "model_parse_error"
                    model_record["failure_reason"] = str(exc)
                    rejected = _rejected_child_result(
                        expression_id=f"{root_parent.expression_id}_t{turn:02d}_parse_error",
                        parent=parent,
                        root_expression_id=root_parent.expression_id,
                        turn=turn,
                        status="model_parse_error",
                        failure_reason=str(exc),
                    )
                    child_results.append(rejected)
                    all_results.append(rejected)
                    branch_child_counts[root_parent.expression_id] += 1
                    population_records.append(
                        build_population_record(
                            rejected,
                            root_expression_id=root_parent.expression_id,
                            generation=turn,
                            split_id=IS_OS_SPLIT_ID,
                            root_score=root_scores[root_parent.expression_id],
                            branch_child_index=branch_child_counts[root_parent.expression_id],
                        )
                    )
                    feedback_rows.append(_feedback_row(rejected))
                    model_call_records.append(model_record)
                    continue

                model_record["proposal_count"] = len(proposals)
                model_call_records.append(model_record)
                for child_index, proposal in enumerate(proposals):
                    child_id = f"{root_parent.expression_id}_ep_t{turn:02d}_c{child_index:02d}"
                    novelty = expression_novelty_diagnostics(
                        expression=proposal.expression,
                        parent_expression=parent.expression,
                        prior_expressions=prior_expressions,
                        near_duplicate_threshold=args.near_duplicate_threshold,
                    )
                    if novelty["exact_duplicate"]:
                        result = _rejected_child_result(
                            expression_id=child_id,
                            parent=parent,
                            root_expression_id=root_parent.expression_id,
                            turn=turn,
                            status="expression_duplicate",
                            failure_reason="exact duplicate of parent or prior child expression",
                            proposal=proposal.as_record(),
                            novelty=novelty,
                        )
                    else:
                        spec = proposal.to_spec(child_id, parent, turn)
                        specs_by_id[child_id] = spec
                        result, result_cost_rows = _evaluate_expression_spec(
                            spec,
                            eval_panel=eval_panel,
                            universe_panel=universe_panel,
                            splits=visible_splits,
                            analysis_end=analysis_end,
                            costs=costs,
                            args=args,
                            config=config,
                            record_type="child",
                            root_expression_id=root_parent.expression_id,
                            parent_expression_id=parent.expression_id,
                            turn=turn,
                            proposal=proposal.as_record(),
                            novelty=novelty,
                        )
                        cost_rows.extend(result_cost_rows)
                    result_by_id[child_id] = result
                    child_results.append(result)
                    all_results.append(result)
                    branch_child_counts[root_parent.expression_id] += 1
                    population_records.append(
                        build_population_record(
                            result,
                            root_expression_id=root_parent.expression_id,
                            generation=turn,
                            split_id=IS_OS_SPLIT_ID,
                            root_score=root_scores[root_parent.expression_id],
                            branch_child_index=branch_child_counts[root_parent.expression_id],
                        )
                    )
                    feedback_rows.append(_feedback_row(result))
                    prior_expressions.append(proposal.expression)

        trajectory_summaries: dict[str, dict[str, Any]] = {}
        for parent in parents:
            parent_score = finite_or_none(
                parent_results[parent.expression_id]
                .get("metrics", {})
                .get("search_sample", {})
                .get("turnover_aware_score")
            )
            parent_child_results = [
                result for result in child_results if result.get("root_expression_id") == parent.expression_id
            ]
            trajectory_summaries[parent.expression_id] = score_expression_trajectory(
                [attempt_record_from_result(result) for result in parent_child_results],
                seed_expression=parent.expression,
                parent_score=parent_score or 0.0,
                pass_margin=args.pass_margin,
            )

        branch_diagnostics = {
            parent.expression_id: branch_stop_loss_diagnostics(
                root_expression_id=parent.expression_id,
                root_score=root_scores[parent.expression_id],
                population_records=population_records,
                min_child_count=args.branch_stop_loss_min_children,
                improvement_margin=args.branch_stop_loss_margin,
            )
            for parent in parents
        }

        rankings = [ranking_row(result) for result in all_results]
        rankings_df = pd.DataFrame(rankings)
        if not rankings_df.empty and "search_turnover_aware_score" in rankings_df:
            rankings_df["_status_rank"] = rankings_df["status"].map(
                {
                    "expression_sample_pass": 0,
                    "expression_sample_review": 1,
                    "expression_duplicate": 2,
                    "expression_error": 3,
                    "model_parse_error": 4,
                }
            ).fillna(5)
            rankings_df = rankings_df.sort_values(
                ["_status_rank", "record_type", "search_turnover_aware_score", "out_sample_sharpe"],
                ascending=[True, True, False, False],
                na_position="last",
            ).drop(columns=["_status_rank"])
        rankings_df.to_csv(out_dir / "expression_episode_rankings.csv", index=False)
        pd.DataFrame(scorecard_rows(all_results)).to_csv(out_dir / "expression_episode_scorecard.csv", index=False)
        pd.DataFrame(cost_rows).to_csv(out_dir / "expression_episode_cost_sensitivity.csv", index=False)
        _write_jsonl(out_dir / "expression_episode_candidates.jsonl", child_results)
        _write_jsonl(out_dir / "expression_population_ledger.jsonl", population_records)
        _write_jsonl(out_dir / "expression_parent_selection.jsonl", parent_selection_records)
        pd.json_normalize(population_records, sep=".").to_csv(
            out_dir / "expression_population_ledger.csv",
            index=False,
        )
        write_json(out_dir / "expression_episode_model_calls.json", model_call_records)
        write_json(out_dir / "expression_population_summary.json", {
            "schema_version": "expression_population_v1",
            "parent_sampling_mode": args.parent_sampling_mode,
            "population_record_count": len(population_records),
            "parent_selection_count": len(parent_selection_records),
            "parent_sampling_eligible_count": sum(
                bool(record.get("parent_sampling_eligible")) for record in population_records
            ),
            "branch_diagnostics": branch_diagnostics,
        })

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
                "expression_episode_rankings": str(out_dir / "expression_episode_rankings.csv"),
                "expression_episode_scorecard": str(out_dir / "expression_episode_scorecard.csv"),
                "expression_episode_cost_sensitivity": str(out_dir / "expression_episode_cost_sensitivity.csv"),
                "expression_episode_candidates": str(out_dir / "expression_episode_candidates.jsonl"),
                "expression_population_ledger_jsonl": str(out_dir / "expression_population_ledger.jsonl"),
                "expression_population_ledger_csv": str(out_dir / "expression_population_ledger.csv"),
                "expression_parent_selection": str(out_dir / "expression_parent_selection.jsonl"),
                "expression_population_summary": str(out_dir / "expression_population_summary.json"),
                "expression_episode_model_calls": str(out_dir / "expression_episode_model_calls.json"),
                "expression_episode_summary": str(out_dir / "expression_episode_summary.json"),
            },
            "result_counts": _result_counts(child_results),
            "parent_results": parent_results,
            "trajectory_summaries": trajectory_summaries,
            "branch_diagnostics": branch_diagnostics,
            "parent_selection_records": parent_selection_records,
            "population_records": population_records,
            "children": child_results,
        }
        write_json(out_dir / "expression_episode_summary.json", summary)
        print(
            write_json(
                out_dir / "run_result.json",
                {
                    "status": "ok",
                    "run_id": run_id,
                    "out_dir": str(out_dir),
                    **summary["result_counts"],
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
        write_json(out_dir / "expression_episode_summary.json", summary)
        print(str(exc), file=sys.stderr)
        return 1


def _parse_float_list(value: str, flag_name: str) -> list[float]:
    items = [item.strip() for item in value.split(",") if item.strip()]
    if not items:
        raise ValueError(f"{flag_name} must include at least one numeric value")
    return [float(item) for item in items]


def _validate_args(args: argparse.Namespace) -> None:
    if args.turns < 1:
        raise ValueError("--turns must be positive")
    if args.offspring_per_turn < 1:
        raise ValueError("--offspring-per-turn must be positive")
    if args.min_portfolio_days < 1:
        raise ValueError("--min-portfolio-days must be positive")
    if not 0.0 < args.min_portfolio_day_coverage <= 1.0:
        raise ValueError("--min-portfolio-day-coverage must be in (0, 1]")
    if not 0.0 <= args.near_duplicate_threshold <= 1.0:
        raise ValueError("--near-duplicate-threshold must be in [0, 1]")
    if args.branch_stop_loss_min_children < 1:
        raise ValueError("--branch-stop-loss-min-children must be positive")


def _evaluate_expression_spec(
    spec: Any,
    *,
    eval_panel: Any,
    universe_panel: Any,
    splits: Any,
    analysis_end: Any,
    costs: list[float],
    args: argparse.Namespace,
    config: Any,
    record_type: str,
    root_expression_id: str | None = None,
    parent_expression_id: str | None = None,
    turn: int | None = None,
    proposal: dict[str, Any] | None = None,
    novelty: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    from research.alphaevolve_lite.daily_stock_contract import CONTRACT
    from research.alphaevolve_lite.expression_evolution import (
        construct_expression_portfolio,
        evaluate_expression_signal,
    )
    from research.alphaevolve_lite.expression_eval_records import (
        expression_sample_hard_gates,
        status_from_metrics,
    )
    from research.alphaevolve_lite.sample_eval_metrics import (
        cost_sensitivity_rows,
        is_os_degradation_metrics,
        portfolio_day_coverage_diagnostics,
        portfolio_from_weights,
        split_metrics,
    )

    result: dict[str, Any] = {
        "expression_id": spec.expression_id,
        "record_type": record_type,
        "root_expression_id": root_expression_id,
        "parent_expression_id": parent_expression_id,
        "turn": turn,
        "title": spec.title,
        "thesis": spec.thesis,
        "expression": spec.expression,
        "mechanism": spec.mechanism,
        "expected_effect": spec.expected_effect,
        "tags": list(spec.tags),
        "status": "expression_error",
        "failure_reason": None,
        "metrics": {},
        "portfolio_coverage": {},
        "hard_gates": {},
        "proposal": proposal or {},
    }
    if novelty:
        result.update(novelty)
    child_cost_rows: list[dict[str, Any]] = []
    try:
        signal = evaluate_expression_signal(spec, eval_panel, config=config, contract=CONTRACT)
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
        result["portfolio_coverage"] = portfolio_coverage
        result["position_rows"] = int(len(positions))
        result["signal_non_null_ratio"] = float(signal.notna().mean())
        result["status"] = status_from_metrics(
            metrics,
            portfolio_coverage,
            max_weight=args.max_weight,
            max_abs_net_exposure=args.max_abs_net_exposure,
            max_missing_held_weight=args.max_missing_held_weight,
        )
        result["hard_gates"] = expression_sample_hard_gates(
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
            child_cost_rows.append(
                {
                    "expression_id": spec.expression_id,
                    "record_type": record_type,
                    "parent_expression_id": parent_expression_id,
                    "turn": turn,
                    **row,
                }
            )
    except Exception as exc:
        result["failure_reason"] = str(exc)
    return result, child_cost_rows


def _rejected_child_result(
    *,
    expression_id: str,
    parent: Any,
    root_expression_id: str,
    turn: int,
    status: str,
    failure_reason: str,
    proposal: dict[str, Any] | None = None,
    novelty: dict[str, Any] | None = None,
) -> dict[str, Any]:
    result = {
        "expression_id": expression_id,
        "record_type": "child",
        "root_expression_id": root_expression_id,
        "parent_expression_id": parent.expression_id,
        "turn": turn,
        "title": f"{parent.title} episode turn {turn}",
        "thesis": "",
        "expression": "" if not proposal else proposal.get("expression", ""),
        "mechanism": "",
        "expected_effect": "",
        "tags": list(parent.tags) + ["episode_child"],
        "status": status,
        "failure_reason": failure_reason,
        "metrics": {},
        "portfolio_coverage": {},
        "hard_gates": {},
        "proposal": proposal or {},
    }
    if novelty:
        result.update(novelty)
    return result


def _feedback_row(result: dict[str, Any]) -> dict[str, Any]:
    metrics = result.get("metrics", {}).get("search_sample", {})
    return {
        "expression_id": result.get("expression_id"),
        "status": result.get("status"),
        "failure_reason": result.get("failure_reason"),
        "expression": result.get("expression"),
        "search_sharpe": metrics.get("sharpe"),
        "search_turnover": metrics.get("turnover"),
        "search_turnover_aware_score": metrics.get("turnover_aware_score"),
        "out_sample_sharpe": result.get("metrics", {}).get("out_sample", {}).get("sharpe"),
        "portfolio_day_coverage": result.get("portfolio_coverage", {}).get("portfolio_day_coverage"),
        "near_duplicate": result.get("near_duplicate"),
        "similarity_to_parent": result.get("similarity_to_parent"),
    }


def _population_context_for_root(
    *,
    root_expression_id: str,
    parent_choice: dict[str, Any],
    population_records: list[dict[str, Any]],
) -> dict[str, Any]:
    root_records = [
        record for record in population_records if record.get("root_expression_id") == root_expression_id
    ]
    eligible = [
        record for record in root_records if record.get("parent_sampling_eligible") is True
    ]
    top_records = sorted(
        eligible,
        key=lambda item: _safe_sort_score(item.get("selection_score")),
        reverse=True,
    )[:5]
    map_cells = sorted({str(record.get("map_cell_key")) for record in root_records if record.get("map_cell_key")})
    return {
        "schema_version": "expression_population_prompt_context_v1",
        "root_expression_id": root_expression_id,
        "parent_choice": parent_choice,
        "population_record_count": len(root_records),
        "eligible_parent_count": len(eligible),
        "occupied_map_cell_count": len(map_cells),
        "occupied_map_cells": map_cells[:12],
        "top_eligible_records": [
            {
                "expression_id": record.get("expression_id"),
                "selection_score": record.get("selection_score"),
                "map_cell_key": record.get("map_cell_key"),
                "status": record.get("status"),
                "root_turnover_aware_delta": record.get("root_turnover_aware_delta"),
            }
            for record in top_records
        ],
        "policy_instruction": (
            "This is population search. Later turns should improve or diversify from eligible "
            "child survivors, not repeatedly rewrite only the original seed."
        ),
    }


def _safe_sort_score(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return float("-inf")
    return number if number == number and abs(number) != float("inf") else float("-inf")


def _result_counts(results: list[dict[str, Any]]) -> dict[str, int]:
    statuses = [str(result.get("status")) for result in results]
    return {
        "child_count": len(results),
        "sample_pass": statuses.count("expression_sample_pass"),
        "sample_review": statuses.count("expression_sample_review"),
        "expression_error": statuses.count("expression_error"),
        "expression_duplicate": statuses.count("expression_duplicate"),
        "model_parse_error": statuses.count("model_parse_error"),
        "near_duplicate": sum(bool(result.get("near_duplicate")) for result in results),
    }


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> Path:
    import json

    from research.alphaevolve_lite.artifact_io import clean_json

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(clean_json(row), sort_keys=True) + "\n")
    return path


if __name__ == "__main__":
    raise SystemExit(main())
