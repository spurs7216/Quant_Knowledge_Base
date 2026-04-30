"""Fixed rolling-universe construction for Phase 4 daily_stock evaluation."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from .daily_stock_contract import CONTRACT, DailyStockContract
from .daily_stock_loader import static_eligibility_mask


UNIVERSE_POLICY_ID = "rolling_top500_market_cap_v1"


def month_start(series: pd.Series) -> pd.Series:
    return series.dt.to_period("M").dt.to_timestamp()


def build_monthly_rolling_universe(
    panel: pd.DataFrame,
    *,
    contract: DailyStockContract = CONTRACT,
    top_n: int = 500,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Compute monthly top-N membership from prior-month-end market cap."""

    if panel.empty:
        membership = pd.DataFrame(columns=["month", "formation_date", contract.security_id])
        summary = pd.DataFrame(
            columns=[
                "month",
                "formation_date",
                "eligible_count",
                "selected_count",
                "median_market_cap",
                "min_selected_market_cap",
                "max_selected_market_cap",
                "missing_price_count",
                "missing_shrout_count",
                "dropped_midmonth_count",
            ]
        )
        return membership, summary

    data = panel.sort_values([contract.date, contract.security_id]).copy()
    data["month"] = month_start(data[contract.date])
    trading_dates = pd.Index(data[contract.date].dropna().sort_values().unique())
    months = pd.Index(data["month"].dropna().sort_values().unique())

    membership_rows: list[dict[str, object]] = []
    summary_rows: list[dict[str, object]] = []

    for raw_month in months:
        month = pd.Timestamp(raw_month)
        prior_dates = trading_dates[trading_dates < month]
        if prior_dates.empty:
            continue
        formation_date = pd.Timestamp(prior_dates[-1])
        formation = data.loc[data[contract.date].eq(formation_date)].copy()
        eligible_mask = static_eligibility_mask(formation, contract, require_return=False)
        eligible = formation.loc[eligible_mask].copy()
        selected = eligible.sort_values(
            [contract.market_cap, contract.security_id],
            ascending=[False, True],
        ).head(top_n)
        selected_ids = set(selected[contract.security_id].dropna().astype(int).tolist())
        month_rows = data.loc[data["month"].eq(month)]
        observed_ids = set(month_rows[contract.security_id].dropna().astype(int).tolist())
        dropped_midmonth_count = len(selected_ids - observed_ids)

        for permno in sorted(selected_ids):
            membership_rows.append(
                {
                    "month": month.date().isoformat(),
                    "formation_date": formation_date.date().isoformat(),
                    contract.security_id: permno,
                }
            )
        summary_rows.append(
            {
                "month": month.date().isoformat(),
                "formation_date": formation_date.date().isoformat(),
                "eligible_count": int(len(eligible)),
                "selected_count": int(len(selected)),
                "median_market_cap": float(selected[contract.market_cap].median()) if len(selected) else float("nan"),
                "min_selected_market_cap": float(selected[contract.market_cap].min()) if len(selected) else float("nan"),
                "max_selected_market_cap": float(selected[contract.market_cap].max()) if len(selected) else float("nan"),
                "missing_price_count": int(formation[contract.price].isna().sum()),
                "missing_shrout_count": int(formation[contract.shares_outstanding].isna().sum()),
                "dropped_midmonth_count": int(dropped_midmonth_count),
            }
        )

    membership = pd.DataFrame(membership_rows)
    summary = pd.DataFrame(summary_rows)
    return membership, summary


def apply_monthly_universe(
    panel: pd.DataFrame,
    membership: pd.DataFrame,
    *,
    contract: DailyStockContract = CONTRACT,
) -> pd.DataFrame:
    """Keep rows that belong to the precomputed monthly universe."""

    if panel.empty or membership.empty:
        return panel.iloc[0:0].copy()
    data = panel.copy()
    data["month"] = month_start(data[contract.date]).dt.date.astype(str)
    keys = membership[["month", contract.security_id]].drop_duplicates().copy()
    keys[contract.security_id] = keys[contract.security_id].astype(data[contract.security_id].dtype)
    filtered = data.merge(keys, on=["month", contract.security_id], how="inner")
    return filtered.drop(columns=["month"]).reset_index(drop=True)


def write_universe_artifacts(
    out_dir: str | Path,
    membership: pd.DataFrame,
    summary: pd.DataFrame,
) -> dict[str, str]:
    path = Path(out_dir)
    path.mkdir(parents=True, exist_ok=True)
    membership_path = path / "universe_membership_monthly.csv"
    summary_path = path / "universe_summary.csv"
    membership.to_csv(membership_path, index=False)
    summary.to_csv(summary_path, index=False)
    return {"membership": str(membership_path), "summary": str(summary_path)}
