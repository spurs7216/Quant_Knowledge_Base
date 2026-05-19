---
title: Phase 4 IS/OS Evaluation Policy 2026-05-19
type: project
status: active
updated: 2026-05-19
tags:
  - project
  - phase4
  - evaluator
  - split-policy
  - daily-stock
sources:
  - "universe_and_split_policy.md"
  - "current_state.md"
  - "daily_stock_forward_coverage_review_20260519.md"
  - "evaluator_forward_return_contract_repair_20260519.md"
  - "../../../wiki/datasets/daily_stock.md"
---
# Phase 4 IS/OS Evaluation Policy 2026-05-19

## Decision

Phase 4 now uses a fixed in-sample / out-of-sample split for data-backed AlphaEvolve feedback.

```yaml
split_id: daily_stock_top500_is_2011_2022_os_2023_2025_v1
analysis_window_start: 2011-01-01
analysis_window_end: 2025-12-31
in_sample: dates before 2023-01-01
out_sample: dates on or after 2023-01-01
universe: rolling_top500_market_cap_v1
data_scope: daily_stock_only
```

The exact first and last trading dates must be computed from the cleaned eligible trading calendar and recorded in `split_manifest.yaml`.

## Why

The older 70/15/15 split was statistically disciplined but awkward for the current research loop. The user-facing quant evidence should look like standard in-sample / out-of-sample research:

- IS Sharpe, turnover, drawdown, max weight, missing-held weight;
- OS Sharpe, turnover, drawdown, max weight, missing-held weight;
- IS-to-OS degradation;
- parent-relative and null-relative OS behavior.

The 2018-2020 period was too short to support serious performance interpretation. It is now a smoke/debug window only.

## Use Rules

EDA and coverage diagnostics should use the full available 2000-2025 timeline whenever feasible.

Alpha-evolution performance feedback should use the 2011-2025 development window. The OS window is inspected during search, so it is validation-style OOS, not a pristine final test. If the project later needs final-test evidence, freeze a branch and define a separate locked final-test protocol.

Generated children may not change:

- the analysis window;
- the `out_sample_start` date;
- rolling top-500 universe construction;
- cost grid;
- duplicate policy;
- return timing;
- missing-return policy.

## Implementation Pointers

- `research/alphaevolve_lite/splits.py` owns `build_is_os_splits`.
- `research/alphaevolve_lite/scripts/remote_sample_eval.py` defaults to 2011-2025 with `--out-sample-start 2023-01-01`.
- `research/alphaevolve_lite/sample_eval_metrics.py` owns `build_forward_returns_from_source`, the active evaluator repair that prices rolling top-500 signal rows from the statically eligible raw return source.
- `research/alphaevolve_lite/scripts/profile_daily_stock_forward_coverage.py` defaults its forward-availability diagnostic to 2011-2025.
- Active manifests should use `daily_stock_top500_is_2011_2022_os_2023_2025_v1`.

## Next Evidence

Before new child generation, rerun seed and attempt017-family sample evaluations under the fixed IS/OS policy and the repaired forward-return source contract. This rerun does not require Qwen or vLLM.
