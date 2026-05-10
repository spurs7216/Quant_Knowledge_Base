---
title: Phase 4 Markdown Package Changelog
type: project
status: active
updated: 2026-05-10
tags:
  - project
  - phase4
  - changelog
---
# Phase 4 Markdown Package Changelog

## 2026-05-10 Attempt017 Repair Hardening

- Fixed population-policy seeding so prior attempts without explicit `parent_id` are not counted as offspring of the active attempt017 parent.
- Added controller-static parent-child behavior-delta diagnostics and exact smoke no-op rejection.
- Added behavior-delta MAP buckets so diversity is tied to functional ranking/portfolio/exposure changes, not patch text alone.
- Added sample-eval exposure diagnostics for gross, net, long, and short exposure.
- Added prompt-card reroute pressure for duplicate-heavy, low-fitness, or no-nonduplicate-pass cards before the next remote run.
- Added `controller_evaluator_hardening_remote_instructions_20260510.md` for the next controller-only remote smoke.

## 2026-05-09 Controller Search Policy Update

- Added `controller_population_policy_v2` and `prompt_fitness_and_lazy_score_v1` as the active controller-only duplicate/novelty policy before remote sample evaluation.
- Updated the diversity top-up handoff to review prompt-card fitness, controller search scores, lazy penalties, near-duplicate patch counts, and prior-summary seeded duplicate state.
- Kept the next milestone as a controller-only remote top-up; no child market evaluation or full validation is authorized until the uniqueness gate is met.

## 2026-04-27 Update

This package updates the prior Phase 4 markdown zip using the latest project decisions.

## Major Changes

- Clarified that `task_001_search_design.md` is the design source of truth.
- Clarified that `task_004_seed_strategy_program.md` implements Task 001 and does not replace it.
- Added `phase4_sampling_policy_v1.md` for data-aware MAP-Elites + island sampling.
- Added `program_database_schema.md` with SQLite tables and JSONL audit requirements.
- Added `universe_and_split_policy.md` with chronological 70/15/15 splits and rolling top-500 market-cap universe.
- Added `dataset_admission_policy.md` with staged dataset unlock and point-in-time join gates.
- Added `processed_outputs_policy.md` to prevent processed CSV outputs from being treated as parent programs without source-script validation.
- Added `remote_csv_execution_policy.md` to handle remote CSV warehouse constraints and no external `.exe` assumption.
- Added `prompt_contracts.md` with exact Qwen prompt, repair, reviewer, and immutable-rule contracts.
- Added `artifact_renderer_contract.md` for `evaluator_summary.json`, `prompt_card.md`, and search-state summaries.
- Added `codex_implementation_tasks.md` as an explicit implementation sequence for Codex.
- Updated model policy to remove Gemma 4 from the active stack.
- Updated first-loop policy to remain daily-stock-only.

## Current Active Design

```yaml
phase4_active_design:
  first_loop_data_scope: daily_stock_only
  universe: rolling_top500_market_cap_v1
  split: chronological_70_15_15
  inner_loop_model: Qwen3.5-9B
  repair_model: Qwen3.5-9B
  medium_reviewer: Qwen3.5-27B-FP8 optional
  deep_reviewer: Qwen3.6-35B-A3B-FP8 scheduled
  database: SQLite
  audit: JSONL
  metric_panels: Parquet if available, CSV fallback
  analysis: DuckDB if available, SQLite/pandas fallback
```
