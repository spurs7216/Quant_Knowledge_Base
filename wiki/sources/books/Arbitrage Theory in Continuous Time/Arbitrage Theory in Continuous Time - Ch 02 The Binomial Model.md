---
title: Arbitrage Theory in Continuous Time - Ch 02 The Binomial Model
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - mathematical-finance
  - discrete-time
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: toc_scan_plus_utf8_text_extraction
technical_depth: selective_deepen
ingest_stage: selective_deepen
chapter_or_section: Ch 02 The Binomial Model
parent_source: "[[Arbitrage Theory in Continuous Time]]"
sources:
  - "[[Arbitrage Theory in Continuous Time]]"
  - "[[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]"
---
# Arbitrage Theory in Continuous Time - Ch 02 The Binomial Model

## Ingest Scope and Depth

- Ingest stage: `selective_deepen`
- Pass 1: full chapter scan completed.
- Pass 2: selective deepening focused on one-period arbitrage, risk-neutral valuation, and completeness of the multiperiod tree.

## Deepening Targets

- If later work needs numerical lattice methods, deepen the dynamic-programming side of the multiperiod tree rather than only the pricing identities.

## Deepened Subparts

- `2.1.2` portfolios and arbitrage
- `2.1.4` risk-neutral valuation
- `2.2` multiperiod replication and completeness

## Role of the chapter

The chapter is the book's discrete-time warm start.

Its real value is not the tree itself. Its real value is that it already contains the whole structure that later survives in continuous time: no-arbitrage, state-price vectors, replication, completeness, and risk-neutral pricing.

## Core mathematical objects

- up and down factors $u,d$
- one-period gross risk-free return $R$
- risk-neutral probability
  $$
  q=\frac{R-d}{u-d}
  $$
- one-period pricing identity
  $$
  \Pi_0[X]=\frac{1}{R}\E^q[X]
  $$

## Structural map of the chapter

- define the one-period stock-bond model
- characterize arbitrage by the location of the risk-free return between up and down returns
- derive replication and state-price valuation
- extend the same logic recursively to the multiperiod tree

## Theorem and derivation spine

### One-period no-arbitrage pins down the risk-neutral probability

In the one-stock one-bond tree, absence of arbitrage is equivalent to the familiar interior condition
$$
d<R<u,
$$
and that condition implies a unique state-price or risk-neutral weighting for the two terminal states.

### Completeness is already present in the tree

Because the two traded assets span the two terminal states, every one-period claim is replicable. The multiperiod chapter keeps that spanning logic through backward induction.

### Risk-neutral valuation is a replication theorem, not a forecasting rule

The chapter's pricing formula is valid because the claim is reachable and the market is arbitrage free, not because the physical probability has changed.

## Failure modes and misuse points

- teaching the tree as a toy without connecting it to spanning and replication
- treating $q$ as a subjective forecast
- forgetting that completeness in the binomial model is a linear-algebra statement

## Quant research relevance

This chapter is the cleanest bridge from elementary finance to the later martingale machinery. It is especially useful when translating continuous-time theorems back into finite-dimensional intuition.

## What should be promoted out of this source note

- mostly forward links into [[Market Completeness and Incomplete Markets]]
- no separate durable note because the main linear-algebra generalization arrives in Chapter 3

## Related notes

- [[Arbitrage Theory in Continuous Time]]
- [[Arbitrage Theory in Continuous Time - Ch 03 A More General One Period Model]]
- [[Market Completeness and Incomplete Markets]]

## Sources

- [[Arbitrage Theory in Continuous Time]]
- [[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]

