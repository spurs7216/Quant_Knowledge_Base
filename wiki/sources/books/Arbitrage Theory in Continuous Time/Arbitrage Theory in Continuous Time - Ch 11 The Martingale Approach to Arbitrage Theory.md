---
title: Arbitrage Theory in Continuous Time - Ch 11 The Martingale Approach to Arbitrage Theory
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
extraction_basis: toc_scan_plus_utf8_text_extraction_and_targeted_rendered_theorem_pages
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 11 The Martingale Approach to Arbitrage Theory
parent_source: "[[Arbitrage Theory in Continuous Time]]"
sources:
  - "[[Arbitrage Theory in Continuous Time]]"
  - "[[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]"
---
# Arbitrage Theory in Continuous Time - Ch 11 The Martingale Approach to Arbitrage Theory

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: theorem-level extraction completed for equivalent martingale measures, the informal first and second fundamental theorems, pricing, replication, and stochastic discount factors.

## Deepening Targets

- The precise proofs are pushed into Chapter 12, so this note keeps the conceptual theorem architecture rather than all technical details.

## Deepened Subparts

- `11.2` absence of arbitrage and martingale measures
- `11.3` sketch of the proof
- `11.5` completeness
- `11.6` pricing contingent claims
- `11.8` stochastic discount factors

## Role of the chapter

This chapter reframes the whole book. Earlier pricing arguments worked by local hedging and PDEs. Here the same logic is rewritten as a statement about equivalent martingale measures.

## Core mathematical objects

- equivalent martingale measure $Q\sim P$
- discounted asset prices $\widetilde{S}=S/S^0$
- pricing rule
  $$
  \Pi_t[X]=S_t^0\E^Q\bracket{\frac{X}{S_T^0}\given\mathcal{F}_t}
  $$
- stochastic discount factor $M_t$

## Structural map of the chapter

- define equivalent martingale measures
- state the first and second fundamental theorems informally
- sketch why existence kills arbitrage and why uniqueness gives completeness
- derive pricing, replication, and SDF formulations

## Theorem and derivation spine

### The first fundamental theorem is the existence claim

The rendered theorem page states the book's central informal result:

- the model is arbitrage free essentially if and only if there exists a local martingale measure

The word "essentially" matters because the fully precise theorem needs technical admissibility conditions that are deferred.

### The second fundamental theorem is the uniqueness claim

Once an equivalent martingale measure is unique, prices of attainable claims are unique as well. That is the measure-theoretic form of completeness.

### Pricing and discount factors are dual languages

The chapter makes explicit that arbitrage-free pricing can be written either with a martingale measure or with a stochastic discount factor. That duality becomes critical again in the equilibrium chapters.

## Failure modes and misuse points

- citing FTAP without saying which theorem version and admissibility conditions are in force
- thinking martingale pricing replaces replication rather than encoding it
- treating the stochastic discount factor as disconnected from the martingale-measure story

## Quant research relevance

This chapter is the control center for:

- no-arbitrage pricing
- market completeness
- pricing-kernel language
- connecting finite-dimensional, PDE, and measure-theoretic views of valuation

## What should be promoted out of this source note

- [[Risk-Neutral Pricing and Fundamental Theorems of Asset Pricing]]
- [[Stochastic Discount Factors]]
- [[Market Completeness and Incomplete Markets]]

## Related notes

- [[Risk-Neutral Pricing and Fundamental Theorems of Asset Pricing]]
- [[Stochastic Discount Factors]]
- [[Market Completeness and Incomplete Markets]]
- [[Arbitrage Theory in Continuous Time - Ch 12 The Mathematics of the Martingale Approach]]

## Sources

- [[Arbitrage Theory in Continuous Time]]
- [[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]

