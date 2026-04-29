---
title: Phase 4 Cost Model Policy
type: project
status: active
updated: 2026-04-27
tags:
  - project
  - phase4
  - transaction-costs
  - evaluator
---
# Phase 4 Cost Model Policy

## Decision

Do not use `10` bps total cost as the default assumption for liquid U.S. equity research.

Use `2.5` bps total proportional cost as the current continuity baseline for early Phase 4 daily-stock research. Treat it as a placeholder until liquidity-conditioned spread and impact estimates are implemented.

Use `10` bps total cost as a severe stress scenario, not as the central estimate.

## Phase 4 Cost Grid

```yaml
cost_grid_bps_total:
  frictionless_diagnostic: 0.0
  baseline_continuity: 2.5
  moderate_stress: 5.0
  severe_stress: 10.0
```

Policy:

- Do not promote a high-turnover strategy solely because it passes at `0.0` or `2.5` bps.
- Do not reject a liquid strategy solely because it fails at `10.0` bps.
- Always report gross and net metrics.
- Always report annualized cost drag.
- Always report turnover by split.

## Required Reporting

Every Phase 4 remote validation job must report:

- gross return metrics;
- net metrics at the full cost grid;
- turnover by split;
- annualized cost drag by split;
- liquidity buckets;
- exchange buckets when available;
- long-side and short-side contribution if long-short;
- max and p99 single-name absolute weight;
- borrow-cost placeholder or explicit missing-borrow warning for short books.

## Promotion Rules

A candidate can survive for mutation if it is interesting but cost fragile. It cannot promote to the candidate registry unless cost robustness is acceptable.

Promotion requires:

```yaml
cost_promotion_requirements:
  baseline_net_metrics_reported: true
  moderate_stress_metrics_reported: true
  severe_stress_metrics_reported: true
  annualized_cost_drag_reported: true
  turnover_by_split_reported: true
  cost_fragility_bucket_not_broken: true
```

## Cost Fragility Buckets

```yaml
cost_fragility_bucket:
  robust:
    description: survives baseline and moderate stress; severe stress not catastrophic
  moderate:
    description: survives baseline; moderate stress weakens but does not destroy evidence
  fragile:
    description: survives only baseline or only frictionless; may survive for mutation but not promote
  broken:
    description: disappears after realistic cost or depends on extreme turnover
  unknown:
    description: insufficient artifact output
```

## Evolve-Block Restriction

Generated candidates may not remove, weaken, bypass, or silently alter cost accounting.

Allowed mutations:

- reduce turnover;
- add no-trade bands;
- smooth target weights;
- add liquidity-aware weighting;
- penalize cost-fragile names.

Disallowed mutations:

- setting cost to zero;
- changing cost grid;
- removing turnover accounting;
- hiding trades through stale weights;
- changing rebalance timing to avoid measured turnover without declaring it.
