---
title: Arbitrage Theory in Continuous Time - Ch 26 Optimal Consumption and Investment
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - stochastic-control
  - portfolio-choice
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: toc_scan_plus_utf8_text_extraction
technical_depth: selective_deepen
ingest_stage: selective_deepen
chapter_or_section: Ch 26 Optimal Consumption and Investment
parent_source: "[[Arbitrage Theory in Continuous Time]]"
sources:
  - "[[Arbitrage Theory in Continuous Time]]"
  - "[[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]"
---
# Arbitrage Theory in Continuous Time - Ch 26 Optimal Consumption and Investment

## Ingest Scope and Depth

- Ingest stage: `selective_deepen`
- Pass 1: full chapter scan completed.
- Pass 2: selective deepening focused on the dynamic investment problem and the mutual-fund theorems.

## Deepening Targets

- The HJB machinery is already promoted from Chapter 25, so this note preserves the portfolio-choice structure rather than redoing all control theory.

## Deepened Subparts

- `26.2` optimal consumption and investment
- `26.3` the mutual fund theorems

## Role of the chapter

This chapter applies control theory to classical Merton-style consumption and portfolio choice.

## Core mathematical objects

- wealth dynamics with consumption
- value function for utility from consumption and terminal wealth
- mutual-fund separation results

## Structural map of the chapter

- generalize the basic control problem
- solve the optimal consumption and investment problem
- derive mutual-fund theorems with and without a risk-free asset

## Theorem and derivation spine

The chapter's main reusable result is structural:

- under the model's regularity assumptions, dynamic portfolio choice can often be collapsed into low-dimensional fund-separation rules

That is useful conceptually even when the exact closed form is not used directly.

## Failure modes and misuse points

- exporting separation results outside the model class that justifies them
- forgetting that utility specification and market completeness affect the fund-separation claim

## Quant research relevance

This chapter supports dynamic allocation work, but the most reusable durable method remains the HJB note plus the Chapter 27 martingale duality note.

## What should be promoted out of this source note

- no standalone durable note yet; keep as support for dynamic portfolio-choice work

## Related notes

- [[Stochastic Optimal Control and Hamilton-Jacobi-Bellman Equation]]
- [[Martingale Methods for Portfolio Optimization]]

## Sources

- [[Arbitrage Theory in Continuous Time]]
- [[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]

