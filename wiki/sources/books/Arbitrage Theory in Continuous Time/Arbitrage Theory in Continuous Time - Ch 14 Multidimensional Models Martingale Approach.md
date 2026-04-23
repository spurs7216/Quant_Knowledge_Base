---
title: Arbitrage Theory in Continuous Time - Ch 14 Multidimensional Models Martingale Approach
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - mathematical-finance
  - multidimensional-pricing
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: toc_scan_plus_utf8_text_extraction_and_targeted_rendered_theorem_pages
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 14 Multidimensional Models Martingale Approach
parent_source: "[[Arbitrage Theory in Continuous Time]]"
sources:
  - "[[Arbitrage Theory in Continuous Time]]"
  - "[[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]"
---
# Arbitrage Theory in Continuous Time - Ch 14 Multidimensional Models Martingale Approach

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: theorem-level extraction completed for multidimensional no-arbitrage conditions, completeness as a rank condition, pricing, market prices of risk, and Hansen-Jagannathan bounds.

## Deepening Targets

- If later work needs a cross-sectional asset-pricing branch, deepen the Hansen-Jagannathan section into its own empirical note.

## Deepened Subparts

- `14.1` absence of arbitrage
- `14.2` completeness
- `14.4` pricing
- `14.6` market prices of risk
- `14.8` Hansen-Jagannathan bounds

## Role of the chapter

This chapter generalizes the martingale approach from one risky asset to many. That is where rank, kernel, and market-price-of-risk geometry become explicit.

## Core mathematical objects

- volatility matrix $\sigma_t$
- market price of risk vector $\lambda_t$
- martingale-measure equation
  $$
  \alpha_t-r_t\mathbf{1}=\sigma_t\lambda_t
  $$
- completeness condition
  $$
  \operatorname{Im}(\sigma_t^\ast)=\mathbb{R}^N
  $$

## Structural map of the chapter

- characterize absence of arbitrage by solvability of the drift-restriction equation
- characterize completeness by a rank condition
- derive pricing and hedging in the multidimensional model
- connect the stochastic discount factor to mean-volatility restrictions

## Theorem and derivation spine

### No-arbitrage is a linear-algebra condition on the drift

The chapter shows that absence of arbitrage requires the excess-drift vector to lie in the image of the volatility matrix:
$$
\alpha_t-r_t\mathbf{1}=\sigma_t\lambda_t.
$$

If that equation has no solution, the model asks for risk premia that no equivalent martingale measure can support.

### Completeness is full spanning of Brownian risk

The rendered theorem page states the precise equivalence:
$$
\operatorname{Im}(\sigma_t^\ast)=\mathbb{R}^N
$$
if and only if the model is complete, and that is equivalent to uniqueness of the martingale measure in this setting.

### Hansen-Jagannathan bounds tie SDF volatility to asset-pricing restrictions

The chapter's final section matters because it moves the stochastic discount factor from a pricing convenience to an empirical restriction on admissible kernels.

## Failure modes and misuse points

- talking about "the" market price of risk when the system is underidentified
- confusing more assets with more completeness even when the volatility span is deficient
- ignoring the distinction between absence of arbitrage and empirical plausibility

## Quant research relevance

This chapter matters for:

- multi-asset derivative pricing
- factor-model pricing restrictions
- stochastic discount factor diagnostics
- thinking clearly about spanning and redundancy

## What should be promoted out of this source note

- refresh [[Risk-Neutral Pricing and Fundamental Theorems of Asset Pricing]]
- refresh [[Stochastic Discount Factors]]
- support [[Market Completeness and Incomplete Markets]]

## Related notes

- [[Risk-Neutral Pricing and Fundamental Theorems of Asset Pricing]]
- [[Stochastic Discount Factors]]
- [[Market Completeness and Incomplete Markets]]
- [[Derivatives Markets]]

## Sources

- [[Arbitrage Theory in Continuous Time]]
- [[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]

