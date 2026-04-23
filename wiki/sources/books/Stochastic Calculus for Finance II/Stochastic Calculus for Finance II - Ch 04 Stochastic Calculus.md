---
title: Stochastic Calculus for Finance II - Ch 04 Stochastic Calculus
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - stochastic-calculus
  - ito-calculus
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: toc_scan_plus_visual_read_of_ito_formula_black_scholes_and_levy_pages
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 04 Stochastic Calculus
parent_source: "[[Stochastic Calculus for Finance II]]"
sources:
  - "[[Stochastic Calculus for Finance II]]"
  - "[[raw/math_statistics/Steven E. Shreve-Stochastic Calculus for Finance II_20150303200346.pdf]]"
---
# Stochastic Calculus for Finance II - Ch 04 Stochastic Calculus

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed against the raw source.
- Pass 2: theorem-level extraction completed for the Ito integral, Ito-Doeblin formula, Black-Scholes-Merton derivation, multivariable Ito rules, and Levy characterization.

## Deepening Targets

- If later work needs a stronger stochastic-numerics branch, deepen Brownian bridge and the integral-construction proofs.

## Deepened Subparts

- `4.2` Ito's integral for simple integrands
- `4.3` Ito's integral for general integrands
- `4.4` Ito-Doeblin formula
- `4.5` Black-Scholes-Merton equation
- `4.6` multivariable stochastic calculus

## Role of the chapter

This is the technical core of the book.

Chapter 3 explains why ordinary calculus fails. Chapter 4 builds the replacement calculus and then immediately shows why it matters for derivative pricing.

## Core mathematical objects

- Ito integral
  $$\int_0^t \Phi(u)\,dW(u)$$
- Ito isometry
  $$\mathbb{E}\bracket{\paren{\int_0^T \Phi(u)\,dW(u)}^2}=\mathbb{E}\int_0^T \Phi^2(u)\,du$$
- Ito-Doeblin formula for Brownian motion
  $$df(W(t))=f'(W(t))\,dW(t)+\frac{1}{2}f''(W(t))\,dt$$
- self-financing stock-cash portfolio
  $$dX(t)=\Delta(t)\,dS(t)+r\paren{X(t)-\Delta(t)S(t)}\,dt$$
- Black-Scholes-Merton PDE
  $$c_t+rxc_x+\frac{1}{2}\sigma^2 x^2 c_{xx}=rc$$

## Structural map of the chapter

- define the Ito integral first for simple and then general adapted integrands
- derive the one-dimensional and multivariate Ito-Doeblin rules
- turn those differential rules into the Black-Scholes-Merton pricing equation
- recognize Brownian motion from martingale plus quadratic-variation structure

## Theorem and derivation spine

### Ito-Doeblin adds the quadratic-variation term

The rendered Ito-Doeblin page states:

$$df(W(t))=f'(W(t))\,dW(t)+\frac{1}{2}f''(W(t))\,dt,$$

and in integral form

$$f(W(t))-f(W(0))=\int_0^t f'(W(u))\,dW(u)+\frac{1}{2}\int_0^t f''(W(u))\,du.$$

The extra drift term is exactly the mathematical effect of $[W,W](t)=t$.

### Product and multivariate rules are not cosmetic extensions

The rendered multivariate page states the Ito product rule:

$$d\paren{X(t)Y(t)}=X(t)\,dY(t)+Y(t)\,dX(t)+dX(t)\,dY(t).$$

This is the operational rule behind self-financing portfolio algebra, covariance terms, and state augmentation.

### Black-Scholes-Merton comes from matching the two discounted evolutions

The chapter writes the discounted stock dynamics as

$$d\paren{e^{-rt}S(t)}=(\alpha-r)e^{-rt}S(t)\,dt+\sigma e^{-rt}S(t)\,dW(t),$$

and the discounted self-financing portfolio dynamics as

$$d\paren{e^{-rt}X(t)}=\Delta(t)\,d\paren{e^{-rt}S(t)}.$$

For the option value $c(t,S(t))$, Ito-Doeblin gives

$$dc(t,S(t))=\bracket{c_t+\alpha S c_x+\frac{1}{2}\sigma^2 S^2 c_{xx}}dt+\sigma S c_x\,dW(t).$$

Discounting and imposing replication with $\Delta(t)=c_x(t,S(t))$ cancels the diffusion term and forces the drift identity

$$c_t+rSc_x+\frac{1}{2}\sigma^2 S^2 c_{xx}=rc.$$

That is the Black-Scholes-Merton equation in the book's chapter order: Ito first, pricing PDE second.

### Levy characterization shows how much structure Brownian motion carries

The rendered theorem page states that if a martingale $M(t)$ has continuous paths, starts at zero, and satisfies

$$[M,M](t)=t,$$

then $M(t)$ is a Brownian motion.

That result matters because it shows quadratic variation is not just a statistic of Brownian motion. Together with the martingale property, it characterizes the process.

## Failure modes and misuse points

- using differential notation without remembering which second-order terms survive
- treating $\Delta=c_x$ as a heuristic rather than the diffusion-canceling choice from replication
- confusing the actual drift $\alpha$ with the risk-free rate $r$
- forgetting that the calculus is adapted-process calculus, not pathwise ordinary differentiation

## Quant research relevance

This chapter is central for:

- SDE modeling
- diffusion simulation
- Black-Scholes and Greek derivations
- self-financing portfolio algebra
- continuous-time control and filtering models that use Ito rules

## What should be promoted out of this source note

- [[Ito Calculus and Stochastic Differential Equations]]
- refreshed umbrella synthesis in [[Stochastic Calculus]]

## Related notes

- [[Stochastic Calculus for Finance II]]
- [[Brownian Motion and Quadratic Variation]]
- [[Ito Calculus and Stochastic Differential Equations]]
- [[Risk-Neutral Pricing and Fundamental Theorems of Asset Pricing]]
- [[Stochastic Calculus]]

## Sources

- [[Stochastic Calculus for Finance II]]
- [[raw/math_statistics/Steven E. Shreve-Stochastic Calculus for Finance II_20150303200346.pdf]]
