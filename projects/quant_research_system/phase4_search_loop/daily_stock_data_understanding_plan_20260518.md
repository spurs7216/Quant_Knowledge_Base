---
title: Phase 4 daily_stock Data Understanding Plan 2026-05-18
type: project
status: reviewed
updated: 2026-05-18
tags:
  - project
  - phase4
  - alphaevolve
  - daily-stock
  - data-exploration
sources:
  - "current_state.md"
  - "daily_stock_contract_v1.md"
  - "dataset_context.md"
  - "remote_csv_execution_policy.md"
  - "daily_stock_eda_full_review_20260518.md"
  - "daily_stock_forward_coverage_remote_instructions_20260518.md"
  - "../../../catalog/README.md"
  - "../../../wiki/datasets/daily_stock.md"
---
# Phase 4 daily_stock Data Understanding Plan 2026-05-18

## Purpose

Pause new child generation and build an empirical map of `daily_stock` before another attempt017 search round.

The controller now rejects many syntactic, semantic, duplicate, no-op, occupied-cell, and execution-neutral failures. The remaining bottleneck is not mainly Qwen mechanics. The children do not yet have enough empirical knowledge about the data surface: distributions, missingness, liquidity skew, industry coverage, universe breadth, and which transformations are natural for `daily_stock`.

This stage should turn the dataset from a field-name contract into prompt-usable research memory.

## Current Evidence Gap

We already know:

- the frozen field names in [daily_stock_contract_v1.md](daily_stock_contract_v1.md);
- the fixed static eligibility filters;
- the rolling top-500 market-cap universe policy;
- that first-N-row samples are not representative because the CSV can be security-sorted;
- that sample-evaluated children have repeatedly produced implementation-shape changes without robust parent-relative alpha improvement.

We do not yet know enough about:

- full-file missingness by required field;
- exact eligibility attrition through each universe filter;
- return, price, volume, dollar-volume, and market-cap tail behavior;
- how many names survive per date after fixed filters;
- how industry groups are distributed inside the rolling top-500 universe;
- whether liquidity and market-cap features should be raw, log, rank, winsorized, or group-relative;
- which data-cleaning or feature-normalization moves should be promoted into prompt data cards.

## Implemented First Slice

Code added:

```text
research/alphaevolve_lite/daily_stock_eda.py
research/alphaevolve_lite/scripts/profile_daily_stock_data.py
research/alphaevolve_lite/tests/test_daily_stock_eda.py
```

The profiler is deliberately separate from strategy evaluation. It writes data-understanding artifacts only. It does not score alpha, does not use held-out test data, does not call Qwen, and does not mutate any candidate program.

## What The Profiler Measures

Full chunked scan:

- contract-column validation;
- raw row count and date-filtered row count;
- unique `PERMNO` and eligible `PERMNO` counts;
- date coverage and daily row counts;
- stepwise fixed-eligibility attrition;
- numeric moments and extrema for returns, prices, volume, dollar volume, market cap, shares outstanding, and derived log variables;
- deterministic sample quantiles for heavy-tailed fields;
- categorical counts for exchange, security type, share type, trading status, conditional type, U.S. incorporation, return/price/cap/volume flags, and industry code.

Optional deep date-window profile:

- duplicate-policy diagnostics;
- fixed eligibility without requiring same-day return for universe formation;
- rolling top-N market-cap universe membership;
- daily top-N tradable breadth;
- per-date return and liquidity cross-sectional summaries;
- SIC2 industry group coverage;
- transform-profile quantiles for return and liquidity primitives.

Prompt-facing outputs:

- `daily_stock_prompt_guidance.json`;
- `prompt_data_cards.md`;
- generated rules for transforms, coverage caveats, and candidate feature primitives.

## Stage Plan

### D1. Local smoke

Run the profiler on the tiny local catalog sample to prove command wiring and artifact writing.

Status: implemented and passed on 2026-05-18.

### D2. Remote full-file empirical map

Run one remote full-file chunked profile with a deep top-500 window matching the current sample-evaluation period.

Primary output target:

```text
artifacts/phase4_alphaevolve/daily_stock_eda_full_20260518
```

This should be reviewed locally before any new child-generation batch.

Status: completed. Reviewed in [daily_stock_eda_full_review_20260518.md](daily_stock_eda_full_review_20260518.md).

### D3. Artifact review and prompt-card freeze

After the artifact returns:

1. inspect `daily_stock_eda_summary.json`;
2. inspect `eligible_numeric_summary.csv`, `sample_quantiles.csv`, and `eligible_sample_quantiles.csv`;
3. inspect `deep_window/deep_window_summary.json`;
4. inspect `deep_window/industry_coverage_profile.csv`;
5. decide which transform rules are real enough to enter prompt context;
6. update `dataset_context.md`, `current_state.md`, and the durable `wiki/datasets/daily_stock.md` note with only artifact-supported claims.

Status: partially completed. The review, notebook, `current_state.md`, and `wiki/datasets/daily_stock.md` now carry artifact-supported data lessons. Prompt-builder integration is intentionally deferred until the forward-return availability diagnostic is run.

### D4. Forward-return availability and whole-timeline top-500 coverage

The first EDA artifact does not explain missing-held-weight failures. Add a second,
separate diagnostic before prompt integration:

- scan rolling top-500 coverage over the whole available timeline;
- report daily, monthly, and PERMNO-level coverage for the selected universe;
- report month-to-month top-500 membership churn;
- compute evaluator-style one-day-forward return availability in the 2018-2020 sample window;
- attribute unavailable held rows to structural causes such as `security_not_observed_next_market_date`, `no_next_security_row`, `missing_forward_return`, or `final_visible_market_date`;
- break forward availability down by price, dollar volume, market cap, industry, exchange, and next-month membership status.

Status: implemented locally. Remote handoff is [daily_stock_forward_coverage_remote_instructions_20260518.md](daily_stock_forward_coverage_remote_instructions_20260518.md). The review notebook is [notebooks/daily_stock_forward_coverage_20260518_report.ipynb](notebooks/daily_stock_forward_coverage_20260518_report.ipynb).

### D5. Prompt integration

Only after review, wire selected data cards into prompt construction. The prompt sampler should receive compact rules such as:

- use date-level ranks or log transforms for highly skewed liquidity fields;
- use winsorized or ranked return-derived signals when tail behavior is extreme;
- use industry-neutral ranking only with group-size fallbacks;
- treat sparse few-day books as coverage artifacts;
- avoid raw first-N sample intuition.

### D6. Resume evolution

The next child-generation round should use the new data cards. It should prefer research moves grounded in the empirical map:

- robust cross-sectional transforms;
- liquidity-relative rather than raw-liquidity rules;
- industry or sector neutralization only where group coverage supports it;
- missingness-aware signal construction, using only fields available at strategy time;
- coverage-preserving portfolio controls.

## Acceptance Criteria

The data-understanding milestone is complete when:

- the remote full-file EDA command runs from a reproducible GitHub commit;
- compact artifacts return to the vault;
- the artifact records row counts, eligibility attrition, numeric distributions, daily breadth, and deep-window top-500 diagnostics;
- at least one project review note states which data lessons are accepted, rejected, or still uncertain;
- prompt data cards are updated from artifact evidence, not assumptions;
- the forward-return availability diagnostic has either explained missing-held-weight causes or clearly stated that they are not concentrated in observable buckets;
- no child-generation or validation decision used the test set.

## Non-Goals

This stage does not:

- promote attempt017 or any child;
- run Qwen;
- run sample evaluation;
- run full validation;
- add non-daily-stock datasets;
- change the fixed universe or split policy;
- treat descriptive statistics as alpha evidence.

## Open Questions For Review

- Are `DlyPrcVol` and `DlyCap` so skewed that raw-scale child edits should be discouraged? Yes. Use log, rank, winsorized, or bounded transforms.
- How often do low-price or low-liquidity names survive the fixed filters and rolling top-500 universe? They survive the broad fixed filters, but the 2018-2020 top-500 universe is much cleaner. Low-price risk is a broad-universe caveat, not the dominant top-500 issue.
- Does SIC2 have enough daily group breadth for industry-neutral ranking without fragile small-group behavior? Partly. There are many SIC2 groups, but median names per group are low; use minimum group-size fallback or shrinkage.
- Do return flags or missing-return fields explain missing-held-weight failures? Not yet answered. This needs a forward-return availability diagnostic.
- Does the top-500 universe have stable enough daily breadth across regimes to support broad long/short books? Yes in the 2018-2020 deep window: median daily tradable count is 500.
- Which transform primitives should become active prompt rules, and which should remain caveats? Active: log/rank/winsorized transforms for liquidity/size and group-size-aware industry logic. Caveat: exact missing-held causes remain unknown.

## Related Notes

- [daily_stock_eda_remote_instructions_20260518.md](daily_stock_eda_remote_instructions_20260518.md)
- [daily_stock_forward_coverage_remote_instructions_20260518.md](daily_stock_forward_coverage_remote_instructions_20260518.md)
- [daily_stock_contract_v1.md](daily_stock_contract_v1.md)
- [dataset_context.md](dataset_context.md)
- [remote_csv_execution_policy.md](remote_csv_execution_policy.md)
- [current_state.md](current_state.md)
