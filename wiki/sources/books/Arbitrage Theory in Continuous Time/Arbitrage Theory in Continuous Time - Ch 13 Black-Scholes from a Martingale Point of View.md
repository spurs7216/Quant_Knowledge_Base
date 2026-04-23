---
title: Arbitrage Theory in Continuous Time - Ch 13 Black-Scholes from a Martingale Point of View
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - mathematical-finance
  - martingale-pricing
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: toc_scan_plus_utf8_text_extraction
technical_depth: selective_deepen
ingest_stage: selective_deepen
chapter_or_section: Ch 13 Black-Scholes from a Martingale Point of View
parent_source: "[[Arbitrage Theory in Continuous Time]]"
sources:
  - "[[Arbitrage Theory in Continuous Time]]"
  - "[[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]"
---
# Arbitrage Theory in Continuous Time - Ch 13 Black-Scholes from a Martingale Point of View

## Ingest Scope and Depth

- Ingest stage: `selective_deepen`
- Pass 1: full chapter scan completed.
- Pass 2: selective deepening focused on the recovery of Black-Scholes by martingale methods rather than PDE hedging.

## Deepening Targets

- This chapter mostly consolidates the previous two chapters, so no separate theorem expansion was needed beyond the pricing identity and completeness link.

## Deepened Subparts

- `13.1` absence of arbitrage
- `13.2` pricing
- `13.3` completeness

## Role of the chapter

This chapter shows that Black-Scholes is not tied to one derivation style. The same model can be derived from PDE hedging or from martingale valuation plus completeness.

## Core mathematical objects

- Black-Scholes stock dynamics
- unique martingale measure
- pricing by conditional expectation under $Q$

## Structural map of the chapter

- verify absence of arbitrage in the diffusion model
- compute the pricing measure
- recover completeness through uniqueness and representation

## Theorem and derivation spine

The point of the chapter is methodological equivalence:

- PDE hedging and martingale pricing are not competing theories
- they are different representations of the same no-arbitrage structure in a complete diffusion model

## Failure modes and misuse points

- treating one derivation route as the "real" one and the other as optional
- forgetting that the two routes can diverge in incomplete or constrained markets

## Quant research relevance

The chapter is a clean reminder that pricing arguments should be checked from more than one angle whenever the model becomes complicated.

## What should be promoted out of this source note

- no separate durable note; this chapter mainly reinforces existing pricing notes

## Related notes

- [[Risk-Neutral Pricing and Fundamental Theorems of Asset Pricing]]
- [[Arbitrage Theory in Continuous Time - Ch 07 Arbitrage Pricing]]
- [[Arbitrage Theory in Continuous Time - Ch 11 The Martingale Approach to Arbitrage Theory]]

## Sources

- [[Arbitrage Theory in Continuous Time]]
- [[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]

