---
title: LLM Wiki Gist
type: source
status: section_ingested
updated: 2026-04-18
tags:
  - source
  - llm
  - knowledge-base
  - schema
sources:
  - "[[raw/LLM Knowledge Bases/llm-wiki.md]]"
---
# LLM Wiki Gist

## Summary

This gist expands the original thread into an explicit operating pattern for LLM-maintained knowledge bases. It defines three layers, three core operations, special index and log files, optional search tooling, and a practical view of Obsidian as the interface where humans inspect what the LLM maintains.

## Section-by-Section Ingest

- `The core idea`: the wiki is a persistent compiled artifact, not a retrieval cache rebuilt from raw documents at every question.
- `Architecture`: raw sources, the wiki, and the schema are separate layers with different responsibilities.
- `Operations`: ingest, query, and lint are the recurring maintenance loop; query is not separate from knowledge growth because good answers should be filed back.
- `Indexing and logging`: `index.md` is content-oriented while `log.md` is chronological; both help the agent navigate at moderate scale.
- `Optional CLI tools`: local search and CLI tools are useful as the wiki grows, but they are not the foundation of the method.
- `Tips and tricks`: Obsidian Web Clipper, local attachments, graph view, Marp, Dataview, and git all make the markdown wiki easier to maintain and inspect.
- `Why this works`: the LLM removes the maintenance burden that normally kills personal wikis.
- `Note`: implementation details are intentionally left open and should be adapted by domain.

## Key Claims

- The wiki should be a persistent, compounding artifact rather than a temporary retrieval cache.
- The architecture has three layers: raw sources, the wiki, and a schema file that tells the LLM how to behave.
- The main recurring operations are ingest, query, and lint.
- `index.md` and `log.md` reduce the need for retrieval infrastructure at moderate scale.
- The human curates sources and asks questions; the LLM handles summarizing, cross-linking, and maintenance.

## Methods and Data

This is an idea file meant to be copied into an LLM session and adapted. It is not tied to one vendor or one repo layout. It also includes practical Obsidian guidance such as attachment handling, graph view, Dataview, and git-backed markdown.

## Why It Matters Here

This vault's `AGENTS.md`, `wiki/index.md`, and `wiki/log.md` are direct descendants of the pattern in this gist. The repo differs mainly in one domain-specific respect: the quant workflow needs a separate evidence layer for numeric claims, so `catalog/` and `artifacts/` matter alongside the wiki.

## Reflection

The most useful idea in this gist for quant work is that the schema is a first-class object. Without explicit ingest and maintenance rules, an LLM drifts toward shallow summaries. With a schema, it can become a disciplined research librarian.

## Caveats

- The gist is abstract by design and leaves domain-specific implementation details open.
- It assumes a small or moderate wiki scale before stronger search infrastructure becomes necessary.
- It does not by itself solve governance for very large, access-controlled enterprise data estates.

## Related Notes

- [[Karpathy LLM Knowledge Bases Thread]]
- [[LLM Knowledge Base Workflow]]
- [[Atlan LLM Knowledge Base Guide]]

## Sources

- [[raw/LLM Knowledge Bases/llm-wiki.md]]
