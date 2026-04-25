---
title: Phase 2 Task Bank V3 Operator Controlled
type: project
status: active
updated: 2026-04-24
tags:
  - project
  - phase2
  - task-bank
  - operator-controlled
  - scored
---
# Phase 2 Task Bank V3 Operator Controlled

## Purpose

This bank is the next scored pass after Task 003.

Its role is to tighten the remaining integrity gaps:

- stronger operator handoff logging
- less answer-shaped packet wording
- partially fresher cases rather than only replaying the most visible earlier traps

## Design

The bank mixes:

- one workflow-level `proceed` case
- two boundary `revise` cases
- four hard `reject` cases

It also mixes evidence sources:

- fresh Phase 1 robustness artifacts for three cases
- carry-forward Phase 2 gate artifacts for leakage, null discipline, and implementation realism

## Case Table

| Case ID | Case name | Canonical class | Canonical decision | Evidence spine |
| --- | --- | --- | --- | --- |
| `CASE-ONYX` | Remote artifact bundle for screening workflow | `hard_proceed` | `proceed` | Phase 1 clean closure artifact bundle |
| `CASE-PRISM` | Daily long-short candidate under base friction assumptions | `boundary` | `revise` | Phase 1 split metrics plus cost sensitivity |
| `CASE-QUARTZ` | Deployment claim under higher friction assumption | `hard_reject` | `reject` | Phase 1 cost sensitivity |
| `CASE-RIDGE` | Test-path claim built from selected annual slices | `hard_reject` | `reject` | Phase 1 subperiod metrics |
| `CASE-SABLE` | Ranked decile proposal without mechanism note | `hard_reject` | `reject` | Phase 2 random-rank evidence |
| `CASE-TORCH` | Daily candidate with signal-timing ambiguity | `hard_reject` | `reject` | Phase 2 leakage evidence |
| `CASE-UMBRA` | Short-side candidate with missing market-access evidence | `boundary` | `revise` | Phase 2 implementation-feasibility evidence |

## Why This Bank Is Better

- the operator log records the exact handoff prompt and session label
- three cases are built from Phase 1 robustness artifacts that were not the center of Task 003
- the packet uses generic decision requests instead of highly guided focus bullets
- the proceed case remains about workflow trust, not accidental alpha promotion

## Caveat

This is still not a hidden benchmark.

The point is to improve operator control and reduce answer-shaping enough that a final local review can decide whether Phase 2 should close.

## Related Notes

- [Phase 2 Task 003 Hardened Scored Falsification Pass](task_003_hardened_scored_falsification_pass.md)
- [Phase 2 Task 003 Local Review](task_003_local_review.md)
