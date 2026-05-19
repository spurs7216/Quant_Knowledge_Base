---
title: Phase 4 Codex Implementation Tasks
type: project
status: active
updated: 2026-05-08
tags:
  - project
  - phase4
  - codex
  - implementation
sources:
  - "task_004_seed_strategy_program.md"
  - "phase4_evaluator_improvement_plan.md"
  - "program_database_schema.md"
  - "prompt_contracts.md"
  - "../phase4_codex_clarifications.md"
---
# Phase 4 Codex Implementation Tasks

## Purpose

This file gives Codex an explicit implementation sequence. Follow it in order. Do not skip Task 001 design constraints.

The local Windows machine cannot run Qwen or other Phase 4 LLM inference. It is limited to editing, GitHub synchronization, and compact artifact review. All Qwen calls, AlphaEvolve-lite controller stages, program-database writes, static filters, toy evaluators, sample evaluators, and warehouse-backed evaluators run on the remote Linux/GPU/data server.

When a remote task calls Qwen, the remote agent must first open a dedicated terminal or `tmux` pane, launch the required Qwen/vLLM server there, keep it running, and verify `/health` plus `/v1/models` from a separate terminal. A connection-refused Qwen client result is an operator-preflight failure until the server is confirmed running.

## Task A. Inspect Project Design

Read in this order:

1. `README.md`
2. `task_001_search_design.md`
3. `universe_and_split_policy.md`
4. `program_database_schema.md`
5. `phase4_sampling_policy_v1.md`
6. `prompt_contracts.md`
7. `evaluator_contract.md`
8. `remote_csv_execution_policy.md`
9. `task_004_seed_strategy_program.md`

Deliverable:

```text
notes/phase4_design_readthrough.md
```

This note should list assumptions, missing files, and implementation risks.

## Task B. Create Package Skeleton

Create:

```text
research/alphaevolve_lite/__init__.py
research/alphaevolve_lite/evolve_blocks.py
research/alphaevolve_lite/diff_blocks.py
research/alphaevolve_lite/static_safety.py
research/alphaevolve_lite/vector_smoke.py
research/alphaevolve_lite/micro_filter.py
research/alphaevolve_lite/program_database_sqlite.py
research/alphaevolve_lite/audit_log.py
research/alphaevolve_lite/prompt_cards.py
research/alphaevolve_lite/evaluator_summary.py
research/alphaevolve_lite/prompt_builder.py
research/alphaevolve_lite/model_router.py
research/alphaevolve_lite/universe.py
research/alphaevolve_lite/splits.py
research/alphaevolve_lite/sampling_policy.py
research/alphaevolve_lite/seeds/kalman_reversal_seed.py
```

Acceptance:

```bash
python -m compileall research/alphaevolve_lite
```

## Task C. Implement Evolve Blocks and Diff Parser

Required functions:

```python
find_evolve_blocks(program_text) -> list[EvolveBlock]
parse_search_replace(diff_text) -> list[SearchReplaceBlock]
apply_search_replace(program_text, blocks, require_inside_evolve_block=True) -> str
```

Tests:

- valid one-line patch applies;
- malformed patch rejected;
- exact SEARCH not found rejected;
- SEARCH spanning outside evolve block rejected;
- duplicate SEARCH rejected.

## Task D. Implement Static Safety and Vector Smoke

Required checks:

- no split policy edits;
- no universe policy edits;
- no raw path edits;
- no cost-policy removal;
- no broker/IBKR/TWS/order/account strings;
- no undeclared imports/names;
- compile;
- NumPy/pandas vector smoke.

## Task E. Implement SQLite Program Database

Use schema from `program_database_schema.md`.

Required functions:

```python
init_db(db_path) -> None
insert_program(record) -> str
insert_prompt(record) -> str
insert_evaluation(record) -> str
append_audit_event(event) -> None
sample_parent(island, mode, rng) -> ProgramRecord
sample_inspirations(parent, k, rng) -> list[ProgramRecord]
update_map_cell(program_id) -> None
get_validation_exposure(root_candidate_id, branch_id, split_id) -> dict
```

## Task F. Implement Universe and Split Builders

Implement rolling top-500 market-cap universe.

Before implementing production universe or PnL logic, add the remote schema-inspection script required by [../phase4_codex_clarifications.md](../phase4_codex_clarifications.md):

```text
research/alphaevolve_lite/scripts/inspect_daily_stock_schema.py
```

It must write:

```text
artifacts/phase4_alphaevolve/data_schema/daily_stock_schema_report.json
artifacts/phase4_alphaevolve/data_schema/daily_stock_schema_report.md
artifacts/phase4_alphaevolve/data_schema/daily_stock_sample_head.csv
artifacts/phase4_alphaevolve/data_schema/daily_stock_field_mapping.yaml
```

Acceptance outputs:

```text
universe_summary.csv
universe_membership_monthly.csv or parquet
split_manifest.yaml
```

Use the active fixed IS/OS split contract from `universe_and_split_policy.md`: 2011-2025 analysis window, `in_sample` before 2023-01-01, and `out_sample` on or after 2023-01-01. Compute first/last cleaned trading dates from the loaded panel rather than manually inserting artifact-specific trading days. Rolling universe membership must still use point-in-time prior-month formation data.

## Task G. Implement Seed Strategy

Create `kalman_reversal_seed.py` with evolve blocks.

Required minimum:

- signal evolve block;
- ranking evolve block;
- portfolio evolve block;
- risk evolve block;
- `evaluate(eval_inputs)` adapter.

The seed can be simple. Correct skeleton boundaries are more important than strategy performance.

## Task H. Insert Generation-Zero Seed

Insert seed into SQLite.

Record:

- program ID;
- root candidate ID;
- branch ID;
- generation 0;
- island;
- descriptors;
- hash;
- artifact paths.

## Task I. Implement Prompt Builder and Qwen Router

Prompt builder must use `prompt_contracts.md`.

The Qwen router is a remote-server client. It must not attempt to launch or call Qwen from local Windows. It must support:

- `fast_generator`: Qwen3.5-9B;
- `critic_repair`: Qwen3.5-9B.

Do not require 27B/35B for first milestone.

## Task J. Run Small Remote Controller Dry Run, Then 50 Attempts

First run 5 to 10 child attempts on the remote server through the remote controller and Qwen3.5-9B. This is a controller-static dry run only. It must not launch child `remote_sample_eval`, `remote_stage0_eval`, `remote_full_validation`, or test-set evaluation.

Status as of 2026-05-09: `controller_batch_001` ran 50 controller-only attempts. It proved the controller mechanics at scale: no empty/reasoning-only outputs, all parse/apply/compile/vector/semantic gates at 1.0, DB insertion at 1.0, and 12 MAP cells occupied. It did not meet the uniqueness gate: 35/50 unique controller-static pass children versus the target of at least 40, with 15 duplicate-child rejects concentrated in `ranking/direction_flip`. No child `remote_sample_eval`, stage-0 evaluation, full validation, or test-set evaluation has run. `controller_population_policy_v2` and `prompt_fitness_and_lazy_score_v1` are now implemented to make duplicate prevention, prompt-card fitness, and lazy invalid-output penalties deterministic sampler/database policy before the next top-up.

Recommended next command:

```bash
python research/alphaevolve_lite/scripts/run_child_batch.py \
  --program-path research/alphaevolve_lite/seeds/kalman_reversal_seed.py \
  --evaluator-summary artifacts/phase4_alphaevolve/remote_sample_eval_refactor_smoke_20260507/evaluator_summary.json \
  --out-dir artifacts/phase4_alphaevolve/controller_batch_001_diversity_topup \
  --db-path artifacts/phase4_alphaevolve/program_database.sqlite \
  --attempts 20 \
  --model-role fast_generator \
  --max-tokens 8192 \
  --memory-card-limit 3 \
  --diagnostic-card-limit 4 \
  --skill-card-limit 3 \
  --duplicate-retry-attempts 2 \
  --population-policy-version v2 \
  --near-duplicate-threshold 0.88 \
  --surface-schedule ranking,signal,portfolio,risk \
  --prior-summary artifacts/phase4_alphaevolve/controller_batch_001/summary.json
```

Review:

```text
artifacts/phase4_alphaevolve/controller_batch_001_diversity_topup/summary.md
artifacts/phase4_alphaevolve/controller_batch_001_diversity_topup/summary.json
artifacts/phase4_alphaevolve/controller_batch_001_diversity_topup/reasoning_memory_update.md
artifacts/phase4_alphaevolve/controller_batch_001_diversity_topup/reasoning_memory_update.json
artifacts/phase4_alphaevolve/controller_batch_001_diversity_topup/evaluator_diagnostic_report.md
artifacts/phase4_alphaevolve/controller_batch_001_diversity_topup/controller_diagnostic_report.md
artifacts/phase4_alphaevolve/controller_batch_001_diversity_topup/skill_update.md
artifacts/phase4_alphaevolve/controller_batch_001_diversity_topup/skill_update.json
artifacts/phase4_alphaevolve/controller_batch_001_diversity_topup/population_policy_state.json
artifacts/phase4_alphaevolve/controller_batch_001_diversity_topup/attempt_*/micro_filter_initial_result.json
artifacts/phase4_alphaevolve/controller_batch_001_diversity_topup/attempt_*/micro_filter_result.json
artifacts/phase4_alphaevolve/controller_batch_001_diversity_topup/attempt_*/raw_output.txt
artifacts/phase4_alphaevolve/controller_batch_001_diversity_topup/attempt_*/repair_output.txt
artifacts/phase4_alphaevolve/controller_batch_001_diversity_topup/attempt_*/duplicate_retry_*_response.json
```

Compare against `controller_batch_001`, especially `unique_child_pass_rate`, `duplicate_retry_success_rate`, `duplicate_child_count`, `near_duplicate_patch_count`, ranking intent compliance, `map_cell_count`, `map_cell_duplicate_count`, `prompt_card_duplicate_counts`, `intent_duplicate_counts`, `reasoning_only_empty_count`, and failure categories.

Also inspect `prompt_card_fitness`, `prompt_card_score_sums`, `prompt_card_lazy_penalty_sums`, `controller_search_score_mean`, and `lazy_penalty_attempt_count`. These are controller-stage search-quality signals only; they are not market-alpha scores.

Also inspect `reasoning_memory_update.md` for `Group-Relative Controller Report`. This report ranks sibling attempts from the same parent by controller validity, uniqueness, repair burden, and MAP-cell diversity. It is not a market-alpha score.

Inspect `evaluator_diagnostic_report.md` and `controller_diagnostic_report.md` as the Dr. RTL-style analyzer output. Inspect `skill_update.md` as candidate skill evidence only; do not promote a new market skill from one controller-static run.

Track:

```yaml
metrics:
  raw_parse_pass_rate:
  repair_attempt_rate:
  repair_success_rate:
  empty_retry_rate:
  empty_retry_success_rate:
  reasoning_only_empty_count:
  max_initial_response_reasoning_length:
  exact_search_match_rate:
  evolve_block_safe_rate:
  compile_pass_rate:
  vector_smoke_pass_rate:
  portfolio_semantic_pass_rate:
  unique_child_pass_rate:
  duplicate_child_count:
  duplicate_patch_fingerprint_count:
  near_duplicate_patch_count:
  duplicate_retry_attempt_rate:
  duplicate_retry_success_rate:
  map_cell_count:
  map_cell_duplicate_count:
  population_policy_version:
  prompt_fitness_policy_version:
  prompt_card_duplicate_counts:
  prompt_card_fitness:
  prompt_card_score_sums:
  prompt_card_lazy_penalty_sums:
  controller_search_score_mean:
  lazy_penalty_attempt_count:
  intent_duplicate_counts:
  db_insert_pass_rate:
```

Write:

```text
artifacts/phase4_alphaevolve/controller_batch_001_diversity_topup/summary.md
artifacts/phase4_alphaevolve/controller_batch_001_diversity_topup/summary.json
```

Pass target for this controller-only milestone:

```yaml
controller_batch_001_diversity_topup_target:
  attempt_count: 20
  prior_pass_count: 35
  unique_semantic_pass_children: ">= 12"
  aggregate_unique_semantic_pass_children: ">= 45 across controller_batch_001 plus top-up"
  duplicate_child_count: "<= 5 preferred"
  near_duplicate_patch_count: "reported"
  population_policy_version: "controller_population_policy_v2"
  prompt_fitness_policy_version: "prompt_fitness_and_lazy_score_v1"
  prompt_card_fitness: "reported"
  controller_search_score_mean: "reported"
  lazy_penalty_attempt_count: "reported"
  empty_output_rate: 0
  reasoning_only_empty_count: 0
  db_insert_pass_rate: "near 1.0"
  remote_sample_eval_launched: false
  full_validation_launched: false
```

## Task K. Do Not Run Remote Data Evaluation Yet Unless Controller Batch Passes

Minimum controller thresholds before `remote_sample_eval`:

```yaml
controller_thresholds:
  parse_pass_rate: ">= 0.80"
  apply_pass_rate: ">= 0.80"
  compile_pass_rate: ">= 0.80"
  vector_smoke_pass_rate: ">= 0.70"
  aggregate_unique_controller_static_children: ">= 45 after controller_batch_001 plus diversity top-up"
  remote_sample_eval_launched_during_controller_batches: false
```

Even if thresholds pass, run `remote_sample_eval` before `remote_stage0_eval` or `remote_full_validation`.
