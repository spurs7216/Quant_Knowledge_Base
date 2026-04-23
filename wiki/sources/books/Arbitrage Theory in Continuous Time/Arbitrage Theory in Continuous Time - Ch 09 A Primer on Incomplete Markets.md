---
title: Arbitrage Theory in Continuous Time - Ch 09 A Primer on Incomplete Markets
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - mathematical-finance
  - incomplete-markets
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: toc_scan_plus_utf8_text_extraction
technical_depth: selective_deepen
ingest_stage: selective_deepen
chapter_or_section: Ch 09 A Primer on Incomplete Markets
parent_source: "[[Arbitrage Theory in Continuous Time]]"
sources:
  - "[[Arbitrage Theory in Continuous Time]]"
  - "[[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]"
---
# Arbitrage Theory in Continuous Time - Ch 09 A Primer on Incomplete Markets

## Ingest Scope and Depth

- Ingest stage: `selective_deepen`
- Pass 1: full chapter scan completed.
- Pass 2: selective deepening focused on the nonpriced-factor example and the shift from unique prices to price intervals.

## Deepening Targets

- Later incompleteness chapters carry the deeper theory, so this note mainly preserves the first model-level intuition.

## Deepened Subparts

- `9.2` a scalar non-priced underlying asset

## Role of the chapter

This chapter is the first clean warning that replication logic is fragile. Add one source of risk that is not spanned by traded assets and unique pricing breaks.

## Core mathematical objects

- traded stock risk
- nontraded factor risk
- family of equivalent martingale measures
- arbitrage-free price interval rather than unique price

## Structural map of the chapter

- introduce a nonspanned factor
- show that no-arbitrage can still hold
- show that claims depending on the hidden factor are not uniquely priced

## Theorem and derivation spine

The chapter's main result is structural rather than formula-heavy:

- incompleteness means there are many admissible pricing measures
- replication no longer pins down one unique value for every claim

This chapter is intentionally simple so the later incomplete-market chapters can work at a higher level without losing intuition.

## Failure modes and misuse points

- saying "risk-neutral price" as if it were unique in every model
- importing complete-market intuition into unspanned-factor models
- ignoring which risks are actually tradable

## Quant research relevance

This chapter is the bridge from textbook Black-Scholes intuition to realistic pricing situations with basis risk, stochastic volatility, credit frictions, and preference-based pricing.

## What should be promoted out of this source note

- support [[Market Completeness and Incomplete Markets]]

## Related notes

- [[Market Completeness and Incomplete Markets]]
- [[Arbitrage Theory in Continuous Time - Ch 08 Completeness and Hedging]]
- [[Arbitrage Theory in Continuous Time - Ch 29 Incomplete Markets]]

## Sources

- [[Arbitrage Theory in Continuous Time]]
- [[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]

