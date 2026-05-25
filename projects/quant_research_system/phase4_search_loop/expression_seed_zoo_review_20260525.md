---
title: Expression Seed Zoo Review 20260525
type: project_evidence_review
status: active
updated: 2026-05-25
tags:
  - project
  - phase4
  - expression-evolution
  - daily-stock
  - seed-zoo
  - alphaagentevo
sources:
  - "expression_seed_zoo_remote_instructions_20260525.md"
  - "daily_stock_expression_evolution_v1.md"
  - "../../../artifacts/expression_seed_zoo_20260525.zip"
---
# Expression Seed Zoo Review 20260525

## Artifact

- Local zip: `artifacts/expression_seed_zoo_20260525.zip`
- Remote artifact root: `artifacts/phase4_alphaevolve/expression_seed_zoo_20260525`
- Run id: `expression_seed_zoo-20260525T132813+0000-111f3a3a`
- Commit: `981b1d31e2104820dc8c2fa381b4a03dd21a7da4`
- Remote hygiene: `git_dirty=false`, `git_head_matches_origin_main=true`, commit fetchable from GitHub
- Qwen/vLLM: not used

## Mechanical Result

The expression seed-zoo evaluator worked as intended.

```yaml
status: ok
seed_count: 24
expression_sample_pass: 23
expression_sample_review: 1
expression_error: 0
contract_id: daily_stock_contract_v1
universe_policy: rolling_top500_market_cap_v1
split_id: daily_stock_top500_is_2011_2022_os_2023_2025_v1
analysis_dates:
  in_sample: 2011-01-03_to_2022-12-30
  out_sample: 2023-01-03_to_2025-11-28
```

Data diagnostics were normal for this stage:

- loaded rows after date filter: 29,757,924;
- rows after duplicate policy: 29,751,954;
- rows after static eligibility: 14,754,079;
- split calendar count: 3,750 trading dates;
- monthly rolling universe months: 178;
- selected count: 500 names every month.

## Main Empirical Read

The baseline expression layer is mechanically healthy, but the seed library does not contain a promotable alpha.

The decisive issue is cost conversion. Several expressions have positive gross/no-cost turnover-aware scores, but almost all become negative after the default 2.5 bps cost. Only one expression has positive full-window turnover-aware score after cost, and it fails OS robustness.

| Expression | Read | Search Sharpe | Turnover | Search TA | IS Sharpe | IS TA | OS Sharpe | OS TA |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `expr_smoothed_rev` | best full-window net expression, but OS negative | 0.1947 | 0.5250 | 0.0124 | 0.2745 | 0.0922 | -0.1312 | -0.3120 |
| `expr_rev_minus_mom` | high IS, fails OS | 0.2064 | 0.6112 | -0.0464 | 0.3429 | 0.0890 | -0.3657 | -0.5639 |
| `expr_stable_liq_rev` | high IS, cost/OS fragile | 0.1522 | 0.6411 | -0.2081 | 0.2970 | -0.0638 | -0.4188 | -0.6269 |
| `expr_size_ind_rev` | only positive IS and OS Sharpe, but net negative after cost | 0.0690 | 0.7527 | -0.2192 | 0.0731 | -0.2158 | 0.0540 | -0.1812 |
| `expr_rev_005` | five-day baseline is too turnover-heavy | 0.0232 | 0.7887 | -0.2740 | 0.0467 | -0.2506 | -0.0760 | -0.3226 |
| `expr_liquidity_momentum` | strong OS, strongly negative IS; likely regime-specific | -0.5026 | 0.5151 | -0.7314 | -0.8106 | -1.0411 | 0.6760 | 0.5045 |
| `expr_mom_060_ind` | OS-positive momentum diagnostic, negative IS | -0.3611 | 0.2526 | -0.4752 | -0.5061 | -0.6208 | 0.2253 | 0.1144 |
| `expr_ranked_rev_vol` | correctly marked review due coverage failure | -0.0844 | 0.7531 | -0.3227 | 0.0704 | -0.1682 | -0.6203 | -0.8576 |

Counts:

- positive full-window turnover-aware score at 2.5 bps: 1/24 (`expr_smoothed_rev`);
- positive IS and OS Sharpe: 1/24 (`expr_size_ind_rev`);
- positive OS turnover-aware score: 2/24 (`expr_mom_060_ind`, `expr_liquidity_momentum`), both with negative IS behavior;
- expression sample-review: 1/24 (`expr_ranked_rev_vol`) due portfolio-day coverage 0.6925 below the 0.80 threshold.

## Cost Sensitivity

At 0 bps, the top expressions look much better:

| Expression | TA at 0 bps | TA at 2.5 bps | Turnover |
| --- | ---: | ---: | ---: |
| `expr_size_ind_rev` | 0.4513 | -0.2192 | 0.7527 |
| `expr_smoothed_rev` | 0.3220 | 0.0124 | 0.5250 |
| `expr_stable_liq_rev` | 0.3113 | -0.2081 | 0.6411 |
| `expr_rev_minus_mom` | 0.3054 | -0.0464 | 0.6112 |
| `expr_rev_size_005` | 0.3050 | -0.2353 | 0.5803 |

This is useful evidence. The first expression-evolution episodes should not ask the model for wholly new economic stories. They should ask it to convert weak gross reversal/momentum signals into lower-turnover, broader-coverage, still-dollar-neutral portfolios without changing the evaluator contract.

## Caveats

- `expression_sample_pass` means the expression passed mechanical expression-seed gates, not promotion.
- The current expression portfolio bridge is a common top/bottom quantile long-short book. It is intentionally simpler than full strategy programs.
- OS is available to the current search loop by policy, but the final test set remains locked. OS-positive and IS-negative behavior should be treated as regime evidence, not alpha.
- The strong OS momentum expressions are probably 2023-2025 regime-specific unless further subperiod diagnostics show otherwise.
- The expression seed catalog is still small. It is a starter library for trajectory learning, not a finished alpha bank.

## Decision

No seed should be promoted and no seed should directly replace attempt017.

The artifact supports moving to an expression-evolution episode runner, but with a narrow objective:

1. preserve the fixed evaluator contracts;
2. start from a small set of evidence-bearing seed expressions;
3. optimize cost conversion and regime stability, not raw Sharpe;
4. record valid ratio, pass@T, similarity, and trajectory score before any program promotion.

## Recommended Parent Seeds For First Qwen Expression Episode

Use three parent roles:

1. `expr_smoothed_rev`
   - role: full-window net incumbent among expression seeds;
   - objective: keep turnover near or below 0.52 while repairing OS weakness;
   - avoid: higher-turnover variants of the same reversal.
2. `expr_size_ind_rev`
   - role: only seed with positive IS and OS Sharpe;
   - objective: reduce turnover/cost drag while preserving broad coverage and both-split sign;
   - avoid: raw size trading or one-sided capacity filters.
3. `expr_mom_060_ind` or `expr_liquidity_momentum`
   - role: OS-positive regime diagnostic, not a promotion parent;
   - objective: test whether the model can add IS-stability controls to a post-2023 momentum effect;
   - avoid: selecting it as an incumbent solely because OS is high.

Do not use `expr_ranked_rev_vol` in the first Qwen episode unless the goal is specifically to study tied/coverage behavior.

## Next Step

Implement `remote_expression_episode_runner_v1`.

Minimum requirements:

- JSON-only Qwen expression proposals, not Python patches;
- expression safety/resource validation before evaluation;
- duplicate and structural-similarity accounting;
- fixed parent-seed schedule for the first run;
- deterministic full-window expression evaluation using the same `run_expression_seed_zoo.py` contracts;
- per-turn feedback with IS/OS, turnover, max weight, missing-held, coverage, and cost sensitivity;
- trajectory summary with valid ratio, pass@T, best turn, seed consistency, exploration, and trajectory score;
- no full validation and no promotion.

After the first episode batch, decide whether to convert any expression winner into a full executable strategy program for `remote_sample_eval`.
