---
title: Task 001 Remote Validation Decision
type: project
status: completed
updated: 2026-04-23
tags:
  - project
  - remote-validation
  - decision
  - daily-stock
sources:
  - "../../../artifacts/remote_runs/20260423_task001_daily_stock_short_reversal/metrics.json"
  - "../../../artifacts/remote_runs/20260423_task001_daily_stock_short_reversal/diagnostics.csv"
  - "../../../artifacts/remote_runs/20260423_task001_daily_stock_short_reversal/failure_report.md"
  - "../../../artifacts/remote_runs/20260423_task001_daily_stock_short_reversal/review.md"
---
# Task 001 Remote Validation Decision

## Run Identity

- job_id: `20260423_task001_daily_stock_short_reversal`
- environment: `remote_validation`
- data file: `/home/b08303004/Desktop/WRDS/data/daily_stock/gago9dveytpx6922.csv`
- artifact bundle: `artifacts/remote_runs/20260423_task001_daily_stock_short_reversal/`
- run status: `completed_with_warnings`
- git commit recorded in bundle: `0981c2840fba336d22575b8b8ccf8f275169bcc3`
- git dirty flag recorded in bundle: `true`

The dirty flag is expected because the validation scaffold was patched locally before the run to close artifact-contract gaps.

## Artifact Intake

The final bundle is accepted as bounded project evidence. It contains:

- `run_manifest.yaml`
- `metrics.json`
- `scorecard.csv`
- `diagnostics.csv`
- `failure_report.md`
- `review.md`
- `subperiod_metrics.csv`
- `cost_sensitivity.csv`
- `exchange_split_metrics.csv`
- `liquidity_bucket_metrics.csv`
- `universe_counts_by_month.csv`
- split return files for train, validation, and test

No raw warehouse data were copied into the vault.

## Gate Outcome

No failure gate failed.

Passing checks include:

- one-trading-day forward return timing
- signal lookahead guard using only `t-1` through `t-5` excess returns
- finite portfolio returns
- turnover cost application
- code snapshot recording

Warnings:

- duplicate `PERMNO` by `DlyCalDt` rows before filters: `11,317`
- duplicate `PERMNO` by `DlyCalDt` rows after universe filters: `2,042`

The implementation reports these duplicates and keeps the first row before signal construction. This is acceptable for an initial workflow validation, but it is not strong enough for a production research method.

## Headline Metrics

All metrics below use the baseline `2.5` bps total trading-cost assumption.

| Split | Annualized return | Annualized vol | Sharpe | Max drawdown | Mean turnover | Beta to `vwretd` |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| train `2000-01-03` to `2012-12-31` | `14.50%` | `9.90%` | `1.464` | `-8.60%` | `0.807` | `0.103` |
| validation `2013-01-01` to `2018-12-31` | `-4.01%` | `5.62%` | `-0.713` | `-27.77%` | `0.764` | `0.117` |
| test `2019-01-01` to `2025-11-28` | `6.48%` | `11.57%` | `0.560` | `-20.47%` | `0.770` | `0.186` |

Cost sensitivity over the full run:

| Total cost bps | Sharpe | Annualized return |
| ---: | ---: | ---: |
| `0.0` | `1.349` | `12.97%` |
| `2.5` | `0.833` | `8.01%` |
| `5.0` | `0.317` | `3.05%` |
| `10.0` | `-0.715` | `-6.87%` |

## Decision

Decision: `revise`.

The remote-validation workflow itself is usable: it ran on the full warehouse file, produced a compact artifact bundle, enforced explicit timing, and returned reviewable evidence. The baseline should not yet be promoted as an alpha candidate. The chronological validation split is negative after costs, the result is highly cost-sensitive, and duplicate security-date rows need a better data-quality policy.

## Required Follow-Up

- Investigate duplicate `PERMNO` by `DlyCalDt` rows and decide whether to keep first row, aggregate, or exclude affected observations.
- Add the random-rank null with the same universe and turnover profile.
- Add borrow-cost and higher-slippage scenarios before short-side interpretation.
- Test whether the effect survives sector, size, and liquidity controls.
- Rerun from a clean committed code snapshot before using this as durable evidence outside this project.
