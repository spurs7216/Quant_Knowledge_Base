---
title: Expression Episode 20260526 Review
type: evidence_review
status: active
updated: 2026-05-26
tags:
  - project
  - phase4
  - expression-evolution
  - remote-run
  - artifact-review
sources:
  - "../../../artifacts/expression_episode_20260526.zip"
  - "expression_episode_remote_instructions_20260526.md"
  - "phase4_caveat_repair_ledger.md"
---
# Expression Episode 20260526 Review

## Artifact

Artifact: `artifacts/expression_episode_20260526.zip`

Remote code state:

- commit: `b44ae3aef4b1efe061bc88b4837273855e902b82`
- `HEAD == origin/main`: true
- worktree dirty: false
- run id: `expression_episode-20260526T012423+0000-82524e85`

## Mechanical Result

The repaired expression runner worked.

- 6 Qwen calls succeeded.
- No null-content, malformed JSON, model-parse, or expression-evaluation failures occurred.
- 12 child proposals were recorded.
- 7 children reached `expression_sample_pass`.
- 5 children were exact duplicates.
- 2 children were near duplicates.
- Required population artifacts were present, including `expression_population.sqlite`, `expression_success_flags.csv`, and `expression_bridge_variants.csv`.
- Validation exposure was correctly marked as development OS feedback only; final-test usage count was 0.

This confirms the controller/evaluator mechanics, not alpha promotion.

## Population Behavior

The population logic partly worked:

- `expr_smoothed_rev` turn 2 fell back to the root because turn 1 produced only duplicate children.
- `expr_size_ind_rev` turn 2 also fell back to the root because turn 1 produced only duplicate children.
- `expr_mom_060_ind` turn 2 sampled a real eligible turn-1 survivor: `expr_mom_060_ind_000_82524e85_ep_t01_c00`.

Branch diagnostics:

| Root | Child count | Eligible children | Best child root delta | Pause? |
| --- | ---: | ---: | ---: | --- |
| `expr_smoothed_rev` | 4 | 2 | 0.0200 | no |
| `expr_size_ind_rev` | 4 | 2 | -0.0072 | yes |
| `expr_mom_060_ind` | 4 | 3 | 0.1578 | no |

The size branch should not get another immediate expression episode without a better mechanism prompt or bridge-policy decision.

## Main Market Evidence

No child is promotable under the primary daily bridge.

The strongest primary daily child was:

`expr_smoothed_rev_000_82524e85_ep_t02_c00`

Expression:

```text
rank(-rolling_mean(rolling_sum(excess_ret, 10), 5))
```

Primary daily metrics:

- search turnover-aware score: 0.0324 versus parent 0.0124
- search Sharpe: 0.1556
- turnover: 0.2927
- IS Sharpe: 0.2672
- OS Sharpe: -0.2849
- OS turnover-aware score: -0.4073
- near duplicate: true

This is not a useful promotion candidate. It improves the full search score by reducing turnover, but the OS behavior is worse and the expression is a near duplicate of the smoothed reversal family.

## Bridge Diagnostic Evidence

The most important result is bridge-dependent.

`expr_smoothed_rev_000_82524e85_ep_t02_c01`

Expression:

```text
rank(-rolling_mean(rolling_sum(excess_ret, 5), 3)) * rank(log1p_abs(dollar_volume))
```

Under the primary daily bridge:

- search turnover-aware score: -0.2217
- search Sharpe: 0.0262
- turnover: 0.5916
- IS Sharpe: 0.0150
- OS Sharpe: 0.0683
- broad coverage: true
- near duplicate: false

Under a 5-day rebalance diagnostic bridge:

- search turnover-aware score: 0.0410
- IS turnover-aware score: 0.0093
- OS turnover-aware score: 0.1570
- search Sharpe: 0.1611
- turnover: 0.2717

Under a signal-decay-5 diagnostic bridge:

- search turnover-aware score: 0.0640
- IS turnover-aware score: -0.0118
- OS turnover-aware score: 0.3775
- search Sharpe: 0.1655
- turnover: 0.2173

Interpretation: the expression itself is not strong under daily rebalancing, but the combination of smoothed reversal, dollar-volume liquidity gating, and slower execution is a plausible cost-conversion mechanism. This is exactly the caveat the bridge diagnostics were meant to expose.

The size branch also improved under bridge variants, but its OS score stayed negative:

- `expr_size_ind_rev_000_82524e85_ep_t02_c00` with rebalance-5: search score 0.1203, IS score 0.1815, OS score -0.1094.
- `expr_size_ind_rev_000_82524e85_ep_t02_c01` with signal-decay-5: search score 0.1043, IS score 0.2093, OS score -0.3055.

Those are cost-shape diagnostics, not follow-up priorities.

## Qwen Behavior

Qwen returned valid JSON reliably, but its novelty quality was weak.

The duplicate failures were meaningful:

- for `expr_smoothed_rev`, turn 1 proposed two already-known seed expressions;
- for `expr_size_ind_rev`, turn 1 proposed two already-known seed expressions;
- for `expr_mom_060_ind`, turn 2 repeated the volatility-filtered momentum expression already generated in turn 1.

The duplicate filter worked, but the next prompt needs stronger memory pressure against known seed expressions and same-family rewrites.

## Decision

Do not promote any child.

Do not run full validation.

Do not run another broad expression episode immediately.

The best next step is a bridge-policy follow-up, not more child generation:

1. Convert `expr_smoothed_rev_000_82524e85_ep_t02_c01` into a reviewed bridge-aware strategy candidate with explicit 5-day rebalance and signal-decay alternatives.
2. Add parent-relative bridge comparison under the same bridge for `expr_smoothed_rev` and the child.
3. Run deterministic remote evaluation for this bridge-aware candidate family before asking Qwen for more expressions.
4. Only if the bridge-aware candidate keeps positive IS/OS after-cost behavior should it become a new root for the next expression-population episode.

## Local Follow-Up Implementation

Implemented after this review:

- `research/alphaevolve_lite/scripts/run_expression_bridge_followup.py`
- `research/alphaevolve_lite/tests/test_expression_bridge_followup.py`
- [expression_bridge_followup_remote_instructions_20260526.md](expression_bridge_followup_remote_instructions_20260526.md)

The runner compares `expr_smoothed_rev` and the liquidity-gated child under identical bridge contracts and writes comparison, scorecard, ranking, and cost-sensitivity artifacts. It is deterministic and does not call Qwen. A bridge follow-up pass is evidence to consider explicit bridge-aware strategy conversion, not promotion.

## Caveats

- The bridge variants are diagnostic artifacts, not the official evaluator status.
- Rebalance and signal-decay bridges change the strategy implementation contract, so they need explicit strategy-program conversion before any promotion discussion.
- The OS interval is still development feedback. It must not be treated as final test evidence.
- The duplicate rate is high enough that future prompts should include a compact seed-expression avoid list or prior-population ledger.
