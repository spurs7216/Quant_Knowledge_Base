---
title: Phase 4 Controller Batch 001 Small Semantic V2 Review
type: project
status: archived
updated: 2026-05-01
tags:
  - project
  - phase4
  - alphaevolve
  - controller-static
  - qwen
sources:
  - "controller_batch_001_small_repair_v1_review_20260430.md"
  - "controller_child_dry_run_20260430.md"
superseded_by: "current_state.md"
---
# Phase 4 Controller Batch 001 Small Semantic V2 Review

> Current compact state: [current_state.md](current_state.md). This dated note is retained as supporting evidence for the semantic-gated controller batches.

## Artifact

Reviewed local artifact:

```text
artifacts/controller_batch_001_small_semantic_v2.zip
```

Extracted review copy:

```text
artifacts/controller_batch_001_small_semantic_v2_review_20260501
```

The zip contained two 10-attempt runs:

```text
controller_batch_001_small_semantic_v2
controller_batch_001_small_semantic_v2_verify_20260501
```

## Summary

First run:

```yaml
attempt_count: 10
pass_count: 6
raw_parse_pass_rate: 0.9
repair_attempt_rate: 0.0
exact_search_match_rate: 0.9
vector_smoke_pass_rate: 0.8
portfolio_semantic_pass_rate: 0.6
unique_child_pass_rate: 0.6
db_insert_pass_rate: 1.0
failure_categories:
  empty_output: 1
  portfolio_semantic_failed: 2
  vector_smoke_failed: 1
```

Verification run:

```yaml
attempt_count: 10
pass_count: 6
raw_parse_pass_rate: 0.8
repair_attempt_rate: 0.2
repair_success_rate: 1.0
vector_smoke_pass_rate: 0.8
portfolio_semantic_pass_rate: 0.6
unique_child_pass_rate: 0.6
db_insert_pass_rate: 1.0
failure_categories:
  empty_output: 2
  portfolio_semantic_failed: 2
```

Interpretation:

- target-surface enforcement and semantic gates worked;
- exact-match repair worked on attempts 007 and 009 in the verification run;
- database insertion remained healthy;
- six unique semantic-pass children per run is useful evidence but not enough to scale yet.

## Failure Modes

### Reasoning-Only Empty Output

Attempts 002 and 004 in the verification run spent the completion-token budget in `message.reasoning`; `message.content` was null. The controller converted null content to an empty string and rejected cleanly as `empty_output`.

Root cause:

- the direct HTTP router had placed `chat_template_kwargs` under `extra_body`, which is correct for some SDK clients but not for this raw HTTP payload;
- vLLM needs `chat_template_kwargs.enable_thinking=false` at top-level.

### Portfolio Semantic Failures

Attempt 006 repeatedly proposed signal-proportional portfolio weights where short-side negative signal values produced no effective short exposure.

Observed smoke metrics:

```yaml
mean_long_exposure: 0.16
mean_short_exposure: 0.0
max_abs_net_exposure: 0.16
side_sign_bad_count: 204
```

The semantic gate correctly rejected this.

### Signal Saturation Failure

Attempt 008 in the verification run changed the signal to:

```python
signal = np.tanh(signal / rolling_vol.clip(lower=1e-4))
```

It preserved sign direction, but created a much denser selected book and too much net exposure after risk controls:

```yaml
max_abs_net_exposure: 0.32
max_gross_exposure: 0.60
side_sign_bad_count: 0
```

This should remain rejected unless the candidate also changes portfolio/risk logic safely.

### Vector Smoke Failure

Attempt 008 in the first run used:

```python
(history / min_history).clip(max=1.0)
```

This is a local API mistake: pandas uses `upper`, not `max`.

## Implemented Follow-Up

Controller hardening added after this review:

- `model_router.py` sends `chat_template_kwargs: {"enable_thinking": false}` at top-level;
- `model_router.py` records `content_was_null` and `reasoning_length`;
- `run_child_batch.py` retries empty final content once with an explicit final-content-only prompt;
- `run_child_batch.py` reports `reasoning_only_empty_count` and max initial reasoning length;
- `run_child_batch.py` treats `vector_smoke_failed` and `portfolio_semantic_failed` as repairable once;
- prompts forbid hidden reasoning/scratchpad output;
- portfolio guidance now explicitly requires positive long magnitudes, positive short magnitudes, negative short weights, and near-zero net exposure;
- signal guidance warns against hard saturation or tied signals that create unbalanced books.

## Next Remote Run

Run another 10-attempt small controller batch:

```bash
python research/alphaevolve_lite/scripts/run_child_batch.py \
  --program-path research/alphaevolve_lite/seeds/kalman_reversal_seed.py \
  --evaluator-summary artifacts/phase4_alphaevolve/remote_sample_eval_seed_v2/evaluator_summary.json \
  --out-dir artifacts/phase4_alphaevolve/controller_batch_001_small_semantic_v3 \
  --db-path artifacts/phase4_alphaevolve/program_database.sqlite \
  --attempts 10 \
  --model-role fast_generator \
  --max-tokens 4096
```

Do not run child historical evaluation yet. If `semantic_v3` reaches roughly 8 unique semantic-pass children out of 10 and empty-output rate falls materially, scale to a 50-attempt controller batch.
