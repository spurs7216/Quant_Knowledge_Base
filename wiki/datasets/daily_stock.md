---
type: dataset
status: seeded
dataset: daily_stock
domain: equities
updated: 2026-04-18
source_count: 5
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
