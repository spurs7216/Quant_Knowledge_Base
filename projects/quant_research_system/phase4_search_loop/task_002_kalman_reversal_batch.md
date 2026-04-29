---
title: Phase 4 Task 002 Kalman Reversal Evaluator Seed
type: project
status: active
updated: 2026-04-27
tags:
  - project
  - phase4
  - remote-validation
  - kalman
  - evaluator-seed
sources:
  - "task_001_search_design.md"
  - "evaluator_contract.md"
  - "dataset_context.md"
  - "universe_and_split_policy.md"
---
# Phase 4 Task 002 Kalman Reversal Evaluator Seed

## Objective

Implement the first executable remote-validation seed batch for the Kalman innovation reversal family.

This task is explicitly not the AlphaEvolve loop. It is a pre-evolution evaluator seed. It tests whether the evaluator, nulls, concentration metrics, cost sensitivity, and dataset diagnostics are strong enough to score later evolved programs.

## Required Updates From Current Discussion

Task 002 must align with:

```yaml
split_policy: chronological_70_15_15
universe_policy: rolling_top500_market_cap_v1
data_scope: daily_stock_only
cost_grid_bps_total: [0.0, 2.5, 5.0, 10.0]
```

If the existing Task 002 script uses a different universe or split, it should be labeled evaluator calibration only and not treated as the final Phase 4 validation contract.

## Batch Variants

The evaluator seed should include:

1. parent reversal baseline;
2. matched-turnover random-rank null;
3. randomized-signal negative control;
4. Kalman fixed-parameter innovation reversal;
5. Kalman train-only parameter-estimated variant;
6. banded / turnover-controlled variant;
7. native daily-stock industry-neutral variant;
8. liquidity-filter or liquidity-weighted variant.

## Required Artifact Outputs

Task 002 must produce:

```text
run_manifest.yaml
metrics.json
scorecard.csv
diagnostics.csv
evaluator_summary.json
failure_report.md
review.md
cost_sensitivity.csv
subperiod_metrics.csv
liquidity_bucket_metrics.csv
concentration_metrics.csv
universe_summary.csv
split_manifest.yaml
null_distribution.csv
```

## How Task 002 Feeds Later AlphaEvolve

Task 002 outputs should be rendered into prompt-cards:

- parent baseline card;
- null baseline card;
- Kalman seed evidence card;
- failure-mode card;
- cost-fragility card.

These cards become inspirations for Task 004 and later search. They are not evolved children by themselves.

## Acceptance Criteria

Task 002 is complete when:

- evaluator seed batch runs on remote daily-stock data;
- artifacts are compact and syncable;
- null and cost artifacts exist;
- universe and split manifests exist;
- `evaluator_summary.json` can be parsed by the prompt sampler;
- no child candidate is claimed unless generated through Task 004 or later AlphaEvolve mechanics.
