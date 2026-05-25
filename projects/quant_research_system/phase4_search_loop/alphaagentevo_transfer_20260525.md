---
title: AlphaAgentEvo Transfer 20260525
type: project_synthesis
status: active
updated: 2026-05-25
tags:
  - project
  - phase4
  - alphaagentevo
  - alphaevolve
  - agentic-rl
  - daily-stock
sources:
  - "../../../wiki/sources/papers/AlphaAgentEvo - Evolution-Oriented Alpha Mining via Self-Evolving Agentic Reinforcement Learning.md"
  - "../../../wiki/methods/AlphaAgentEvo-Style Alpha Evolution for Quant Search.md"
  - "remote_sample_eval_pzoo_0_review_20260525.md"
---
# AlphaAgentEvo Transfer 20260525

## Why We Read It Now

Phase 4 has been stuck in a local-patch regime. The controller and evaluator are healthy, but the generated children are mostly:

- smoothing or dampening;
- turnover changes without robust OS alpha;
- regime labels implemented as per-name volatility dampeners;
- cost-fragile variants of the same reversal family.

The latest parent-zoo sample eval confirms this. `PROG-20260522-PZOO-00-0005` has the best net score because turnover collapses, but OS Sharpe is negative. The five-day children have positive gross Sharpe but high turnover and negative turnover-aware scores.

AlphaAgentEvo is relevant because it attacks exactly this failure mode: prompt-only agents tend to get trapped in repetitive local modifications, while a self-evolving trajectory learns to critique prior attempts and reconstruct alpha semantics.

## Setting Comparison

| Dimension | AlphaAgentEvo | Phase 4 currently | Transfer implication |
| --- | --- | --- | --- |
| Search unit | factor expression | executable Python strategy patch | Add expression-level search; Python patching is too heavy for early semantic exploration. |
| Interaction | multi-turn trajectory with tool calls | mostly one-shot child batch plus later review | Add episode runner with several turns and feedback. |
| Model | Qwen3 1.7B/4B trained by GRPO | Qwen3.5 9B generator, 27B/35B reviewers, no training | Do not assume larger model fixes search; objective and feedback loop matter more. |
| Reward | tool, consistency, exploration, performance, streak | hard gates plus evaluator metrics, prompt fitness, MAP policy | Add trajectory score and pass@T diagnostics before RL. |
| Seed base | AlphaEvo500 seed alpha library | seed-zoo has 10 deterministic strategy parents | Build a larger daily-stock expression seed library. |
| Data | China A-share price, chip, money flow, benchmark, industry | WRDS daily_stock only for first loop | Use only admitted daily-stock fields now; later consider dataset admission for richer flow/fundamental data. |
| Portfolio | long-only top 10%, 5-day rebalance | dollar-neutral long/short top/bottom quantiles, daily-ish weights | Keep our portfolio contract, but borrow factor-expression evolution. |
| Evaluation | IR/AER, valid ratio, pass@3/pass@5, diversity, transfer | IS/OS Sharpe, turnover, cost, concentration, nulls, hard gates | Add valid ratio, pass@T, structural similarity, and trajectory streak. |
| OOS | different periods/regimes and Alpha158 transfer | 2011-2022 IS, 2023-2025 OS; test locked | Add regime slices for search diagnostics without unlocking final test. |

## What We Should Adopt

### 1. Factor-Expression Evolution Sandbox

The biggest practical change is to add a safe daily-stock expression layer.

Current Python evolve blocks are good for final implementation hardening, but they make exploration too local. A factor DSL lets the model propose ideas like:

```text
industry_neutralize(rank(rolling_sum(excess_return, 5)))
rank(rolling_beta(return, benchmark_return, 60) residual reversal)
rank(short_term_reversal / rolling_volatility)
rank(liquidity_adjusted_reversal)
```

The sandbox should compile expressions into the fixed Phase 4 portfolio/evaluator contracts. It must not let generated children edit universe, split, costs, data loading, or portfolio risk rules.

### 2. Daily-Stock Seed Library

AlphaAgentEvo relies on seed alphas. Our 10-program seed zoo is too small for learning transformation behavior.

Build an `AlphaEvo_US_daily_stock` seed library with 50-100 expressions covering:

- one-day and five-day reversal;
- volatility-normalized reversal;
- momentum and reversal interactions;
- benchmark residuals and rolling beta residuals;
- liquidity and dollar-volume conditioning;
- price level and market-cap conditioning only through ranks/log transforms;
- industry-neutral ranks where group size is adequate;
- simple persistence and holding-period proxies.

Each seed should store mechanism label, allowed operators, expected failure mode, and baseline IS/OS metrics.

### 3. Multi-Turn Episode Runner

Run a small episode per seed:

```yaml
turns: 3
offspring_per_turn: 2-4
evaluator: controller_static first, then sample_eval for selected frontier
feedback_to_model:
  - valid or invalid
  - gross and net metrics
  - turnover and cost drag
  - parent-relative score
  - structural similarity
  - duplicate or MAP-cell status
```

This should be implemented before any RL training. It gives us the trajectory data needed to decide whether training is justified.

### 4. Trajectory Reward For Search Control

Adopt AlphaAgentEvo's reward decomposition as a deterministic score:

```text
trajectory_score =
  capped(tool_validity)
  + capped(seed_consistency)
  + capped(exploration)
  + capped(performance_improvement) * capped(streak)
  - turnover_cost_penalty
  - concentration_penalty
```

Use this score for prompt-card fitness, parent sampling, MAP-cell ranking, and reasoning-memory extraction. Do not use it as an automatic promotion score.

### 5. Pass@T And Valid Ratio

Every multi-turn run should report:

- valid ratio;
- pass@1, pass@3, pass@5 or pass@T;
- best turn;
- best child by gross score;
- best child by net score;
- best child by turnover-aware score;
- duplicate rate;
- structural diversity among top children.

This tells us whether the system is actually evolving or merely sampling.

### 6. Structural Similarity As A Soft Band

We already reject duplicates and near duplicates. AlphaAgentEvo adds the other side: keep children related enough to the seed to remain interpretable.

For expression alphas, use token/AST similarity bands:

```yaml
too_close: duplicate or lazy local tweak
useful_band: related mechanism with structural change
too_far: unrelated search jump unless explicitly scheduled as exploration
```

This is better than only rejecting exact duplicates.

## What We Should Not Adopt Yet

- Do not start GRPO or LoRA training immediately. We lack enough clean daily-stock trajectories.
- Do not import China-specific chip-distribution or money-flow assumptions into US daily_stock without dataset admission and point-in-time checks.
- Do not switch the production objective to long-only top 10%. Our first-loop contract is dollar-neutral long/short.
- Do not train on one year and claim robust alpha. Use the 2011-2025 IS/OS development policy.
- Do not expose data range, universe, cost, or split controls to the generator.

## Concrete Next Milestone

Milestone: `daily_stock_expression_evolution_v1`.

Deliverables:

1. expression grammar and safe operator registry;
2. compiler from expression to signal panel under `daily_stock_contract_v1`;
3. fixed portfolio bridge into the existing evaluator;
4. 50-100 seed expressions;
5. controller/evaluator smoke tests for no lookahead, finite values, coverage, rank behavior, industry group size, and duplicate handling;
6. remote handoff for a small multi-turn Qwen episode batch;
7. artifact schema for trajectory records, pass@T, valid ratio, structural similarity, and trajectory score.

This is the best route to a breakthrough because it changes the proposal space from local Python modifications to semantic factor construction while keeping the evaluator contracts we have already hardened.

## Implementation Slice 2026-05-25

Implemented the first bounded slice in `research/alphaevolve_lite/expression_evolution.py`.

Included now:

- safe expression parser and AST validator;
- admitted daily-stock fields from `daily_stock_contract_v1`;
- causal operators: cross-sectional rank/z-score/winsorization, industry neutralization, positive delays, rolling mean/sum/std/rank/beta, safe division, conditional `where`, clipping, and simple transforms;
- fixed bridge from expression signal to constrained dollar-neutral top/bottom-quantile weights;
- starter seed catalog with 24 daily-stock expressions across reversal, momentum, benchmark residual, liquidity, volatility, capacity, industry-neutral, and path-shape mechanisms;
- expression similarity for duplicate/consistency diagnostics;
- deterministic trajectory score with valid ratio, pass@T, best turn, improvement streak, consistency, and exploration;
- prompt-facing export script: `research/alphaevolve_lite/scripts/export_expression_interface.py`;
- focused unit tests in `research/alphaevolve_lite/tests/test_expression_evolution.py`.

This slice intentionally does not yet run Qwen, call the sample evaluator, write program-database rows, or promote expression children. It creates the smaller semantic search object that the next remote episode runner can use.

Important design choice: expression evolution is not allowed to edit universe, IS/OS split, data loading, total cost, portfolio accounting, or promotion gates. Those stay in the existing evaluator/controller layer.

## Open Questions

- Should the first expression sandbox be long/short only, or should it also report a long-only diagnostic to match the AlphaAgentEvo paper?
- Should expressions be allowed to reference `SICCD` industry-neutralization in v1, or should industry-neutral operators wait for a group-size smoke gate? Current answer: allowed through `industry_neutralize`, with date-level z-score fallback when the industry group is too small.
- Should the expression seed library include intentionally weak or negative seeds so the agent learns sign correction, as in AlphaAgentEvo's case study?
- What should be the first `pass@T` success threshold: improve over parent, improve over zero, or improve over attempt017 incumbent after costs?

## Decision

Adopt the AlphaAgentEvo trajectory-scoring and expression-evolution ideas. Defer RL training. The next implementation step should be the daily-stock expression sandbox and seed library, not another broad Qwen patch batch.
