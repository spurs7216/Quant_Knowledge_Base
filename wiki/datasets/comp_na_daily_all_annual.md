---
type: dataset
status: seeded
dataset: comp_na_daily_all_annual
domain: fundamentals
updated: 2026-04-18
source_count: 4
tags:
  - dataset
  - fundamentals
  - compustat
  - equities
sources:
  - "[[catalog/csv_data_catalog.md]]"
  - "[[catalog/csv_data_inventory.csv]]"
  - "[[catalog/samples/comp_na_daily_all_annual/sid0ftr1vfrdyxan.csv]]"
  - "[[catalog/samples/processed/eda/comp_na_daily_all_annual_date_summary.csv]]"
---
# comp_na_daily_all_annual

## Summary

`comp_na_daily_all_annual` is the main annual fundamentals dataset currently mirrored in the vault. It looks like a Compustat North America annual export with firm descriptors, identifiers, accounting fields, sector data, and filing-related date fields.

## What It Is

The catalog describes this as a Compustat North America annual fundamentals export. The mirrored inventory reports about 167,644 rows and 980 columns in the physical file.

The sample shows a wide company-year style record that includes:

- identifiers such as `[[gvkey]]`, `tic`, `[[cusip]]`, and `cik`
- company metadata such as `conm`, `busdesc`, sector, SIC, and NAICS
- accounting fields such as `at`, `ceq`, `ni`, `sale`, and price/market-value fields
- filing and publication-related dates such as `datadate`, `fdate`, `pdate`, and `apdedate`

## Canonical Path

- Mirror inventory entry: `comp_na_daily_all_annual/sid0ftr1vfrdyxan.csv`
- Sample file: `catalog/samples/comp_na_daily_all_annual/sid0ftr1vfrdyxan.csv`

## Business Meaning

This is the main annual accounting and firm-descriptor layer for equity research in the vault. It is the natural source for:

- firm characteristics
- annual accounting signals
- valuation ratios
- sector and industry classification

## Grain

The working grain appears to be firm-date at annual reporting frequency, anchored by `[[gvkey]]` and `datadate`.

## Primary Keys and Identifiers

Important identifiers include:

- `[[gvkey]]`
- `tic`
- `[[cusip]]`
- `cik`

For production-quality market-data joins, `[[gvkey]]` should typically be routed through [[CCM]] rather than matched directly on ticker or cusip.

## Time Coverage

The mirrored inventory reports:

- `datadate`: 2010-01-31 to 2025-12-31
- `apdedate`: 2010-01-25 to 2025-12-31
- `fdate`: 2009-11-06 to 2026-01-16
- `pdate`: 2010-02-16 to 2026-01-16
- `ipodate`: 1946-01-14 to 2026-01-13

## Important Fields

The compact EDA summary highlights these fields:

- `gvkey`
- `gsector`
- `sic`
- `at`
- `ceq`
- `ni`
- `sale`
- `mkvalt`
- `prcc_f`

The physical file is much wider than the compact EDA summary, so field selection should be project-specific.

## Common Joins

- `[[gvkey]]` to [[CCM]]
- through [[CCM]] to [[daily_stock]] via `LPERMNO` and `[[permno]]`
- `tic` and `[[cusip]]` for exploratory checks only

## Known Quality Issues

- The physical file is very wide. Many fields will need explicit interpretation before use.
- Several date fields exist and they do not mean the same thing. `datadate`, `fdate`, `pdate`, and `apdedate` should not be conflated.
- The EDA mirror tracks a smaller subset of columns than the physical file. That is a mirror-summary choice, not a contradiction.
- Direct joins on ticker or cusip are riskier than routed joins through [[CCM]].

## Research Uses

- annual accounting signals
- firm characteristic construction
- valuation and quality factors
- industry and sector classification
- accounting-side support for cross-sectional alpha research

## Related Pages

- [[gvkey]]
- [[CCM]]
- [[permno]]
- [[ticker]]
- [[cusip]]
- [[daily_stock]]

## Sources

- [[catalog/csv_data_catalog.md]]
- [[catalog/csv_data_inventory.csv]]
- [[catalog/samples/comp_na_daily_all_annual/sid0ftr1vfrdyxan.csv]]
- [[catalog/samples/processed/eda/comp_na_daily_all_annual_date_summary.csv]]
