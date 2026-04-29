---
title: Phase 4 Dataset Context
type: project
status: active
updated: 2026-04-27
tags:
  - project
  - phase4
  - catalog
  - datasets
sources:
  - "../../../catalog/README.md"
  - "../../../catalog/csv_data_catalog.md"
  - "../../../catalog/csv_data_inventory.csv"
  - "dataset_admission_policy.md"
  - "universe_and_split_policy.md"
---
# Phase 4 Dataset Context

## Purpose

Phase 4 search should know what data exists before proposing features.

The first production loop is daily-stock-only. The broader catalog remains important for later stages, but non-primary datasets must pass admission gates before they enter executable candidates.

## Catalog Profile

The current catalog mirrors:

- CSV file count: `706`
- combined CSV size: about `43.94 GB`
- sample root: `catalog/samples/`
- full warehouse location: remote server
- local vault role: samples, metadata, EDA summaries, and compact evidence artifacts only

## Primary Dataset Families

| Dataset area | Main role | First-loop status |
| --- | --- | --- |
| `daily_stock` | CRSP-like daily equity panel with returns, prices, volume, identifiers, exchange/type fields | active |
| `daily_market_index` | market return/index context | diagnostic/accounting only |
| `risk_free_rate` | risk-free and excess-return context | diagnostic/accounting only |
| `Fama-French` | factor diagnostics | locked until Stage 1 diagnostics |
| `cboe_vix` | volatility-regime context | locked until Stage 1 diagnostics |
| `Treasurey_Term_structure` | rate-regime context | locked until Stage 1 diagnostics |
| `CCM` | CRSP-Compustat bridge | locked until dataset admission |
| `comp_na_daily_all_annual` | annual fundamentals/classifications | locked until dataset admission |
| `ownership_13F` | institutional ownership | locked until dataset admission |
| `option_forward_price` | option pricing/forward panel | locked until Stage 4 |
| `option_volumne` | option volume/open-interest panel | locked until Stage 4 |
| `bond_return`, `reit`, macro panels | cross-asset context | locked until later stages |
| `processed` | EDA/research/backtest outputs | inspiration/calibration only unless source scripts are validated |

## Immediate Equity Uses

Early Phase 4 should prioritize fields already in or directly adjacent to `daily_stock`:

- returns and excess returns;
- lagged market cap for rolling top-500 universe;
- price, volume, dollar volume, shares outstanding;
- exchange and security-type filters;
- native industry/sector group fields such as `SICCD`, `NAICS`, or `ICBIndustry` when present;
- market-adjusted returns using in-file market fields or approved market index data;
- turnover and concentration diagnostics.

This keeps the first loop focused on evaluator reliability before adding fragile point-in-time joins.

## Join Discipline

Any candidate adding a non-primary dataset must declare:

1. dataset source and physical catalog path;
2. join key and grain;
3. timestamp field and availability lag;
4. expected coverage loss;
5. ablation plan versus the same candidate without the added dataset.

If any item is missing, mark the candidate `revise` before remote execution.

## Known Join Paths

```yaml
compustat_join:
  path: "daily_stock.PERMNO -> CCM.LPERMNO -> GVKEY"
  required_checks:
    - LINKDT_LINKENDDT_validity
    - fundamental_datadate_timing
    - reporting_lag
    - coverage_loss
    - ablation

option_join:
  path: "daily_stock CUSIP/ticker -> option secid/date/cusip/ticker"
  status: exploratory_until_mapping_validated
  required_checks:
    - date_aware_identifier_validation
    - contract_to_equity_aggregation
    - coverage_loss
    - liquidity_diagnostics
    - ablation

ownership_join:
  path: "daily_stock CUSIP -> ownership_13F CUSIP"
  required_checks:
    - report_date_lag
    - filing_availability_lag
    - coverage_loss
    - ablation

date_level_join:
  path: "calendar date"
  applies_to:
    - market index
    - VIX
    - Treasury
    - Fama-French
  required_checks:
    - publication_or_availability_timing_when_relevant
```

## Phase 4 Search Implications

### Stage 0

Only daily-stock features and evaluator/accounting data are active.

Allowed examples:

- Kalman innovation reversal;
- rank innovations within native industry groups;
- liquidity-aware weighting using price/volume/dollar volume;
- turnover banding;
- concentration controls;
- market-adjusted return variants.

### Later stages

Later child candidates may add:

- factor or VIX/rate diagnostics;
- Compustat sector/fundamental controls;
- 13F ownership concentration;
- option volume/open-interest pressure;
- event or revision features if source scripts are validated.

These additions are distinct child candidates, not silent mutations.
