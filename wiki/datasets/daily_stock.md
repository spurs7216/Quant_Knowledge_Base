---
type: dataset
status: active
dataset: daily_stock
domain: equities
updated: 2026-05-19
source_count: 12
tags:
  - dataset
  - equities
  - market-data
sources:
  - "[[catalog/csv_data_catalog.md]]"
  - "[[catalog/csv_data_inventory.csv]]"
  - "[[catalog/samples/daily_stock/gago9dveytpx6922.csv]]"
  - "[[catalog/samples/processed/eda/daily_stock_universe_summary.csv]]"
  - "[[catalog/samples/processed/eda/equity_research_eda_notes.csv]]"
  - "[[projects/quant_research_system/phase4_search_loop/daily_stock_contract_v1.md]]"
  - "[[projects/quant_research_system/phase4_search_loop/daily_stock_data_understanding_plan_20260518.md]]"
  - "[[projects/quant_research_system/phase4_search_loop/universe_and_split_policy.md]]"
  - "[[projects/quant_research_system/phase4_search_loop/is_os_evaluation_policy_20260519.md]]"
  - "[[projects/quant_research_system/phase4_search_loop/daily_stock_eda_full_review_20260518.md]]"
  - "[[projects/quant_research_system/phase4_search_loop/daily_stock_forward_coverage_review_20260519.md]]"
  - "[[projects/quant_research_system/phase4_search_loop/evaluator_forward_return_contract_repair_20260519.md]]"
---
# daily_stock

## Summary

`daily_stock` is the main daily equity panel in the vault's mirrored data catalog. It appears to be a CRSP-like security-day file with identifiers, security metadata, prices, returns, volume, dividend/distribution fields, and broad market return fields.

## What It Is

The dataset contains one row per security-date observation. The local mirror reports approximately 49.65 million rows and 94 columns in the physical file.

The sample shows that each row can contain:

- security identifiers such as `PERMNO`, `PERMCO`, `CUSIP`, `Ticker`, and `TradingSymbol`
- security descriptors such as exchange, issuer type, security type, and activity flags
- daily market data such as price, return, close, bid, ask, open, volume, and trade counts
- distribution fields and share-outstanding fields
- reference market returns such as `vwretd`, `vwretx`, `ewretd`, `ewretx`, and `sprtrn`

## Canonical Path

- Mirror inventory entry: `daily_stock/gago9dveytpx6922.csv`
- Sample file: `catalog/samples/daily_stock/gago9dveytpx6922.csv`

## Business Meaning

This is the core daily security panel for U.S. equity-style research in the vault. It is likely the main starting point for:

- security-level return construction
- universe formation
- volume and liquidity filters
- event alignment
- cross-sectional backtests

## Grain

The working grain appears to be `[[permno]]` by `DlyCalDt`.

The sample strongly suggests a security-day observation. In practice, users should still confirm whether any special duplicate conditions exist for halted, delisted, or distribution-heavy cases before production use.

## Primary Keys and Identifiers

Important identifiers observed in the mirror include:

- `[[permno]]`
- `PERMCO`
- `[[ticker]]`
- `[[cusip]]`
- `TradingSymbol`

The most trustworthy working identifier in this dataset is `[[permno]]`.

## Time Coverage

The mirrored inventory reports:

- `DlyCalDt`: 2000-01-03 to 2025-11-28

The EDA universe summary reports:

- total rows: 49,651,441
- unique permnos: 25,139
- unique tickers: 25,153
- missing ticker rows: 634,656
- missing ticker rate: about 1.28%

## Important Fields

Frequently useful fields visible in the sample include:

- `PERMNO`
- `PERMCO`
- `DlyCalDt`
- `DlyPrc`
- `DlyRet`
- `DlyRetx`
- `DlyVol`
- `PrimaryExch`
- `SecurityType`
- `Ticker`
- `vwretd`
- `sprtrn`

## Common Joins

- `[[permno]]` to [[CCM]] via `LPERMNO` for linking to Compustat-style fundamentals
- `[[ticker]]` or `[[cusip]]` for exploratory matching only
- market-return fields already live in-file, but dedicated market context also exists in `daily_market_index`
- excess-return construction should reference [[risk_free_rate]]

## Known Quality Issues

- `Ticker` is not complete and is not a safe primary production key.
- `Ticker` and `CUSIP` are time-varying and can drift across corporate actions.
- The physical file has 94 columns, but the compact EDA summary tracks a smaller analytic subset. Treat that as a mirror-summary convention, not a contradiction in the raw file.
- Distribution and share fields mean some research workflows need careful treatment of ordinary versus extraordinary returns.
- Do not infer cross-sectional behavior from first-N-row samples because the CSV can be security-sorted.
- Broad eligible-universe caveats and rolling top-500 caveats are not identical. The top-500 portfolio universe is cleaner, but still has heavy-tailed liquidity, market-cap, volume, and price fields.

## Phase 4 Profiling Workflow

The current AlphaEvolve-lite loop uses `daily_stock` only. The active project contract is [[projects/quant_research_system/phase4_search_loop/daily_stock_contract_v1.md]].

Active alpha-evolution evidence uses fixed IS/OS over the last-15-year development window:

- analysis window: 2011-01-01 through 2025-12-31
- in-sample: 2011-01-01 through 2022-12-31
- out-of-sample: 2023-01-01 through the latest available 2025 date
- split id: `daily_stock_top500_is_2011_2022_os_2023_2025_v1`

EDA and coverage diagnostics should still use the full available 2000-2025 timeline. The older 2018-2020 window is a smoke/debug window, not a performance-evidence window.

The remote empirical-map command is documented in [[projects/quant_research_system/phase4_search_loop/daily_stock_eda_remote_instructions_20260518.md]]. It uses:

- `research/alphaevolve_lite/daily_stock_eda.py`
- `research/alphaevolve_lite/scripts/profile_daily_stock_data.py`

The profiler writes compact artifact tables for row counts, fixed-eligibility attrition, missingness, numeric distributions, deterministic sample quantiles, daily breadth, rolling top-500 diagnostics, and prompt-facing data cards. Those outputs are data-understanding evidence, not alpha evidence.

The follow-up forward-coverage diagnostic is documented in [[projects/quant_research_system/phase4_search_loop/daily_stock_forward_coverage_remote_instructions_20260518.md]]. It uses:

- `research/alphaevolve_lite/daily_stock_forward_coverage.py`
- `research/alphaevolve_lite/scripts/profile_daily_stock_forward_coverage.py`

This second diagnostic measures whole-timeline rolling top-500 selected-name coverage and evaluator-style one-day-forward return availability. Its outputs should be interpreted as data-coverage and missing-held-cause evidence, not as strategy performance evidence.

## Phase 4 Empirical Profile 2026-05-18

Reviewed artifact: [[projects/quant_research_system/phase4_search_loop/daily_stock_eda_full_review_20260518.md]].

Full-file profile:

- rows scanned: 49,651,441
- date range: 2000-01-03 to 2025-11-28
- trading dates: 6,517
- unique `PERMNO`: 25,139
- fixed-contract eligible rows: 28,302,925, about 57.0% of raw rows
- unique eligible `PERMNO`: 13,342
- median eligible rows per date: about 4,136

2018-2020 rolling top-500 deep smoke profile:

- tradable top-500 rows: 367,092
- tradable dates: 735
- distinct `PERMNO`: 686
- median daily tradable count: 500
- median SIC2 groups per date: 53
- median SIC2 groups with at least 10 names: 15
- median largest SIC2 group share: about 13.2%
- median month-to-month top-500 membership Jaccard: about 0.957

Implementation lessons:

- Use date-window or rolling-universe loaders for research claims.
- Prefer date-level ranks, `log1p`, winsorized z-scores, or bounded transforms for `DlyPrcVol`, `DlyCap`, and `DlyVol`.
- Treat raw return levels as outlier-prone; exact full eligible stats include extreme returns even when high sample quantiles are less severe.
- Industry-neutral ranking is plausible in the top-500 universe only with minimum group-size fallback or shrinkage.
- Few-day portfolios are artifacts; the top-500 evaluation universe supports broad daily activity.

## Phase 4 Forward Coverage Profile 2026-05-19

Reviewed artifact: [[projects/quant_research_system/phase4_search_loop/daily_stock_forward_coverage_review_20260519.md]].

Whole-timeline rolling top-500 profile:

- monthly top-500 universes: 310
- top-500 membership rows: 155,000
- distinct rolling top-500 `PERMNO`: 1,675
- daily coverage rows: 6,497
- median daily observed selected names: 500
- median daily coverage rate: 1.000
- mean daily coverage rate: about 0.9984
- minimum daily coverage rate: 0.986, or 493 observed selected names out of 500

Membership churn:

- median month-to-month top-500 Jaccard: 0.953125
- median monthly entries: 12
- maximum monthly entries: 49
- minimum month-to-month Jaccard: about 0.8215

2018-2020 evaluator-style forward-return availability smoke diagnostic:

- forward rows: 377,592
- available rows: 376,668
- unavailable rows: 924
- raw availability rate: about 0.9976
- unavailable causes: 500 `final_visible_market_date`, 235 `security_not_observed_next_market_date`, 189 `no_next_security_row`, and 0 `missing_forward_return`
- excluding the final visible date, availability is about 0.9989
- 392 of 424 non-final unavailable rows occur at month-end dates inside the evaluator panel

Main interpretation: missing-held-weight failures are not mainly broad raw data missingness. They are largely induced by building forward returns on the already monthly-universe-filtered panel. If a date-\(t\) holding exits the top-500 at the next month, its date-\(t+1\) row can be absent from `universe_panel` even when the raw eligible panel has the return.

Evaluator implication: membership at date \(t\) should define the signal-date trading universe, but next-day returns for date-\(t\) holdings should be sourced from the eligible raw panel, not from next-month membership. This is now implemented in the Phase 4 sample evaluator as `signal_universe_t_return_source_eligible_t_plus_1_v1`. Generated child strategies still must not read evaluator-only fields such as `fwd_ret`, `fwd_date`, `next_market_date`, or `one_day_forward`.

## Research Uses

- daily equity return panels
- universe screening
- liquidity filters
- event studies
- cross-sectional alpha testing
- portfolio backtests

## Related Pages

- [[permno]]
- [[ticker]]
- [[cusip]]
- [[CCM]]
- [[comp_na_daily_all_annual]]
- [[risk_free_rate]]

## Sources

- [[catalog/csv_data_catalog.md]]
- [[catalog/csv_data_inventory.csv]]
- [[catalog/samples/daily_stock/gago9dveytpx6922.csv]]
- [[catalog/samples/processed/eda/daily_stock_universe_summary.csv]]
- [[catalog/samples/processed/eda/equity_research_eda_notes.csv]]
