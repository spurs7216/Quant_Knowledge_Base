"""
Task 001: daily_stock short-horizon reversal remote validation.

Run on the remote Ubuntu machine that has the full WRDS mirror.

Example:
    python research/remote_validation/task001_daily_stock_short_reversal.py \
        --data-root /home/b08303004/Desktop/WRDS/data \
        --output-dir artifacts/remote_runs/20260423_task001_daily_stock_short_reversal

The script writes a compact artifact bundle only. It does not copy raw data.
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


JOB_ID = "20260423_task001_daily_stock_short_reversal"
REQUIRED_COLUMNS = [
    "PERMNO",
    "DlyCalDt",
    "DlyRetx",
    "DlyPrc",
    "DlyVol",
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

PORTFOLIO_COLUMNS = [
    "DlyCalDt",
    "signal_date",
    "gross_return",
    "net_return",
    "turnover",
    "n_long",
    "n_short",
    "vwretd",
    "sprtrn",
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


def split_metrics(df: pd.DataFrame, split: Split) -> dict[str, float]:
    if df.empty or "DlyCalDt" not in df.columns:
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
            "mean_daily_n_long": float("nan"),
            "mean_daily_n_short": float("nan"),
            "gross_exposure": float("nan"),
            "net_exposure": float("nan"),
            "nonfinite_return_count": 0,
        }
    mask = (df["DlyCalDt"] >= split.start) & (df["DlyCalDt"] <= split.end)
    part = df.loc[mask].copy()
    rets = part.set_index("DlyCalDt")["net_return"]
    gross_rets = part.set_index("DlyCalDt")["gross_return"]
    mkt = part.set_index("DlyCalDt")["vwretd"]
    ann = 252.0
    mean = rets.mean()
    vol = rets.std(ddof=1)
    gross_mean = gross_rets.mean()
    gross_vol = gross_rets.std(ddof=1)
    return {
        "annualized_return": float(mean * ann) if pd.notna(mean) else float("nan"),
        "annualized_volatility": float(vol * math.sqrt(ann)) if pd.notna(vol) else float("nan"),
        "sharpe": float(mean / vol * math.sqrt(ann)) if vol and vol > 0 else float("nan"),
        "gross_annualized_return": float(gross_mean * ann) if pd.notna(gross_mean) else float("nan"),
        "gross_sharpe": float(gross_mean / gross_vol * math.sqrt(ann)) if gross_vol and gross_vol > 0 else float("nan"),
        "max_drawdown": max_drawdown(rets),
        "turnover": float(part["turnover"].mean()) if len(part) else float("nan"),
        "hit_rate": float((rets > 0).mean()) if len(rets) else float("nan"),
        "beta_to_vwretd": beta_to_market(rets, mkt),
        "mean_daily_n_long": float(part["n_long"].mean()) if len(part) else float("nan"),
        "mean_daily_n_short": float(part["n_short"].mean()) if len(part) else float("nan"),
        "gross_exposure": 1.0,
        "net_exposure": 0.0,
        "nonfinite_return_count": int((~np.isfinite(rets.to_numpy())).sum()) if len(rets) else 0,
    }


def make_scorecard(metrics: dict[str, Any]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for split in SPLITS:
        split_metrics_dict = metrics.get(split.name, {})
        for metric, value in split_metrics_dict.items():
            rows.append(
                {
                    "job_id": JOB_ID,
                    "split": split.name,
                    "start_date": split.start,
                    "end_date": split.end,
                    "metric": metric,
                    "value": value,
                    "unit": "decimal_or_count",
                    "notes": "",
                }
            )
    return pd.DataFrame(rows)


def load_daily_stock(path: Path) -> pd.DataFrame:
    usecols = REQUIRED_COLUMNS
    df = pd.read_csv(path, usecols=usecols, parse_dates=["DlyCalDt"], low_memory=False)
    for col in ["DlyRetx", "DlyPrc", "DlyVol", "vwretd", "sprtrn"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def prepare_panel(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    diagnostics: list[dict[str, Any]] = []
    diagnostics.append({"check": "raw_rows", "status": "info", "value": len(df), "threshold": "", "notes": ""})
    diagnostics.append(
        {
            "check": "duplicate_permno_date_before_filters",
            "status": "warn" if df.duplicated(["PERMNO", "DlyCalDt"]).any() else "pass",
            "value": int(df.duplicated(["PERMNO", "DlyCalDt"]).sum()),
            "threshold": 0,
            "notes": "Duplicate security-date rows should be investigated if nonzero.",
        }
    )

    filtered = df.loc[
        (df["SecurityType"] == "EQTY")
        & (df["ShareType"] == "NS")
        & (df["TradingStatusFlg"] == "A")
        & (df["DlyPrc"].abs() > 5)
        & (df["DlyVol"] > 0)
        & df["DlyRetx"].notna()
        & df["vwretd"].notna()
    ].copy()
    filtered.sort_values(["PERMNO", "DlyCalDt"], inplace=True)
    filtered["rx"] = filtered["DlyRetx"] - filtered["vwretd"]
    grouped = filtered.groupby("PERMNO", sort=False)
    filtered["prior_obs"] = grouped.cumcount()
    filtered["signal"] = -grouped["rx"].transform(lambda x: x.shift(1).rolling(5).sum())
    filtered["fwd_ret"] = grouped["DlyRetx"].shift(-1)
    filtered["fwd_date"] = grouped["DlyCalDt"].shift(-1)
    filtered = filtered.loc[
        (filtered["prior_obs"] >= 60)
        & filtered["signal"].notna()
        & filtered["fwd_ret"].notna()
    ].copy()

    diagnostics.append({"check": "rows_after_filters", "status": "info", "value": len(filtered), "threshold": "", "notes": ""})
    diagnostics.append(
        {
            "check": "duplicate_permno_date_after_filters",
            "status": "warn" if filtered.duplicated(["PERMNO", "DlyCalDt"]).any() else "pass",
            "value": int(filtered.duplicated(["PERMNO", "DlyCalDt"]).sum()),
            "threshold": 0,
            "notes": "",
        }
    )
    return filtered, pd.DataFrame(diagnostics)


def build_portfolio(panel: pd.DataFrame, total_cost_bps: float) -> tuple[pd.DataFrame, pd.DataFrame]:
    results: list[dict[str, Any]] = []
    universe_rows: list[dict[str, Any]] = []
    prev_weights: pd.Series | None = None
    cost_rate = total_cost_bps / 10000.0

    for date, g in panel.groupby("DlyCalDt", sort=True):
        g = g.dropna(subset=["signal", "fwd_ret"])
        n = len(g)
        universe_rows.append({"DlyCalDt": date, "n_eligible": n})
        if n < 20:
            continue
        q_long = g["signal"].quantile(0.9)
        q_short = g["signal"].quantile(0.1)
        longs = g.loc[g["signal"] >= q_long, ["PERMNO", "fwd_ret", "vwretd", "sprtrn"]]
        shorts = g.loc[g["signal"] <= q_short, ["PERMNO", "fwd_ret", "vwretd", "sprtrn"]]
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

        ret_map = pd.concat([longs[["PERMNO", "fwd_ret"]], shorts[["PERMNO", "fwd_ret"]]]).drop_duplicates("PERMNO").set_index("PERMNO")["fwd_ret"]
        gross_return = float((weights * ret_map.reindex(weights.index)).sum())
        net_return = gross_return - turnover * cost_rate
        fwd_date = g["fwd_date"].iloc[0]
        results.append(
            {
                "DlyCalDt": pd.Timestamp(fwd_date),
                "signal_date": pd.Timestamp(date),
                "gross_return": gross_return,
                "net_return": net_return,
                "turnover": turnover,
                "n_long": int(len(longs)),
                "n_short": int(len(shorts)),
                "vwretd": float(g["vwretd"].iloc[0]),
                "sprtrn": float(g["sprtrn"].iloc[0]),
            }
        )

    portfolio = pd.DataFrame(results, columns=PORTFOLIO_COLUMNS)
    if not portfolio.empty:
        portfolio = portfolio.sort_values("DlyCalDt")
    return portfolio, pd.DataFrame(universe_rows)


def cost_sensitivity(panel: pd.DataFrame, costs: list[float]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for cost in costs:
        portfolio, _ = build_portfolio(panel, cost)
        if portfolio.empty:
            rows.append({"total_cost_bps": cost, "split": "all", "sharpe": float("nan"), "annualized_return": float("nan"), "turnover": float("nan")})
            continue
        all_split = Split("all", str(portfolio["DlyCalDt"].min().date()), str(portfolio["DlyCalDt"].max().date()))
        sm = split_metrics(portfolio, all_split)
        rows.append(
            {
                "total_cost_bps": cost,
                "split": "all",
                "sharpe": sm["sharpe"],
                "annualized_return": sm["annualized_return"],
                "turnover": sm["turnover"],
            }
        )
    return pd.DataFrame(rows)


def write_json(path: Path, data: dict[str, Any]) -> None:
    def clean(obj: Any) -> Any:
        if isinstance(obj, dict):
            return {str(k): clean(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [clean(v) for v in obj]
        if isinstance(obj, tuple):
            return [clean(v) for v in obj]
        if isinstance(obj, (pd.Timestamp, datetime)):
            return obj.isoformat()
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return finite_float(obj)
        if isinstance(obj, float):
            return obj if math.isfinite(obj) else None
        return obj

    path.write_text(json.dumps(clean(data), indent=2, allow_nan=False), encoding="utf-8")


def write_manifest(path: Path, args: argparse.Namespace, row_count: int) -> None:
    snapshot = git_snapshot()
    manifest = {
        "schema_version": 0.1,
        "job_id": JOB_ID,
        "created": datetime.now().isoformat(timespec="seconds"),
        "environment": "remote_validation",
        "sync": {"channel": "github", "remote_os": "ubuntu", "artifact_import_policy": "manual_review"},
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
                "row_count_observed": row_count,
                "required_columns": REQUIRED_COLUMNS,
            }
        ],
        "signal": {
            "definition": "s_i_t = -sum_{k=1}^5 (DlyRetx_i_{t-k} - vwretd_{t-k})",
            "return_timing": "signal after close t, earn DlyRetx on t+1",
        },
        "cost_model": {"total_cost_bps": args.total_cost_bps},
    }
    path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def make_failure_report(path: Path, diagnostics: pd.DataFrame, metrics: dict[str, Any]) -> None:
    failed = diagnostics.loc[diagnostics["status"].eq("fail")]
    warns = diagnostics.loc[diagnostics["status"].eq("warn")]
    lines = [
        "# Failure Report",
        "",
        "## Summary",
        "",
        f"Job `{JOB_ID}` completed with status `{metrics.get('status')}`.",
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
    lines.extend(
        [
            "",
            "## Data Caveats",
            "",
            "- Price filter uses `abs(DlyPrc) > 5` because CRSP-like price fields can use sign conventions.",
            "- This baseline does not adjust for sector or industry exposure.",
            "",
            "## Implementation Caveats",
            "",
            "- The strategy is an auditable workflow baseline, not an alpha claim.",
            "- Borrow costs are set to zero in the first pass.",
            "",
            "## Decision Implications",
            "",
            "- Review the artifact bundle before importing it as approved evidence.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def make_review(path: Path) -> None:
    text = f"""# Manual Review

## Run Identity

- job_id: `{JOB_ID}`
- status: pending human review

## Artifact Completeness

- [ ] run_manifest.yaml exists
- [ ] metrics.json exists
- [ ] scorecard.csv exists
- [ ] diagnostics.csv exists
- [ ] failure_report.md exists
- [ ] optional diagnostics reviewed

## Reviewer Decision

- [ ] approved for local artifact import
- [ ] revise and rerun
- [ ] reject

## Reasons

TBD.

## Required Follow-Up

TBD.
"""
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=Path, default=Path("/home/b08303004/Desktop/WRDS/data"))
    parser.add_argument("--data-path", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--total-cost-bps", type=float, default=2.5)
    args = parser.parse_args()

    if args.data_path is None:
        args.data_path = args.data_root / "daily_stock" / "gago9dveytpx6922.csv"

    args.output_dir.mkdir(parents=True, exist_ok=True)
    if not args.data_path.exists():
        raise FileNotFoundError(f"daily_stock file not found: {args.data_path}")

    raw = load_daily_stock(args.data_path)
    panel, diagnostics = prepare_panel(raw)
    portfolio, universe_counts = build_portfolio(panel, args.total_cost_bps)

    diagnostics = pd.concat(
        [
            diagnostics,
            pd.DataFrame(
                [
                    {
                        "check": "portfolio_rows",
                        "status": "pass" if len(portfolio) else "fail",
                        "value": len(portfolio),
                        "threshold": ">0",
                        "notes": "",
                    },
                    {
                        "check": "nonfinite_portfolio_returns",
                        "status": "fail" if portfolio.empty or (~np.isfinite(portfolio["net_return"])).any() else "pass",
                        "value": int((~np.isfinite(portfolio["net_return"])).sum()) if not portfolio.empty else "",
                        "threshold": 0,
                        "notes": "",
                    },
                ]
            ),
        ],
        ignore_index=True,
    )

    has_failed_gate = diagnostics["status"].eq("fail").any()
    has_warning = diagnostics["status"].eq("warn").any()
    if has_failed_gate:
        run_status = "failed_gates"
    elif has_warning:
        run_status = "completed_with_warnings"
    else:
        run_status = "completed"

    metrics: dict[str, Any] = {
        "job_id": JOB_ID,
        "status": run_status,
        "date_range": {"min": str(raw["DlyCalDt"].min().date()), "max": str(raw["DlyCalDt"].max().date())},
        "universe": {
            "raw_rows": int(len(raw)),
            "eligible_signal_rows": int(len(panel)),
            "portfolio_days": int(len(portfolio)),
        },
        "cost_model": {"total_cost_bps": args.total_cost_bps},
        "failure_gates": diagnostics.set_index("check")["status"].to_dict(),
    }
    for split in SPLITS:
        metrics[split.name] = split_metrics(portfolio, split)

    write_manifest(args.output_dir / "run_manifest.yaml", args, len(raw))
    write_json(args.output_dir / "metrics.json", metrics)
    make_scorecard(metrics).to_csv(args.output_dir / "scorecard.csv", index=False)
    diagnostics.insert(0, "job_id", JOB_ID)
    diagnostics.to_csv(args.output_dir / "diagnostics.csv", index=False)
    if not universe_counts.empty:
        universe_counts["month"] = universe_counts["DlyCalDt"].dt.to_period("M").astype(str)
        universe_counts.groupby("month", as_index=False)["n_eligible"].mean().to_csv(args.output_dir / "universe_counts_by_month.csv", index=False)
    else:
        pd.DataFrame(columns=["month", "n_eligible"]).to_csv(args.output_dir / "universe_counts_by_month.csv", index=False)
    cost_sensitivity(panel, [0.0, 2.5, 5.0, 10.0]).to_csv(args.output_dir / "cost_sensitivity.csv", index=False)
    for split in SPLITS:
        split_port = portfolio[(portfolio["DlyCalDt"] >= split.start) & (portfolio["DlyCalDt"] <= split.end)]
        split_port.assign(split=split.name).to_csv(args.output_dir / f"returns_{split.name}.csv", index=False)
    make_failure_report(args.output_dir / "failure_report.md", diagnostics, metrics)
    make_review(args.output_dir / "review.md")
    print(f"Wrote artifact bundle to {args.output_dir}")


if __name__ == "__main__":
    main()
