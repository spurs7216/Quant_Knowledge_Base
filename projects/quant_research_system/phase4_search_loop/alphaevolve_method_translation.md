---
title: Phase 4 AlphaEvolve Method Translation
type: project
status: active
updated: 2026-04-29
tags:
  - project
  - phase4
  - alphaevolve
  - search-loop
  - qwen
sources:
  - "AlphaEvolve - A coding agent for scientific and algorithmic discovery.pdf"
  - "README.md"
  - "task_001_search_design.md"
  - "phase4_sampling_policy_v1.md"
  - "program_database_schema.md"
  - "evaluator_contract.md"
---
# Phase 4 AlphaEvolve Method Translation

## Core Correction

The unit of evolution is an executable program, not a parameter grid and not a remote validation batch.

The transferable loop is:

```text
parent_program, inspirations = database.sample()
prompt = prompt_sampler.build(parent_program, inspirations)
diff = llm.generate(prompt)
child_program = apply_diff(parent_program, diff)
results = evaluator.execute(child_program)
database.add(child_program, results)
```

For this project:

- Task 001 is the search-design source of truth.
- Task 002 is a pre-evolution evaluator seed, not the loop itself.
- Task 003 supplies code-control primitives.
- Task 004 implements the first seed strategy program and remote Qwen-integrated controller loop.

## Paper-To-System Mapping

| AlphaEvolve element | Quant-system counterpart |
| --- | --- |
| Problem definition | discover robust alpha candidates under cost, null, leakage, stability, and implementation constraints |
| Initial program | executable seed strategy module, initially daily-stock reversal / Kalman innovation reversal |
| EVOLVE block | bounded function regions for signal, ranking, portfolio, turnover, risk, or admitted feature joins |
| Evaluation function | `evaluate(eval_inputs) -> dict[str, float]`, scalar scores where larger is better |
| Prompt sampler | vault-aware context builder using parent code, inspirations, wiki notes, dataset context, cost policy, and evaluator summaries |
| SEARCH/REPLACE diffs | structured generated patches applied only inside evolve blocks unless whole-block rewrite is explicitly allowed |
| LLM ensemble | measured Qwen-only stack: Qwen3.5-9B inner loop, Qwen3.5-27B-FP8 reviewer, Qwen3.6-35B-A3B-FP8 scheduled deep model |
| Evaluator pool | `controller_static`, `toy_eval`, `remote_sample_eval`, `remote_stage0_eval`, `remote_full_validation`, artifact review |
| Program database | search-facing memory of programs, code hashes, prompts, diffs, scores, diagnostics, descriptors, lineage, and failure reasons |
| Evolution policy | data-aware MAP-Elites + islands + validation-overuse penalties |
| Distributed controller | serial first; asynchronous later when interfaces are stable |

## Quant-Specific Constraint

AlphaEvolve works best when candidates can be automatically evaluated. Quant alpha research is machine-gradeable but noisy and easy to overfit.

Therefore, Phase 4 must add protections not emphasized in generic algorithmic benchmarks:

- fixed chronological splits;
- rolling point-in-time universe;
- strict cost grid;
- matched-turnover nulls;
- liquidity and sector buckets;
- concentration diagnostics;
- point-in-time join checks;
- validation-overuse penalties;
- branch freeze before test evaluation.

## Initial Abstraction Level

Use direct executable strategy artifacts first.

Do not start with:

- whole-codebase evolution;
- opaque ML model search;
- option/fundamental/event features;
- general RL training;
- notebook rewrites.

Start with:

```text
seed_strategy_module.py
  compute_signal()
  rank_or_transform_signal()
  construct_portfolio()
  apply_risk_controls()
  evaluate()
```

The evaluator and skeleton own data loading, split policy, universe policy, duplicate policy, costs, and artifact writing.

## Multiple Scores

Use multiple scalar scores for search, but keep hard gates separate.

Scalar scores:

- validation net Sharpe;
- validation net return;
- negative turnover;
- negative cost drag;
- negative concentration;
- parent delta;
- null delta;
- subperiod stability;
- liquidity robustness;
- novelty.

Hard gates:

- leakage;
- split change;
- universe change;
- cost-policy change;
- duplicate-policy change;
- broker logic;
- point-in-time join failure;
- nonfinite returns;
- too few names;
- missing artifacts.

## Program Database

The program database should not sample only by Sharpe.

It should store:

- program text or path;
- diff;
- prompt;
- model role and settings;
- metrics;
- hard gates;
- descriptors;
- validation exposure;
- artifact paths;
- failure reason;
- lineage.

It should sample by:

- adjusted selection score;
- MAP-Elites cell coverage;
- island population;
- novelty;
- near-miss repair value;
- negative-control relevance;
- validation exposure.

## Prompt Sampling

Every prompt should include:

- parent code;
- allowed mutation surface;
- immutable rules;
- parent prompt-card;
- inspiration prompt-cards;
- relevant evaluator summaries;
- dataset/cost context;
- strict SEARCH/REPLACE example.

The prompt sampler should not dump large raw artifacts into context.

## Evaluation Cascade

```text
controller_static
-> toy_eval
-> remote_sample_eval
-> remote_stage0_eval
-> remote_full_validation
-> candidate registry review
-> branch freeze
-> test evaluation, if unlocked
```

The test set is never part of ordinary search feedback.
