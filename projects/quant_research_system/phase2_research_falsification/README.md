---
title: Phase 2 Research Falsification
type: project
status: active
updated: 2026-04-23
tags:
  - project
  - phase2
  - research-falsification
  - quant
---
# Phase 2 Research Falsification

## Purpose

Phase 2 tests whether the research system can reject bad ideas before candidate search scales them.

The goal is not to produce a new alpha. The goal is to make false-positive control explicit:

- reject null or randomized signals
- reject lookahead and leakage traps even when the backtest looks attractive
- reject identifier artifacts without an economic or statistical mechanism
- reject strategies that are not implementable under plausible trading, borrow, capacity, or broker constraints
- record failure reasons so rejected ideas remain useful evidence

## Entry State

Phase 1 is closed as an engineering milestone. The remote-validation path can run on the remote warehouse and return a compact artifact bundle.

Phase 2 starts from that capability and adds adversarial task design.

## Phase Package

- [task_bank_v0.md](task_bank_v0.md): first visible calibration bank of five null / weak / infeasible tasks.
- [evaluator_checklist.md](evaluator_checklist.md): required checks before any Phase 2 decision.
- [scorecard_template.csv](scorecard_template.csv): machine-readable scoring shape for falsification tasks.
- [task_001_daily_stock_falsification_suite.md](task_001_daily_stock_falsification_suite.md): first remote-run suite on `daily_stock`.
- [task_001_manifest.yaml](task_001_manifest.yaml): concrete manifest for the first Phase 2 remote run.
- [remote_instructions.md](remote_instructions.md): instructions for a remote agent or human runner.

Executable scaffold:

- [../../../research/research_falsification/phase2_daily_stock_falsification_suite.py](../../../research/research_falsification/phase2_daily_stock_falsification_suite.py)

## Task-Bank Status

The first task bank is visible calibration, not a hidden benchmark. It is meant to teach the evaluator and make the failure taxonomy concrete.

Later Phase 2 work can create hidden tasks once the visible bank and scoring template are stable.

## Decision Classes

- `reject`: evidence, design, or implementation constraints make the idea unsuitable for further alpha work.
- `revise`: the idea may be testable, but the current specification has fixable gaps.
- `proceed`: the idea passes falsification checks and deserves stronger validation.

For Phase 2, a false accept means the system chooses `proceed` for a task whose expected decision is `reject`.

False accepts are more serious than false rejects because the system is being trained to avoid wasting expensive validation and search capacity on bad ideas.

## Exit Criteria

Phase 2 can close only when:

- at least five null / weak / infeasible tasks exist with expected decisions and scoring fields
- the evaluator checklist is used in at least one run
- false accepts are recorded in a scorecard
- at least one task includes a statistical null failure
- at least one task includes a leakage or lookahead failure
- at least one task includes an implementation-feasibility failure
- local review records whether the system should proceed to candidate registry work

Remote machines and remote agents can produce evidence and recommendations. Final phase closure remains a local control-plane decision.

## Sources

- [Build Sequence](../build_sequence.md)
- [Environment Contract](../environments.md)
- [Phase 1 Closure Review](../phase1_remote_validation/task_001_closure_decision.md)
- [Quant Research Eval Suite Scorecard](../../quant_research_eval/scorecard.md)
