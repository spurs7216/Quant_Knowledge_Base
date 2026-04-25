---
title: Phase 3 Task 001 Seed Candidate Registry
type: project
status: completed
updated: 2026-04-25
tags:
  - project
  - phase3
  - candidate-registry
sources:
  - "../phase1_remote_validation/task_001_closure_decision.md"
  - "../phase2_research_falsification/task_004_local_review.md"
  - "../phase2b_implementation_translation/task_001_local_review.md"
  - "candidate_registry.csv"
  - "candidate_event_log.csv"
---
# Phase 3 Task 001 Seed Candidate Registry

## Objective

Start Phase 3 by creating the candidate registry package and seeding it with the candidates already produced by earlier phases.

This task deliberately does not start Phase 4 search. It creates the control-plane memory needed before search can safely generate child variants.

## Inputs Read

- [Build Sequence](../build_sequence.md)
- [Quant Research System Architecture](../architecture.md)
- [Quant Research System Environments](../environments.md)
- [Remote Data and GPU Workflow](../remote_workflow.md)
- [Phase 1 Closure Review](../phase1_remote_validation/task_001_closure_decision.md)
- [Phase 2 Task 004 Local Review](../phase2_research_falsification/task_004_local_review.md)
- [Phase 2B Task 001 Local Review](../phase2b_implementation_translation/task_001_local_review.md)

## Seed Candidates

### `CAND-20260423-001`

Research candidate:

- source: Phase 1 daily-stock short-horizon reversal task
- artifact type: `research_script`
- environment: `remote_validation`
- decision: `revise`
- status: `active`

Reasoning:

The candidate has accepted workflow evidence and a clean closure run, but it is not alpha-ready. The validation split is negative after costs, the result is cost-sensitive, and duplicate `PERMNO` by date rows still need a production-quality policy.

### `CAND-20260424-001`

Implementation-translation child:

- parent: `CAND-20260423-001`
- artifact type: `implementation_translation`
- environment: `implementation_translation_smoke`
- decision: `record-only`
- status: `active`

Reasoning:

This row preserves the fact that the revised strategy has been translated into no-send broker-facing artifacts. It is not alpha evidence, not a paper-trading approval, and not a separate strategy proposal.

## Outputs Created

- [candidate_registry_schema.md](candidate_registry_schema.md)
- [candidate_registry.csv](candidate_registry.csv)
- [candidate_event_log.csv](candidate_event_log.csv)
- [candidate_manifest.template.yaml](candidate_manifest.template.yaml)
- [../../../research/candidate_registry/validate_candidate_registry.py](../../../research/candidate_registry/validate_candidate_registry.py)

## Validation

The first registry validation should pass with:

```text
validated_candidates: 2
validated_events: 5
```

## Next Phase 3 Task

Create a manifest-driven registration path for the next revised research candidate, likely a child of `CAND-20260423-001` that fixes one specific weakness:

- duplicate `PERMNO` by `DlyCalDt` handling
- higher-friction and borrow-cost assumptions
- sector, size, or liquidity control
- random-rank null comparison under the same turnover profile
