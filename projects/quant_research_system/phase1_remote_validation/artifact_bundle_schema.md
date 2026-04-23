---
title: Remote Validation Artifact Bundle Schema
type: project
status: active
updated: 2026-04-23
tags:
  - project
  - artifacts
  - remote-validation
  - schema
---
# Remote Validation Artifact Bundle Schema

## Purpose

Define what a remote validation job must return before its result can support a project decision.

The artifact bundle is not the raw dataset and not a warehouse mirror. It is bounded evidence.

## Storage Pattern

Recommended local path:

```text
artifacts/remote_runs/<YYYYMMDD>_<short_job_id>/
```

The remote machine may use a different scratch path, but the approved local bundle should follow this structure after manual review.

## Required Files

### `run_manifest.yaml`

The exact manifest used for the run.

Must include:

- job id
- environment
- vault git snapshot
- remote research repo git snapshot
- dataset paths
- universe filters
- date splits
- signal definition
- cost model
- expected outputs

### `metrics.json`

Machine-readable headline metrics.

Required top-level keys:

```json
{
  "job_id": "",
  "status": "",
  "date_range": {},
  "universe": {},
  "cost_model": {},
  "train": {},
  "validation": {},
  "test": {},
  "robustness": {},
  "failure_gates": {}
}
```

Required metric fields by split:

- `annualized_return`
- `annualized_volatility`
- `sharpe`
- `max_drawdown`
- `turnover`
- `gross_exposure`
- `net_exposure`
- `mean_daily_n_names`
- `nonfinite_return_count`

### `scorecard.csv`

Tabular summary for human inspection.

Required columns:

- `job_id`
- `split`
- `start_date`
- `end_date`
- `metric`
- `value`
- `unit`
- `notes`

### `diagnostics.csv`

Validation and data-quality diagnostics.

Required columns:

- `job_id`
- `check`
- `status`
- `value`
- `threshold`
- `notes`

Recommended checks:

- row count after filters
- unique `PERMNO` count
- date coverage
- missing return rate
- duplicate `PERMNO` by `DlyCalDt` count
- universe count by month
- turnover distribution
- cost sensitivity
- subperiod stability

### `failure_report.md`

Plain-language account of failures, warnings, and caveats.

Required sections:

- `Summary`
- `Failed Gates`
- `Warnings`
- `Data Caveats`
- `Implementation Caveats`
- `Decision Implications`

### `review.md`

Manual-review wrapper created before local artifact import is treated as approved.

Required sections:

- `Run Identity`
- `Artifact Completeness`
- `Reviewer Decision`
- `Reasons`
- `Required Follow-Up`

## Optional Files

Optional files are encouraged when useful:

- `returns_by_day.csv`
- `portfolio_weights_sample.csv`
- `universe_counts_by_month.csv`
- `turnover_by_day.csv`
- `subperiod_metrics.csv`
- `cost_sensitivity.csv`
- `liquidity_bucket_metrics.csv`
- `exchange_split_metrics.csv`
- `plots/*.png`

Keep optional files compact. Do not import full warehouse-sized outputs into the local vault.

## Pass Conditions

An artifact bundle passes local intake only if:

- all required files exist
- `run_manifest.yaml` matches the reviewed job
- code snapshots are filled with exact commits or explicitly marked dirty
- dataset paths match `catalog/`
- failure gates are reported
- manual review marks the bundle as approved for local import

## Failure Handling

Failed runs are still useful evidence.

If a run fails, keep a compact failure bundle when it reveals something important:

- manifest
- logs trimmed to the relevant error
- failure report
- next-action note

Do not hide failed runs if they changed system understanding.
