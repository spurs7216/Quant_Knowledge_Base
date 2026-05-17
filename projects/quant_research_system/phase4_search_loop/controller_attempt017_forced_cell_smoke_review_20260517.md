---
title: Controller Attempt017 Forced-Cell Smoke Review 2026-05-17
type: project
status: active
updated: 2026-05-17
tags:
  - project
  - phase4
  - alphaevolve
  - artifact-review
  - controller
sources:
  - "../../../artifacts/controller_attempt017_forced_cell_smoke_20260517.zip"
  - "controller_attempt017_forced_cell_smoke_remote_instructions_20260517.md"
  - "forced_target_cell_schedule_patch_20260517.md"
---
# Controller Attempt017 Forced-Cell Smoke Review 2026-05-17

## Verdict

The forced-cell infrastructure worked, but the batch produced no sample-eval candidate.

Do not run sample evaluation on this artifact.

## Reproducibility And Scope

```yaml
artifact: artifacts/controller_attempt017_forced_cell_smoke_20260517.zip
git_commit: aa9f74943810a27f8adeb84e0f7cecedf36dfb54
git_origin_main_commit: aa9f74943810a27f8adeb84e0f7cecedf36dfb54
git_head_matches_origin_main: true
manifest_commit_fetchable_from_github: true
remote_sample_eval_launched: false
full_validation_launched: false
mechanism_cards_enabled: false
attempt_count: 6
```

The run obeyed the exact schedule:

```yaml
target_cell_schedule_enabled: true
target_cell_schedule:
  - portfolio/liquidity_weighted_sides
  - portfolio/persistence_trade_gate
  - risk/liquidity_scaled_cap
  - risk/liquidity_scaled_cap
  - signal/liquidity_adjusted_reversal
  - signal/liquidity_adjusted_reversal
ranking_attempt_count: 0
```

## Summary Metrics

```yaml
pass_count: 2
sample_eval_candidate_count: 0
raw_parse_pass_rate: 1.0
exact_search_match_rate: 1.0
evolve_block_safe_rate: 1.0
apply_pass_rate: 1.0
compile_pass_rate: 1.0
vector_smoke_pass_rate: 0.6666666667
portfolio_semantic_pass_rate: 0.5
behavior_delta_pass_rate: 0.3333333333
target_intent_match_rate: 1.0
duplicate_child_count: 0
duplicate_patch_fingerprint_count: 0
near_duplicate_patch_count: 0
behavioral_noop_count: 1
failure_categories:
  behavioral_noop: 1
  portfolio_semantic_failed: 1
  vector_smoke_failed: 2
```

## Attempt-Level Read

| Attempt | Forced cell | Decision | Main reason |
| --- | --- | --- | --- |
| `000` | `portfolio/liquidity_weighted_sides` | reject | Liquidity side weights were absorbed; final smoke outputs were identical to parent. |
| `001` | `portfolio/persistence_trade_gate` | reject | Used `panel.loc[..., "signal"]`; `signal` is local controller data, not a panel field. |
| `002` | `risk/liquidity_scaled_cap` | reject | Short book was effectively removed; net exposure reached about `0.08`. |
| `003` | `risk/liquidity_scaled_cap` | reject | Liquidity cap scaling breached the `0.02` max-weight smoke limit. |
| `004` | `signal/liquidity_adjusted_reversal` | pass | Raw signal changed, but ranks and final weights did not; occupied MAP cell did not beat elite. |
| `005` | `signal/liquidity_adjusted_reversal` | pass | Duplicate retry produced a distinct raw-signal scale, but ranks and final weights still did not change. |

The two passes are controller-safe, not execution-effective.

## Mechanism Lessons

`liquidity_adjusted_reversal` should not use inverse raw dollar volume clipped to a narrow range. Because dollar volume is large, `1 / dollar_volume` collapses to the lower clip bound and becomes nearly uniform. That changes raw signal magnitude but not cross-sectional ranks or final weights.

`persistence_trade_gate` must compute prior signal from local `data["signal"]`, for example by creating `data["prior_signal"] = data.groupby(CONTRACT.security_id)["signal"].shift(1)` before the date loop. It must not read `panel.loc[..., "signal"]`.

`liquidity_scaled_cap` must compute per-name effective caps that never exceed `max_weight`, then clip, side-renormalize, and clip again. Cap formulas that multiply weights after side normalization can break max-weight or net-exposure constraints.

`liquidity_weighted_sides` can be absorbed by downstream max-weight clipping and side renormalization. It needs a formula that changes final side allocations after risk controls, or it should return `NO_VALID_PATCH`.

## Adopted Local Hardening

The follow-up patch adds a controller execution-effect contract:

- signal/ranking edits must change ranked signal or final weights;
- portfolio/risk edits must change final weights or exposure shape after risk controls;
- execution-neutral controller passes are not success-skill candidates;
- `execution_effect_failed` is repairable and appears in controller summaries and diagnostics.

This converts the old attempt `004` style from pass to reject:

```yaml
old_decision: pass
new_decision: reject
new_failure_category: execution_effect_failed
reason: ranked_signal_and_final_weights_unchanged
```

## Next Step

After GitHub sync, run one more controller-only forced-cell smoke with the same broad schedule. The purpose is to test whether the new execution-effect gate and prompt repairs produce at least one target-matched, novel, final-weight-effective child.

Do not run sample evaluation, 27B review, broad validation, full validation, or test-set evaluation until the next controller artifact is reviewed locally.
