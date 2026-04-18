---
type: identifier
status: seeded
updated: 2026-04-18
tags:
  - identifier
  - fundamentals
  - compustat
sources:
  - "[[comp_na_daily_all_annual]]"
  - "[[CCM]]"
  - "[[catalog/csv_data_inventory.csv]]"
---
# gvkey

## Summary

`gvkey` is the main Compustat-style entity identifier in this vault. It is the natural key on the fundamentals side of equity research.

## Definition

In the mirrored data, `GVKEY` identifies the firm-side entity in [[CCM]], and `gvkey` identifies the firm record in [[comp_na_daily_all_annual]].

## Where It Appears

- [[comp_na_daily_all_annual]]
- [[CCM]]

## What It Joins

- fundamentals to other Compustat-style firm records
- fundamentals to CRSP-style equity data through [[CCM]] and then [[permno]]

## Caveats

- `gvkey` is not a security identifier.
- A direct join from `gvkey` to [[daily_stock]] is usually not appropriate.
- Use [[CCM]] to bridge to CRSP-style security panels.

## Related Pages

- [[comp_na_daily_all_annual]]
- [[CCM]]
- [[permno]]
- [[cusip]]
- [[ticker]]

## Sources

- [[comp_na_daily_all_annual]]
- [[CCM]]
- [[catalog/csv_data_inventory.csv]]
