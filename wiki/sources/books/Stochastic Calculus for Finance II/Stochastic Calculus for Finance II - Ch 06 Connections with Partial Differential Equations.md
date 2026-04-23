---
title: Stochastic Calculus for Finance II - Ch 06 Connections with Partial Differential Equations
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - stochastic-calculus
  - pde
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: toc_scan_plus_visual_read_of_feynman_kac_and_interest_rate_pde_pages
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 06 Connections with Partial Differential Equations
parent_source: "[[Stochastic Calculus for Finance II]]"
sources:
  - "[[Stochastic Calculus for Finance II]]"
  - "[[raw/math_statistics/Steven E. Shreve-Stochastic Calculus for Finance II_20150303200346.pdf]]"
---
# Stochastic Calculus for Finance II - Ch 06 Connections with Partial Differential Equations

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed against the raw source.
- Pass 2: theorem-level extraction completed for stochastic differential equations, the Feynman-Kac theorem, discounted Feynman-Kac logic, and the one-factor interest-rate PDE.

## Deepening Targets

- If later work needs a stronger numerical branch, deepen the finite-difference and calibration implications of the PDE formulations.

## Deepened Subparts

- `6.2` stochastic differential equations
- `6.4` partial differential equations
- `6.5` interest rate models
- `6.6` multidimensional Feynman-Kac theorems

## Role of the chapter

This chapter explains why derivative pricing can be written either as a conditional expectation or as a PDE boundary-value problem.

That equivalence is one of the book's most reusable structural insights.

## Core mathematical objects

- one-dimensional SDE
  $$dX(u)=\beta(u,X(u))\,du+\gamma(u,X(u))\,dW(u)$$
- Feynman-Kac value function
  $$g(t,x)=\mathbb{E}^{t,x}h(X(T))$$
- associated PDE
  $$g_t+\beta g_x+\frac{1}{2}\gamma^2 g_{xx}=0, \qquad g(T,x)=h(x)$$
- discounted interest-rate PDE
  $$c_t+\beta c_r+\frac{1}{2}\gamma^2 c_{rr}=rc$$

## Structural map of the chapter

- SDEs as the state dynamics beneath pricing
- one-dimensional Feynman-Kac
- PDE representation for interest-rate contingent claims
- multidimensional Feynman-Kac generalization

## Theorem and derivation spine

### Feynman-Kac converts future expectation into present PDE

The rendered theorem page states:

$$dX(u)=\beta(u,X(u))\,du+\gamma(u,X(u))\,dW(u),$$
$$g(t,x)=\mathbb{E}^{t,x}h(X(T)).$$

Then $g$ satisfies

$$g_t(t,x)+\beta(t,x)g_x(t,x)+\frac{1}{2}\gamma^2(t,x)g_{xx}(t,x)=0,$$

with terminal condition

$$g(T,x)=h(x).$$

This is the formal bridge from a diffusion law to a valuation PDE.

### Discounting changes the PDE source term

When the claim is discounted by the short rate, the PDE acquires the $rc$ term.

The rendered interest-rate example writes the call-price function $c(t,r)$ as the solution of

$$c_t(t,r)+\beta(t,r)c_r(t,r)+\frac{1}{2}\gamma^2(t,r)c_{rr}(t,r)=r\,c(t,r).$$

That is the rates analogue of the Black-Scholes equation, with the state variable now being the short rate instead of the stock price.

### Multidimensional state variables do not change the logic

The rendered multidimensional page extends the theorem to a system driven by two Brownian motions:

$$dX_1(u)=\beta_1\,du+\gamma_{11}\,dW_1(u)+\gamma_{12}\,dW_2(u),$$
$$dX_2(u)=\beta_2\,du+\gamma_{21}\,dW_1(u)+\gamma_{22}\,dW_2(u),$$

with value functions

$$g(t,x_1,x_2)=\mathbb{E}^{t,x_1,x_2}h(X_1(T),X_2(T)),$$
$$f(t,x_1,x_2)=\mathbb{E}^{t,x_1,x_2}\bracket{e^{-r(T-t)}h(X_1(T),X_2(T))}.$$

So the PDE route is not restricted to one-dimensional textbook examples.

## Failure modes and misuse points

- treating the PDE and expectation forms as different models rather than equivalent representations
- forgetting which drift and discount rate belong to the pricing measure
- using a PDE solver without first checking whether the underlying SDE model is well specified
- assuming the state variable is always the asset price rather than a richer Markov state

## Quant research relevance

This chapter matters for:

- pricing under state-variable diffusions
- rates derivatives
- numerical PDE solvers
- linking simulation and PDE validation in the same model

## What should be promoted out of this source note

- PDE synthesis inside [[Risk-Neutral Pricing and Fundamental Theorems of Asset Pricing]]
- durable bridge into [[Term-Structure Models]]

## Related notes

- [[Stochastic Calculus for Finance II]]
- [[Stochastic Calculus for Finance II - Ch 05 Risk-Neutral Pricing]]
- [[Stochastic Calculus for Finance II - Ch 10 Term-Structure Models]]
- [[Risk-Neutral Pricing and Fundamental Theorems of Asset Pricing]]
- [[Term-Structure Models]]

## Sources

- [[Stochastic Calculus for Finance II]]
- [[raw/math_statistics/Steven E. Shreve-Stochastic Calculus for Finance II_20150303200346.pdf]]
