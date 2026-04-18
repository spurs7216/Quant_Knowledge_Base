---
type: dataset
status: seeded
dataset: option_forward_price
domain: options
updated: 2026-04-18
source_count: 4
tags:
  - dataset
  - options
  - derivatives
sources:
  - "[[catalog/csv_data_catalog.md]]"
  - "[[catalog/csv_data_inventory.csv]]"
  - "[[catalog/samples/option_forward_price/albvtzgilyy7iwg5.csv]]"
  - "[[catalog/samples/processed/eda/option_forward_price_date_summary.csv]]"
---
# option_forward_price

## Summary

`option_forward_price` is the main mirrored option forward-price panel in the vault. It is an options-side dataset keyed around `[[secid]]`, observation date, and expiration, with a forward-price measure and underlying-security descriptors.

## What It Is

The catalog describes it as an option-level forward or pricing panel. The mirrored inventory reports about 123.30 million rows and 14 columns in the physical file.

The sample shows that each row contains:

- `[[secid]]`
- observation `date`
- `expiration`
- `ForwardPrice`
- underlying descriptors such as `[[cusip]]`, `[[ticker]]`, `sic`, `exchange_d`, and issuer fields

## Canonical Path

- Mirror inventory entry: `option_forward_price/albvtzgilyy7iwg5.csv`
- Sample file: `catalog/samples/option_forward_price/albvtzgilyy7iwg5.csv`

## Business Meaning

This dataset appears to describe underlying forward prices across option expirations. It is useful for options research where the underlying forward term structure matters more than just spot price.

## Grain

The working grain appears to be:

- `[[secid]]`
- `date`
- `expiration`

## Primary Keys and Identifiers

Important identifiers include:

- `[[secid]]`
- `[[cusip]]`
- `[[ticker]]`

`[[secid]]` is the safest dataset-native working key inside the options family.

## Time Coverage

The mirrored inventory and EDA summary report:

- `date`: 2000-01-03 to 2000-12-29

Important caution:

The currently mirrored view reports only year-2000 coverage. Before using this dataset as if it spans the full sample history of the vault, verify whether the remote server contains additional years or whether this particular file is intentionally year-2000-limited.

## Important Fields

Useful fields in the sample include:

- `secid`
- `date`
- `expiration`
- `AMSettlement`
- `ForwardPrice`
- `cusip`
- `ticker`
- `exchange_d`
- `industry_group`
- `issuer`

## Common Joins

- `[[secid]]` to other options-family datasets such as `option_volumne`
- `[[ticker]]` or `[[cusip]]` for exploratory mapping to equity data

Production joins from options data into equity panels should be treated carefully. `[[ticker]]` and `[[cusip]]` can help with exploration, but they are not guaranteed to be stable enough to replace a documented security map.

## Known Quality Issues

- The mirrored date range currently appears very short relative to the dataset size and the rest of the vault. Validate coverage on the remote side before relying on this file alone.
- The compact EDA summary tracks only a subset of the 14 physical columns.
- The dataset-native identifier is `[[secid]]`, which is not interchangeable with `[[permno]]` or `[[gvkey]]`.

## Research Uses

- option term-structure work
- forward-price based option analytics
- linking options information to equity signals, with careful identifier handling
- event and expiration alignment

## Related Pages

- [[secid]]
- [[ticker]]
- [[cusip]]
- [[daily_stock]]

## Sources

- [[catalog/csv_data_catalog.md]]
- [[catalog/csv_data_inventory.csv]]
- [[catalog/samples/option_forward_price/albvtzgilyy7iwg5.csv]]
- [[catalog/samples/processed/eda/option_forward_price_date_summary.csv]]
