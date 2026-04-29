---
title: Phase 4 Artifact Renderer Contract
type: project
status: active
updated: 2026-04-29
tags:
  - project
  - phase4
  - artifacts
  - evaluator-summary
  - prompt-cards
sources:
  - "evaluator_contract.md"
  - "phase4_sampling_policy_v1.md"
  - "program_database_schema.md"
---
# Phase 4 Artifact Renderer Contract

## Purpose

The prompt sampler must not parse long CSVs, large logs, or arbitrary report files. It should read compact rendered artifacts.

This contract defines the artifacts that every controller and remote data-evaluation stage should produce for future prompts and database sampling.

## Required Artifact: `evaluator_summary.json`

Every child attempt that reaches `controller_static` must produce:

```text
artifacts/phase4/<run_id>/evaluator_summary.json
```

Minimum schema:

```json
{
  "schema_version": "phase4_evaluator_summary_v1",
  "run_id": "RUN-YYYYMMDD-000001",
  "program_id": "PROG-YYYYMMDD-000123",
  "parent_program_id": "PROG-YYYYMMDD-000001",
  "root_candidate_id": "CAND-20260423-001",
  "branch_id": "BRANCH-CAND-20260423-001-001",
  "split_id": "daily_stock_top500_chrono_70_15_15_v1",
  "eval_stage": "controller_static|toy_eval|remote_sample_eval|remote_stage0_eval|remote_full_validation",
  "decision": "reject|revise|survive_for_mutation|promote_to_candidate_registry|record_only",
  "selection_score": null,
  "metrics": {},
  "hard_gates": {},
  "diagnostics": {},
  "warnings": [],
  "mutation_surface": {},
  "descriptors": {},
  "validation_exposure": {},
  "artifact_paths": {},
  "failure_category": null,
  "failure_reason": null,
  "next_prompt_hint": ""
}
```

## Required Artifact: `prompt_card.md`

The prompt card is the human-readable, prompt-ready summary of a program.

Template:

```markdown
# Program Card: {program_id}

- parent: {parent_program_id}
- generation: {generation}
- island: {island}
- status: {status}
- mutation surface: {mutation_surface.primary}
- data scope: {descriptors.data_scope}
- selection score: {selection_score}

## What Changed

{short_change_summary}

## Key Metrics

| metric | value |
| --- | ---: |
| validation_net_sharpe | ... |
| null_delta_validation_sharpe | ... |
| turnover | ... |
| cost_drag | ... |
| max_abs_weight_p99 | ... |

## Gate Summary

- controller_static gates: pass/fail
- point-in-time gates: pass/fail/not applicable
- cost gates: pass/fail
- null gates: pass/fail

## Failure or Warning

{failure_reason_or_warning}

## Next Prompt Hint

{next_prompt_hint}
```

## Required Artifact: `failure_report.md`

Every failed or rejected program should have a failure report.

Required sections:

```markdown
# Failure Report

## Failure Category

## Exact Gate That Failed

## Minimal Reproduction

## Whether Repair Is Allowed

## Next Prompt Hint

## Whether This Failure Can Be Used As Inspiration
```

Leakage, split changes, broker logic, and cost removal may be used as negative examples but not as repair parents.

## Required Artifact: `search_state_summary.json`

Every 30 to 50 children, the controller should write a search-state summary for medium/deep reviewers.

Schema:

```json
{
  "schema_version": "phase4_search_state_summary_v1",
  "root_candidate_id": "CAND-20260423-001",
  "split_id": "daily_stock_top500_chrono_70_15_15_v1",
  "num_children": 0,
  "num_local_pass": 0,
  "num_remote_sample_eval_pass": 0,
  "num_remote_validated": 0,
  "island_counts": {},
  "top_program_cards": [],
  "underexplored_map_cells": [],
  "common_failure_categories": {},
  "validation_exposure": {},
  "null_summary": {},
  "cost_fragility_summary": {},
  "recommendation_request": "Suggest bounded mutation surfaces; do not write code."
}
```

## Artifact Size Policy

Compact artifacts should be small enough to sync to the vault.

```yaml
artifact_size_policy:
  evaluator_summary_json: small_required
  prompt_card_md: small_required
  failure_report_md: small_required
  scorecard_csv: small_required
  diagnostics_csv: small_required
  positions_sample: optional_compact_sample
  full_warehouse_extracts: forbidden
```

## Renderer Implementation Tasks

Codex should implement:

```python
render_evaluator_summary(record, metrics, diagnostics, decisions) -> dict
write_evaluator_summary(path, summary) -> None
render_prompt_card(program_record, evaluator_summary) -> str
render_failure_report(failure) -> str
render_search_state_summary(database, root_candidate_id, branch_id) -> dict
```

## Prompt-Sampler Rule

The prompt sampler should prefer:

1. `prompt_card.md`
2. selected fields from `evaluator_summary.json`
3. source-code slices around evolve blocks

It should not load full historical returns, full positions, or large CSV outputs into prompts.
