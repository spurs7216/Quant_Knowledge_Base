---
title: Reasoning Memory for AlphaEvolve Search
type: method
status: active
updated: 2026-05-04
tags:
  - method
  - alphaevolve
  - reasoningbank
  - memory
  - quant-research
sources:
  - "../sources/papers/ReasoningBank - Scaling Agent Self-Evolving with Reasoning Memory.md"
  - "../../raw/Alpha_evolve/ReasoningBank - Scaling Agent Self-Evolving with Reasoning Memory.pdf"
  - "../../projects/quant_research_system/phase4_search_loop/reasoning_memory_layer_design.md"
---
# Reasoning Memory for AlphaEvolve Search

## Summary

Reasoning memory is the compact lesson layer for an AlphaEvolve-style search loop. It is not the program database. It is not the raw artifact archive. It is the set of prompt-ready lessons distilled from prior proposing, repairing, evaluating, and rejecting.

In a quant search system, reasoning memory should store evidence-linked operating knowledge such as:

- what patch shapes pass controller filters;
- what portfolio transformations violate exposure or concentration semantics;
- what data-contract assumptions are frozen;
- what failure modes Qwen repeatedly shows;
- what evaluator or null-control lessons should be remembered before the next proposal.

## Core Pattern

Let \(c_t\) be the current search context, \(\tau_t\) the trajectory or episode record, and \(y_t\) the deterministic outcome label from the evaluator. A memory extractor produces candidate lessons:

```text
M_t = Extract(c_t, tau_t, y_t)
B_{t+1} = Consolidate(B_t, M_t)
Prompt_t = BuildPrompt(c_t, Retrieve(B_t, c_t))
```

The content of a memory item should be small enough to insert into a prompt and general enough to apply beyond the exact child that produced it.

## Memory Item Contract

Minimum fields:

```yaml
memory_item_id: stable id
memory_type: success_strategy | failure_guardrail | repair_pattern | evaluator_caveat | data_contract | model_routing
title: short label
description: applicability condition
content: concrete prompt-facing lesson
source_run_id: artifact run id
source_program_ids: parent or child ids when available
source_attempt_ids: attempt ids when available
source_outcome: success | failure | mixed
target_surface: signal | ranking | portfolio | neutralization | evaluator | routing | patch_contract
evidence: compact metrics, hard gates, and failure categories
status: candidate | active | superseded | rejected
```

For Phase 4, a memory item is active only if it is supported by a controller or evaluator artifact. LLM-generated memory candidates remain candidate items until a deterministic support check accepts them.

## Extraction

Use different extraction paths for different evidence types:

- success trajectory: extract the reusable strategy or patch form that worked;
- failure trajectory: extract the violated invariant and the corrective guardrail;
- repaired trajectory: extract the exact repair pattern and the original malformed pattern;
- batch of siblings: use self-contrast to compare accepted, rejected, duplicate, and repaired attempts.

ReasoningBank uses an LLM judge to label success or failure. In a quant system, deterministic evaluator outcomes should be the label source whenever possible. The LLM should synthesize the lesson, not decide whether the child was valid.

## Retrieval

Retrieval should be stage-aware before it is semantic.

First filter by hard context:

- data stage, such as `stage_0_daily_stock`;
- controller stage, such as `controller_static` or `remote_sample_eval`;
- target evolve surface, such as `signal` or `portfolio`;
- search island or MAP-Elites behavior cell;
- active status.

Then rank by lexical or embedding similarity. Insert only a small number of high-confidence cards into the prompt. The memory cards should be written as instructions the model can obey, not as vague summaries.

## Integration With Program Search

The program database remains the source of exhaustive search evidence. Reasoning memory is a derived layer.

```text
program_database -> episode packet -> memory candidates -> active memory bank -> prompt sampler
```

The memory bank should store pointers back to artifact paths and database ids. This makes every prompt-facing lesson auditable.

## Group-Relative Skill Signal

Reasoning memory becomes stronger when it uses Dr. RTL-style sibling comparison. A batch of children from the same parent under the same evaluator context is a matched group. The memory update should compare siblings by relative advantage before extracting skills.

At controller-static stage this relative advantage measures validity, uniqueness, repair burden, and MAP-cell diversity. It is not market-alpha evidence. At remote sample-evaluation stage, the relative score can include net performance, cost sensitivity, null comparison, turnover, exposure, and stability.

## Integration With MAP-Elites

MAP-Elites encourages behavioral diversity. Reasoning memory can make that diversity useful by tagging lessons with behavior cells.

Examples:

- a `portfolio_risk_turnover` cell can store exposure-balance and turnover-control lessons;
- a `signal_transform` cell can store ranking, clipping, and smoothing lessons;
- a `repair_near_miss` cell can store malformed but fixable patch patterns.

After a small batch, self-contrast across cells should extract lessons that are more robust than a single-child explanation.

## Quant-Specific Guardrails

Reasoning memory must not become a backtest-overfitting channel.

Do not store lessons such as "increase parameter X because it improved validation Sharpe in this one window" unless the evaluator evidence establishes robustness. Store the structural reason, not a lucky number.

Prefer memories such as:

- "When building long/short proportional weights, convert each side to positive magnitudes before assigning signed weights."
- "Do not expose or edit split, universe, cost, or data-loading code inside child-generation prompts."
- "If a Qwen response has reasoning but no final content, treat it as empty output and retry with thinking disabled."

Avoid memories such as:

- "Use a 17-day lookback because one child improved validation Sharpe."
- "Remove turnover penalties to pass the score gate."
- "Use a dataset not admitted for the current stage."

## Failure Modes

- Memory bloat: too many prompt cards reduce instruction salience.
- Stale memory: an old workaround may conflict with a later frozen contract.
- Over-specific lessons: a memory item may encode a one-run accident.
- Judge leakage: an LLM may infer success from text that is not supported by metrics.
- Retrieval mismatch: a portfolio lesson can distract a signal-only patch.

## Minimum Operating Rule

After every controller or evaluator batch, write one compact memory update:

```text
what succeeded
what failed
what invariant was learned
which future prompt or filter should use the lesson
which artifact proves it
```

Then retrieve only the relevant active lessons for the next prompt.

## Related Notes

- [[ReasoningBank - Scaling Agent Self-Evolving with Reasoning Memory]]
- [[Dr RTL - Autonomous Agentic RTL Optimization through Tool-Grounded Self-Improvement]]
- [[Group-Relative Skill Learning for Alpha Search]]
- [[AlphaEvolve Lite Quant Search Workflow]]
- [Phase 4 reasoning memory design](../../projects/quant_research_system/phase4_search_loop/reasoning_memory_layer_design.md)
