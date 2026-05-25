---
title: Daily Stock Expression Evolution V1
type: implementation_note
status: active
updated: 2026-05-26
tags:
  - project
  - phase4
  - alphaagentevo
  - expression-evolution
  - daily-stock
sources:
  - "alphaagentevo_transfer_20260525.md"
  - "../../../wiki/methods/AlphaAgentEvo-Style Alpha Evolution for Quant Search.md"
  - "../../../wiki/sources/papers/AlphaAgentEvo - Evolution-Oriented Alpha Mining via Self-Evolving Agentic Reinforcement Learning.md"
---
# Daily Stock Expression Evolution V1

## Goal

Create a smaller, safer search object before another broad Python-patch controller batch.

The current controller can generate executable children, but the child space has been too local: smoothing, dampening, and near-repeat portfolio edits. AlphaAgentEvo suggests moving the early search object closer to an alpha expression, then evaluating a multi-turn trajectory rather than isolated one-shot patches.

## Implemented Files

- `research/alphaevolve_lite/expression_evolution.py`
- `research/alphaevolve_lite/expression_episode.py`
- `research/alphaevolve_lite/expression_eval_records.py`
- `research/alphaevolve_lite/expression_population.py`
- `research/alphaevolve_lite/scripts/export_expression_interface.py`
- `research/alphaevolve_lite/scripts/run_expression_seed_zoo.py`
- `research/alphaevolve_lite/scripts/run_expression_episode.py`
- `research/alphaevolve_lite/tests/test_expression_evolution.py`
- `research/alphaevolve_lite/tests/test_expression_episode.py`

## Expression Contract

Expressions can reference only admitted daily-stock aliases:

```yaml
ret: DlyRetx
total_ret: DlyRet
benchmark_return: vwretd
excess_ret: DlyRetx - vwretd
price: abs(DlyPrc)
volume: DlyVol
dollar_volume: DlyPrcVol
market_cap: DlyCap
shares_outstanding: ShrOut
```

`SICCD` is not a tradable raw field in the expression DSL. It is used internally only by `industry_neutralize`.

Operators are safe vectorized functions:

```yaml
cross_sectional:
  - rank
  - zscore
  - winsorize
  - industry_neutralize
time_series:
  - delay
  - delta
  - rolling_mean
  - rolling_sum
  - rolling_std
  - rolling_rank
  - rolling_beta
math:
  - safe_divide
  - log1p_abs
  - signed_sqrt
  - clip
conditional:
  - where
```

The AST validator rejects attribute access, imports, file IO, subscripts, comprehensions, loops, undefined names, chained comparisons, and non-positive rolling windows. It also caps expression length, AST node count, nesting depth, and operator-call count before evaluation. This is important because expression evolution should explore alpha semantics, not mutate infrastructure or create resource-denial artifacts.

## Portfolio Bridge

The bridge converts a signal into dollar-neutral long/short weights using fixed top/bottom quantiles, minimum names per side, max-weight limits, and gross-exposure caps.

This deliberately preserves the Phase 4 evaluator contract:

- no generator control over universe;
- no generator control over IS/OS split;
- no generator control over transaction cost;
- no generator control over forward-return construction;
- no generator control over promotion gates.

## Seed Library

The first catalog has 24 starter expressions. It covers:

- one-day and multi-day reversal;
- volatility-normalized reversal;
- industry-neutral residuals;
- liquidity and dollar-volume confidence;
- capacity tilts through market-cap ranks;
- intermediate momentum;
- horizon interactions;
- volume-pressure and volatility-event variants;
- rolling benchmark-beta residuals;
- path-shape filters.

This is a starter library, not the final AlphaEvo-style bank. The next version should expand only after remote baselines attach measured IS/OS, turnover, max-weight, null-relative, and failure-mode evidence.

## Trajectory Score

`score_expression_trajectory` reports:

- attempt count;
- valid ratio;
- pass@T by turn;
- best score, best turn, and best expression id;
- improvement streak;
- seed consistency;
- exploration versus prior expressions;
- deterministic trajectory score.

This score is diagnostic. It should inform prompt-card fitness, parent selection, and reasoning-memory extraction, but it is not an automatic promotion gate.

## Remote Seed Evaluation

The deterministic remote seed evaluator is `research/alphaevolve_lite/scripts/run_expression_seed_zoo.py`.

It loads the active daily-stock window, applies the frozen static eligibility filter, builds the lagged rolling top-500 universe, attaches one-day-forward returns from the eligible raw panel, evaluates expression seeds into fixed long/short weights, and writes:

- `expression_evaluator_summary.json`;
- `expression_rankings.csv`;
- `expression_scorecard.csv`;
- `expression_cost_sensitivity.csv`;
- universe and split artifacts;
- the prompt-facing expression interface and seed library.

This script intentionally does not call Qwen. It gives us seed-expression baseline evidence before using a model to evolve them.

`expression_sample_pass` is an expression seed-zoo status, not promotion. It now requires portfolio coverage, max-weight compliance, near-zero net exposure, finite turnover-aware score, and max missing-held weight within the same 0.05 sample tolerance used by the main evaluator.

## Remote Expression Episode

The Qwen-backed remote episode runner is `research/alphaevolve_lite/scripts/run_expression_episode.py`.

It:

- calls remote Qwen through `model_router.py`;
- requires JSON-only expression proposals, not Python patches;
- writes every system prompt, user prompt, and model response under `model_calls/`;
- parses malformed or empty model content into explicit `model_parse_error` records;
- rejects exact duplicate expressions before data-backed evaluation;
- records structural similarity to the parent and prior siblings;
- samples later-turn parents from eligible child survivors by default, rather than repeatedly mutating only the original seed;
- writes a population ledger with MAP-style descriptors, parent-selection records, selection scores, and branch stop-loss diagnostics;
- evaluates valid expressions through the same rolling top-500, forward-return, IS/OS, cost, max-weight, net-exposure, coverage, and missing-held contracts as the seed-zoo evaluator;
- writes per-parent trajectory summaries using valid ratio, pass@T, consistency, exploration, best score, and best turn.

The local Windows machine still must not run Qwen. Local verification uses `--mock-response-json`, which exercises the real loader/evaluator path with a saved JSON response.

## Why This Part Matters

The AlphaAgentEvo supplemental implementation is incomplete as a direct transplant: the local source includes interface and data assets, but the referenced reward implementation is not fully present and there are port/count inconsistencies. The transferable idea is therefore the objective decomposition, not the exact code.

For our project, the goal of this part is:

1. make alpha proposals more semantic than Python diff patches;
2. keep the generator inside verified daily-stock fields;
3. produce fast validity/pass@T evidence before expensive sample eval;
4. preserve existing evaluator hardening;
5. create trajectory records that could later support RL or prompt-policy learning.

## Next Remote Step

Run `remote_expression_episode_run_v1` from [expression_episode_remote_instructions_20260526.md](expression_episode_remote_instructions_20260526.md).

Episode command shape:

```bash
python research/alphaevolve_lite/scripts/run_expression_episode.py \
  --csv-path /path/to/daily_stock.csv \
  --out-dir artifacts/phase4_alphaevolve/expression_episode_YYYYMMDD \
  --start-date 2011-01-01 \
  --end-date 2025-12-31 \
  --out-sample-start 2023-01-01 \
  --top-n 500 \
  --total-cost-bps 2.5 \
  --parent-seed-id expr_smoothed_rev \
  --parent-seed-id expr_size_ind_rev \
  --parent-seed-id expr_mom_060_ind \
  --turns 2 \
  --offspring-per-turn 2 \
  --parent-sampling-mode population_mixed \
  --branch-stop-loss-min-children 4 \
  --model-role fast_generator \
  --max-tokens 8192
```

This is still a population-aware pilot, not the final Phase 4 production loop. Do not run full validation or promotion from this layer until expression winners have been converted into reviewed executable strategy programs.
