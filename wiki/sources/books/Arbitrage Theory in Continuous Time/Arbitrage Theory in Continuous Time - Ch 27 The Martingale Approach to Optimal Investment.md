---
title: Arbitrage Theory in Continuous Time - Ch 27 The Martingale Approach to Optimal Investment
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - portfolio-choice
  - martingale-methods
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: toc_scan_plus_utf8_text_extraction_and_targeted_rendered_theorem_pages
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 27 The Martingale Approach to Optimal Investment
parent_source: "[[Arbitrage Theory in Continuous Time]]"
sources:
  - "[[Arbitrage Theory in Continuous Time]]"
  - "[[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]"
---
# Arbitrage Theory in Continuous Time - Ch 27 The Martingale Approach to Optimal Investment

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: theorem-level extraction completed for the Lagrangian solution of optimal terminal wealth, the wealth-process representation, and portfolio recovery from the optimal claim.

## Deepening Targets

- If later work needs incomplete-market duality, deepen the connection from this complete-market martingale method to the divergence and indifference chapters.

## Deepened Subparts

- `27.2` the basic idea
- `27.3` the optimal terminal wealth
- `27.4` the optimal wealth process
- `27.5` the optimal portfolio

## Role of the chapter

This chapter is the dual counterpart to the HJB approach. Instead of optimizing directly over controls, it optimizes over terminal wealth subject to a budget constraint written with the pricing kernel.

## Core mathematical objects

- utility conjugacy through $I=(U')^{-1}$
- stochastic discount factor
  $$
  M_t=e^{-\int_0^t r_u\,du}L_t
  $$
- optimal terminal wealth
  $$
  \widehat{X}_T=I(\lambda M_T)
  $$
- optimal wealth process
  $$
  \widehat{X}_t=\E^P\bracket{\frac{M_T}{M_t}\widehat{X}_T\given\mathcal{F}_t}
  $$

## Structural map of the chapter

- rewrite the investment problem as terminal-wealth choice
- solve the static Lagrangian pointwise
- recover the wealth process by martingale valuation
- back out optimal portfolio weights

## Theorem and derivation spine

### The budget constraint is a pricing-kernel constraint

The control problem becomes tractable once feasible terminal wealths are characterized by the discounted expectation constraint under the pricing kernel.

### Optimal terminal wealth is inverse marginal utility evaluated at the pricing kernel

The rendered proposition page states the canonical result:
$$
\widehat{X}_T=I(\lambda M_T).
$$

This is one of the most durable formulas in continuous-time portfolio theory because it shows directly how state prices and preferences interact.

### Dynamic wealth is just the conditional price of the optimal terminal claim

The next proposition then gives
$$
\widehat{X}_t=\E^P\bracket{\frac{M_T}{M_t}\widehat{X}_T\given\mathcal{F}_t},
$$
which shows how the dynamic strategy is recovered from the static optimal terminal claim.

## Failure modes and misuse points

- using the complete-market dual formula in incomplete markets without modification
- forgetting that $\lambda$ is pinned down by the budget constraint, not chosen freely
- treating the pricing kernel as a preference object only, rather than a market-pricing object too

## Quant research relevance

This chapter is central for dynamic asset allocation, consumption-portfolio duality, and the link between utility optimization and state-price densities.

## What should be promoted out of this source note

- [[Martingale Methods for Portfolio Optimization]]
- reinforce [[Stochastic Discount Factors]]

## Related notes

- [[Martingale Methods for Portfolio Optimization]]
- [[Stochastic Discount Factors]]
- [[Stochastic Optimal Control and Hamilton-Jacobi-Bellman Equation]]

## Sources

- [[Arbitrage Theory in Continuous Time]]
- [[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]

