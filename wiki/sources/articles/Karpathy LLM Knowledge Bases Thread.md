---
title: Karpathy LLM Knowledge Bases Thread
type: source
status: section_ingested
updated: 2026-04-18
tags:
  - source
  - llm
  - knowledge-base
  - obsidian
sources:
  - "[[raw/LLM Knowledge Bases/Thread by @karpathy.md]]"
---
# Karpathy LLM Knowledge Bases Thread

## Summary

This thread is the shortest and clearest statement of the workflow that motivated this vault. Karpathy describes a loop where raw sources are collected into `raw/`, an LLM incrementally compiles a markdown wiki, Obsidian acts as the browsing frontend, and later questions or outputs are filed back into the knowledge base instead of being lost in chat history.

## Section-by-Section Ingest

- `Data ingest`: the source layer should be broad enough to include articles, papers, repos, datasets, and images, but the compiled wiki should remain the working synthesis layer.
- `IDE`: Obsidian is not just a note app in this workflow; it is the inspection surface where raw sources, compiled notes, and derived outputs live together.
- `Q&A`: once the wiki is large enough and the index is maintained, the agent can answer multi-document questions from the compiled layer without re-deriving everything from scratch.
- `Output`: answers should become files such as markdown, slides, or plots so they can be reviewed and filed back into the vault.
- `Linting`: the LLM should actively look for contradictions, missing data, and article candidates instead of waiting passively for instructions.
- `Extra tools`: small search or CLI tools become useful only after the wiki exists; they are secondary accelerators, not the starting point.
- `Further explorations`: synthetic data or fine-tuning only becomes interesting after the knowledge base itself is healthy.

## Key Claims

- The LLM should read from an immutable `raw/` source layer and maintain the wiki itself.
- Obsidian can serve as the IDE-like frontend for browsing sources, wiki pages, and generated outputs.
- At moderate scale, an auto-maintained wiki plus index files can often answer complex questions without heavy RAG infrastructure.
- Good outputs should be rendered as files such as markdown, slides, or figures and then filed back into the wiki.
- Periodic linting or "health checks" can improve consistency, fill gaps, and suggest new questions.

## Methods and Data

This is a workflow sketch, not a benchmark study or software package. The thread mentions Karpathy's own research wiki at roughly 100 articles and 400K words, plus practical tooling such as Obsidian Web Clipper, local image downloads, and CLI helpers.

## Why It Matters Here

This vault adopts the same basic doctrine:

- `raw/` for source material
- `wiki/` for LLM-maintained durable notes
- Obsidian as the local frontend
- `artifacts/` for generated outputs that support future work

The main quant-specific extension is that numerical claims also need support from `catalog/` and `artifacts/`, not only conceptual synthesis.

## Reflection

For a quant researcher, the most important lesson in this thread is not "use Obsidian." It is that research should compound. Every source ingest, comparison, and question should improve the persistent knowledge graph rather than disappear into temporary dialogue.

## Caveats

- The thread is intentionally compact and does not define a full schema.
- The scale claims are personal and anecdotal rather than benchmarked.
- It is best read as the motivating pattern, not the finished operating manual.

## Related Notes

- [[LLM Wiki Gist]]
- [[LLM Knowledge Base Workflow]]
- [[Atlan LLM Knowledge Base Guide]]
- [[Obsidian Spaced Repetition Plugin]]

## Sources

- [[raw/LLM Knowledge Bases/Thread by @karpathy.md]]
