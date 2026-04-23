---
title: Arbitrage Theory in Continuous Time - Ch 20 Short Rate Models
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - fixed-income
  - short-rate
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: toc_scan_plus_utf8_text_extraction
technical_depth: selective_deepen
ingest_stage: selective_deepen
chapter_or_section: Ch 20 Short Rate Models
parent_source: "[[Arbitrage Theory in Continuous Time]]"
sources:
  - "[[Arbitrage Theory in Continuous Time]]"
  - "[[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]"
---
# Arbitrage Theory in Continuous Time - Ch 20 Short Rate Models

## Ingest Scope and Depth

- Ingest stage: `selective_deepen`
- Pass 1: full chapter scan completed.
- Pass 2: selective deepening focused on the term-structure equation and the role of the market price of risk in short-rate models.

## Deepening Targets

- The concrete tractable short-rate families are treated more heavily in Chapter 21, so this note stays at the modeling-framework level.

## Deepened Subparts

- `20.2` the term structure equation
- `20.3` martingale analysis

## Role of the chapter

This chapter packages the short-rate program: specify an SDE for $r_t$, add a market price of risk, and solve for bond prices.

## Core mathematical objects

- short-rate diffusion
  $$
  dr_t=\mu(t,r_t)\,dt+\sigma(t,r_t)\,dW_t
  $$
- term-structure PDE
- pricing kernel via risk-neutral valuation

## Structural map of the chapter

- generalities
- derive the term-structure PDE
- restate bond pricing by martingale methods

## Theorem and derivation spine

The key durable point is that short-rate models do not determine the market price of risk endogenously. Arbitrage fixes the pricing PDE once $\lambda$ is specified, but it does not choose $\lambda$ for you.

## Failure modes and misuse points

- thinking a short-rate diffusion alone is a complete rates model
- forgetting that calibration depends on both state dynamics and risk-premium specification

## Quant research relevance

This chapter is useful as the entry point into Vasicek, CIR, Hull-White, and other tractable rate models.

## What should be promoted out of this source note

- no separate durable note; feed Chapter 21 and the term-structure note instead

## Related notes

- [[Term-Structure Models]]
- [[Arbitrage Theory in Continuous Time - Ch 21 Martingale Models for the Short Rate]]

## Sources

- [[Arbitrage Theory in Continuous Time]]
- [[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]

