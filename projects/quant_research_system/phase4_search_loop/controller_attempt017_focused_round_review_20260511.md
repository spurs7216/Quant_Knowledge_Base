---
title: Controller Attempt017 Focused Round Review 2026-05-11
type: project
status: active
updated: 2026-05-11
tags:
  - project
  - phase4
  - alphaevolve
  - controller
  - evaluator
sources:
  - "../../artifacts/controller_attempt017_focused_round_20260511.zip"
  - "controller_evaluator_hardening_smoke_review_20260511.md"
  - "current_state.md"
---
# Controller Attempt017 Focused Round Review 2026-05-11

## Decision

No promotion.

The focused controller round produced one target-matched child worth a single sample evaluation, `PROG-20260511-A017-FOCUS-0000`. The remote decision was also no promotion: the child improved missing-held-weight behavior, but failed parent-relative performance and turnover-aware criteria badly. Full validation remains too early and was not run.

The separate sample-eval artifact named `remote_sample_eval_controller_attempt017_focused_round_attempt_000_20260511` was not present in the local `artifacts/` folder at review time. This note records the controller artifact plus the remote machine decision; exact sample-eval metrics should be filled in if that artifact is later added.

## Controller Round

Artifact:

```text
artifacts/controller_attempt017_focused_round_20260511.zip
```

Key controller metrics:

```yaml
attempt_count: 12
pass_count: 3
unique_child_pass_rate: 0.25
raw_parse_pass_rate: 1.0
exact_search_match_rate: 0.9166666666666666
evolve_block_safe_rate: 0.9166666666666666
apply_pass_rate: 0.9166666666666666
compile_pass_rate: 0.9166666666666666
vector_smoke_pass_rate: 0.9166666666666666
portfolio_semantic_pass_rate: 0.9166666666666666
behavior_delta_pass_rate: 0.3333333333333333
behavioral_noop_count: 7
duplicate_child_count: 0
duplicate_patch_fingerprint_count: 0
near_duplicate_patch_count: 1
target_intent_match_rate: 0.3333333333333333
target_intent_mismatch_pass_count: 2
map_cell_count: 3
db_insert_pass_rate: 1.0
reasoning_only_empty_count: 0
```

Controller mechanics are still healthy: no empty Qwen outputs, no duplicate child concentration, and database insertion worked. The main failure is search quality. Seven attempts were behavioral no-ops, one failed exact SEARCH matching, and one direction-flip-style child was rejected as a near duplicate.

## Pass Children

`attempt_000` / `PROG-20260511-A017-FOCUS-0000`:

```yaml
surface: signal
target_intent: bounded_tanh_dampening
patch_intent: bounded_tanh_dampening
target_intent_match: true
controller_search_score: 1.0
behavior: material signal, ranking, and portfolio delta
gross_delta_bucket: no_gross_delta
net_exposure_bucket: balanced
sample_eval_decision: no_promotion
```

This was the only target-matched controller pass and therefore the only reasonable sample-eval candidate. Its final patch was:

```python
signal = signal * np.tanh(signal * 0.7)
```

The controller smoke showed a material behavior delta:

```yaml
active_position_jaccard: 0.3333333333333333
active_position_symmetric_diff_count: 408.0
signal_max_abs_delta: 117.48991604909739
ranked_signal_max_abs_delta: 4.36940983387877
weight_max_abs_delta: 0.04
max_abs_gross_exposure_delta: 0.0
max_abs_net_exposure_delta: 0.0
```

However, the smoke-panel daily Sharpe was already negative:

```yaml
eval_daily_sharpe: -1.2166169172931935
mean_gross_exposure: 0.16
max_weight: 0.02
```

`attempt_003` and `attempt_006` were controller passes but off target:

```yaml
attempt_003:
  target_intent: direction_flip
  patch_intent: signal_other
  target_intent_match: false
attempt_006:
  target_intent: direction_flip
  patch_intent: clipped_magnitude_dampening
  target_intent_match: false
```

They should remain database evidence only.

## Interpretation

The new result is useful negative evidence. It shows the search can improve an evaluator risk diagnostic, missing-held weight, while destroying the parent-relative economics. That means missing-held-weight should stay a hard gate / diagnostic, not become a single-objective target.

The failure also says the current attempt017-focused prompt is still too easy for Qwen to satisfy with generic nonlinear signal magnitude transformations. `bounded_tanh_dampening` and `clipped_magnitude_dampening` can create material portfolio deltas, but that does not imply alpha improvement.

Important lessons:

- Improving missing-held weight alone is not promotion evidence.
- Generic signal dampening should be treated as controller-safe but market-unproven, and now has negative sample-eval evidence in the attempt017 branch.
- The next prompt should ask for a mechanism that preserves or improves parent-relative return and turnover-aware score while addressing missing-held risk, not for generic signal compression.
- Portfolio and risk prompt cards are still producing many no-ops after downstream controls; they need stronger behavior-survival requirements before another focused run.

## Next Step

Do not run full validation. Do not stage-0 validate. Do not sample-evaluate more children from this round.

The local search-control patch is now implemented. It injects this negative sample-eval lesson into the prompt, reasoning-memory, and skill-library layers:

```yaml
next_local_patch:
  status: complete
  add_attempt000_negative_sample_eval_memory: implemented
  mark_generic_signal_dampening_as_market_unproven_for_attempt017: implemented
  strengthen_missing_held_prompt: "implemented; must preserve parent-relative turnover-aware score and broad-sample Sharpe"
  strengthen_portfolio_risk_noop_avoidance: implemented
  avoid_full_validation: true
```

The next remote run should be another small controller-only focused round, not broad evaluation. Sample-evaluate at most one child, and only if it is target-matched, behaviorally nontrivial, and plausibly improves both missing-held risk and parent-relative performance.
