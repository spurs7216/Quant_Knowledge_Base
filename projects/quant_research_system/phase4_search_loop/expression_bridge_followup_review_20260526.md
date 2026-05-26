---
title: Expression Bridge Follow-Up Review 20260526
type: evidence_review
status: active
updated: 2026-05-26
tags:
  - project
  - phase4
  - expression-evolution
  - bridge-policy
  - remote-run
  - artifact-review
sources:
  - "../../../artifacts/expression_bridge_followup_20260526.zip"
  - "expression_bridge_followup_remote_instructions_20260526.md"
  - "expression_episode_20260526_review.md"
---
# Expression Bridge Follow-Up Review 20260526

## Artifact

Artifact: `artifacts/expression_bridge_followup_20260526.zip`

Remote code state:

- commit: `c7966ed7765d73e17a9dbea1480dd0e57953779f`
- `HEAD == origin/main`: true
- worktree dirty: false
- run id: `expression_bridge_followup-20260526T022319+0000-c71d64e8`

The run used the fixed Phase 4 development split:

- in-sample: 2011-01-03 through 2022-12-30, 3020 dates
- out-of-sample feedback: 2023-01-03 through 2025-11-28, 730 dates
- final test: not defined and not used

## Mechanical Result

The deterministic bridge follow-up worked.

- Status: `ok`
- Qwen/vLLM use: none
- Parent/child bridge records: 6
- `expression_sample_pass`: 6
- `expression_error`: 0
- Required comparison, ranking, scorecard, cost, universe, split, and Git hygiene artifacts were present.

All hard gates passed for the parent and child under `daily`, `rebalance_5`, and `signal_decay_5`: broad coverage, max weight, net exposure, missing-held tolerance, and reported turnover-aware score.

## Main Bridge Evidence

Candidate:

```text
expr_smoothed_rev_liq_bridge_20260526
rank(-rolling_mean(rolling_sum(excess_ret, 5), 3)) * rank(log1p_abs(dollar_volume))
```

Parent:

```text
expr_smoothed_rev
rank(-rolling_mean(rolling_sum(excess_ret, 5), 3))
```

### Daily Bridge

The child is worse than the parent under daily rebalancing.

| Metric | Parent | Child | Child - Parent |
| --- | ---: | ---: | ---: |
| Search Sharpe | 0.1947 | 0.0262 | -0.1684 |
| Search turnover | 0.5250 | 0.5916 | +0.0666 |
| Search turnover-aware score | 0.0124 | -0.2217 | -0.2341 |
| IS turnover-aware score | 0.0922 | -0.2332 | -0.3254 |
| OS turnover-aware score | -0.3120 | -0.1281 | +0.1839 |

Interpretation: this is not expression-alpha evidence under the primary daily bridge.

### Five-Day Rebalance Bridge

`rebalance_5` is the only bridge that passes the follow-up rule.

| Metric | Parent | Child | Child - Parent |
| --- | ---: | ---: | ---: |
| Search Sharpe | 0.1493 | 0.1611 | +0.0117 |
| Search turnover | 0.3327 | 0.2717 | -0.0610 |
| Search turnover-aware score | 0.0151 | 0.0410 | +0.0259 |
| IS Sharpe | 0.2321 | 0.1294 | -0.1027 |
| IS turnover-aware score | 0.0978 | 0.0093 | -0.0884 |
| OS Sharpe | -0.1642 | 0.2747 | +0.4389 |
| OS turnover-aware score | -0.2968 | 0.1570 | +0.4538 |

Interpretation: the child improves the total search score and OS behavior under a slower bridge, but the in-sample edge is weak and below the parent. This is enough to justify robustness testing, not promotion.

### Signal-Decay-5 Bridge

`signal_decay_5` improves search and OS versus the parent, but fails the stricter follow-up rule because in-sample turnover-aware score is negative.

| Metric | Parent | Child | Child - Parent |
| --- | ---: | ---: | ---: |
| Search Sharpe | 0.1583 | 0.1655 | +0.0072 |
| Search turnover | 0.2585 | 0.2173 | -0.0412 |
| Search turnover-aware score | 0.0426 | 0.0640 | +0.0214 |
| IS turnover-aware score | 0.1799 | -0.0118 | -0.1917 |
| OS turnover-aware score | -0.4775 | 0.3775 | +0.8550 |

Interpretation: this is an OS-heavy diagnostic, not the next primary bridge.

## Cost Sensitivity

At 2.5 bps, `rebalance_5` child search turnover-aware score is positive: 0.0410.

At 5 bps, it becomes negative: -0.1836. The parent is also negative at 5 bps: -0.1929.

So the child is better than the parent around the active 2.5 bps cost assumption, but the bridge is not robust to a doubled cost setting. This should stay a caveat in future prompt and promotion logic.

## Decision

Do not promote.

Do not run full validation.

Do not run another broad Qwen expression episode yet.

The result supports a narrower deterministic next step: bridge robustness, especially rebalance phase and period robustness.

## Next Step

The next local implementation should make bridge robustness first-class:

1. Extend bridge variants or add a follow-up runner for `rebalance_N` with phase offsets.
2. Evaluate the parent and child under `rebalance_5` offsets 0 through 4, because the current `rebalance_5` contract is anchored to the first analysis date.
3. Add neighboring bridge periods such as `rebalance_3`, `rebalance_10`, and perhaps `signal_decay_3`, `signal_decay_10`.
4. Require the child to keep positive IS and OS turnover-aware scores across most offsets, not just one anchored `rebalance_5` path.
5. Only after that should we convert the child into a first-class bridge-aware expression strategy parent for later Qwen evolution.

Local implementation completed:

- `BridgeVariantSpec` now supports `phase_offset`.
- Rebalance variants can be named `rebalance_N_offset_M`.
- `run_expression_bridge_followup.py` now writes `expression_bridge_followup_robustness.csv` and `robust_bridge_families`.
- The remote handoff is [expression_bridge_robustness_remote_instructions_20260526.md](expression_bridge_robustness_remote_instructions_20260526.md).

## Caveats

- `rebalance_5` currently means every fifth available trading date from the analysis-window start. That can create calendar-phase dependence.
- The follow-up used 2023-2025 OS as development feedback; it is not final validation.
- The child is cost-fragile at 5 bps.
- The child's in-sample score under `rebalance_5` is positive but weaker than the parent, so the evidence is not a clean all-split improvement.
