---
title: LLM Knowledge Base Workflow
type: system
status: seeded
updated: 2026-04-18
tags:
  - system
  - llm
  - obsidian
  - workflow
source_count: 5
sources:
  - "[[raw/LLM Knowledge Bases/Thread by @karpathy.md]]"
  - "[[raw/LLM Knowledge Bases/llm-wiki.md]]"
  - "[[raw/LLM Knowledge Bases/LLM Knowledge Base Definition, Components, and Enterprise Use.md]]"
  - "[[raw/LLM Knowledge Bases/st3v3nmwobsidian-spaced-repetition Fight the forgetting curve by reviewing flashcards & entire notes on Obsidian.md]]"
  - "[[raw/Obsidian/Obsidian_README.md]]"
---
# LLM Knowledge Base Workflow

## Summary

The core workflow is:

1. collect immutable sources in `raw/`
2. let the LLM compile and maintain linked notes in `wiki/`
3. use a schema file to govern ingest, query, lint, and crystallization behavior
4. browse and review everything in Obsidian
5. file useful outputs back into the vault so knowledge compounds

## Core Layers

### Raw Sources

Original papers, books, clipped articles, images, and data descriptions. They are read, not rewritten.

### Compiled Wiki

Persistent markdown notes that summarize, connect, and refine what the source layer contains.

### Schema

An operating file such as `agent.md` or `AGENTS.md` that tells the LLM how to organize the wiki and how to behave when ingesting, answering, or linting.

## Core Operations

### Ingest

Read a source, extract reusable concepts, update related pages, and log the change.

### Ingest Depth Rule

For this vault, ingest depth is part of quality control:

- books and textbooks should be processed chapter by chapter
- long markdown essays, guides, and thread captures should be processed section by section
- the agent should read, understand, reflect, and only then update the wiki
- shallow whole-source summaries are not enough for core quant materials

### Query

Answer from the compiled wiki first, then drill into supporting notes or raw sources as needed.

### Lint

Search for contradictions, stale claims, missing links, unsupported assertions, and new candidate pages.

### Crystallize

Turn useful outputs or project findings into durable pages instead of letting them disappear into chat history.

## Obsidian's Role

Obsidian is the local frontend, not the intelligence layer. In this workflow it is useful for:

- browsing raw files and compiled notes side by side
- following backlinks and graph structure
- rendering Dataview tables
- managing templates and task lists
- optionally using plugins such as spaced repetition for deliberate study

## Enterprise Contrast

Karpathy's workflow assumes a curated, small-to-medium personal wiki. The Atlan guide adds the enterprise warning: once data is large, multi-owner, and access-controlled, governance and metadata quality become as important as retrieval. That matters here because this vault has a remote warehouse behind the local notes.

## Implications for This Vault

This quant vault extends the basic pattern in three domain-specific ways:

- `catalog/` mirrors dataset descriptions and small samples from the remote Linux warehouse
- `artifacts/` stores bounded evidence for numerical claims
- quantitative conclusions must keep conceptual synthesis separate from measured results
- important raw resources should leave behind chapter-level or section-level source notes rather than only top-level summaries

## Related Notes

- [[Karpathy LLM Knowledge Bases Thread]]
- [[LLM Wiki Gist]]
- [[Atlan LLM Knowledge Base Guide]]
- [[Obsidian Spaced Repetition Plugin]]
- [[Obsidian CLI README]]
- [[Panel Data]]

## Sources

- [[raw/LLM Knowledge Bases/Thread by @karpathy.md]]
- [[raw/LLM Knowledge Bases/llm-wiki.md]]
- [[raw/LLM Knowledge Bases/LLM Knowledge Base Definition, Components, and Enterprise Use.md]]
- [[raw/LLM Knowledge Bases/st3v3nmwobsidian-spaced-repetition Fight the forgetting curve by reviewing flashcards & entire notes on Obsidian.md]]

## Links, Bases, and Tags

For this vault, three Obsidian capabilities matter more than most plugin or UI details:

- `Links` are the primary knowledge structure. Durable notes should connect through wikilinks so the graph, backlinks, and source-to-synthesis path stay legible.
- `Bases` are the primary operational view layer. They should summarize notes that already have stable frontmatter, not replace markdown as the source of truth.
- `Tags` are secondary facets. They are useful for filtering and maintenance views, but they should not replace links, folders, or note titles.

## CLI and MCP Implication

When the Obsidian automation surface is available, note-local operations should prefer it over generic filesystem treatment. That is especially useful for searching, backlink-oriented linting, note appends, periodic-note workflows, and future Base-driven maintenance views.
