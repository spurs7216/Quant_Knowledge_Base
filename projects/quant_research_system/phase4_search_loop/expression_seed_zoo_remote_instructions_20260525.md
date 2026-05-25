---
title: Expression Seed Zoo Remote Instructions 20260525
type: remote_instructions
status: active
updated: 2026-05-25
tags:
  - project
  - phase4
  - remote-run
  - expression-evolution
  - daily-stock
sources:
  - "daily_stock_expression_evolution_v1.md"
  - "current_state.md"
---
# Expression Seed Zoo Remote Instructions 20260525

## Purpose

Run the deterministic daily-stock expression seed-zoo baseline before any Qwen expression-evolution episode.

This run does not call Qwen and does not require vLLM. It should baseline the 24 starter expressions under the repaired Phase 4 evaluator contracts:

- static daily-stock eligibility;
- lagged rolling top-500 universe;
- one-day-forward returns sourced from the eligible raw panel;
- fixed 2011-2025 IS/OS split;
- 2.5 bps default total cost plus cost grid;
- max-weight, net-exposure, coverage, and missing-held gates.

## Preflight

On the remote machine:

1. Pull the latest `origin/main`.
2. Confirm `git status --short` is clean before the run.
3. Confirm the daily_stock CSV path.
4. Do not launch Qwen or vLLM for this run.

## Command

Use the real remote daily_stock CSV path:

```bash
python research/alphaevolve_lite/scripts/run_expression_seed_zoo.py \
  --csv-path /path/to/daily_stock.csv \
  --out-dir artifacts/phase4_alphaevolve/expression_seed_zoo_20260525 \
  --start-date 2011-01-01 \
  --end-date 2025-12-31 \
  --out-sample-start 2023-01-01 \
  --top-n 500 \
  --total-cost-bps 2.5 \
  --cost-grid-bps 0,1,2.5,5,10
```

If the remote CSV path differs from prior runs, record the exact path in the artifact notes.

## Expected Artifacts

Collect the output directory as a zip.

Required files:

- `expression_evaluator_summary.json`
- `expression_rankings.csv`
- `expression_scorecard.csv`
- `expression_cost_sensitivity.csv`
- `expression_interface.md`
- `expression_seed_library.json`
- `universe_membership_monthly.csv`
- `universe_summary.csv`
- `split_manifest.yaml`
- `git_status.txt`
- `git_diff_stat.txt`
- `run_result.json`

## Review Questions

The local reviewer should answer:

- Which seed expressions are `expression_sample_pass`?
- Are any passes driven by sparse coverage, high missing-held weight, one-sided exposure, or high max weight?
- Which mechanisms have positive IS and OS evidence after 2.5 bps?
- Which mechanisms are gross-positive but cost-fragile?
- Which seeds should become parents for the first remote Qwen expression episode?

## Stop Conditions

Stop and return artifacts without improvising if:

- the repository is dirty before the run;
- `HEAD` does not match `origin/main`;
- the daily_stock CSV cannot be found;
- required columns fail `daily_stock_contract_v1`;
- no eligible rows remain after static eligibility;
- the rolling top-500 universe is empty.

Do not run full validation and do not promote any expression from this seed-zoo baseline.
