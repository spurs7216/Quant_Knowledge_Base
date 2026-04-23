---
title: LLM Knowledge Base Workflow
type: system
status: active
updated: 2026-04-22
tags:
  - system
  - llm
  - obsidian
  - workflow
source_count: 6
sources:
  - "[[raw/LLM Knowledge Bases/Thread by @karpathy.md]]"
  - "[[raw/LLM Knowledge Bases/llm-wiki.md]]"
  - "[[raw/LLM Knowledge Bases/LLM Wiki v2 — extending Karpathy's LLM Wiki pattern with lessons from building agentmemory.md]]"
  - "[[raw/LLM Knowledge Bases/LLM Knowledge Base Definition, Components, and Enterprise Use.md]]"
  - "[[raw/LLM Knowledge Bases/st3v3nmwobsidian-spaced-repetition Fight the forgetting curve by reviewing flashcards & entire notes on Obsidian.md]]"
  - "[[raw/Obsidian/Obsidian_README.md]]"
---
# LLM Knowledge Base Workflow

## Summary

The vault follows Karpathy's basic pattern, but now with a clearer lifecycle doctrine:

1. collect immutable sources in `raw/`
2. keep active uncertain synthesis in `projects/`
3. compile durable semantic and procedural notes into `wiki/`
4. support numerical or operational claims with `catalog/` and `artifacts/`
5. use Obsidian as the frontend and QMD or exact search as retrieval tools
6. treat schema and governance as first-class parts of the system

## Core layers

### Source memory

`raw/` stores the original books, papers, clipped guides, images, and source captures.

### Working or episodic memory

`projects/` stores live research threads, session digests, temporary synthesis, and uncertain conclusions that are not yet ready to become durable memory.

### Semantic and procedural memory

`wiki/` stores the durable concepts, methods, maps, and source digests that should remain useful across sessions.

### Evidence and observability memory

`catalog/` and `artifacts/` store mirrored data understanding, diagnostics, charts, query outputs, and other bounded evidence that supports quantitative claims.

## Core operations

### Ingest

Read the source, classify it, build honest coverage, deepen what matters, promote the reusable layer, and update the control notes.

### Query

Answer from the compiled layer first, then escalate only when the cheaper support is insufficient:

- known path or exact phrase -> direct read or exact search
- note-local reading or edits -> Obsidian
- broad or fuzzy discovery -> QMD
- source verification or ingest -> `raw/` and PDF tooling

### Lint

Look for contradictions, stale notes, unsupported claims, broken links, missing promotion targets, and notes whose declared depth no longer matches their content.

### Crystallize

Treat useful project outcomes and high-value query outputs as candidate sources for the durable layer instead of letting them disappear into chat history.

## What v2 adds that we should adopt

### 1. Lifecycle discipline

The v2 guide is right that not all knowledge should be treated as equally mature. For this vault, the right implementation is folder-level and workflow-level, not per-fact pseudo-math.

That means:

- fresh observations stay in `projects/`
- stable reusable syntheses move to `wiki/`
- measured support stays tied to `catalog/` or `artifacts/`

### 2. Explicit supersession

Karpathy's original pattern says to note contradictions. The v2 guide improves this by pushing for explicit replacement logic.

For this vault, that means:

- use `last_verified`, `verification_status`, `supersedes`, and `superseded_by` when freshness or contradiction matters
- do not quietly rewrite older notes so they still look current by omission

### 3. Light graph structure

The v2 guide is right that pages plus generic links leave structure on the table.

For this vault, the right upgrade is not a separate graph database. It is:

- stable note types
- explicit source links
- optional typed relation fields such as `depends_on`, `used_by`, and `contradicts` when the relation is load-bearing
- clearer relation prose inside notes

### 4. Trigger-based maintenance

We do not need full event infrastructure yet, but the system should behave as if certain events imply maintenance work:

- new source -> shelf and ingest review
- contradiction -> supersession review
- durable project result -> crystallization
- periodic maintenance -> lint and stale review

### 5. Redaction and governance

The v2 guide is right that knowledge-base systems need a secret-filtering doctrine. This matters even in a personal vault because clipped sources, interview prep, and operational notes can carry sensitive data.

## What v2 suggests that we should not adopt directly

### Numeric confidence scores on facts

I do not think this vault should assign fake decimal confidence values like `0.85` to ordinary markdown claims. That creates false precision and maintenance overhead without improving inspectability.

The better substitute is:

- explicit provenance
- explicit verification state
- explicit caveats
- explicit contradiction and supersession links

### Forgetting inside `wiki/`

The v2 guide's retention curve makes sense for memory engines, but this vault is an inspectable research archive. Durable knowledge should not silently fade because it was not recently accessed.

The better rule here is:

- archive or deprioritize scratch material
- verify or supersede durable notes
- do not simulate forgetting in the durable layer

### Full event-driven automation

Useful long term, but premature now. The current system benefits more from better written trigger rules than from a half-built automation layer.

## Implications for this vault

The whole system is now better described as:

- Karpathy's compiled-wiki core
- Atlan's governance warning about freshness and provenance
- the v2 guide's lifecycle and supersession logic
- quant-specific separation between conceptual truth and numerical truth

That combination is stronger than any one source alone.

## Related notes

- [[Karpathy LLM Knowledge Bases Thread]]
- [[LLM Wiki Gist]]
- [[LLM Wiki v2 Guide]]
- [[Atlan LLM Knowledge Base Guide]]
- [[Obsidian Spaced Repetition Plugin]]
- [[Obsidian CLI README]]

## Sources

- [[raw/LLM Knowledge Bases/Thread by @karpathy.md]]
- [[raw/LLM Knowledge Bases/llm-wiki.md]]
- [[raw/LLM Knowledge Bases/LLM Wiki v2 — extending Karpathy's LLM Wiki pattern with lessons from building agentmemory.md]]
- [[raw/LLM Knowledge Bases/LLM Knowledge Base Definition, Components, and Enterprise Use.md]]
- [[raw/LLM Knowledge Bases/st3v3nmwobsidian-spaced-repetition Fight the forgetting curve by reviewing flashcards & entire notes on Obsidian.md]]
- [[raw/Obsidian/Obsidian_README.md]]
