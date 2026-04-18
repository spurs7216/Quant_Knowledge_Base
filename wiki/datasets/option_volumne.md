---
type: dataset
status: seeded
dataset: option_volumne
domain: options
updated: 2026-04-18
source_count: 5
tags:
  - dataset
  - options
  - activity
  - derivatives
sources:
  - "[[catalog/csv_data_catalog.md]]"
  - "[[catalog/csv_data_inventory.csv]]"
  - "[[catalog/samples/option_volumne/ypbvvpsmuiv0jgxq.csv]]"
  - "[[catalog/samples/processed/eda/option_volumne_date_summary.csv]]"
  - "[[catalog/samples/processed/eda/option_volumne_numeric_summary.csv]]"
---
# option_volumne

## Summary

`option_volumne` is the vault's mirrored option activity panel. It appears to track daily option volume and open interest by underlying security and option side, with dataset-native identifier `[[secid]]` plus basic issuer descriptors.

## What It Is

The catalog reports about 73.70 million rows and 13 columns in the physical file. The sample contains:

- `[[secid]]`
- observation `date`
- `cp_flag`
- `index_flag`
- `[[cusip]]`
- `[[ticker]]`
- `volume`
- `open_interest`

Unlike a full option chain file, the sample does not show strike or expiration fields.

## Canonical Path

- Mirror inventory entry: `option_volumne/ypbvvpsmuiv0jgxq.csv`
- Sample file: `catalog/samples/option_volumne/ypbvvpsmuiv0jgxq.csv`

## Business Meaning

This looks like a compact option-activity layer for studying underlying-level option demand, attention, or liquidity. Because strike and expiration are absent from the mirrored sample, it likely behaves more like an aggregated option-side panel than a full contract-surface dataset.

## Grain

The working grain appears to be:

- `[[secid]]`
- `date`
- likely `cp_flag`

Confirm whether additional hidden aggregation dimensions exist on the remote side before using the mirror as if it were a contract-level chain.

## Primary Keys and Identifiers

Important identifiers include:

- `[[secid]]`
- `[[cusip]]`
- `[[ticker]]`
- `cp_flag`

`[[secid]]` is the safest dataset-native key inside the options family.

## Time Coverage

The mirrored inventory and processed date summary report:

- `date`: 2000-01-03 to 2025-08-29

## Important Fields

- `secid`
- `date`
- `cp_flag`
- `index_flag`
- `cusip`
- `ticker`
- `exchange_d`
- `class`
- `issue_type`
- `industry_group`
- `volume`
- `open_interest`

## Common Joins

- `[[secid]]` to [[option_forward_price]], with caution because the two mirrors likely operate at different grains
- `[[ticker]]` or `[[cusip]]` into equity data for exploratory analysis

If the research question is contract-specific, this mirror is probably too aggregated on its own.

## Known Quality Issues

- The directory spelling `option_volumne` should be preserved when referencing physical paths.
- Sample rows show missing `cp_flag` values, so call/put classification needs validation.
- No strike or expiration fields appear in the mirrored sample, which limits chain-level analysis.
- `[[ticker]]` and `[[cusip]]` remain unstable exploratory keys rather than primary identifiers.

## Research Uses

- option attention or activity screens
- put-call imbalance style features, if `cp_flag` is reliable
- linking option demand signals to underlying equity panels
- open-interest based event studies

## Related Pages

- [[secid]]
- [[ticker]]
- [[cusip]]
- [[option_forward_price]]
- [[Derivatives Markets]]

## Sources

- [[catalog/csv_data_catalog.md]]
- [[catalog/csv_data_inventory.csv]]
- [[catalog/samples/option_volumne/ypbvvpsmuiv0jgxq.csv]]
- [[catalog/samples/processed/eda/option_volumne_date_summary.csv]]
- [[catalog/samples/processed/eda/option_volumne_numeric_summary.csv]]
