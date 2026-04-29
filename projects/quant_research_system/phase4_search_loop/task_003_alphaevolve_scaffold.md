---
title: Phase 4 Task 003 AlphaEvolve Scaffold
type: project
status: active
updated: 2026-04-27
tags:
  - project
  - phase4
  - alphaevolve
  - scaffold
sources:
  - "alphaevolve_method_translation.md"
  - "program_database_schema.md"
  - "prompt_contracts.md"
---
# Phase 4 Task 003 AlphaEvolve Scaffold

## Objective

Build the minimal local scaffold needed before Phase 4 can honestly claim to mimic AlphaEvolve.

This task does not ask an LLM to propose strategy changes yet. It builds the mechanics that make later proposal generation controllable.

## Required Local Modules

```text
research/alphaevolve_lite/evolve_blocks.py
research/alphaevolve_lite/diff_blocks.py
research/alphaevolve_lite/program_database.py
research/alphaevolve_lite/prompt_cards.py
research/alphaevolve_lite/evaluator_summary.py
```

## Required Mechanics

- discover evolve blocks;
- parse SEARCH/REPLACE diffs;
- apply exact SEARCH/REPLACE diffs;
- reject oversized SEARCH blocks when not allowed;
- create SQLite database and tables;
- append JSONL audit events;
- insert generation-zero seed records;
- sample parent and inspiration records;
- render prompt-cards from evaluator summaries.

## Intended Flow

```text
seed_program = read_program()
evolve_blocks = find_evolve_blocks(seed_program)
database.insert_seed(seed_program)
parent, inspirations = database.sample()
prompt = build_prompt(parent, inspirations)
diff = llm_or_human_proposal()
child_program = apply_search_replace(parent.program_text, diff)
local_preflight(child_program)
database.append(child_program, metrics, descriptors)
```

Task 003 can be completed without any LLM API.

## Acceptance Checks

- Python compilation passes for the scaffold modules;
- a local smoke test detects evolve blocks;
- a valid SEARCH/REPLACE diff applies;
- an oversized SEARCH block is rejected;
- a seed record inserts into SQLite;
- an audit event appends to JSONL;
- database sampling returns parent and inspiration records;
- prompt-card rendering works from a dummy evaluator summary.

## Next Task

Task 004 implements Task 001 using this scaffold.
