---
title: Arbitrage Theory in Continuous Time - Ch 36 The Cox-Ingersoll-Ross Factor Model
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - equilibrium
  - chapter-digest
  - mathematical-finance
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: toc_scan_plus_utf8_text_extraction_and_targeted_rendered_theorem_pages
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 36 The Cox-Ingersoll-Ross Factor Model
parent_source: "[[Arbitrage Theory in Continuous Time]]"
sources:
  - "[[Arbitrage Theory in Continuous Time]]"
  - "[[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]"
---
# Arbitrage Theory in Continuous Time - Ch 36 The Cox-Ingersoll-Ross Factor Model

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: theorem-level extraction completed for the equilibrium HJB equation, equilibrium short rate, equilibrium risk premium, and the equilibrium stochastic discount factor.

## Deepening Targets

- If later work needs a stronger macro-finance branch, deepen the economic-agent side of the model rather than only the pricing formulas.

## Deepened Subparts

- `36.2` the portfolio problem
- `36.3` equilibrium
- `36.4` the short rate and the risk premium for $F$
- `36.5` the equilibrium stochastic discount factor
- `36.6` risk neutral valuation

## Role of the chapter

This chapter is where the book's arbitrage theory reconnects with equilibrium economics in a fully worked factor model.

## Core mathematical objects

- equilibrium HJB system
- equilibrium short rate
  $$
  r=\mu+\sigma^2\frac{xV_{xx}}{V_x}+\sigma b\frac{V_{xy}}{V_x}
  $$
- equilibrium risk premium for the derivative factor
- equilibrium stochastic discount factor

## Structural map of the chapter

- define exogenous objects and agents
- solve the portfolio problem in equilibrium
- derive the short rate and factor risk premium from the value function
- derive the equilibrium SDF and risk-neutral valuation formulas

## Theorem and derivation spine

### Equilibrium still solves an HJB equation

The rendered theorem page states the equilibrium HJB system. The important point is that equilibrium pricing objects are derived from an optimization problem, not postulated independently.

### The short rate and risk premium come from marginal value curvature

The chapter derives
$$
r=\mu+\sigma^2\frac{xV_{xx}}{V_x}+\sigma b\frac{V_{xy}}{V_x},
$$
and a matching formula for the factor risk premium. Those formulas show directly how risk premia and rates inherit curvature from the equilibrium value function.

### The stochastic discount factor is endogenous

Unlike earlier no-arbitrage chapters, the discount factor here is not selected from the martingale-measure family by fiat. It is implied by the equilibrium optimization problem.

## Failure modes and misuse points

- treating equilibrium SDF formulas as if they were purely no-arbitrage objects
- forgetting the dependence on the specific utility and state dynamics
- reading the CIR factor label as merely a rates model instead of a full equilibrium model here

## Quant research relevance

This chapter is useful because it makes explicit how rates, risk premia, and pricing kernels can all come from one equilibrium structure.

## What should be promoted out of this source note

- [[Dynamic Equilibrium Asset Pricing]]
- reinforce [[Stochastic Discount Factors]]

## Related notes

- [[Dynamic Equilibrium Asset Pricing]]
- [[Stochastic Discount Factors]]
- [[Stochastic Optimal Control and Hamilton-Jacobi-Bellman Equation]]

## Sources

- [[Arbitrage Theory in Continuous Time]]
- [[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]

