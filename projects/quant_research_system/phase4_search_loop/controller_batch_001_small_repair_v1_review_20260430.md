---
title: Phase 4 Controller Batch 001 Small Repair V1 Review
type: project
status: archived
updated: 2026-04-30
tags:
  - project
  - phase4
  - alphaevolve
  - controller-static
  - qwen
sources:
  - "controller_batch_001_small_review_20260430.md"
  - "controller_child_dry_run_20260430.md"
superseded_by: "current_state.md"
---
# Phase 4 Controller Batch 001 Small Repair V1 Review

> Current compact state: [current_state.md](current_state.md). This dated note is retained as supporting evidence for the repair-enabled controller batch.

## Artifact

Reviewed local artifact:

```text
artifacts/controller_batch_001_small_repair_v1.zip
```

Extracted review copy:

```text
artifacts/controller_batch_001_small_repair_v1_review_20260430/controller_batch_001_small_repair_v1
```

## Summary

The repair-enabled small run fixed the prior format failure.

```yaml
attempt_count: 5
pass_count: 5
raw_parse_pass_rate: 1.0
repair_attempt_rate: 0.0
exact_search_match_rate: 1.0
evolve_block_safe_rate: 1.0
apply_pass_rate: 1.0
compile_pass_rate: 1.0
vector_smoke_pass_rate: 1.0
db_insert_pass_rate: 1.0
failure_categories: {}
```

Interpretation:

- prompt slicing worked;
- Qwen generated strict inside-block patches;
- database insertion worked;
- no repair pass was needed.

## Accepted Patch Review

```yaml
attempt_000:
  target_surface: signal
  idea: flip signal sign after volatility scaling
  status: plausible unique child

attempt_001:
  target_surface: ranking
  idea: flip ranked signal direction
  status: plausible but semantically close to attempt_000

attempt_002:
  target_surface: portfolio
  idea: signal-strength weighted selected tails
  status: unsafe despite vector-smoke pass
  reason: short-side negative signals became positive weights

attempt_003:
  target_surface: risk
  idea: reduce side normalization from 0.5 to 0.3
  status: controller-safe, but should be treated as risk/gross-change child

attempt_004:
  target_surface: signal
  idea: exact duplicate of attempt_000
  status: duplicate child
```

Additional local diagnostic found for `attempt_002`:

```yaml
positive_weight_count: 408
negative_weight_count: 0
mean_net_exposure: 0.16
max_abs_net_exposure: 0.16
side_sign_bad_count: 204
```

This child should not reach historical evaluation.

## Implemented Follow-Up

Controller hardening added after this review:

- `micro_filter` now supports `target_surface` and rejects patches outside that specific evolve block;
- portfolio semantic smoke checks now reject one-sided books, large net exposure, sign-inconsistent weights, excessive gross exposure, and max-weight breaches;
- `run_child_batch.py` records `portfolio_semantic_pass_rate`, `unique_child_pass_rate`, and `duplicate_child_count`;
- duplicate child-program hashes are marked as `duplicate_child` rather than counted as unique passes;
- generation prompts include prior accepted patches for the same target surface to discourage repeated sign flips;
- `remote_sample_eval.py` now accepts `--program-path` so generated `child_program.py` files can be evaluated directly.

Local verification:

```yaml
bad_portfolio_child:
  previous_status: passed vector smoke
  new_status: reject
  failure_category: portfolio_semantic_failed
  failure_reason: net exposure too large

target_surface_mismatch:
  ranking_patch_with_ranking_target: pass
  ranking_patch_with_signal_target: reject

duplicate_sign_flip_mock:
  duplicate_child_count: 1
  unique_child_pass_rate: 0.2

marker_oversize_repair_mock:
  repair_attempt_rate: 1.0
  repair_success_rate: 1.0
  portfolio_semantic_pass_rate: 1.0
```

## Next Remote Run

Run another small controller batch before scaling:

```bash
python research/alphaevolve_lite/scripts/run_child_batch.py \
  --program-path research/alphaevolve_lite/seeds/kalman_reversal_seed.py \
  --evaluator-summary artifacts/phase4_alphaevolve/remote_sample_eval_seed_v2/evaluator_summary.json \
  --out-dir artifacts/phase4_alphaevolve/controller_batch_001_small_semantic_v2 \
  --db-path artifacts/phase4_alphaevolve/program_database.sqlite \
  --attempts 10 \
  --model-role fast_generator \
  --max-tokens 4096
```

Do not run child historical evaluation from this small rerun. If it produces several unique semantic-pass children, the next step is a 50-attempt controller batch.
