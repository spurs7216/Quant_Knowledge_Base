"""Rolling top-N coverage and forward-return availability diagnostics.

This module complements `daily_stock_eda.py`. The EDA profiler describes the
dataset distribution; this module describes whether the rolling top-N universe
has enough observed next-day returns for sample evaluation.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from .artifact_io import write_json
from .daily_stock_contract import CONTRACT, DailyStockContract, unique_preserving_order, validate_columns
from .daily_stock_loader import coerce_daily_stock_frame, static_eligibility_mask
from .sample_eval_metrics import build_forward_returns


FORWARD_COVERAGE_SCHEMA_VERSION = "daily_stock_forward_coverage_v1"

OPTIONAL_CAUSE_COLUMNS = (
    "Ticker",
    "DlyRetMissFlg",
    "DlyPrcFlg",
    "DlyCapFlg",
    "DlyVolFlg",
)


@dataclass(frozen=True)
class MonthFormation:
    month: str
    formation_date: pd.Timestamp
    selected_count: int


def profile_daily_stock_forward_coverage(
    *,
    csv_path: str | Path,
    out_dir: str | Path,
    chunksize: int = 1_000_000,
    top_n: int = 500,
    coverage_start_date: str | None = None,
    coverage_end_date: str | None = None,
    forward_start_date: str = "2018-01-01",
    forward_end_date: str = "2020-12-31",
    max_input_rows: int | None = None,
) -> dict[str, Any]:
    """Write rolling top-N coverage and forward-return availability artifacts."""

    if top_n <= 0:
        raise ValueError("top_n must be positive")
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    csv = Path(csv_path)
    columns = _read_header(csv)
    validate_columns(columns, CONTRACT)
    usecols = _coverage_usecols(columns, CONTRACT)

    calendar = _scan_calendar(
        csv,
        usecols=usecols,
        chunksize=chunksize,
        start_date=coverage_start_date,
        end_date=coverage_end_date,
        max_input_rows=max_input_rows,
        contract=CONTRACT,
    )
    trading_dates = pd.Index(pd.to_datetime(sorted(calendar["trading_dates"])))
    formations = _month_formations(trading_dates)
    formation_dates = sorted({formation.formation_date for formation in formations.values()})
    formation_frame = _load_formation_rows(
        csv,
        usecols=usecols,
        chunksize=chunksize,
        formation_dates=formation_dates,
        max_input_rows=max_input_rows,
        contract=CONTRACT,
    )
    membership = _build_membership(formation_frame, formations, top_n=top_n, contract=CONTRACT)
    if membership.empty:
        raise RuntimeError("rolling top-N membership is empty")

    top_panel = _load_topn_panel(
        csv,
        usecols=usecols,
        chunksize=chunksize,
        membership=membership,
        start_date=coverage_start_date,
        end_date=coverage_end_date,
        max_input_rows=max_input_rows,
        contract=CONTRACT,
    )
    if top_panel.empty:
        raise RuntimeError("rolling top-N panel is empty")

    daily_coverage = _daily_coverage(top_panel, membership, trading_dates, CONTRACT)
    monthly_coverage = _monthly_coverage(daily_coverage)
    permno_coverage = _permno_coverage(top_panel, membership, daily_coverage, CONTRACT)
    churn = _membership_churn(membership, CONTRACT)
    forward_payload = _forward_availability_profile(
        top_panel,
        membership,
        start_date=forward_start_date,
        end_date=forward_end_date,
        contract=CONTRACT,
    )

    paths = _write_forward_coverage_artifacts(
        out,
        membership=membership,
        daily_coverage=daily_coverage,
        monthly_coverage=monthly_coverage,
        permno_coverage=permno_coverage,
        churn=churn,
        forward_payload=forward_payload,
        calendar=calendar,
        csv_path=csv,
        top_n=top_n,
        coverage_start_date=coverage_start_date,
        coverage_end_date=coverage_end_date,
        forward_start_date=forward_start_date,
        forward_end_date=forward_end_date,
        max_input_rows=max_input_rows,
    )
    return {
        "schema_version": FORWARD_COVERAGE_SCHEMA_VERSION,
        "out_dir": str(out),
        "artifact_paths": paths,
        "summary": _summary_payload(
            calendar=calendar,
            membership=membership,
            daily_coverage=daily_coverage,
            monthly_coverage=monthly_coverage,
            permno_coverage=permno_coverage,
            churn=churn,
            forward_payload=forward_payload,
            top_n=top_n,
            coverage_start_date=coverage_start_date,
            coverage_end_date=coverage_end_date,
            forward_start_date=forward_start_date,
            forward_end_date=forward_end_date,
            max_input_rows=max_input_rows,
            csv_path=csv,
        ),
    }


def _scan_calendar(
    csv: Path,
    *,
    usecols: list[str],
    chunksize: int,
    start_date: str | None,
    end_date: str | None,
    max_input_rows: int | None,
    contract: DailyStockContract,
) -> dict[str, Any]:
    start = pd.Timestamp(start_date) if start_date else None
    end = pd.Timestamp(end_date) if end_date else None
    scanned = 0
    rows_after_date_filter = 0
    raw_trading_dates: set[pd.Timestamp] = set()
    eligible_trading_dates: set[pd.Timestamp] = set()
    raw_daily_counts: dict[str, int] = {}
    eligible_daily_counts: dict[str, int] = {}

    for raw in pd.read_csv(csv, usecols=usecols, chunksize=chunksize, low_memory=False):
        if max_input_rows is not None:
            remaining = max_input_rows - scanned
            if remaining <= 0:
                break
            raw = raw.head(remaining)
        scanned += len(raw)
        chunk = coerce_daily_stock_frame(raw, contract)
        chunk = _filter_date_window(chunk, contract, start, end)
        if chunk.empty:
            if max_input_rows is not None and scanned >= max_input_rows:
                break
            continue
        rows_after_date_filter += int(len(chunk))
        _update_daily_count(raw_daily_counts, chunk[contract.date])
        eligible = static_eligibility_mask(chunk, contract, require_return=True)
        _update_daily_count(eligible_daily_counts, chunk.loc[eligible, contract.date])
        raw_trading_dates.update(pd.to_datetime(chunk[contract.date].dropna()).tolist())
        eligible_trading_dates.update(pd.to_datetime(chunk.loc[eligible, contract.date].dropna()).tolist())
        if max_input_rows is not None and scanned >= max_input_rows:
            break

    return {
        "rows_scanned_raw": int(scanned),
        "rows_after_date_filter": int(rows_after_date_filter),
        "raw_trading_dates": sorted(raw_trading_dates),
        "eligible_trading_dates": sorted(eligible_trading_dates),
        # Rolling-universe formation should match remote_sample_eval, which
        # builds its calendar after fixed eligibility and duplicate handling.
        "trading_dates": sorted(eligible_trading_dates),
        "raw_daily_counts": raw_daily_counts,
        "eligible_daily_counts": eligible_daily_counts,
    }


def _month_formations(trading_dates: pd.Index) -> dict[str, MonthFormation]:
    months = pd.Index(trading_dates.to_period("M").to_timestamp().unique()).sort_values()
    formations: dict[str, MonthFormation] = {}
    for raw_month in months:
        month = pd.Timestamp(raw_month)
        prior_dates = trading_dates[trading_dates < month]
        if prior_dates.empty:
            continue
        month_key = month.date().isoformat()
        formations[month_key] = MonthFormation(
            month=month_key,
            formation_date=pd.Timestamp(prior_dates[-1]),
            selected_count=0,
        )
    return formations


def _load_formation_rows(
    csv: Path,
    *,
    usecols: list[str],
    chunksize: int,
    formation_dates: list[pd.Timestamp],
    max_input_rows: int | None,
    contract: DailyStockContract,
) -> pd.DataFrame:
    if not formation_dates:
        return pd.DataFrame(columns=usecols)
    date_set = set(pd.to_datetime(formation_dates))
    frames: list[pd.DataFrame] = []
    scanned = 0
    for raw in pd.read_csv(csv, usecols=usecols, chunksize=chunksize, low_memory=False):
        if max_input_rows is not None:
            remaining = max_input_rows - scanned
            if remaining <= 0:
                break
            raw = raw.head(remaining)
        scanned += len(raw)
        chunk = coerce_daily_stock_frame(raw, contract)
        chunk = chunk.loc[chunk[contract.date].isin(date_set)].copy()
        if chunk.empty:
            if max_input_rows is not None and scanned >= max_input_rows:
                break
            continue
        eligible = static_eligibility_mask(chunk, contract, require_return=True)
        frames.append(chunk.loc[eligible].copy())
        if max_input_rows is not None and scanned >= max_input_rows:
            break
    if not frames:
        return pd.DataFrame(columns=usecols)
    return pd.concat(frames, ignore_index=True).drop_duplicates(
        [contract.date, contract.security_id],
        keep="first",
    )


def _build_membership(
    formation_frame: pd.DataFrame,
    formations: dict[str, MonthFormation],
    *,
    top_n: int,
    contract: DailyStockContract,
) -> pd.DataFrame:
    if formation_frame.empty:
        return pd.DataFrame(columns=["month", "formation_date", contract.security_id])
    rows: list[dict[str, Any]] = []
    by_date = dict(tuple(formation_frame.groupby(contract.date, sort=False)))
    for month, formation in formations.items():
        frame = by_date.get(formation.formation_date)
        if frame is None or frame.empty:
            continue
        selected = frame.sort_values(
            [contract.market_cap, contract.security_id],
            ascending=[False, True],
        ).head(top_n)
        for _, row in selected.iterrows():
            rows.append(
                {
                    "month": month,
                    "formation_date": formation.formation_date.date().isoformat(),
                    contract.security_id: int(row[contract.security_id]),
                    "formation_market_cap": float(row[contract.market_cap]),
                    "formation_abs_price": float(abs(row[contract.price])),
                    "formation_dollar_volume": _safe_float(row.get(contract.dollar_volume)),
                    "formation_exchange": str(row.get(contract.exchange, "")),
                    "formation_sic2": _sic2(row.get(contract.industry_primary)),
                }
            )
    return pd.DataFrame(rows)


def _load_topn_panel(
    csv: Path,
    *,
    usecols: list[str],
    chunksize: int,
    membership: pd.DataFrame,
    start_date: str | None,
    end_date: str | None,
    max_input_rows: int | None,
    contract: DailyStockContract,
) -> pd.DataFrame:
    start = pd.Timestamp(start_date) if start_date else None
    end = pd.Timestamp(end_date) if end_date else None
    keys = membership[["month", contract.security_id]].drop_duplicates().copy()
    keys[contract.security_id] = keys[contract.security_id].astype("Int64")
    frames: list[pd.DataFrame] = []
    scanned = 0

    for raw in pd.read_csv(csv, usecols=usecols, chunksize=chunksize, low_memory=False):
        if max_input_rows is not None:
            remaining = max_input_rows - scanned
            if remaining <= 0:
                break
            raw = raw.head(remaining)
        scanned += len(raw)
        chunk = coerce_daily_stock_frame(raw, contract)
        chunk = _filter_date_window(chunk, contract, start, end)
        if chunk.empty:
            if max_input_rows is not None and scanned >= max_input_rows:
                break
            continue
        eligible = static_eligibility_mask(chunk, contract, require_return=True)
        chunk = chunk.loc[eligible].copy()
        if chunk.empty:
            if max_input_rows is not None and scanned >= max_input_rows:
                break
            continue
        chunk["month"] = chunk[contract.date].dt.to_period("M").dt.to_timestamp().dt.date.astype(str)
        matched = chunk.merge(keys, on=["month", contract.security_id], how="inner")
        if not matched.empty:
            frames.append(_with_panel_features(matched, contract))
        if max_input_rows is not None and scanned >= max_input_rows:
            break

    if not frames:
        return pd.DataFrame(columns=unique_preserving_order([*usecols, "month"]))
    panel = pd.concat(frames, ignore_index=True)
    panel = panel.drop_duplicates([contract.date, contract.security_id], keep="first")
    return panel.sort_values([contract.date, contract.security_id]).reset_index(drop=True)


def _daily_coverage(
    panel: pd.DataFrame,
    membership: pd.DataFrame,
    trading_dates: pd.Index,
    contract: DailyStockContract,
) -> pd.DataFrame:
    selected_counts = membership.groupby("month")[contract.security_id].nunique().rename("selected_count")
    months = set(selected_counts.index)
    calendar = pd.DataFrame({"date": pd.to_datetime(trading_dates)})
    calendar["month"] = calendar["date"].dt.to_period("M").dt.to_timestamp().dt.date.astype(str)
    calendar = calendar.loc[calendar["month"].isin(months)].copy()
    observed = (
        panel.groupby([contract.date, "month"])[contract.security_id]
        .nunique()
        .rename("observed_count")
        .reset_index()
        .rename(columns={contract.date: "date"})
    )
    daily = calendar.merge(observed, on=["date", "month"], how="left")
    daily["observed_count"] = daily["observed_count"].fillna(0).astype(int)
    daily = daily.merge(selected_counts.reset_index(), on="month", how="left")
    daily["missing_selected_count"] = daily["selected_count"] - daily["observed_count"]
    daily["coverage_rate"] = daily["observed_count"] / daily["selected_count"]
    return daily.sort_values("date").reset_index(drop=True)


def _monthly_coverage(daily_coverage: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for month, group in daily_coverage.groupby("month", sort=True):
        selected = int(group["selected_count"].max())
        trading_days = int(len(group))
        observed_rows = int(group["observed_count"].sum())
        expected_rows = int(selected * trading_days)
        rows.append(
            {
                "month": month,
                "selected_count": selected,
                "trading_days": trading_days,
                "expected_rows": expected_rows,
                "observed_rows": observed_rows,
                "missing_selected_rows": expected_rows - observed_rows,
                "coverage_rate": observed_rows / expected_rows if expected_rows else np.nan,
                "min_daily_observed_count": int(group["observed_count"].min()),
                "median_daily_observed_count": float(group["observed_count"].median()),
                "max_daily_observed_count": int(group["observed_count"].max()),
            }
        )
    return pd.DataFrame(rows)


def _permno_coverage(
    panel: pd.DataFrame,
    membership: pd.DataFrame,
    daily_coverage: pd.DataFrame,
    contract: DailyStockContract,
) -> pd.DataFrame:
    month_days = daily_coverage.groupby("month")["date"].nunique().rename("expected_days")
    expected = membership[["month", contract.security_id]].merge(month_days.reset_index(), on="month", how="left")
    expected_rows = (
        expected.groupby(contract.security_id)
        .agg(months_in_topn=("month", "nunique"), expected_days=("expected_days", "sum"))
        .reset_index()
    )
    observed_rows = (
        panel.groupby(contract.security_id)
        .agg(
            observed_days=(contract.date, "nunique"),
            first_observed_date=(contract.date, "min"),
            last_observed_date=(contract.date, "max"),
            median_market_cap=(contract.market_cap, "median"),
            median_dollar_volume=(contract.dollar_volume, "median"),
        )
        .reset_index()
    )
    result = expected_rows.merge(observed_rows, on=contract.security_id, how="left")
    result["observed_days"] = result["observed_days"].fillna(0).astype(int)
    result["coverage_rate"] = result["observed_days"] / result["expected_days"]
    return result.sort_values(["months_in_topn", "observed_days"], ascending=[False, False])


def _membership_churn(membership: pd.DataFrame, contract: DailyStockContract) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    month_sets = {
        month: set(group[contract.security_id].dropna().astype(int).tolist())
        for month, group in membership.groupby("month", sort=True)
    }
    prev_month = None
    prev_set: set[int] | None = None
    for month in sorted(month_sets):
        current = month_sets[month]
        if prev_set is None:
            rows.append(
                {
                    "month": month,
                    "selected_count": len(current),
                    "prior_month": "",
                    "entries": np.nan,
                    "exits": np.nan,
                    "retained": np.nan,
                    "jaccard_vs_prior": np.nan,
                }
            )
        else:
            union = current | prev_set
            rows.append(
                {
                    "month": month,
                    "selected_count": len(current),
                    "prior_month": prev_month,
                    "entries": len(current - prev_set),
                    "exits": len(prev_set - current),
                    "retained": len(current & prev_set),
                    "jaccard_vs_prior": len(current & prev_set) / len(union) if union else np.nan,
                }
            )
        prev_month = month
        prev_set = current
    return pd.DataFrame(rows)


def _forward_availability_profile(
    panel: pd.DataFrame,
    membership: pd.DataFrame,
    *,
    start_date: str,
    end_date: str,
    contract: DailyStockContract,
) -> dict[str, Any]:
    start = pd.Timestamp(start_date)
    end = pd.Timestamp(end_date)
    window = panel.loc[panel[contract.date].between(start, end)].copy()
    if window.empty:
        empty = pd.DataFrame()
        return {
            "summary": {
                "enabled": False,
                "reason": "no top-N panel rows in forward window",
                "start_date": start_date,
                "end_date": end_date,
            },
            "availability_by_date": empty,
            "availability_by_bucket": empty,
            "availability_by_industry": empty,
            "availability_by_exchange": empty,
            "row_diagnostics_head": empty,
        }

    forward = build_forward_returns(window, contract)
    forward = _add_forward_missing_causes(forward, contract)
    forward = _add_bucket_columns(forward, contract)
    forward = _add_membership_exit_flag(forward, membership, contract)

    by_date = _forward_by_date(forward, contract)
    by_bucket = _forward_by_bucket(forward)
    by_industry = _forward_by_dimension(forward, "sic2")
    by_exchange = _forward_by_dimension(forward, contract.exchange)
    cause_counts = forward["forward_availability_cause"].value_counts(dropna=False).to_dict()
    available = int((forward["forward_availability_cause"] == "available").sum())
    total = int(len(forward))
    summary = {
        "enabled": True,
        "start_date": start_date,
        "end_date": end_date,
        "row_count": total,
        "available_count": available,
        "unavailable_count": int(total - available),
        "availability_rate": available / total if total else None,
        "cause_counts": {str(key): int(value) for key, value in cause_counts.items()},
        "date_count": int(forward[contract.date].nunique()),
        "permno_count": int(forward[contract.security_id].nunique()),
        "mean_daily_availability_rate": float(by_date["availability_rate"].mean()) if not by_date.empty else None,
        "min_daily_availability_rate": float(by_date["availability_rate"].min()) if not by_date.empty else None,
    }
    keep_cols = [
        contract.date,
        contract.security_id,
        "month",
        contract.exchange,
        "sic2",
        "abs_price",
        "log_dollar_volume",
        "log_market_cap",
        "next_market_date",
        "fwd_date",
        "fwd_ret",
        "one_day_forward",
        "forward_availability_cause",
        "membership_continues_next_month",
        "price_bucket",
        "dollar_volume_bucket",
        "market_cap_bucket",
    ]
    return {
        "summary": summary,
        "availability_by_date": by_date,
        "availability_by_bucket": by_bucket,
        "availability_by_industry": by_industry,
        "availability_by_exchange": by_exchange,
        "row_diagnostics_head": forward[[col for col in keep_cols if col in forward.columns]].head(50_000),
    }


def _add_forward_missing_causes(frame: pd.DataFrame, contract: DailyStockContract) -> pd.DataFrame:
    out = frame.copy()
    cause = pd.Series("available", index=out.index, dtype="object")
    cause = cause.mask(out["next_market_date"].isna(), "final_visible_market_date")
    cause = cause.mask(out["next_market_date"].notna() & out["fwd_date"].isna(), "no_next_security_row")
    gap = out["fwd_date"].notna() & out["next_market_date"].notna() & ~out["fwd_date"].eq(out["next_market_date"])
    cause = cause.mask(gap, "security_not_observed_next_market_date")
    missing_return = out["fwd_date"].eq(out["next_market_date"]) & out["fwd_ret"].isna()
    cause = cause.mask(missing_return, "missing_forward_return")
    out["forward_availability_cause"] = cause
    out["sic2"] = (pd.to_numeric(out[contract.industry_primary], errors="coerce") // 100).astype("Int64")
    return out


def _add_bucket_columns(frame: pd.DataFrame, contract: DailyStockContract) -> pd.DataFrame:
    out = frame.copy()
    out["abs_price"] = out[contract.price].abs()
    out["log_dollar_volume"] = np.log1p(out[contract.dollar_volume].clip(lower=0.0))
    out["log_market_cap"] = np.log1p(out[contract.market_cap].clip(lower=0.0))
    out["price_bucket"] = _date_rank_bucket(out, "abs_price")
    out["dollar_volume_bucket"] = _date_rank_bucket(out, contract.dollar_volume)
    out["market_cap_bucket"] = _date_rank_bucket(out, contract.market_cap)
    return out


def _add_membership_exit_flag(
    frame: pd.DataFrame,
    membership: pd.DataFrame,
    contract: DailyStockContract,
) -> pd.DataFrame:
    out = frame.copy()
    months = sorted(str(month) for month in membership["month"].dropna().unique())
    next_month = {months[idx]: months[idx + 1] for idx in range(len(months) - 1)}
    out["next_membership_month"] = out["month"].map(next_month)
    next_keys = membership[["month", contract.security_id]].drop_duplicates().rename(
        columns={"month": "next_membership_month"}
    )
    next_keys["membership_continues_next_month"] = True
    out = out.merge(next_keys, on=["next_membership_month", contract.security_id], how="left")
    out["membership_continues_next_month"] = out["membership_continues_next_month"].where(
        out["next_membership_month"].notna(),
        None,
    )
    out.loc[out["next_membership_month"].notna(), "membership_continues_next_month"] = (
        out.loc[out["next_membership_month"].notna(), "membership_continues_next_month"].fillna(False)
    )
    return out


def _forward_by_date(frame: pd.DataFrame, contract: DailyStockContract) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for date, group in frame.groupby(contract.date, sort=True):
        cause_counts = group["forward_availability_cause"].value_counts()
        total = int(len(group))
        available = int(cause_counts.get("available", 0))
        rows.append(
            {
                "date": pd.Timestamp(date).date().isoformat(),
                "row_count": total,
                "available_count": available,
                "unavailable_count": total - available,
                "availability_rate": available / total if total else np.nan,
                "security_not_observed_next_market_date": int(
                    cause_counts.get("security_not_observed_next_market_date", 0)
                ),
                "missing_forward_return": int(cause_counts.get("missing_forward_return", 0)),
                "no_next_security_row": int(cause_counts.get("no_next_security_row", 0)),
                "final_visible_market_date": int(cause_counts.get("final_visible_market_date", 0)),
            }
        )
    return pd.DataFrame(rows)


def _forward_by_bucket(frame: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for column in ["price_bucket", "dollar_volume_bucket", "market_cap_bucket"]:
        rows.extend(_dimension_rows(frame, column, dimension_name=column))
    rows.extend(_dimension_rows(frame, "membership_continues_next_month", dimension_name="membership_continues_next_month"))
    return pd.DataFrame(rows)


def _forward_by_dimension(frame: pd.DataFrame, column: str) -> pd.DataFrame:
    return pd.DataFrame(_dimension_rows(frame, column, dimension_name=column))


def _dimension_rows(frame: pd.DataFrame, column: str, *, dimension_name: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if column not in frame.columns:
        return rows
    for value, group in frame.groupby(column, dropna=False, sort=True, observed=False):
        cause_counts = group["forward_availability_cause"].value_counts()
        total = int(len(group))
        available = int(cause_counts.get("available", 0))
        rows.append(
            {
                "dimension": dimension_name,
                "value": str(value),
                "row_count": total,
                "available_count": available,
                "unavailable_count": total - available,
                "availability_rate": available / total if total else np.nan,
                "security_not_observed_next_market_date": int(
                    cause_counts.get("security_not_observed_next_market_date", 0)
                ),
                "missing_forward_return": int(cause_counts.get("missing_forward_return", 0)),
                "no_next_security_row": int(cause_counts.get("no_next_security_row", 0)),
                "final_visible_market_date": int(cause_counts.get("final_visible_market_date", 0)),
            }
        )
    return rows


def _write_forward_coverage_artifacts(
    out: Path,
    *,
    membership: pd.DataFrame,
    daily_coverage: pd.DataFrame,
    monthly_coverage: pd.DataFrame,
    permno_coverage: pd.DataFrame,
    churn: pd.DataFrame,
    forward_payload: dict[str, Any],
    calendar: dict[str, Any],
    csv_path: Path,
    top_n: int,
    coverage_start_date: str | None,
    coverage_end_date: str | None,
    forward_start_date: str,
    forward_end_date: str,
    max_input_rows: int | None,
) -> dict[str, str]:
    summary = _summary_payload(
        calendar=calendar,
        membership=membership,
        daily_coverage=daily_coverage,
        monthly_coverage=monthly_coverage,
        permno_coverage=permno_coverage,
        churn=churn,
        forward_payload=forward_payload,
        top_n=top_n,
        coverage_start_date=coverage_start_date,
        coverage_end_date=coverage_end_date,
        forward_start_date=forward_start_date,
        forward_end_date=forward_end_date,
        max_input_rows=max_input_rows,
        csv_path=csv_path,
    )
    paths = {
        "summary_json": str(write_json(out / "forward_coverage_summary.json", summary)),
    }
    membership.to_csv(out / "top500_membership_monthly.csv", index=False)
    daily_coverage.to_csv(out / "top500_daily_coverage.csv", index=False)
    monthly_coverage.to_csv(out / "top500_monthly_coverage.csv", index=False)
    permno_coverage.to_csv(out / "top500_permno_coverage.csv", index=False)
    churn.to_csv(out / "top500_membership_churn.csv", index=False)
    forward_payload["availability_by_date"].to_csv(out / "forward_availability_by_date.csv", index=False)
    forward_payload["availability_by_bucket"].to_csv(out / "forward_availability_by_bucket.csv", index=False)
    forward_payload["availability_by_industry"].to_csv(out / "forward_availability_by_industry.csv", index=False)
    forward_payload["availability_by_exchange"].to_csv(out / "forward_availability_by_exchange.csv", index=False)
    forward_payload["row_diagnostics_head"].to_csv(out / "forward_availability_diagnostics_head.csv", index=False)
    write_json(out / "forward_availability_summary.json", forward_payload["summary"])
    _write_prompt_cards(out / "held_availability_prompt_cards.md", summary)
    _write_markdown_review(out / "forward_coverage_summary.md", summary)
    paths.update(
        {
            "summary_markdown": str(out / "forward_coverage_summary.md"),
            "prompt_cards": str(out / "held_availability_prompt_cards.md"),
            "top500_membership_monthly": str(out / "top500_membership_monthly.csv"),
            "top500_daily_coverage": str(out / "top500_daily_coverage.csv"),
            "top500_monthly_coverage": str(out / "top500_monthly_coverage.csv"),
            "top500_permno_coverage": str(out / "top500_permno_coverage.csv"),
            "top500_membership_churn": str(out / "top500_membership_churn.csv"),
            "forward_availability_by_date": str(out / "forward_availability_by_date.csv"),
            "forward_availability_by_bucket": str(out / "forward_availability_by_bucket.csv"),
            "forward_availability_by_industry": str(out / "forward_availability_by_industry.csv"),
            "forward_availability_by_exchange": str(out / "forward_availability_by_exchange.csv"),
            "forward_availability_summary": str(out / "forward_availability_summary.json"),
            "forward_availability_diagnostics_head": str(out / "forward_availability_diagnostics_head.csv"),
        }
    )
    return paths


def _summary_payload(
    *,
    calendar: dict[str, Any],
    membership: pd.DataFrame,
    daily_coverage: pd.DataFrame,
    monthly_coverage: pd.DataFrame,
    permno_coverage: pd.DataFrame,
    churn: pd.DataFrame,
    forward_payload: dict[str, Any],
    top_n: int,
    coverage_start_date: str | None,
    coverage_end_date: str | None,
    forward_start_date: str,
    forward_end_date: str,
    max_input_rows: int | None,
    csv_path: Path,
) -> dict[str, Any]:
    daily_rates = daily_coverage["coverage_rate"] if not daily_coverage.empty else pd.Series(dtype=float)
    monthly_rates = monthly_coverage["coverage_rate"] if not monthly_coverage.empty else pd.Series(dtype=float)
    churn_jaccard = churn["jaccard_vs_prior"].dropna() if not churn.empty else pd.Series(dtype=float)
    return {
        "schema_version": FORWARD_COVERAGE_SCHEMA_VERSION,
        "csv_path": str(csv_path),
        "top_n": int(top_n),
        "coverage_start_date": coverage_start_date,
        "coverage_end_date": coverage_end_date,
        "forward_start_date": forward_start_date,
        "forward_end_date": forward_end_date,
        "max_input_rows": max_input_rows,
        "rows_scanned_raw": calendar["rows_scanned_raw"],
        "rows_after_date_filter": calendar["rows_after_date_filter"],
        "raw_trading_date_count": len(calendar.get("raw_trading_dates", calendar["trading_dates"])),
        "eligible_trading_date_count": len(calendar["trading_dates"]),
        "trading_date_count": len(calendar["trading_dates"]),
        "topn_month_count": int(membership["month"].nunique()) if not membership.empty else 0,
        "topn_membership_rows": int(len(membership)),
        "topn_distinct_permnos": int(membership[CONTRACT.security_id].nunique()) if not membership.empty else 0,
        "daily_coverage": {
            "row_count": int(len(daily_coverage)),
            "mean_coverage_rate": _safe_float(daily_rates.mean()),
            "min_coverage_rate": _safe_float(daily_rates.min()),
            "median_coverage_rate": _safe_float(daily_rates.median()),
            "p01_coverage_rate": _safe_float(daily_rates.quantile(0.01)) if len(daily_rates) else None,
            "median_observed_count": _safe_float(daily_coverage["observed_count"].median()) if not daily_coverage.empty else None,
            "min_observed_count": _safe_float(daily_coverage["observed_count"].min()) if not daily_coverage.empty else None,
        },
        "monthly_coverage": {
            "mean_coverage_rate": _safe_float(monthly_rates.mean()),
            "min_coverage_rate": _safe_float(monthly_rates.min()),
            "median_coverage_rate": _safe_float(monthly_rates.median()),
        },
        "permno_coverage": {
            "row_count": int(len(permno_coverage)),
            "median_months_in_topn": _safe_float(permno_coverage["months_in_topn"].median())
            if not permno_coverage.empty
            else None,
            "max_months_in_topn": _safe_float(permno_coverage["months_in_topn"].max())
            if not permno_coverage.empty
            else None,
        },
        "membership_churn": {
            "median_jaccard_vs_prior": _safe_float(churn_jaccard.median()) if len(churn_jaccard) else None,
            "min_jaccard_vs_prior": _safe_float(churn_jaccard.min()) if len(churn_jaccard) else None,
            "median_entries": _safe_float(churn["entries"].median()) if "entries" in churn else None,
            "max_entries": _safe_float(churn["entries"].max()) if "entries" in churn else None,
        },
        "forward_availability": forward_payload["summary"],
    }


def _write_prompt_cards(path: Path, summary: dict[str, Any]) -> None:
    forward = summary.get("forward_availability", {})
    coverage = summary.get("daily_coverage", {})
    churn = summary.get("membership_churn", {})
    lines = [
        "# Held Availability Prompt Cards",
        "",
        "These cards describe structural top-N coverage and next-day return availability. They are not alpha evidence.",
        "",
        "## Coverage Card",
        "",
        f"- top_n: `{summary.get('top_n')}`",
        f"- topn_month_count: `{summary.get('topn_month_count')}`",
        f"- topn_distinct_permnos: `{summary.get('topn_distinct_permnos')}`",
        f"- median_daily_coverage_rate: `{coverage.get('median_coverage_rate')}`",
        f"- min_daily_coverage_rate: `{coverage.get('min_coverage_rate')}`",
        "",
        "## Forward Availability Card",
        "",
        f"- forward_window: `{summary.get('forward_start_date')} to {summary.get('forward_end_date')}`",
        f"- availability_rate: `{forward.get('availability_rate')}`",
        f"- cause_counts: `{forward.get('cause_counts')}`",
        "",
        "## Membership Churn Card",
        "",
        f"- median_jaccard_vs_prior: `{churn.get('median_jaccard_vs_prior')}`",
        f"- median_entries: `{churn.get('median_entries')}`",
        f"- max_entries: `{churn.get('max_entries')}`",
        "",
        "## Prompt Rules",
        "",
        "- Treat next-day availability as a structural evaluator constraint, not a strategy feature.",
        "- If missing forward returns concentrate in low-liquidity, low-price, industry, or membership-exit buckets, prefer robust risk or holding rules that reduce that exposure without using future returns.",
        "- Separate signal turnover from rolling-universe membership churn when interpreting turnover.",
        "- Do not use `fwd_ret`, `fwd_date`, `next_market_date`, or `one_day_forward` inside generated child strategies.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_markdown_review(path: Path, summary: dict[str, Any]) -> None:
    lines = [
        "# Forward Coverage Summary",
        "",
        f"- schema_version: `{summary.get('schema_version')}`",
        f"- rows_after_date_filter: `{summary.get('rows_after_date_filter')}`",
        f"- trading_date_count: `{summary.get('trading_date_count')}`",
        f"- topn_month_count: `{summary.get('topn_month_count')}`",
        f"- topn_membership_rows: `{summary.get('topn_membership_rows')}`",
        f"- topn_distinct_permnos: `{summary.get('topn_distinct_permnos')}`",
        "",
        "## Daily Coverage",
        "",
    ]
    for key, value in (summary.get("daily_coverage") or {}).items():
        lines.append(f"- {key}: `{value}`")
    lines.extend(["", "## Membership Churn", ""])
    for key, value in (summary.get("membership_churn") or {}).items():
        lines.append(f"- {key}: `{value}`")
    lines.extend(["", "## Forward Availability", ""])
    for key, value in (summary.get("forward_availability") or {}).items():
        lines.append(f"- {key}: `{value}`")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _filter_date_window(
    frame: pd.DataFrame,
    contract: DailyStockContract,
    start: pd.Timestamp | None,
    end: pd.Timestamp | None,
) -> pd.DataFrame:
    out = frame
    if start is not None:
        out = out.loc[out[contract.date] >= start]
    if end is not None:
        out = out.loc[out[contract.date] <= end]
    return out


def _with_panel_features(frame: pd.DataFrame, contract: DailyStockContract) -> pd.DataFrame:
    out = frame.copy()
    out["abs_price"] = out[contract.price].abs()
    out["log_dollar_volume"] = np.log1p(out[contract.dollar_volume].clip(lower=0.0))
    out["log_market_cap"] = np.log1p(out[contract.market_cap].clip(lower=0.0))
    out["sic2"] = (pd.to_numeric(out[contract.industry_primary], errors="coerce") // 100).astype("Int64")
    return out


def _date_rank_bucket(frame: pd.DataFrame, column: str) -> pd.Series:
    ranks = frame.groupby(CONTRACT.date)[column].rank(pct=True, method="average")
    labels = ["q00_q20", "q20_q40", "q40_q60", "q60_q80", "q80_q100"]
    return pd.cut(ranks, bins=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0], labels=labels, include_lowest=True)


def _update_daily_count(target: dict[str, int], dates: pd.Series) -> None:
    cleaned = pd.to_datetime(dates, errors="coerce").dropna().dt.date.astype(str)
    counts = cleaned.value_counts()
    for date, count in counts.items():
        target[str(date)] = int(target.get(str(date), 0) + count)


def _coverage_usecols(columns: list[str], contract: DailyStockContract) -> list[str]:
    optional = [col for col in OPTIONAL_CAUSE_COLUMNS if col in set(columns)]
    return unique_preserving_order([*contract.required_columns, *optional])


def _read_header(csv: Path) -> list[str]:
    return [str(col) for col in pd.read_csv(csv, nrows=0).columns]


def _sic2(value: Any) -> int | None:
    numeric = _safe_float(value)
    if numeric is None:
        return None
    return int(numeric // 100)


def _safe_float(value: Any) -> float | None:
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    return result if np.isfinite(result) else None


__all__ = [
    "FORWARD_COVERAGE_SCHEMA_VERSION",
    "profile_daily_stock_forward_coverage",
]
