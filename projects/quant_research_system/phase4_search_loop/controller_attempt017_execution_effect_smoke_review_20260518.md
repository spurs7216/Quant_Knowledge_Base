---
title: Controller Attempt017 Execution-Effect Smoke Review 2026-05-18
type: project
status: reviewed
updated: 2026-05-18
tags:
  - project
  - phase4
  - alphaevolve
  - controller
  - review
sources:
  - "controller_execution_effect_hardening_20260517.md"
  - "controller_attempt017_execution_effect_smoke_remote_instructions_20260517.md"
  - "daily_stock_data_understanding_plan_20260518.md"
---
# Controller Attempt017 Execution-Effect Smoke Review 2026-05-18

## Artifact

```text
artifacts/controller_attempt017_execution_effect_smoke_20260517.zip
```

## Summary

The execution-effect forced-cell smoke showed that the controller path is still healthy, but it did not produce a clean next child to promote or evaluate immediately.

Observed summary:

```yaml
attempt_count: 6
pass_count: 2
sample_eval_candidate_count: 2
execution_effect_pass_rate: 0.3333333333
behavioral_noop_count: 3
failure_categories:
  behavioral_noop: 3
  execution_effect_failed: 1
remote_sample_eval_launched: false
git_head_matches_origin_main: true
```

## Candidate Caveats

`PROG-20260517-A017-EXEFFECT-0003` was a `risk/liquidity_scaled_cap` child. It changed final weights and gross exposure, but the mechanism looks mainly like liquidity-conditioned exposure dampening after clipping. That can improve implementation diagnostics without being new alpha evidence.

`PROG-20260517-A017-EXEFFECT-0005` was a `signal/liquidity_adjusted_reversal` child. It changed ranks and final weights, but the patch was confounded: the replacement removed the parent volatility scaling, min-history filter, and EWM smoothing while adding a market-cap/liquidity weighting rule. The code comment also said to dampen less-liquid names, while the formula appeared to dampen high-market-cap names more.

## Decision

Do not launch sample evaluation directly from this artifact.

The next move is a data-understanding milestone, not another controller tweak. The controller has enough machinery to detect many malformed, duplicate, no-op, occupied-cell, and execution-neutral children. The more important bottleneck is that child proposals are not sufficiently grounded in the empirical structure of `daily_stock`.

## Lessons

- Execution-effect gating is useful, but it does not by itself distinguish alpha-relevant mechanisms from generic exposure dampening.
- A child can be controller-effective and still be research-confounded if it removes multiple parent mechanisms in the same SEARCH/REPLACE patch.
- The search loop needs prompt-facing data cards about liquidity skew, return tails, missingness, universe breadth, and industry coverage before further attempt017 evolution.

## Next Step

Run the remote full-file `daily_stock` EDA described in [daily_stock_eda_remote_instructions_20260518.md](daily_stock_eda_remote_instructions_20260518.md), review the artifact locally, then decide which data lessons should enter prompt construction.
