---
type: dataset
status: seeded
dataset: Treasurey_Term_structure
domain: fixed-income
updated: 2026-04-18
source_count: 5
tags:
  - dataset
  - treasury
  - term-structure
  - fixed-income
sources:
  - "[[catalog/csv_data_catalog.md]]"
  - "[[catalog/csv_data_inventory.csv]]"
  - "[[catalog/samples/Treasurey_Term_structure/sxg8q1bnq7qho4km.csv]]"
  - "[[catalog/samples/processed/eda/Treasurey_Term_structure_date_summary.csv]]"
  - "[[catalog/samples/processed/eda/Treasurey_Term_structure_numeric_summary.csv]]"
---
# Treasurey_Term_structure

## Summary

`Treasurey_Term_structure` is the vault's cross-maturity Treasury benchmark panel. It appears to organize yield-curve and forward-rate information by standardized term labels rather than by individual Treasury security.

## What It Is

The catalog reports about 168,438 rows and 32 columns in the physical file. The sample header includes:

- series keys: `KYTREASNOX`, `TIDXFAM`, `TTERMTYPE`, `TTERMLBL`
- calendar date: `CALDT`
- linked instrument references: `RDTREASNO`, `RDCRSPID`
- rate and return fields: `TDBID`, `TDASK`, `TDNOMPRC`, `TDBIDYLD`, `TDASKYLD`, `TDYLD`
- duration and forward or holding-period fields: `TDDURATN`, `TDBIDFWD1`, `TDAVEFWD1`, `TDBIDHLD1`

The first few sampled rows are label-like and mostly empty, while the numeric summary confirms that populated daily observations exist for many rate fields.

## Canonical Path

- Mirror inventory entry: `Treasurey_Term_structure/sxg8q1bnq7qho4km.csv`
- Sample file: `catalog/samples/Treasurey_Term_structure/sxg8q1bnq7qho4km.csv`

## Business Meaning

This is the standardized term-structure layer for curve analysis. It looks suitable for benchmark series such as risk-free rates, fixed-term indexes, yield-curve slope or carry features, and duration-aware macro controls.

## Grain

The working grain appears to be:

- term-structure series identifier such as `KYTREASNOX` or `TTERMLBL`
- `CALDT`

## Primary Keys and Identifiers

Important identifiers include:

- `KYTREASNOX`
- `TIDXFAM`
- `TTERMTYPE`
- `TTERMLBL`
- `CALDT`
- `RDTREASNO`
- `RDCRSPID`

Unlike equity panels, this dataset is indexed by rate-family or maturity buckets rather than by issuer.

## Time Coverage

The mirrored inventory and processed date summary report:

- `CALDT`: 2000-01-03 to 2025-11-28

## Important Fields

- `KYTREASNOX`
- `TIDXFAM`
- `TTERMTYPE`
- `TTERMLBL`
- `CALDT`
- `TDYLD`
- `TDDURATN`
- `TDBIDFWD1`
- `TDAVEFWD1`
- `TDBIDHLD1`

The sample labels indicate families such as `RISKFREE` and `FIXEDTERM`, including series like `CRSP Risk Free Rates - 1-Month (Nominal)`.

## Common Joins

- aggregate or align to [[risk_free_rate]] by term label and date frequency
- use `RDTREASNO` or `RDCRSPID` to trace back to [[Treasurey_Daily_Time_Series]] when the benchmark series is linked to an instrument-level source

## Known Quality Issues

- The mirror name preserves the current spelling `Treasurey`.
- The sampled first rows look like sparse label definitions rather than typical populated observations, so row previews can be misleading.
- Linked instrument references are not guaranteed populated for every row.
- This is a curve-level benchmark panel, not a direct substitute for a security-level Treasury file.

## Research Uses

- yield-curve features and slope measures
- risk-free and fixed-term benchmark construction
- duration-aware macro controls
- linking benchmark curve data into derivatives and fixed-income research

## Related Pages

- [[Treasurey_Daily_Time_Series]]
- [[risk_free_rate]]
- [[Derivatives Markets]]

## Sources

- [[catalog/csv_data_catalog.md]]
- [[catalog/csv_data_inventory.csv]]
- [[catalog/samples/Treasurey_Term_structure/sxg8q1bnq7qho4km.csv]]
- [[catalog/samples/processed/eda/Treasurey_Term_structure_date_summary.csv]]
- [[catalog/samples/processed/eda/Treasurey_Term_structure_numeric_summary.csv]]
