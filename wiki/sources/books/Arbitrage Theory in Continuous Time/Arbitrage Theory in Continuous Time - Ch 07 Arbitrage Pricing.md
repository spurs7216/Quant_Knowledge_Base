---
title: Arbitrage Theory in Continuous Time - Ch 07 Arbitrage Pricing
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - mathematical-finance
  - arbitrage-pricing
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: toc_scan_plus_utf8_text_extraction_and_targeted_rendered_theorem_pages
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 07 Arbitrage Pricing
parent_source: "[[Arbitrage Theory in Continuous Time]]"
sources:
  - "[[Arbitrage Theory in Continuous Time]]"
  - "[[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]"
---
# Arbitrage Theory in Continuous Time - Ch 07 Arbitrage Pricing

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: theorem-level extraction completed for bank-account dynamics, contingent-claim pricing, the Black-Scholes equation, risk-neutral valuation, and volatility interpretation.

## Deepening Targets

- If later work needs a richer volatility branch, deepen the implied-volatility remarks and their dependence on model misspecification.

## Deepened Subparts

- `7.3` contingent claims and arbitrage
- `7.4` the Black-Scholes equation
- `7.5` risk neutral valuation
- `7.6` the Black-Scholes formula
- `7.8` volatility

## Role of the chapter

This chapter is the first full continuous-time pricing chapter in the book.

It turns the self-financing machinery into a derivative-pricing theorem and makes explicit that the Black-Scholes PDE and risk-neutral expectation are two faces of the same arbitrage argument.

## Core mathematical objects

- money-market account
  $$
  dB_t=r_t B_t\,dt
  $$
- claim price $F(t,S_t)$
- Black-Scholes PDE
  $$
  F_t+rSF_S+\frac{1}{2}\sigma^2 S^2 F_{SS}-rF=0
  $$
- risk-neutral valuation
  $$
  \Pi_t[X]=B_t\E^Q\bracket{\frac{X}{B_T}\given\mathcal{F}_t}
  $$

## Structural map of the chapter

- model the bank account and stock
- define contingent claims and the arbitrage principle
- derive the pricing PDE from self-financing replication
- recover the same value by martingale valuation
- connect theory to forwards, futures, and volatility language

## Theorem and derivation spine

### Local riskless hedging forces the pricing PDE

The chapter's central replication argument chooses the stock holding so the diffusion term in the hedged portfolio vanishes. Arbitrage then forces the remaining drift to equal the short rate, yielding
$$
F_t+rSF_S+\frac{1}{2}\sigma^2 S^2 F_{SS}-rF=0.
$$

### Risk-neutral valuation is the same theorem in measure form

Once the discounted stock is a martingale under $Q$, the pricing rule becomes
$$
\Pi_t[X]=B_t\E^Q\bracket{\frac{X}{B_T}\given\mathcal{F}_t}.
$$

The point is not that $Q$ is a forecast measure. The point is that $Q$ is the measure under which arbitrage-free discounted pricing becomes conditional expectation.

### Volatility enters pricing through diffusion scale, not directly through expected return

The chapter keeps stressing the standard Black-Scholes lesson: under arbitrage pricing, expected return drops out of the option formula, while volatility remains.

## Failure modes and misuse points

- treating the risk-neutral measure as a physical-return model
- forgetting that the PDE is derived under self-financing replication
- speaking about implied volatility as if it were a primitive structural parameter

## Quant research relevance

This chapter remains foundational for:

- option pricing
- delta hedging
- forward and futures valuation
- the conceptual split between pricing drift and statistical drift

## What should be promoted out of this source note

- reinforce [[Risk-Neutral Pricing and Fundamental Theorems of Asset Pricing]]
- reinforce [[Term-Structure Models]] through the general pricing identity

## Related notes

- [[Risk-Neutral Pricing and Fundamental Theorems of Asset Pricing]]
- [[Arbitrage Theory in Continuous Time - Ch 08 Completeness and Hedging]]
- [[Arbitrage Theory in Continuous Time - Ch 11 The Martingale Approach to Arbitrage Theory]]
- [[Derivatives Markets]]

## Sources

- [[Arbitrage Theory in Continuous Time]]
- [[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]

