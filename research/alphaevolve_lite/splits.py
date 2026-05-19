"""Chronological split construction for Phase 4 daily_stock evaluation."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

import pandas as pd


IS_OS_SPLIT_ID = "daily_stock_top500_is_2011_2022_os_2023_2025_v1"
LEGACY_70_15_15_SPLIT_ID = "daily_stock_top500_chrono_70_15_15_v1"
DEFAULT_ANALYSIS_START_DATE = "2011-01-01"
DEFAULT_ANALYSIS_END_DATE = "2025-12-31"
DEFAULT_OUT_SAMPLE_START_DATE = "2023-01-01"


@dataclass(frozen=True)
class Split:
    name: str
    start: pd.Timestamp
    end: pd.Timestamp
    n_dates: int

    def contains(self, dates: pd.Series) -> pd.Series:
        return dates.between(self.start, self.end)

    def as_record(self) -> dict[str, object]:
        record = asdict(self)
        record["start"] = self.start.date().isoformat()
        record["end"] = self.end.date().isoformat()
        return record


def build_chronological_splits(
    trading_dates: pd.Series | pd.Index,
    *,
    train_fraction: float = 0.70,
    validation_fraction: float = 0.15,
) -> list[Split]:
    """Build legacy 70/15/15 splits from cleaned unique trading dates."""

    dates = pd.Index(pd.to_datetime(pd.Series(trading_dates).dropna()).sort_values().unique())
    if len(dates) < 10:
        raise ValueError(f"need at least 10 trading dates to split; observed {len(dates)}")
    train_end_idx = max(1, int(len(dates) * train_fraction))
    validation_end_idx = max(train_end_idx + 1, int(len(dates) * (train_fraction + validation_fraction)))
    validation_end_idx = min(validation_end_idx, len(dates) - 1)
    return [
        Split("train", dates[0], dates[train_end_idx - 1], train_end_idx),
        Split("validation", dates[train_end_idx], dates[validation_end_idx - 1], validation_end_idx - train_end_idx),
        Split("test", dates[validation_end_idx], dates[-1], len(dates) - validation_end_idx),
    ]


def build_is_os_splits(
    trading_dates: pd.Series | pd.Index,
    *,
    out_sample_start: str | pd.Timestamp = DEFAULT_OUT_SAMPLE_START_DATE,
) -> list[Split]:
    """Build the Phase 4 fixed IS/OS split from cleaned unique trading dates.

    The caller owns the outer data window. For the active first loop that
    window is expected to start on or after 2011-01-01 and end in 2025. The
    split itself is fixed by calendar date so repeated evaluations do not move
    the out-of-sample boundary after seeing results.
    """

    dates = pd.Index(pd.to_datetime(pd.Series(trading_dates).dropna()).sort_values().unique())
    if len(dates) < 10:
        raise ValueError(f"need at least 10 trading dates to split; observed {len(dates)}")
    os_start = pd.Timestamp(out_sample_start)
    in_dates = dates[dates < os_start]
    os_dates = dates[dates >= os_start]
    if in_dates.empty:
        raise ValueError(f"no in-sample dates before out_sample_start={os_start.date().isoformat()}")
    if os_dates.empty:
        raise ValueError(f"no out-of-sample dates on or after out_sample_start={os_start.date().isoformat()}")
    return [
        Split("in_sample", in_dates[0], in_dates[-1], len(in_dates)),
        Split("out_sample", os_dates[0], os_dates[-1], len(os_dates)),
    ]


def split_for_date(date: pd.Timestamp, splits: list[Split]) -> str | None:
    for split in splits:
        if split.start <= date <= split.end:
            return split.name
    return None


def write_split_manifest(
    path: str | Path,
    *,
    splits: list[Split],
    calendar_count: int,
    universe_policy: str,
    duplicate_policy: dict[str, object],
    split_id: str = IS_OS_SPLIT_ID,
    split_policy: str = "fixed_calendar_is_os",
) -> Path:
    """Write a simple YAML manifest without requiring PyYAML."""

    lines = [
        f"split_id: {split_id}",
        "split_unit: cleaned_unique_trading_dates",
        f"split_policy: {split_policy}",
        f"calendar_count: {calendar_count}",
        f"universe_policy: {universe_policy}",
        "out_sample_used_for_search_feedback: true",
        "final_test_set_defined: false",
        "no_full_period_static_top500: true",
        "duplicate_policy:",
    ]
    for key, value in duplicate_policy.items():
        lines.append(f"  {key}: {value}")
    lines.append("splits:")
    for split in splits:
        lines.append(f"  - name: {split.name}")
        lines.append(f"    start: {split.start.date().isoformat()}")
        lines.append(f"    end: {split.end.date().isoformat()}")
        lines.append(f"    n_dates: {split.n_dates}")
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return Path(path)
