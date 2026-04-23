---
title: Arbitrage Theory in Continuous Time - Ch 31 Minimizing f-Divergence
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - incomplete-markets
  - divergence
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: toc_scan_plus_utf8_text_extraction_and_targeted_rendered_theorem_pages
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 31 Minimizing f-Divergence
parent_source: "[[Arbitrage Theory in Continuous Time]]"
sources:
  - "[[Arbitrage Theory in Continuous Time]]"
  - "[[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]"
---
# Arbitrage Theory in Continuous Time - Ch 31 Minimizing f-Divergence

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: theorem-level extraction completed for reverse entropy, minimal entropy, and the duality link between divergence minimization and utility maximization.

## Deepening Targets

- If later work needs a stronger convex-duality connection, deepen the conjugate-function machinery alongside Appendix D.

## Deepened Subparts

- `31.1` definition and basic properties
- `31.2` minimal reverse entropy
- `31.3` minimal entropy in a factor model
- `31.4` duality

## Role of the chapter

This chapter broadens measure selection from one named construction to an optimization class over martingale measures.

## Core mathematical objects

- $f$-divergence
- reverse entropy and entropy
- martingale-measure constraint
- convex duality with utility maximization

## Structural map of the chapter

- define divergence-based measure selection
- solve the reverse-entropy case
- study minimal entropy in a factor model
- connect the problem to utility maximization by duality

## Theorem and derivation spine

### Reverse entropy reproduces the minimal martingale measure

The chapter states explicitly that the minimal reverse-entropy measure coincides with the minimal martingale measure. That is the first important bridge between seemingly different measure-selection principles.

### Utility and divergence are dual problems

The later section shows that choosing a martingale measure by minimizing a divergence is closely tied to optimizing utility over terminal wealth or derivative positions. This is the conceptual bridge into indifference pricing.

## Failure modes and misuse points

- treating entropy or divergence criteria as if they were purely statistical rather than financially constrained
- forgetting that the optimization is over martingale measures, not arbitrary distributions
- using a divergence criterion without considering the investor or market interpretation it implies

## Quant research relevance

This chapter is important because it connects pricing, optimization, and information geometry in incomplete markets.

## What should be promoted out of this source note

- [[Esscher Transform and Minimal Martingale Measure]]
- [[Utility Indifference Pricing]]

## Related notes

- [[Esscher Transform and Minimal Martingale Measure]]
- [[Utility Indifference Pricing]]
- [[Martingale Methods for Portfolio Optimization]]

## Sources

- [[Arbitrage Theory in Continuous Time]]
- [[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]

