---
title: Arbitrage Theory in Continuous Time - Ch 32 Portfolio Optimization in Incomplete Markets
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - incomplete-markets
  - portfolio-choice
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: toc_scan_plus_utf8_text_extraction
technical_depth: selective_deepen
ingest_stage: selective_deepen
chapter_or_section: Ch 32 Portfolio Optimization in Incomplete Markets
parent_source: "[[Arbitrage Theory in Continuous Time]]"
sources:
  - "[[Arbitrage Theory in Continuous Time]]"
  - "[[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]"
---
# Arbitrage Theory in Continuous Time - Ch 32 Portfolio Optimization in Incomplete Markets

## Ingest Scope and Depth

- Ingest stage: `selective_deepen`
- Pass 1: full chapter scan completed.
- Pass 2: selective deepening focused on the contrast between complete- and incomplete-market utility maximization.

## Deepening Targets

- This chapter should be revisited together with Chapter 31 if the vault later builds a dedicated convex-duality and utility-optimization branch.

## Deepened Subparts

- `32.2` the complete market case
- `32.3` incomplete market, finite $\Omega$
- `32.4` incomplete market, general $\Omega$

## Role of the chapter

This chapter extends portfolio optimization beyond the complete-market formulas from Chapter 27.

## Core mathematical objects

- utility maximization over attainable wealths
- feasible-claim set under incompleteness
- dual characterization through martingale measures

## Structural map of the chapter

- restate the complete-market benchmark
- move to finite-state incompleteness
- extend to general-state settings

## Theorem and derivation spine

The durable point is structural:

- in incomplete markets, optimal portfolio choice is constrained by the attainable-claim set and by the entire family of martingale measures, not just one pricing kernel

## Failure modes and misuse points

- applying complete-market first-order conditions in incomplete settings
- ignoring feasibility and attainability constraints

## Quant research relevance

This chapter is support material for utility-based and robust portfolio design.

## What should be promoted out of this source note

- support [[Martingale Methods for Portfolio Optimization]]
- support [[Utility Indifference Pricing]]

## Related notes

- [[Martingale Methods for Portfolio Optimization]]
- [[Utility Indifference Pricing]]
- [[Market Completeness and Incomplete Markets]]

## Sources

- [[Arbitrage Theory in Continuous Time]]
- [[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]

