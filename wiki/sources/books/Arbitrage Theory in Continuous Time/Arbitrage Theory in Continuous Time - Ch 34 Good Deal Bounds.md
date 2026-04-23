---
title: Arbitrage Theory in Continuous Time - Ch 34 Good Deal Bounds
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - incomplete-markets
  - valuation-bounds
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: toc_scan_plus_utf8_text_extraction
technical_depth: selective_deepen
ingest_stage: selective_deepen
chapter_or_section: Ch 34 Good Deal Bounds
parent_source: "[[Arbitrage Theory in Continuous Time]]"
sources:
  - "[[Arbitrage Theory in Continuous Time]]"
  - "[[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]"
---
# Arbitrage Theory in Continuous Time - Ch 34 Good Deal Bounds

## Ingest Scope and Depth

- Ingest stage: `selective_deepen`
- Pass 1: full chapter scan completed.
- Pass 2: selective deepening focused on the optimization problem that narrows arbitrage-free price intervals by excluding implausibly attractive deals.

## Deepening Targets

- Later work could deepen the relation to Sharpe-ratio constraints, robust pricing, and basis-risk applications.

## Deepened Subparts

- `34.3` the good deal bounds
- `34.4` the embedded optimization problem
- `34.5` relations to the minimal martingale measure

## Role of the chapter

This chapter sits between pure no-arbitrage intervals and preference-based prices. It narrows the admissible set by excluding deals that are too good to be plausible.

## Core mathematical objects

- admissible martingale-measure set under extra performance restrictions
- lower and upper good-deal bounds
- basis-risk example

## Structural map of the chapter

- set up the model
- define the good-deal constraint
- solve the embedded optimization problem
- compare the result to minimal-martingale pricing

## Theorem and derivation spine

The main durable point is methodological:

- good-deal bounds are not arbitrage prices
- they are constrained-price intervals built by imposing an extra economic acceptability filter on the martingale-measure set

## Failure modes and misuse points

- confusing good-deal bounds with no-arbitrage theorems
- forgetting that the extra bound depends on a chosen notion of "too good"

## Quant research relevance

This chapter is useful when pure arbitrage intervals are too wide but one still wants something weaker than a full utility-based price.

## What should be promoted out of this source note

- [[Good Deal Bounds]]

## Related notes

- [[Good Deal Bounds]]
- [[Utility Indifference Pricing]]
- [[Esscher Transform and Minimal Martingale Measure]]

## Sources

- [[Arbitrage Theory in Continuous Time]]
- [[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]

