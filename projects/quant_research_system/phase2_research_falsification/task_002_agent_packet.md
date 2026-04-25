---
title: Phase 2 Task 002 Agent Packet
type: project
status: active
updated: 2026-04-24
tags:
  - project
  - phase2
  - falsification
  - packet
---
# Phase 2 Task 002 Agent Packet

## Instructions To The Answering Agent

Read only the run-local copy of this packet and the evidence files it cites.

Do not use any answer key, expected-decision table, or scoring file.

Do not edit reusable templates in `projects/`.

Write only to the run-local `responses.csv` inside the assigned artifact folder.

For each task, output exactly one of:

- `reject`
- `revise`
- `proceed`

Your response must tie the decision to the cited evidence and should distinguish:

- statistical defects
- leakage or timing defects
- implementation defects
- reasons the idea might still deserve repair instead of outright rejection

## Task `SFT-001`

Name: `Daily-stock short reversal baseline`

Question:
Should this idea move directly into candidate-registry style promotion, or does it still need revision first?

Primary evidence:

- [Task 001 Phase 1 Closure Review](../phase1_remote_validation/task_001_closure_decision.md)
- [Phase 1 metrics.json](../../../artifacts/remote_runs/20260423_task001_daily_stock_short_reversal_closure_clean/metrics.json)
- [Phase 1 diagnostics.csv](../../../artifacts/remote_runs/20260423_task001_daily_stock_short_reversal_closure_clean/diagnostics.csv)

Focus:

- split stability
- unresolved data-quality issues
- robustness gaps
- whether the right next action is promotion, repair, or rejection

## Task `SFT-002`

Name: `Random-rank null with realistic turnover cost`

Question:
Does the evidence justify any further alpha work on this signal?

Primary evidence:

- [Phase 2 metrics.json](../../../artifacts/remote_runs/20260423_phase2_daily_stock_falsification_suite/metrics.json)
- [Random-rank seed metrics](../../../artifacts/remote_runs/20260423_phase2_daily_stock_falsification_suite/random_rank_seed_metrics.csv)
- [Failure report](../../../artifacts/remote_runs/20260423_phase2_daily_stock_falsification_suite/failure_report.md)

Focus:

- ex ante mechanism
- multiple-seed behavior
- turnover-cost interaction

## Task `SFT-003`

Name: `Same-day return leakage trap`

Question:
Does the enormous reported performance matter, or should the idea be stopped on timing grounds?

Primary evidence:

- [Leakage metrics](../../../artifacts/remote_runs/20260423_phase2_daily_stock_falsification_suite/leakage_trap_metrics.csv)
- [Phase 2 diagnostics.csv](../../../artifacts/remote_runs/20260423_phase2_daily_stock_falsification_suite/diagnostics.csv)
- [Failure report](../../../artifacts/remote_runs/20260423_phase2_daily_stock_falsification_suite/failure_report.md)

Focus:

- decision-time versus return-realization timing
- whether headline metrics are admissible after a hard leakage failure

## Task `SFT-004`

Name: `Future survivorship universe trap`

Question:
Can this universe definition support historical inference, or is the backtest structurally contaminated?

Primary evidence:

- [Phase 2 diagnostics.csv](../../../artifacts/remote_runs/20260423_phase2_daily_stock_falsification_suite/diagnostics.csv)
- [Failure report](../../../artifacts/remote_runs/20260423_phase2_daily_stock_falsification_suite/failure_report.md)

Focus:

- use of `SecurityActiveFlg`
- use of `SecurityEndDt`
- whether future universe information is being used for earlier dates

## Task `SFT-005`

Name: `Static identifier artifact with positive validation split`

Question:
Does the positive validation split justify further work, or is this still an identifier artifact that should be stopped?

Primary evidence:

- [Identifier-artifact metrics](../../../artifacts/remote_runs/20260423_phase2_daily_stock_falsification_suite/identifier_artifact_metrics.csv)
- [Failure report](../../../artifacts/remote_runs/20260423_phase2_daily_stock_falsification_suite/failure_report.md)

Focus:

- economic mechanism
- whether a positive split is enough without a coherent state variable
- sample-composition and disguised-exposure risk

## Task `SFT-006`

Name: `Microcap shorting implementation trap`

Question:
Should this idea be rejected now, or revised into a more realistic specification before any further work?

Primary evidence:

- [Implementation feasibility](../../../artifacts/remote_runs/20260423_phase2_daily_stock_falsification_suite/implementation_feasibility.csv)
- [Phase 2 diagnostics.csv](../../../artifacts/remote_runs/20260423_phase2_daily_stock_falsification_suite/diagnostics.csv)
- [Failure report](../../../artifacts/remote_runs/20260423_phase2_daily_stock_falsification_suite/failure_report.md)

Focus:

- borrow and locate absence
- microcap and low-dollar-volume concentration
- difference between alpha plausibility and implementability

## Response Format

Fill the run-local `responses.csv` prepared by the operator and optionally add one markdown memo per task under the run-local `memos/` folder if a longer rationale is needed.
