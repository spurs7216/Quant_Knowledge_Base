---
title: Phase 2 Task 004 Agent Packet
type: project
status: active
updated: 2026-04-24
tags:
  - project
  - phase2
  - falsification
  - packet
  - operator-controlled
---
# Phase 2 Task 004 Agent Packet

## Instructions To The Answering Agent

Read only the run-local copy of this packet and the evidence files it cites.

Do not use any answer key, scoring file, score report, or local review note.

Do not edit reusable templates in `projects/`.

Write only to the run-local `responses.csv` inside the assigned artifact folder.

For each case, choose exactly one of:

- `reject`
- `revise`
- `proceed`

For each case you must:

- fill one row in `responses.csv`
- provide a non-empty `decision_summary`
- provide a non-empty `evidence_path`
- leave `memo_path` blank unless you actually create a memo under `memos/`

## Case `CASE-ONYX`

Claim under review:

`The current remote validation workflow is strong enough for routine candidate-screening use.`

Evidence:

- [Phase 1 clean artifact review](../../../artifacts/remote_runs/20260423_task001_daily_stock_short_reversal_closure_clean/review.md)
- [Phase 1 clean metrics](../../../artifacts/remote_runs/20260423_task001_daily_stock_short_reversal_closure_clean/metrics.json)
- [Phase 1 clean diagnostics](../../../artifacts/remote_runs/20260423_task001_daily_stock_short_reversal_closure_clean/diagnostics.csv)
- [Phase 1 clean run manifest](../../../artifacts/remote_runs/20260423_task001_daily_stock_short_reversal_closure_clean/run_manifest.yaml)

## Case `CASE-PRISM`

Claim under review:

`The daily long-short reversal candidate should move forward in the research pipeline under the current 2.5 bps friction assumption.`

Evidence:

- [Phase 1 clean metrics](../../../artifacts/remote_runs/20260423_task001_daily_stock_short_reversal_closure_clean/metrics.json)
- [Phase 1 clean review](../../../artifacts/remote_runs/20260423_task001_daily_stock_short_reversal_closure_clean/review.md)
- [Phase 1 cost sensitivity](../../../artifacts/remote_runs/20260423_task001_daily_stock_short_reversal_closure_clean/cost_sensitivity.csv)
- [Phase 1 diagnostics](../../../artifacts/remote_runs/20260423_task001_daily_stock_short_reversal_closure_clean/diagnostics.csv)

## Case `CASE-QUARTZ`

Claim under review:

`The same daily long-short candidate remains strong enough for advancement even if total trading frictions are closer to 10 bps than 2.5 bps.`

Evidence:

- [Phase 1 clean metrics](../../../artifacts/remote_runs/20260423_task001_daily_stock_short_reversal_closure_clean/metrics.json)
- [Phase 1 cost sensitivity](../../../artifacts/remote_runs/20260423_task001_daily_stock_short_reversal_closure_clean/cost_sensitivity.csv)

## Case `CASE-RIDGE`

Claim under review:

`The candidate's recent test path is robust enough to support advancement because several annual slices are strong.`

Evidence:

- [Phase 1 clean metrics](../../../artifacts/remote_runs/20260423_task001_daily_stock_short_reversal_closure_clean/metrics.json)
- [Phase 1 subperiod metrics](../../../artifacts/remote_runs/20260423_task001_daily_stock_short_reversal_closure_clean/subperiod_metrics.csv)

## Case `CASE-SABLE`

Claim under review:

`A ranked-decile proposal without a stated mechanism still deserves further alpha work because observed splits can sometimes look attractive.`

Evidence:

- [Phase 2 metrics](../../../artifacts/remote_runs/20260423_phase2_daily_stock_falsification_suite/metrics.json)
- [Random-rank seed metrics](../../../artifacts/remote_runs/20260423_phase2_daily_stock_falsification_suite/random_rank_seed_metrics.csv)
- [Failure report](../../../artifacts/remote_runs/20260423_phase2_daily_stock_falsification_suite/failure_report.md)

## Case `CASE-TORCH`

Claim under review:

`A very high-performing daily candidate should still move forward even though the ranking field is unusually contemporaneous with the traded return.`

Evidence:

- [Leakage metrics](../../../artifacts/remote_runs/20260423_phase2_daily_stock_falsification_suite/leakage_trap_metrics.csv)
- [Phase 2 diagnostics](../../../artifacts/remote_runs/20260423_phase2_daily_stock_falsification_suite/diagnostics.csv)
- [Failure report](../../../artifacts/remote_runs/20260423_phase2_daily_stock_falsification_suite/failure_report.md)

## Case `CASE-UMBRA`

Claim under review:

`A short-side candidate can advance before any borrow, locate, or broker contract evidence is supplied because backtest edge is the main decision driver.`

Evidence:

- [Implementation feasibility](../../../artifacts/remote_runs/20260423_phase2_daily_stock_falsification_suite/implementation_feasibility.csv)
- [Phase 2 diagnostics](../../../artifacts/remote_runs/20260423_phase2_daily_stock_falsification_suite/diagnostics.csv)
- [Failure report](../../../artifacts/remote_runs/20260423_phase2_daily_stock_falsification_suite/failure_report.md)

## Response Format

Fill the run-local `responses.csv` prepared by the operator and optionally add one markdown memo per case under the run-local `memos/` folder if a longer rationale is needed.
