---
title: Controller Evaluator Hardening Smoke Review 2026-05-11
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
  - "../../artifacts/controller_evaluator_hardening_smoke_20260510.zip"
  - "controller_evaluator_hardening_remote_instructions_20260510.md"
  - "controller_batch_001_attempt017_repair_hardening_20260510.md"
---
# Controller Evaluator Hardening Smoke Review 2026-05-11

## Decision

The hardening smoke succeeded as a controller/evaluator contract test, but it did not produce a promote-ready child.

Do not promote `attempt_004`. Do not sample-evaluate more children from this 6-attempt smoke. The next local action is to fix the sample-eval lineage contract and tighten signal intent classification before any further remote run.

## Controller Smoke

Artifact folder:

```text
controller_evaluator_hardening_smoke_20260510
```

Key controller results:

```yaml
attempt_count: 6
pass_count: 2
raw_parse_pass_rate: 1.0
exact_search_match_rate: 1.0
evolve_block_safe_rate: 1.0
apply_pass_rate: 1.0
compile_pass_rate: 1.0
vector_smoke_pass_rate: 1.0
portfolio_semantic_pass_rate: 1.0
behavior_delta_pass_rate: 0.3333333333333333
behavioral_noop_count: 4
duplicate_child_count: 0
duplicate_patch_fingerprint_count: 0
near_duplicate_patch_count: 0
map_cell_count: 2
db_insert_pass_rate: 1.0
reasoning_only_empty_count: 0
remote_sample_eval_launched_by_controller: false
```

The new behavior-delta gate worked. Four generated patches compiled and passed portfolio semantics, but had exactly zero smoke-panel change versus the parent. They were correctly rejected as `behavioral_noop`.

The parent-offspring seeding fix also worked:

```yaml
parent_offspring_counts:
  PROG-20260430-000000: 48
  PROG-20260430-CHILD-0017: 10
```

Historical missing-parent children were not incorrectly assigned to attempt017.

## Pass Children

`attempt_003`:

- target: `ranking:rank_transform`
- actual intent: `rank_transform`
- target match: true
- behavior: material ranked-signal delta but no smoke portfolio delta
- decision: keep as controller evidence only; not worth sample evaluation from this run

`attempt_004`:

- target: `signal:volatility_floor_or_scaling`
- actual classifier output before local patch: `time_smoothing`
- behavior: material signal/ranking/portfolio delta, no gross or net exposure change
- sample-evaluated because it was the only nontrivial signal child

The classifier label was too broad because `rolling_vol.rolling(...)` was caught by the generic rolling/time-smoothing rule before the volatility-scaling rule. This is a local classifier issue, not evidence that the child should receive time-smoothing credit.

## Sample Eval For Attempt004

Artifact folder:

```text
remote_sample_eval_controller_evaluator_hardening_smoke_attempt_004_20260511
```

Decision:

```yaml
decision: sample_review
failed_gate:
  missing_held_weight_within_sample_tolerance: false
```

Coverage and exposure diagnostics:

```yaml
portfolio_days: 581
visible_universe_days: 621
portfolio_day_coverage: 0.9355877616747182
mean_gross_exposure: 1.0
max_gross_exposure: 1.0000000000000002
max_abs_net_exposure: 2.7755575615628914e-17
max_weight: 0.010416666666666668
max_missing_held_weight: 0.11999999999999998
```

The child is broad-coverage and not a de-grossing artifact. The failure is that it does not fix the attempt017 missing-held-weight problem.

Parent-relative comparison to attempt017:

```yaml
search_sample_sharpe:
  attempt017_parent: 0.44259876228477274
  attempt004_child: 0.3950373426180869
search_sample_annualized_return:
  attempt017_parent: 0.05974649689082866
  attempt004_child: 0.053034525095893764
turnover:
  attempt017_parent: 0.46502555411148977
  attempt004_child: 0.46926695118667094
turnover_aware_score:
  attempt017_parent: -0.2736576262430996
  attempt004_child: -0.32227939517858073
max_missing_held_weight:
  attempt017_parent: 0.11999999999999998
  attempt004_child: 0.11999999999999998
```

The child is worse than the parent on Sharpe, return, turnover, turnover-aware score, and does not improve max missing-held weight.

Split behavior is unstable:

```yaml
train_sharpe: -0.38178854327451534
validation_sharpe: 1.313170956695391
```

Cost sensitivity remains fragile:

```yaml
0_bps_sharpe: 0.6151406311410408
2_5_bps_sharpe: 0.3950373426180869
5_bps_sharpe: 0.17485172438954674
10_bps_sharpe: -0.26569284564129236
```

## Caveats

The sample-eval command recorded `program_id: PROG-20260430-000000`, the seed default, even though the evaluated program path was the attempt004 child. The numerical evidence is still usable, but the lineage metadata is wrong.

Local fix after this review:

- `remote_sample_eval.py` now refuses child sample evaluation under the seed default program id.
- child sample eval accepts `--parent-program-id`;
- sample-eval artifacts and database records include `parent_program_id`;
- attempt017 repair instructions now use the attempt017 parent summary and explicit child ids.

## Next Step

Do not run full validation. Do not run stage-0 validation. Do not promote attempt004.

Before the next remote run, push the lineage/classifier patch. Then run another small controller-only generation if needed, using the new `behavioral_noop` memory and stricter lineage contract. Only sample-evaluate a child if it is:

- behaviorally nontrivial after signal, ranking, portfolio, and risk controls;
- target-intent matched after the corrected classifier;
- not just a gross-exposure or turnover artifact;
- plausibly able to improve attempt017 on missing-held weight or parent-relative turnover-aware score.
