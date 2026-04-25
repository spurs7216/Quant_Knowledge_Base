---
title: Phase 2 Task 003 Agent Packet
type: project
status: active
updated: 2026-04-24
tags:
  - project
  - phase2
  - falsification
  - packet
  - hardened
---
# Phase 2 Task 003 Agent Packet

## Instructions To The Answering Agent

Read only the run-local copy of this packet and the evidence files it cites.

Do not use any answer key, expected-decision table, scoring file, or phase-review note.

Do not edit reusable templates in `projects/`.

Write only to the run-local `responses.csv` inside the assigned artifact folder.

For each case, output exactly one of:

- `reject`
- `revise`
- `proceed`

For each case you must:

- fill one row in `responses.csv`
- provide a non-empty `decision_summary`
- provide a non-empty `evidence_path`
- leave `memo_path` blank unless you actually create a memo under `memos/`

Do not guess the final score.

## Case `CASE-ATLAS`

Name: `Workflow trust under complete artifact evidence`

Question:
Should this validation workflow proceed to routine use as a candidate-screening environment, or is the evidence still too weak to trust it?

Primary evidence:

- [Phase 1 clean artifact review](../../../artifacts/remote_runs/20260423_task001_daily_stock_short_reversal_closure_clean/review.md)
- [Phase 1 clean metrics](../../../artifacts/remote_runs/20260423_task001_daily_stock_short_reversal_closure_clean/metrics.json)
- [Phase 1 clean diagnostics](../../../artifacts/remote_runs/20260423_task001_daily_stock_short_reversal_closure_clean/diagnostics.csv)
- [Phase 1 clean run manifest](../../../artifacts/remote_runs/20260423_task001_daily_stock_short_reversal_closure_clean/run_manifest.yaml)

Focus:

- artifact completeness
- explicit non-leaky timing
- code-snapshot recording
- whether workflow trust can be separated from strategy promotion

## Case `CASE-BIRCH`

Name: `Decile book with no ex ante mechanism`

Question:
Does the evidence justify any further alpha work on this signal?

Primary evidence:

- [Phase 2 metrics](../../../artifacts/remote_runs/20260423_phase2_daily_stock_falsification_suite/metrics.json)
- [Random-rank seed metrics](../../../artifacts/remote_runs/20260423_phase2_daily_stock_falsification_suite/random_rank_seed_metrics.csv)
- [Failure report](../../../artifacts/remote_runs/20260423_phase2_daily_stock_falsification_suite/failure_report.md)

Focus:

- mechanism
- multi-seed behavior
- turnover-cost interaction

## Case `CASE-CINDER`

Name: `Exceptional performance with causal-order violation`

Question:
Does the enormous reported performance matter, or should the idea be stopped on timing grounds?

Primary evidence:

- [Leakage metrics](../../../artifacts/remote_runs/20260423_phase2_daily_stock_falsification_suite/leakage_trap_metrics.csv)
- [Phase 2 diagnostics](../../../artifacts/remote_runs/20260423_phase2_daily_stock_falsification_suite/diagnostics.csv)
- [Failure report](../../../artifacts/remote_runs/20260423_phase2_daily_stock_falsification_suite/failure_report.md)

Focus:

- decision-time versus return-realization timing
- whether headline metrics survive a hard timing failure

## Case `CASE-DRIFT`

Name: `Historical universe built from future-status fields`

Question:
Can this universe definition support historical inference, or is the backtest structurally contaminated?

Primary evidence:

- [Phase 2 diagnostics](../../../artifacts/remote_runs/20260423_phase2_daily_stock_falsification_suite/diagnostics.csv)
- [Failure report](../../../artifacts/remote_runs/20260423_phase2_daily_stock_falsification_suite/failure_report.md)

Focus:

- use of `SecurityActiveFlg`
- use of `SecurityEndDt`
- whether future universe information is being used for earlier dates

## Case `CASE-EMBER`

Name: `Opaque bucket signal with one attractive split`

Question:
Does the attractive split justify further work, or should the idea stop here?

Primary evidence:

- [Identifier-artifact metrics](../../../artifacts/remote_runs/20260423_phase2_daily_stock_falsification_suite/identifier_artifact_metrics.csv)
- [Failure report](../../../artifacts/remote_runs/20260423_phase2_daily_stock_falsification_suite/failure_report.md)

Focus:

- economic mechanism
- whether one favorable split is enough
- sample-composition and disguised-exposure risk

## Case `CASE-FORGE`

Name: `Short-book idea blocked by implementation missingness`

Question:
Should this idea be rejected now, or revised into a more realistic specification before any further work?

Primary evidence:

- [Implementation feasibility](../../../artifacts/remote_runs/20260423_phase2_daily_stock_falsification_suite/implementation_feasibility.csv)
- [Phase 2 diagnostics](../../../artifacts/remote_runs/20260423_phase2_daily_stock_falsification_suite/diagnostics.csv)
- [Failure report](../../../artifacts/remote_runs/20260423_phase2_daily_stock_falsification_suite/failure_report.md)

Focus:

- borrow and locate absence
- low-price and low-dollar-volume concentration
- difference between alpha plausibility and current implementability

## Response Format

Fill the run-local `responses.csv` prepared by the operator and optionally add one markdown memo per case under the run-local `memos/` folder if a longer rationale is needed.
