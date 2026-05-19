---
title: Evaluator Forward-Return Contract Repair 2026-05-19
type: project-note
status: implemented
updated: 2026-05-19
tags:
  - project
  - phase4
  - evaluator
  - daily-stock
sources:
  - "daily_stock_forward_coverage_review_20260519.md"
  - "is_os_evaluation_policy_20260519.md"
  - "../../../wiki/datasets/daily_stock.md"
---
# Evaluator Forward-Return Contract Repair 2026-05-19

## Problem

The forward-coverage diagnostic showed that top-500 daily coverage is broadly healthy, but unavailable one-day-forward rows were concentrated around month-end membership transitions. The old sample evaluator built one-day-forward returns after applying the monthly rolling top-500 universe:

```text
eligible raw panel -> rolling top-500 universe panel -> grouped shift for fwd_ret
```

That can create a false missing-held-weight event. A date-t holding can exit the next month's top-500 universe while still having a valid date-(t+1) return in the statically eligible raw panel. If the evaluator shifts only within `universe_panel`, that valid next-day return is hidden.

## Repaired Contract

The repaired sample evaluator separates two roles:

- signal-date universe: rolling top-500 membership at date t;
- forward-return source: duplicate-resolved, statically eligible raw panel before monthly top-500 filtering.

The explicit contract id recorded by remote sample evaluation is:

```yaml
forward_return_contract: signal_universe_t_return_source_eligible_t_plus_1_v1
signal_panel_source: rolling_top500_universe_panel
forward_return_source: eligible_static_panel
```

Implementation:

- `research/alphaevolve_lite/sample_eval_metrics.py`
  - adds `build_forward_returns_from_source(signal_panel, return_source_panel, contract)`;
  - keeps `build_forward_returns(panel, contract)` as a same-panel diagnostic wrapper.
- `research/alphaevolve_lite/scripts/remote_sample_eval.py`
  - now calls `build_forward_returns_from_source(universe_panel, eligible, CONTRACT)`;
  - records the source contract in `run_manifest.json`, `evaluator_summary.json`, and database descriptors.

## Timing Discipline

This repair does not let generated strategy programs read future data. Strategy functions still receive the signal-date `eval_panel`, but the prompt and controller contracts forbid generated children from using evaluator-only fields:

- `fwd_ret`
- `fwd_date`
- `fwd_vwretd`
- `next_market_date`
- `one_day_forward`

Those fields belong to evaluator accounting only. The strategy's tradable universe remains rolling top-500 at date t.

## Regression Tests

The local regression test covers the important failure mode:

- a stock is in the date-t signal universe on `2022-01-31`;
- it exits the next month's top-500 signal universe;
- the eligible raw panel still has its `2022-02-01` return;
- the repaired helper attaches that `2022-02-01` return and marks `one_day_forward = true`.

A second test verifies that if the next market date exists but the held security has no next-day eligible row, the evaluator records `fwd_date` as that next market date and marks `one_day_forward = false`. This lets `missing_held_weight` count the missing held position instead of silently dropping the date.

## Research Implication

Previous missing-held-weight failures, especially attempt017-family results, are now suspect as evaluator artifacts until rerun under this repaired contract and the fixed IS/OS split. The repair does not make any child promotable by itself. It only removes a known accounting distortion before the next market-evidence comparison.

## Next Evidence

Run the remote sample evaluator, without Qwen or new child generation, for:

1. the canonical seed;
2. `attempt_017`;
3. prior attempt017-family children only if their child program paths are present and reproducible from Git-tracked code plus artifact snapshots.

The required review is:

- confirm `split_id = daily_stock_top500_is_2011_2022_os_2023_2025_v1`;
- confirm `forward_return_source = eligible_static_panel`;
- compare seed versus attempt017 on IS Sharpe, OS Sharpe, turnover, max weight, max missing-held weight, and turnover-aware score;
- decide whether attempt017 remains a useful structural lead after the accounting repair.
