---
title: Phase 4 Task 001 Search Design
type: project
status: active
updated: 2026-05-19
tags:
  - project
  - phase4
  - search-loop
  - design
  - source-of-truth
sources:
  - "README.md"
  - "alphaevolve_method_translation.md"
  - "phase4_sampling_policy_v1.md"
  - "universe_and_split_policy.md"
  - "program_database_schema.md"
  - "evaluator_contract.md"
---
# Phase 4 Task 001 Search Design

## Objective

Define the first bounded AlphaEvolve-style search loop before generating child candidates at scale.

This task is the design source of truth. Task 004 implements this task; it does not replace it.

## Starting Root

Use:

```text
CAND-20260423-001
```

The duplicate-policy child should be inherited as the data-cleaning baseline for future reversal-family candidates.

## First-Loop Decisions

```yaml
first_loop:
  data_scope: daily_stock_only
  universe_policy: rolling_top500_market_cap_v1
  split_policy: daily_stock_top500_is_2011_2022_os_2023_2025_v1
  in_sample: 2011-01-01_to_2022-12-31
  out_sample: 2023-01-01_to_latest_2025_date
  generator: Qwen3.5-9B
  repair_model: Qwen3.5-9B
  qwen_execution_location: remote_linux_gpu_server_only
  program_database: SQLite
  audit_log: JSONL
  test_set_use: forbidden_until_branch_freeze
```

## Required Program Interface

The first true seed must expose:

- one or more `# EVOLVE-BLOCK-START` / `# EVOLVE-BLOCK-END` regions;
- stable skeleton outside evolve blocks for data loading, duplicate policy, timing, splits, costs, diagnostics, and artifact writing;
- `evaluate(eval_inputs) -> dict[str, float]` wrapper or adapter;
- scalar metrics where higher is better;
- descriptors for diversity sampling;
- strict SEARCH/REPLACE diff format.

Early evolve blocks may include:

- signal construction;
- ranking transforms;
- portfolio construction;
- turnover control;
- concentration control;
- native daily-stock grouping/liquidity controls.

Early evolve blocks may not include:

- fixed IS/OS split dates;
- rolling top-500 universe logic;
- raw data paths;
- duplicate policy;
- cost-accounting removal;
- artifact completeness checks;
- broker, IBKR, TWS, account, order, or position logic.

## Prompt Contract

Every child-generation prompt must include:

- parent program or bounded slice;
- allowed mutation surface;
- immutable rules;
- parent prompt-card;
- inspiration prompt-cards;
- evaluator feedback;
- dataset and cost context;
- exact SEARCH/REPLACE example;
- instruction that SEARCH must stay strictly inside evolve blocks.

Use [prompt_contracts.md](prompt_contracts.md).

## Sampling Policy

Use [phase4_sampling_policy_v1.md](phase4_sampling_policy_v1.md).

The first 200 to 300 children use these islands:

```yaml
active_islands:
  daily_stock_signal: 0.45
  ranking_transform: 0.15
  portfolio_risk_turnover: 0.20
  neutralization_liquidity: 0.10
  repair_near_miss: 0.05
  negative_control: 0.05
```

Dataset-feature additions are disabled until review unlocks them.

## Evaluator Cascade

```yaml
evaluator_cascade:
  controller_static:
    - parse SEARCH/REPLACE
    - exact unique SEARCH match
    - inside evolve block
    - forbidden edit checks
    - AST/name checks
    - compile
    - vector smoke

  toy_eval:
    - synthetic in-memory data
    - strategy function shape
    - vector behavior
    - evaluator summary schema

  remote_sample_eval:
    - 2011-2025 IS/OS daily-stock sample
    - enough names per side
    - score not constant
    - turnover not pathological
    - compact artifacts exist

  remote_stage0_eval:
    - full IS/OS comparison
    - parent comparison
    - matched-turnover null
    - cost grid
    - concentration
    - subperiod check

  remote_full_validation:
    - full IS/OS evaluator battery
    - complete artifact bundle
    - cost sensitivity
    - null distribution
    - liquidity and sector buckets
    - concentration diagnostics
```

## Storage and Artifacts

Use [program_database_schema.md](program_database_schema.md) and [artifact_renderer_contract.md](artifact_renderer_contract.md).

Each child attempt must be recorded, including failures.

## Acceptance Criteria

Task 001 design is satisfied when:

- Task 004 can implement a seed program without changing this design;
- split and universe policies are fixed before child generation;
- program database schema exists;
- prompt contracts exist;
- evaluator contract exists;
- sampling policy exists;
- dataset admission policy exists;
- Codex has a concrete implementation task list.
