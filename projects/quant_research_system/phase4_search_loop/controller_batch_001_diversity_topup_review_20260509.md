---
title: Controller Batch 001 Diversity Top-Up Review
type: project
status: active
updated: 2026-05-09
tags:
  - project
  - phase4
  - alphaevolve
  - controller-static
  - artifact-review
sources:
  - "artifacts/controller_batch_001_diversity_topup.zip"
  - "controller_batch_001_review_20260509.md"
  - "current_state.md"
---
# Controller Batch 001 Diversity Top-Up Review

## Decision

The diversity top-up did its main job. It added 13 unique controller-static pass children from 20 attempts after seeding the prior 35 pass children from `controller_batch_001`, bringing the aggregate unique controller-static population to 48. The pre-market controller population gate is now satisfied.

This is still not market validation. The next stage should be a small, curated `remote_sample_eval` over a diverse subset of controller-static pass children, not another broad controller-only generation run.

## Artifact

```text
artifacts/controller_batch_001_diversity_topup.zip
```

## Key Metrics

```yaml
attempt_count: 20
pass_count: 13
prior_pass_count: 35
aggregate_unique_controller_pass_children: 48
unique_child_pass_rate: 0.65
duplicate_child_count: 2
duplicate_patch_fingerprint_count: 1
near_duplicate_patch_count: 0
duplicate_retry_attempt_rate: 0.40
duplicate_retry_success_rate: 0.625
map_cell_count: 9
raw_parse_pass_rate: 1.0
exact_search_match_rate: 1.0
evolve_block_safe_rate: 1.0
apply_pass_rate: 1.0
compile_pass_rate: 1.0
vector_smoke_pass_rate: 0.95
portfolio_semantic_pass_rate: 0.80
empty_retry_rate: 0.0
reasoning_only_empty_count: 0
db_insert_pass_rate: 1.0
remote_sample_eval_launched: false
full_validation_launched: false
```

## What Worked

- Prior-summary seeding worked: previously accepted child hashes and patch fingerprints were used during the top-up.
- The ranking duplicate pocket was materially reduced. The prior 50-attempt batch had 15 duplicate rejects, mostly `ranking/direction_flip`; the 20-attempt top-up had only 3 duplicate-style rejects.
- Qwen no longer produced reasoning-only null final content in this run.
- Database insertion, SEARCH/REPLACE parsing, evolve-block containment, apply, and compile stayed healthy.
- Reasoning memory, diagnostic reports, skill updates, and group-relative summaries were emitted.

## Failure Concentration

```yaml
portfolio_semantic_failed:
  count: 3
  concentration: signal/time_smoothing
  repeated_patch: "signal = signal * np.exp(-np.abs(signal) / 2.0)"
  diagnosis: "This is a nonlinear magnitude dampener, not time smoothing. It can reorder ranked signals enough to produce sign-disagreeing portfolio weights."

vector_smoke_failed:
  count: 1
  concentration: portfolio/no_trade_band_or_sparsity
  diagnosis: "The generated sparse-book patch used a boolean Series from valid['signal'] directly against weights.loc, causing an unalignable boolean indexer."

duplicate_style_rejects:
  count: 3
  diagnosis: "Much smaller than the prior duplicate problem. Still useful as negative evidence for prompt-card fitness."
```

## Additional Local Finding

The artifact exposed an accounting bug in the MAP descriptor layer: patch intent was classified from the full replacement block, so unchanged context lines could dominate the intent label. Examples:

- a real EWM time-smoothing patch was labeled `history_confidence_weighting` because the unchanged `history >= min_history` line remained in the replacement block;
- risk patches were over-labeled as `side_renormalization` because unchanged `long_sum` / `short_sum` lines remained in the replacement block;
- ranking shrinkage via `scale + constant` was under-labeled as `ranking_other`.

The fix is to classify intent from changed replacement lines, not from the whole replacement block.

After local reclassification, 9 of the 13 pass children are target-intent matches. Four controller-safe children are useful database evidence but should receive reduced prompt-card credit because they landed off target.

## Applied Local Fix

The local scaffold now:

- classifies patch intent from changed replacement lines;
- adds `target_intent_match_rate` and `target_intent_mismatch_pass_count` to batch summaries;
- penalizes controller-safe but off-target children in prompt-card fitness instead of treating them as full target-cell successes;
- adds a diagnostic card for target-intent mismatch;
- adds prompt, reasoning-memory, and skill-library guidance for:
  - binding target intent;
  - pandas boolean mask alignment;
  - not substituting nonlinear dampening for signal time smoothing.
- aligns `remote_sample_eval.py` with the active cost policy: the central total cost remains `2.5` bps, and the default cost grid now includes `10` bps as a severe stress scenario.

## Next Step

After this patch is synchronized to the remote machine, run a curated `remote_sample_eval` on a small diverse subset of controller-static pass children. Do not evaluate all 48 children blindly.

Prioritize children that are target-compliant, nontrivial, and not merely cosmetic exposure dampening. Good first candidates from the top-up are:

```yaml
controller_batch_001_diversity_topup_candidates:
  - attempt_000: "ranking / robust_center_scale: median absolute deviation scale"
  - attempt_004: "ranking / shrinkage_transform: divide by scale + 0.01"
  - attempt_010: "portfolio / no_trade_band_or_sparsity: repaired sparse signal-weighted sides"
  - attempt_011: "risk / small_book_guard: damp small long/short books"
  - attempt_017: "signal / time_smoothing: causal EWM smoothing"
```

Avoid using controller smoke-test Sharpe as selection evidence. The controller smoke panel is only an invariant test, not market evidence.
