---
title: Group-Relative Skill Learning for Alpha Search
type: method
status: active
updated: 2026-05-04
tags:
  - method
  - alphaevolve
  - map-elites
  - skill-learning
  - quant-research
sources:
  - "../sources/papers/Dr RTL - Autonomous Agentic RTL Optimization through Tool-Grounded Self-Improvement.md"
  - "../sources/papers/ReasoningBank - Scaling Agent Self-Evolving with Reasoning Memory.md"
  - "../../raw/Alpha_evolve/MAP-Elites Algorithm Analysis.md"
  - "../../projects/quant_research_system/phase4_search_loop/dr_rtl_method_transfer_20260504.md"
---
# Group-Relative Skill Learning for Alpha Search

## Summary

Group-relative skill learning compares sibling candidates generated from the same parent under the same evaluator context, then extracts reusable transformation knowledge from the relative winners and losers.

It is the quant-search analogue of Dr. RTL's skill learning:

```text
same parent + same diagnostics + same evaluator
-> sibling candidates
-> deterministic validity and score
-> relative advantage within the group
-> pattern-strategy skill update
```

This differs from ordinary program memory. A program database stores candidates. A group-relative skill library stores the conditions under which a transformation tends to work or fail.

## Why Relative Comparison Matters

Absolute backtest outcomes are noisy. A candidate may look good because the parent was easy, the market window was favorable, or the evaluator stage was weak. A sibling group controls some of this variation because all siblings share the same parent, split, cost model, universe, and prompt context.

The useful object is:

```text
strategy advantage = child quality - sibling-group average quality
```

For controller-static batches, quality is not market performance. It is validity, uniqueness, low repair burden, and behavior-cell diversity. For remote sample evaluation, quality can include net performance, turnover, stability, null comparison, cost drag, exposure, and concentration.

## Skill Entry Contract

A quant skill should be evidence-linked:

```yaml
skill_id: skill_...
pattern:
  name: diagnostic failure or opportunity
  diagnostics: evaluator fields that identify it
strategy:
  description: reusable transformation principle
  allowed_mutations: bounded code surfaces or operators
avoid:
  - known risky transformations
evidence:
  sibling_batch_ids: []
  occurrence_count:
  pass_count:
  mean_relative_advantage:
  failure_modes: []
confidence: high | medium | low | avoid
status: active | candidate | superseded | rejected
```

## Relationship To MAP-Elites

MAP-Elites stores the best candidate in each behavior cell. Group-relative skill learning stores transformation knowledge learned while filling those cells.

They answer different questions:

- MAP-Elites: What is the best alpha we have in this niche?
- Skill learning: When a parent has this diagnostic pattern, which transformation tends to help?

The two should be linked through descriptors such as target surface, patch intent, turnover bucket, exposure bucket, strategy family, and data stage.

## Controller-Static Version

Before data-backed child evaluation, we can still learn controller skills.

Controller-static relative quality should reward:

- parse/apply/compile/vector/semantic pass;
- unique child hash;
- distinct normalized patch fingerprint;
- filled MAP cell;
- low repair burden;
- no empty or reasoning-only output.

It should penalize:

- evolve-block violations;
- exact SEARCH mismatch;
- one-sided or net-exposed portfolios;
- duplicate children;
- vector-smoke API mistakes;
- empty final content.

This score is only for prompt/controller learning. It is not evidence of market alpha.

## Remote Evaluation Version

After children reach remote sample evaluation, group-relative quality can include:

- net validation Sharpe or turnover-aware score;
- matched-null improvement;
- parent-relative improvement;
- cost sensitivity;
- turnover and capacity;
- max weight and concentration;
- subperiod stability;
- sector/factor exposure;
- validation exposure penalty.

Invalid candidates should be rejected before scoring.

## Extraction Rule

After each sibling batch:

1. Build an episode packet with attempts, prompt cards, diffs, metrics, gates, and diagnostic summaries.
2. Compute group-relative advantages deterministically.
3. Identify top and bottom sibling patterns.
4. Ask remote Qwen to propose skill candidates from the evidence packet.
5. Promote only skills supported by deterministic evidence.

## Failure Modes

- A small sibling group may not provide enough evidence for a durable skill.
- Relative advantage can reward controller compliance while saying nothing about market quality.
- A skill may overfit one evaluator stage.
- Prompting too many skills can reduce instruction salience.
- LLM skill extraction can over-explain noise; keep evidence thresholds.

## Related Notes

- [[Dr RTL - Autonomous Agentic RTL Optimization through Tool-Grounded Self-Improvement]]
- [[Reasoning Memory for AlphaEvolve Search]]
- [[AlphaEvolve Lite Quant Search Workflow]]
