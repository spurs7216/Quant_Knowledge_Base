---
title: Arbitrage Theory in Continuous Time - Ch 38 Endowment Equilibrium Unit Net Supply
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
chapter_or_section: Ch 38 Endowment Equilibrium Unit Net Supply
parent_source: "[[Arbitrage Theory in Continuous Time]]"
sources:
  - "[[Arbitrage Theory in Continuous Time]]"
  - "[[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]"
---
# Arbitrage Theory in Continuous Time - Ch 38 Endowment Equilibrium Unit Net Supply

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: theorem-level extraction completed for the marginal-utility stochastic discount factor, equilibrium short rate, equilibrium Girsanov kernel, and the log-utility specialization.

## Deepening Targets

- If the vault later builds a consumption-based asset-pricing branch, deepen the multiple-endowment extension and factor-model generalization.

## Deepened Subparts

- `38.2` the martingale approach
- `38.2.3` log utility
- `38.3` extending the model

## Role of the chapter

This chapter is the cleanest final statement of the equilibrium branch: the stochastic discount factor is the ratio of marginal utilities, and rates plus risk premia fall out of that object.

## Core mathematical objects

- equilibrium stochastic discount factor
  $$
  M_t=\frac{U_c(t,e_t)}{U_c(0,e_0)}
  $$
- equilibrium short rate
  $$
  r(t,e)= -\frac{U_{ct}(t,e)+a(e)U_{cc}(t,e)+\frac{1}{2}b^2(e)U_{ccc}(t,e)}{U_c(t,e)}
  $$
- equilibrium Girsanov kernel
  $$
  \phi(t,e)=\frac{U_{cc}(t,e)}{U_c(t,e)}\,b(e)
  $$

## Structural map of the chapter

- define the endowment economy
- derive the martingale approach to equilibrium
- compute the SDF, short rate, and risk kernel
- specialize to log utility
- extend to more general endowment structures

## Theorem and derivation spine

### The stochastic discount factor is the marginal-utility ratio

The rendered proposition page states the central equilibrium formula:
$$
M_t=\frac{U_c(t,e_t)}{U_c(0,e_0)}.
$$

That is one of the deepest conceptual closures in the book because it shows how the pricing kernel can emerge from utility curvature instead of only from arbitrage normalization.

### The short rate and Girsanov kernel are implied by utility derivatives

The same page gives explicit formulas for the equilibrium short rate and the equilibrium Girsanov kernel. Those formulas tie time preference, consumption dynamics, and risk aversion directly to pricing objects.

### Log utility gives an interpretable benchmark

The chapter's log-utility specialization makes the equilibrium rate formula concrete and easier to inspect.

## Failure modes and misuse points

- identifying the marginal-utility SDF with a universal empirical fact rather than a model implication
- forgetting that the formulas depend on the chosen utility and endowment dynamics
- mixing equilibrium kernels with arbitrage-only kernels without saying what additional assumptions were used

## Quant research relevance

This chapter matters because it ties together:

- stochastic discount factors
- short rates
- risk premia
- endowment-based equilibrium interpretations of asset prices

## What should be promoted out of this source note

- [[Dynamic Equilibrium Asset Pricing]]
- reinforce [[Stochastic Discount Factors]]

## Related notes

- [[Dynamic Equilibrium Asset Pricing]]
- [[Stochastic Discount Factors]]
- [[Stochastic Optimal Control and Hamilton-Jacobi-Bellman Equation]]
- [[Term-Structure Models]]

## Sources

- [[Arbitrage Theory in Continuous Time]]
- [[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]
