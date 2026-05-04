---
title: Dr RTL Method Transfer To Phase 4
type: project
status: active
updated: 2026-05-04
tags:
  - project
  - phase4
  - dr-rtl
  - group-relative
  - skill-learning
sources:
  - "../../../raw/Alpha_evolve/Dr. RTL - Autonomous Agentic RTL Optimization through.pdf"
  - "../../../raw/Alpha_evolve/MAP-Elites Algorithm Analysis.md"
  - "https://github.com/hkust-zhiyao/DR_RTL/tree/main"
  - "https://github.com/hkust-zhiyao/DR_RTL/tree/main/.claude"
  - "reasoning_memory_layer_design.md"
---
# Dr RTL Method Transfer To Phase 4

## Decision

Before the next remote controller run, Phase 4 should add Dr. RTL-style group-relative sibling reporting to the reasoning-memory update.

This is not an RTL-specific transfer. The useful method is:

```text
parallel siblings from same parent
same tool/evaluator context
deterministic validity and score
relative comparison inside the group
skill extraction from winners and losers
confidence-aware reuse
```

## Paper Readthrough

### Introduction

Dr. RTL criticizes prior LLM RTL optimization as unrealistic because it often optimizes degraded toy RTL with weak tools and coarse feedback. The paper instead starts from human-written RTL, uses industrial synthesis and formal sequential equivalence checking, and reads fine-grained timing diagnostics.

Transfer: our quant loop should not optimize toy strategies or scalar Sharpe only. It needs realistic data contracts, fixed costs, null baselines, and diagnostic evaluator cards.

### Problem Formulation

Dr. RTL optimizes WNS/TNS/area subject to equivalence. Hard correctness is outside the scalar score.

Transfer: Phase 4 must keep leakage, split, universe, cost, and data-contract gates outside the score. Invalid children are rejected, not merely penalized.

### Evaluation Environment

The paper's evaluation reports final PPA, improvement, validity pass rate, and convergence steps.

Transfer: our controller should report not only pass count, but also unique-pass rate, duplicate retry success, MAP-cell count, repair burden, and failure-category distribution.

### Methodology

The orchestrator coordinates specialized agents:

- analyzer: diagnose;
- optimizer: propose transformations;
- evaluator: execute only;
- skill learner: compare trajectories and extract skills.

Transfer: Phase 4 should keep evaluator execution deterministic and non-reasoning. Prompt generation and memory extraction can use Qwen, but validity labels come from controller/evaluator artifacts.

### Group-Relative Skill Learning

The most important method detail is sibling comparison. Dr. RTL compares candidates generated from the same parent under the same timing context, then computes relative advantage against the group.

Transfer: `controller_batch_001_small_semantic_v4` should produce a group-relative controller report. Later remote sample batches should compute sibling-relative market/evaluator quality.

### Results And Ablations

The paper reports that removing fine-grained feedback, multi-agent structure, or the skill library hurts performance. Learned skills also improve pass rate.

Transfer: the next Phase 4 investment should not be only more attempts. It should improve feedback structure and skill extraction quality.

### Discussion And Skill Library

The `.claude/skill/rtl-opt/skill.md` file organizes skills into high-confidence, medium-confidence, low-confidence, and anti-patterns. Each entry has applicability, strategy, expected effect, risk, evidence, and key insight.

Transfer: our reasoning memory should evolve toward confidence-aware skills:

- success strategy;
- repair pattern;
- evaluator caveat;
- avoid strategy;
- data-contract guardrail;
- model-routing guardrail.

## MAP-Elites Conversation Readthrough

The MAP-Elites analysis frames MAP-Elites as illumination rather than just optimization. The output is an archive over user-chosen behavior descriptors, not a single best solution.

The AlphaEvolve discussion translates this into a program database with prompt sampler, LLM ensemble, evaluator pools, and program database.

The Dr. RTL discussion adds a missing layer: an archive of transformation skills. MAP-Elites stores what worked in each niche; Dr. RTL stores why a transformation worked and when to reuse it.

Phase 4 should therefore maintain three related but distinct objects:

- program database: exhaustive child evidence;
- MAP-Elites cells: diverse elites by behavior descriptor;
- skill/reasoning memory: reusable pattern-strategy lessons.

## Patch Implemented

Implemented 2026-05-04:

- `research/alphaevolve_lite/reasoning_memory.py`
  - adds `build_group_relative_controller_report`;
  - computes controller-static quality scores for sibling attempts;
  - records top and bottom siblings by relative advantage;
  - aggregates strategy stats by target surface and patch intent;
  - writes the report into `reasoning_memory_update.json` and `.md`.
- `research/alphaevolve_lite/prompt_builder.py`
  - adds a group-relative sibling role reminder to child-generation prompts.

The score is intentionally controller-specific. It is not a market-alpha score.

## Remote Run Implication

The next remote run command stays the same, but review must include:

```text
artifacts/phase4_alphaevolve/controller_batch_001_small_semantic_v4/reasoning_memory_update.md
```

New review questions:

- Which sibling had the highest controller-relative advantage?
- Which target surface and patch intent produced the best controller behavior?
- Which strategy groups had zero pass rate?
- Did memory cards reduce duplicate or semantic failures?
- Are any candidate memory topics strong enough for remote Qwen self-contrast extraction?

## Still Vague

- The controller-static score is a validity/diversity score, not a future market-quality score.
- We still need a separate group-relative score for `remote_sample_eval`.
- Skill activation should probably require deterministic support plus human review until enough runs exist.
- The 9B model may be enough for structured skill extraction, but 27B may be better for cross-batch abstraction.

## Related Notes

- [[Dr RTL - Autonomous Agentic RTL Optimization through Tool-Grounded Self-Improvement]]
- [[Group-Relative Skill Learning for Alpha Search]]
- [Reasoning memory design](reasoning_memory_layer_design.md)
