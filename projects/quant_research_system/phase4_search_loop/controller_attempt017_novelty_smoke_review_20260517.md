---
title: Controller Attempt017 Novelty Smoke Review 2026-05-17
type: project
status: active
updated: 2026-05-17
tags:
  - project
  - phase4
  - alphaevolve
  - artifact-review
  - attempt017
  - novelty-smoke
sources:
  - "../../../artifacts/controller_attempt017_novelty_smoke_20260516.zip"
  - "controller_attempt017_novelty_smoke_remote_instructions_20260516.md"
  - "sample_eval_novelty_hardening_20260515.md"
---
# Controller Attempt017 Novelty Smoke Review 2026-05-17

## Decision

Do not sample-evaluate any child from this run.

The controller-only proof run succeeded as an infrastructure check, but it produced zero `sample_eval_candidate_eligibility_v2` candidates. The right next step is a local runner/prompt-sampler patch, not another remote evaluation.

## Artifact

```yaml
artifact: artifacts/controller_attempt017_novelty_smoke_20260516.zip
artifact_sha256: 575C616D54941655B010D7AE64D71831DAE61F81E25F6DC577B92CE1F2C62972
git_commit: 6315dd342deb334069c4764b8790db9b8bce94d3
git_origin_main_commit: 6315dd342deb334069c4764b8790db9b8bce94d3
git_head_matches_origin_main: true
git_status_txt_empty: true
git_diff_stat_empty: true
```

The run used the intended six-attempt surface schedule:

```yaml
surface_schedule:
  - portfolio
  - portfolio
  - risk
  - risk
  - signal
  - signal
ranking_attempt_count: 0
mechanism_cards_enabled: false
remote_sample_eval_launched: false
full_validation_launched: false
test_set_used: false
```

## Controller Summary

```yaml
attempt_count: 6
pass_count: 1
sample_eval_candidate_count: 0
sample_eval_candidate_program_ids: []
raw_parse_pass_rate: 1.0
exact_search_match_rate: 1.0
evolve_block_safe_rate: 1.0
apply_pass_rate: 1.0
compile_pass_rate: 1.0
vector_smoke_pass_rate: 1.0
portfolio_semantic_pass_rate: 1.0
behavior_delta_pass_rate: 0.3333333333333333
unique_child_pass_rate: 0.16666666666666666
target_intent_match_rate: 1.0
duplicate_child_count: 1
duplicate_patch_fingerprint_count: 0
near_duplicate_patch_count: 0
behavioral_noop_count: 4
duplicate_retry_attempt_rate: 0.16666666666666666
duplicate_retry_success_rate: 0.0
map_cell_count: 1
map_cell_duplicate_count: 1
db_insert_pass_rate: 1.0
reasoning_only_empty_count: 0
```

This is a good mechanics result: parsing, patch application, compile, vector smoke, semantic smoke, database insertion, no-thinking routing, and git reproducibility all worked. It is a poor search-quality result: five of six attempts were rejected as lazy/duplicate evidence, and the one pass was not sample-eval eligible.

## Attempt-Level Read

| Attempt | Target | Patch shape | Decision | Why it matters |
| --- | --- | --- | --- | --- |
| `000` | `portfolio/signal_weighted_sides` | signal-magnitude side weights | reject: behavioral no-op | Downstream caps/renormalization made final smoke weights identical to parent. |
| `001` | `portfolio/signal_weighted_sides` | near-identical signal-magnitude side weights | reject: behavioral no-op | Same absorbed mechanism as attempt000. |
| `002` | `risk/max_weight_tightening` | late small-book shrink after existing cap logic | reject: behavioral no-op | The edit happens after the effective cap/renormalization path and does not change final outputs. |
| `003` | `risk/cap_shape_change` | clip positives and negatives after renormalization | reject: behavioral no-op | Re-clipping at the same max-weight boundary leaves final outputs unchanged. |
| `004` | `signal/liquidity_adjusted_reversal` | divide signal by rolling dollar-volume proxy | controller pass, sample-eval ineligible | Material final-weight delta, but it lands in an occupied MAP cell and does not beat the cell elite. |
| `005` | `signal/liquidity_adjusted_reversal` | exact duplicate of attempt004; retry was near-duplicate | reject: duplicate child | Duplicate retry generated `signal / (rolling_vol * liquidity_proxy)`, but edit-signature similarity to attempt004 was `0.892 >= 0.880`. |

Attempt004 details:

```yaml
program_id: PROG-20260516-A017-NOVELTY-0004
target_surface: signal
patch_intent: liquidity_adjusted_reversal
decision: pass
sample_eval_eligible: false
sample_eval_eligibility_reasons:
  - occupied_map_cell_does_not_beat_elite
map_cell_already_occupied: true
map_cell_elite_program_id: PROG-20260513-A017-MECH-0007
map_cell_elite_controller_search_score: 1.0
map_cell_elite_controller_score_beaten: false
map_cell_elite_behavior_distinct: true
weight_changed_fraction: 0.155
weight_max_abs_delta: 0.02
signal_changed_fraction: 0.5666666666666667
ranked_signal_changed_fraction: 0.5666666666666667
vector_smoke_eval_daily_sharpe: -1.8420701512491373
```

The occupied-cell gate did the right thing. `PROG-20260513-A017-MECH-0007` was already sample-evaluated and was worse than attempt017 on parent-relative Sharpe, return, turnover-aware score, drawdown, and missing-held exposure. A new same-cell controller pass should not consume another sample evaluation unless it beats the cell elite on the controller budget gate.

## Main Diagnosis

The proof run validated the new eligibility plumbing, but it also exposed a target-routing gap.

The remote instruction listed preferred underfilled cells:

```yaml
preferred_cells:
  - portfolio/liquidity_weighted_sides
  - portfolio/persistence_trade_gate
  - risk/liquidity_scaled_cap
  - signal/liquidity_adjusted_reversal
```

The actual command only supplied a surface schedule:

```bash
--surface-schedule portfolio,portfolio,risk,risk,signal,signal
```

Because `run_child_batch.py` has no exact target-cell or target-intent schedule, the population policy chose:

```yaml
actual_targets:
  - portfolio/signal_weighted_sides
  - portfolio/signal_weighted_sides
  - risk/max_weight_tightening
  - risk/cap_shape_change
  - signal/liquidity_adjusted_reversal
  - signal/liquidity_adjusted_reversal
```

That matters because the two portfolio cells and two risk cells are exactly the kind of edits the downstream controller can absorb. The prompt did warn that absorbed edits should output `NO_VALID_PATCH`, but Qwen still proposed plausible code edits that produced identical smoke outputs. This is not a Qwen server problem and not a token-limit problem. It is a sampler/control problem.

## What Worked

- Git reproducibility is clean: `HEAD == origin/main`, with empty `git_status.txt` and `git_diff_stat.txt`.
- No ranking attempts were scheduled.
- No remote sample evaluation or validation was launched.
- `sample_eval_candidate_eligibility_v2` fields are present.
- No-final-weight-delta children were ineligible.
- Occupied MAP-cell elite comparison fields are present on attempt004.
- Empty/reasoning-only output did not recur.
- The controller correctly rejected no-op and duplicate children.

## What Did Not Work

- The runner could not force the exact preferred mechanism cells named in the remote instruction.
- The sampler selected two portfolio/risk target cells that prior evidence already suggests are easy to absorb downstream.
- Duplicate retry did not rescue attempt005; the retry was a near-duplicate of attempt004.
- The final attempt005 summary reports the original duplicate-child rejection, while the retry artifact contains the more informative near-duplicate diagnosis. Future summaries should surface terminal retry reasons more clearly.

## Next Step

Patch the local controller runner before another remote run:

```yaml
local_patch_needed:
  - add an exact target-intent or target-cell schedule to run_child_batch.py
  - pass forced target intents into the prompt/population-policy selection path
  - make forced cells reject unavailable or invalid surface/intent pairs early
  - record forced_target_cell_schedule in summary.json
  - surface duplicate-retry terminal rejection reasons in summary.json
  - add tests that a forced schedule produces the requested cells
```

Then run another controller-only proof, still without automatic sample evaluation. A reasonable first forced schedule is:

```yaml
target_cell_schedule:
  - portfolio/liquidity_weighted_sides
  - portfolio/persistence_trade_gate
  - risk/liquidity_scaled_cap
  - risk/liquidity_scaled_cap
  - signal/liquidity_adjusted_reversal
  - signal/liquidity_adjusted_reversal
```

If the goal is to avoid the already negative signal-liquidity pocket for a short proof, shift one or both signal attempts to direct portfolio/risk cells instead. Do not bring back `ranking/industry_neutral_rank` yet; it remains an occupied/replay-heavy cell for this branch.

Do not use 27B for the immediate next step. The current bottleneck is deterministic search-control routing, not model ideation.

## Follow-Up

Implemented on 2026-05-17 in [forced_target_cell_schedule_patch_20260517.md](forced_target_cell_schedule_patch_20260517.md). The next remote step is a controller-only forced-cell smoke after GitHub sync.
