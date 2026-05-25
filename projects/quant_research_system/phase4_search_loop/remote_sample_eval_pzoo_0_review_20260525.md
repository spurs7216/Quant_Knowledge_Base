---
title: Remote Sample Eval PZOO 0 Review 20260525
type: project_evidence_review
status: active
updated: 2026-05-25
tags:
  - project
  - phase4
  - parent-zoo
  - sample-eval
  - daily-stock
sources:
  - "parent_zoo_curated_sample_eval_remote_instructions_20260522.md"
  - "../../../artifacts/remote_sample_eval_pzoo_0.zip"
---
# Remote Sample Eval PZOO 0 Review 20260525

## Artifact

- Local zip: `artifacts/remote_sample_eval_pzoo_0.zip`
- Included runs:
  - `remote_sample_eval_pzoo_00_0005_20260522`
  - `remote_sample_eval_pzoo_01_0002_20260522`
  - `remote_sample_eval_pzoo_01_0004_20260522`
- Remote commit: `d871f331b8d66980829ccd5c238c171d4ccc5145`
- Remote hygiene: all runs record clean worktree, `HEAD == origin/main`, and fetchable manifest commit.
- Split: `daily_stock_top500_is_2011_2022_os_2023_2025_v1`
- Cost: 2.5 bps total cost.
- Forward-return contract: `signal_universe_t_return_source_eligible_t_plus_1_v1`

All three runs completed and were marked `sample_pass`. In this evaluator, `sample_pass` means the hard gates passed. It does not mean promotion.

## Result Table

| Program | Parent | Mechanism | IS Sharpe | OS Sharpe | Search Sharpe | Turnover | Turnover-aware score | Decision |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| `PROG-20260522-PZOO-00-0005` | attempt017 repair | extra EWM smoothing | 0.3770 | -0.1110 | 0.2786 | 0.1372 | 0.1922 | no promotion; useful low-turnover control |
| `PROG-20260522-PZOO-01-0002` | five-day excess reversal | EWM-summed reversal | 0.1833 | 0.1324 | 0.1735 | 0.7748 | -0.1202 | no promotion; gross edge but cost fragile |
| `PROG-20260522-PZOO-01-0004` | five-day excess reversal | per-name volatility regime proxy | 0.1134 | 0.1143 | 0.1136 | 0.8251 | -0.1927 | no promotion; weaker than `01_0002` |

Common portfolio diagnostics were healthy:

- portfolio-day coverage: 0.9893 to 0.9920;
- max weight: about 1.04%;
- max missing-held weight: 1.04% for `00_0005`, 2.0% for five-day children;
- net exposure near zero;
- gross exposure near one.

## Parent-Relative Read

### `PROG-20260522-PZOO-00-0005`

Relative to attempt017 repair:

- search Sharpe improved from 0.2244 to 0.2786;
- turnover dropped from 0.5602 to 0.1372;
- turnover-aware score improved from 0.0322 to 0.1922;
- gross Sharpe fell from 0.6258 to 0.3868;
- OS Sharpe became negative at -0.1110.

This is not promote-ready because the OS behavior is wrong. It is still useful evidence: the current evaluator strongly rewards lower turnover after cost, and attempt017 may have too much churn. The mechanism is a control lesson, not a new alpha thesis.

### `PROG-20260522-PZOO-01-0002`

Relative to the five-day excess reversal seed:

- search Sharpe improved from 0.0463 to 0.1735;
- gross Sharpe improved from 0.5216 to 0.6280;
- turnover-aware score improved from -0.2511 to -0.1202;
- turnover stayed very high at 0.7748;
- OS Sharpe was positive but only 0.1324.

This child has real controller and evaluator information value. It shows the five-day family has a gross signal that can improve with smoothing, but the net edge is still destroyed by turnover at 2.5 bps.

### `PROG-20260522-PZOO-01-0004`

Relative to the five-day excess reversal seed:

- search Sharpe improved from 0.0463 to 0.1136;
- gross Sharpe improved from 0.5216 to 0.6118;
- turnover-aware score improved from -0.2511 to -0.1927;
- it is worse than `01_0002` on search Sharpe, annualized return, and turnover-aware score;
- it has essentially no IS-to-OS Sharpe degradation, but both levels are weak.

This is negative evidence for the simple per-name volatility dampener as the next main mechanism. It is not a true market-regime model.

## Interpretation

The curated parent-zoo sample eval did not produce a promotable child.

The important new evidence is not "children are too bad" in a broad sense. It is more specific:

1. The attempt017 smoothing child improved cost-aware score by cutting turnover, but lost OS alpha.
2. The five-day children have positive gross signal, but high turnover makes them net-unattractive.
3. The simple volatility-regime proxy is weaker than the EWM smoothing child and does not solve the cost problem.
4. All three results are broad-coverage and mechanically clean, so the conclusion is about alpha/economic quality rather than infrastructure failure.

This means the next search move should not be another broad Python patch batch. We need a higher-level evolution interface that can produce semantic alpha changes and learn from multi-turn feedback.

## Decision

No child is promoted.

Keep as evidence:

- `00_0005`: low-turnover control and cost-awareness lesson.
- `01_0002`: best five-day-family gross edge, but requires turnover-control or holding-period redesign before it can matter.
- `01_0004`: regime-proxy negative control; do not keep sampling simple per-name volatility dampeners as if they were regime models.

Next design move:

1. ingest AlphaAgentEvo and translate its multi-turn trajectory scoring into Phase 4;
2. add a factor-expression evolution sandbox before further broad patch generation;
3. use pass@T, valid ratio, trajectory reward, and streak reward as search diagnostics;
4. defer full RL fine-tuning until the expression interface and trajectory database are stable.

## Sources

- `artifacts/remote_sample_eval_pzoo_0.zip`
- `*/evaluator_summary.json`
- `*/metrics.json`
- `*/review.md`
- `*/program_snapshot.py`
