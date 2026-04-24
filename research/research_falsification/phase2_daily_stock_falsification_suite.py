"""
Phase 2 daily-stock falsification suite.

Run on the remote Ubuntu machine with the full WRDS mirror.

Example:
    python research/research_falsification/phase2_daily_stock_falsification_suite.py \
        --data-root /home/b08303004/Desktop/WRDS/data \
        --output-dir artifacts/remote_runs/20260423_phase2_daily_stock_falsification_suite

The script writes compact evidence only. It does not copy raw data.
"""

from __future__ import annotations

import argparse
import json
import math
import platform
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


JOB_ID = "20260423_phase2_daily_stock_falsification_suite"
TASK_BANK_VERSION = "phase2_falsification_v0"
REQUIRED_COLUMNS = [
    "PERMNO",
    "Ticker",
    "DlyCalDt",
    "DlyRet",
    "DlyRetx",
    "DlyPrc",
    "DlyVol",
    "SecurityEndDt",
    "SecurityActiveFlg",
    "PrimaryExch",
    "SecurityType",
    "ShareType",
    "TradingStatusFlg",
    "vwretd",
    "sprtrn",
]


@dataclass(frozen=True)
class Split:
    name: str
    start: str
    end: str


SPLITS = [
    Split("train", "2000-01-03", "2012-12-31"),
    Split("validation", "2013-01-01", "2018-12-31"),
    Split("test", "2019-01-01", "2025-11-28"),
]


def run_git(args: list[str]) -> str:
    try:
        out = subprocess.check_output(["git", *args], stderr=subprocess.DEVNULL)
        return out.decode("utf-8", errors="replace").strip()
    except Exception:
        return "unknown"


def git_snapshot() -> dict[str, Any]:
    status = run_git(["status", "--porcelain"])
    return {
        "repo": run_git(["config", "--get", "remote.origin.url"]),
        "branch": run_git(["rev-parse", "--abbrev-ref", "HEAD"]),
        "commit": run_git(["rev-parse", "HEAD"]),
        "dirty": bool(status),
    }


def finite_float(value: Any) -> float | None:
    try:
        x = float(value)
    except Exception:
        return None
    if math.isfinite(x):
        return x
    return None


def clean_json(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {str(k): clean_json(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [clean_json(v) for v in obj]
    if isinstance(obj, tuple):
        return [clean_json(v) for v in obj]
    if isinstance(obj, (pd.Timestamp, datetime)):
        return obj.isoformat()
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return finite_float(obj)
    if isinstance(obj, float):
        return obj if math.isfinite(obj) else None
    return obj


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(clean_json(data), indent=2, allow_nan=False), encoding="utf-8")


def max_drawdown(returns: pd.Series) -> float:
    returns = returns.fillna(0.0)
    wealth = (1.0 + returns).cumprod()
    peak = wealth.cummax()
    dd = wealth / peak - 1.0
    return float(dd.min()) if len(dd) else float("nan")


def beta_to_market(returns: pd.Series, market: pd.Series) -> float:
    joined = pd.concat([returns, market], axis=1).dropna()
    if len(joined) < 2:
        return float("nan")
    y = joined.iloc[:, 0].to_numpy()
    x = joined.iloc[:, 1].to_numpy()
    var_x = np.var(x, ddof=1)
    if var_x <= 0 or not np.isfinite(var_x):
        return float("nan")
    return float(np.cov(x, y, ddof=1)[0, 1] / var_x)


def split_metrics(portfolio: pd.DataFrame, split: Split) -> dict[str, float]:
    if portfolio.empty:
        return {
            "annualized_return": float("nan"),
            "annualized_volatility": float("nan"),
            "sharpe": float("nan"),
            "max_drawdown": float("nan"),
            "turnover": float("nan"),
            "hit_rate": float("nan"),
            "beta_to_vwretd": float("nan"),
            "mean_daily_n_long": float("nan"),
            "mean_daily_n_short": float("nan"),
            "portfolio_days": 0,
        }
    mask = (portfolio["DlyCalDt"] >= split.start) & (portfolio["DlyCalDt"] <= split.end)
    part = portfolio.loc[mask].copy()
    if part.empty:
        return split_metrics(pd.DataFrame(), split)
    rets = part.set_index("DlyCalDt")["net_return"]
    mkt = part.set_index("DlyCalDt")["vwretd"]
    ann = 252.0
    mean = rets.mean()
    vol = rets.std(ddof=1)
    return {
        "annualized_return": float(mean * ann) if pd.notna(mean) else float("nan"),
        "annualized_volatility": float(vol * math.sqrt(ann)) if pd.notna(vol) else float("nan"),
        "sharpe": float(mean / vol * math.sqrt(ann)) if vol and vol > 0 else float("nan"),
        "max_drawdown": max_drawdown(rets),
        "turnover": float(part["turnover"].mean()) if len(part) else float("nan"),
        "hit_rate": float((rets > 0).mean()) if len(rets) else float("nan"),
        "beta_to_vwretd": beta_to_market(rets, mkt),
        "mean_daily_n_long": float(part["n_long"].mean()) if len(part) else float("nan"),
        "mean_daily_n_short": float(part["n_short"].mean()) if len(part) else float("nan"),
        "portfolio_days": int(len(part)),
    }


def flatten_metrics(task_id: str, portfolio: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split in SPLITS:
        metrics = split_metrics(portfolio, split)
        for metric, value in metrics.items():
            rows.append(
                {
                    "job_id": JOB_ID,
                    "task_id": task_id,
                    "split": split.name,
                    "start_date": split.start,
                    "end_date": split.end,
                    "metric": metric,
                    "value": value,
                }
            )
    return rows


def load_daily_stock(path: Path) -> pd.DataFrame:
    dtype = {
        "PERMNO": "int32",
        "Ticker": "string",
        "PrimaryExch": "category",
        "SecurityType": "category",
        "ShareType": "category",
        "TradingStatusFlg": "category",
        "SecurityActiveFlg": "category",
    }
    df = pd.read_csv(
        path,
        usecols=REQUIRED_COLUMNS,
        dtype=dtype,
        parse_dates=["DlyCalDt", "SecurityEndDt"],
        low_memory=False,
    )
    for col in ["DlyRet", "DlyRetx", "DlyPrc", "DlyVol", "vwretd", "sprtrn"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def prepare_base_panel(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    diagnostics: list[dict[str, Any]] = []
    diagnostics.append({"check": "raw_rows", "status": "info", "value": len(df), "threshold": "", "notes": ""})
    diagnostics.append(
        {
            "check": "duplicate_permno_date_before_filters",
            "status": "warn" if df.duplicated(["PERMNO", "DlyCalDt"]).any() else "pass",
            "value": int(df.duplicated(["PERMNO", "DlyCalDt"]).sum()),
            "threshold": 0,
            "notes": "Duplicate rows are not repaired silently; first row is kept for this calibration run.",
        }
    )

    filtered = df.loc[
        (df["SecurityType"] == "EQTY")
        & (df["ShareType"] == "NS")
        & (df["TradingStatusFlg"] == "A")
        & df["DlyRetx"].notna()
        & df["vwretd"].notna()
    ].copy()
    filtered.sort_values(["PERMNO", "DlyCalDt"], inplace=True)

    duplicate_after = int(filtered.duplicated(["PERMNO", "DlyCalDt"]).sum())
    diagnostics.append(
        {
            "check": "duplicate_permno_date_after_base_filters",
            "status": "warn" if duplicate_after else "pass",
            "value": duplicate_after,
            "threshold": 0,
            "notes": "First row is kept so the suite can run; production policy remains a separate research issue.",
        }
    )
    if duplicate_after:
        filtered = filtered.drop_duplicates(["PERMNO", "DlyCalDt"], keep="first").copy()

    trading_dates = pd.Index(filtered["DlyCalDt"].drop_duplicates().sort_values())
    next_date_map = pd.Series(trading_dates[1:].to_numpy(), index=trading_dates[:-1])
    filtered["next_market_date"] = filtered["DlyCalDt"].map(next_date_map)
    grouped = filtered.groupby("PERMNO", sort=False)
    filtered["fwd_ret"] = grouped["DlyRetx"].shift(-1)
    filtered["fwd_date"] = grouped["DlyCalDt"].shift(-1)
    filtered["fwd_vwretd"] = grouped["vwretd"].shift(-1)
    filtered["fwd_sprtrn"] = grouped["sprtrn"].shift(-1)
    filtered["rx"] = filtered["DlyRetx"] - filtered["vwretd"]
    filtered["prior_obs"] = grouped.cumcount()
    filtered["dollar_volume"] = filtered["DlyPrc"].abs() * filtered["DlyVol"]

    one_day_forward = filtered["fwd_date"].eq(filtered["next_market_date"])
    panel = filtered.loc[
        (filtered["prior_obs"] >= 60)
        & filtered["fwd_ret"].notna()
        & one_day_forward
        & filtered["DlyPrc"].notna()
        & filtered["DlyVol"].notna()
    ].copy()
    diagnostics.append({"check": "base_panel_rows", "status": "info", "value": len(panel), "threshold": "", "notes": ""})
    diagnostics.append(
        {
            "check": "return_timing_one_trading_day",
            "status": "pass" if panel["fwd_date"].eq(panel["next_market_date"]).all() else "fail",
            "value": int((~panel["fwd_date"].eq(panel["next_market_date"])).sum()),
            "threshold": 0,
            "notes": "Valid non-leaky portfolio builders use next trading day returns only.",
        }
    )
    return panel, pd.DataFrame(diagnostics)


def build_next_day_decile_portfolio(
    panel: pd.DataFrame,
    signal_col: str,
    total_cost_bps: float,
    min_names: int = 20,
) -> pd.DataFrame:
    results: list[dict[str, Any]] = []
    prev_weights: pd.Series | None = None
    cost_rate = total_cost_bps / 10000.0

    for date, g in panel.groupby("DlyCalDt", sort=True):
        g = g.dropna(subset=[signal_col, "fwd_ret"])
        n = len(g)
        if n < min_names:
            continue
        q_long = g[signal_col].quantile(0.9)
        q_short = g[signal_col].quantile(0.1)
        longs = g.loc[g[signal_col] >= q_long, ["PERMNO", "fwd_ret"]]
        shorts = g.loc[g[signal_col] <= q_short, ["PERMNO", "fwd_ret"]]
        if longs.empty or shorts.empty:
            continue

        weights = pd.Series(0.0, index=pd.Index(pd.concat([longs["PERMNO"], shorts["PERMNO"]]).unique(), name="PERMNO"))
        weights.loc[longs["PERMNO"].to_numpy()] = 0.5 / len(longs)
        weights.loc[shorts["PERMNO"].to_numpy()] = -0.5 / len(shorts)
        if prev_weights is None:
            turnover = float(weights.abs().sum())
        else:
            combined = weights.index.union(prev_weights.index)
            turnover = float((weights.reindex(combined, fill_value=0.0) - prev_weights.reindex(combined, fill_value=0.0)).abs().sum())
        prev_weights = weights

        ret_map = pd.concat([longs, shorts]).drop_duplicates("PERMNO").set_index("PERMNO")["fwd_ret"]
        gross_return = float((weights * ret_map.reindex(weights.index)).sum())
        results.append(
            {
                "DlyCalDt": pd.Timestamp(g["fwd_date"].iloc[0]),
                "signal_date": pd.Timestamp(date),
                "gross_return": gross_return,
                "net_return": gross_return - turnover * cost_rate,
                "turnover": turnover,
                "n_long": int(len(longs)),
                "n_short": int(len(shorts)),
                "vwretd": float(g["fwd_vwretd"].iloc[0]),
                "sprtrn": float(g["fwd_sprtrn"].iloc[0]),
            }
        )
    return pd.DataFrame(results).sort_values("DlyCalDt") if results else pd.DataFrame()


def build_same_day_leak_portfolio(panel: pd.DataFrame, total_cost_bps: float) -> pd.DataFrame:
    results: list[dict[str, Any]] = []
    prev_weights: pd.Series | None = None
    cost_rate = total_cost_bps / 10000.0

    for date, g in panel.groupby("DlyCalDt", sort=True):
        g = g.dropna(subset=["DlyRetx"])
        if len(g) < 20:
            continue
        q_long = g["DlyRetx"].quantile(0.9)
        q_short = g["DlyRetx"].quantile(0.1)
        longs = g.loc[g["DlyRetx"] >= q_long, ["PERMNO", "DlyRetx"]]
        shorts = g.loc[g["DlyRetx"] <= q_short, ["PERMNO", "DlyRetx"]]
        if longs.empty or shorts.empty:
            continue
        weights = pd.Series(0.0, index=pd.Index(pd.concat([longs["PERMNO"], shorts["PERMNO"]]).unique(), name="PERMNO"))
        weights.loc[longs["PERMNO"].to_numpy()] = 0.5 / len(longs)
        weights.loc[shorts["PERMNO"].to_numpy()] = -0.5 / len(shorts)
        if prev_weights is None:
            turnover = float(weights.abs().sum())
        else:
            combined = weights.index.union(prev_weights.index)
            turnover = float((weights.reindex(combined, fill_value=0.0) - prev_weights.reindex(combined, fill_value=0.0)).abs().sum())
        prev_weights = weights
        ret_map = pd.concat([longs, shorts]).drop_duplicates("PERMNO").set_index("PERMNO")["DlyRetx"]
        gross_return = float((weights * ret_map.reindex(weights.index)).sum())
        results.append(
            {
                "DlyCalDt": pd.Timestamp(date),
                "signal_date": pd.Timestamp(date),
                "gross_return": gross_return,
                "net_return": gross_return - turnover * cost_rate,
                "turnover": turnover,
                "n_long": int(len(longs)),
                "n_short": int(len(shorts)),
                "vwretd": float(g["vwretd"].iloc[0]),
                "sprtrn": float(g["sprtrn"].iloc[0]),
            }
        )
    return pd.DataFrame(results).sort_values("DlyCalDt") if results else pd.DataFrame()


def random_rank_seed_metrics(panel: pd.DataFrame, total_cost_bps: float, random_seeds: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    summary_rows: list[dict[str, Any]] = []
    score_rows: list[dict[str, Any]] = []
    for seed in range(random_seeds):
        rng = np.random.default_rng(seed)
        panel["random_signal"] = rng.standard_normal(len(panel))
        portfolio = build_next_day_decile_portfolio(panel, "random_signal", total_cost_bps)
        for split in SPLITS:
            metrics = split_metrics(portfolio, split)
            summary_rows.append(
                {
                    "task_id": "FAL-001",
                    "seed": seed,
                    "split": split.name,
                    "annualized_return": metrics["annualized_return"],
                    "annualized_volatility": metrics["annualized_volatility"],
                    "sharpe": metrics["sharpe"],
                    "max_drawdown": metrics["max_drawdown"],
                    "turnover": metrics["turnover"],
                    "portfolio_days": metrics["portfolio_days"],
                }
            )
        score_rows.extend(flatten_metrics(f"FAL-001_seed_{seed}", portfolio))
    if "random_signal" in panel.columns:
        panel.drop(columns=["random_signal"], inplace=True)
    return pd.DataFrame(summary_rows), pd.DataFrame(score_rows)


def identifier_artifact_metrics(panel: pd.DataFrame, total_cost_bps: float) -> tuple[pd.DataFrame, pd.DataFrame]:
    panel["identifier_signal"] = (panel["PERMNO"].astype("int64") % 1000).astype(float)
    portfolio = build_next_day_decile_portfolio(panel, "identifier_signal", total_cost_bps)
    metrics_rows = flatten_metrics("FAL-004", portfolio)
    panel.drop(columns=["identifier_signal"], inplace=True)
    return pd.DataFrame(metrics_rows), portfolio


def implementation_feasibility(panel: pd.DataFrame) -> pd.DataFrame:
    low_price = panel["DlyPrc"].abs() < 5
    low_dollar_volume = panel["dollar_volume"] <= panel["dollar_volume"].quantile(0.1)
    microcap_like = low_price | low_dollar_volume
    rows = [
        {
            "task_id": "FAL-005",
            "check": "low_price_or_bottom_decile_dollar_volume_rate",
            "value": float(microcap_like.mean()),
            "status": "warn" if microcap_like.any() else "pass",
            "notes": "High concentration here signals borrow, capacity, and orderability concerns.",
        },
        {
            "task_id": "FAL-005",
            "check": "missing_borrow_data",
            "value": 1,
            "status": "fail",
            "notes": "daily_stock file does not provide borrow availability or borrow fees.",
        },
        {
            "task_id": "FAL-005",
            "check": "broker_contract_resolution_unspecified",
            "value": 1,
            "status": "fail",
            "notes": "No local IBKR contract-resolution request or order-intent artifact is supplied; broker-facing verification belongs to local Phase 2B.",
        },
    ]
    return pd.DataFrame(rows)


def task_scorecard() -> pd.DataFrame:
    rows = [
        {
            "task_id": "FAL-001",
            "task_name": "Random-rank daily-stock null",
            "task_bank_version": TASK_BANK_VERSION,
            "expected_decision": "reject",
            "automated_evaluator_decision": "reject",
            "statistical_gate": "fail",
            "leakage_gate": "pass",
            "implementation_gate": "not_primary",
            "primary_failure_reason": "Random ranks have no ex ante predictive content; any attractive split is noise evidence.",
            "false_accept_if_agent_decision": "proceed",
        },
        {
            "task_id": "FAL-002",
            "task_name": "Same-day return leakage trap",
            "task_bank_version": TASK_BANK_VERSION,
            "expected_decision": "reject",
            "automated_evaluator_decision": "reject",
            "statistical_gate": "not_needed",
            "leakage_gate": "fail",
            "implementation_gate": "fail",
            "primary_failure_reason": "Signal uses same-day return that is not known at decision time.",
            "false_accept_if_agent_decision": "proceed",
        },
        {
            "task_id": "FAL-003",
            "task_name": "Future survivorship universe trap",
            "task_bank_version": TASK_BANK_VERSION,
            "expected_decision": "reject",
            "automated_evaluator_decision": "reject",
            "statistical_gate": "not_needed",
            "leakage_gate": "fail",
            "implementation_gate": "not_primary",
            "primary_failure_reason": "Universe uses future security activity or end-date information.",
            "false_accept_if_agent_decision": "proceed",
        },
        {
            "task_id": "FAL-004",
            "task_name": "Static identifier artifact",
            "task_bank_version": TASK_BANK_VERSION,
            "expected_decision": "reject",
            "automated_evaluator_decision": "reject",
            "statistical_gate": "fail",
            "leakage_gate": "pass",
            "implementation_gate": "not_primary",
            "primary_failure_reason": "PERMNO hash has no standalone economic mechanism and is likely a composition artifact.",
            "false_accept_if_agent_decision": "proceed",
        },
        {
            "task_id": "FAL-005",
            "task_name": "Microcap shorting implementation trap",
            "task_bank_version": TASK_BANK_VERSION,
            "expected_decision": "reject_or_revise",
            "automated_evaluator_decision": "reject",
            "statistical_gate": "not_primary",
            "leakage_gate": "pass",
            "implementation_gate": "fail",
            "primary_failure_reason": "Shorting, borrow, capacity, and contract-resolution assumptions are missing.",
            "false_accept_if_agent_decision": "proceed",
        },
    ]
    return pd.DataFrame(rows)


def survivorship_diagnostics(panel: pd.DataFrame) -> pd.DataFrame:
    sample_end = pd.Timestamp("2025-11-28")
    active_flag_rate = float((panel["SecurityActiveFlg"] == "Y").mean()) if "SecurityActiveFlg" in panel else float("nan")
    known_future_survivor = panel["SecurityEndDt"].notna() & (panel["SecurityEndDt"] >= sample_end)
    return pd.DataFrame(
        [
            {
                "task_id": "FAL-003",
                "check": "security_active_flag_available",
                "status": "info",
                "value": active_flag_rate,
                "threshold": "",
                "notes": "Using full-sample activity as a historical universe filter is a lookahead trap.",
            },
            {
                "task_id": "FAL-003",
                "check": "future_survivor_flag_rate",
                "status": "info",
                "value": float(known_future_survivor.mean()),
                "threshold": "",
                "notes": "SecurityEndDt relative to the sample end is future information for earlier dates.",
            },
            {
                "task_id": "FAL-003",
                "check": "survivorship_filter_gate",
                "status": "fail",
                "value": "SecurityActiveFlg or SecurityEndDt full-sample filter",
                "threshold": "no future universe fields",
                "notes": "This is intentionally marked fail for the trap task.",
            },
        ]
    )


def write_manifest(path: Path, args: argparse.Namespace, raw_rows: int, panel_rows: int) -> None:
    snapshot = git_snapshot()
    manifest = {
        "schema_version": 0.1,
        "job_id": JOB_ID,
        "created": datetime.now().isoformat(timespec="seconds"),
        "environment": "research_falsification",
        "task_bank_version": TASK_BANK_VERSION,
        "sync": {"channel": "github", "remote_os": "ubuntu", "artifact_import_policy": "manual_review"},
        "vault_snapshot": snapshot,
        "research_code_snapshot": snapshot,
        "runtime": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "pandas": pd.__version__,
            "numpy": np.__version__,
        },
        "datasets": [
            {
                "logical_name": "daily_stock",
                "remote_path": str(args.data_path),
                "catalog_relative_path": "data/daily_stock/gago9dveytpx6922.csv",
                "row_count_observed": raw_rows,
                "panel_rows_observed": panel_rows,
                "required_columns": REQUIRED_COLUMNS,
            }
        ],
        "cost_model": {"total_cost_bps": args.total_cost_bps},
        "random_seeds": args.random_seeds,
        "expected_outputs": [
            "run_manifest.yaml",
            "metrics.json",
            "task_scorecard.csv",
            "diagnostics.csv",
            "failure_report.md",
            "review.md",
            "random_rank_seed_metrics.csv",
            "random_rank_detailed_metrics.csv",
            "identifier_artifact_metrics.csv",
            "leakage_trap_metrics.csv",
            "implementation_feasibility.csv",
        ],
    }
    path.write_text(json.dumps(clean_json(manifest), indent=2), encoding="utf-8")


def make_failure_report(path: Path, diagnostics: pd.DataFrame, scorecard: pd.DataFrame) -> None:
    failed = diagnostics.loc[diagnostics["status"].eq("fail")]
    warns = diagnostics.loc[diagnostics["status"].eq("warn")]
    lines = [
        "# Phase 2 Falsification Failure Report",
        "",
        "## Summary",
        "",
        f"Job `{JOB_ID}` produced expected decisions for `{len(scorecard)}` visible calibration tasks.",
        "",
        "This report is not an alpha decision. It documents why the task bank should reject weak, leaked, or infeasible ideas.",
        "",
        "## Failed Gates",
        "",
    ]
    if failed.empty:
        lines.append("- None recorded.")
    else:
        lines.extend(f"- {row.check}: {row.value} ({row.notes})" for row in failed.itertuples())
    lines.extend(["", "## Warnings", ""])
    if warns.empty:
        lines.append("- None recorded.")
    else:
        lines.extend(f"- {row.check}: {row.value} ({row.notes})" for row in warns.itertuples())
    lines.extend(["", "## Expected Rejections", ""])
    for row in scorecard.itertuples():
        lines.append(f"- `{row.task_id}`: `{row.automated_evaluator_decision}` because {row.primary_failure_reason}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def make_review(path: Path) -> None:
    text = f"""# Manual Review

## Run Identity

- job_id: `{JOB_ID}`
- status: pending human review

## Artifact Completeness

- [ ] run_manifest.yaml exists
- [ ] metrics.json exists
- [ ] task_scorecard.csv exists
- [ ] diagnostics.csv exists
- [ ] failure_report.md exists
- [ ] random_rank_seed_metrics.csv exists
- [ ] random_rank_detailed_metrics.csv exists
- [ ] identifier_artifact_metrics.csv exists
- [ ] leakage_trap_metrics.csv exists
- [ ] implementation_feasibility.csv exists

## Reviewer Decision

- [ ] accept artifacts as Phase 2 calibration evidence
- [ ] revise and rerun
- [ ] blocked

## Notes

TBD.
"""
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=Path, default=Path("/home/b08303004/Desktop/WRDS/data"))
    parser.add_argument("--data-path", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--total-cost-bps", type=float, default=2.5)
    parser.add_argument("--random-seeds", type=int, default=5)
    args = parser.parse_args()

    if args.data_path is None:
        args.data_path = args.data_root / "daily_stock" / "gago9dveytpx6922.csv"
    if args.random_seeds <= 0:
        raise ValueError("--random-seeds must be positive")
    if args.data_path is None or not args.data_path.exists():
        raise FileNotFoundError(f"daily_stock file not found: {args.data_path}")

    args.output_dir.mkdir(parents=True, exist_ok=True)

    raw = load_daily_stock(args.data_path)
    panel, base_diagnostics = prepare_base_panel(raw)

    random_summary, random_detail = random_rank_seed_metrics(panel, args.total_cost_bps, args.random_seeds)
    identifier_detail, _ = identifier_artifact_metrics(panel, args.total_cost_bps)
    leak_portfolio = build_same_day_leak_portfolio(panel, args.total_cost_bps)
    leakage_metrics = pd.DataFrame(flatten_metrics("FAL-002", leak_portfolio))
    implementation = implementation_feasibility(panel)
    survivorship = survivorship_diagnostics(panel)
    scorecard = task_scorecard()

    diagnostics = pd.concat(
        [
            base_diagnostics.assign(task_id="ALL"),
            survivorship.rename(columns={"threshold": "threshold"}),
            implementation.rename(columns={"task_id": "task_id"}),
            pd.DataFrame(
                [
                    {
                        "task_id": "FAL-002",
                        "check": "same_day_return_used_as_signal",
                        "status": "fail",
                        "value": "DlyRetx_t",
                        "threshold": "signal must be known before traded return",
                        "notes": "This is intentionally marked fail for the leakage trap.",
                    },
                    {
                        "task_id": "ALL",
                        "check": "task_scorecard_complete",
                        "status": "pass" if len(scorecard) == 5 else "fail",
                        "value": len(scorecard),
                        "threshold": 5,
                        "notes": "",
                    },
                    {
                        "task_id": "ALL",
                        "check": "no_ibkr_or_broker_dependency",
                        "status": "pass",
                        "value": "no broker imports, credentials, account state, or order endpoints used",
                        "threshold": "remote falsification run is data-only",
                        "notes": "IBKR/TWS access is local-only; this remote script does not attempt broker connectivity.",
                    },
                ]
            ),
        ],
        ignore_index=True,
        sort=False,
    )

    reject_expected = scorecard["expected_decision"].isin(["reject", "reject_or_revise"])
    automated_false_accepts = int(((scorecard["automated_evaluator_decision"] == "proceed") & reject_expected).sum())
    null_discipline_score = 100.0 * (1.0 - automated_false_accepts / max(int(reject_expected.sum()), 1))

    metrics = {
        "job_id": JOB_ID,
        "status": "completed_with_expected_failures" if diagnostics["status"].eq("fail").any() else "completed",
        "task_bank_version": TASK_BANK_VERSION,
        "raw_rows": int(len(raw)),
        "base_panel_rows": int(len(panel)),
        "task_count": int(len(scorecard)),
        "reject_expected_task_count": int(reject_expected.sum()),
        "automated_false_accept_count": automated_false_accepts,
        "automated_null_discipline_score": null_discipline_score,
        "random_rank": {
            "seed_count": int(args.random_seeds),
            "validation_sharpe_min": float(random_summary.loc[random_summary["split"].eq("validation"), "sharpe"].min()),
            "validation_sharpe_max": float(random_summary.loc[random_summary["split"].eq("validation"), "sharpe"].max()),
            "test_sharpe_min": float(random_summary.loc[random_summary["split"].eq("test"), "sharpe"].min()),
            "test_sharpe_max": float(random_summary.loc[random_summary["split"].eq("test"), "sharpe"].max()),
        },
        "required_human_scoring_note": "Official Phase 2 score requires comparing agent decisions against expected decisions.",
    }

    write_manifest(args.output_dir / "run_manifest.yaml", args, len(raw), len(panel))
    write_json(args.output_dir / "metrics.json", metrics)
    scorecard.to_csv(args.output_dir / "task_scorecard.csv", index=False)
    diagnostics.insert(0, "job_id", JOB_ID)
    diagnostics.to_csv(args.output_dir / "diagnostics.csv", index=False)
    random_summary.to_csv(args.output_dir / "random_rank_seed_metrics.csv", index=False)
    random_detail.to_csv(args.output_dir / "random_rank_detailed_metrics.csv", index=False)
    identifier_detail.to_csv(args.output_dir / "identifier_artifact_metrics.csv", index=False)
    leakage_metrics.to_csv(args.output_dir / "leakage_trap_metrics.csv", index=False)
    implementation.to_csv(args.output_dir / "implementation_feasibility.csv", index=False)
    make_failure_report(args.output_dir / "failure_report.md", diagnostics, scorecard)
    make_review(args.output_dir / "review.md")
    print(f"Wrote Phase 2 falsification artifact bundle to {args.output_dir}")


if __name__ == "__main__":
    main()
