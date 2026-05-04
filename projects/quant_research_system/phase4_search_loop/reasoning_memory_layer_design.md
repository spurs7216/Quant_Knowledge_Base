---
title: Phase 4 Reasoning Memory Layer Design
type: project
status: active
updated: 2026-05-04
tags:
  - project
  - phase4
  - alphaevolve
  - reasoningbank
  - memory-layer
sources:
  - "../../../raw/Alpha_evolve/ReasoningBank - Scaling Agent Self-Evolving with Reasoning Memory.pdf"
  - "https://github.com/google-research/reasoning-bank"
  - "https://raw.githubusercontent.com/google-research/reasoning-bank/main/WebArena/memory_management.py"
  - "https://raw.githubusercontent.com/google-research/reasoning-bank/main/WebArena/prompts/memory_instruction.py"
  - "current_state.md"
  - "program_database_schema.md"
  - "prompt_contracts.md"
  - "artifact_renderer_contract.md"
  - "diagnostic_analyzer_and_skill_library_20260504.md"
---
# Phase 4 Reasoning Memory Layer Design

## Decision

Phase 4 should add a ReasoningBank-style memory layer before the next planned child-evaluation milestone.

The current project already keeps informal lessons in [current_state.md](current_state.md). That is useful for humans, but it is not enough for an AlphaEvolve loop. The controller needs a structured layer that can be updated after each proposing/evaluating round and retrieved by the prompt sampler.

## What ReasoningBank Adds

ReasoningBank contributes four design principles:

1. Store distilled reasoning lessons, not raw trajectories.
2. Learn from both successful and failed attempts.
3. Retrieve only relevant memory items for the current task.
4. Use multiple trajectories or refinement steps to extract better contrastive memory.

The paper's implementation is intentionally simple: memory items contain title, description, and content; extraction uses different prompts for success and failure; consolidation appends new items; retrieval embeds the current query and returns top relevant memories.

For our system, the transferable mechanism is not the exact WebArena setup. It is the conversion:

```text
evaluated episode -> supported lesson -> compact memory card -> future prompt context
```

## Difference From Program Database

The program database is exhaustive search memory. It stores every generated child, prompt, diff, code hash, metrics, descriptors, gates, and artifact paths.

The reasoning memory bank is prompt-facing operating memory. It stores only the lessons worth reusing.

The explicit skill library is a narrower derived layer. It stores pattern -> strategy rules with confidence, status, applicability, and evidence. Reasoning memory can hold broad lessons; the skill library should hold only operational rules that are safe to inject as prompt instructions.

They should be linked but not merged:

```text
program_database / artifacts
  -> episode packet
  -> memory extraction
  -> reasoning_memory_items
  -> skill candidates when the lesson is a reusable pattern -> strategy rule
  -> prompt sampler
```

## Adapted Memory Item Schema

Recommended Phase 4 item:

```yaml
memory_item_id: "mem_..."
source_run_id: "controller_batch_001_small_semantic_v3"
source_program_ids: []
source_attempt_ids: []
source_stage: controller_static | toy_eval | remote_sample_eval | validation
source_outcome: success | failure | mixed
memory_type: success_strategy | failure_guardrail | repair_pattern | evaluator_caveat | data_contract | model_routing
title: short label
description: when this applies
content: concrete instruction for future prompts or filters
applicability:
  data_stage: stage_0_daily_stock
  target_surface: signal | ranking | portfolio | neutralization | patch_contract | routing
  island: daily_stock_signal | portfolio_risk_turnover | repair_near_miss | negative_control
  map_cell: optional MAP-Elites behavior cell
evidence:
  hard_gates: {}
  metrics: {}
  failure_categories: []
  artifact_paths: []
retrieval_text: title + description + content + tags
status: candidate | active | superseded | rejected
created_at: timestamp
```

The first implementation can store this as JSONL under:

```text
artifacts/phase4_alphaevolve/reasoning_memory/memory_items.jsonl
artifacts/phase4_alphaevolve/reasoning_memory/memory_updates.jsonl
```

Embeddings can be added later on the remote server. The local machine should not require Qwen or embedding inference.

## Extraction Workflow

Use deterministic evidence first:

1. Build an episode packet from batch summaries, attempt files, evaluator summaries, failure categories, DB rows, and artifact paths.
2. Label each item from controller/evaluator evidence, not from LLM opinion.
3. Ask Qwen on the remote server to extract candidate memories only after the evidence packet is built.
4. Use success, failure, repaired, and self-contrast prompts depending on the packet.
5. Reject candidates that are unsupported, too specific, duplicated, or inconsistent with frozen contracts.
6. Append accepted active items to the memory bank.
7. Retrieve stage/surface-specific active items for the next prompt.

This keeps the LLM in the synthesis role, while deterministic gates decide whether a memory item is supported.

## Self-Contrast For Child Batches

The most useful Phase 4 extraction mode is batch self-contrast.

A small controller batch usually contains accepted children, repaired children, duplicates, semantic rejects, vector-smoke failures, and empty-output failures. Comparing these together gives stronger lessons than explaining each child alone.

Example self-contrast questions:

- Which patch shapes passed all controller-static gates?
- Which failures were caused by prompt format rather than strategy logic?
- Which portfolio formulas preserved signs but broke net exposure?
- Which duplicate patterns suggest the model is stuck in one search cell?
- Which lessons should become prompt instructions versus deterministic filters?

Dr. RTL strengthens this rule: compare siblings generated from the same parent under the same evaluator context before extracting skills. The implementation now writes a `group_relative_controller_report` into each controller batch's `reasoning_memory_update.json` / `.md`.

Dr. RTL also requires a diagnostic agent before optimization. The Phase 4 implementation now writes deterministic diagnostic reports:

```text
evaluator_diagnostic_report.json/.md
controller_diagnostic_report.json/.md
```

These reports localize bottlenecks such as cost fragility, high turnover, sign-flip dominance, duplicate generation, portfolio semantic failures, and reasoning-only empty output. They are analyzer output, not alpha evidence.

## Current Seed Memory From Phase 4

The initial active memory should include these lessons, all already supported by prior artifacts and [current_state.md](current_state.md):

- Full-program prompts invite marker copying and helper edits. Child-generation prompts should expose one target evolve-block body.
- Syntax, compile, and vector smoke are not enough. Long/short portfolio children require semantic checks for sign direction, both-side exposure, gross/net exposure, and max weight.
- Signal-proportional weights must compute positive magnitudes on each side before assigning signed long and short weights.
- Qwen can return reasoning-only responses with null final content. Disable thinking mode in the actual HTTP payload and retry empty final content once.
- Duplicate children should be stored as evidence but should not count as unique controller passes.
- Pandas API mistakes such as `.clip(max=...)` are repairable vector-smoke failures; use `.clip(upper=...)`.

These are memory items, not market-alpha claims.

## Prompt Injection Rule

Prompt sampler should insert memory cards after immutable contracts and before the target evolve-block instructions.

Suggested format:

```text
RELEVANT REASONING MEMORY
- [failure_guardrail | portfolio] Long/short proportional weights:
  Convert each side to positive magnitudes first, then assign signed weights.
  Evidence: controller_batch_001_small_semantic_v2 portfolio semantic reject.
```

Limit insertion to the most relevant active cards. A first cap of three to five items is safer than dumping the memory bank into every prompt.

## Relationship To AlphaEvolve Modules

| AlphaEvolve module | Memory-layer hook |
| --- | --- |
| Prompt sampler | Retrieves active memory by stage, surface, island, MAP cell, and similarity; injects compact cards into child prompts. |
| LLM ensemble | Qwen generates children and, on the remote server only, extracts memory candidates from evidence packets. |
| Evaluator pools | Produce deterministic outcomes and failure categories that support or reject memory candidates. |
| Program database | Supplies lineage and artifact references; memory items point back to programs and runs. |

## Implementation Milestones

### C0 - Documentation And Schema

Done in this note and the durable wiki notes:

- [[ReasoningBank - Scaling Agent Self-Evolving with Reasoning Memory]]
- [[Reasoning Memory for AlphaEvolve Search]]

### C1 - Local Scaffold

Implemented 2026-05-04 in:

- `research/alphaevolve_lite/reasoning_memory.py`
- `research/alphaevolve_lite/prompt_builder.py`
- `research/alphaevolve_lite/scripts/run_child_batch.py`

The lightweight local module can:

- define and validate memory item records;
- append JSONL memory items;
- retrieve active items by stage/surface/island with lexical fallback;
- render compact prompt cards.
- write a deterministic `reasoning_memory_update.json` / `.md` after a controller batch.
- compute a Dr. RTL-style group-relative controller report across sibling attempts.

This does not require local Qwen or embedding inference. `run_child_batch.py` bootstraps the default Phase 4 seed lessons into `artifacts/phase4_alphaevolve/reasoning_memory/memory_items.jsonl` unless reasoning memory is explicitly disabled.

### C1b - Diagnostic Analyzer And Explicit Skill Library

Implemented 2026-05-04 in:

- `research/alphaevolve_lite/diagnostic_analyzer.py`
- `research/alphaevolve_lite/skill_library.py`
- `research/alphaevolve_lite/prompt_builder.py`
- `research/alphaevolve_lite/scripts/run_child_batch.py`

The scaffold now:

- builds evaluator diagnostic cards before generation;
- builds controller diagnostic cards after the batch;
- bootstraps a conservative skill library under `artifacts/phase4_alphaevolve/skill_library/skill_items.jsonl`;
- retrieves stage/surface-specific skill cards into prompts;
- writes `skill_update.json` / `.md` with candidate skills after a batch.

New candidate skills are not auto-promoted to active from one controller batch.

### C2 - Remote Extraction

Add a remote-only script that builds an episode packet from a controller/evaluator batch and calls the Qwen server to propose candidate memory items.

Remote operator instruction: before any extraction call, open a persistent terminal or `tmux` pane, launch vLLM, keep it running, and verify `/health` plus `/v1/models` from a separate terminal.

### C3 - Prompt Sampler Integration

Child-generation and duplicate-retry prompts now inject retrieved memory cards, diagnostic cards, and skill cards filtered by controller stage, data stage, and target evolve surface. Direct repair-prompt injection is still deferred; repair already receives the concrete failure reason and target editable body.

### C4 - Consolidation

Start append-only. Add dedupe and supersession once there are enough items to observe collisions.

## Vague Parts To Resolve

- Whether active memory items require human approval or can become active after deterministic support checks alone.
- Which remote model should extract memory: 9B is cheaper and likely enough for structured extraction, while 27B may be better for self-contrast summaries.
- Whether embeddings should use a local lexical fallback forever or move to remote embedding once the memory bank grows.
- How many memory cards should be injected by default. The initial recommendation is three, with a hard cap of five.
- Whether memory should be stored only as JSONL or mirrored into SQLite next to the program database.
- Which deterministic support threshold should promote candidate skills to active after remote sample-evaluator evidence exists.

## Next Step

Run `controller_batch_001_small_semantic_v4` with memory, diagnostic, and skill cards enabled but without using Qwen extraction locally. After the run, perform C2 remotely and review both `reasoning_memory_update.md` and `skill_update.md` before promoting any new lesson or skill.
