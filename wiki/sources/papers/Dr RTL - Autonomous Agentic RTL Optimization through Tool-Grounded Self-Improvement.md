---
title: Dr RTL - Autonomous Agentic RTL Optimization through Tool-Grounded Self-Improvement
type: source
status: active
read_scope: full_source
technical_depth: method_level
updated: 2026-05-04
tags:
  - source
  - paper
  - llm-agents
  - tool-grounded-optimization
  - skill-learning
sources:
  - "../../raw/Alpha_evolve/Dr. RTL - Autonomous Agentic RTL Optimization through.pdf"
  - "https://github.com/hkust-zhiyao/DR_RTL/tree/main"
  - "https://github.com/hkust-zhiyao/DR_RTL/tree/main/.claude"
---
# Dr RTL - Autonomous Agentic RTL Optimization through Tool-Grounded Self-Improvement

## Summary

Dr. RTL is a tool-grounded agentic optimization framework for register-transfer-level timing optimization. Its transferable contribution is not RTL-specific code rewriting. The reusable method is:

```text
fine-grained tool diagnosis
-> parallel sibling candidate rewrites
-> deterministic tool evaluation
-> group-relative selection
-> confidence-aware skill extraction
-> future skill-guided optimization
```

The paper reports a realistic RTL setting with human-written designs, commercial synthesis, sequential equivalence checking, and fine-grained timing reports. It then uses a multi-agent loop and a reusable skill library to improve timing and area beyond commercial synthesis.

For AlphaEvolve-style quant research, the key lesson is that a system should not only store candidate programs and scores. It should learn reusable transformation skills from matched sibling comparisons.

## Section 1 - Introduction

The introduction argues that prior LLM-based RTL optimization is too weak as evidence because it often starts from manually degraded designs, uses small modules, relies on weak open-source toolchains, and receives only coarse design-level feedback.

Dr. RTL instead targets realistic human-written RTL. The agent interacts with industrial EDA tools, reads fine-grained critical-path reports, proposes RTL transformations, evaluates them with synthesis and sequential equivalence checking, and distills reusable optimization skills.

The transferable idea is tool-grounding. The LLM is not the evaluator. It is a proposal generator inside a verified loop.

## Section 2 - Problem Formulation

The paper formulates RTL timing optimization as improving post-synthesis PPA while preserving equivalence to the original design. The objective combines WNS, TNS, and area under a correctness constraint.

The important method point is the separation between hard validity and scalar tradeoff. A candidate that fails equivalence is not scored as a weak candidate. It is invalid.

For quant research, the analogue is:

```text
validity first: no leakage, fixed split, point-in-time data, fixed costs, fixed universe
then score: net performance, stability, turnover, capacity, concentration, novelty
```

## Section 3 - Agentic RTL Optimization Evaluation Environment

The evaluation environment has three upgrades over prior work:

- original human-written RTL rather than manually degraded examples;
- commercial synthesis plus sequential formal equivalence checking;
- iteration metrics including best PPA, improvement, pass rate, and convergence steps.

The quant analogue is to avoid toy alpha repair benchmarks. The system should evaluate on realistic data contracts, realistic costs, rolling universes, null baselines, and held-out validation discipline.

## Section 4 - Dr. RTL Methodology

The method has two coupled pieces: a closed-loop multi-agent optimizer and group-relative skill learning.

### Agent Design

The orchestrator coordinates the loop, selects among parallel candidates, and maintains structured JSON trajectory logs.

The timing analysis agent diagnoses critical paths and root causes but does not propose fixes. This role separation matters because diagnosis should be tied to tool output rather than free-form creativity.

The optimization agent rewrites RTL using either learned skills or proposed new transformations. It records whether the transformation came from learned memory or new exploration.

The evaluation agent runs synthesis and equivalence checking only. It performs no reasoning or interpretation.

This maps directly to quant search:

```text
analysis agent: read evaluator diagnostics and identify failure modes
optimization agent: propose bounded SEARCH/REPLACE diffs
evaluation agent: run deterministic checks and backtests
skill learner: compare sibling attempts and update reusable memory
orchestrator: schedule, select, log, and promote
```

### Group-Relative Skill Learning

The central idea is to compare parallel candidates generated from the same parent under the same context. Absolute outcomes can be noisy and design-dependent. Within-group comparison gives a cleaner signal.

Dr. RTL computes a relative advantage from candidate score compared with the group mean and standard deviation. It then extracts pattern-strategy pairs from relatively successful trajectories and tracks empirical statistics such as occurrence count, pass count, and mean relative advantage.

For quant, a group is a sibling batch generated from one parent alpha under the same dataset, split, cost model, and evaluator stage. A relative skill signal is more informative than an isolated child result.

## Section 5 - Experimental Results

The paper evaluates 20 real-world RTL designs with 10 iterations and 5 parallel candidates per iteration. The reported average result is WNS/TNS improvement of about 21%/17%, area reduction of about 6%, and SEC pass rate of about 86%.

The ablations are the strongest evidence for the architecture:

- removing fine-grained timing feedback causes the largest performance drop;
- replacing the multi-agent design with a single agent reduces performance;
- removing the learned skill library reduces both optimization quality and pass rate.

The quant translation is clear: scalar Sharpe alone is weak feedback; specialized roles help; reusable skill memory improves validity and convergence.

## Section 6 - Discussion

The discussion externalizes the learned skill library. Skills are organized by confidence:

- high-confidence strategies;
- medium-confidence strategies;
- low-confidence or risky strategies;
- anti-patterns that should be avoided.

Each skill has applicability, strategy, expected effect, risk, and evidence. This is more operational than raw memory. It tells the next optimizer when to reuse a transformation and when to avoid one.

The GitHub `.claude/skill/rtl-opt/skill.md` file shows the practical skill format: pattern, strategy, expected improvement, area impact, risk, evidence, and key insight. The `.claude/agents/` folder shows the role definitions used by the agent loop.

## Section 7 - Conclusion

The conclusion frames Dr. RTL as a step toward practical agentic design automation. The enduring lesson is that agentic optimization should accumulate reusable knowledge from verified tool interaction, not rely on one-shot model reasoning.

## GitHub Implementation Notes

The public repository exposes the operational design:

- `CLAUDE.md`: orchestrator rules, versioning, scoring, promotion, end criteria;
- `.claude/agents/rtl-timing-analyzer.md`: diagnosis-only critical-path analyzer;
- `.claude/agents/rtl-optimizer.md`: skill-guided or proposed rewrite agent;
- `.claude/agents/rtl-synthesis-evaluator.md`: execution-only evaluator;
- `.claude/agents/rtl-opt-skill-extractor*.md`: per-design and cross-design skill extraction;
- `.claude/skill/rtl-opt/skill.md`: confidence-aware skill library with anti-patterns.

The most useful implementation detail is the structured trajectory:

```json
{
  "diversity_strategy": {},
  "critical_paths": [],
  "evaluation": {},
  "scoring": {}
}
```

This is the exact type of evidence packet a quant AlphaEvolve loop should create for every sibling batch.

## Transfer To Quant Research

Dr. RTL should improve our Phase 4 design in three ways:

1. The evaluator summary should become diagnostic, not only scalar.
2. Sibling batches should be compared group-relatively before extracting memories.
3. Reasoning memory should evolve into a confidence-aware skill library with success strategies and avoid strategies.

Immediate patch:

- add group-relative controller reports to `reasoning_memory_update`;
- record top and bottom siblings by controller-static quality;
- aggregate strategy stats by target surface and patch intent;
- use those records as the evidence packet for later remote Qwen self-contrast extraction.

## Related Notes

- [[Group-Relative Skill Learning for Alpha Search]]
- [[Reasoning Memory for AlphaEvolve Search]]
- [[AlphaEvolve Lite Quant Search Workflow]]
- [Phase 4 Dr RTL transfer note](../../../projects/quant_research_system/phase4_search_loop/dr_rtl_method_transfer_20260504.md)
