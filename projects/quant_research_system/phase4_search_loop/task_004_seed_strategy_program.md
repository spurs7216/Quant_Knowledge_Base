---
title: Phase 4 Task 004 Seed Strategy Program and Qwen Loop
type: project
status: proposed
updated: 2026-04-29
tags:
  - project
  - phase4
  - alphaevolve
  - seed-program
  - qwen
sources:
  - "README.md"
  - "task_001_search_design.md"
  - "task_003_alphaevolve_scaffold.md"
  - "universe_and_split_policy.md"
  - "program_database_schema.md"
  - "prompt_contracts.md"
---
# Phase 4 Task 004 Seed Strategy Program and Qwen Loop

## Objective

Create the first true AlphaEvolve-style seed strategy program for the Kalman/reversal family and connect it to the measured Qwen model stack.

This task implements Task 001. It does not replace Task 001. Task 001 remains the design contract for the Phase 4 search loop.

All Qwen calls and AlphaEvolve-lite controller execution for this task run on the remote Linux/GPU/data server. The local Windows machine may edit the code/specification and review compact artifacts, but it must not launch Qwen or run LLM inference.

## Required Deliverables

### 1. Seed Strategy Module

Create:

```text
research/alphaevolve_lite/seeds/kalman_reversal_seed.py
```

Required interface:

```python
def compute_signal(panel, params):
    # EVOLVE-BLOCK-START: signal
    ...
    # EVOLVE-BLOCK-END


def rank_or_transform_signal(signal, panel, params):
    # EVOLVE-BLOCK-START: ranking
    ...
    # EVOLVE-BLOCK-END


def construct_portfolio(signal, panel, params):
    # EVOLVE-BLOCK-START: portfolio
    ...
    # EVOLVE-BLOCK-END


def apply_risk_controls(weights, panel, params):
    # EVOLVE-BLOCK-START: risk
    ...
    # EVOLVE-BLOCK-END


def evaluate(eval_inputs) -> dict[str, float]:
    ...
```

Non-evolvable skeleton owns:

- CSV data loading;
- rolling top-500 universe construction;
- chronological 70/15/15 split;
- duplicate policy;
- return timing;
- cost model;
- null generation;
- artifact writing;
- remote packet construction;
- broker/live-trading exclusion.

### 2. Universe and Split Implementation

Implement:

```text
research/alphaevolve_lite/universe.py
research/alphaevolve_lite/splits.py
```

Requirements:

- rolling top-500 market-cap universe computed monthly from prior-month-end information;
- split computed once from sorted unique trading dates;
- split manifest written;
- universe summary written;
- candidate code cannot edit these files through evolve blocks.

### 3. Program Database Generation Zero

Insert seed as generation zero:

```yaml
program_id: PROG-YYYYMMDD-000000
parent_program_id: null
root_candidate_id: CAND-20260423-001
branch_id: BRANCH-CAND-20260423-001-001
generation: 0
status: seed
island: daily_stock_signal
model_role: human_seed
mutation_surface:
  primary: seed
  secondary: []
  surface_count: 0
data_scope: daily_stock_only
```

### 4. Prompt Builder

Create:

```text
research/alphaevolve_lite/prompt_builder.py
```

Prompt must include:

- current parent code;
- allowed mutation surface;
- evaluator summaries for parent and inspirations;
- dataset context;
- cost model policy;
- immutable rules;
- strict SEARCH/REPLACE format with example;
- model role and decoding settings.

Use [prompt_contracts.md](prompt_contracts.md).

### 5. Qwen Model Router

Create:

```text
research/alphaevolve_lite/model_router.py
```

Required first roles:

```yaml
fast_generator:
  model: qwen35-9b-fast
  base_url: http://127.0.0.1:8001/v1

critic_repair:
  model: qwen35-9b-fast
  base_url: http://127.0.0.1:8001/v1
```

These URLs are localhost from the remote server's point of view. They are not local Windows services.

Optional later roles:

```yaml
medium_quality_reviewer:
  model: qwen35-27b-fp8
  base_url: http://127.0.0.1:8020/v1

deep_generator:
  model: qwen36-35b-a3b-deep
  base_url: http://127.0.0.1:8010/v1
```

### 6. Controller Static Micro-Filter

Create:

```text
research/alphaevolve_lite/micro_filter.py
```

Required checks:

- parse SEARCH/REPLACE;
- exact unique SEARCH match;
- SEARCH inside evolve block;
- no forbidden files or sections;
- no split edits;
- no universe edits;
- no cost model weakening;
- no broker logic;
- no undeclared imports or global names;
- no known semantic danger patterns;
- compile;
- vector smoke.

### 7. First Remote Controller Batch

Run:

```text
50 Qwen3.5-9B child attempts
```

This batch runs on the remote server. It is called a controller batch, not a local batch.

Track:

- raw parse pass;
- repair attempts;
- repair pass;
- exact-search match;
- evolve-block safe;
- undeclared-name pass;
- semantic-warning pass;
- compile pass;
- vector-smoke pass;
- program database insertion pass.

### 8. First Sample Evaluation

After `controller_static` and `toy_eval` success, run a small historical `remote_sample_eval` on remote CSV data.

Do not run full remote validation until:

- controller batch metrics are recorded;
- sample evaluation artifacts are valid;
- null and cost outputs exist;
- `evaluator_summary.json` is prompt-ready.

## Acceptance Criteria

Task 004 is complete only if:

- seed strategy module compiles;
- rolling top-500 universe builder compiles and writes manifest;
- chronological 70/15/15 split builder compiles and writes manifest;
- evolve blocks are detected;
- generation-zero record inserted into SQLite;
- Qwen3.5-9B produces at least one valid child patch;
- malformed or oversized patch gets one repair attempt;
- `controller_static` rejects unsafe changes;
- at least 50 attempts are recorded in the program database;
- evaluator summaries are valid JSON;
- no remote validation launches for a child that fails `controller_static` gates;
- no test set is used.
