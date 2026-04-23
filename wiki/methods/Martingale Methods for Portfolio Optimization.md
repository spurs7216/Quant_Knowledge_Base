---
title: Martingale Methods for Portfolio Optimization
type: method
status: seed
updated: 2026-04-22
tags:
  - method
  - quant-finance
  - portfolio-optimization
  - martingale-methods
domain: quant-finance
sources:
  - "[[Arbitrage Theory in Continuous Time]]"
  - "[[Arbitrage Theory in Continuous Time - Ch 27 The Martingale Approach to Optimal Investment]]"
  - "[[Stochastic Discount Factors]]"
---
# Martingale Methods for Portfolio Optimization

## Summary

Martingale methods solve dynamic investment problems by shifting from direct control of portfolio weights to optimization over terminal wealth subject to a pricing-kernel budget constraint.

## Core equations

Let $I=(U')^{-1}$. In a complete market, the optimal terminal wealth is
$$
\widehat{X}_T=I(\lambda M_T),
$$
where $M_T$ is the stochastic discount factor and $\lambda$ is chosen to satisfy the budget constraint.

The optimal wealth process is then
$$
\widehat{X}_t=\E^P\bracket{\frac{M_T}{M_t}\widehat{X}_T\given\mathcal{F}_t}.
$$

## Main logic

- write feasibility through the pricing kernel rather than through direct controls
- solve the static Lagrangian pointwise in terminal wealth
- price the optimal terminal claim back to earlier times
- recover the dynamic portfolio from the resulting wealth process

## Failure modes

- using the complete-market formula in incomplete markets without extra dual machinery
- forgetting that the multiplier $\lambda$ is pinned down by wealth feasibility
- treating the method as if it were separate from HJB when the two are dual views of the same problem

## Related notes

- [[Stochastic Optimal Control and Hamilton-Jacobi-Bellman Equation]]
- [[Stochastic Discount Factors]]
- [[Utility Indifference Pricing]]

## Sources

- [[Arbitrage Theory in Continuous Time]]
- [[Arbitrage Theory in Continuous Time - Ch 27 The Martingale Approach to Optimal Investment]]
- [[Stochastic Discount Factors]]

