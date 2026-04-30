"""Run a compact remote sample evaluation for the Kalman reversal seed."""

from __future__ import annotations

import argparse
import json
import math
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
    parser = argparse.ArgumentParser(description="Remote sample-evaluate the Phase 4 Kalman seed.")
    parser.add_argument("--csv-path", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--db-path", default="")
    parser.add_argument("--start-date", default="2018-01-01")
    parser.add_argument("--end-date", default="2020-12-31")
    parser.add_argument("--chunksize", type=int, default=1_000_000)
    parser.add_argument("--max-input-rows", type=int)
    parser.add_argument("--top-n", type=int, default=500)
    parser.add_argument("--total-cost-bps", type=float, default=2.5)
    parser.add_argument("--cost-grid-bps", default="0,1,2.5,5")
    parser.add_argument("--program-id", default="PROG-20260430-000000")
    parser.add_argument("--run-id", default="")
    return parser.parse_args()


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def git_value(args: list[str]) -> str:
    try:
        out = subprocess.check_output(["git", *args], stderr=subprocess.DEVNULL)
        return out.decode("utf-8", errors="replace").strip()
    except Exception:
        return "unknown"


def clean_json(obj: Any) -> Any:
    try:
        import numpy as np
        import pandas as pd
    except Exception:  # pragma: no cover
        np = None
        pd = None

    if isinstance(obj, dict):
        return {str(k): clean_json(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [clean_json(v) for v in obj]
    if pd is not None and isinstance(obj, pd.Timestamp):
        return obj.isoformat()
    if np is not None and isinstance(obj, np.generic):
        return clean_json(obj.item())
    if isinstance(obj, float):
        return obj if math.isfinite(obj) else None
    return obj


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(clean_json(payload), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_lines(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def max_drawdown(returns):
    wealth = (1.0 + returns.fillna(0.0)).cumprod()
    peak = wealth.cummax()
    drawdown = wealth / peak - 1.0
    return float(drawdown.min()) if len(drawdown) else float("nan")


def beta_to_market(returns, market):
    import numpy as np
    import pandas as pd

    joined = pd.concat([returns, market], axis=1).dropna()
    if len(joined) < 2:
        return float("nan")
    y = joined.iloc[:, 0].to_numpy(dtype=float)
    x = joined.iloc[:, 1].to_numpy(dtype=float)
    var_x = np.var(x, ddof=1)
    if var_x <= 0 or not np.isfinite(var_x):
        return float("nan")
    return float(np.cov(x, y, ddof=1)[0, 1] / var_x)


def split_metrics(portfolio, split_name: str, start, end) -> dict[str, float]:
    import numpy as np

    if portfolio.empty:
        return {
            "annualized_return": float("nan"),
            "annualized_volatility": float("nan"),
            "sharpe": float("nan"),
            "gross_annualized_return": float("nan"),
            "gross_sharpe": float("nan"),
            "max_drawdown": float("nan"),
            "turnover": float("nan"),
            "hit_rate": float("nan"),
            "beta_to_vwretd": float("nan"),
            "mean_daily_n_names": float("nan"),
            "mean_missing_held_weight": float("nan"),
            "max_missing_held_weight": float("nan"),
            "max_weight": float("nan"),
        }
    part = portfolio.loc[portfolio["DlyCalDt"].between(start, end)].copy()
    if part.empty:
        return split_metrics(part, split_name, start, end)
    ann = 252.0
    rets = part.set_index("DlyCalDt")["net_return"]
    gross = part.set_index("DlyCalDt")["gross_return"]
    market = part.set_index("DlyCalDt")["vwretd"]
    vol = rets.std(ddof=1)
    gross_vol = gross.std(ddof=1)
    return {
        "annualized_return": float(rets.mean() * ann),
        "annualized_volatility": float(vol * math.sqrt(ann)) if np.isfinite(vol) else float("nan"),
        "sharpe": float(rets.mean() / vol * math.sqrt(ann)) if vol and vol > 0 else float("nan"),
        "gross_annualized_return": float(gross.mean() * ann),
        "gross_sharpe": float(gross.mean() / gross_vol * math.sqrt(ann)) if gross_vol and gross_vol > 0 else float("nan"),
        "max_drawdown": max_drawdown(rets),
        "turnover": float(part["turnover"].mean()),
        "hit_rate": float((rets > 0).mean()),
        "beta_to_vwretd": beta_to_market(rets, market),
        "mean_daily_n_names": float(part["n_names"].mean()),
        "mean_missing_held_weight": float(part["missing_held_weight"].mean()),
        "max_missing_held_weight": float(part["missing_held_weight"].max()),
        "max_weight": float(part["max_weight"].max()),
    }


def build_forward_returns(panel, contract):
    import pandas as pd

    data = panel.sort_values([contract.security_id, contract.date]).copy()
    trading_dates = pd.Index(data[contract.date].drop_duplicates().sort_values())
    next_date_map = pd.Series(trading_dates[1:].to_numpy(), index=trading_dates[:-1])
    data["next_market_date"] = data[contract.date].map(next_date_map)
    grouped = data.groupby(contract.security_id, sort=False)
    data["fwd_ret"] = grouped[contract.ex_dividend_return].shift(-1)
    data["fwd_date"] = grouped[contract.date].shift(-1)
    data["fwd_vwretd"] = grouped[contract.benchmark_return_primary].shift(-1)
    data["one_day_forward"] = data["fwd_date"].eq(data["next_market_date"])
    return data


def portfolio_from_weights(panel, weights, total_cost_bps: float, contract):
    import pandas as pd

    data = panel[
        [contract.date, contract.security_id, "fwd_ret", "fwd_date", "fwd_vwretd", "one_day_forward"]
    ].copy()
    data["weight"] = weights.reindex(data.index).fillna(0.0)
    data = data.loc[data["weight"].ne(0.0)].copy()
    if data.empty:
        return pd.DataFrame(
            columns=[
                "DlyCalDt",
                "signal_date",
                "gross_return",
                "net_return",
                "turnover",
                "n_names",
                "missing_held_weight",
                "max_weight",
                "vwretd",
            ]
        ), data

    cost_rate = total_cost_bps / 10000.0
    rows: list[dict[str, Any]] = []
    prev_weights = None
    for signal_date, group in data.groupby(contract.date, sort=True):
        w = group.set_index(contract.security_id)["weight"]
        if prev_weights is None:
            turnover = float(w.abs().sum())
        else:
            combined = w.index.union(prev_weights.index)
            turnover = float((w.reindex(combined, fill_value=0.0) - prev_weights.reindex(combined, fill_value=0.0)).abs().sum())
        prev_weights = w

        valid = group["one_day_forward"].fillna(False) & group["fwd_ret"].notna()
        missing_held_weight = float(group.loc[~valid, "weight"].abs().sum())
        available = group.loc[valid].copy()
        if available.empty:
            gross_return = float("nan")
            next_date = group["fwd_date"].dropna().min()
            market_return = float("nan")
        else:
            gross_return = float((available["weight"] * available["fwd_ret"]).sum())
            next_date = available["fwd_date"].iloc[0]
            market_return = float(available["fwd_vwretd"].iloc[0])
        rows.append(
            {
                "DlyCalDt": pd.Timestamp(next_date) if pd.notna(next_date) else pd.NaT,
                "signal_date": pd.Timestamp(signal_date),
                "gross_return": gross_return,
                "net_return": gross_return - turnover * cost_rate if math.isfinite(gross_return) else float("nan"),
                "turnover": turnover,
                "n_names": int(len(group)),
                "missing_held_weight": missing_held_weight,
                "max_weight": float(group["weight"].abs().max()),
                "vwretd": market_return,
            }
        )
    portfolio = pd.DataFrame(rows).dropna(subset=["DlyCalDt"]).sort_values("DlyCalDt")
    return portfolio, data


def scorecard_from_metrics(program_id: str, metrics: dict[str, dict[str, float]], splits) -> Any:
    import pandas as pd

    rows = []
    split_dates = {split.name: split for split in splits}
    for split_name, values in metrics.items():
        split = split_dates.get(split_name)
        for metric, value in values.items():
            rows.append(
                {
                    "program_id": program_id,
                    "split": split_name,
                    "start_date": split.start.date().isoformat() if split else "",
                    "end_date": split.end.date().isoformat() if split else "",
                    "metric": metric,
                    "value": value,
                }
            )
    return pd.DataFrame(rows)


def main() -> int:
    _ensure_repo_import()
    import pandas as pd

    from research.alphaevolve_lite.daily_stock_contract import CONTRACT, eligibility_query_description
    from research.alphaevolve_lite.daily_stock_loader import (
        apply_duplicate_policy,
        apply_static_eligibility,
        load_daily_stock_window,
    )
    from research.alphaevolve_lite.program_database import init_db, insert_program_record
    from research.alphaevolve_lite.seeds import kalman_reversal_seed
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

    diagnostics: list[dict[str, Any]] = []
    decision = "reject"
    failure_reason = None

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
        diagnostics.extend({"check": key, "status": "info", "value": value} for key, value in eligibility_diag.items())

        if eligible.empty:
            raise RuntimeError("no eligible rows after daily_stock_contract_v1 filters")

        splits = build_chronological_splits(eligible[CONTRACT.date])
        membership, universe_summary = build_monthly_rolling_universe(eligible, top_n=args.top_n)
        universe_panel = apply_monthly_universe(eligible, membership)
        if universe_panel.empty:
            raise RuntimeError("rolling universe produced no sample rows")

        eval_panel = build_forward_returns(universe_panel, CONTRACT)
        signal = kalman_reversal_seed.compute_signal(eval_panel, kalman_reversal_seed.DEFAULT_PARAMS)
        ranked = kalman_reversal_seed.rank_or_transform_signal(signal, eval_panel, kalman_reversal_seed.DEFAULT_PARAMS)
        raw_weights = kalman_reversal_seed.construct_portfolio(ranked, eval_panel, kalman_reversal_seed.DEFAULT_PARAMS)
        weights = kalman_reversal_seed.apply_risk_controls(raw_weights, eval_panel, kalman_reversal_seed.DEFAULT_PARAMS)
        full_portfolio, positions = portfolio_from_weights(eval_panel, weights, args.total_cost_bps, CONTRACT)
        validation_end = splits[1].end
        portfolio = full_portfolio.loc[full_portfolio["DlyCalDt"] <= validation_end].copy()
        positions = positions.loc[positions[CONTRACT.date] <= validation_end].copy()
        if portfolio.empty:
            raise RuntimeError("seed produced no nonzero portfolio returns")

        visible_splits = [split for split in splits if split.name in {"train", "validation"}]
        metrics = {
            split.name: split_metrics(portfolio, split.name, split.start, split.end)
            for split in visible_splits
        }
        metrics["search_sample"] = split_metrics(
            portfolio,
            "search_sample",
            portfolio["DlyCalDt"].min(),
            portfolio["DlyCalDt"].max(),
        )
        hard_gates = {
            "daily_stock_contract_v1_columns_present": True,
            "rolling_universe_nonempty": bool(len(membership)),
            "portfolio_nonempty": bool(len(portfolio)),
            "max_weight_reported": "max_weight" in metrics["search_sample"],
            "test_metrics_locked": True,
            "missing_held_weight_within_sample_tolerance": metrics["search_sample"]["max_missing_held_weight"] <= 0.05,
        }
        decision = "sample_pass" if all(hard_gates.values()) else "sample_review"

        scorecard = scorecard_from_metrics(args.program_id, metrics, visible_splits)
        cost_rows = []
        for cost in costs:
            cost_portfolio = portfolio.copy()
            cost_portfolio["net_return"] = cost_portfolio["gross_return"] - cost_portfolio["turnover"] * (cost / 10000.0)
            cost_metrics = split_metrics(cost_portfolio, "all", cost_portfolio["DlyCalDt"].min(), cost_portfolio["DlyCalDt"].max())
            cost_rows.append(
                {
                    "total_cost_bps": cost,
                    "annualized_return": cost_metrics["annualized_return"],
                    "sharpe": cost_metrics["sharpe"],
                    "turnover": cost_metrics["turnover"],
                }
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
            "csv_path": args.csv_path,
            "start_date": args.start_date,
            "end_date": args.end_date,
            "top_n": args.top_n,
            "total_cost_bps": args.total_cost_bps,
            "cost_grid_bps": costs,
            "daily_stock_contract": CONTRACT.contract_id,
            "universe_policy": UNIVERSE_POLICY_ID,
            "eligibility_filters": eligibility_query_description(),
            "git_commit": git_value(["rev-parse", "HEAD"]),
            "git_dirty": bool(git_value(["status", "--porcelain"])),
            "python": sys.version,
            "platform": platform.platform(),
            "created_at": utc_now_iso(),
        }
        write_json(out_dir / "metrics.json", {"program_id": args.program_id, "metrics": metrics})
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
                "descriptors": {
                    "daily_stock_contract": CONTRACT.contract_id,
                    "strategy_family": "kalman_innovation_reversal",
                    "universe_policy": UNIVERSE_POLICY_ID,
                    "data_scope": "daily_stock_only",
                },
                "next_prompt_hint": "If sample_pass, register the seed and proceed to controller_static child-generation dry run. Do not use test metrics for prompt sampling.",
                "artifact_paths": {
                    "scorecard": "scorecard.csv",
                    "diagnostics": "diagnostics.csv",
                    "cost_sensitivity": "cost_sensitivity.csv",
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
                f"- max_weight: `{metrics['search_sample']['max_weight']}`",
                f"- max_missing_held_weight: `{metrics['search_sample']['max_missing_held_weight']}`",
            ],
        )

        if args.db_path:
            init_db(args.db_path)
            insert_program_record(
                args.db_path,
                {
                    "program_id": args.program_id,
                    "parent_id": None,
                    "root_id": "CAND-20260423-001",
                    "branch_id": "BRANCH-CAND-20260423-001-001",
                    "generation": 0,
                    "island": "daily_stock_signal",
                    "mutation_surface": "seed",
                    "data_scope": "daily_stock_only",
                    "status": "seed_sample_evaluated",
                    "program_path": "research/alphaevolve_lite/seeds/kalman_reversal_seed.py",
                    "evaluator_summary_path": str(out_dir / "evaluator_summary.json"),
                    "metrics": metrics,
                    "descriptors": {"daily_stock_contract": CONTRACT.contract_id},
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
