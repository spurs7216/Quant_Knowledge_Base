---
title: Seed Zoo IS OS Review 20260522
type: project_evidence_review
status: active
updated: 2026-05-22
tags:
  - project
  - phase4
  - seed-zoo
  - daily-stock
  - is-os
---
# Seed Zoo IS OS Review 20260522

## Artifact

- Artifact zip: `artifacts/seed_zoo_is_os_20260521.zip`
- Remote artifact root: `seed_zoo_is_os_20260521/`
- Git commit recorded by remote summaries: `f6c135ee9972b6df9a56c3c68efd86393a0ddfe1`
- Remote hygiene: clean worktree, `HEAD == origin/main`
- Split: `daily_stock_top500_is_2011_2022_os_2023_2025_v1`
- Cost setting: `total_cost_bps = 2.5`, cost grid `0,1,2.5,5,10`
- Reference summary: repaired attempt017 IS/OS forward-return run

## Mechanical Result

All 10 deterministic seed-zoo programs completed `remote_sample_eval` with `sample_pass`.

No seed failed the hard mechanics:

- rolling top-500 universe and repaired forward-return source were used;
- portfolio coverage was high, roughly `0.9786` to `0.9946`;
- books were balanced long/short with negligible net exposure;
- max single-name weight stayed near `1.0%`;
- reference-equivalence checks said each seed was metric-distinct from repaired attempt017.

This means the seed-zoo infrastructure is healthy. The result is not a promotion result; it is parent-discovery evidence.

## Aggregate Ranking

Ranked by search-sample turnover-aware score at 2.5 bps:

| Rank | Seed | IS Sharpe | OS Sharpe | Search Sharpe | Turnover | Turnover-Aware Score | Note |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | `five_day_excess_reversal` | `0.0687` | `-0.0475` | `0.0463` | `0.7894` | `-0.2511` | Best costed seed, but weak OS. |
| 2 | `momentum_reversal_blend` | `-0.1436` | `-0.0621` | `-0.1264` | `0.6709` | `-0.3473` | Lowest turnover among broad simple seeds. |
| 3 | `liquidity_confidence_reversal` | `0.0202` | `-0.1108` | `-0.0057` | `0.8217` | `-0.3611` | Better than naive liquidity intuition, but not strong. |
| 4 | `industry_neutral_reversal` | `-0.0661` | `-0.0310` | `-0.0593` | `0.8534` | `-0.3727` | Useful neutralization branch, not a lead. |
| 5 | `vol_norm_five_day_reversal` | `-0.0362` | `0.0658` | `-0.0164` | `0.8509` | `-0.3791` | Good gross signal and positive OS, cost-fragile. |
| 6 | `size_bucket_reversal` | `-0.0985` | `0.0698` | `-0.0651` | `0.8567` | `-0.4293` | Similar to vol-normalized branch. |
| 7 | `kalman_ewm_reversal` | `-0.1729` | `0.4459` | `-0.0562` | `0.9824` | `-0.4518` | High OS, negative IS, high turnover; diagnostic only. |
| 8 | `one_day_excess_reversal` | `-0.9454` | `0.2220` | `-0.7167` | `1.7093` | `-1.2441` | Too high-turnover and unstable. |
| 9 | `beta_residual_reversal` | `-1.2753` | `-0.4260` | `-1.1119` | `1.7589` | `-1.7047` | Reject as current root. |
| 10 | `kalman_reversal_base` | `-1.3701` | `-0.3332` | `-1.1553` | `1.7950` | `-1.8041` | Reject as current root. |

Against repaired attempt017, every seed had negative benchmark deltas. The best seed, `five_day_excess_reversal`, still trailed attempt017 on benchmark turnover-aware score by about `0.2833` and on search Sharpe by about `0.1781`.

## Cost Read

The cost grid is the important lesson.

At zero cost, several seeds show gross signal:

- `kalman_ewm_reversal`: Sharpe `0.646`
- `industry_neutral_reversal`: Sharpe `0.632`
- `vol_norm_five_day_reversal`: Sharpe `0.579`
- `liquidity_confidence_reversal`: Sharpe `0.567`
- `size_bucket_reversal`: Sharpe `0.562`
- `five_day_excess_reversal`: Sharpe `0.522`

At 2.5 bps, almost all of that disappears:

- only `five_day_excess_reversal` stays slightly positive on search Sharpe, at `0.046`;
- all turnover-aware scores are negative;
- high-turnover variants, especially one-day reversal, beta-residual reversal, and base Kalman reversal, become clearly unusable as roots.

Interpretation: the daily-stock reversal family has gross structure, but current simple implementations trade too much. The next search should not ask for a completely new signal first. It should ask for cost-aware execution transformations that preserve reversal ranking while reducing turnover and improving holding stability.

## Direct Next-Step Read

A direct metric read would choose `five_day_excess_reversal` as the new lead deterministic seed because it is the only seed with positive 2.5 bps search Sharpe and the highest turnover-aware score among the seed zoo.

However, direct promotion would be too aggressive because:

- its OS Sharpe is slightly negative;
- its turnover-aware score is still below repaired attempt017;
- its edge appears thin after realistic costs;
- it does not solve the project-level obstacle by itself.

Direct conclusion: use `five_day_excess_reversal` as an active root, not as a promoted candidate.

## Zoom-Out Diagnosis

The seed-zoo run changes the diagnosis of the stall.

The problem is not simply that Qwen cannot propose better children. We were evolving from one parent branch whose remaining weakness is not missing-held weight or mechanical validity; it is cost sensitivity and train-period robustness. The seed zoo confirms that many simple reversal ideas have gross alpha-like behavior before costs, but the portfolio implementation burns the edge through daily churn.

At the system level, the next useful AlphaEvolve loop should be a parent-zoo search:

- keep repaired attempt017 as the incumbent benchmark and exploitation root;
- add one or two deterministic seed roots that expose simpler reversal structure;
- mutate toward holding stability, turnover control, liquidity-aware execution, and ranking persistence;
- evaluate against parent-relative and benchmark-relative cost-aware metrics;
- reject children that improve OS by hurting IS, shrinking coverage, or relying on sparse trade days.

Zoom-out conclusion: do not replace attempt017 with the seed zoo. Use the seed zoo to widen the root set and make the search objective explicitly cost-friction aware.

## Final Decision

Do not promote any seed-zoo program.

Implement the next controller milestone as a small multi-parent cost-aware root batch:

1. Parent roots:
   - incumbent: repaired `attempt017`;
   - deterministic lead: `five_day_excess_reversal`;
   - cost-fragile but informative branch: `vol_norm_five_day_reversal`;
   - optional low-turnover diagnostic branch if budget allows: `momentum_reversal_blend`.
2. Treat `kalman_ewm_reversal` as a diagnostic/regime card only, not a primary search root, because its OS Sharpe is high but IS Sharpe is negative and turnover is high.
3. Mutations should target:
   - signal persistence and causal smoothing;
   - no-trade bands that preserve both-side exposure;
   - holding-period aware ranking;
   - liquidity/capacity confidence that changes ranks without inverse-volume instability;
   - side-renormalized turnover caps that preserve max-weight and net exposure contracts.
4. Sample-evaluate at most one child per parent branch after controller review.
5. No full validation and no test-set use.

## Practical Implementation Needs

Before the next remote run, add or verify:

- controller batch metadata carries `parent_strategy_id` and `parent_root_id`;
- sample-eval eligibility can compare a child against both its parent and the incumbent benchmark;
- duplicate/equivalence checks can use prior summaries from seed siblings and attempt017-family siblings;
- prompt cards include the cost-grid lesson: gross Sharpe alone is insufficient when 2.5 bps turns the edge negative;
- remote instructions explicitly say the goal is cost-aware preservation of reversal signal, not generic dampening.

## Sources

- `artifacts/seed_zoo_is_os_20260521.zip`
- `seed_zoo_results.csv`
- `seed_zoo_report.md`
- per-seed `evaluator_summary.json`, `review.md`, `cost_sensitivity.csv`, and `returns_by_split.csv`
