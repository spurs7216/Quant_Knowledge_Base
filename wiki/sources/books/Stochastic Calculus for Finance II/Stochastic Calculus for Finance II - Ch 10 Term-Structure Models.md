---
title: Stochastic Calculus for Finance II - Ch 10 Term-Structure Models
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - stochastic-calculus
  - term-structure
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: toc_scan_plus_visual_read_of_affine_yield_hjm_and_forward_libor_pages
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 10 Term-Structure Models
parent_source: "[[Stochastic Calculus for Finance II]]"
sources:
  - "[[Stochastic Calculus for Finance II]]"
  - "[[raw/math_statistics/Steven E. Shreve-Stochastic Calculus for Finance II_20150303200346.pdf]]"
---
# Stochastic Calculus for Finance II - Ch 10 Term-Structure Models

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed against the raw source.
- Pass 2: theorem-level extraction completed for affine-yield structure, Heath-Jarrow-Morton dynamics, and the forward-LIBOR market-model bridge to Black caplets.

## Deepening Targets

- If later work needs a stronger fixed-income branch, deepen the calibration and empirical instability issues of HJM and forward-LIBOR models.

## Deepened Subparts

- `10.2` affine-yield models
- `10.3` Heath-Jarrow-Morton model
- `10.4` forward LIBOR model

## Role of the chapter

This chapter moves from one risky asset to an entire yield curve.

It is where continuous-time pricing becomes explicitly infinite-dimensional, and where no-arbitrage drift restrictions become model design constraints instead of after-the-fact checks.

## Core mathematical objects

- zero-coupon bond price
  $$B(t,T)$$
- instantaneous forward rate
  $$f(t,T)$$
- HJM volatility integral
  $$\sigma^\star(t,T)=\int_t^T \sigma(t,u)\,du$$
- HJM risk-neutral dynamics
  $$df(t,T)=\sigma(t,T)\sigma^\star(t,T)\,dt+\sigma(t,T)\,d\widetilde{W}(t)$$
- bond-price dynamics
  $$dB(t,T)=R(t)B(t,T)\,dt-\sigma^\star(t,T)B(t,T)\,d\widetilde{W}(t)$$
- forward LIBOR
  $$L(t,T)=\frac{1}{\delta}\paren{\frac{B(t,T)}{B(t,T+\delta)}-1}$$

## Structural map of the chapter

- affine-yield short-rate families
- HJM as a forward-rate-curve model
- forward-LIBOR market model for caplet pricing

## Theorem and derivation spine

### Affine-yield models keep bond prices exponential-affine in the state

The chapter starts with affine-yield families where yields or log bond prices are affine functions of the state variables.

That structure matters because it makes term-structure modeling analytically tractable while preserving economic interpretation of factors.

### HJM makes the whole forward curve the state

The rendered HJM theorem page states that, under the risk-neutral measure, an arbitrage-free term-structure model satisfies

$$df(t,T)=\sigma(t,T)\sigma^\star(t,T)\,dt+\sigma(t,T)\,d\widetilde{W}(t),$$

with

$$\sigma^\star(t,T)=\int_t^T \sigma(t,u)\,du, \qquad R(t)=f(t,t).$$

The corresponding bond-price dynamics are

$$dB(t,T)=R(t)B(t,T)\,dt-\sigma^\star(t,T)B(t,T)\,d\widetilde{W}(t).$$

This is the no-arbitrage drift restriction. In HJM, volatility can be specified more freely, but drift is then forced.

### Forward LIBOR aligns the model with caplet trading conventions

The chapter then explains why continuously compounded forward rates are awkward for some fixed-income derivatives and instead moves to the forward LIBOR rate.

The rendered caplet page writes

$$L(t,T)=\frac{1}{\delta}\paren{\frac{B(t,T)}{B(t,T+\delta)}-1},$$

and prices the caplet by using $B(t,T+\delta)$ as numeraire. That is the conceptual route from no-arbitrage term-structure modeling to Black-style caplet formulas and later BGM market models.

## Failure modes and misuse points

- treating a curve model as just many short-rate models pasted together
- ignoring the HJM drift restriction and then calling the specification arbitrage-free
- forgetting that calibration convenience and economic realism can pull in different directions
- using a forward-rate model whose state variable does not match the derivative payoff convention

## Quant research relevance

This chapter matters for:

- yield-curve modeling
- rates derivative pricing
- caplet and swaption logic
- curve-factor interpretation and calibration

## What should be promoted out of this source note

- [[Term-Structure Models]]

## Related notes

- [[Stochastic Calculus for Finance II]]
- [[Stochastic Calculus for Finance II - Ch 09 Change of Numeraire]]
- [[Term-Structure Models]]
- [[Change of Numeraire and Forward Measures]]
- [[Risk-Neutral Pricing and Fundamental Theorems of Asset Pricing]]

## Sources

- [[Stochastic Calculus for Finance II]]
- [[raw/math_statistics/Steven E. Shreve-Stochastic Calculus for Finance II_20150303200346.pdf]]
