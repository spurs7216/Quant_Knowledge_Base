---
title: Phase 4 Readthrough
type: project
status: archived
updated: 2026-04-29
tags:
  - project
  - phase4
  - readthrough
  - design-review
sources:
  - "README.md"
  - "CHANGELOG.md"
  - "../phase4_codex_clarifications.md"
superseded_by: "current_state.md"
---
# Phase 4 Readthrough

> Current compact state: [current_state.md](current_state.md). This dated readthrough is retained as the old-plan comparison and adoption record. Its split-policy discussion is superseded by [is_os_evaluation_policy_20260519.md](is_os_evaluation_policy_20260519.md).

## Bottom Line

The clarified package is a material upgrade over the old Phase 4 plan. It is now the active Phase 4 control package, with the remote-Qwen clarification applied.

The old plan correctly separated a remote validation batch from the true AlphaEvolve loop, but it was still too light on production details. The clarified plan fixes the missing operating contracts:

- daily-stock-only first production loop;
- rolling point-in-time top-500 market-cap universe;
- then-planned chronological split discipline, later superseded by fixed IS/OS;
- Qwen-only measured model stack;
- SQLite program database plus JSONL audit log;
- data-aware MAP-Elites plus island sampling;
- prompt, artifact-renderer, remote CSV, processed-output, and dataset-admission policies;
- explicit Task 004 seed-program and Qwen-loop implementation task.

Clarification applied on 2026-04-29: local Windows cannot run Qwen. All Qwen calls and AlphaEvolve-lite controller/evaluator stages run on the remote Linux/GPU/data server.

## What Changed From The Old Plan

### Search Scope

Old plan:

- AlphaEvolve-like loop was defined in principle.
- First search family was daily-stock reversal / Kalman innovation reversal.
- Dataset additions were allowed if declared.

Clarified package:

- First production loop is explicitly `daily_stock_only`.
- Dataset-feature additions are locked until the daily-stock loop has stable local and sample-evaluation behavior.
- Native daily-stock fields remain usable for liquidity and sector/industry grouping.

### Universe And Split

Old plan:

- Required chronological split discipline, but did not fix the exact universe and split policy.

Clarified package:

- Requires rolling top-500 by lagged market cap, recomputed monthly from prior-month-end information.
- Required chronological split over sorted unique trading dates at the time. This is superseded by fixed IS/OS as of 2026-05-19.

This is a major improvement because it closes a large survivorship and validation-leakage channel before search starts.

### LLM Stack

Old plan:

- Preferred a Qwen/Gemma ensemble, with Gemma for diversity and critique.

Clarified package:

- Retires Gemma 4 from the active stack.
- Uses Qwen3.5-9B for inner-loop generation and repair.
- Uses Qwen3.5-27B-FP8 for optional medium review.
- Uses Qwen3.6-35B-A3B-FP8 only for scheduled deep review.
- Keeps deterministic Python as the mandatory micro-filter.

This is consistent with the measured remote vLLM notes in the clarified package. The evaluator, not the model, remains the authority.

### Program Database

Old plan:

- Started with an inspectable JSONL program database.

Clarified package:

- Uses SQLite for searchable program metadata.
- Keeps JSONL as the append-only audit log.
- Adds tables for programs, prompts, evaluations, MAP cells, validation exposure, and dataset admissions.

I updated the active schema so runtime SQLite and audit files live under `artifacts/phase4_alphaevolve/`, not under tracked source-code paths.

### Sampling

Old plan:

- Mentioned exploration/exploitation and descriptors.

Clarified package:

- Defines `phase4_sampling_v1` as data-aware MAP-Elites plus island sampling.
- Adds validation-overuse penalties, novelty, correlation redundancy, coverage-shrinkage penalties, repair loops, and negative controls.
- Defines the first 200 to 300 child island weights.

This is much closer to the AlphaEvolve database role than a best-Sharpe leaderboard.

### Evaluator And Artifacts

Old plan:

- Required cost, nulls, concentration, and dataset diagnostics.

Clarified package:

- Adds concrete artifact contracts: `evaluator_summary.json`, `prompt_card.md`, `failure_report.md`, and `search_state_summary.json`.
- Requires compact prompt-facing summaries rather than large CSV dumps.
- Adds validation-exposure accounting and branch-freeze/test unlock logic.

## Adopted Modifications

I made the clarified markdown package the active folder:

```text
projects/quant_research_system/phase4_search_loop/
```

I also added a config copy at:

```text
projects/quant_research_system/phase4_search_loop/configs/phase4_stage0_remote_qwen.yaml
```

I made these small corrections while adopting it:

- Native `daily_stock` industry fields are now explicitly allowed in Stage 0 because the active search policy already activates `neutralization_liquidity` and Task 002 includes a native industry-neutral variant.
- Runtime database and audit files are now documented as artifact outputs under `artifacts/phase4_alphaevolve/`, not tracked source files under `research/alphaevolve_lite/db/`.
- The README now says the 50-child Qwen batch uses the remote server's localhost vLLM API, avoiding confusion with local Windows execution.
- Stage naming now uses `controller_static` instead of `local_static`.
- The remote Qwen config path comment now points to the active project folder.

## Vague Or Still Unresolved Parts

1. The active package reports measured Qwen results, but the artifact path for those tests is not named in the active package. It would be better to link the exact remote smoke-test artifacts or create a short review note under `artifacts/` or `projects/`.

2. Resolved: the phrase `local_static` is deprecated. New executable stages should use `controller_static`; the deprecated alias may be accepted temporarily with a warning.

3. The exact `daily_stock` field names and value filters for common equity, major exchanges, price, shares outstanding, and next-return availability still need sample/EDA verification before implementation.

4. The split policy says to compute boundaries from sorted unique trading dates after global cleaning and date coverage checks. We still need to define whether this is before or after rolling-top-500 universe construction. My preference: compute split dates from cleaned `daily_stock` trading dates before candidate logic, then apply universe membership inside each split.

5. The rolling top-500 policy needs a missing-return convention for disappearing names. The note says not to forward-fill returns, but the exact PnL treatment for names disappearing after position formation should be encoded in the evaluator.

6. The cost model is still a proportional placeholder. This is acceptable for Stage 0, but high-turnover candidates should not be promoted until liquidity-conditioned spread/impact modeling is added.

7. Resolved: dataset additions require human approval before executable multi-dataset generation. Codex may write reviews and recommendations, but may not create the final unlock approval file unless explicitly instructed.

## Current Recommendation

The right next engineering step is not to generate strategy variants. It is to implement the clarified Task A through Task H sequence:

1. create the missing AlphaEvolve-lite modules;
2. implement SQLite program database and JSONL audit;
3. implement rolling universe and split builders;
4. implement seed strategy module with evolve blocks;
5. insert the generation-zero seed.

Only after that should the remote Qwen controller loop attempt 50 child patches.
