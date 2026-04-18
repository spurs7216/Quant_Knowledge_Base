---
type: identifier
status: seeded
updated: 2026-04-18
tags:
  - identifier
  - securities
sources:
  - "[[daily_stock]]"
  - "[[comp_na_daily_all_annual]]"
  - "[[option_forward_price]]"
  - "[[CCM]]"
---
# cusip

## Summary

`cusip` is a widely used security identifier family in the vault, but it needs careful handling because format and time behavior differ across datasets.

## Definition

The mirrored data shows multiple cusip-style fields:

- `CUSIP` and `CUSIP9` in [[daily_stock]]
- `cusip` in [[CCM]]
- `cusip` in [[comp_na_daily_all_annual]]
- `cusip` in [[option_forward_price]]

Some forms appear to be 8-character and some 9-character variants.

## Where It Appears

- [[daily_stock]]
- [[CCM]]
- [[comp_na_daily_all_annual]]
- [[option_forward_price]]

## What It Joins

`cusip` can be useful for:

- exploratory matching
- issuer-level sanity checks
- mapping across source systems when a stronger bridge is not yet documented

## Caveats

- `cusip` can change over time.
- Different datasets may store 8-character versus 9-character forms.
- `cusip` is useful, but it should not automatically replace [[permno]], [[gvkey]], or [[secid]].
- Time-aware and format-aware normalization is often required.

## Related Pages

- [[daily_stock]]
- [[CCM]]
- [[comp_na_daily_all_annual]]
- [[option_forward_price]]
- [[permno]]
- [[gvkey]]
- [[secid]]
- [[ticker]]

## Sources

- [[daily_stock]]
- [[CCM]]
- [[comp_na_daily_all_annual]]
- [[option_forward_price]]
