---
title: Expression Bridge Robustness Review 20260526
type: evidence_review
status: active
updated: 2026-05-26
tags:
  - project
  - phase4
  - expression-evolution
  - bridge-policy
  - robustness
  - remote-run
  - artifact-review
sources:
  - "../../../artifacts/expression_bridge_robustness_20260526.zip"
  - "expression_bridge_robustness_remote_instructions_20260526.md"
  - "expression_bridge_followup_review_20260526.md"
  - "expression_episode_20260526_review.md"
---
# Expression Bridge Robustness Review 20260526

## Artifact

Artifact: `artifacts/expression_bridge_robustness_20260526.zip`

Remote code state:

- commit: `55d25a97178ee7740d593dc2ec0f55b12a8408fa`
- `HEAD == origin/main`: true
- worktree dirty: false
- manifest commit fetchable from GitHub: true
- run id: `expression_bridge_followup-20260526T030434+0000-d4131bc4`

The local instruction-only commit `f636f093a1bb368c9589de629e82988b4bfcef47` was pushed after the code commit and does not affect this run's metrics.

## Mechanical Result

The robustness runner worked.

```yaml
status: ok
parent_baseline_count: 22
bridge_child_count: 22
sample_pass: 44
sample_review: 0
expression_error: 0
comparison_count: 22
promising_bridge_variant_count: 2
robust_bridge_family_count: 0
```

Required artifacts were present, including `expression_bridge_followup_robustness.csv`, `expression_bridge_followup_comparison.csv`, `expression_bridge_followup_scorecard.csv`, cost sensitivity, universe, split, and Git hygiene files.

## Candidate

Parent:

```text
expr_smoothed_rev
rank(-rolling_mean(rolling_sum(excess_ret, 5), 3))
```

Child:

```text
expr_smoothed_rev_liq_bridge_20260526
rank(-rolling_mean(rolling_sum(excess_ret, 5), 3)) * rank(log1p_abs(dollar_volume))
```

The tested thesis was that explicit dollar-volume confidence plus slower execution might convert the smoothed reversal seed into a more cost-resilient expression.

## Robustness Result

No bridge family is robust enough to convert the child into a bridge-aware parent.

| Bridge family | Variants | Follow-up pass | Child positive search | Child positive IS | Child positive OS | Child beats parent search | Robust? |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `daily` | 1 | 0 | 0 | 0 | 0 | 0 | no |
| `rebalance_3` | 3 | 0 | 1 | 1 | 2 | 0 | no |
| `rebalance_5` | 5 | 1 | 3 | 3 | 3 | 3 | no |
| `rebalance_10` | 10 | 1 | 5 | 3 | 10 | 8 | no |
| `signal_decay_3` | 1 | 0 | 1 | 0 | 1 | 0 | no |
| `signal_decay_5` | 1 | 0 | 1 | 0 | 1 | 1 | no |
| `signal_decay_10` | 1 | 0 | 1 | 0 | 1 | 1 | no |

`rebalance_5` was the original promising bridge, but phase testing weakens the evidence:

| Variant | Child search TA | Child IS TA | Child OS TA | Child minus parent search TA | Follow-up pass |
| --- | ---: | ---: | ---: | ---: | --- |
| `rebalance_5` | 0.0725 | 0.0409 | 0.1876 | 0.0581 | true |
| `rebalance_5_offset_1` | 0.1052 | 0.1035 | 0.1139 | -0.0931 | false |
| `rebalance_5_offset_2` | -0.0173 | -0.1226 | 0.4408 | -0.0198 | false |
| `rebalance_5_offset_3` | 0.0503 | 0.1351 | -0.2744 | 0.0796 | false |
| `rebalance_5_offset_4` | -0.1314 | -0.1443 | -0.0326 | 0.0027 | false |

The child improves OS relative to parent across all `rebalance_5` phases, but it does not keep positive OS across all phases and never beats the parent in IS turnover-aware score. This is not a stable implementation policy.

`rebalance_10_offset_5` is numerically the strongest single variant:

| Metric | Parent | Child | Child - Parent |
| --- | ---: | ---: | ---: |
| Search turnover-aware score | 0.2709 | 0.2732 | 0.0023 |
| IS turnover-aware score | 0.4252 | 0.2581 | -0.1671 |
| OS turnover-aware score | -0.3275 | 0.3299 | 0.6574 |

But this is a single phase among ten. It is not a bridge-family result.

## Cost Sensitivity

The candidate remains cost fragile.

Selected search turnover-aware scores:

| Variant | Parent at 2.5 bps | Child at 2.5 bps | Parent at 5 bps | Child at 5 bps |
| --- | ---: | ---: | ---: | ---: |
| `rebalance_5` | 0.0144 | 0.0725 | -0.1936 | -0.1517 |
| `rebalance_5_offset_1` | 0.1983 | 0.1052 | -0.0117 | -0.1208 |
| `rebalance_5_offset_3` | -0.0293 | 0.0503 | -0.2345 | -0.1698 |
| `rebalance_10_offset_5` | 0.2709 | 0.2732 | 0.1570 | 0.1510 |
| `signal_decay_10` | 0.0161 | 0.1153 | -0.0994 | -0.0318 |

At 5 bps, the strongest single child bridge does not beat the parent (`rebalance_10_offset_5`: 0.1510 vs 0.1570), and most other child bridges are negative. This does not meet a robust cost-conversion standard.

## Interpretation

The child is not useless, but its evidence is the wrong shape for promotion.

What appears stable:

- adding dollar-volume confidence often reduces turnover under slower bridges;
- the child frequently improves OS relative to the parent;
- all mechanical hard gates pass.

What fails:

- the primary daily bridge remains bad;
- `rebalance_5` depends heavily on phase;
- `rebalance_10` has one strong phase but weak median behavior;
- signal-decay variants are OS-heavy and IS-negative;
- no bridge family is robust;
- 5 bps costs remove most of the apparent gain.

The most likely reading is regime/phase-specific cost-shape improvement, not a new stable alpha parent.

## Decision

Do not promote.

Do not convert `expr_smoothed_rev_liq_bridge_20260526` into a first-class bridge-aware parent.

Do not run full validation.

Do not spend another deterministic follow-up on this same child unless a future expression independently rediscovers the mechanism with stronger IS stability.

## Next Step

Resume expression-population search, but inject this run as negative memory.

The next remote generation run should be an expression episode v2, not another bridge robustness run. It should:

1. load the prior expression population ledger from `expression_episode_20260526`;
2. keep multi-root search rather than focusing on this child;
3. tell Qwen that multiplicative raw liquidity gating of smoothed reversal was phase-sensitive and not robust;
4. require primary daily improvement first, while treating bridge variants as diagnostics;
5. prefer mechanisms that reduce turnover without sacrificing IS turnover-aware score;
6. keep bridge diagnostics in the artifact, but avoid selecting a new parent solely because one bridge phase is strong.

Recommended parent roots:

- continue `expr_smoothed_rev`, but with a warning against repeating the liquidity-gated child;
- continue `expr_mom_060_ind` as an OS-regime diagnostic only if the prompt asks for IS-stability repair;
- pause or downweight `expr_size_ind_rev` unless the prompt is made more mechanism-specific, because the first episode already triggered branch pause diagnostics.

Before the next remote run, local work should add a compact bridge-robustness lesson to the expression prompt or remote instruction so the model sees the negative evidence directly.
