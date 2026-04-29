---
title: Phase 4 Codex Implementation Tasks
type: project
status: active
updated: 2026-04-29
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

## Task J. Run 50 Remote Controller Attempts

Run 50 child attempts on the remote server through the remote controller and Qwen3.5-9B.

Track:

```yaml
metrics:
  raw_parse_pass_rate:
  repair_attempt_rate:
  repair_success_rate:
  exact_search_match_rate:
  evolve_block_safe_rate:
  undeclared_name_pass_rate:
  compile_pass_rate:
  vector_smoke_pass_rate:
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
