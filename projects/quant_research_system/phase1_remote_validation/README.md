---
title: Phase 1 Remote Validation
type: project
status: active
updated: 2026-04-23
tags:
  - project
  - phase1
  - remote-validation
  - quant
---
# Phase 1 Remote Validation

## Purpose

Turn the `remote_validation` environment from design into an executable contract.

This phase does not optimize for smallness. It builds the first robust foundation for real-data research:

- a reusable remote job manifest
- a compact artifact bundle schema
- a local preflight checklist
- one auditable baseline task on `daily_stock`

## Files

- [remote_job_manifest.template.yaml](remote_job_manifest.template.yaml): generic manifest template for remote validation jobs.
- [artifact_bundle_schema.md](artifact_bundle_schema.md): required and optional outputs from the remote Ubuntu machine.
- [preflight_checklist.md](preflight_checklist.md): local checks before a job is sent to remote compute.
- [task_001_daily_stock_short_reversal.md](task_001_daily_stock_short_reversal.md): first concrete validation task.
- [task_001_manifest.yaml](task_001_manifest.yaml): concrete draft manifest for the first task.
- [task_001_decision.md](task_001_decision.md): decision from the first full remote-validation run.
- [task_001_closure_decision.md](task_001_closure_decision.md): remote closure evidence pulled from the clean rerun plus local review status.
- [manual_remote_steps.md](manual_remote_steps.md): commands the human should run on the remote Ubuntu machine.
- [phase1_closure_remote_instructions.md](phase1_closure_remote_instructions.md): stricter clean-run instructions for producing closure evidence.

Executable scaffold:

- [../../../research/remote_validation/task001_daily_stock_short_reversal.py](../../../research/remote_validation/task001_daily_stock_short_reversal.py)
- [../../../research/remote_validation/requirements.txt](../../../research/remote_validation/requirements.txt)

## Phase 1 Success Criteria

Phase 1 is complete when:

- the task manifest is filled with exact git snapshots
- the remote Ubuntu machine can pull the relevant GitHub commit
- the remote run executes against the full warehouse data
- a compact artifact bundle is manually reviewed locally, or a human explicitly waives local artifact import
- approved artifacts are copied into `artifacts/remote_runs/`, unless waived
- a local or human-reviewed project note records `proceed`, `revise`, or `reject`
- a local or human-reviewed project note records the final phase-close decision

Remote agents may provide evidence and recommendations, but they must not be treated as final authority for phase closure.

## Relationship To System Design

This folder implements the first environment from [environments.md](../environments.md):

- environment: `remote_validation`
- first data family: `daily_stock`
- first candidate type: auditable baseline factor/strategy
- evidence path: compact artifacts, not heavy data copies

## Non-Goals

- Do not build large-scale search yet.
- Do not use IBKR execution yet.
- Do not push remote warehouse data into GitHub.
- Do not treat the first baseline as an alpha claim.
