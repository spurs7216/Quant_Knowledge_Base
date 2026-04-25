---
title: Phase 3 Task 002 Manifest Candidate Registration
type: project
status: completed
updated: 2026-04-25
tags:
  - project
  - phase3
  - candidate-registry
  - manifest
sources:
  - "candidate_registry_schema.md"
  - "candidate_manifest.template.yaml"
  - "manifests/cand_20260425_001_duplicate_policy_revision.yaml"
  - "candidate_registry.csv"
  - "candidate_event_log.csv"
---
# Phase 3 Task 002 Manifest Candidate Registration

## Objective

Prove that Phase 3 can add a new candidate from a manifest without changing the registry table by hand.

This task creates the first manifest-registered child of the Phase 1 reversal baseline. It is an active planned revision candidate, not a new backtest result and not an alpha promotion.

## Candidate Added

`CAND-20260425-001`: Daily stock reversal duplicate-policy revision.

Lineage:

- parent: `CAND-20260423-001`
- root: `CAND-20260423-001`
- source phase: `phase3_candidate_registry`
- environment: `remote_validation`
- local decision: `pending`
- status: `active`

## Why This Candidate Comes Next

The Phase 1 baseline remains `revise` for several reasons, but the duplicate `PERMNO` by `DlyCalDt` handling is the cleanest first child candidate because it is a data-quality policy rather than a new alpha idea.

The planned change is narrow:

- keep the signal family fixed
- replace implicit keep-first duplicate handling with an explicit candidate policy
- preserve diagnostics for duplicate counts before and after universe filters
- rerun the same remote-validation gates before any broader search

## Registration Path

The new script is:

- [../../../research/candidate_registry/register_candidate.py](../../../research/candidate_registry/register_candidate.py)

The script:

- reads a simple candidate manifest
- appends one registry row
- appends one event-log row
- validates candidate ids, event ids, allowed values, parent-child lineage, and event coverage before writing

## Validation

Expected validation after registration:

```text
validated_candidates: 3
validated_events: 6
```

## Next Work

The next task should turn `CAND-20260425-001` into an executable remote-validation revision:

- define the duplicate-row policy precisely
- create a remote-validation manifest for the revised run
- patch or fork the research script only in the duplicate-policy surface
- compare the revised run against `CAND-20260423-001`
