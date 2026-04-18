---
type: dataset
status: seeded
dataset: Treasurey_Daily_Time_Series
domain: fixed-income
updated: 2026-04-18
source_count: 5
tags:
  - dataset
  - treasury
  - rates
  - fixed-income
sources:
  - "[[catalog/csv_data_catalog.md]]"
  - "[[catalog/csv_data_inventory.csv]]"
  - "[[catalog/samples/Treasurey_Daily_Time_Series/zrlsjramv99uwk7x.csv]]"
  - "[[catalog/samples/processed/eda/Treasurey_Daily_Time_Series_date_summary.csv]]"
  - "[[catalog/samples/processed/eda/Treasurey_Daily_Time_Series_numeric_summary.csv]]"
---
# Treasurey_Daily_Time_Series

## Summary

`Treasurey_Daily_Time_Series` is the vault's instrument-level Treasury panel. It contains daily bid, ask, nominal price, yield, duration, coupon, and outstanding-value fields for individual Treasury securities, along with issue and maturity dates.

## What It Is

The catalog reports about 638,246 rows and 35 columns in the physical file. The sample shows fields such as:

- instrument identifiers: `KYTREASNO`, `KYCRSPID`, `CRSPID`, `TCUSIP`
- date fields: `TDATDT`, `TMATDT`, `TFCPDT`, `CALDT`
- coupon and issue attributes: `TCOUPRT`, `TNIPPY`, `ITYPE`, `ITAX`
- daily market measures: `TDBID`, `TDASK`, `TDNOMPRC`, `TDYLD`, `TDDURATN`
- size or amount fields: `TDPUBOUT`, `TDTOTOUT`

## Canonical Path

- Mirror inventory entry: `Treasurey_Daily_Time_Series/zrlsjramv99uwk7x.csv`
- Sample file: `catalog/samples/Treasurey_Daily_Time_Series/zrlsjramv99uwk7x.csv`

## Business Meaning

This is the security-level Treasury reference layer behind fixed-income and rates work. It appears suited to instrument-level price, yield, maturity, and duration analysis rather than only benchmark curve summaries.

## Grain

The working grain appears to be an individual Treasury instrument by daily quote date:

- `KYTREASNO` or `CRSPID`
- `CALDT`

## Primary Keys and Identifiers

Important identifiers include:

- `KYTREASNO`
- `KYCRSPID`
- `CRSPID`
- `TCUSIP`

These identifiers are specific to the Treasury or CRSP fixed-income family and are not interchangeable with equity identifiers.

## Time Coverage

The full inventory reports:

- `CALDT`: 2020-01-02 to 2025-11-28
- `TDATDT`: 1990-02-15 to 2025-12-04
- `TFCPDT`: 1990-08-15 to 2026-05-31
- `TMATDT`: 2020-01-07 to 2055-11-15

The compact processed date summary only reaches into 2021 for several fields, which strongly suggests that the EDA output was built from a limited row sample rather than the whole dataset.

## Important Fields

- `KYTREASNO`
- `CRSPID`
- `TCUSIP`
- `TDATDT`
- `TMATDT`
- `CALDT`
- `TCOUPRT`
- `TDBID`
- `TDASK`
- `TDNOMPRC`
- `TDYLD`
- `TDDURATN`

## Common Joins

- `CRSPID` or Treasury identifiers into [[Treasurey_Term_structure]] reference fields such as `RDTREASNO` or `RDCRSPID`, when populated
- monthly aggregation into macro benchmark layers when a security-level Treasury measure is needed before summarization

This is not a company-level security master.

## Known Quality Issues

- The mirror name preserves the current spelling `Treasurey`, and that spelling should be kept in physical path references.
- Several date fields are partially missing in the sample and processed summaries.
- Sample-based EDA outputs understate the apparent full-file date range.
- Treasury-specific identifiers do not align directly with equity research keys such as `[[permno]]` or `[[gvkey]]`.

## Research Uses

- Treasury security-level yield and duration analysis
- mapping benchmark instrument behavior into curve or carry work
- validating fixed-income assumptions used in macro or derivatives research

## Related Pages

- [[Treasurey_Term_structure]]
- [[risk_free_rate]]
- [[Derivatives Markets]]

## Sources

- [[catalog/csv_data_catalog.md]]
- [[catalog/csv_data_inventory.csv]]
- [[catalog/samples/Treasurey_Daily_Time_Series/zrlsjramv99uwk7x.csv]]
- [[catalog/samples/processed/eda/Treasurey_Daily_Time_Series_date_summary.csv]]
- [[catalog/samples/processed/eda/Treasurey_Daily_Time_Series_numeric_summary.csv]]
