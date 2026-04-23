---
title: American Options and Optimal Stopping
type: method
status: seed
updated: 2026-04-22
tags:
  - method
  - quant-finance
  - american-options
  - optimal-stopping
domain: quant-finance
sources:
  - "[[Stochastic Calculus for Finance II]]"
  - "[[Stochastic Calculus for Finance II - Ch 08 American Derivative Securities]]"
  - "[[Arbitrage Theory in Continuous Time - Ch 28 Optimal Stopping Theory and American Options]]"
---
# American Options and Optimal Stopping

## Summary

American-option pricing is a stopping-time problem, not only a replication problem. The option holder chooses when to exercise, so the value is the supremum of discounted payoff over admissible stopping times, and the resulting price solves a complementarity or free-boundary problem.

## Core equations

A stopping time $\tau$ satisfies
$$\set{\tau \le t}\in\mathcal{F}(t), \qquad t \ge 0.$$

In discrete time, the Snell-envelope recursion is
$$V_n=\max\bracket{Z_n,\E[V_{n+1}\given\mathcal{F}_n]}.$$

For an American put expiring at $T$,
$$v(t,x)=\max_{\tau \in \mathcal{T}_{t,T}}\widetilde{\mathbb{E}}\bracket{e^{-r(\tau-t)}\paren{K-S(\tau)}^+\given S(t)=x}.$$

The finite-expiration put price satisfies the complementarity conditions
$$v(t,x)\ge (K-x)^+,$$
$$rv-v_t-rxv_x-\frac{1}{2}\sigma^2x^2v_{xx}\ge 0,$$
with equality in one of the two relations at each $(t,x)$.

## Main logic

### 1. Admissible exercise rules must be stopping times

The holder may use current information, not future information. That filtration constraint is part of the pricing problem itself.

### 2. The value is a supremum over exercise times

American pricing is a dynamic optimization problem under the pricing measure.

### 3. The state space splits into stopping and continuation regions

Inside the continuation set, the price solves the pricing PDE. Inside the stopping set, the value equals immediate exercise payoff.

### 4. Carry determines whether early exercise is rational

For a non-dividend-paying stock, early exercise of a call is not optimal. With dividends or carry, that conclusion can change.

## Workflow

1. Specify the filtration and admissible stopping-time set.
2. Write the discounted-payoff supremum.
3. Derive the associated complementarity system or free-boundary problem.
4. Compute the exercise boundary or approximate it numerically.
5. Check whether economic carry conditions imply trivial or nontrivial early exercise.

## Failure modes

- treating American options as European options plus an arbitrary premium
- using a heuristic exercise rule without verifying stopping-time admissibility
- ignoring the free-boundary structure and solving only the continuation PDE
- transferring no-dividend call intuition to dividend-paying assets

## Quant relevance

This method matters for:

- equity options with dividends
- callable or cancelable structured products
- optimal stopping problems under diffusion models
- Longstaff-Schwartz and related Monte Carlo exercise methods

## Related notes

- [[Risk-Neutral Pricing and Fundamental Theorems of Asset Pricing]]
- [[Change of Numeraire and Forward Measures]]
- [[Derivatives Markets]]
- [[Monte Carlo Methods]]

## Sources

- [[Stochastic Calculus for Finance II]]
- [[Stochastic Calculus for Finance II - Ch 08 American Derivative Securities]]
- [[Arbitrage Theory in Continuous Time - Ch 28 Optimal Stopping Theory and American Options]]
