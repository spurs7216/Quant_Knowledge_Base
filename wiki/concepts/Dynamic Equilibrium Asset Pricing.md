---
title: Dynamic Equilibrium Asset Pricing
type: concept
status: seed
updated: 2026-04-22
tags:
  - concept
  - quant-finance
  - equilibrium
  - asset-pricing
domain: quant-finance
sources:
  - "[[Arbitrage Theory in Continuous Time]]"
  - "[[Arbitrage Theory in Continuous Time - Ch 35 Equilibrium Theory A Simple Production Model]]"
  - "[[Arbitrage Theory in Continuous Time - Ch 36 The Cox-Ingersoll-Ross Factor Model]]"
  - "[[Arbitrage Theory in Continuous Time - Ch 38 Endowment Equilibrium Unit Net Supply]]"
---
# Dynamic Equilibrium Asset Pricing

## Summary

Dynamic equilibrium asset pricing explains prices, rates, and risk premia from economic primitives such as utility, endowments, production, and market clearing rather than from no-arbitrage alone.

## Core equations

In endowment-style models, the equilibrium stochastic discount factor is
$$
M_t=\frac{U_c(t,e_t)}{U_c(0,e_0)}.
$$

The equilibrium short rate then becomes a function of utility curvature and endowment dynamics, and risk premia are implied by the same marginal-value structure.

## Why it matters

- it connects pricing kernels to economic primitives
- it explains why short rates and risk premia can be endogenous objects
- it gives a deeper interpretation of stochastic discount factors than pure martingale normalization

## Caveats

- equilibrium results are model-dependent and not automatically empirical truths
- the extra economic structure is a strength conceptually but also a source of misspecification risk

## Related notes

- [[Stochastic Discount Factors]]
- [[Stochastic Optimal Control and Hamilton-Jacobi-Bellman Equation]]
- [[Risk-Neutral Pricing and Fundamental Theorems of Asset Pricing]]

## Sources

- [[Arbitrage Theory in Continuous Time]]
- [[Arbitrage Theory in Continuous Time - Ch 35 Equilibrium Theory A Simple Production Model]]
- [[Arbitrage Theory in Continuous Time - Ch 36 The Cox-Ingersoll-Ross Factor Model]]
- [[Arbitrage Theory in Continuous Time - Ch 38 Endowment Equilibrium Unit Net Supply]]

