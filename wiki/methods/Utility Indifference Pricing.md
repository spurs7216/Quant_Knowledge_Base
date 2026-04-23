---
title: Utility Indifference Pricing
type: method
status: seed
updated: 2026-04-22
tags:
  - method
  - quant-finance
  - incomplete-markets
  - utility-pricing
domain: quant-finance
sources:
  - "[[Arbitrage Theory in Continuous Time]]"
  - "[[Arbitrage Theory in Continuous Time - Ch 31 Minimizing f-Divergence]]"
  - "[[Arbitrage Theory in Continuous Time - Ch 33 Utility Indifference Pricing and Other Topics]]"
---
# Utility Indifference Pricing

## Summary

Utility indifference pricing values a claim by the cash amount that makes an investor indifferent, in expected utility terms, between holding and not holding the claim. It is a preference-based pricing rule for incomplete markets.

## Core equations

If $H$ is the claim and $p$ the indifference price, then $p$ is defined implicitly by
$$
\sup_\pi \E[U(X_T^\pi+H-p)]
=
\sup_\pi \E[U(X_T^\pi)].
$$

Marginal indifference prices arise by linearizing this equality around a small position size.

## Main logic

- the market does not pin down a unique price
- investor preferences and endowment exposure complete the pricing problem
- the resulting price is inventory- and utility-dependent

## Failure modes

- treating the indifference price as universal across investors
- forgetting that the price depends on endowment, utility, and admissible strategy sets

## Related notes

- [[Martingale Methods for Portfolio Optimization]]
- [[Esscher Transform and Minimal Martingale Measure]]
- [[Good Deal Bounds]]
- [[Market Completeness and Incomplete Markets]]

## Sources

- [[Arbitrage Theory in Continuous Time]]
- [[Arbitrage Theory in Continuous Time - Ch 31 Minimizing f-Divergence]]
- [[Arbitrage Theory in Continuous Time - Ch 33 Utility Indifference Pricing and Other Topics]]

