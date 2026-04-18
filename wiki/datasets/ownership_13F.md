---
type: dataset
status: seeded
dataset: ownership_13F
domain: ownership
updated: 2026-04-18
source_count: 5
tags:
  - dataset
  - ownership
  - holdings
  - institutions
sources:
  - "[[catalog/csv_data_catalog.md]]"
  - "[[catalog/csv_data_inventory.csv]]"
  - "[[catalog/samples/ownership_13F/cpq2naym3nlhqsla.csv]]"
  - "[[catalog/samples/processed/eda/ownership_13F_date_summary.csv]]"
  - "[[catalog/samples/processed/eda/ownership_13F_numeric_summary.csv]]"
---
# ownership_13F

## Summary

`ownership_13F` is the vault's mirrored institutional-ownership panel. The sample suggests that it is not raw manager-holding line data, but a security-level summary layer of 13F ownership statistics such as concentration, number of owners, and top-holder shares.

## What It Is

The catalog reports about 81,036 rows and 18 columns in the physical file. The sample rows are security-date summaries with fields such as:

- security descriptors: `cusip`, `stkname`, `ticker`, `exchcd`, `stkcd`
- price and shares outstanding: `prc`, `shrout`
- institutional ownership metrics: `Top5InstOwn`, `Top10InstOwn`, `NumInstOwners`, `InstOwn`, `InstOwn_HHI`, `InstOwn_Perc`

## Canonical Path

- Mirror inventory entry: `ownership_13F/cpq2naym3nlhqsla.csv`
- Sample file: `catalog/samples/ownership_13F/cpq2naym3nlhqsla.csv`

## Business Meaning

This dataset looks suitable for crowding, ownership concentration, blockholder presence, and institutional-participation overlays. It is closer to a quarterly security-level ownership summary than to a full filing-detail database.

## Grain

The working grain appears to be a security by report date:

- `rdate`
- `[[cusip]]`
- often also `[[ticker]]`

Before production use, confirm whether any duplicate share-class or exchange cases violate simple uniqueness.

## Primary Keys and Identifiers

Important identifiers and descriptors include:

- `rdate`
- `[[cusip]]`
- `[[ticker]]`
- `stkname`

There is no direct `[[permno]]` or `[[gvkey]]` in the mirrored sample.

## Time Coverage

There is a coverage discrepancy that should be treated carefully:

- top-level catalog area summary: `rdate` from 2024-06-30 to 2025-06-30
- processed EDA sample summary: `rdate` from 2024-06-30 to 2025-03-31

The most likely explanation is that the compact EDA summary was built from a row-limited sample rather than from the full file.

## Important Fields

- `rdate`
- `cusip`
- `ticker`
- `prc`
- `shrout`
- `Top5InstOwn`
- `Top10InstOwn`
- `NumInstBlockOwners`
- `InstBlockOwn`
- `NumInstOwners`
- `MaxInstOwn`
- `InstOwn`
- `InstOwn_HHI`
- `InstOwn_Perc`

## Common Joins

- `[[cusip]]` or `[[ticker]]` into equity panels such as [[daily_stock]], with date-aware caution
- security-level ownership overlays for fundamentals or price panels after an explicit mapping step

Because the dataset lacks `[[permno]]` and `[[gvkey]]`, production joins should not be treated as trivial.

## Known Quality Issues

- The mirror looks aggregated rather than raw-manager-level, so filer-level analyses likely require another source.
- `[[ticker]]` is not guaranteed complete or stable.
- `InstOwn_Perc` has extreme values in the numeric summary, so units and outliers need verification before direct interpretation.
- The full-file date range and the sample-based EDA date range do not fully agree.

## Research Uses

- ownership concentration and crowding
- blockholder and institutional participation screens
- security-level ownership overlays for alpha or risk models
- studying whether institutional presence correlates with liquidity or returns

## Related Pages

- [[cusip]]
- [[ticker]]
- [[daily_stock]]
- [[CCM]]
- [[Panel Data]]

## Sources

- [[catalog/csv_data_catalog.md]]
- [[catalog/csv_data_inventory.csv]]
- [[catalog/samples/ownership_13F/cpq2naym3nlhqsla.csv]]
- [[catalog/samples/processed/eda/ownership_13F_date_summary.csv]]
- [[catalog/samples/processed/eda/ownership_13F_numeric_summary.csv]]
