"""Chunked daily_stock loading and fixed eligibility filters."""

from __future__ import annotations

from pathlib import Path
from typing import Iterator

import pandas as pd

from .daily_stock_contract import (
    ACTIVE_TRADING_STATUS,
    COMMON_EQUITY_SECURITY_TYPE,
    COMMON_SHARE_TYPE,
    CONTRACT,
    MAJOR_US_EXCHANGES,
    REGULAR_WAY_CONDITIONAL_TYPE,
    US_INCORPORATED_FLAG,
    DailyStockContract,
    unique_preserving_order,
    validate_columns,
)


def coerce_daily_stock_frame(
    frame: pd.DataFrame,
    contract: DailyStockContract = CONTRACT,
) -> pd.DataFrame:
    """Apply contract dtypes with explicit date/numeric coercion."""

    validate_columns(frame.columns, contract)
    df = frame.copy()
    df[contract.date] = pd.to_datetime(df[contract.date], errors="coerce")
    for col in contract.numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df[contract.security_id] = pd.to_numeric(df[contract.security_id], errors="coerce").astype("Int64")
    df[contract.issuer_id] = pd.to_numeric(df[contract.issuer_id], errors="coerce").astype("Int64")
    return df


def static_eligibility_mask(
    frame: pd.DataFrame,
    contract: DailyStockContract = CONTRACT,
    *,
    require_return: bool = True,
    require_positive_volume: bool = True,
) -> pd.Series:
    """Fixed non-evolvable daily_stock universe/tradability filter."""

    mask = (
        frame[contract.us_incorporated].eq(US_INCORPORATED_FLAG)
        & frame[contract.security_type].eq(COMMON_EQUITY_SECURITY_TYPE)
        & frame[contract.share_type].eq(COMMON_SHARE_TYPE)
        & frame[contract.trading_status].eq(ACTIVE_TRADING_STATUS)
        & frame[contract.conditional_type].eq(REGULAR_WAY_CONDITIONAL_TYPE)
        & frame[contract.exchange].isin(MAJOR_US_EXCHANGES)
        & frame[contract.date].notna()
        & frame[contract.security_id].notna()
        & frame[contract.price].abs().gt(0.0)
        & frame[contract.market_cap].gt(0.0)
    )
    if require_positive_volume:
        mask &= frame[contract.volume].gt(0.0)
    if require_return:
        mask &= frame[contract.ex_dividend_return].notna()
    return mask.fillna(False)


def iter_daily_stock_chunks(
    csv_path: str | Path,
    *,
    contract: DailyStockContract = CONTRACT,
    chunksize: int = 1_000_000,
    start_date: str | None = None,
    end_date: str | None = None,
    max_input_rows: int | None = None,
    extra_columns: list[str] | None = None,
) -> Iterator[pd.DataFrame]:
    """Yield coerced chunks, optionally filtered to a date window.

    `max_input_rows` caps raw rows scanned and is intended only for smoke
    checks. Leave it unset for date-window sample evaluation so a stock-sorted
    CSV can still produce cross-sectional coverage.
    """

    csv = Path(csv_path)
    usecols = unique_preserving_order([*contract.required_columns, *(extra_columns or [])])
    start = pd.Timestamp(start_date) if start_date else None
    end = pd.Timestamp(end_date) if end_date else None
    scanned = 0

    for raw in pd.read_csv(csv, usecols=usecols, chunksize=chunksize, low_memory=False):
        if max_input_rows is not None:
            remaining = max_input_rows - scanned
            if remaining <= 0:
                break
            raw = raw.head(remaining)
        scanned += len(raw)
        chunk = coerce_daily_stock_frame(raw, contract)
        if start is not None:
            chunk = chunk.loc[chunk[contract.date] >= start]
        if end is not None:
            chunk = chunk.loc[chunk[contract.date] <= end]
        if not chunk.empty:
            yield chunk
        if max_input_rows is not None and scanned >= max_input_rows:
            break


def load_daily_stock_window(
    csv_path: str | Path,
    *,
    contract: DailyStockContract = CONTRACT,
    chunksize: int = 1_000_000,
    start_date: str | None = None,
    end_date: str | None = None,
    max_input_rows: int | None = None,
    extra_columns: list[str] | None = None,
) -> tuple[pd.DataFrame, dict[str, object]]:
    """Load a remote sample window without requiring the full CSV in memory."""

    frames: list[pd.DataFrame] = []
    raw_chunks = 0
    rows_loaded = 0
    for chunk in iter_daily_stock_chunks(
        csv_path,
        contract=contract,
        chunksize=chunksize,
        start_date=start_date,
        end_date=end_date,
        max_input_rows=max_input_rows,
        extra_columns=extra_columns,
    ):
        raw_chunks += 1
        rows_loaded += len(chunk)
        frames.append(chunk)
    if frames:
        panel = pd.concat(frames, ignore_index=True)
    else:
        panel = pd.DataFrame(columns=contract.required_columns)
    diagnostics = {
        "csv_path": str(csv_path),
        "chunks_with_rows": raw_chunks,
        "rows_loaded_after_date_filter": int(rows_loaded),
        "start_date": start_date,
        "end_date": end_date,
        "max_input_rows": max_input_rows,
    }
    return panel, diagnostics


def apply_duplicate_policy(
    frame: pd.DataFrame,
    contract: DailyStockContract = CONTRACT,
) -> tuple[pd.DataFrame, dict[str, object]]:
    """Keep first security-date row after sorting and report duplicates."""

    if frame.empty:
        return frame.copy(), {"duplicate_permno_date_count": 0, "rows_after_duplicate_policy": 0}
    ordered = frame.sort_values([contract.security_id, contract.date]).copy()
    duplicate_count = int(ordered.duplicated([contract.security_id, contract.date]).sum())
    if duplicate_count:
        ordered = ordered.drop_duplicates([contract.security_id, contract.date], keep="first")
    return ordered.reset_index(drop=True), {
        "duplicate_permno_date_count": duplicate_count,
        "rows_after_duplicate_policy": int(len(ordered)),
    }


def apply_static_eligibility(
    frame: pd.DataFrame,
    contract: DailyStockContract = CONTRACT,
    *,
    require_return: bool = True,
) -> tuple[pd.DataFrame, dict[str, object]]:
    """Apply the frozen contract filters and return compact diagnostics."""

    if frame.empty:
        return frame.copy(), {"rows_before_static_eligibility": 0, "rows_after_static_eligibility": 0}
    mask = static_eligibility_mask(frame, contract, require_return=require_return)
    filtered = frame.loc[mask].copy()
    return filtered.reset_index(drop=True), {
        "rows_before_static_eligibility": int(len(frame)),
        "rows_after_static_eligibility": int(len(filtered)),
        "dropped_by_static_eligibility": int(len(frame) - len(filtered)),
        "missing_ex_dividend_return_rate": float(frame[contract.ex_dividend_return].isna().mean()),
        "nonpositive_price_count": int(frame[contract.price].abs().le(0.0).fillna(True).sum()),
        "nonpositive_market_cap_count": int(frame[contract.market_cap].le(0.0).fillna(True).sum()),
        "nonpositive_volume_count": int(frame[contract.volume].le(0.0).fillna(True).sum()),
    }
