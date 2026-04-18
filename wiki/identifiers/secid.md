---
type: identifier
status: seeded
updated: 2026-04-18
tags:
  - identifier
  - options
sources:
  - "[[option_forward_price]]"
  - "[[catalog/csv_data_inventory.csv]]"
---
# secid

## Summary

`secid` is the main dataset-native identifier in the mirrored options data.

## Definition

In [[option_forward_price]], `secid` indexes the underlying security representation used inside the options-family dataset.

## Where It Appears

- [[option_forward_price]]
- the mirrored inventory suggests it also appears in `option_volumne`

## What It Joins

- options-family datasets to each other
- possibly option-level observations across multiple derived option tables

## Caveats

- `secid` is not automatically interchangeable with [[permno]] or [[gvkey]].
- If an options-to-equity join is needed, document the mapping path explicitly.
- Exploratory joins through [[ticker]] or [[cusip]] may help, but they should not be treated as equivalent to a documented security map.

## Related Pages

- [[option_forward_price]]
- [[ticker]]
- [[cusip]]
- [[permno]]
- [[gvkey]]

## Sources

- [[option_forward_price]]
- [[catalog/csv_data_inventory.csv]]
