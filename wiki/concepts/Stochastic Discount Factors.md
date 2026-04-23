---
title: Stochastic Discount Factors
type: concept
status: seed
updated: 2026-04-22
tags:
  - concept
  - quant-finance
  - stochastic-discount-factor
  - pricing-kernel
domain: quant-finance
sources:
  - "[[Arbitrage Theory in Continuous Time]]"
  - "[[Arbitrage Theory in Continuous Time - Ch 03 A More General One Period Model]]"
  - "[[Arbitrage Theory in Continuous Time - Ch 11 The Martingale Approach to Arbitrage Theory]]"
  - "[[Arbitrage Theory in Continuous Time - Ch 14 Multidimensional Models Martingale Approach]]"
  - "[[Arbitrage Theory in Continuous Time - Ch 36 The Cox-Ingersoll-Ross Factor Model]]"
  - "[[Arbitrage Theory in Continuous Time - Ch 38 Endowment Equilibrium Unit Net Supply]]"
---
# Stochastic Discount Factors

## Summary

A stochastic discount factor is a positive pricing-kernel process that prices payoffs by discounting states differently across time and uncertainty. It is the object that links no-arbitrage pricing, martingale measures, and equilibrium marginal utility.

## Core equations

For a payoff $X$ at time $T$,
$$
\Pi_t[X]=\E^P\bracket{\frac{M_T}{M_t}X\given\mathcal{F}_t}.
$$

If $L_t=dQ/dP|_{\mathcal{F}_t}$ and the money-market account is the numeraire, then a standard no-arbitrage SDF is
$$
M_t=e^{-\int_0^t r_u\,du}L_t.
$$

In equilibrium endowment models, the SDF can be written as a marginal-utility ratio:
$$
M_t=\frac{U_c(t,e_t)}{U_c(0,e_0)}.
$$

## Why it matters

- it is the dual object behind equivalent martingale measures
- it unifies arbitrage pricing and equilibrium pricing in one notation
- it makes clear which risk exposures are expensive in state-price terms

## Failure modes

- treating the SDF as unique in incomplete markets
- mixing equilibrium SDFs with purely no-arbitrage SDFs without stating the extra assumptions
- forgetting that the SDF depends on the numeraire and model structure

## Related notes

- [[Risk-Neutral Pricing and Fundamental Theorems of Asset Pricing]]
- [[Market Completeness and Incomplete Markets]]
- [[Dynamic Equilibrium Asset Pricing]]
- [[Change of Numeraire and Forward Measures]]

## Sources

- [[Arbitrage Theory in Continuous Time]]
- [[Arbitrage Theory in Continuous Time - Ch 03 A More General One Period Model]]
- [[Arbitrage Theory in Continuous Time - Ch 11 The Martingale Approach to Arbitrage Theory]]
- [[Arbitrage Theory in Continuous Time - Ch 14 Multidimensional Models Martingale Approach]]
- [[Arbitrage Theory in Continuous Time - Ch 36 The Cox-Ingersoll-Ross Factor Model]]
- [[Arbitrage Theory in Continuous Time - Ch 38 Endowment Equilibrium Unit Net Supply]]

