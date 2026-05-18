---
title: daily_stock EDA Full Review 2026-05-18
type: project
status: reviewed
updated: 2026-05-18
tags:
  - project
  - phase4
  - daily-stock
  - data-exploration
  - artifact-review
sources:
  - "../../../artifacts/daily_stock_eda_full_20260518.zip"
  - "daily_stock_data_understanding_plan_20260518.md"
  - "daily_stock_eda_remote_instructions_20260518.md"
  - "daily_stock_contract_v1.md"
  - "../../../wiki/datasets/daily_stock.md"
---
# daily_stock EDA Full Review 2026-05-18

## Artifact

```text
artifacts/daily_stock_eda_full_20260518.zip
```

Notebook report:

```text
projects/quant_research_system/phase4_search_loop/notebooks/daily_stock_eda_full_20260518_report.ipynb
projects/quant_research_system/phase4_search_loop/notebooks/daily_stock_eda_full_20260518_report_executed.ipynb
```

The artifact contains the expected EDA outputs: full summary JSON/markdown, prompt guidance, numeric summaries, categorical counts, daily counts, deterministic sample quantiles, and the 2018-2020 deep top-500 window.

Important reproducibility caveat: this bundle does not include `git_status.txt`, `git_diff_stat.txt`, or a run manifest. The command output is still usable as data evidence, but future data jobs should capture Git state directly in the artifact.

## Executive Read

The EDA gives enough evidence to stop treating `daily_stock` as merely a schema. It shows two distinct statistical objects:

1. the broad eligible daily-stock universe, which is large, noisy, and strongly heavy-tailed;
2. the rolling top-500 evaluation universe, which is much cleaner, nearly always has 500 tradable names per date, and has usable but uneven industry coverage.

The next AlphaEvolve prompts should use this distinction. Raw-scale liquidity, market-cap, volume, and return-level edits are too crude. Good child ideas should use date-level ranks, log transforms, robust z-scores, winsorization, bounded transforms, and group-size-aware industry logic.

## Full-File Profile

The full scan covered:

```yaml
rows_scanned: 49,651,441
date_range: 2000-01-03 to 2025-11-28
trading_dates: 6,517
unique_permnos: 25,139
eligible_rows: 28,302,925
eligible_row_rate: 57.0%
unique_eligible_permnos: 13,342
deterministic_sample_rows: 248,258
```

Fixed eligibility attrition:

| Step | Rows | Raw-row keep rate | Incremental keep rate |
| --- | ---: | ---: | ---: |
| raw rows | 49,651,441 | 100.0% | 100.0% |
| valid date/security | 49,651,441 | 100.0% | 100.0% |
| U.S. incorporated | 43,355,550 | 87.3% | 87.3% |
| common equity/common share | 29,620,281 | 59.7% | 68.3% |
| active regular-way | 29,051,185 | 58.5% | 98.1% |
| major exchange | 29,039,565 | 58.5% | 100.0% |
| positive price/cap | 29,037,331 | 58.5% | 100.0% |
| positive volume | 28,309,392 | 57.0% | 97.5% |
| usable ex-dividend return | 28,302,925 | 57.0% | 100.0% |

Median eligible rows per date are about `4,136`, with 1st and 99th percentile daily eligible counts around `3,721` and `6,440`.

## Distribution Lessons

Full eligible sample tails are heavy:

| Field | Median | q99 | q999 | Max from exact stats |
| --- | ---: | ---: | ---: | ---: |
| `DlyRetx` | 0.0000 | 0.1313 | 0.3699 | 39.7253 |
| `abs_price` | 15.23 | 261.65 | 1,311.48 | 809,350 |
| `DlyVol` | 171,700 | 15,805,310 | 64,377,490 | 5,737,258,000 |
| `DlyPrcVol` | 2,214,735 | 645,493,300 | 2,916,772,000 | 155,183,300,000 |
| `DlyCap` | 413,353 | 94,697,580 | 390,032,700 | 5,032,107,000 |

Use source units for these fields; do not assume the report has converted `DlyCap` or `DlyPrcVol` into economic dollars.

Research implication:

- raw-scale liquidity and market-cap multipliers are unsafe;
- date-level ranks, `log1p`, winsorized z-scores, and bounded transforms should be the default feature primitives;
- return-derived signals should use robust preprocessing even if q999 is not extreme, because exact max returns show severe outliers.

## Top-500 Deep Window

The deep profile used the current sample-evaluation window:

```yaml
window: 2018-01-01 to 2020-12-31
rows_loaded_after_date_filter: 5,735,631
duplicate_permno_date_rows: 1,125
rows_after_static_eligibility_no_return_required: 2,838,434
monthly_universe_rows: 17,500
top_n_months: 35
tradable_universe_rows: 367,092
tradable_dates: 735
tradable_permnos: 686
median_daily_tradable_count: 500
```

The top-500 profile is much cleaner:

| Field | q001 | Median | q99 | q999 |
| --- | ---: | ---: | ---: | ---: |
| `DlyRetx` | -0.1618 | 0.0010 | 0.0701 | 0.1561 |
| `DlyPrcVol` | 3,238,607 | 173,272,400 | 3,692,008,000 | 14,633,680,000 |
| `DlyCap` | 6,203,506 | 21,997,700 | 402,779,800 | 1,529,699,000 |
| `DlyVol` | 283 | 1,958,536 | 45,492,960 | 118,771,600 |
| `abs_price` | 5.65 | 89.98 | 1,317.39 | 308,796.9 |

The full eligible low-price caveat is real, but it is less central inside the current rolling top-500 universe. Top-500 price and liquidity still have large tails, so raw-scale edits remain inappropriate.

## Industry Coverage

The 2018-2020 top-500 universe has:

```yaml
median_sic2_groups_per_date: 53
median_groups_with_at_least_10_names: 15
median_names_per_group: about 3
median_largest_group_share: 13.2%
missing_industry_rate: 0.0%
```

Industry-neutral ranking is plausible, but only with group-size fallback:

- use SIC2 or another approved group only when the per-date group has enough names;
- otherwise fall back to date-level ranking or a shrinkage blend between group-rank and date-rank;
- do not force full neutralization on small groups.

## Universe Churn

The monthly top-500 membership file is complete in the artifact (`17,500` rows, below the `50,000` head cap). Month-to-month churn:

```yaml
mean_entries_per_month: 12.1
median_entries_per_month: 11
max_entries_per_month: 27
median_jaccard_vs_prior_month: 0.957
min_jaccard_vs_prior_month: 0.898
```

Portfolio turnover diagnostics should distinguish signal turnover from universe turnover. A child that appears to increase turnover may be interacting with membership churn, not only signal instability.

## Prompt Decisions

Accept these into prompt memory:

- Never use first-N rows as cross-sectional evidence; use date-window or rolling-universe loaders.
- Prefer date-level ranks, `log1p`, winsorized z-scores, or bounded transforms for `DlyPrcVol`, `DlyCap`, and `DlyVol`.
- Treat raw return levels as outlier-prone; robust preprocessing is justified.
- Allow industry-neutral ranking only with minimum group-size fallback or shrinkage.
- Preserve broad daily activity; few-day books are artifacts, not alpha.
- Separate broad eligible-universe caveats from top-500-universe caveats.

Reject or weaken these prompt ideas:

- raw inverse-volume or raw market-cap scaling;
- liquidity dampening that only reduces gross exposure without a signal thesis;
- full industry neutralization without group-size checks;
- treating low-price caveats as central to top-500 without checking the top-500 distribution.

## Remaining Data Questions

This EDA does not explain the missing-held-weight problem directly. It does not measure:

- next-global-date return availability for held names;
- status, halt, delist, or missing-return flags at the holding date and next date;
- whether missing-held exposure is concentrated by liquidity, price, industry, exchange, or membership exits;
- whether high turnover comes from signal changes or rolling top-500 membership churn.

## Recommended Next Step

Do one focused remote diagnostic before new child generation:

```yaml
next_data_diagnostic:
  purpose: forward_return_availability_and_missing_held_causes
  window: 2018-01-01_to_2020-12-31
  universe: rolling_top500_market_cap_v1
  outputs:
    - next_date_return_availability_by_date.csv
    - missing_forward_return_by_price_liquidity_industry_bucket.csv
    - membership_churn_by_month.csv
    - held_availability_prompt_cards.md
```

After that, wire accepted EDA cards into prompt construction and run a small data-aware controller batch. Do not sample-evaluate children until they are target-matched, novel, final-book-effective, broad-coverage, and not merely de-grossing artifacts.
