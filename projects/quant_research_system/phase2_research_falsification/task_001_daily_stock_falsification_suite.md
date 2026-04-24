---
title: Phase 2 Task 001 Daily-Stock Falsification Suite
type: project
status: draft
updated: 2026-04-23
tags:
  - project
  - phase2
  - remote-validation
  - falsification
  - daily-stock
sources:
  - "../../../catalog/samples/daily_stock/gago9dveytpx6922.csv"
  - "../phase1_remote_validation/task_001_closure_decision.md"
---
# Phase 2 Task 001 Daily-Stock Falsification Suite

## Objective

Run the first Phase 2 visible falsification suite on the remote `daily_stock` warehouse file.

The suite tests whether the system can reject:

- random cross-sectional signals
- same-day leakage
- future-survivorship filters
- static identifier artifacts
- non-implementable microcap short books

## Candidate Artifact

Executable script:

- [../../../research/research_falsification/phase2_daily_stock_falsification_suite.py](../../../research/research_falsification/phase2_daily_stock_falsification_suite.py)

The script is not an alpha generator. It is an evaluator scaffold that produces compact evidence for the visible task bank.

## Dataset

- remote path: `/home/b08303004/Desktop/WRDS/data/daily_stock/gago9dveytpx6922.csv`
- local catalog sample: `catalog/samples/daily_stock/gago9dveytpx6922.csv`
- expected rows: `49,651,441`
- date range from catalog: `2000-01-03` to `2025-11-28`

## Expected Outputs

Remote artifact root:

```text
artifacts/remote_runs/20260423_phase2_daily_stock_falsification_suite/
```

Required files:

- `run_manifest.yaml`
- `metrics.json`
- `task_scorecard.csv`
- `diagnostics.csv`
- `failure_report.md`
- `review.md`
- `random_rank_seed_metrics.csv`
- `random_rank_detailed_metrics.csv`
- `identifier_artifact_metrics.csv`
- `leakage_trap_metrics.csv`
- `implementation_feasibility.csv`

## Evaluation Logic

The suite should produce an automated expected-decision scorecard. The official Phase 2 score still requires comparing those expected decisions against the agent's independent decisions.

The key quantity is the false accept count:

$$
N_{\text{false accept}} =
\sum_{j=1}^{J} \mathbf{1}
\{\text{expected}_j = \text{reject},\ \text{agent}_j = \text{proceed}\}.
$$

Visible calibration runs can use the automated expected-decision fields. Later hidden benchmark runs should hide the expected decision from the answering agent.

## Acceptance Standard

This task passes as a Phase 2 scaffold if:

- all required files are produced
- every task has an expected decision
- hard-gate failures are visible
- statistical and implementation failures are separated
- no raw warehouse data are copied into the vault

This task does not close Phase 2 by itself.

## Related Notes

- [Phase 2 README](README.md)
- [Task Bank v0](task_bank_v0.md)
- [Evaluator Checklist](evaluator_checklist.md)
