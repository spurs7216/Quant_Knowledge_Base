---
type: dataset
status: seeded
dataset: risk_free_rate
domain: macro
updated: 2026-04-18
source_count: 4
tags:
  - dataset
  - rates
  - macro
  - excess-returns
sources:
  - "[[catalog/csv_data_catalog.md]]"
  - "[[catalog/csv_data_inventory.csv]]"
  - "[[catalog/samples/risk_free_rate/pql9tfxhavhstowr.csv]]"
  - "[[catalog/samples/processed/eda/risk_free_rate_date_summary.csv]]"
---
# risk_free_rate

## Summary

`risk_free_rate` is the vault's compact mirror of a CRSP-style risk-free rate history. It appears to provide monthly Treasury-based nominal risk-free rates across term labels and is the natural reference layer for excess-return construction.

## What It Is

The catalog describes this as risk-free rate history used for excess-return calculations. The sample shows one monthly observation per rate series with yield measures and duration.

## Canonical Path

- Mirror inventory entry: `risk_free_rate/pql9tfxhavhstowr.csv`
- Sample file: `catalog/samples/risk_free_rate/pql9tfxhavhstowr.csv`

## Business Meaning

This dataset provides the macro cash benchmark needed when converting raw returns into excess returns. It is especially important for:

- monthly excess-return calculations
- benchmarking simple strategies against a cash alternative
- interpreting term labels and Treasury maturity assumptions

## Grain

The working grain appears to be:

- series identifier such as `KYTREASNOX`
- monthly date `MCALDT`

## Primary Keys and Identifiers

Important fields include:

- `KYTREASNOX`
- `TIDXFAM`
- `TTERMTYPE`
- `TTERMLBL`
- `MCALDT`
- `RMTREASNO`
- `RMCRSPID`

## Time Coverage

The mirrored inventory reports:

- `MCALDT`: 2000-01-31 to 2025-11-28

## Important Fields

Useful fields in the sample include:

- `TTERMLBL`
- `MCALDT`
- `TMBIDYTM`
- `TMASKYTM`
- `TMYTM`
- `TMDURATN`

The sample rows shown are labeled as `CRSP Risk Free Rates - 1-Month (Nominal)`.

## Common Joins

- align to monthly strategy returns by `MCALDT`
- use as the risk-free leg when converting returns from raw to excess-return form

This is not a company-level join dataset. It is a macro benchmark layer.

## Known Quality Issues

- This mirror is monthly, not daily. Daily strategies need a documented alignment convention.
- Different term labels may coexist. The intended benchmark series should be chosen explicitly.
- Do not assume that the same risk-free convention applies automatically to every strategy frequency.

## Research Uses

- excess-return construction
- macro context for portfolio evaluation
- validating whether a backtest uses raw or excess returns

## Related Pages

- [[daily_stock]]
- [[ticker]]

## Sources

- [[catalog/csv_data_catalog.md]]
- [[catalog/csv_data_inventory.csv]]
- [[catalog/samples/risk_free_rate/pql9tfxhavhstowr.csv]]
- [[catalog/samples/processed/eda/risk_free_rate_date_summary.csv]]
