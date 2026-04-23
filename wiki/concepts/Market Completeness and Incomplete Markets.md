---
title: Market Completeness and Incomplete Markets
type: concept
status: seed
updated: 2026-04-22
tags:
  - concept
  - quant-finance
  - completeness
  - incomplete-markets
domain: quant-finance
sources:
  - "[[Arbitrage Theory in Continuous Time]]"
  - "[[Arbitrage Theory in Continuous Time - Ch 03 A More General One Period Model]]"
  - "[[Arbitrage Theory in Continuous Time - Ch 08 Completeness and Hedging]]"
  - "[[Arbitrage Theory in Continuous Time - Ch 09 A Primer on Incomplete Markets]]"
  - "[[Arbitrage Theory in Continuous Time - Ch 29 Incomplete Markets]]"
---
# Market Completeness and Incomplete Markets

## Summary

A market is complete when every admissible contingent claim can be replicated by trading existing assets. It is incomplete when some payoff risk is not spanned, so arbitrage-free prices are no longer unique.

## Core objects and definitions

In a complete market:

- every claim is attainable
- hedging can eliminate model-consistent residual risk
- the pricing functional is unique

In many diffusion models, completeness can be expressed as a rank condition on the volatility span:
$$
\operatorname{Im}(\sigma_t^\ast)=\mathbb{R}^N.
$$

In those settings, completeness is equivalent to uniqueness of the equivalent martingale measure.

## Why it matters

- uniqueness of price is a completeness claim, not only a no-arbitrage claim
- incomplete markets force a second decision layer: measure selection, utility pricing, or bounds
- many realistic quant problems involve unspanned state variables, basis risk, or trading constraints

## Failure modes

- assuming continuous-time models are automatically complete
- speaking about "the risk-neutral price" in incomplete models
- confusing numerical hedge error with structural incompleteness

## Related notes

- [[Risk-Neutral Pricing and Fundamental Theorems of Asset Pricing]]
- [[Stochastic Discount Factors]]
- [[Esscher Transform and Minimal Martingale Measure]]
- [[Utility Indifference Pricing]]
- [[Good Deal Bounds]]

## Sources

- [[Arbitrage Theory in Continuous Time]]
- [[Arbitrage Theory in Continuous Time - Ch 03 A More General One Period Model]]
- [[Arbitrage Theory in Continuous Time - Ch 08 Completeness and Hedging]]
- [[Arbitrage Theory in Continuous Time - Ch 09 A Primer on Incomplete Markets]]
- [[Arbitrage Theory in Continuous Time - Ch 29 Incomplete Markets]]

