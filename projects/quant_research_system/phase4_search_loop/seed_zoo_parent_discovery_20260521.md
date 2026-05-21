---
title: Seed Zoo Parent Discovery 2026-05-21
type: project
status: implemented
updated: 2026-05-21
tags:
  - project
  - phase4
  - alphaevolve
  - seed-zoo
  - parent-discovery
sources:
  - "remote_sample_eval_is_os_forward_repair_review_20260520.md"
  - "daily_stock_eda_full_review_20260518.md"
  - "daily_stock_forward_coverage_review_20260519.md"
---
# Seed Zoo Parent Discovery 2026-05-21

## Purpose

The attempt017 branch has been useful, but Phase 4 has spent too long trying to repair one modest local parent. The seed zoo is a deterministic parent-discovery layer before more LLM evolution.

This is not grid search as the final research method. It is a way to populate the program database with several interpretable daily-stock parents so AlphaEvolve has better starting points.

## Implemented Boundary

Code:

- `research/alphaevolve_lite/seed_zoo.py`
- `research/alphaevolve_lite/scripts/run_seed_zoo.py`
- `research/alphaevolve_lite/tests/test_seed_zoo.py`

Evaluator compatibility:

- `remote_sample_eval.py` now accepts `--program-kind seed` for non-canonical deterministic parent programs.
- Seed-zoo programs are recorded as generation-0 seed candidates, not as children of the canonical Kalman seed.
- Strategy descriptors now include `strategy_family` and `strategy_id`.

The seed zoo renders concrete executable strategy programs under the run artifact directory. Each rendered program contains normal Phase 4 strategy hooks and EVOLVE blocks:

```python
compute_signal
rank_or_transform_signal
construct_portfolio
apply_risk_controls
```

That means a winning seed-zoo parent can later become a normal AlphaEvolve parent path.

## Seed List

```yaml
seed_count: 10
program_prefix: PROG-20260521-SEEDZOO
seeds:
  - one_day_excess_reversal
  - five_day_excess_reversal
  - vol_norm_five_day_reversal
  - beta_residual_reversal
  - liquidity_confidence_reversal
  - industry_neutral_reversal
  - size_bucket_reversal
  - momentum_reversal_blend
  - kalman_reversal_base
  - kalman_ewm_reversal
```

The set intentionally includes simple parents, normalized parents, neutralized parents, liquidity-aware parents, and Kalman anchors. The goal is to answer whether attempt017 is genuinely a good parent or merely the best result from an over-narrow initial family.

## Ranking Rule

The aggregate seed-zoo report writes:

- `seed_zoo_results.json`
- `seed_zoo_results.csv`
- `seed_zoo_report.md`

Rows include:

```yaml
metrics:
  - IS Sharpe
  - OS Sharpe
  - search-sample Sharpe
  - annualized return
  - turnover
  - turnover-aware score
  - max missing-held weight
  - max weight
  - IS-to-OS Sharpe degradation
  - benchmark deltas if attempt017 summary is supplied
tier:
  candidate: sample_pass, positive OS Sharpe, positive turnover-aware score, broad enough coverage
  review: everything else
```

The admission score is only for parent triage. It is not promotion evidence and not final validation.

## Important Design Choice

The first implementation calls the existing repaired `remote_sample_eval.py` once per generated seed. This is intentionally conservative:

- every seed gets the exact same artifact contract as prior sample evaluations;
- each seed has its own program snapshot, git record, diagnostics, cost sensitivity, and evaluator summary;
- no new multi-strategy evaluator path can accidentally diverge from the repaired forward-return source contract.

If remote runtime becomes a bottleneck, the next refactor can extract shared data preparation from `remote_sample_eval.py` and evaluate many programs after one CSV load. That is an optimization, not needed before the first seed-zoo evidence run.

## Verification

Local checks passed:

```text
python -m py_compile research/alphaevolve_lite/seed_zoo.py research/alphaevolve_lite/scripts/run_seed_zoo.py research/alphaevolve_lite/scripts/remote_sample_eval.py research/alphaevolve_lite/tests/test_seed_zoo.py
python -m unittest discover research/alphaevolve_lite/tests
python research/alphaevolve_lite/scripts/run_seed_zoo.py --csv-path dummy.csv --out-dir .tmp/seed_zoo_render_smoke --render-only
```

The unit test imports every rendered program through the same loader used by `remote_sample_eval.py`, then checks that each generated parent produces nonempty long/short books and respects max-weight control on synthetic daily-stock data.

## Next Step

Run [seed_zoo_remote_instructions_20260521.md](seed_zoo_remote_instructions_20260521.md) on the remote machine. Do not run Qwen. Do not run a controller batch until the seed-zoo parent ranking is reviewed.
