---
title: ReasoningBank - Scaling Agent Self-Evolving with Reasoning Memory
type: source
status: active
read_scope: full_source
technical_depth: method_level
updated: 2026-05-04
tags:
  - source
  - paper
  - llm-agents
  - reasoning-memory
  - test-time-scaling
sources:
  - "../../raw/Alpha_evolve/ReasoningBank - Scaling Agent Self-Evolving with Reasoning Memory.pdf"
  - "https://github.com/google-research/reasoning-bank"
  - "https://raw.githubusercontent.com/google-research/reasoning-bank/main/WebArena/memory_management.py"
  - "https://raw.githubusercontent.com/google-research/reasoning-bank/main/WebArena/prompts/memory_instruction.py"
---
# ReasoningBank - Scaling Agent Self-Evolving with Reasoning Memory

## Summary

ReasoningBank is a memory layer for self-evolving agents. Its central claim is that an agent should not store only raw trajectories or only successful workflows. It should distill both successes and failures into compact reasoning memories that can be retrieved for future tasks.

The reusable memory item is:

```yaml
title: short task-agnostic label
description: when the lesson applies
content: prompt-ready reasoning strategy, guardrail, or corrective heuristic
```

The method has three loops:

1. retrieve relevant memories for the current task;
2. extract new memories from completed trajectories, using different prompts for success and failure;
3. consolidate the new items into the bank.

The paper then adds MaTTS, or Memory-augmented Test-Time Scaling, where multiple trajectories or refinement steps are compared to produce better memory than isolated single-run extraction.

## Why It Matters

AlphaEvolve-style search produces many failed or near-miss programs. A program database stores the evidence, but it is too large and too raw to inject into future prompts directly. ReasoningBank supplies the missing middle layer: concise, evidence-grounded lessons that tell the next generator what patterns worked, what failed, and why.

For quant research, this matters because many failures are reusable:

- malformed patches and evolve-block boundary violations;
- portfolio semantics such as one-sided books or excessive net exposure;
- data-contract mistakes;
- cost, turnover, or concentration evasions;
- repeated duplicate children;
- prompt-routing failures such as reasoning-only model responses.

These are not market-alpha facts. They are operating lessons that should compound across controller iterations.

## Reading Logic

The paper is read as a method paper, not as empirical proof that the exact WebArena or SWE-Bench setup transfers unchanged to quant research. The important transferable object is the memory architecture: what gets stored, how it is extracted, how it is retrieved, and how multi-trajectory evidence improves the memory.

## Section 1 - Introduction

The introduction frames the problem as persistent agent improvement across a stream of tasks. Existing agents can be strong within a single task, but without durable memory they repeat past mistakes. Raw trajectory memory is too verbose and task-specific, while workflow memory often learns mainly from successes.

ReasoningBank proposes to store abstract reasoning strategies and hints extracted from prior experience. A failure is useful because it exposes pitfalls and counterfactual reasoning that a success-only memory misses.

The introduction also connects memory to test-time scaling. Extra samples or refinement steps are not valuable only because they might solve the current task; they also create contrastive evidence for future tasks.

## Section 2 - Related Work

The related-work section positions ReasoningBank among LLM agents, external memory, self-evolving systems, and test-time scaling.

The main distinction is content granularity. ReasoningBank does not treat memory as a dump of full trajectories. It turns trajectories into compact reasoning items. It also does not treat failures as disposable. Failed traces become guardrails when the failure mode is general enough.

This is important for an AlphaEvolve-like loop because many bad children are still informative. A rejected patch can teach a future prompt sampler that certain transformations violate a contract even if the program compiles.

## Section 3 - Methodology

The method defines a continual task setting. At task step \(i\), the agent receives the current task and an external memory bank, acts in an environment, obtains a trajectory and outcome, then updates memory for later tasks.

### ReasoningBank

ReasoningBank has three operations.

Retrieval embeds the current task query, compares it against stored memory-item embeddings, and injects the top relevant memory into the agent instruction. The paper's implementation keeps this intentionally simple: cosine similarity over embeddings, top-k retrieval, and direct prompt insertion.

Extraction turns a completed trajectory into structured memory. The paper uses an LLM judge to classify the trajectory as success or failure, then applies different extraction instructions. Successful trajectories produce validated strategies. Failed trajectories produce pitfalls, corrections, and guardrails.

Consolidation appends the extracted memory items to the bank. The paper does not focus on advanced pruning, clustering, or hierarchical memory. The initial system is deliberately simple and append-only.

### MaTTS

MaTTS improves memory by using more than one trajectory signal.

Parallel scaling samples multiple trajectories for the same task under the same memory state. A self-contrast extractor compares successful and failed trajectories and looks for stable differences. This can identify robust strategies and reject spurious details.

Sequential scaling refines or rechecks a trajectory through multiple intermediate steps. Those intermediate notes create additional memory signals.

The key idea is that additional test-time compute should improve future memory, not only current-task success.

## Section 4 - Experiments

The experiments evaluate ReasoningBank on web browsing, web task execution, and software engineering environments, including WebArena, Mind2Web, and SWE-Bench-style settings.

The reported pattern is consistent across tasks: distilled reasoning memory improves success rate and often reduces interaction steps compared with baselines that use no memory, raw trajectory memory, or success-only workflow memory.

The experiments also test smaller and open-source backbones. The paper's useful transfer claim for this project is not that a specific model is mandatory, but that memory distillation helps lower-latency models use prior experience more effectively.

## Section 5 - Analysis

The analysis section is the most important part for Phase 4 design.

First, failure-derived memory matters. The paper shows that adding failed trajectories can help ReasoningBank, while some success-only memory baselines are weaker or can degrade when failures are included naively. This supports a separate failure-memory path rather than dumping all bad traces into prompts.

Second, the memory items are more reusable than raw traces because they identify the reasoning step, not the environment transcript. A good memory says what principle to apply, when it applies, and what trap it avoids.

Third, MaTTS and ReasoningBank reinforce each other. Multiple rollouts give better contrastive evidence; better memory improves later rollouts.

For our search controller, this maps directly to sibling child batches. A batch with accepted children, semantic rejects, duplicate rejects, and repair successes is a richer memory source than a single child.

## Section 6 - Conclusion

The conclusion presents reasoning memory as a general mechanism for self-improving agents. The main engineering lesson is modest but powerful: store the useful reasoning lesson, not the entire trace, and update the memory after every interaction.

## Appendices And Implementation Details

The appendix gives the concrete implementation constraints that matter for our system:

- a memory item has title, description, and content;
- the extractor can emit multiple items, with the paper using a small cap per trajectory;
- success and failure extraction use different prompts;
- a classifier or judge decides whether the trajectory is successful before extraction;
- retrieval uses embeddings and cosine similarity, with a small top-k inserted into the prompt;
- memory storage is JSON-like and append-oriented;
- self-contrast extraction can produce a small set of stronger items from multiple trajectories.

The limitation section explicitly says the paper is about memory content more than sophisticated memory architecture. That leaves room for project-specific additions such as deterministic labels, schema filters, supersession, and stage-aware retrieval.

## GitHub Implementation Notes

The official repository is `google-research/reasoning-bank`. The WebArena implementation exposes the practical shape of the system.

`WebArena/memory_management.py` defines a `MemoryManagement` class with three main behaviors:

- `extract_memory`: reads task/result trajectories, determines success or failure, and calls an LLM with the corresponding memory-extraction instruction;
- `retrieve_memory`: embeds the current task intent, compares it with stored memory embeddings, and returns the most similar memory;
- `compute_embeddings`: computes and stores embeddings for existing memory records.

The implementation stores memory records in line-oriented JSON-like files and keeps a separate embeddings file. The prompts in `WebArena/prompts/memory_instruction.py` use the same structured memory item fields described in the paper.

This code is intentionally simple. It validates the method's architecture more than it provides a production-grade memory database.

## Strengths

- Converts failed attempts into reusable guardrails.
- Keeps prompt memory compact compared with raw trajectory replay.
- Separates evidence storage from prompt-facing lessons.
- Works with parallel rollouts through self-contrast.
- Can help smaller or faster models because it reduces the amount of rediscovery needed.

## Caveats

- LLM-as-a-judge can be noisy. In quant research, deterministic evaluator labels should be primary whenever available.
- Append-only memory can accumulate duplicates or stale lessons.
- Retrieval can return irrelevant memory unless it is filtered by stage, target surface, dataset, and strategy family.
- A memory item can overfit one run if it records incidental details instead of a general principle.
- Bad memory is dangerous because it can bias many future children.

## Quant Research Translation

For AlphaEvolve-lite quant search, ReasoningBank should become a separate memory layer between the program database and the prompt sampler.

The program database stores exhaustive evidence: every prompt, patch, child hash, evaluation result, metric, gate, and artifact path. The reasoning memory bank stores distilled lessons: what to try, what to avoid, and what invariant must be respected.

The strongest adaptation is to replace the paper's pure LLM success judge with deterministic evaluator outcomes:

```text
controller/evaluator result -> deterministic label -> LLM distills candidate memory -> deterministic support/dedup filter -> memory bank
```

This preserves the ReasoningBank loop while respecting the higher standard needed for trading research.

## Related Notes

- [[Reasoning Memory for AlphaEvolve Search]]
- [[AlphaEvolve Lite Quant Search Workflow]]
- [[AlphaEvolve - A coding agent for scientific and algorithmic discovery]]
- [Phase 4 reasoning memory design](../../../projects/quant_research_system/phase4_search_loop/reasoning_memory_layer_design.md)
