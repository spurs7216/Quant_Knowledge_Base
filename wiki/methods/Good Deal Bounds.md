---
title: Good Deal Bounds
type: method
status: seed
updated: 2026-04-22
tags:
  - method
  - quant-finance
  - incomplete-markets
  - valuation-bounds
domain: quant-finance
sources:
  - "[[Arbitrage Theory in Continuous Time]]"
  - "[[Arbitrage Theory in Continuous Time - Ch 34 Good Deal Bounds]]"
---
# Good Deal Bounds

## Summary

Good deal bounds tighten the wide arbitrage-free price interval in incomplete markets by excluding martingale measures that imply deals considered implausibly favorable.

## Main logic

- no-arbitrage gives a feasible price set
- an extra performance or acceptability restriction shrinks that set
- the resulting lower and upper prices are not theorems of arbitrage alone; they are constrained valuation bounds

## Why it matters

- it is weaker than full utility-based pricing
- it is stronger than pure no-arbitrage intervals
- it is useful when one wants disciplined bounds under basis risk or model incompleteness

## Failure modes

- confusing good-deal bounds with exact prices
- forgetting that the result depends on the chosen notion of "too good"

## Related notes

- [[Utility Indifference Pricing]]
- [[Esscher Transform and Minimal Martingale Measure]]
- [[Market Completeness and Incomplete Markets]]

## Sources

- [[Arbitrage Theory in Continuous Time]]
- [[Arbitrage Theory in Continuous Time - Ch 34 Good Deal Bounds]]
