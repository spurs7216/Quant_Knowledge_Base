---
type: identifier
status: seeded
updated: 2026-04-18
tags:
  - identifier
  - market-data
sources:
  - "[[daily_stock]]"
  - "[[comp_na_daily_all_annual]]"
  - "[[option_forward_price]]"
  - "[[catalog/samples/processed/eda/daily_stock_universe_summary.csv]]"
---
# ticker

## Summary

`ticker` is the most human-readable identifier in the vault, but it is not the most stable one.

## Definition

`ticker` is the exchange-facing trading symbol or symbol-like short code used for human recognition. It appears across equities, fundamentals, options, and ownership data.

## Where It Appears

- [[daily_stock]] as `Ticker`
- [[comp_na_daily_all_annual]] as `tic`
- [[option_forward_price]] as `ticker`
- mirrored ownership data

## What It Is Good For

- exploration
- visual inspection
- sanity checks
- quick linking across notes and charts

## What It Is Not Good For

- sole production-quality joins across long time spans
- handling corporate actions and identifier drift without supporting logic
- replacing [[permno]], [[gvkey]], or [[secid]]

## Caveats

- Tickers change over time.
- Tickers can be reused.
- Multiple share classes can complicate ticker usage.
- The daily equity mirror explicitly has missing ticker rows, so ticker coverage is not complete even within a single dataset.

## Related Pages

- [[daily_stock]]
- [[comp_na_daily_all_annual]]
- [[option_forward_price]]
- [[permno]]
- [[gvkey]]
- [[cusip]]

## Sources

- [[daily_stock]]
- [[comp_na_daily_all_annual]]
- [[option_forward_price]]
- [[catalog/samples/processed/eda/daily_stock_universe_summary.csv]]
