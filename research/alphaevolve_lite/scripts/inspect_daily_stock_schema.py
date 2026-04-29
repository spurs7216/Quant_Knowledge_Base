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
    "market_cap": ["DlyCap", "MktCap", "market_cap", "mktcap"],
    "shares_outstanding": ["ShrOut", "SHROUT", "shrout"],
    "shares_or_market_cap": ["DlyCap", "ShrOut", "SHROUT", "shrout", "MktCap", "market_cap", "mktcap"],
    "exchange": ["PrimaryExch", "primary_exchange", "EXCHCD", "exchcd"],
    "security_type": ["SecurityType", "security_type", "SHRCD", "shrcd"],
    "share_type": ["ShareType", "share_type"],
    "trading_status": ["TradingStatusFlg", "trading_status", "trading_status_flag"],
    "conditional_type": ["ConditionalType", "conditional_type"],
    "us_incorporated": ["USIncFlg", "us_incorporated", "us_inc_flag"],
    "industry": ["SICCD", "NAICS", "ICBIndustry"],
    "benchmark_return": ["vwretd", "vwretx", "ewretd", "ewretx", "sprtrn"],
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
        detected[group] = list(dict.fromkeys(hits))
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


def infer_field_mapping(candidate_fields: dict[str, list[str]]) -> dict[str, str | None]:
    """Choose conservative primary fields for implementation contracts."""

    return {
        "date": _first(candidate_fields.get("date")),
        "security_id": _prefer(candidate_fields.get("identifier"), ["PERMNO", "permno"]),
        "issuer_id": _prefer(candidate_fields.get("identifier"), ["PERMCO", "permco"]),
        "total_return": _prefer(candidate_fields.get("return"), ["DlyRet", "RET", "ret"]),
        "ex_dividend_return": _prefer(candidate_fields.get("return"), ["DlyRetx", "RETX", "retx"]),
        "price": _first(candidate_fields.get("price")),
        "volume": _first(candidate_fields.get("volume")),
        "dollar_volume": _first(candidate_fields.get("dollar_volume")),
        "market_cap": _first(candidate_fields.get("market_cap")),
        "shares_outstanding": _first(candidate_fields.get("shares_outstanding")),
        "exchange": _first(candidate_fields.get("exchange")),
        "security_type": _first(candidate_fields.get("security_type")),
        "share_type": _first(candidate_fields.get("share_type")),
        "trading_status": _first(candidate_fields.get("trading_status")),
        "conditional_type": _first(candidate_fields.get("conditional_type")),
        "us_incorporated": _first(candidate_fields.get("us_incorporated")),
        "industry_primary": _prefer(candidate_fields.get("industry"), ["SICCD", "NAICS", "ICBIndustry"]),
        "benchmark_return_primary": _prefer(candidate_fields.get("benchmark_return"), ["vwretd", "sprtrn"]),
    }


def _first(values: list[str] | None) -> str | None:
    return values[0] if values else None


def _prefer(values: list[str] | None, preferred: list[str]) -> str | None:
    if not values:
        return None
    for candidate in preferred:
        if candidate in values:
            return candidate
    return values[0]


def summarize_columns(pd: Any, sample: Any, columns: list[str]) -> dict[str, Any]:
    summaries: dict[str, Any] = {}
    for col in columns:
        if col not in sample.columns:
            continue
        series = sample[col]
        item: dict[str, Any] = {
            "dtype": str(series.dtype),
            "missing_rate": float(series.isna().mean()),
            "unique_in_sample": int(series.nunique(dropna=True)),
        }
        if pd.api.types.is_numeric_dtype(series):
            numeric = pd.to_numeric(series, errors="coerce").dropna()
            if not numeric.empty:
                quantiles = numeric.quantile([0.0, 0.01, 0.05, 0.5, 0.95, 0.99, 1.0])
                item["numeric_summary"] = {
                    str(key): float(value) for key, value in quantiles.items()
                }
                item["mean"] = float(numeric.mean())
        else:
            counts = series.fillna("<NA>").astype(str).value_counts(dropna=False).head(20)
            item["top_values"] = {str(key): int(value) for key, value in counts.items()}
        summaries[col] = item
    return summaries


def write_field_mapping(out_dir: Path, field_mapping: dict[str, str | None]) -> None:
    lines = [
        "# Generated by inspect_daily_stock_schema.py from a bounded sample.",
        "# Review before treating this as the frozen daily_stock contract.",
    ]
    for key, value in field_mapping.items():
        rendered = "null" if value is None else value
        lines.append(f"{key}: {rendered}")
    lines.append("")
    (out_dir / "daily_stock_field_mapping.yaml").write_text("\n".join(lines), encoding="utf-8")


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
    lines.extend(["", "## Primary Field Mapping", ""])
    for field, value in report["field_mapping"].items():
        lines.append(f"- {field}: {value or 'MISSING'}")
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
    write_field_mapping(out_dir, report["field_mapping"])


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
    field_mapping = infer_field_mapping(candidate_fields)
    missing_required = [group for group in REQUIRED_GROUPS if not candidate_fields.get(group)]
    warnings = [f"required candidate group missing: {group}" for group in missing_required]
    contract_columns = list(dict.fromkeys(col for col in field_mapping.values() if col))

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
        "field_mapping": field_mapping,
        "contract_column_diagnostics": summarize_columns(pd, sample, contract_columns),
        "sample_date_range": infer_date_range(pd, sample, candidate_fields.get("date", [])),
        "warnings": warnings,
    }
    write_reports(Path(args.out_dir), report)
    sample.head(20).to_csv(Path(args.out_dir) / "daily_stock_sample_head.csv", index=False)
    print(json.dumps({"status": "ok", "out_dir": args.out_dir}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
