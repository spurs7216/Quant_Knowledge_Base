---
title: Jump Processes and Compensators
type: concept
status: seed
updated: 2026-04-22
tags:
  - concept
  - probability
  - stochastic-calculus
  - jump-processes
  - compensators
domain: mathematics
sources:
  - "[[Stochastic Calculus for Finance II]]"
  - "[[Stochastic Calculus for Finance II - Ch 11 Introduction to Jump Processes]]"
---
# Jump Processes and Compensators

## Summary

Jump processes extend diffusion models by allowing discontinuous moves. Their key structural object is the compensator: the predictable finite-variation term that must be removed so the residual process becomes a martingale.

## Core definitions

For a Poisson process with intensity $\lambda$,
$$\mathbb{E}[N(t)-N(s)]=\lambda(t-s), \qquad \operatorname{Var}[N(t)-N(s)]=\lambda(t-s).$$

The compensated Poisson process is
$$M(t)=N(t)-\lambda t.$$

For a jump process $X$, the Ito-Doeblin formula becomes
$$f(X(t))=f(X(0))+\int_0^t f'(X(s))\,dX^c(s)+\frac{1}{2}\int_0^t f''(X(s))\,d[X^c,X^c](s)+\sum_{0<s\le t}\bracket{f(X(s))-f(X(s-))}.$$

## Load-bearing implications

### 1. Center the jump arrivals with the compensator

For Poisson arrivals, subtracting $\lambda t$ gives the martingale
$$M(t)=N(t)-\lambda t.$$

This is the jump analogue of removing drift from a diffusion.

### 2. Jumps add a discrete correction to calculus

The jump sum
$$\sum_{0<s\le t}\bracket{f(X(s))-f(X(s-))}$$
is what diffusion Ito calculus is missing.

### 3. Measure changes can alter intensity and jump law

For Poisson measure change, Shreve uses
$$Z(t)=e^{(\lambda-\tilde{\lambda})t}\paren{\frac{\tilde{\lambda}}{\lambda}}^{N(t)},$$
which changes the jump intensity from $\lambda$ to $\tilde{\lambda}$.

So in jump models, "risk-neutralization" can move arrival rates, not only drifts.

## Why this concept matters

Once markets react discontinuously to news, diffusion-only language becomes structurally incomplete. Compensators are the right way to keep martingale methods alive in that environment.

## Failure modes

- forcing diffusion intuition onto discontinuous paths
- ignoring left limits $X(t-)$ when the process jumps
- assuming a jump-model measure change only modifies drift
- assuming complete-market hedging still holds after adding jumps

## Quant relevance

This concept matters for:

- earnings jumps and event risk
- jump-diffusion models
- compensator-based martingale pricing
- stress scenarios with discontinuous price moves

## Related notes

- [[Brownian Motion and Quadratic Variation]]
- [[Ito Calculus and Stochastic Differential Equations]]
- [[Risk-Neutral Pricing and Fundamental Theorems of Asset Pricing]]
- [[Stochastic Calculus]]

## Sources

- [[Stochastic Calculus for Finance II]]
- [[Stochastic Calculus for Finance II - Ch 11 Introduction to Jump Processes]]
