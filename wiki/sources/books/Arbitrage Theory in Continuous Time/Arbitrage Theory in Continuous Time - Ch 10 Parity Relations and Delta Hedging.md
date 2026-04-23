---
title: Arbitrage Theory in Continuous Time - Ch 10 Parity Relations and Delta Hedging
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - mathematical-finance
  - option-hedging
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: toc_scan_plus_utf8_text_extraction
technical_depth: selective_deepen
ingest_stage: selective_deepen
chapter_or_section: Ch 10 Parity Relations and Delta Hedging
parent_source: "[[Arbitrage Theory in Continuous Time]]"
sources:
  - "[[Arbitrage Theory in Continuous Time]]"
  - "[[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]"
---
# Arbitrage Theory in Continuous Time - Ch 10 Parity Relations and Delta Hedging

## Ingest Scope and Depth

- Ingest stage: `selective_deepen`
- Pass 1: full chapter scan completed.
- Pass 2: selective deepening focused on parity identities, the Greeks, and continuously rebalanced delta-gamma hedging.

## Deepening Targets

- If later work needs a practical volatility note, deepen the hedge-instability implications of gamma and rebalancing frequency.

## Deepened Subparts

- `10.1` parity relations
- `10.2` the Greeks
- `10.3` delta and gamma hedging

## Role of the chapter

This chapter packages several practitioner-facing consequences of the earlier theory.

Parity identities are static arbitrage restrictions. The Greeks and hedge formulas translate the PDE solution into local risk exposures.

## Core mathematical objects

- put-call parity
  $$
  C-P=S-KB(t,T)
  $$
- delta
  $$
  \Delta = \frac{\partial V}{\partial S}
  $$
- gamma
  $$
  \Gamma = \frac{\partial^2 V}{\partial S^2}
  $$

## Structural map of the chapter

- derive static parity relations
- define the Greeks as local sensitivity objects
- show how continuous rebalancing implements delta or delta-gamma hedges

## Theorem and derivation spine

The chapter's core insight is that dynamic hedging is local. Delta hedging removes first-order exposure; gamma measures the curvature that makes discrete rebalancing costly and unstable.

## Failure modes and misuse points

- using parity without matching carry or dividends correctly
- treating a continuously rebalanced hedge as if it were a practical zero-cost identity
- ignoring gamma when discussing hedge quality

## Quant research relevance

This chapter matters for translating arbitrage theory into risk management language: parity, delta, gamma, and hedge slippage.

## What should be promoted out of this source note

- no separate durable note yet; the content mainly strengthens derivatives and hedging notes

## Related notes

- [[Derivatives Markets]]
- [[Risk-Neutral Pricing and Fundamental Theorems of Asset Pricing]]
- [[American Options and Optimal Stopping]]

## Sources

- [[Arbitrage Theory in Continuous Time]]
- [[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]
