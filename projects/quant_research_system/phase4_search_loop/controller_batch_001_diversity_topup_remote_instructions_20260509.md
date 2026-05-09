---
title: Controller Batch 001 Diversity Top-Up Remote Instructions
type: project
status: active
updated: 2026-05-09
tags:
  - project
  - phase4
  - alphaevolve
  - controller-static
  - remote-run
sources:
  - "controller_batch_001_review_20260509.md"
  - "current_state.md"
---
# Controller Batch 001 Diversity Top-Up Remote Instructions

## Purpose

Run a controller-only diversity top-up after `controller_batch_001`.

This is still not a market evaluation. The goal is to verify that the patched prompt, controller state seeding, `controller_population_policy_v2`, and `prompt_fitness_and_lazy_score_v1` reduce duplicate generation, especially the `ranking/direction_flip` pocket, while preserving the healthy controller mechanics from the 50-attempt batch.

## Preflight

1. Pull the latest GitHub state after the local patch is pushed.
2. Keep the existing remote artifact directory available:

```text
artifacts/phase4_alphaevolve/controller_batch_001/summary.json
```

3. Start Qwen/vLLM in a persistent terminal or `tmux` pane.
4. From a separate terminal, verify `/health` and `/v1/models`.
5. Do not launch `remote_sample_eval`, full validation, test-set evaluation, IBKR, TWS, account-state, position, order, or credential logic.

## Command

Run from the repository root on the remote Linux/GPU/data machine:

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

If `remote_sample_eval_refactor_smoke_20260507/evaluator_summary.json` is missing, use the behavior-equivalent seed-v2 evaluator summary:

```bash
--evaluator-summary artifacts/phase4_alphaevolve/remote_sample_eval_seed_v2/evaluator_summary.json
```

## Return Artifacts

Return a compact archive containing:

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
artifacts/phase4_alphaevolve/controller_batch_001_diversity_topup/attempt_*/prompt.md
artifacts/phase4_alphaevolve/controller_batch_001_diversity_topup/attempt_*/raw_output.txt
artifacts/phase4_alphaevolve/controller_batch_001_diversity_topup/attempt_*/duplicate_retry_*_output.txt
artifacts/phase4_alphaevolve/controller_batch_001_diversity_topup/attempt_*/micro_filter_result.json
```

## Review Gates

```yaml
controller_batch_001_diversity_topup:
  attempt_count: 20
  prior_summary_loaded: true
  prior_pass_count: 35
  unique_semantic_pass_children: "at least 12 of 20"
  aggregate_unique_children_with_controller_batch_001: "at least 45"
  duplicate_child_count: "materially below 15/50; target <= 5/20"
  near_duplicate_patch_count: "reported; lower is better"
  ranking_direction_flip_duplicate_pocket: "reduced"
  population_policy_version: "controller_population_policy_v2"
  prompt_fitness_policy_version: "prompt_fitness_and_lazy_score_v1"
  prompt_card_duplicate_counts: "reported"
  prompt_card_fitness: "reported in summary.json and population_policy_state.json"
  prompt_card_lazy_penalty_sums: "reported"
  controller_search_score_mean: "reported"
  lazy_penalty_attempt_count: "reported"
  low_prompt_card_fitness_diagnostic: "reported if triggered"
  intent_duplicate_counts: "reported"
  raw_parse_pass_rate: 1.0
  exact_search_match_rate: 1.0
  evolve_block_safe_rate: 1.0
  compile_pass_rate: 1.0
  vector_smoke_pass_rate: 1.0
  portfolio_semantic_pass_rate: 1.0
  db_insert_pass_rate: "near 1.0"
  reasoning_only_empty_count: 0
  remote_sample_eval_launched: false
  full_validation_launched: false
```

If the top-up passes, the next local action is selecting a small diverse subset for `remote_sample_eval`. If it fails, inspect target-intent compliance in ranking prompts before changing evaluator gates.
