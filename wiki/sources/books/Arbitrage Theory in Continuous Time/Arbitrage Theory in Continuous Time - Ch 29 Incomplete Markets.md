---
title: Arbitrage Theory in Continuous Time - Ch 29 Incomplete Markets
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - incomplete-markets
  - chapter-digest
  - mathematical-finance
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: toc_scan_plus_utf8_text_extraction_and_targeted_rendered_theorem_pages
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 29 Incomplete Markets
parent_source: "[[Arbitrage Theory in Continuous Time]]"
sources:
  - "[[Arbitrage Theory in Continuous Time]]"
  - "[[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]"
---
# Arbitrage Theory in Continuous Time - Ch 29 Incomplete Markets

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: theorem-level extraction completed for factor-Markov incompleteness, the independent-factor model, and the structural reason unique pricing fails.

## Deepening Targets

- The chapter mainly builds the model class used in later measure-selection chapters, so the next deepening step would be to merge it with Chapters 30 to 34 as one incompleteness cluster.

## Deepened Subparts

- `29.2` a Markov factor model
- `29.3` the independent factor Markov model
- `29.4` methods to handle market incompleteness

## Role of the chapter

This chapter defines the main incomplete-market model class used later: traded assets depend on state factors, but not all factors are spanned by traded securities.

## Core mathematical objects

- factor process $Y_t$
- traded asset process $S_t$
- traded-risk and nontraded-risk decomposition
- family of admissible martingale measures

## Structural map of the chapter

- define the factor-Markov model
- specialize to independent-factor structure
- prove the existence of unspanned risk
- catalog the main ways to choose prices in incomplete markets

## Theorem and derivation spine

### Incompleteness comes from unspanned factor risk

The chapter's core theorem says that even when stock risk has a unique market-price-of-risk component, nontraded factor shocks leave many martingale measures admissible.

### Measure selection is a separate problem

Once the market is incomplete, no-arbitrage alone produces a set of prices rather than a single price. Later chapters then choose among those measures by Esscher, entropy, utility, or good-deal criteria.

## Failure modes and misuse points

- speaking about "the" martingale measure in an incomplete model
- forgetting which components of state risk are actually hedgeable
- assuming incompleteness is a numerical issue rather than a structural one

## Quant research relevance

This chapter is the durable entry point into realistic pricing settings with stochastic volatility, basis risk, nontraded state variables, and preference-dependent valuation.

## What should be promoted out of this source note

- [[Market Completeness and Incomplete Markets]]
- support [[Esscher Transform and Minimal Martingale Measure]]

## Related notes

- [[Market Completeness and Incomplete Markets]]
- [[Esscher Transform and Minimal Martingale Measure]]
- [[Utility Indifference Pricing]]
- [[Good Deal Bounds]]

## Sources

- [[Arbitrage Theory in Continuous Time]]
- [[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]

