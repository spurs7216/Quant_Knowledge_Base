---
title: Risk-Neutral Pricing and Fundamental Theorems of Asset Pricing
type: method
status: seed
updated: 2026-04-22
tags:
  - method
  - quant-finance
  - risk-neutral-pricing
  - asset-pricing
domain: quant-finance
sources:
  - "[[Stochastic Calculus for Finance II]]"
  - "[[Stochastic Calculus for Finance II - Ch 05 Risk-Neutral Pricing]]"
  - "[[Stochastic Calculus for Finance II - Ch 06 Connections with Partial Differential Equations]]"
  - "[[Arbitrage Theory in Continuous Time - Ch 11 The Martingale Approach to Arbitrage Theory]]"
  - "[[Arbitrage Theory in Continuous Time - Ch 12 The Mathematics of the Martingale Approach]]"
  - "[[Arbitrage Theory in Continuous Time - Ch 14 Multidimensional Models Martingale Approach]]"
---
# Risk-Neutral Pricing and Fundamental Theorems of Asset Pricing

## Summary

Risk-neutral pricing is the valuation method that replaces actual expected returns with martingale pricing under a measure tied to a numeraire. The fundamental theorems explain when this procedure is valid and when the resulting prices are unique.

## Core equations

If
$$Z=\frac{d\widetilde{\mathbb{P}}}{d\mathbb{P}},$$
then
$$\widetilde{\mathbb{E}}X=\mathbb{E}[XZ].$$

In Brownian models, the density process often takes the Girsanov form
$$Z(t)=\exp\bracket{-\int_0^t \theta(u)\,dW(u)-\frac{1}{2}\int_0^t \theta^2(u)\,du},$$
and under the new measure
$$\widetilde{W}(t)=W(t)+\int_0^t \theta(u)\,du$$
is Brownian motion.

For payoff $V(T)$ and money-market discount factor $D(t)$,
$$V(t)=\frac{1}{D(t)}\widetilde{\mathbb{E}}\bracket{D(T)V(T)\given\mathcal{F}(t)}.$$

## Core logic

### 1. Reweight the world so discounted traded assets are martingales

The point is not to predict prices under $\widetilde{\mathbb{P}}$. The point is to value claims consistently with no arbitrage.

### 2. Hedging comes from martingale representation

The pricing formula alone is not enough. The hedge exists because the discounted claim value can be represented as a stochastic integral with respect to the traded-noise sources.

### 3. Existence gives no-arbitrage, uniqueness gives completeness

The practical translation of the fundamental theorems is:

- at least one equivalent martingale measure means no arbitrage
- exactly one equivalent martingale measure in the model means unique hedge prices

### 4. Stochastic discount factors are the dual pricing language

The same arbitrage-free pricing system can be written through an equivalent martingale measure or through a stochastic discount factor. The two views differ in interpretation, not in pricing content.

### 5. PDE pricing and expectation pricing are the same method in different clothes

Feynman-Kac converts the risk-neutral expectation representation into the associated pricing PDE.

## When this method is the right tool

- the problem is valuation of a traded contingent claim
- the numeraire is clear
- the model is strong enough to define an equivalent martingale measure

## Failure modes

- using the risk-neutral measure for forecasting
- ignoring incompleteness and then claiming uniqueness of price
- forgetting that the numeraire choice changes the martingale measure
- treating discounted martingale arguments as valid when trading constraints or frictions break replication

## Quant relevance

This method matters for:

- option and rates pricing
- hedge design
- valuation adjustments across numeraires
- understanding when a model price is a theorem and when it is a convention

## Related notes

- [[Ito Calculus and Stochastic Differential Equations]]
- [[Change of Numeraire and Forward Measures]]
- [[American Options and Optimal Stopping]]
- [[Term-Structure Models]]
- [[Derivatives Markets]]

## Sources

- [[Stochastic Calculus for Finance II]]
- [[Stochastic Calculus for Finance II - Ch 05 Risk-Neutral Pricing]]
- [[Stochastic Calculus for Finance II - Ch 06 Connections with Partial Differential Equations]]
- [[Arbitrage Theory in Continuous Time - Ch 11 The Martingale Approach to Arbitrage Theory]]
- [[Arbitrage Theory in Continuous Time - Ch 12 The Mathematics of the Martingale Approach]]
- [[Arbitrage Theory in Continuous Time - Ch 14 Multidimensional Models Martingale Approach]]
