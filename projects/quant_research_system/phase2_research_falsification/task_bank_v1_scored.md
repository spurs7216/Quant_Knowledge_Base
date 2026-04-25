---
title: Phase 2 Falsification Task Bank v1 Scored
type: project
status: active
updated: 2026-04-24
tags:
  - project
  - phase2
  - task-bank
  - falsification
  - scored
---
# Phase 2 Falsification Task Bank v1 Scored

## Purpose

This bank is the first genuine scored falsification pass after the visible calibration suite.

The goal is to score independent agent decisions, not the scaffold's built-in expected rejections.

This bank is still Phase 2 work. It is not a hidden benchmark and it is not an alpha-search environment.

## Design Changes From v0

- use existing reviewed evidence instead of asking the remote script to fill in agent decisions
- separate the agent packet from the answer key
- include boundary tasks where `revise` is the canonical answer so the agent cannot maximize score by blindly rejecting everything
- compute both strict accuracy and tolerant boundary accuracy

## Task Table

| Task ID | Name | Evidence source | Canonical decision | Task class | Why it matters |
| --- | --- | --- | --- | --- | --- |
| `SFT-001` | Daily-stock short reversal baseline | Phase 1 closure review | `revise` | boundary | tests whether the agent can avoid both naive promotion and over-harsh rejection |
| `SFT-002` | Random-rank null with realistic turnover cost | Phase 2 calibration artifacts | `reject` | hard reject | tests null discipline against a no-mechanism signal |
| `SFT-003` | Same-day return leakage trap | Phase 2 calibration artifacts | `reject` | hard reject | tests whether timing gates override attractive metrics |
| `SFT-004` | Future survivorship universe trap | Phase 2 calibration artifacts | `reject` | hard reject | tests whether universe leakage is caught explicitly |
| `SFT-005` | Static identifier artifact with positive validation split | Phase 2 calibration artifacts | `reject` | hard reject | tests whether the agent can reject a superficially tempting but unjustified signal |
| `SFT-006` | Microcap shorting implementation trap | Phase 2 calibration artifacts | `revise` | boundary | tests whether the agent can separate alpha plausibility from broker-facing infeasibility |

## Scoring Philosophy

The bank uses two layers of scoring:

1. strict decision scoring
   Compare the agent decision to the canonical expected decision.
2. tolerant boundary scoring
   For boundary tasks, allow a small set of acceptable answers when the evidence truly supports more than one conservative judgment.

This avoids fake precision while still preventing "always reject" behavior from scoring perfectly.

## Why There Is No `proceed` Task Yet

Independent judgment: the first scored falsification pass should still bias toward null discipline and conservative boundary handling.

Adding a `proceed` task too early would risk teaching the evaluator to look for reasons to advance weak candidates before the boundary between calibration and real research scoring is stable.

A mixed `reject` / `revise` / `proceed` bank should come later, likely at the transition from late Phase 2 to Phase 3, after the scored falsification workflow itself is stable.

## Exit Implication

A good result on this bank would mean:

- the system can make independent falsification decisions from reviewed evidence
- false accepts are no longer hidden inside scaffold code
- boundary cases are handled with some nuance

It would still not, by itself, justify search-loop work unless the local review agrees that the decision memos are serious and inspectable.

## Related Notes

- [README](README.md)
- [Task Bank v0](task_bank_v0.md)
- [Task 001 Local Review](task_001_local_review.md)
- [Task 002 Scored Falsification Pass](task_002_scored_falsification_pass.md)
