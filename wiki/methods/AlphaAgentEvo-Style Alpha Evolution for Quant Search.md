---
title: AlphaAgentEvo-Style Alpha Evolution for Quant Search
type: method
status: active
updated: 2026-05-25
tags:
  - method
  - alpha-mining
  - alphaevolve
  - agentic-rl
  - quant-research
sources:
  - "../sources/papers/AlphaAgentEvo - Evolution-Oriented Alpha Mining via Self-Evolving Agentic Reinforcement Learning.md"
  - "../../projects/quant_research_system/phase4_search_loop/alphaagentevo_transfer_20260525.md"
---
# AlphaAgentEvo-Style Alpha Evolution for Quant Search

## Summary

AlphaAgentEvo-style search treats alpha mining as multi-turn trajectory optimization. The reusable object is not just a generated alpha. It is the policy behavior that transforms a seed into better alphas after reading evaluator feedback.

For a quant research system, the transferable loop is:

```text
seed alpha or parent program
  -> propose 2-4 offspring
  -> evaluate with a fixed tool
  -> reflect on valid, invalid, stronger, weaker, and repeated candidates
  -> propose next offspring
  -> score the whole trajectory
```

This is different from a one-shot prompt batch. It creates evidence about whether the agent can learn from its own prior attempts.

## Trajectory Score Components

The score should stay decomposed before any scalar aggregation:

| Component | Purpose | Quant translation |
| --- | --- | --- |
| Tool validity | Learn executable proposals | parse, compile, vector smoke, evaluator execution, no malformed tool calls |
| Consistency | Stay related to seed | structural similarity to seed or parent above a low floor |
| Exploration | Avoid repeats | low similarity to prior offspring, new MAP cell, no duplicate signature |
| Performance | Improve objective | parent-relative and max-zero-relative net score improvement |
| Streak | Reward compounding | repeated improvement across turns, not one lucky child |
| Cost realism | Avoid fake alpha | turnover-aware score, cost sensitivity, capacity and max-weight checks |
| Stability | Avoid one-window fit | IS/OS, subperiod, regime, and null-relative checks |

This score can be used for parent sampling, prompt-card fitness, reasoning-memory extraction, and later RL training data. It should not become an automatic promotion rule.

## Why This Helps Phase 4

The current Phase 4 loop has made many controller-safe children, but the market evidence is mostly local smoothing, dampening, or near-repeat behavior. AlphaAgentEvo explains why: isolated patch generation rewards local compliance more than semantic reconstruction.

The paper's case study shows a better behavior pattern:

```text
weak seed
  -> critique signal direction
  -> infer why prior variants failed
  -> combine independent mechanisms
  -> test several offspring
  -> keep the mechanism that improves the trajectory
```

Our current loop should therefore add an expression-level alpha evolution mode before trying RL fine-tuning. Expression proposals let the model combine rank, z-score, industry-neutralization, rolling return, volatility, liquidity, beta residual, and benchmark-relative operators without fighting Python patch boundaries.

## Recommended Adoption Order

Use now:

1. Add trajectory-level evaluation records: turn id, offspring id, parent id, metrics, hard gates, similarity, MAP cell, and prior-feedback summary.
2. Add pass@T and valid-ratio metrics for controller and sample-eval runs.
3. Add a trajectory score with decomposed validity, consistency, exploration, performance, turnover, and streak components.
4. Build a daily-stock expression sandbox with a small safe operator set.
5. Build a seed library of daily-stock expression alphas, not only full Python strategy programs.

Use after the sandbox is stable:

1. Run Qwen multi-turn factor-expression episodes on the remote machine.
2. Store every tool call and evaluator response as a trajectory.
3. Use trajectory self-contrast to update reasoning memory and skill cards.
4. Promote expression winners into executable strategy programs only after sample-eval gates.

Use later:

1. Train or LoRA-tune a small Qwen model with GRPO-style trajectory rewards.
2. Add model-bandit routing across stable remote models.
3. Add richer point-in-time datasets after dataset-admission approval.

Do not adopt blindly:

- China A-share chip and money-flow variables without a point-in-time US data equivalent.
- Long-only top-decile backtests as a replacement for our dollar-neutral first loop.
- One-year training windows as evidence of robust predictive power.
- RL fine-tuning before there is enough clean trajectory data.

## Minimum Daily-Stock Expression Interface

A first expression interface for our project should expose only point-in-time daily-stock fields and safe transforms:

```yaml
fields:
  return: DlyRetx
  price: DlyPrc
  volume: DlyVol
  dollar_volume: DlyPrcVol
  market_cap: DlyCap
  shares_outstanding: ShrOut
internal_grouping:
  industry: SICCD via industry_neutralize only
  benchmark_return: vwretd
operators:
  cross_sectional: rank, zscore, winsorize, industry_neutralize
  time_series: delay, delta, rolling_mean, rolling_sum, rolling_std, rolling_rank
  residualization: rolling_beta, benchmark_residual
  math: log, signed_sqrt, clip, safe_divide
  portfolio_bridge: long_short_top_bottom_quantiles
```

The expression evaluator should compile expressions into the same fixed universe, split, cost, and portfolio contracts already used by Phase 4. Generated expressions may not edit data loading, split rules, costs, or universe construction.

## Implemented V1 In Phase 4

The first production scaffold is `research/alphaevolve_lite/expression_evolution.py`.

Current contract:

- fields are aliases over `daily_stock_contract_v1`: `ret`, `total_ret`, `benchmark_return`, `excess_ret`, `price`, `volume`, `dollar_volume`, `market_cap`, and `shares_outstanding`; `SICCD` is internal to `industry_neutralize` and is not tradable as raw `industry`;
- operators are safe vectorized functions: `rank`, `zscore`, `winsorize`, `industry_neutralize`, `delay`, `delta`, `rolling_mean`, `rolling_sum`, `rolling_std`, `rolling_rank`, `rolling_beta`, `safe_divide`, `log1p_abs`, `signed_sqrt`, `clip`, and `where`;
- AST validation rejects attribute access, imports, subscripts, comprehensions, Python loops, undefined names, chained comparisons, and negative/zero rolling windows;
- portfolio bridge is fixed dollar-neutral long/short top-bottom quantiles with explicit max-weight and minimum-side-count constraints;
- seed catalog starts with 24 expressions, not the final 50-100 target;
- deterministic remote seed evaluation is available through `research/alphaevolve_lite/scripts/run_expression_seed_zoo.py`;
- trajectory scoring reports valid ratio, pass@T, best turn, improvement streak, seed consistency, exploration, and a deterministic scalar diagnostic score.

The prompt-facing export script is `research/alphaevolve_lite/scripts/export_expression_interface.py`. It writes the exact interface markdown and seed-library JSON for remote Qwen runs. The seed-zoo evaluator reuses the repaired rolling top-500, forward-return, IS/OS, cost, max-weight, and coverage contracts without calling Qwen.

Remaining work:

- run the remote expression seed-zoo baseline and review which seeds deserve multi-turn evolution;
- connect expressions to a remote multi-turn episode runner;
- write trajectory artifacts into the existing controller/evaluator evidence path;
- sample-evaluate only frontier expressions, then promote winners into executable seed programs;
- expand the seed catalog with measured baselines and failure modes after the first remote expression batch.

## Related Notes

- [[AlphaAgentEvo - Evolution-Oriented Alpha Mining via Self-Evolving Agentic Reinforcement Learning]]
- [[AlphaEvolve Lite Quant Search Workflow]]
- [[AlphaEvolve Extension Methods for Quant Search]]
- [[Reasoning Memory for AlphaEvolve Search]]
- [[Group-Relative Skill Learning for Alpha Search]]
