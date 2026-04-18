---
type: identifier
status: seeded
updated: 2026-04-18
tags:
  - identifier
  - equities
  - crsp
sources:
  - "[[daily_stock]]"
  - "[[CCM]]"
  - "[[catalog/csv_data_inventory.csv]]"
---
# permno

## Summary

`permno` is the main CRSP-style security identifier in this vault. It is the safest working key for security-level daily equity work.

## Definition

In the mirrored equity data, `PERMNO` identifies the security-level observation in [[daily_stock]]. In the link layer, the same concept appears as `LPERMNO` in [[CCM]].

## Where It Appears

- [[daily_stock]] as `PERMNO`
- [[CCM]] as `LPERMNO`
- many mirrored processed research outputs in `catalog/samples/processed/research/`

## What It Joins

- market data to market data inside daily equity workflows
- daily equity data to fundamentals through [[CCM]]
- research outputs and backtest selections back to the underlying security panel

## Caveats

- `permno` is security-level, not firm-level.
- One firm can have multiple securities, so `permno` is not interchangeable with `permco`.
- Do not replace `permno` joins with [[ticker]] joins when doing production-quality research.

## Related Pages

- [[daily_stock]]
- [[CCM]]
- [[gvkey]]
- [[ticker]]
- [[cusip]]

## Sources

- [[daily_stock]]
- [[CCM]]
- [[catalog/csv_data_inventory.csv]]
