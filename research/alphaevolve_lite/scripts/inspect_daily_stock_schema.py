"""Inspect a bounded sample of the remote daily_stock CSV schema."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


CANDIDATE_FIELDS = {
    "date": ["DlyCalDt", "date", "Date", "CALDT", "caldt"],
    "identifier": ["PERMNO", "permno", "permco", "PERMCO"],
    "return": ["DlyRet", "RET", "ret", "DlyRetx", "RETX", "retx"],
    "price": ["DlyPrc", "PRC", "prc", "price"],
    "volume": ["DlyVol", "VOL", "vol", "volume"],
    "dollar_volume": ["DlyPrcVol", "dollar_volume", "dolvol"],
    "shares_or_market_cap": ["ShrOut", "SHROUT", "shrout", "MktCap", "market_cap", "mktcap"],
    "exchange": ["PrimaryExch", "primary_exchange", "EXCHCD", "exchcd"],
    "security_type": ["SecurityType", "security_type", "SHRCD", "shrcd"],
    "industry": ["SICCD", "NAICS", "ICBIndustry"],
}

REQUIRED_GROUPS = ["date", "identifier", "return"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect daily_stock CSV schema from a bounded sample.")
    parser.add_argument("--csv-path", required=True, help="Remote path to daily_stock CSV.")
    parser.add_argument("--out-dir", required=True, help="Directory for schema reports.")
    parser.add_argument("--sample-rows", type=int, default=50000, help="Maximum rows to sample.")
    return parser.parse_args()


def _import_pandas():
    try:
        import pandas as pd
    except Exception as exc:  # pragma: no cover - environment dependent
        raise RuntimeError("pandas is required for schema inspection") from exc
    return pd


def detect_candidates(columns: list[str]) -> dict[str, list[str]]:
    column_set = set(columns)
    lower_map = {col.lower(): col for col in columns}
    detected: dict[str, list[str]] = {}
    for group, candidates in CANDIDATE_FIELDS.items():
        hits: list[str] = []
        for candidate in candidates:
            if candidate in column_set:
                hits.append(candidate)
            elif candidate.lower() in lower_map:
                hits.append(lower_map[candidate.lower()])
        detected[group] = sorted(set(hits))
    return detected


def infer_date_range(pd: Any, sample: Any, date_candidates: list[str]) -> dict[str, str | None]:
    for col in date_candidates:
        try:
            parsed = pd.to_datetime(sample[col], errors="coerce")
        except Exception:
            continue
        valid = parsed.dropna()
        if not valid.empty:
            return {
                "date_column": col,
                "min_sample_date": str(valid.min().date()),
                "max_sample_date": str(valid.max().date()),
            }
    return {"date_column": None, "min_sample_date": None, "max_sample_date": None}


def write_reports(out_dir: Path, report: dict[str, Any]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "daily_stock_schema_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    lines = [
        "# Daily Stock Schema Report",
        "",
        f"- csv path: {report['csv_path']}",
        f"- sample rows requested: {report['sample_rows_requested']}",
        f"- sample rows read: {report['sample_rows_read']}",
        f"- column count: {len(report['columns'])}",
        "",
        "## Candidate Fields",
        "",
    ]
    for group, hits in report["candidate_fields"].items():
        value = ", ".join(hits) if hits else "MISSING"
        lines.append(f"- {group}: {value}")
    lines.extend(
        [
            "",
            "## Date Range",
            "",
            f"- date column: {report['sample_date_range']['date_column']}",
            f"- min sample date: {report['sample_date_range']['min_sample_date']}",
            f"- max sample date: {report['sample_date_range']['max_sample_date']}",
            "",
            "## Warnings",
            "",
        ]
    )
    if report["warnings"]:
        lines.extend(f"- {warning}" for warning in report["warnings"])
    else:
        lines.append("- none")
    lines.append("")
    (out_dir / "daily_stock_schema_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    csv_path = Path(args.csv_path)
    if not csv_path.exists():
        print(f"ERROR: CSV path does not exist: {csv_path}", file=sys.stderr)
        return 1
    if args.sample_rows <= 0:
        print("ERROR: --sample-rows must be positive", file=sys.stderr)
        return 1

    pd = _import_pandas()
    sample = pd.read_csv(csv_path, nrows=args.sample_rows, low_memory=False)
    columns = [str(col) for col in sample.columns]
    candidate_fields = detect_candidates(columns)
    missing_required = [group for group in REQUIRED_GROUPS if not candidate_fields.get(group)]
    warnings = [f"required candidate group missing: {group}" for group in missing_required]

    report = {
        "csv_path": str(csv_path),
        "sample_rows_requested": args.sample_rows,
        "sample_rows_read": int(len(sample)),
        "columns": columns,
        "dtypes": {str(col): str(dtype) for col, dtype in sample.dtypes.items()},
        "missingness_by_column": {
            str(col): float(sample[col].isna().mean()) for col in sample.columns
        },
        "candidate_fields": candidate_fields,
        "sample_date_range": infer_date_range(pd, sample, candidate_fields.get("date", [])),
        "warnings": warnings,
    }
    write_reports(Path(args.out_dir), report)
    print(json.dumps({"status": "ok", "out_dir": args.out_dir}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
