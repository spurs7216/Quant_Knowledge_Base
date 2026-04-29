---
title: Phase 4 Universe and Split Policy
type: project
status: active
updated: 2026-04-29
tags:
  - project
  - phase4
  - universe
  - splits
  - daily-stock
sources:
  - "README.md"
  - "dataset_context.md"
  - "csv_data_catalog.md"
---
# Phase 4 Universe and Split Policy

## Purpose

This note fixes the first Phase 4 universe and split policy.

The policy must be defined before candidate generation. Candidates may not change it inside evolve blocks.

Implementation must first verify the remote `daily_stock` schema. Do not hardcode field names from memory. Use the generated field mapping from:

```text
artifacts/phase4_alphaevolve/data_schema/daily_stock_field_mapping.yaml
```

## Final Decision

```yaml
split_policy:
  type: chronological_by_cleaned_trading_dates
  proportions: [0.70, 0.15, 0.15]
  unit: cleaned_unique_trading_dates
  construct_after_duplicate_policy: true
  construct_after_basic_validity_checks: true
  test_set_locked_until_branch_freeze: true

universe_policy:
  name: rolling_top500_market_cap
  recompute_frequency: monthly
  formation_date: last_trading_day_of_prior_month
  effective_period: next_calendar_month_trading_days
  ranking_variable: lagged_market_cap
  data_scope: daily_stock_only
```

## Why Rolling Top 500

A static top-500 list is not acceptable because it uses future membership information. The top-500 universe must change through time.

The first implementation uses a monthly rolling universe because:

- daily recomputation creates unnecessary churn and cost noise;
- monthly membership is easier to audit;
- it matches common institutional universe-construction practice;
- it still avoids full-period survivorship and future-membership leakage.

## Market-Cap Definition

Use only information observable at or before the formation date.

```python
lagged_market_cap = abs(DlyPrc) * ShrOut
```

Notes:

- If `ShrOut` is in thousands, the unit scale does not affect ranking.
- Use absolute price because CRSP-style prices can be signed.
- A candidate may not change this definition inside an evolve block.
- Field names are placeholders until the remote schema report confirms them.
- If a verified market-cap field exists in the dataset, it can replace this definition only through a manifest update, not through evolution.
- If market cap cannot be verified, `remote_full_validation` must fail closed. `remote_sample_eval` may use a declared dollar-volume top-500 fallback only as an early diagnostic, not for promotion.

## Monthly Rolling Top-500 Procedure

For each calendar month `M`:

1. Find the last trading date `F` before the first trading date of `M`.
2. Apply static eligibility filters on `F`.
3. Compute `lagged_market_cap` on `F`.
4. Rank eligible names descending by `lagged_market_cap`.
5. Select top 500 names.
6. Use this membership for all trading dates in `M`.
7. If a selected name disappears mid-month, do not forward-fill returns. Treat missing tradable data according to the evaluator's missing-return policy.

## Static Eligibility Filters

The first implementation should use conservative filters:

```yaml
eligibility_filters:
  common_equity_only: true
  major_us_exchange_only: true
  positive_shares_outstanding: true
  nonmissing_price: true
  nonmissing_market_cap: true
  nonmissing_next_return_required_for_pnl: true
```

The exact field names must be resolved from the `daily_stock` schema. Candidate programs may consume the already-built universe mask but may not alter the universe-construction code.

## Timing Convention

For a signal computed at date `t`:

```text
formation information: available on or before t
positions: formed after signal date t
return earned: next available trading-day return, t+1
```

No smoothing, filtering, ranking, or universe selection may use observations after `t`.

## Split Construction

The split is computed once from cleaned sorted unique trading dates after duplicate policy, basic validity checks, and date parsing, not per candidate.

Construction order:

```text
1. load daily_stock
2. parse and clean date field
3. apply duplicate policy at identifier-date grain
4. apply basic validity checks
5. derive cleaned trading-date calendar
6. sort trading dates
7. cut chronological 70/15/15 split by trading-date count
8. compute rolling universe membership inside each split using only prior/available information
```

Persist as:

```yaml
split_id: daily_stock_top500_chrono_70_15_15_v1
split_unit: cleaned_unique_trading_dates
train_start: <computed>
train_end: <computed>
validation_start: <computed>
validation_end: <computed>
test_start: <computed>
test_end: <computed>
```

Do not manually choose dates after seeing results. The exact boundaries should be computed by the script and recorded in the artifact bundle.

## Test-Set Rules

```yaml
test_set_policy:
  accessible_during_search: false
  unlock_requires_branch_freeze: true
  mutation_after_test_evaluation_allowed: false
  prompt_sampler_may_read_test_metrics: false
  test_metrics_storage: candidate_registry_only_after_unlock
```

The program database may store that a branch has test evaluation, but child sampling from test-informed results is forbidden.

## Universe Artifact Requirements

Every remote validation run must emit:

```text
universe_summary.csv
universe_membership_monthly.parquet or universe_membership_monthly.csv
split_manifest.yaml
```

`split_manifest.yaml` must include cleaned-calendar counts, duplicate-policy metadata, split date ranges, universe policy, and the declaration that no full-period static top-500 list was used.

Minimum `universe_summary.csv` fields:

```yaml
fields:
  - month
  - formation_date
  - eligible_count
  - selected_count
  - median_market_cap
  - min_selected_market_cap
  - max_selected_market_cap
  - missing_price_count
  - missing_shrout_count
  - dropped_midmonth_count
```

If Parquet dependencies are unavailable, CSV fallback is acceptable.

## Candidate Restrictions

Candidates may not change:

- split proportions
- split dates
- universe recompute frequency
- top-500 count
- market-cap field
- static eligibility filters
- return timing
- missing-return policy

## Missing-Return Policy

Do not forward-fill returns. Do not silently drop held names. Do not silently renormalize surviving names without reporting the missing-held weight.

Default policy:

```yaml
missing_return_policy:
  default: fail_if_held_return_missing
  no_forward_fill_returns: true
  no_silent_drop_held_names: true
  no_silent_survivor_renormalization: true
  terminal_return_recovery_requires_verified_field: true
  max_allowed_missing_held_weight_remote_full_validation: 0.0001
```

If a verified delisting or terminal-return field exists, the evaluator may apply it once on the terminal date and then set the name's weight to zero until the next rebalance. Otherwise, held names with missing next returns are an evaluator failure except below the tiny configured tolerance.

A future explicit project task may revise universe policy, but generated children may not.

## Smoke Tests For Universe Logic

Implement tests that assert:

- no date in validation or test is used to construct training-time universe membership;
- monthly membership for month `M` uses only prior-month-end information;
- top-500 membership changes over time;
- delisted or disappearing names are not silently removed from historical membership before disappearance;
- total selected names per month is at most 500;
- candidate code cannot edit universe builder files.
