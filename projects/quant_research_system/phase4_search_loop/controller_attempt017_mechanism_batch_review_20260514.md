---
title: Controller Attempt017 Mechanism Batch Review 2026-05-14
type: project
status: active
updated: 2026-05-14
tags:
  - project
  - phase4
  - alphaevolve
  - controller
  - sample-eval
  - attempt017
sources:
  - "../../artifacts/controller_attempt017_mechanism_batch_20260513.zip"
  - "../../artifacts/remote_sample_eval_controller_attempt017_mechanism_batch_20260513_attempt_007.zip"
  - "attempt017_mechanism_design_20260513.md"
  - "controller_attempt017_mechanism_batch_remote_instructions_20260513.md"
  - "current_state.md"
---
# Controller Attempt017 Mechanism Batch Review 2026-05-14

## Decision

No promotion.

Do not run full validation, stage-0 broad validation, or test-set evaluation from this batch.

The remote operator followed the sample-eval rule correctly: the controller batch produced exactly one sample-eval-eligible child, `PROG-20260513-A017-MECH-0007`, and only that child was evaluated. The child is broad and nontrivial, but its sample evaluation is worse than the attempt017 parent on Sharpe, annualized return, turnover-aware score, drawdown, and missing-held exposure.

## Reproducibility Note

The sample-eval manifest reports:

```yaml
git_commit: 4416733215d124322d2da421a6fe17c1e1eee4f6
git_dirty: false
```

This commit is not fetchable from GitHub at review time. The remote explanation is that this was a local hygiene commit, `Ignore Codex local state`, rebased on top of `origin/main`; it only ignores `.codex/`. Practical interpretation:

- research code and metrics are likely reproducible from `origin/main`;
- the manifest is not exactly reproducible from GitHub unless the hygiene commit is pushed or the run is repeated from exact `origin/main`;
- future remote artifact reviews should record whether a clean run means clean against `origin/main` or clean against an unpushed local branch.

## Controller Batch Summary

Artifact:

```text
artifacts/controller_attempt017_mechanism_batch_20260513.zip
```

Summary:

```yaml
attempt_count: 12
pass_count: 5
unique_child_pass_rate: 0.4166666666666667
raw_parse_pass_rate: 1.0
exact_search_match_rate: 1.0
evolve_block_safe_rate: 1.0
apply_pass_rate: 1.0
compile_pass_rate: 1.0
vector_smoke_pass_rate: 0.5
portfolio_semantic_pass_rate: 0.5
behavior_delta_pass_rate: 0.4166666666666667
target_intent_match_rate: 1.0
duplicate_child_count: 0
near_duplicate_patch_count: 0
behavioral_noop_count: 1
sample_eval_candidate_count: 1
sample_eval_candidate_attempts: [7]
sample_eval_candidate_program_ids:
  - PROG-20260513-A017-MECH-0007
```

What worked:

- Qwen no-thinking routing stayed healthy: no empty or reasoning-only outputs.
- Patch-format mechanics were excellent: parse, exact match, evolve-block safety, apply, and compile all passed.
- Duplicate pressure was controlled: no duplicate child, duplicate patch, or near-duplicate rejects.
- Target-intent match among controller passes was 1.0.
- The sample-eval eligibility summary selected only one candidate.

What failed:

- Six of twelve attempts failed vector smoke.
- Direct portfolio/risk mechanisms did not get a fair market test because they failed controller smoke.
- Three controller passes changed ranking or signal but left final weights unchanged on the smoke panel.
- The only sample-eval-eligible child was a signal-side liquidity adjustment, not the direct portfolio/risk tradability mechanism we most wanted to test.

## Per-Attempt Read

| Attempt | Target | Decision | Controller read |
| --- | --- | --- | --- |
| 000 | portfolio/liquidity_weighted_sides | reject | `DlyPrcVol` key error. Patch used `valid[CONTRACT.dollar_volume]`, but the portfolio block's local `data` does not include that field. |
| 001 | ranking/industry_neutral_rank | reject | weights all zero. The industry-neutral patch returned too many missing ranks or collapsed selection. |
| 002 | portfolio/persistence_trade_gate | reject | `signal_lag` key error. The block did not have a lagged signal column. |
| 003 | signal/liquidity_adjusted_reversal | pass | Target matched but no final-weight delta, so not sample-eval eligible. |
| 004 | risk/liquidity_scaled_cap | reject | Used `CONTRACT.volume[group.index]`, treating a contract field string as a Series. |
| 005 | portfolio/liquidity_weighted_sides | reject | Behavioral no-op: child smoke signal, ranks, and weights were identical to parent. |
| 006 | ranking/industry_neutral_rank | pass | Rank delta, but no final-weight delta on smoke panel. |
| 007 | signal/liquidity_adjusted_reversal | pass | Only sample-eval candidate; material rank and final-weight delta on controller smoke. |
| 008 | risk/liquidity_scaled_cap | reject | `DlyPrcVol` key error. Same local data-scope issue as attempt 000. |
| 009 | portfolio/persistence_trade_gate | reject | Boolean index length mismatch from using a boolean mask not aligned to the target index labels. |
| 010 | ranking/shrinkage_transform | pass | Ranking delta, but no final-weight delta. |
| 011 | signal/liquidity_adjusted_reversal | pass | No final-weight delta and same MAP cell as a prior pass. |

## Sample Evaluation Of Attempt 007

Artifact:

```text
artifacts/remote_sample_eval_controller_attempt017_mechanism_batch_20260513_attempt_007.zip
```

Decision:

```yaml
decision: sample_review
program_id: PROG-20260513-A017-MECH-0007
parent_program_id: PROG-20260430-CHILD-0017
portfolio_days: 581
portfolio_day_coverage: 0.9355877616747182
not_metric_equivalent_to_reference: true
missing_held_weight_within_sample_tolerance: false
test_metrics_locked: true
```

Parent-relative search-sample comparison:

| Metric | attempt017 parent | attempt007 child | Delta |
| --- | ---: | ---: | ---: |
| annualized_return | 0.0597464969 | 0.0515093102 | -0.0082371866 |
| Sharpe | 0.4425987623 | 0.3655419045 | -0.0770568578 |
| gross Sharpe | 0.6595563928 | 0.5707057633 | -0.0888506294 |
| max drawdown | -0.2624308119 | -0.2911748187 | -0.0287440068 |
| turnover | 0.4650255541 | 0.4594224127 | -0.0056031414 |
| turnover-aware score | -0.2736576262 | -0.3993136987 | -0.1256560724 |
| max missing-held weight | 0.12 | 0.13 | +0.01 |
| mean missing-held weight | 0.0017601748 | 0.0020531250 | +0.0002929502 |
| hit rate | 0.5025817556 | 0.4905335628 | -0.0120481928 |

Train/validation comparison is also worse:

```yaml
train_sharpe_delta: -0.0959986370
validation_sharpe_delta: -0.0897425809
validation_turnover_delta: +0.0552001686
validation_turnover_aware_delta: -0.1535426230
```

The child remains far better than random matched long/short baselines and the sign flip, but it is worse than its real parent. That is the relevant comparison for promotion.

## Research Interpretation

This batch is useful negative evidence, not a failed infrastructure run.

The mechanism prompt did move Qwen away from generic dampening and duplicate patches. However, it exposed a controller interface gap: the prompt says children may use daily-stock `CONTRACT` fields, but the editable portfolio, ranking, and risk blocks often work with local `data`, `group`, or `valid` frames that do not contain those columns. Qwen therefore wrote plausible-looking mechanism patches that were invalid in the actual block scope.

The direct tradability mechanisms have not been rejected by market evidence yet. They mostly failed before evaluation because the surface-local data-access contract was underspecified.

By contrast, the one signal-side liquidity adjustment that reached sample evaluation is now negative parent-relative evidence for the attempt017 branch. It changed weights but worsened parent-relative economics and missing-held behavior.

## Lessons To Keep

- A target-intent match is not enough. The patch must be valid in the local variable scope of the target EVOLVE block.
- For portfolio/risk targets, the prompt must explicitly say to use `panel.loc[index, CONTRACT.dollar_volume]`, `panel.loc[index, CONTRACT.volume]`, `panel.loc[index, CONTRACT.market_cap]`, and similar lookups rather than `valid[CONTRACT.dollar_volume]` when the local frame lacks the field.
- For ranking industry targets, the prompt must explicitly say to use `panel.loc[group.index, CONTRACT.industry_primary]` because the ranking block's `data` frame only carries date and signal.
- The controller smoke panel should contain multiple industries and tradability variation. A one-industry smoke panel cannot tell whether industry neutralization affects selection.
- Repair prompts need examples for local data-scope mistakes and aligned index-label assignment; otherwise they often return `NO_VALID_PATCH`.
- Controller-relative success memory must not be promoted to active strategy skill until sample-eval evidence is checked. The skill update correctly labels the controller successes as low-confidence candidates.

## Next Step

Run a local controller/prompt repair slice before another remote generation batch:

```yaml
next_stage: local_controller_prompt_smoke_repair
do_not_do:
  - full_validation
  - test_evaluation
  - another blind mechanism batch
repair_scope:
  prompt_builder:
    - add surface-local data-access contracts
    - add examples for panel.loc index-aligned daily_stock field access
    - mark signal/liquidity_adjusted_reversal attempt007 as negative sample-eval evidence for attempt017
  micro_filter:
    - vary industry_primary across smoke names
    - preserve liquidity and market-cap heterogeneity
    - optionally add a targeted local smoke fixture for portfolio/risk field-access patches
  reasoning_memory_or_skill_layer:
    - do not promote controller-only signal liquidity skills
    - add failure memory for local-frame field access errors
remote_after_patch:
  type: small_controller_only_mechanism_rerun
  preferred_targets:
    - portfolio/liquidity_weighted_sides
    - portfolio/persistence_trade_gate
    - risk/liquidity_scaled_cap
    - ranking/industry_neutral_rank
  sample_eval_limit: 0_or_1
```

Only after the controller can generate at least one valid direct portfolio/risk mechanism with a final-weight delta should we spend another sample-eval run.
