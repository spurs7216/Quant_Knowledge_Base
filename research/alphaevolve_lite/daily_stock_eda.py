"""Daily-stock empirical profiling for Phase 4 search.

This module turns the frozen daily_stock contract into compact evidence for
child generation. It is deliberately separate from strategy evaluation: the
output is a data-understanding artifact, not alpha evidence.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

import numpy as np
import pandas as pd

from .artifact_io import write_json
from .daily_stock_contract import CONTRACT, DailyStockContract, unique_preserving_order, validate_columns
from .daily_stock_loader import (
    apply_duplicate_policy,
    apply_static_eligibility,
    coerce_daily_stock_frame,
    load_daily_stock_window,
    static_eligibility_mask,
)
from .universe import apply_monthly_universe, build_monthly_rolling_universe


EDA_SCHEMA_VERSION = "daily_stock_empirical_map_v1"

OPTIONAL_PROFILE_COLUMNS = (
    "Ticker",
    "NAICS",
    "ICBIndustry",
    "DlyRetMissFlg",
    "DlyPrcFlg",
    "DlyCapFlg",
    "DlyVolFlg",
    "DlyNumTrd",
    "DlyBid",
    "DlyAsk",
    "DlyOpen",
    "DlyClose",
    "DlyLow",
    "DlyHigh",
)

PROFILE_NUMERIC_COLUMNS = (
    "DlyRet",
    "DlyRetx",
    "excess_return_vs_vwretd",
    "DlyPrc",
    "abs_price",
    "DlyVol",
    "DlyPrcVol",
    "DlyCap",
    "ShrOut",
    "vwretd",
    "sprtrn",
    "log_abs_price",
    "log_volume",
    "log_dollar_volume",
    "log_market_cap",
)

PROFILE_CATEGORICAL_COLUMNS = (
    "PrimaryExch",
    "SecurityType",
    "ShareType",
    "TradingStatusFlg",
    "ConditionalType",
    "USIncFlg",
    "SICCD",
    "DlyRetMissFlg",
    "DlyPrcFlg",
    "DlyCapFlg",
    "DlyVolFlg",
)


@dataclass
class NumericAccumulator:
    """Streaming numeric moments and extrema for one column."""

    column: str
    row_count: int = 0
    finite_count: int = 0
    missing_count: int = 0
    positive_count: int = 0
    zero_count: int = 0
    negative_count: int = 0
    sum_value: float = 0.0
    sum_square: float = 0.0
    min_value: float | None = None
    max_value: float | None = None

    def update(self, values: pd.Series) -> None:
        numeric = pd.to_numeric(values, errors="coerce")
        self.row_count += int(len(numeric))
        finite = numeric[np.isfinite(numeric)]
        self.finite_count += int(len(finite))
        self.missing_count += int(len(numeric) - len(finite))
        if finite.empty:
            return
        self.positive_count += int(finite.gt(0.0).sum())
        self.zero_count += int(finite.eq(0.0).sum())
        self.negative_count += int(finite.lt(0.0).sum())
        self.sum_value += float(finite.sum())
        self.sum_square += float((finite * finite).sum())
        current_min = float(finite.min())
        current_max = float(finite.max())
        self.min_value = current_min if self.min_value is None else min(self.min_value, current_min)
        self.max_value = current_max if self.max_value is None else max(self.max_value, current_max)

    def to_record(self) -> dict[str, Any]:
        mean = self.sum_value / self.finite_count if self.finite_count else None
        variance = None
        if self.finite_count > 1 and mean is not None:
            variance = max(0.0, self.sum_square / self.finite_count - mean * mean)
        return {
            "column": self.column,
            "row_count": self.row_count,
            "finite_count": self.finite_count,
            "missing_count": self.missing_count,
            "missing_rate": self.missing_count / self.row_count if self.row_count else None,
            "positive_count": self.positive_count,
            "zero_count": self.zero_count,
            "negative_count": self.negative_count,
            "mean": mean,
            "std_population": variance**0.5 if variance is not None else None,
            "min": self.min_value,
            "max": self.max_value,
        }


@dataclass
class ScanState:
    """Mutable state for a chunked full-scan profile."""

    contract: DailyStockContract
    numeric_stats: dict[str, NumericAccumulator] = field(default_factory=dict)
    eligible_numeric_stats: dict[str, NumericAccumulator] = field(default_factory=dict)
    categorical_counts: dict[str, Counter[str]] = field(default_factory=dict)
    eligible_categorical_counts: dict[str, Counter[str]] = field(default_factory=dict)
    daily_row_counts: Counter[str] = field(default_factory=Counter)
    daily_eligible_counts: Counter[str] = field(default_factory=Counter)
    unique_permnos: set[int] = field(default_factory=set)
    unique_eligible_permnos: set[int] = field(default_factory=set)
    row_count: int = 0
    date_filtered_row_count: int = 0
    sample_frames: list[pd.DataFrame] = field(default_factory=list)
    eligibility_steps: Counter[str] = field(default_factory=Counter)


def profile_daily_stock_data(
    *,
    csv_path: str | Path,
    out_dir: str | Path,
    chunksize: int = 1_000_000,
    start_date: str | None = None,
    end_date: str | None = None,
    max_input_rows: int | None = None,
    sample_modulus: int = 200,
    max_sample_rows: int = 300_000,
    deep_start_date: str | None = None,
    deep_end_date: str | None = None,
    deep_top_n: int = 500,
) -> dict[str, Any]:
    """Run the Phase 4 daily_stock empirical map and write artifacts."""

    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    csv = Path(csv_path)
    columns = _read_header(csv)
    validate_columns(columns, CONTRACT)
    usecols = _profile_usecols(columns, CONTRACT)

    scan = _scan_csv(
        csv,
        usecols=usecols,
        chunksize=chunksize,
        start_date=start_date,
        end_date=end_date,
        max_input_rows=max_input_rows,
        sample_modulus=sample_modulus,
        max_sample_rows=max_sample_rows,
        contract=CONTRACT,
    )
    sample = _sample_frame(scan)
    numeric_summary = _numeric_summary_frame(scan.numeric_stats, sample, PROFILE_NUMERIC_COLUMNS)
    eligible_numeric_summary = _numeric_summary_frame(
        scan.eligible_numeric_stats,
        sample.loc[sample["eligible_static_return"]].copy() if "eligible_static_return" in sample else sample.iloc[0:0],
        PROFILE_NUMERIC_COLUMNS,
    )
    categorical_counts = _counter_frame(scan.categorical_counts, "raw_count")
    eligible_categorical_counts = _counter_frame(scan.eligible_categorical_counts, "eligible_count")
    daily_counts = _daily_counts_frame(scan.daily_row_counts, scan.daily_eligible_counts)

    deep_payload = _build_deep_window_profile(
        csv_path=csv,
        out_dir=out,
        start_date=deep_start_date or start_date,
        end_date=deep_end_date or end_date,
        chunksize=chunksize,
        max_input_rows=max_input_rows,
        top_n=deep_top_n,
    )
    guidance = build_data_guidance(
        scan_summary=_scan_summary(scan, csv, start_date, end_date, max_input_rows, sample_modulus),
        numeric_summary=eligible_numeric_summary,
        daily_counts=daily_counts,
        deep_summary=deep_payload.get("summary", {}),
    )

    paths = _write_profile_artifacts(
        out,
        scan=scan,
        sample=sample,
        numeric_summary=numeric_summary,
        eligible_numeric_summary=eligible_numeric_summary,
        categorical_counts=categorical_counts,
        eligible_categorical_counts=eligible_categorical_counts,
        daily_counts=daily_counts,
        guidance=guidance,
        deep_payload=deep_payload,
        csv_path=csv,
        start_date=start_date,
        end_date=end_date,
        max_input_rows=max_input_rows,
        sample_modulus=sample_modulus,
    )
    return {
        "schema_version": EDA_SCHEMA_VERSION,
        "out_dir": str(out),
        "artifact_paths": paths,
        "summary": guidance["summary"],
        "prompt_rules": guidance["prompt_rules"],
    }


def build_data_guidance(
    *,
    scan_summary: dict[str, Any],
    numeric_summary: pd.DataFrame,
    daily_counts: pd.DataFrame,
    deep_summary: dict[str, Any],
) -> dict[str, Any]:
    """Convert EDA tables into prompt-facing data rules."""

    rules: list[str] = []
    caveats: list[str] = []
    feature_primitives: list[dict[str, str]] = []

    _add_size_and_coverage_rules(rules, caveats, scan_summary, daily_counts)
    _add_numeric_transform_rules(rules, caveats, feature_primitives, numeric_summary)
    _add_deep_window_rules(rules, caveats, feature_primitives, deep_summary)

    return {
        "schema_version": EDA_SCHEMA_VERSION,
        "summary": {
            "rows_scanned": scan_summary.get("rows_scanned_after_date_filter"),
            "eligible_rows": scan_summary.get("eligibility_steps", {}).get("eligible_static_return"),
            "unique_permnos": scan_summary.get("unique_permnos"),
            "unique_eligible_permnos": scan_summary.get("unique_eligible_permnos"),
            "deep_window": deep_summary,
        },
        "prompt_rules": rules,
        "caveats": caveats,
        "feature_primitives": feature_primitives,
    }


def _scan_csv(
    csv: Path,
    *,
    usecols: list[str],
    chunksize: int,
    start_date: str | None,
    end_date: str | None,
    max_input_rows: int | None,
    sample_modulus: int,
    max_sample_rows: int,
    contract: DailyStockContract,
) -> ScanState:
    state = ScanState(contract=contract)
    start = pd.Timestamp(start_date) if start_date else None
    end = pd.Timestamp(end_date) if end_date else None
    scanned = 0
    kept_sample_rows = 0

    for raw in pd.read_csv(csv, usecols=usecols, chunksize=chunksize, low_memory=False):
        if max_input_rows is not None:
            remaining = max_input_rows - scanned
            if remaining <= 0:
                break
            raw = raw.head(remaining)
        raw_len = len(raw)
        positions = np.arange(scanned, scanned + raw_len)
        scanned += raw_len
        state.row_count += raw_len

        chunk = coerce_daily_stock_frame(raw, contract)
        chunk_positions = pd.Series(positions, index=chunk.index)
        if start is not None:
            keep = chunk[contract.date] >= start
            chunk = chunk.loc[keep]
            chunk_positions = chunk_positions.loc[keep]
        if end is not None:
            keep = chunk[contract.date] <= end
            chunk = chunk.loc[keep]
            chunk_positions = chunk_positions.loc[keep]
        if chunk.empty:
            if max_input_rows is not None and scanned >= max_input_rows:
                break
            continue

        state.date_filtered_row_count += int(len(chunk))
        chunk = _with_derived_columns(chunk, contract)
        eligible = static_eligibility_mask(chunk, contract, require_return=True)
        chunk["eligible_static_return"] = eligible
        _update_state(state, chunk, eligible)

        if sample_modulus > 0 and kept_sample_rows < max_sample_rows:
            selected = (chunk_positions % sample_modulus) == 0
            sampled = chunk.loc[selected].copy()
            if not sampled.empty:
                remaining_sample = max_sample_rows - kept_sample_rows
                sampled = sampled.head(remaining_sample)
                state.sample_frames.append(sampled)
                kept_sample_rows += int(len(sampled))

        if max_input_rows is not None and scanned >= max_input_rows:
            break
    return state


def _update_state(state: ScanState, chunk: pd.DataFrame, eligible: pd.Series) -> None:
    contract = state.contract
    _update_unique_permnos(state.unique_permnos, chunk[contract.security_id])
    _update_unique_permnos(state.unique_eligible_permnos, chunk.loc[eligible, contract.security_id])
    _update_daily_counts(state.daily_row_counts, chunk[contract.date])
    _update_daily_counts(state.daily_eligible_counts, chunk.loc[eligible, contract.date])
    _update_eligibility_steps(state.eligibility_steps, chunk, contract)

    for column in PROFILE_NUMERIC_COLUMNS:
        if column not in chunk.columns:
            continue
        state.numeric_stats.setdefault(column, NumericAccumulator(column)).update(chunk[column])
        state.eligible_numeric_stats.setdefault(column, NumericAccumulator(column)).update(chunk.loc[eligible, column])
    for column in PROFILE_CATEGORICAL_COLUMNS:
        if column not in chunk.columns:
            continue
        state.categorical_counts.setdefault(column, Counter()).update(_clean_categories(chunk[column]))
        state.eligible_categorical_counts.setdefault(column, Counter()).update(_clean_categories(chunk.loc[eligible, column]))


def _build_deep_window_profile(
    *,
    csv_path: Path,
    out_dir: Path,
    start_date: str | None,
    end_date: str | None,
    chunksize: int,
    max_input_rows: int | None,
    top_n: int,
) -> dict[str, Any]:
    if not start_date or not end_date:
        return {
            "enabled": False,
            "reason": "deep_start_date and deep_end_date are required for top-N cross-sectional profiling",
        }

    columns = _read_header(csv_path)
    optional_columns = [
        col for col in OPTIONAL_PROFILE_COLUMNS if col in columns and col not in CONTRACT.required_columns
    ]
    panel, load_diag = load_daily_stock_window(
        csv_path,
        chunksize=chunksize,
        start_date=start_date,
        end_date=end_date,
        max_input_rows=max_input_rows,
        extra_columns=optional_columns,
    )
    deduped, duplicate_diag = apply_duplicate_policy(panel)
    universe_base, eligibility_diag = apply_static_eligibility(deduped, require_return=False)
    membership, universe_summary = build_monthly_rolling_universe(universe_base, top_n=top_n)
    universe_panel = apply_monthly_universe(universe_base, membership)
    tradable = universe_panel.loc[static_eligibility_mask(universe_panel, require_return=True)].copy()
    tradable = _with_derived_columns(tradable, CONTRACT)

    deep_dir = out_dir / "deep_window"
    deep_dir.mkdir(parents=True, exist_ok=True)
    universe_summary.to_csv(deep_dir / "universe_summary.csv", index=False)
    membership.head(50_000).to_csv(deep_dir / "universe_membership_head.csv", index=False)
    daily_profile = _deep_daily_profile(tradable)
    industry_profile = _industry_coverage_profile(tradable)
    transform_profile = _deep_transform_profile(tradable)
    daily_profile.to_csv(deep_dir / "daily_cross_section_profile.csv", index=False)
    industry_profile.to_csv(deep_dir / "industry_coverage_profile.csv", index=False)
    transform_profile.to_csv(deep_dir / "transform_profile.csv", index=False)

    summary = {
        "enabled": True,
        "start_date": start_date,
        "end_date": end_date,
        "top_n": top_n,
        "rows_loaded_after_date_filter": load_diag.get("rows_loaded_after_date_filter"),
        "rows_after_duplicate_policy": duplicate_diag.get("rows_after_duplicate_policy"),
        "rows_after_static_eligibility_no_return_required": eligibility_diag.get("rows_after_static_eligibility"),
        "monthly_universe_rows": int(len(membership)),
        "universe_panel_rows": int(len(universe_panel)),
        "tradable_universe_rows": int(len(tradable)),
        "tradable_dates": int(tradable[CONTRACT.date].nunique()) if not tradable.empty else 0,
        "tradable_permnos": int(tradable[CONTRACT.security_id].nunique()) if not tradable.empty else 0,
        "median_daily_tradable_count": _safe_float(daily_profile["row_count"].median()) if not daily_profile.empty else None,
        "median_daily_industry_groups": (
            _safe_float(industry_profile["industry_group_count"].median()) if not industry_profile.empty else None
        ),
        "median_daily_groups_ge_10": (
            _safe_float(industry_profile["groups_ge_10"].median()) if not industry_profile.empty else None
        ),
        "paths": {
            "universe_summary": str(deep_dir / "universe_summary.csv"),
            "universe_membership_head": str(deep_dir / "universe_membership_head.csv"),
            "daily_cross_section_profile": str(deep_dir / "daily_cross_section_profile.csv"),
            "industry_coverage_profile": str(deep_dir / "industry_coverage_profile.csv"),
            "transform_profile": str(deep_dir / "transform_profile.csv"),
        },
    }
    write_json(deep_dir / "deep_window_summary.json", summary)
    return {"enabled": True, "summary": summary}


def _write_profile_artifacts(
    out: Path,
    *,
    scan: ScanState,
    sample: pd.DataFrame,
    numeric_summary: pd.DataFrame,
    eligible_numeric_summary: pd.DataFrame,
    categorical_counts: pd.DataFrame,
    eligible_categorical_counts: pd.DataFrame,
    daily_counts: pd.DataFrame,
    guidance: dict[str, Any],
    deep_payload: dict[str, Any],
    csv_path: Path,
    start_date: str | None,
    end_date: str | None,
    max_input_rows: int | None,
    sample_modulus: int,
) -> dict[str, str]:
    summary = _scan_summary(scan, csv_path, start_date, end_date, max_input_rows, sample_modulus)
    payload = {
        "schema_version": EDA_SCHEMA_VERSION,
        "summary": summary,
        "guidance": guidance,
        "deep_window": deep_payload,
    }
    paths = {
        "summary_json": str(write_json(out / "daily_stock_eda_summary.json", payload)),
        "guidance_json": str(write_json(out / "daily_stock_prompt_guidance.json", guidance)),
    }
    sample_quantiles = _sample_quantiles_frame(sample, PROFILE_NUMERIC_COLUMNS)
    eligible_sample = sample.loc[sample["eligible_static_return"]].copy() if "eligible_static_return" in sample else sample.iloc[0:0]
    eligible_sample_quantiles = _sample_quantiles_frame(eligible_sample, PROFILE_NUMERIC_COLUMNS)
    numeric_summary.to_csv(out / "numeric_summary.csv", index=False)
    eligible_numeric_summary.to_csv(out / "eligible_numeric_summary.csv", index=False)
    sample_quantiles.to_csv(out / "sample_quantiles.csv", index=False)
    eligible_sample_quantiles.to_csv(out / "eligible_sample_quantiles.csv", index=False)
    categorical_counts.to_csv(out / "categorical_counts.csv", index=False)
    eligible_categorical_counts.to_csv(out / "eligible_categorical_counts.csv", index=False)
    daily_counts.to_csv(out / "daily_counts.csv", index=False)
    sample.head(50_000).to_csv(out / "deterministic_sample_head.csv", index=False)
    _write_markdown_summary(out / "daily_stock_eda_summary.md", payload)
    _write_prompt_data_cards(out / "prompt_data_cards.md", guidance)
    paths.update(
        {
            "summary_markdown": str(out / "daily_stock_eda_summary.md"),
            "prompt_data_cards": str(out / "prompt_data_cards.md"),
            "numeric_summary": str(out / "numeric_summary.csv"),
            "eligible_numeric_summary": str(out / "eligible_numeric_summary.csv"),
            "sample_quantiles": str(out / "sample_quantiles.csv"),
            "eligible_sample_quantiles": str(out / "eligible_sample_quantiles.csv"),
            "categorical_counts": str(out / "categorical_counts.csv"),
            "eligible_categorical_counts": str(out / "eligible_categorical_counts.csv"),
            "daily_counts": str(out / "daily_counts.csv"),
            "deterministic_sample_head": str(out / "deterministic_sample_head.csv"),
        }
    )
    return paths


def _write_markdown_summary(path: Path, payload: dict[str, Any]) -> None:
    guidance = payload["guidance"]
    summary = payload["summary"]
    lines = [
        "# daily_stock EDA Summary",
        "",
        f"- schema_version: `{payload.get('schema_version')}`",
        f"- rows_scanned_after_date_filter: `{summary.get('rows_scanned_after_date_filter')}`",
        f"- unique_permnos: `{summary.get('unique_permnos')}`",
        f"- unique_eligible_permnos: `{summary.get('unique_eligible_permnos')}`",
        f"- date_min: `{summary.get('date_min')}`",
        f"- date_max: `{summary.get('date_max')}`",
        "",
        "## Eligibility Steps",
        "",
    ]
    for key, value in (summary.get("eligibility_steps") or {}).items():
        lines.append(f"- {key}: `{value}`")
    lines.extend(["", "## Prompt Rules", ""])
    for item in guidance.get("prompt_rules", []) or ["none"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Caveats", ""])
    for item in guidance.get("caveats", []) or ["none"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Feature Primitives", ""])
    for item in guidance.get("feature_primitives", []) or []:
        lines.append(f"- `{item.get('name')}`: {item.get('rule')}")
    if not guidance.get("feature_primitives"):
        lines.append("- none")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_prompt_data_cards(path: Path, guidance: dict[str, Any]) -> None:
    summary = guidance.get("summary", {})
    lines = [
        "# daily_stock Prompt Data Cards",
        "",
        "These cards are data-understanding inputs for Phase 4 prompts. They are not alpha evidence.",
        "",
        "## Scan Card",
        "",
        f"- rows_scanned: `{summary.get('rows_scanned')}`",
        f"- eligible_rows: `{summary.get('eligible_rows')}`",
        f"- unique_permnos: `{summary.get('unique_permnos')}`",
        f"- unique_eligible_permnos: `{summary.get('unique_eligible_permnos')}`",
        "",
        "## Rules For Child Programs",
        "",
    ]
    for rule in guidance.get("prompt_rules", []) or ["No prompt rules were generated."]:
        lines.append(f"- {rule}")
    lines.extend(["", "## Caveats", ""])
    for caveat in guidance.get("caveats", []) or ["No caveats were generated."]:
        lines.append(f"- {caveat}")
    lines.extend(["", "## Feature Primitives", ""])
    for primitive in guidance.get("feature_primitives", []) or []:
        lines.append(f"- `{primitive.get('name')}`: {primitive.get('rule')}")
    if not guidance.get("feature_primitives"):
        lines.append("- No feature primitives were generated.")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _scan_summary(
    scan: ScanState,
    csv_path: Path,
    start_date: str | None,
    end_date: str | None,
    max_input_rows: int | None,
    sample_modulus: int,
) -> dict[str, Any]:
    dates = sorted(scan.daily_row_counts)
    return {
        "schema_version": EDA_SCHEMA_VERSION,
        "csv_path": str(csv_path),
        "rows_scanned_raw_before_date_filter": scan.row_count,
        "rows_scanned_after_date_filter": scan.date_filtered_row_count,
        "start_date": start_date,
        "end_date": end_date,
        "max_input_rows": max_input_rows,
        "sample_modulus": sample_modulus,
        "deterministic_sample_rows": int(sum(len(frame) for frame in scan.sample_frames)),
        "date_min": dates[0] if dates else None,
        "date_max": dates[-1] if dates else None,
        "trading_date_count": len(dates),
        "unique_permnos": len(scan.unique_permnos),
        "unique_eligible_permnos": len(scan.unique_eligible_permnos),
        "eligibility_steps": dict(scan.eligibility_steps),
    }


def _with_derived_columns(frame: pd.DataFrame, contract: DailyStockContract) -> pd.DataFrame:
    out = frame.copy()
    out["abs_price"] = out[contract.price].abs()
    out["excess_return_vs_vwretd"] = out[contract.ex_dividend_return] - out[contract.benchmark_return_primary]
    out["log_abs_price"] = np.log1p(out["abs_price"].clip(lower=0.0))
    out["log_volume"] = np.log1p(out[contract.volume].clip(lower=0.0))
    out["log_dollar_volume"] = np.log1p(out[contract.dollar_volume].clip(lower=0.0))
    out["log_market_cap"] = np.log1p(out[contract.market_cap].clip(lower=0.0))
    return out


def _update_eligibility_steps(counter: Counter[str], frame: pd.DataFrame, contract: DailyStockContract) -> None:
    mask = pd.Series(True, index=frame.index)
    counter["rows"] += int(len(frame))
    mask &= frame[contract.date].notna() & frame[contract.security_id].notna()
    counter["valid_date_security"] += int(mask.sum())
    mask &= frame[contract.us_incorporated].eq("Y")
    counter["us_incorporated"] += int(mask.sum())
    mask &= frame[contract.security_type].eq("EQTY") & frame[contract.share_type].eq("NS")
    counter["common_equity_common_share"] += int(mask.sum())
    mask &= frame[contract.trading_status].eq("A") & frame[contract.conditional_type].eq("RW")
    counter["active_regular_way"] += int(mask.sum())
    mask &= frame[contract.exchange].isin({"A", "N", "Q"})
    counter["major_exchange"] += int(mask.sum())
    mask &= frame[contract.price].abs().gt(0.0)
    counter["positive_abs_price"] += int(mask.sum())
    mask &= frame[contract.market_cap].gt(0.0)
    counter["positive_market_cap"] += int(mask.sum())
    mask &= frame[contract.volume].gt(0.0)
    counter["positive_volume"] += int(mask.sum())
    mask &= frame[contract.ex_dividend_return].notna()
    counter["eligible_static_return"] += int(mask.sum())


def _numeric_summary_frame(
    stats: dict[str, NumericAccumulator],
    sample: pd.DataFrame,
    columns: Iterable[str],
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    quantiles = [0.001, 0.01, 0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99, 0.999]
    for column in columns:
        if column not in stats:
            continue
        row = stats[column].to_record()
        if column in sample.columns and not sample.empty:
            values = pd.to_numeric(sample[column], errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
            for quantile in quantiles:
                row[f"sample_q{quantile:g}"] = _safe_float(values.quantile(quantile)) if len(values) else None
        rows.append(row)
    return pd.DataFrame(rows)


def _sample_quantiles_frame(sample: pd.DataFrame, columns: Iterable[str]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    quantiles = [0.001, 0.01, 0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99, 0.999]
    for column in columns:
        if column not in sample.columns or sample.empty:
            continue
        values = pd.to_numeric(sample[column], errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
        if values.empty:
            continue
        row: dict[str, Any] = {"column": column, "sample_count": int(len(values))}
        for quantile in quantiles:
            row[f"q{quantile:g}"] = _safe_float(values.quantile(quantile))
        rows.append(row)
    return pd.DataFrame(rows)


def _counter_frame(counters: dict[str, Counter[str]], count_name: str) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for column, counter in sorted(counters.items()):
        for value, count in counter.most_common(200):
            rows.append({"column": column, "value": value, count_name: int(count)})
    return pd.DataFrame(rows)


def _daily_counts_frame(raw_counts: Counter[str], eligible_counts: Counter[str]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for date in sorted(set(raw_counts) | set(eligible_counts)):
        raw = int(raw_counts.get(date, 0))
        eligible = int(eligible_counts.get(date, 0))
        rows.append(
            {
                "date": date,
                "row_count": raw,
                "eligible_static_return_count": eligible,
                "eligible_static_return_rate": eligible / raw if raw else None,
            }
        )
    return pd.DataFrame(rows)


def _deep_daily_profile(frame: pd.DataFrame) -> pd.DataFrame:
    if frame.empty:
        return pd.DataFrame(columns=["date", "row_count"])
    rows = []
    for date, group in frame.groupby(CONTRACT.date, sort=True):
        rows.append(
            {
                "date": pd.Timestamp(date).date().isoformat(),
                "row_count": int(len(group)),
                "permno_count": int(group[CONTRACT.security_id].nunique()),
                "median_abs_price": _safe_float(group["abs_price"].median()),
                "median_log_dollar_volume": _safe_float(group["log_dollar_volume"].median()),
                "median_log_market_cap": _safe_float(group["log_market_cap"].median()),
                "return_q01": _safe_float(group[CONTRACT.ex_dividend_return].quantile(0.01)),
                "return_q99": _safe_float(group[CONTRACT.ex_dividend_return].quantile(0.99)),
                "missing_return_rate": _safe_float(group[CONTRACT.ex_dividend_return].isna().mean()),
                "zero_volume_rate": _safe_float(group[CONTRACT.volume].le(0.0).mean()),
            }
        )
    return pd.DataFrame(rows)


def _industry_coverage_profile(frame: pd.DataFrame) -> pd.DataFrame:
    if frame.empty:
        return pd.DataFrame(columns=["date", "industry_group_count"])
    data = frame[[CONTRACT.date, CONTRACT.industry_primary, CONTRACT.security_id]].copy()
    data["sic2"] = (pd.to_numeric(data[CONTRACT.industry_primary], errors="coerce") // 100).astype("Int64")
    rows = []
    for date, group in data.groupby(CONTRACT.date, sort=True):
        counts = group.dropna(subset=["sic2"]).groupby("sic2")[CONTRACT.security_id].nunique()
        total = int(group[CONTRACT.security_id].nunique())
        largest_share = float(counts.max() / total) if total and len(counts) else None
        rows.append(
            {
                "date": pd.Timestamp(date).date().isoformat(),
                "name_count": total,
                "industry_group_count": int(len(counts)),
                "groups_ge_3": int(counts.ge(3).sum()),
                "groups_ge_5": int(counts.ge(5).sum()),
                "groups_ge_10": int(counts.ge(10).sum()),
                "median_names_per_group": _safe_float(counts.median()) if len(counts) else None,
                "largest_group_share": largest_share,
                "missing_industry_rate": _safe_float(group["sic2"].isna().mean()),
            }
        )
    return pd.DataFrame(rows)


def _deep_transform_profile(frame: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for column in ["abs_price", "DlyVol", "DlyPrcVol", "DlyCap", "DlyRetx", "excess_return_vs_vwretd"]:
        if column not in frame.columns:
            continue
        values = pd.to_numeric(frame[column], errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
        if values.empty:
            continue
        row = {"column": column, "count": int(len(values))}
        for q in [0.001, 0.01, 0.05, 0.25, 0.50, 0.75, 0.95, 0.99, 0.999]:
            row[f"q{q:g}"] = _safe_float(values.quantile(q))
        row["mean"] = _safe_float(values.mean())
        row["std"] = _safe_float(values.std(ddof=0))
        rows.append(row)
    return pd.DataFrame(rows)


def _add_size_and_coverage_rules(
    rules: list[str],
    caveats: list[str],
    scan_summary: dict[str, Any],
    daily_counts: pd.DataFrame,
) -> None:
    if scan_summary.get("rows_scanned_after_date_filter"):
        rules.append("Never infer cross-sectional behavior from first-N rows; the source CSV can be security-sorted.")
    if not daily_counts.empty:
        median_count = daily_counts["eligible_static_return_count"].median()
        rules.append(
            f"Use date-window or rolling-universe loaders for child evaluation; median eligible static rows per date in this scan is about {median_count:.0f}."
        )
    if scan_summary.get("max_input_rows"):
        caveats.append("This EDA used max_input_rows and is a smoke profile, not a full empirical map.")


def _add_numeric_transform_rules(
    rules: list[str],
    caveats: list[str],
    primitives: list[dict[str, str]],
    numeric_summary: pd.DataFrame,
) -> None:
    by_col = {str(row["column"]): row for _, row in numeric_summary.iterrows()}
    for field, name in [
        ("DlyPrcVol", "log_or_rank_dollar_volume"),
        ("DlyCap", "log_or_rank_market_cap"),
        ("DlyVol", "log_or_rank_volume"),
    ]:
        row = by_col.get(field)
        if row is None:
            continue
        q50 = _safe_float(row.get("sample_q0.5"))
        q99 = _safe_float(row.get("sample_q0.99"))
        if q50 and q99 and q99 / max(q50, 1e-12) > 20.0:
            rules.append(f"Use log, percentile rank, or winsorized z-score for {field}; raw scale is highly skewed.")
            primitives.append(
                {
                    "name": name,
                    "rule": f"Compute date-level rank or log1p transform of {field}, then use bounded weights.",
                }
            )
    ret = by_col.get("DlyRetx")
    if ret is not None:
        q001 = _safe_float(ret.get("sample_q0.001"))
        q999 = _safe_float(ret.get("sample_q0.999"))
        if q001 is not None and q999 is not None and (q001 < -0.5 or q999 > 0.5):
            rules.append("Use robust date-level winsorization or rank transforms for returns/signals before z-scoring.")
            primitives.append(
                {
                    "name": "date_level_winsorized_return_signal",
                    "rule": "Winsorize or rank signal inputs within date before cross-sectional z-scoring.",
                }
            )
    price = by_col.get("abs_price")
    if price is not None and (_safe_float(price.get("sample_q0.05")) or 0.0) < 5.0:
        caveats.append("Low-price names appear in the eligible sample; price and liquidity filters may affect turnover and missing-return risk.")


def _add_deep_window_rules(
    rules: list[str],
    caveats: list[str],
    primitives: list[dict[str, str]],
    deep_summary: dict[str, Any],
) -> None:
    if not deep_summary.get("enabled"):
        caveats.append("No deep top-N date-window profile was run; industry and transform rules are provisional.")
        return
    median_groups_ge_10 = deep_summary.get("median_daily_groups_ge_10")
    if median_groups_ge_10 is not None and float(median_groups_ge_10) > 0:
        rules.append(
            "Industry-neutral ranking is allowed only with a per-date group-size fallback; inspect SIC2 group counts before forcing neutrality."
        )
        primitives.append(
            {
                "name": "sic2_group_rank_with_min_count",
                "rule": "Rank or z-score within SIC2 only when the date-group has enough names; otherwise use date-level fallback.",
            }
        )
    if deep_summary.get("median_daily_tradable_count"):
        rules.append(
            "Controller children should preserve broad daily activity; sparse few-day books are coverage artifacts, not alpha."
        )


def _sample_frame(scan: ScanState) -> pd.DataFrame:
    if not scan.sample_frames:
        return pd.DataFrame()
    return pd.concat(scan.sample_frames, ignore_index=True)


def _profile_usecols(columns: list[str], contract: DailyStockContract) -> list[str]:
    available = set(columns)
    optional = [col for col in OPTIONAL_PROFILE_COLUMNS if col in available]
    return unique_preserving_order([*contract.required_columns, *optional])


def _read_header(csv: Path) -> list[str]:
    return [str(col) for col in pd.read_csv(csv, nrows=0).columns]


def _update_unique_permnos(target: set[int], values: pd.Series) -> None:
    for value in values.dropna().astype("Int64").tolist():
        if pd.notna(value):
            target.add(int(value))


def _update_daily_counts(counter: Counter[str], dates: pd.Series) -> None:
    cleaned = pd.to_datetime(dates, errors="coerce").dropna().dt.date.astype(str)
    counter.update(cleaned.tolist())


def _clean_categories(series: pd.Series) -> list[str]:
    return series.fillna("<NA>").astype(str).replace("", "<EMPTY>").tolist()


def _safe_float(value: Any) -> float | None:
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    return result if np.isfinite(result) else None


__all__ = [
    "EDA_SCHEMA_VERSION",
    "build_data_guidance",
    "profile_daily_stock_data",
]
