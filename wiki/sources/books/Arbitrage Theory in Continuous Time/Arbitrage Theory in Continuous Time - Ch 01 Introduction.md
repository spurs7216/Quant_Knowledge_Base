---
title: Arbitrage Theory in Continuous Time - Ch 01 Introduction
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - mathematical-finance
  - continuous-time-finance
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: scanned_chapter
extraction_basis: toc_scan_plus_utf8_text_extraction
technical_depth: scan
ingest_stage: scan
chapter_or_section: Ch 01 Introduction
parent_source: "[[Arbitrage Theory in Continuous Time]]"
sources:
  - "[[Arbitrage Theory in Continuous Time]]"
  - "[[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]"
---
# Arbitrage Theory in Continuous Time - Ch 01 Introduction

## Ingest Scope and Depth

- Ingest stage: `scan`
- Pass 1: chapter scan completed against the raw source.
- Pass 2: no theorem-level deepen was needed because the chapter is mainly framing rather than technical proof work.

## Deepening Targets

- If this shelf later needs a durable introductory finance note, reuse this chapter's contrast between actuarial discounting, supply-demand stories, and arbitrage-based pricing.

## Role of the chapter

This chapter states the book's governing problem:

- what is a fair derivative price?
- how can a seller hedge the resulting risk?

It also states the book's most important philosophical move: derivative pricing is not an unconditional expectation problem and not a pure equilibrium-demand story. It is a relative-pricing problem constrained by the underlying traded assets.

## Core mathematical objects

- contingent claim $X$
- traded underlying assets $S$
- hedging portfolio $h$
- arbitrage and relative pricing consistency

## Structural map of the chapter

- formulate fair-pricing and hedging as the two main problems
- reject naive discounted-expectation pricing as the whole story
- reject pure supply-demand agnosticism as the whole story
- define the book's target as pricing claims consistently with traded underlying assets

## Theorem and derivation spine

This chapter is not theorem-heavy. The load-bearing result is conceptual:

- derivative prices must be linked to traded-asset prices by arbitrage restrictions
- later chapters formalize that link through self-financing, martingale measures, and completeness

## Failure modes and misuse points

- treating pricing as plain expectation under the physical measure
- treating "market price" as too unconstrained for theory to say anything useful
- missing that the entire book studies relative pricing, not absolute value

## Quant research relevance

This chapter sets the doctrine for the rest of the shelf:

- fair pricing is model-dependent but not arbitrary
- hedging and pricing must be studied together
- no-arbitrage theory is the bridge between mathematical finance and market data

## What should be promoted out of this source note

- no immediate durable note; this chapter mainly frames the book

## Related notes

- [[Arbitrage Theory in Continuous Time]]
- [[Derivatives Markets]]
- [[Risk-Neutral Pricing and Fundamental Theorems of Asset Pricing]]

## Sources

- [[Arbitrage Theory in Continuous Time]]
- [[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]

