---
title: AlphaAgentEvo - Evolution-Oriented Alpha Mining via Self-Evolving Agentic Reinforcement Learning
type: source
source_type: paper
source_class: paper_source
read_scope: full_source
extraction_basis: local PDF text extraction plus supplementary code inspection
technical_depth: section_level_deep
ingest_stage: promoted
status: active
updated: 2026-05-25
tags:
  - source
  - paper
  - alpha-mining
  - agentic-rl
  - alphaevolve
  - quant-research
sources:
  - "../../../raw/Alpha_evolve/ALPHAAGENTEVO - EVOLUTION-ORIENTED ALPHA MINING VIA SELF-EVOLVING AGENTIC REINFORCE- MENT LEARNING.pdf"
  - "../../../raw/Alpha_evolve/3446_AlphaAgentEvo_Evolution_O_Supplementary Material/AlphaAgentEvo/"
---
# AlphaAgentEvo - Evolution-Oriented Alpha Mining via Self-Evolving Agentic Reinforcement Learning

## Citation / Metadata

- Title: *AlphaAgentEvo: Evolution-Oriented Alpha Mining via Self-Evolving Agentic Reinforcement Learning*
- Venue status in source: ICLR 2026 conference paper.
- Authors in source: Ziyi Tang, Xuexiong Yin, Weixin Chen, Zechuan Chen, Yongsen Zheng, Wenxuan Ye, Keze Wang, Liang Lin.
- Supplement inspected: `AlphaAgentEvo/` project folder with interface prompt, API server, factor-evolution scripts, AlphaEvo500 parquet files, and a `verl` training scaffold.

## Why This Paper Matters

This paper is close to the current Phase 4 project because it treats alpha mining as a multi-turn evaluator-in-the-loop evolution problem, not as independent factor sampling. The main transferable idea is that the learning object should be an evolution policy over trajectories:

```text
seed alpha
  -> think about prior feedback
  -> propose several offspring
  -> evaluate with a backtest tool
  -> reflect
  -> repeat
```

Our current AlphaEvolve-lite loop already has a prompt sampler, model stack, evaluator cascade, program database, MAP-cell diversity pressure, and reasoning memory. AlphaAgentEvo adds a stronger training and scoring view: the agent should be rewarded for valid tool use, structural consistency with a seed, exploration away from repeated ideas, performance improvement, and sustained improvement streaks.

## Section Map

| Section | Role | Durable takeaways |
| --- | --- | --- |
| Abstract / Introduction | Motivation | Alpha mining should move beyond `search-backtest-restart` into continuous alpha evolution with planning and reflection. |
| 2.1 Problem Definition | Formal objective | Learn an evolution policy from seed alpha distribution to evolved alpha sets, evaluated on evolution and test market distributions. |
| 2.2 Self-Evolving Agentic RL | Training algorithm | Extends GRPO to multi-turn tool-in-the-loop trajectories; only policy-generated tokens receive gradients. |
| 2.3 Reward Function | Core mechanism | Hierarchical reward combines tool validity, seed consistency, exploration, performance improvement, and improvement streak. |
| 3 Experiments | Evidence | Qwen3-4B trained with this ARL setup beats stronger prompt-only baselines on pass rates, diversity, and OOS transfer in the paper's benchmark. |
| 4 Related Work | Positioning | Differentiates from GP, LLM prompting, multi-agent alpha agents, and generic self-evolving LLMs. |
| 5 Conclusion | Claim | Self-evolving ARL is presented as a scalable alpha-mining paradigm. |
| Appendix B | Portfolio comparison | Top-10 AlphaAgentEvo alphas are equally combined and compared to TS, RL, and LLM-agent baselines. |
| Appendix C-D | Training details | Qwen3 1.7B/4B, 10 RTX4090, 150 steps, 20 seeds/batch, 3 rollouts/seed, up to 3 turns, up to 4 tool calls/turn. |
| Appendix E | Case study | The trained agent critiques alpha semantics and combines mechanisms, while the baseline mostly tunes windows and normalizations. |
| Appendix F-G | Tool and data | `evaluate_factor` tool schema; data variables and expression functions. |
| Supplement | Implementation evidence | Shows a factor expression interface, FastAPI backtest service, training script, and AlphaEvo500 parquet prompts. Some paper-claimed reward/config pieces are not fully present in the supplement. |

## Core Objects

Let:

- $S = \{s_1,\ldots,s_N\}$ be a stock universe.
- $H = \{h_1,\ldots,h_L\}$ be a time horizon.
- $X \in \mathbb{R}^{N \times L \times d}$ be market features.
- $f$ be an alpha factor mapping observed market data up to time $h$ to a forecast of $r_{h+1}$.
- $D_{\text{seed}}$ be a distribution over seed alphas.
- $\pi$ be an evolution policy.
- $F_\pi(f_{\text{seed}})$ be the evolved alpha set generated from a seed after multi-turn interaction.
- $D_{\text{evo}}$ be the market distribution used during evolution.
- $D_{\text{test}}$ be the held-out or different-regime market distribution.
- $s(f; X)$ be the backtest score.
- $\operatorname{sim}(f_i, f_j)$ be an AST-overlap structural similarity.

The paper frames the objective as learning a policy that maximizes the best evolved alpha's score under both evolution and test distributions, with a structural similarity constraint against the seed.

Important caveat: the printed objective uses a `sim(f, f_seed) <= delta` style constraint, while the prose describes staying in a local interpretable neighborhood and the consistency reward rewards similarity above a low threshold. Since their similarity is AST overlap, larger means more similar. The inequality in the objective is therefore ambiguous relative to the prose. The transferable principle is not the sign of that inequality; it is the need to keep offspring direction-aware and interpretable relative to their seed.

## Agentic RL Formulation

The policy LLM generates multi-turn trajectories. At each turn:

1. the model reasons from the full past trajectory;
2. it proposes $k$ offspring alpha factors as tool calls;
3. the backtesting tool evaluates them;
4. tool responses are appended to the context for the next turn.

The paper extends GRPO to this setting. A group of trajectories from the same prompt or seed is rolled out by the old policy. Rewards are normalized within the group to estimate relative advantages:

$$
\hat A_g = \frac{R(\tau_g) - \mu_T}{\sigma_T}.
$$

Only policy-generated tokens contribute gradients. Tool responses are context but not optimized tokens. This distinction matters for our project: evaluator output should guide the next prompt and database score, but generated code or factor expressions remain the only object credited to the model.

## Reward Function

The reward is hierarchical and capped by component. It is designed to turn noisy backtest feedback into denser learning signals.

### Tool Call Reward

Tool use is rewarded when valid and penalized when failed:

$$
R_{\text{tool}}(\tau)
= \alpha_{\text{succ}} N_{\text{succ}}
- \alpha_{\text{fail}} N_{\text{fail}}.
$$

This teaches the model to make executable tool calls and discourages brute-force invalid proposals.

### Consistency Reward

Consistency keeps the candidate structurally related to the seed. The paper computes structural similarity by AST overlap:

$$
\operatorname{sim}(f_i, f_j)
=
\frac{|AST(f_i) \cap AST(f_j)|}
{\max(|AST(f_i)|, |AST(f_j)|)}.
$$

The consistency reward gives credit when generated factors stay above a low similarity threshold to the seed. The point is not to forbid novelty; it is to prevent uncontrolled semantic drift.

### Exploration Reward

Exploration rewards candidates that are structurally different from previous proposals:

$$
R_{\text{expl}}(\tau)
=
\sum_{f_i \in F_{\text{succ}}(\tau)}
\alpha_{\text{exp}}
\left(
1 - \max_{f_j \in F_{<i}(\tau)}
\operatorname{sim}(f_i, f_j)
\right).
$$

This is close to our MAP-cell and near-duplicate policy, but expressed as a trajectory reward instead of only a rejection rule.

### Performance Reward

Performance reward uses a smooth transform of improvement over the seed threshold:

$$
R_{\text{perf}}(\tau)
\propto
\log \left(1 + \exp(s(f^*) - \max(0, s(f_{\text{seed}})))\right).
$$

The success condition used in experiments is stricter than "better than seed": an evolved alpha must beat $\max(0, s(f_{\text{seed}}))$. This matters in alpha mining because many seed alphas are weak or negative.

### Streak Reward

The streak reward gives a bonus for the longest sequence of progressive performance improvements. This rewards an evolution trajectory that learns and compounds, not just one lucky offspring.

### Total Reward

The paper caps each reward component and combines them hierarchically. Tool, consistency, and exploration provide dense compliance and search-quality feedback. Performance and streak provide the higher-level objective. The practical insight is that a single scalar such as Sharpe or IR is too sparse and noisy to teach a useful alpha-evolution policy by itself.

## Experimental Setting

### Datasets

The paper constructs AlphaEvo500 as an expert-curated benchmark. The paper states 350 training seed alphas, 50 validation seeds, and 100 test seeds. The supplement's parquet files inspected locally contain 300 train, 30 validation, and 100 test rows, so the released supplement appears smaller or not fully aligned with the paper text.

The paper also uses Alpha158 as an external test library.

### Markets And Backtests

The paper evaluates on China A-share universes including HS300 and CSI500 over January 2023 to November 2025. Model training uses one year of market data, 2023-01-01 to 2024-01-01, to accelerate iteration. Evaluation uses a bearish period, 2023-01-01 to 2024-01-01, and a bullish period, 2024-01-01 to 2025-01-01.

The factor protocol is single-factor and long-only:

- factor values are cross-sectional signals;
- rebalance every 5 trading days;
- buy at most the top 10% of stocks with non-NaN factor values;
- default metric is Information Ratio with cost in the supplement.

### Metrics

The paper tracks:

- valid ratio: syntactically valid and executable factor generations;
- pass@3 and pass@5: whether any alpha through turn $T$ beats $\max(0, s(f_{\text{seed}}))$;
- annualized excess return;
- information ratio;
- structural similarity among top alphas;
- OOS transfer performance.

The authors explicitly avoid IC-style metrics because some seed factors are Boolean selectors with NaN for unselected stocks.

## Main Results

The strongest reported result is that AlphaAgentEvo-4B beats prompt-only and tool-use baselines despite using a smaller model than closed-source reasoning baselines. On AlphaEvo500, the paper reports AlphaAgentEvo-4B near the top in valid ratio and pass rates across HS300 and CSI500. On Alpha158, AlphaAgentEvo-4B again has high valid ratio and strong pass@5, especially in the 2024-2025 period.

The diversity analysis is also important. The paper compares structural similarity among top generated alphas and reports that AlphaAgentEvo-4B has both low average and lower maximum similarity than several LLM baselines. The intended interpretation is that training with consistency plus exploration avoids both random drift and repeated local patterns.

The case study is the most useful qualitative evidence. The baseline model proposes horizontal tweaks such as window changes or z-scoring. AlphaAgentEvo critiques the seed's trading semantics, notices that the signal direction may be wrong, and combines the seed with mechanisms such as RSI, volatility adjustment, swing points, industry neutralization, and ATR. This is the behavior our current loop is missing when it repeatedly generates smoothing or dampening variants.

## Supplementary Material

The supplement includes:

- `factor_evolution/interface_rl_v2.md`: a factor-construction interface that lists variables, functions, output rules, and an example conditional expression.
- `factor_evolution/evo_factor.py`: an OpenAI-compatible local server client that asks Qwen3-4B to call `evaluate_factor`, sends factors to a backtest API, appends tool responses, and repeats multi-turn evolution.
- `factor_evolution/generate_factor_dataset.py`: builds parquet training samples with prompt, reward-model placeholder, seed answer, and tool metadata.
- `api_server_fast.py` and `start_api.py`: a FastAPI backtest service with `/backtest`, `/health`, `/example`, and `/test_expr`.
- `AlphaEvo500/*.parquet`: released seed-prompt datasets.
- `run_qwen3-4b_instruct_alphaevo_multiturn.sh`: `verl` GRPO training script using Qwen3-4B-Thinking, max prompt length 4096, max response length 10000, rollout `n=3`, max model length 14500, and multi-turn assistant cap 2 in the script.

Local supplement caveats:

- The reward function file referenced by the run script was not present in the inspected supplement path.
- The paper says AlphaEvo500 is 350/50/100 train/validation/test, while the local parquet release is 300/30/100.
- The supplement has port inconsistencies: API service documentation says port 8001, `api_server_fast.py` standalone block says port 8000, and some scripts point to 8001 or 8003.
- The supplement is still useful as an implementation sketch, but it is not a fully self-contained reproducibility package.

## Transferable Lessons

1. Alpha evolution should be evaluated as a trajectory, not only as isolated offspring.
2. A small open model can outperform larger prompt-only models when trained or scored against the right multi-turn tool objective.
3. Validity, consistency, exploration, performance, and streak are separate signals; collapsing them into Sharpe alone loses search information.
4. Expression-level factor evolution can explore semantic alpha ideas faster than arbitrary program patching.
5. A seed library is part of the method, not an afterthought. The agent learns how to transform seed families.
6. Structural similarity is useful both as a diversity metric and as a guard against semantic drift.
7. Good alpha evolution needs a rich operator/data interface. The agent cannot invent usable mechanisms if the allowed variables and operators are too narrow or poorly surfaced.

## Caveats

- The market, universe, and data variables differ from our WRDS daily-stock setting.
- The paper's backtest horizon is short relative to our 2011-2025 development window.
- The reported protocol is long-only top-decile; our first loop is dollar-neutral long/short.
- The training objective uses repeated tool feedback on market data, so overfit control depends heavily on hidden evaluation periods and transfer tests.
- The supplement is incomplete for exact reward reproduction.
- The method should not justify immediate RL fine-tuning in our project before we have a stable expression/evaluator interface and a large trajectory dataset.

## Related Notes

- [[AlphaEvolve - A coding agent for scientific and algorithmic discovery]]
- [[AlphaEvolve Lite Quant Search Workflow]]
- [[AlphaAgentEvo-Style Alpha Evolution for Quant Search]]
- [[Reasoning Memory for AlphaEvolve Search]]
- [[Group-Relative Skill Learning for Alpha Search]]
- [Phase 4 current state](../../../projects/quant_research_system/phase4_search_loop/current_state.md)
