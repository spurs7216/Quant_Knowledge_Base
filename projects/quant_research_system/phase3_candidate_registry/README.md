---
title: Phase 3 Candidate Registry
type: project
status: active
updated: 2026-04-25
tags:
  - project
  - phase3
  - candidate-registry
  - quant
---
# Phase 3 Candidate Registry

## Purpose

Phase 3 creates the candidate lineage layer before any AlphaEvolve-style search loop begins.

The registry exists so that proposed factors, strategies, implementation translations, constructors, and later search variants do not disappear into chat history. A candidate must be inspectable by id, parent, artifact type, evidence, decision, and current status.

This phase is not a search loop and not a promotion step. It is the control-plane memory needed before search can safely scale.

## Entry State

Phase 3 starts after:

- Phase 1 closed the remote validation workflow as an engineering milestone.
- Phase 2 closed the falsification workflow with zero false accepts in the hardened and operator-controlled passes.
- Phase 2B closed the first static no-send implementation translation smoke test.

The short-horizon reversal baseline remains `revise`, not promoted alpha. It is still useful as the first registry seed because it has full remote evidence, closure review, and a child implementation-translation artifact.

## Package

- [candidate_registry_schema.md](candidate_registry_schema.md): required registry fields, allowed values, and status-transition rules.
- [candidate_registry.csv](candidate_registry.csv): current registry table.
- [candidate_event_log.csv](candidate_event_log.csv): append-only candidate event history.
- [candidate_manifest.template.yaml](candidate_manifest.template.yaml): manifest template for adding a new candidate.
- [candidate_status_update.template.yaml](candidate_status_update.template.yaml): manifest template for updating an existing candidate after review.
- [task_001_seed_registry.md](task_001_seed_registry.md): first Phase 3 task and seed rationale.
- [task_002_manifest_registration.md](task_002_manifest_registration.md): manifest-driven registration test.
- [task_003_evaluation_intake.md](task_003_evaluation_intake.md): candidate status-update and event-intake test.
- [task_004_remote_validation_handoff.md](task_004_remote_validation_handoff.md): executable remote-validation handoff for the duplicate-policy revision.
- [task_005_remote_execution_packet.md](task_005_remote_execution_packet.md): local-to-remote execution packet and artifact intake checklist.

Executable support:

- [../../../research/candidate_registry/validate_candidate_registry.py](../../../research/candidate_registry/validate_candidate_registry.py)
- [../../../research/candidate_registry/register_candidate.py](../../../research/candidate_registry/register_candidate.py)
- [../../../research/candidate_registry/update_candidate_status.py](../../../research/candidate_registry/update_candidate_status.py)

## Registry Discipline

Every candidate row should preserve:

- a stable `candidate_id`
- a `parent_id` when the candidate derives from another candidate
- a `root_candidate_id` for family-level lineage
- the artifact type and current status
- the code or artifact path that defines the candidate
- the evaluator result and local decision
- the evidence path that justifies the status

The registry should stay compact. Detailed backtest results, order intents, scorecards, and diagnostics belong in `artifacts/` and project notes. The registry links to them.

## Status Vocabulary

Allowed current statuses:

- `active`: still under investigation or awaiting a revised run.
- `rejected`: should not receive more candidate-search budget unless reopened explicitly.
- `promoted`: passed the current research gate and is eligible for a stronger downstream environment.
- `paper-test`: frozen and approved for a later paper-testing workflow.
- `superseded`: replaced by a child candidate or corrected artifact.

Allowed local decisions:

- `pending`
- `reject`
- `revise`
- `proceed`
- `paper-test`
- `record-only`

`pending` is for candidates that have been registered before evaluator-backed review. `record-only` is for registry or implementation-support artifacts that preserve lineage but are not themselves alpha candidates.

## Current Seed State

The registry currently contains four entries:

| Candidate | Role | Current decision | Current status |
| --- | --- | --- | --- |
| `CAND-20260423-001` | Daily stock short-horizon reversal baseline | `revise` | `active` |
| `CAND-20260424-001` | Representative no-send implementation translation child | `record-only` | `active` |
| `CAND-20260425-001` | Duplicate-policy revision planning child | `record-only` | `superseded` |
| `CAND-20260425-002` | Executable duplicate-policy revision handoff | `pending` | `active` |

The first entry is a research candidate. The second entry is a lineage-preserving implementation artifact derived from the first entry. The third entry proved that a planning candidate can be registered and later superseded without deleting history. The fourth entry is the executable remote-validation handoff for the same duplicate-policy revision, now with a remote execution packet ready.

Current validation state:

```text
validated_candidates: 4
validated_events: 10
```

## Exit Criteria

Phase 3 can close when:

- candidate ids and parent-child lineage are stable and validated
- seed candidates from earlier phases are registered
- a new candidate can be added from a manifest without changing the schema
- an existing candidate can receive a status/update event without mutating identity or lineage fields
- an executable remote-validation handoff exists for one registered child candidate
- a remote execution packet exists before any remote run is claimed
- the registry captures evaluator result, evidence path, and status consistently
- Phase 4 search can create child candidates without losing provenance

## Sources

- [Build Sequence](../build_sequence.md)
- [Quant Research System Architecture](../architecture.md)
- [Quant Research System Environments](../environments.md)
- [Phase 1 Closure Review](../phase1_remote_validation/task_001_closure_decision.md)
- [Phase 2 Task 004 Local Review](../phase2_research_falsification/task_004_local_review.md)
- [Phase 2B Task 001 Local Review](../phase2b_implementation_translation/task_001_local_review.md)
