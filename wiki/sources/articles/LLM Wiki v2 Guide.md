---
title: LLM Wiki v2 Guide
type: source
status: section_ingested
updated: 2026-04-22
tags:
  - source
  - llm
  - knowledge-base
  - memory-lifecycle
  - governance
sources:
  - "[[raw/LLM Knowledge Bases/LLM Wiki v2 — extending Karpathy's LLM Wiki pattern with lessons from building agentmemory.md]]"
---
# LLM Wiki v2 Guide

## Summary

This guide extends Karpathy's wiki pattern with lifecycle management, knowledge-graph structure, hybrid search, automation triggers, quality control, collaboration, and auditability. Its strongest contribution is not the graph language by itself. It is the claim that a wiki needs explicit memory-management rules or it will rot.

## Section-by-Section Ingest

- `The missing layer: memory lifecycle`: argues that knowledge should not be treated as equally valid forever; confidence, supersession, retention, and consolidation tiers should exist.
- `Beyond flat pages: the knowledge graph`: pushes entity extraction and typed relationships as a layer on top of prose pages.
- `Search that actually scales`: argues that `index.md` eventually becomes too large and that hybrid BM25, vector, and graph retrieval should take over.
- `Automation: from manual to event-driven`: reframes ingest, session compression, contradiction checks, and filing as triggerable maintenance work.
- `Quality and self-correction`: recommends quality scoring, self-healing lint, and contradiction resolution instead of passive flagging only.
- `Multi-agent and collaboration`: adds shared/private scope and light work coordination for multi-agent settings.
- `Security`: argues for redaction, audit trails, and governed bulk operations.
- `Crystallization`: emphasizes that completed research or debugging threads should be ingested back as first-class knowledge sources.
- `Schema is the real product`: makes the schema document the main durable operating asset.

## Key Claims

- Persistent wiki systems need lifecycle management, not only ingest, query, and lint.
- Supersession should be explicit when new knowledge replaces old knowledge.
- Typed relationships and graph-aware retrieval improve discovery once the wiki grows.
- Maintenance should become increasingly trigger-driven rather than entirely manual.
- Quality control and auditability are part of trust, not optional extras.

## Methods and Data

This is still an idea guide, not a benchmark or software spec. It extends the Karpathy pattern with lessons framed as operational architecture from a persistent-memory engine.

## Why It Matters Here

The guide is useful because it highlights what our vault already does well and what it still lacked:

- we already had Karpathy's raw or wiki or schema split
- we already had quant-specific evidence separation
- we did not yet formalize lifecycle, explicit supersession, trigger rules, or redaction guidance clearly enough

## Reflection

The guide is strongest when it warns against flat memory. It is weaker when it implies that all of this should become a fully quantified memory engine. For this vault, numeric confidence scores and forgetting inside `wiki/` would be false precision. Explicit provenance, verification state, and supersession are better fits.

## Caveats

- The guide is ambitious and somewhat production-memory-engine flavored; not every suggestion should be copied into a markdown vault.
- Some ideas are clearly more useful at team or multi-agent scale than in a single-user research vault.
- It needs adaptation by domain, especially in math-heavy or evidence-heavy research systems.

## Related Notes

- [[Karpathy LLM Knowledge Bases Thread]]
- [[LLM Wiki Gist]]
- [[LLM Knowledge Base Workflow]]
- [[Atlan LLM Knowledge Base Guide]]

## Sources

- [[raw/LLM Knowledge Bases/LLM Wiki v2 — extending Karpathy's LLM Wiki pattern with lessons from building agentmemory.md]]
