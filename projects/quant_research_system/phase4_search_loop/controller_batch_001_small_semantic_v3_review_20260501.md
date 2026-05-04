---
title: Phase 4 Controller Batch 001 Small Semantic V3 Review
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
  - "current_state.md"
  - "controller_batch_001_small_semantic_v2_review_20260501.md"
superseded_by: "current_state.md"
---
# Phase 4 Controller Batch 001 Small Semantic V3 Review

> Current compact state: [current_state.md](current_state.md). This dated note is retained as supporting evidence for the no-thinking controller batch and duplicate bottleneck.

## Artifact

Reviewed local artifact:

```text
artifacts/controller_batch_001_small_semantic_v3.zip
```

Extracted review copy:

```text
artifacts/controller_batch_001_small_semantic_v3_review_20260501/controller_batch_001_small_semantic_v3/
```

## Summary

```yaml
attempt_count: 10
pass_count: 7
raw_parse_pass_rate: 1.0
exact_search_match_rate: 1.0
evolve_block_safe_rate: 1.0
apply_pass_rate: 1.0
compile_pass_rate: 1.0
vector_smoke_pass_rate: 1.0
portfolio_semantic_pass_rate: 1.0
unique_child_pass_rate: 0.7
duplicate_child_count: 3
db_insert_pass_rate: 1.0
empty_retry_rate: 0.0
reasoning_only_empty_count: 0
max_initial_response_reasoning_length: 0
failure_categories:
  duplicate_child: 3
remote_sample_eval_launched: false
full_validation_launched: false
```

Interpretation:

- The null-content / reasoning-only failure was fixed for this run.
- All generated outputs had final content and zero recorded reasoning text.
- All non-duplicate children passed parse, exact match, evolve-block, compile, vector-smoke, and portfolio semantic gates.
- The remaining controller-quality bottleneck is duplicate generation, not malformed output or semantic invalidity.

## Token And Thinking-Mode Lesson

The prior null response was not solved mainly by increasing `max_tokens`. It was solved by disabling Qwen thinking mode correctly in the raw vLLM HTTP payload:

```json
"chat_template_kwargs": {"enable_thinking": false}
```

This field must be sent at the top level of the request body for the direct HTTP router. Putting it under SDK-style `extra_body` did not reliably disable thinking for this raw client.

The controller also records `content_was_null` and `reasoning_length`, and retries once when final content is empty.

After reviewing the actual output sizes, the active completion budget is set below the initially discussed 16k budget:

```yaml
max_tokens: 8192
```

Because vLLM counts prompt tokens plus completion tokens under `--max-model-len`, the 9B server configuration should use a larger context window when memory allows:

```yaml
max_model_len: 32768
max_num_seqs: 1
```

## Attempt Pattern

Accepted unique children:

- `attempt_000`: signal dampening with `signal * tanh(signal / 2.0)`.
- `attempt_001`: ranking sign flip.
- `attempt_002`: portfolio refactor preserving equal long/short side weights.
- `attempt_003`: risk max-weight dampening.
- `attempt_004`: signal soft sign dampening.
- `attempt_007`: risk dampening variant.
- `attempt_008`: signal clipped-magnitude dampening.

Rejected duplicates:

- `attempt_005`: duplicate of `attempt_001`.
- `attempt_006`: duplicate of `attempt_002`.
- `attempt_009`: duplicate of `attempt_001`.

## Next Implication

Do not launch child `remote_sample_eval` from this batch yet. The controller is now format- and semantic-safe, but it still needs stronger duplicate avoidance or duplicate-retry logic before scaling.

The next controller improvement should treat `duplicate_child` as a repairable category: after computing the child hash, ask Qwen once for a different same-surface patch using the duplicate's raw patch as a negative example.
