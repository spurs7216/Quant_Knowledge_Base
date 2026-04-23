---
title: Brownian Motion and Quadratic Variation
type: concept
status: seed
updated: 2026-04-22
tags:
  - concept
  - probability
  - stochastic-calculus
  - brownian-motion
  - quadratic-variation
domain: mathematics
sources:
  - "[[Stochastic Calculus for Finance II]]"
  - "[[Stochastic Calculus for Finance II - Ch 03 Brownian Motion]]"
---
# Brownian Motion and Quadratic Variation

## Summary

Brownian motion is the canonical continuous-time martingale noise. Its decisive structural feature is not only Gaussian increments. It is the path property
$$[W,W](t)=t,$$
which makes Brownian paths continuous but rough enough that ordinary calculus fails and Ito calculus becomes necessary.

## Core definitions

A process $W(t)$ is Brownian motion if:

- $W(0)=0$
- for $0=t_0<t_1<\cdots<t_m$, the increments are independent
- each increment satisfies
  $$W(t_{i+1})-W(t_i)\sim \mathcal{N}(0,t_{i+1}-t_i)$$

The quadratic variation of a function $f$ on $[0,T]$ is
$$[f,f](T)=\lim_{\norm{\Pi}\to 0}\sum_{j=0}^{n-1}\bracket{f(t_{j+1})-f(t_j)}^2.$$

For Brownian motion,
$$[W,W](T)=T.$$

## Load-bearing implications

### 1. Smooth paths have zero quadratic variation, Brownian paths do not

If $f$ has a continuous derivative, then
$$[f,f](T)=0.$$

So quadratic variation is the mathematical signal that Brownian paths are not differentiable in the ordinary sense.

### 2. The Ito correction comes from quadratic variation

Because $[W,W](t)=t$, the correct chain rule is
$$df(W(t))=f'(W(t))\,dW(t)+\frac{1}{2}f''(W(t))\,dt.$$

The extra drift term is not a modeling convention. It is forced by path geometry.

### 3. Brownian motion plus martingale plus quadratic variation is a characterization

Shreve uses Levy's theorem: if a continuous martingale $M$ starts at zero and satisfies
$$[M,M](t)=t,$$
then $M$ is Brownian motion.

So quadratic variation is not only descriptive. Together with the martingale property, it identifies the process.

### 4. Hitting-time and barrier logic come from reflection symmetry

Reflection-principle arguments translate barrier and maximum events into normal-tail calculations. That is why Brownian motion sits underneath barrier, lookback, and first-passage pricing.

## Why this concept matters

Brownian motion is the object that links probability, stochastic calculus, PDE pricing, and continuous-time hedging.

Without quadratic variation, continuous-time models would reduce to ordinary differential equations with random coefficients. With it, the entire Ito framework becomes necessary.

## Failure modes

- equating Brownian motion with generic Gaussian noise
- forgetting that the increments, not the levels, are independent
- using smooth-path intuition where quadratic variation is nonzero
- treating passage-time formulas as robust to jumps or discrete monitoring

## Quant relevance

This concept matters for:

- diffusion models for asset prices and state variables
- option-pricing Greeks and hedging
- Monte Carlo path simulation
- barrier, lookback, and first-passage logic

## Related notes

- [[Ito Calculus and Stochastic Differential Equations]]
- [[Diffusion Processes]]
- [[Stochastic Calculus]]
- [[Jump Processes and Compensators]]

## Sources

- [[Stochastic Calculus for Finance II]]
- [[Stochastic Calculus for Finance II - Ch 03 Brownian Motion]]
