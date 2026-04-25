---
title: Phase 3 Task 003 Candidate Evaluation Intake
type: project
status: completed
updated: 2026-04-25
tags:
  - project
  - phase3
  - candidate-registry
  - lifecycle
sources:
  - "candidate_registry_schema.md"
  - "candidate_status_update.template.yaml"
  - "status_updates/cand_20260425_001_ready_for_remote_manifest.yaml"
  - "candidate_registry.csv"
  - "candidate_event_log.csv"
---
# Phase 3 Task 003 Candidate Evaluation Intake

## Objective

Add a status-update path for existing candidates.

Task 002 proved that the registry can create candidates from manifests. Task 003 proves that the registry can process later candidate events without losing lineage or manually rewriting history.

## New Capability

The new script is:

- [../../../research/candidate_registry/update_candidate_status.py](../../../research/candidate_registry/update_candidate_status.py)

It accepts a status-update manifest and:

- verifies that the candidate exists
- verifies the current status matches the manifest expectation
- checks the requested transition against the allowed transition table
- updates only mutable review/status fields
- appends one event-log row
- validates the full registry and event log before writing

Mutable fields are limited to:

- `evaluator_result`
- `local_decision`
- `status`
- `score_summary`
- `evidence_path`
- `notes`

Identity and lineage fields are intentionally immutable through this path.

## Control-Plane Update Applied

Candidate:

- `CAND-20260425-001`

Transition:

- `active -> active`

Reason:

No new empirical result exists yet, so the candidate should not be promoted, rejected, or revised. The update records that its scope is now fixed enough for remote-validation manifest construction.

Updated state:

- evaluator result: `ready_for_remote_manifest_construction`
- local decision: `pending`
- status: `active`
- next gate: remote-validation manifest for the duplicate-policy revision

## Why This Matters

Phase 3 should not only preserve candidate birth records. It needs a lifecycle:

- create candidate
- add review or evaluator events
- update status under explicit transition rules
- preserve all events as an append-only trail
- keep identity and lineage stable

This is the minimum registry behavior needed before Phase 4 search begins generating many child candidates.

## Validation

Expected validation after the Task 003 update:

```text
validated_candidates: 3
validated_events: 7
```

## Next Work

Task 004 later created the remote-validation handoff by making executable child `CAND-20260425-002`:

- define the duplicate-row policy precisely
- create a remote job manifest
- create or patch the research code path for the revised duplicate-policy candidate
- keep the signal family fixed so the child tests one issue rather than a bundle of changes

See [Task 004 Remote Validation Handoff](task_004_remote_validation_handoff.md).
