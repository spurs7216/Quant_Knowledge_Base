---
title: Phase 3 Candidate Registry Schema
type: project
status: active
updated: 2026-04-25
tags:
  - project
  - phase3
  - schema
  - candidate-registry
---
# Phase 3 Candidate Registry Schema

## Purpose

This schema defines the minimal candidate table needed before Phase 4 search begins.

The registry is a control-plane table, not an artifact store. It should point to code, manifests, project decisions, and evidence bundles rather than duplicating their contents.

## Candidate Identity

Candidate ids use:

```text
CAND-YYYYMMDD-NNN
```

Rules:

- ids are stable after creation
- ids are never reused after rejection or supersession
- parent-child lineage is explicit through `parent_id`
- all members of a candidate family share the same `root_candidate_id`

## Required Columns

`candidate_registry.csv` must contain exactly these columns:

| Column | Meaning |
| --- | --- |
| `candidate_id` | Stable candidate id. |
| `parent_id` | Parent candidate id, blank only for root candidates. |
| `root_candidate_id` | Root id of the candidate family. |
| `candidate_name` | Human-readable descriptive name. |
| `created` | ISO date when the row was created. |
| `artifact_type` | Type of candidate artifact. |
| `environment` | Environment that produced or evaluates the artifact. |
| `artifact_path` | Path to the defining project note, manifest, or artifact bundle. |
| `code_path` | Path to defining code if any, blank if not code-defined. |
| `patch_path` | Patch or diff path if the candidate was produced by a patch, blank otherwise. |
| `evaluator_result` | Compact machine or reviewer result. |
| `local_decision` | Local control-plane decision. |
| `status` | Current registry status. |
| `score_summary` | Compact score or gate summary. |
| `evidence_path` | Main evidence path supporting the current status. |
| `source_phase` | Phase that produced the candidate or artifact. |
| `notes` | Short caveat or next action. |

## Allowed Artifact Types

- `strategy_rule`
- `factor_definition`
- `research_script`
- `constructor`
- `search_artifact`
- `implementation_translation`
- `evaluation_workflow`

## Allowed Environments

- `remote_validation`
- `research_falsification`
- `implementation_translation_smoke`
- `implementation_execution`
- `prospective_paper`
- `manual_control_plane`

## Allowed Decisions

- `pending`
- `reject`
- `revise`
- `proceed`
- `paper-test`
- `record-only`

Decision meaning:

- `pending`: candidate is registered but has not yet received an evaluator-backed local decision.
- `reject`: evidence blocks further research budget.
- `revise`: fixable gaps remain; do not promote.
- `proceed`: eligible for stronger validation or child candidate generation.
- `paper-test`: eligible for a later frozen prospective paper workflow.
- `record-only`: preserve lineage for support artifacts that are not alpha candidates.

## Allowed Statuses

- `active`
- `rejected`
- `promoted`
- `paper-test`
- `superseded`

Status meaning:

- `active`: still under investigation or awaiting revision.
- `rejected`: stopped unless explicitly reopened.
- `promoted`: passed the current gate and can feed a stronger downstream environment.
- `paper-test`: frozen and approved for a paper-testing workflow.
- `superseded`: replaced by a child candidate or corrected artifact.

## Status Transition Rules

Allowed ordinary transitions:

| From | To | Required evidence |
| --- | --- | --- |
| `active` | `rejected` | local decision note or artifact review |
| `active` | `promoted` | accepted evaluator result and local decision |
| `active` | `paper-test` | accepted validation plus execution-safety review |
| `active` | `superseded` | child candidate id and reason |
| `promoted` | `paper-test` | paper-test approval note |
| `promoted` | `superseded` | stronger child candidate or corrected artifact |

Reopening a `rejected` or `superseded` candidate requires a new event-log row explaining the reason. Prefer creating a child candidate over mutating the old row when the artifact definition changes.

The status-update script currently permits the following transitions:

- `active -> active`
- `active -> rejected`
- `active -> promoted`
- `active -> paper-test`
- `active -> superseded`
- `promoted -> promoted`
- `promoted -> paper-test`
- `promoted -> superseded`
- `rejected -> active`
- `superseded -> active`

Reopening from `rejected` or `superseded` should remain rare and must have an explicit event rationale.

## Event Log

`candidate_event_log.csv` is append-only. It records candidate creation, evaluator results, status changes, supersession, and manual corrections.

Required event columns:

| Column | Meaning |
| --- | --- |
| `event_id` | Stable event id. |
| `event_date` | ISO date. |
| `candidate_id` | Candidate affected by the event. |
| `event_type` | Creation, evaluation, status change, or note. |
| `from_status` | Prior status, blank for creation. |
| `to_status` | New status when applicable. |
| `actor_role` | Local role or environment that produced the event. |
| `evidence_path` | Main supporting path. |
| `summary` | Short explanation. |

## Manifest Registration

New candidates should normally enter through a manifest rather than manual CSV edits.

Registration command:

```text
python research/candidate_registry/register_candidate.py --manifest <manifest-path>
```

The registration script:

- reads `candidate_manifest.template.yaml`-style files
- appends exactly one candidate row
- appends exactly one event-log row
- validates the combined registry before writing
- refuses duplicate candidate ids or duplicate event ids

Use `--dry-run` before writing when testing a new manifest.

## Status Update

Existing candidates should receive later review or evaluator results through a status-update manifest.

Update command:

```text
python research/candidate_registry/update_candidate_status.py --manifest <status-update-path>
```

The update script:

- verifies the candidate exists
- verifies the current status matches the manifest expectation
- checks the requested transition against the allowed transition table
- updates only mutable review/status fields
- appends exactly one event-log row
- validates the combined registry before writing

Mutable fields:

- `evaluator_result`
- `local_decision`
- `status`
- `score_summary`
- `evidence_path`
- `notes`

Identity and lineage fields are immutable through this path.

## Validation Rules

The validator must check:

- required columns are present in the registry and event log
- candidate ids are unique
- candidate ids and event ids match the required id formats
- root candidates have blank `parent_id`
- non-root candidates reference an existing parent
- non-root candidates keep the same `root_candidate_id` as their parent
- statuses, decisions, artifact types, and environments use allowed values
- event-log status fields use allowed statuses when nonblank
- each candidate has at least one event-log row
- status-update manifests preserve identity and lineage fields

The validator is intentionally schema-level. It does not decide whether an alpha is good.
