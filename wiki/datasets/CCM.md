---
type: dataset
status: seeded
dataset: CCM
domain: identifiers
updated: 2026-04-18
source_count: 3
tags:
  - dataset
  - linkage
  - fundamentals
  - equities
sources:
  - "[[catalog/csv_data_catalog.md]]"
  - "[[catalog/csv_data_inventory.csv]]"
  - "[[catalog/samples/CCM/obvhttgmrtddf1tq.csv]]"
---
# CCM

## Summary

`CCM` is the critical bridge dataset between Compustat-style identifiers and CRSP-style identifiers in this vault. It is the main link layer between `[[gvkey]]` and `[[permno]]`.

## What It Is

The catalog describes `CCM` as a WRDS CCM-linked Compustat export. The mirrored file is not just a minimal link table. The sample shows that it includes:

- link fields such as `GVKEY`, `LINKPRIM`, `LINKTYPE`, `LPERMNO`, `LPERMCO`, `LINKDT`, and `LINKENDDT`
- quarterly and yearly accounting fields
- firm descriptors such as `tic`, `cusip`, `conm`, `cik`, and sector information

So this mirror behaves like a link-rich Compustat export rather than a tiny bridge-only file.

## Canonical Path

- Mirror inventory entry: `CCM/obvhttgmrtddf1tq.csv`
- Sample file: `catalog/samples/CCM/obvhttgmrtddf1tq.csv`

## Business Meaning

This dataset is the main bridge for combining market data and fundamentals:

- `[[gvkey]]` identifies the Compustat-side entity
- `LPERMNO` identifies the CRSP-side security
- link dates define when the mapping is valid

Without this bridge, joins between daily market panels and Compustat-style fundamentals are much more error-prone.

## Grain

The exact grain is not a simple one-row-per-entity bridge. The sample suggests a combination of:

- entity linkage
- accounting observation date
- time-valid mapping windows

In practice, joins should be treated as time-aware and link-aware, not as a one-column static map.

## Primary Keys and Identifiers

Important identifiers observed in the mirror include:

- `[[gvkey]]`
- `LPERMNO`
- `LPERMCO`
- `tic`
- `[[cusip]]`
- `cik`

Important link governance fields include:

- `LINKPRIM`
- `LINKTYPE`
- `LINKDT`
- `LINKENDDT`

## Time Coverage

The inventory preview shows link and accounting date fields, but the mirrored inventory does not summarize CCM date coverage as cleanly as some other datasets. The sample clearly includes `datadate`, `LINKDT`, and `LINKENDDT`, so time-aware joining is mandatory.

## Important Fields

The key working fields for linkage are:

- `GVKEY`
- `LPERMNO`
- `LPERMCO`
- `LINKPRIM`
- `LINKTYPE`
- `LINKDT`
- `LINKENDDT`
- `datadate`
- `tic`
- `cusip`

## Common Joins

- `[[gvkey]]` to [[comp_na_daily_all_annual]]
- `LPERMNO` to [[daily_stock]] through `[[permno]]`
- `tic` and `[[cusip]]` for sanity checks only

The safest workflow is usually:

1. identify the Compustat entity via `[[gvkey]]`
2. filter valid links using `LINKDT` and `LINKENDDT`
3. join to CRSP-style daily data through `LPERMNO`

## Known Quality Issues

- This mirror is wide and mixes bridge information with accounting content.
- Multiple link types and link priorities likely exist, so naive joins may duplicate observations.
- Link validity windows matter. Ignoring `LINKDT` and `LINKENDDT` risks look-ahead or stale matches.
- `tic` and `cusip` should not replace the explicit link logic.

## Research Uses

- linking daily returns to fundamentals
- aligning accounting data with market outcomes
- building cross-sectional equity panels
- checking identifier lineage during replication work

## Related Pages

- [[gvkey]]
- [[permno]]
- [[cusip]]
- [[ticker]]
- [[daily_stock]]
- [[comp_na_daily_all_annual]]

## Sources

- [[catalog/csv_data_catalog.md]]
- [[catalog/csv_data_inventory.csv]]
- [[catalog/samples/CCM/obvhttgmrtddf1tq.csv]]
