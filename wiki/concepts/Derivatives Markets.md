---
title: Derivatives Markets
type: market
status: seeded
updated: 2026-04-18
tags:
  - market
  - derivatives
  - options
  - futures
source_count: 1
sources:
  - "[[raw/finance_microstructure/Options, Futures, and Other Derivatives.pdf]]"
---
# Derivatives Markets

## Summary

Derivatives markets are organized around contracts whose value depends on an underlying asset, rate, spread, or event. The core contract families are forwards, futures, options, and swaps, and the practical questions are market structure, pricing, hedging, risk measurement, and model choice.

## Market Structure

- exchange-traded contracts emphasize standardization, margining, and central clearing
- over-the-counter contracts emphasize customization but introduce counterparty and valuation complexity
- trader roles usually separate into hedgers, speculators, and arbitrageurs

## Source Synthesis

- Early Hull chapters emphasize that contract specification, margining, delivery, and trader objectives are part of the model, not only market background.
- The rates and carry chapters show that forward pricing, discounting, and term-structure assumptions are foundational across many derivative families.
- The options chapters turn payoff geometry into pricing, hedging, and sensitivity management through trees, Itô calculus, Black-Scholes-Merton, and Greeks.
- The volatility and numerical chapters show that realistic pricing quickly becomes a surface-calibration and computation problem rather than a closed-form formula problem.
- The credit, rate, commodity, and real-option chapters generalize the same logic to different underlyings and risk sources.
- The closing mishaps chapter makes governance, control, and misuse part of derivatives knowledge rather than an afterthought.

## Core Research Questions

- how the contract is priced relative to spot, carry, rates, and volatility
- how exposure should be hedged
- how liquidity, margining, and contract design affect behavior
- how model risk enters through volatility, term structure, and correlation assumptions
- how pricing assumptions break when the market is stressed, illiquid, or institutionally constrained

## Practical Layers

- `contract mechanics`: what is traded, how it settles, and what cash flows exist
- `pricing layer`: spot, carry, discounting, volatility, and arbitrage logic
- `risk layer`: Greeks, scenario sensitivity, VaR, expected shortfall, and credit exposure
- `governance layer`: collateral, CCP structure, funding, capital, and model-risk controls

## Why It Matters in This Vault

The derivatives layer connects directly to:

- [[option_forward_price]]
- [[option_volumne]]
- [[Treasurey_Daily_Time_Series]]
- [[Treasurey_Term_structure]]

It also provides the market context needed before treating option or Treasury fields as purely statistical features.

## Common Risks

- incorrect carry or discount-rate assumptions
- ignoring convexity and nonlinear payoff structure
- unstable volatility inputs
- mismatching contract-level and underlying-level data grains
- treating liquidity or execution frictions as negligible
- confusing benchmark curve data with instrument-level data
- using elegant pricing models without matching their assumptions to market convention or data quality

## Related Notes

- [[Hull Options Futures and Other Derivatives]]
- [[option_forward_price]]
- [[option_volumne]]
- [[risk_free_rate]]
- [[Treasurey_Daily_Time_Series]]
- [[Treasurey_Term_structure]]

## Sources

- [[raw/finance_microstructure/Options, Futures, and Other Derivatives.pdf]]
