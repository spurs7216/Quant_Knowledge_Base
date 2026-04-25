---
title: Phase 2 Research Falsification
type: project
status: completed
updated: 2026-04-24
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

Phase 2 started from that capability and added adversarial task design.

Current status:

- `phase2_closed` on 2026-04-24 after Task 004 local review
- Task 001, Task 002, Task 003, and Task 004 are accepted evidence
- the current falsification objective is complete within scope
- next required track: [Strategy-to-IBKR Translation Smoke Test](../execution_translation_smoke_test.md)

## Phase Package

- [task_bank_v0.md](task_bank_v0.md): first visible calibration bank of five null / weak / infeasible tasks.
- [task_bank_v1_scored.md](task_bank_v1_scored.md): first local scored bank that separates the agent packet from the answer key and includes boundary tasks.
- [task_bank_v2_hardened.md](task_bank_v2_hardened.md): hardened bank with neutral case labels and one serious proceed case.
- [task_bank_v3_operator_controlled.md](task_bank_v3_operator_controlled.md): next bank with stronger handoff controls and fresher Phase 1 robustness cases.
- [task_bank_v2_requirements.md](task_bank_v2_requirements.md): hardening requirements for the next scored pass before Phase 2 can close.
- [evaluator_checklist.md](evaluator_checklist.md): required checks before any Phase 2 decision.
- [scorecard_template.csv](scorecard_template.csv): machine-readable scoring shape for falsification tasks.
- [task_001_daily_stock_falsification_suite.md](task_001_daily_stock_falsification_suite.md): first remote-run suite on `daily_stock`.
- [task_001_manifest.yaml](task_001_manifest.yaml): concrete manifest for the first Phase 2 remote run.
- [task_002_scored_falsification_pass.md](task_002_scored_falsification_pass.md): first genuine agent-scored falsification pass using already reviewed evidence.
- [task_003_hardened_scored_falsification_pass.md](task_003_hardened_scored_falsification_pass.md): hardened scored pass with stronger workflow controls and richer decision-class coverage.
- [task_003_local_review.md](task_003_local_review.md): local review of the hardened scored pass.
- [task_004_operator_controlled_scored_pass.md](task_004_operator_controlled_scored_pass.md): operator-controlled scored pass with explicit handoff logging and fresher mixed cases.
- [task_004_agent_packet.md](task_004_agent_packet.md): operator-controlled answering-agent packet used in Task 004.
- [task_004_local_review.md](task_004_local_review.md): closure review for the operator-controlled scored pass.
- [task_003_agent_packet.md](task_003_agent_packet.md): hardened answering-agent packet used in Task 003.
- [answering_agent_protocol.md](answering_agent_protocol.md): exact answering-agent rules.
- [local_operator_scoring_protocol.md](local_operator_scoring_protocol.md): exact operator, scorer, and reviewer split.
- [independence_attestation_template.md](independence_attestation_template.md): required attestation template for hardened scored runs.
- [remote_instructions.md](remote_instructions.md): instructions for a remote agent or human runner.

Executable scaffold:

- [../../../research/research_falsification/phase2_daily_stock_falsification_suite.py](../../../research/research_falsification/phase2_daily_stock_falsification_suite.py)
- [../../../research/research_falsification/score_phase2_falsification_responses.py](../../../research/research_falsification/score_phase2_falsification_responses.py)
- [../../../research/research_falsification/prepare_phase2_scored_run.py](../../../research/research_falsification/prepare_phase2_scored_run.py)

## Task-Bank Status

The first task bank is visible calibration, not a hidden benchmark. It is meant to teach the evaluator and make the failure taxonomy concrete.

The second bank adds scored local decision work using already reviewed evidence. It is still inspectable and still not a hidden benchmark, but it no longer lets the scaffold itself stand in for the agent's decisions.

The hardened bank reduced several earlier weaknesses and added a real `proceed` task. The operator-controlled bank then added the missing prompt trail and fresher robustness cases. The remaining caveats are no longer closure blockers for Phase 2 as currently defined.

## Decision Classes

- `reject`: evidence, design, or implementation constraints make the idea unsuitable for further alpha work.
- `revise`: the idea may be testable, but the current specification has fixable gaps.
- `proceed`: the idea passes falsification checks and deserves stronger validation.

For Phase 2, a false accept means the system chooses `proceed` for a task whose expected decision is `reject`.

False accepts are more serious than false rejects because the system is being trained to avoid wasting expensive validation and search capacity on bad ideas.

## Exit Criteria

Phase 2 closed because the following conditions are now satisfied:

- at least five null / weak / infeasible tasks exist with expected decisions and scoring fields
- the evaluator checklist is used in at least one run
- false accepts are recorded in a scorecard built from actual agent decisions rather than only scaffold defaults
- at least one task includes a statistical null failure
- at least one task includes a leakage or lookahead failure
- at least one task includes an implementation-feasibility failure
- the scored run records an independence-control trail
- the scored bank includes at least one real `proceed` task
- local review records whether the system should proceed to candidate registry work

Remote machines and remote agents can produce evidence and recommendations. Final phase closure remains a local control-plane decision.

## Closure Decision

Phase 2 is closed.

What now supports closure:

- the remote falsification scaffold works on full warehouse data
- the local system can score explicit agent falsification decisions against a separate answer key
- false accepts are visible in real scored passes
- the later runs include `reject`, `revise`, and `proceed`
- Task 004 records the operator prompt and session label directly in the artifact bundle

What still remains imperfect:

- the bank is still small and internal
- the operator-controlled run still logged a narrow non-leaking deviation from strict packet-only access
- this is still not a hidden benchmark

These limits matter for future evaluator maturity, but they no longer block movement to Phase 2B.

## Sources

- [Build Sequence](../build_sequence.md)
- [Environment Contract](../environments.md)
- [Phase 1 Closure Review](../phase1_remote_validation/task_001_closure_decision.md)
- [Task 001 Local Review](task_001_local_review.md)
- [Task 002 Local Review](task_002_local_review.md)
- [Task 003 Local Review](task_003_local_review.md)
- [Task 004 Local Review](task_004_local_review.md)
- [Task 004 Operator Controlled Scored Pass](task_004_operator_controlled_scored_pass.md)
- [Task 003 Hardened Scored Falsification Pass](task_003_hardened_scored_falsification_pass.md)
- [Quant Research Eval Suite Scorecard](../../quant_research_eval/scorecard.md)
