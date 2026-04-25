---
title: Phase 2 Task Bank V2 Hardened
type: project
status: active
updated: 2026-04-24
tags:
  - project
  - phase2
  - task-bank
  - hardened
  - scored
---
# Phase 2 Task Bank V2 Hardened

## Purpose

This is the first hardened scored bank for Phase 2.

It exists to address the remaining caveats from Task 002:

- stronger answer-key independence controls
- less-visible task presentation
- at least one serious `proceed` case

## Design

The case names are neutral and do not expose the expected decision directly.

The bank contains:

- one serious `proceed` case
- four hard `reject` cases
- one boundary `revise` case

## Case Table

| Case ID | Case name | Canonical class | Canonical decision | Evidence spine |
| --- | --- | --- | --- | --- |
| `CASE-ATLAS` | Workflow trust under complete artifact evidence | `hard_proceed` | `proceed` | Phase 1 clean closure artifact bundle |
| `CASE-BIRCH` | Decile book with no ex ante mechanism | `hard_reject` | `reject` | Phase 2 random-rank calibration evidence |
| `CASE-CINDER` | Exceptional performance with causal-order violation | `hard_reject` | `reject` | Phase 2 leakage evidence |
| `CASE-DRIFT` | Historical universe built from future-status fields | `hard_reject` | `reject` | Phase 2 survivorship diagnostics |
| `CASE-EMBER` | Opaque bucket signal with one attractive split | `hard_reject` | `reject` | Phase 2 identifier-artifact evidence |
| `CASE-FORGE` | Short-book idea blocked by implementation missingness | `boundary` | `revise` | Phase 2 implementation-feasibility evidence |

## Case Intent

### `CASE-ATLAS`

This is the serious `proceed` case.

The object being evaluated is not the reversal alpha itself. It is the trustworthiness of the remote validation workflow as a candidate-screening environment.

Proceed means:

- the workflow should be used for future validation work
- the baseline strategy inside that workflow is still allowed to remain `revise`

### `CASE-FORGE`

This remains a boundary task.

The core idea may still deserve repair or reframing, but it must not proceed as an implementation-ready alpha claim.

## Why This Bank Is Harder

- the answering agent gets a run-local packet rather than the reusable project files
- the operator records independence controls
- the proceed class can no longer be ignored
- the case labels are more neutral than the earlier explicit trap names

## Related Notes

- [Task Bank V2 Requirements](task_bank_v2_requirements.md)
- [Task 003 Hardened Scored Falsification Pass](task_003_hardened_scored_falsification_pass.md)
