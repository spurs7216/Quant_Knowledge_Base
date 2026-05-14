---
title: Controller Attempt017 Mechanism Rerun Review 2026-05-14
type: project
status: active
updated: 2026-05-14
tags:
  - project
  - phase4
  - alphaevolve
  - artifact-review
  - attempt017
sources:
  - "../../artifacts/controller_attempt017_mechanism_rerun_20260514.zip"
  - "../../artifacts/remote_sample_eval_controller_attempt017_mechanism_rerun_20260514_attempt_009.zip"
  - "controller_attempt017_mechanism_rerun_remote_instructions_20260514.md"
  - "controller_prompt_smoke_repair_20260514.md"
---
# Controller Attempt017 Mechanism Rerun Review 2026-05-14

## Decision

No promotion.

The controller rerun found one sample-eval-eligible child, `PROG-20260514-A017-MECHFIX-0009`. The remote sample evaluation correctly treated it as `sample_review`, not `sample_pass`.

## Controller Result

```yaml
artifact: artifacts/controller_attempt017_mechanism_rerun_20260514.zip
attempt_count: 12
pass_count: 2
sample_eval_candidate_count: 1
sample_eval_candidate_program_ids:
  - PROG-20260514-A017-MECHFIX-0009
failure_categories:
  behavioral_noop: 7
  duplicate_child: 1
  vector_smoke_failed: 2
vector_smoke_pass_rate: 0.8333333333333334
behavior_delta_pass_rate: 0.25
unique_child_pass_rate: 0.16666666666666666
target_intent_match_rate: 0.5
```

The local prompt/smoke field-access repair helped the controller reach a valid direct mechanism candidate, but the search quality is still weak. Most attempts were absorbed by the smoke path and became behavioral no-ops. The two controller passes were:

| Attempt | Target | Patch intent | Controller decision | Sample-eval eligible | Comment |
| --- | --- | --- | --- | --- | --- |
| `attempt_003` | `ranking/winsorization_quantile_change` | `ranking_other` | pass | no | off-target target-intent mismatch |
| `attempt_009` | `ranking/industry_neutral_rank` | `industry_neutral_rank` | pass | yes | valid candidate selected for sample eval |

## Attempt009 Patch Shape

`attempt_009` changed the ranking block. It added industry-aware ranking using:

```text
panel.loc[group.index, CONTRACT.industry_primary]
```

This confirms the surface-local data-access repair was used correctly. The controller measured a material rank and final-weight effect:

```yaml
ranked_signal_max_abs_delta: 2.1293282524343167
weight_max_abs_delta: 0.02
weight_changed_fraction: 0.06
active_position_jaccard: 0.6190476190476191
sample_eval_eligible: true
```

## Sample Evaluation

```yaml
artifact: artifacts/remote_sample_eval_controller_attempt017_mechanism_rerun_20260514_attempt_009.zip
program_id: PROG-20260514-A017-MECHFIX-0009
parent_program_id: PROG-20260430-CHILD-0017
decision: sample_review
portfolio_days: 581
portfolio_day_coverage: 0.9355877616747182
reference_metric_equivalent: false
max_missing_held_weight: 0.05122261612580676
missing_held_gate: failed_narrowly
```

Parent-relative sample metrics:

| Metric | attempt017 parent | attempt009 child | Delta |
| --- | ---: | ---: | ---: |
| annualized return | 0.0597464969 | 0.0160184107 | -0.0437280862 |
| Sharpe | 0.4425987623 | 0.3183261147 | -0.1242726476 |
| turnover | 0.4650255541 | 0.2723031701 | -0.1927223840 |
| turnover-aware score | -0.2736576262 | -0.0058627585 | +0.2677948678 |
| max drawdown | -0.2624308119 | -0.0969370997 | +0.1654937122 |
| max missing-held weight | 0.12 | 0.0512226161 | -0.0687773839 |
| mean daily names | 98.8364888124 | 255.6402753873 | +156.8037865749 |

Split behavior:

```yaml
train_sharpe: -0.7341433994
validation_sharpe: 1.5468579747
search_sample_sharpe: 0.3183261147
```

The child is useful evidence but not a strategy promotion. It improved implementation shape, turnover, drawdown, breadth, and missing-held weight, but gave up parent-relative return and Sharpe. The train/validation split is too asymmetric to treat the validation result as alpha evidence.

## Reproducibility Caveat

The sample-eval manifest recorded:

```yaml
git_dirty: false
git_commit: fa4b9134f329a30c4321b638ffe77271008f0e55
```

After local `git fetch origin`, that commit was not present locally and `origin/main` remained `0073da0bf927b227fe5b134d699b637820e764fe`. A clean remote worktree is therefore not enough: the run was clean on the remote machine, but not proven reproducible from a GitHub-fetchable commit.

Local repair after this review:

```yaml
remote_sample_eval_now_records:
  - program_snapshot.py
  - program_sha256
  - git_origin_main_commit
  - git_head_matches_origin_main
  - manifest_commit_fetchable_from_github
controller_batch_now_records:
  - parent_program_snapshot.py
  - parent_program_sha256
  - git_origin_main_commit
  - git_head_matches_origin_main
```

## Interpretation

The attempt017 branch now has a clear tradeoff:

```yaml
attempt017:
  better_alpha_metrics: true
  worse_turnover_missing_held_and_drawdown: true
attempt009:
  better_implementation_shape: true
  worse_parent_relative_return_and_sharpe: true
```

This suggests the next search should not ask for another generic direct mechanism. It should ask a stronger reviewer to synthesize the tradeoff and propose a small set of mechanism cards before 9B writes code.

## Next Step

Use `Qwen/Qwen3.5-27B-FP8` as a medium reviewer to produce JSON mechanism cards only. Then use the 9B generator for strict SEARCH/REPLACE patches conditioned on those cards.

Do not let the 27B model emit direct patches in this step. Prior model evidence says 27B is better suited to medium-depth review and mutation-surface proposal than strict patch generation.
