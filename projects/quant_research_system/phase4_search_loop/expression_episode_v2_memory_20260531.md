---
title: Expression Episode V2 Research Memory 20260531
type: project_memory
status: active
updated: 2026-05-31
tags:
  - project
  - phase4
  - expression-evolution
  - research-memory
  - bridge-policy
sources:
  - "expression_episode_20260526_review.md"
  - "expression_bridge_followup_review_20260526.md"
  - "expression_bridge_robustness_review_20260526.md"
  - "phase4_caveat_repair_ledger.md"
---
# Expression Episode V2 Research Memory 20260531

Use this as reviewed memory for the next Qwen expression episode. It is a compact prompt input, not a promotion decision.

## Negative Bridge Memory

The child

```text
rank(-rolling_mean(rolling_sum(excess_ret, 5), 3)) * rank(log1p_abs(dollar_volume))
```

looked interesting only under selected slower bridge variants. It failed the primary daily bridge, failed bridge-family robustness, and was not cost robust at 5 bps. Do not reuse it as a parent, do not repeat raw multiplicative liquidity gating as the main idea, and do not select a child because one rebalance phase is strong.

## Search Objective

The next run is a multi-root expression-population episode. It should improve daily-bridge behavior first. Bridge variants are diagnostics for implementation robustness, not the primary selection objective.

Good children should try to reduce turnover or improve IS stability without creating sparse event-only books, one-sided exposure, excessive max weight, high missing-held weight, or OS-only phase artifacts.

## Population Discipline

Load the prior `expression_population_ledger` from `expression_episode_20260526`. Later turns should sample eligible survivor children when present, not repeatedly rewrite only the original root seed.

Keep three roots active unless branch stop-loss pauses one:

- `expr_smoothed_rev`: improve cost conversion and OS behavior without repeating liquidity-gated phase overfit.
- `expr_mom_060_ind`: treat OS-positive momentum as a regime diagnostic and repair negative IS stability.
- `expr_size_ind_rev`: use only if the model proposes a concrete mechanism beyond raw size or ordinal industry; raw `industry` is forbidden except inside `industry_neutralize(...)`.

## Mechanism Pressure

Prefer causal expression-level mechanisms over parameter grid search:

- robust date-level ranks, winsorization, and smoothing;
- industry-neutral or industry-aware residualization through the DSL operator only;
- volatility or drawdown state controls that affect rank or holding stability;
- liquidity and capacity features used as confidence or robustness controls, not ordinal stand-ins for expected return;
- turnover reduction that preserves broad daily coverage.

Avoid:

- exact or near duplicates of seed expressions or prior child expressions;
- raw SIC/industry numeric trading;
- stronger daily churn;
- sparse no-trade artifacts;
- children selected by OS-only behavior or a lucky rebalance offset.

