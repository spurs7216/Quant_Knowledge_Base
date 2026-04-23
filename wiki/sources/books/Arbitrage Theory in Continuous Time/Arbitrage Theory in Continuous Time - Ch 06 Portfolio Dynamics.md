---
title: Arbitrage Theory in Continuous Time - Ch 06 Portfolio Dynamics
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - mathematical-finance
  - portfolio-dynamics
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: toc_scan_plus_utf8_text_extraction
technical_depth: selective_deepen
ingest_stage: selective_deepen
chapter_or_section: Ch 06 Portfolio Dynamics
parent_source: "[[Arbitrage Theory in Continuous Time]]"
sources:
  - "[[Arbitrage Theory in Continuous Time]]"
  - "[[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]"
---
# Arbitrage Theory in Continuous Time - Ch 06 Portfolio Dynamics

## Ingest Scope and Depth

- Ingest stage: `selective_deepen`
- Pass 1: full chapter scan completed.
- Pass 2: selective deepening focused on self-financing definitions, continuous-time wealth dynamics, and portfolio weights.

## Deepening Targets

- If this branch later needs transaction-cost or consumption extensions, deepen the distinction between holdings, weights, and dividend-adjusted gains.

## Deepened Subparts

- `6.2` self-financing portfolios in discrete time
- `6.3` self-financing portfolios in continuous time
- `6.4` portfolio weights

## Role of the chapter

This chapter formalizes what a trading strategy is allowed to do.

Later pricing theorems do not work without this bookkeeping layer because arbitrage, replication, and hedging all depend on the precise self-financing definition.

## Core mathematical objects

- holdings vector $h_t$
- wealth process
  $$
  V_t=h_t S_t
  $$
- self-financing condition
  $$
  dV_t=h_t\,dS_t
  $$
- cumulative dividend adjustments
- portfolio weights $w_t$

## Structural map of the chapter

- define portfolios and wealth in discrete time
- separate dividend flows from capital gains
- move to continuous-time self-financing dynamics
- rewrite the same logic in terms of wealth weights

## Theorem and derivation spine

The chapter is definition-heavy rather than theorem-heavy. Its load-bearing content is the self-financing identity:
$$
dV_t=h_t\,dS_t,
$$
possibly after adjusting for dividends or consumptions.

Without that identity, later claims about hedging and replication are only slogans.

## Failure modes and misuse points

- mixing wealth weights with asset holdings
- forgetting dividend adjustments
- writing down a hedge without checking that the strategy is self-financing

## Quant research relevance

This chapter matters whenever a pricing argument claims:

- a claim can be replicated
- a portfolio is delta hedged
- a change of numeraire is implemented through trading rather than pure algebra

## What should be promoted out of this source note

- no separate durable note yet; this chapter mainly supports pricing and control notes

## Related notes

- [[Arbitrage Theory in Continuous Time - Ch 07 Arbitrage Pricing]]
- [[Arbitrage Theory in Continuous Time - Ch 08 Completeness and Hedging]]
- [[Risk-Neutral Pricing and Fundamental Theorems of Asset Pricing]]

## Sources

- [[Arbitrage Theory in Continuous Time]]
- [[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]

