---
title: Phase 4 Evaluator Improvement Plan for Codex
type: project
status: active
updated: 2026-04-29
tags:
  - project
  - phase4
  - evaluator
  - codex
sources:
  - "README.md"
  - "evaluator_contract.md"
  - "phase4_sampling_policy_v1.md"
  - "program_database_schema.md"
  - "universe_and_split_policy.md"
---
# Phase 4 Evaluator Improvement Plan for Codex

## Purpose

This note specifies concrete system improvements for the Phase 4 AlphaEvolve-style quant research loop.

The local Windows machine cannot run Qwen. All Qwen calls, AlphaEvolve-lite controller stages, program-database updates, static filters, toy evaluators, sample evaluators, and warehouse-backed evaluators must run on the remote Linux/GPU/data server.

The current design is: generated programs must be bounded by evolve blocks, evaluated through a fixed cascade, and stored with lineage, metrics, diagnostics, and validation-exposure accounting.

## Source Files Codex Should Inspect First

1. `README.md`
2. `task_001_search_design.md`
3. `universe_and_split_policy.md`
4. `phase4_sampling_policy_v1.md`
5. `program_database_schema.md`
6. `prompt_contracts.md`
7. `evaluator_contract.md`
8. `artifact_renderer_contract.md`
9. `remote_csv_execution_policy.md`
10. `dataset_admission_policy.md`

## High-Priority Implementation Changes

### 1. Implement rolling top-500 universe and 70/15/15 split

Files:

```text
research/alphaevolve_lite/universe.py
research/alphaevolve_lite/splits.py
```

Must write:

```text
universe_summary.csv
universe_membership_monthly.csv or parquet
split_manifest.yaml
```

### 2. Implement SQLite program database

Files:

```text
research/alphaevolve_lite/program_database_sqlite.py
research/alphaevolve_lite/db_init.py
```

Implement tables from [program_database_schema.md](program_database_schema.md).

### 3. Implement JSONL audit log

Every material event must append to:

```text
artifacts/phase4_alphaevolve/audit_log.jsonl
```

### 4. Implement deterministic micro-filter

Files:

```text
research/alphaevolve_lite/diff_parser.py
research/alphaevolve_lite/evolve_block_guard.py
research/alphaevolve_lite/static_safety.py
research/alphaevolve_lite/vector_smoke.py
research/alphaevolve_lite/micro_filter.py
```

Required checks:

- parse SEARCH/REPLACE;
- unique exact SEARCH match;
- SEARCH fully inside evolve block;
- no forbidden files;
- no split/universe/cost/raw-path edits;
- no broker logic;
- no undeclared names or imports;
- no semantic danger patterns;
- compile;
- vector-smoke tests for expected signal types.

Executable stage name: `controller_static`. Do not name this stage `local_static` in new code.

### 5. Implement evaluator summary renderer

Files:

```text
research/alphaevolve_lite/evaluator_summary.py
research/alphaevolve_lite/prompt_cards.py
```

Must emit:

```text
evaluator_summary.json
prompt_card.md
failure_report.md
```

### 6. Implement validation-overuse controls

Update database and evaluator adapters to record:

- children per root/branch;
- controller_static passes per root/branch;
- sample evals per root/branch;
- remote validations per root/branch;
- promotions per root/branch;
- branch freeze status;
- test evaluation status.

### 7. Implement sampling policy

Files:

```text
research/alphaevolve_lite/sampling_policy.py
```

Must support:

- island selection;
- MAP-Elites cell selection;
- top adjusted score selection;
- novelty survivor selection;
- repair candidate selection;
- inspiration sampling.

### 8. Implement model router

Files:

```text
research/alphaevolve_lite/model_router.py
```

Required first roles:

- `fast_generator`: Qwen3.5-9B
- `critic_repair`: Qwen3.5-9B

Optional:

- `medium_quality_reviewer`: Qwen3.5-27B-FP8
- `deep_generator`: Qwen3.6-35B-A3B-FP8

### 9. Implement remote CSV execution adapter

Files:

```text
research/alphaevolve_lite/remote_packet.py
research/remote_validation/phase4_runner.py
```

Must not require external `.exe` installs.

Must support CSV input and compact artifact output.

### 10. Implement dataset admission registry later

Do not implement feature code for non-daily-stock datasets until the registry exists.

## First Milestone

```yaml
milestone_1:
  name: remote_controller_qwen_loop_on_seed_program
  target_children: 50
  required:
    - seed program
    - SQLite DB
    - JSONL audit
    - prompt builder
    - Qwen3.5-9B generation on remote server
    - repair once
    - micro-filter
    - evaluator summaries
  forbidden:
    - remote full validation before controller_static gates
    - test set
    - dataset additions
    - broker logic
```

## Second Milestone

```yaml
milestone_2:
  name: remote_sample_eval_on_remote_csv
  target_children: 5_to_10
  required:
    - rolling top500 universe manifest
    - split manifest
    - cost grid
    - matched-turnover nulls
    - compact artifact bundle
```

## Third Milestone

```yaml
milestone_3:
  name: first_remote_full_validation
  target_children: 1_to_3
  required:
    - full evaluator contract
    - validation exposure tracking
    - prompt cards for future sampling
```
