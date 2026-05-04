---
title: Phase 4 Codex Implementation Tasks
type: project
status: active
updated: 2026-05-04
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

Do not hardcode final split dates manually. Compute them from cleaned sorted trading dates after duplicate policy and basic validity checks, then compute rolling universe membership inside each split.

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

Status as of 2026-05-04: no-thinking routing removed the null-content failure in `controller_batch_001_small_semantic_v3`, but the run produced only 7 unique children out of 10 because three attempts were duplicates. MAP-Elites-style diversity targeting, duplicate-retry hardening, the C1 ReasoningBank-style memory scaffold, Dr. RTL-style group-relative controller reporting, deterministic diagnostic cards, and the explicit skill-library scaffold are now implemented. The next small rerun should keep reasoning memory and skill-library prompts enabled and should not launch child `remote_sample_eval`.

Recommended next small command:

```bash
python research/alphaevolve_lite/scripts/run_child_batch.py \
  --program-path research/alphaevolve_lite/seeds/kalman_reversal_seed.py \
  --evaluator-summary artifacts/phase4_alphaevolve/remote_sample_eval_seed_v2/evaluator_summary.json \
  --out-dir artifacts/phase4_alphaevolve/controller_batch_001_small_semantic_v4 \
  --db-path artifacts/phase4_alphaevolve/program_database.sqlite \
  --attempts 10 \
  --model-role fast_generator \
  --max-tokens 8192 \
  --memory-card-limit 3 \
  --diagnostic-card-limit 4 \
  --skill-card-limit 3 \
  --duplicate-retry-attempts 1
```

Review:

```text
artifacts/phase4_alphaevolve/controller_batch_001_small_semantic_v4/summary.md
artifacts/phase4_alphaevolve/controller_batch_001_small_semantic_v4/summary.json
artifacts/phase4_alphaevolve/controller_batch_001_small_semantic_v4/reasoning_memory_update.md
artifacts/phase4_alphaevolve/controller_batch_001_small_semantic_v4/reasoning_memory_update.json
artifacts/phase4_alphaevolve/controller_batch_001_small_semantic_v4/evaluator_diagnostic_report.md
artifacts/phase4_alphaevolve/controller_batch_001_small_semantic_v4/controller_diagnostic_report.md
artifacts/phase4_alphaevolve/controller_batch_001_small_semantic_v4/skill_update.md
artifacts/phase4_alphaevolve/controller_batch_001_small_semantic_v4/skill_update.json
artifacts/phase4_alphaevolve/controller_batch_001_small_semantic_v4/attempt_*/micro_filter_initial_result.json
artifacts/phase4_alphaevolve/controller_batch_001_small_semantic_v4/attempt_*/micro_filter_result.json
artifacts/phase4_alphaevolve/controller_batch_001_small_semantic_v4/attempt_*/raw_output.txt
artifacts/phase4_alphaevolve/controller_batch_001_small_semantic_v4/attempt_*/repair_output.txt
artifacts/phase4_alphaevolve/controller_batch_001_small_semantic_v4/attempt_*/empty_retry_*_response.json
```

Compare against the `semantic_v3` baseline, especially `duplicate_child_count`, `duplicate_retry_success_rate`, `map_cell_count`, `unique_child_pass_rate`, and `reasoning_only_empty_count`.

Also inspect `reasoning_memory_update.md` for `Group-Relative Controller Report`. This report ranks sibling attempts from the same parent by controller validity, uniqueness, repair burden, and MAP-cell diversity. It is not a market-alpha score.

Inspect `evaluator_diagnostic_report.md` and `controller_diagnostic_report.md` as the Dr. RTL-style analyzer output. Inspect `skill_update.md` as candidate skill evidence only; do not promote a new market skill from one controller-static run.

If the small dry run shows the controller path is healthy, then run the larger batch:

Run 50 child attempts on the remote server through the remote controller and Qwen3.5-9B.

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
  duplicate_retry_attempt_rate:
  duplicate_retry_success_rate:
  map_cell_count:
  map_cell_duplicate_count:
  db_insert_pass_rate:
```

Write:

```text
artifacts/phase4_alphaevolve/controller_batch_001/summary.md
artifacts/phase4_alphaevolve/controller_batch_001/summary.json
```

## Task K. Do Not Run Remote Data Evaluation Yet Unless Controller Batch Passes

Minimum controller thresholds before `remote_sample_eval`:

```yaml
controller_thresholds:
  parse_pass_rate: ">= 0.80"
  apply_pass_rate: ">= 0.80"
  compile_pass_rate: ">= 0.80"
  vector_smoke_pass_rate: ">= 0.70"
```

Even if thresholds pass, run `remote_sample_eval` before `remote_stage0_eval` or `remote_full_validation`.
