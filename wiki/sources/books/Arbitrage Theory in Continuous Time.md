---
title: Arbitrage Theory in Continuous Time
type: source
status: chapter_ingested
updated: 2026-04-18
tags:
  - source
  - mathematical-finance
  - stochastic-calculus
  - textbook
sources:
  - "[[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]"
---
# Arbitrage Theory in Continuous Time

## Summary

Björk's text is a comprehensive mathematical-finance book that moves from discrete-time pricing intuition into stochastic calculus, martingale pricing, interest-rate modeling, incomplete markets, optimal control, and equilibrium theory. It is one of the cleanest bridges in the raw shelf from derivative pricing to deeper asset-pricing mathematics.

## Chapter-by-Chapter Ingest

- `Chapter 1. Introduction`: frames arbitrage pricing as the central organizing idea.
- `Chapter 2. The Binomial Model`: starts from the simplest complete-market pricing model.
- `Chapter 3. A More General One Period Model`: extends no-arbitrage logic beyond the textbook binomial tree.
- `Chapter 4. Stochastic Integrals`: introduces the integration machinery needed for continuous-time trading.
- `Chapter 5. Stochastic Differential Equations`: develops dynamic state evolution under stochastic shocks.
- `Chapter 6. Portfolio Dynamics`: formalizes self-financing trading in continuous time.
- `Chapter 7. Arbitrage Pricing`: states the no-arbitrage pricing logic in continuous models.
- `Chapter 8. Completeness and Hedging`: studies when replication is possible and what hedging means.
- `Chapter 9. A Primer on Incomplete Markets`: introduces pricing and hedging when exact replication fails.
- `Chapter 10. Parity Relations and Delta Hedging`: connects static arbitrage relations with dynamic hedge construction.
- `Chapter 11. The Martingale Approach to Arbitrage Theory`: reframes pricing around equivalent martingale measures.
- `Chapter 12. The Mathematics of the Martingale Approach`: deepens the measure-theoretic support behind martingale pricing.
- `Chapter 13. Black-Scholes from a Martingale Point of View`: re-derives the canonical model through the martingale lens.
- `Chapter 14. Multidimensional Models: Martingale Approach`: extends pricing machinery to multi-asset settings.
- `Chapter 15. Change of Numeraire`: shows how pricing simplifications arise from changing the benchmark asset.
- `Chapter 16. Dividends`: integrates payout structure into pricing and hedging.
- `Chapter 17. Forward and Futures Contracts`: treats linear derivative claims and carry relations.
- `Chapter 18. Currency Derivatives`: extends no-arbitrage logic into FX settings.
- `Chapter 19. Bonds and Interest Rates`: begins the fixed-income term-structure layer.
- `Chapter 20. Short Rate Models`: models the short rate as the primitive state variable.
- `Chapter 21. Martingale Models for the Short Rate`: brings martingale methods into short-rate pricing.
- `Chapter 22. Forward Rate Models`: moves from short-rate to forward-rate dynamics.
- `Chapter 23. LIBOR Market Models`: studies market-model style interest-rate dynamics.
- `Chapter 24. Potentials and Positive Interest`: handles positivity and structural constraints in rates models.
- `Chapter 25. Stochastic Optimal Control`: introduces dynamic optimization under uncertainty.
- `Chapter 26. Optimal Consumption and Investment`: studies dynamic portfolio choice.
- `Chapter 27. The Martingale Approach to Optimal Investment`: solves investment problems through dual martingale methods.
- `Chapter 28. Optimal Stopping Theory and American Options`: treats early exercise as an optimal stopping problem.
- `Chapter 29. Incomplete Markets`: revisits incompleteness in a fuller pricing-and-hedging setting.
- `Chapter 30. The Esscher Transform and the Minimal Martingale Measure`: studies alternative pricing transforms in incomplete settings.
- `Chapter 31. Minimizing f-Divergence`: introduces divergence criteria for measure selection.
- `Chapter 32. Portfolio Optimization in Incomplete Markets`: links market incompleteness with portfolio choice.
- `Chapter 33. Utility Indifference Pricing and Other Topics`: prices claims through investor preferences rather than pure replication.
- `Chapter 34. Good Deal Bounds`: studies valuation bounds that exclude deals that are too good to be plausible.
- `Chapter 35. Equilibrium Theory: A Simple Production Model`: moves from pricing to equilibrium asset allocation.
- `Chapter 36. The Cox-Ingersoll-Ross Factor Model`: embeds equilibrium structure in a tractable factor setting.
- `Chapter 37. The Cox-Ingersoll-Ross Interest Rate Model`: connects equilibrium logic with term-structure modeling.
- `Chapter 38. Endowment Equilibrium: Unit Net Supply`: closes with a fuller equilibrium perspective.

## Key Claims

- No-arbitrage pricing is best understood through martingales, numeraires, and market completeness.
- Continuous-time finance becomes coherent only when pricing, hedging, optimization, and equilibrium are studied together.
- Incomplete markets are not edge cases; they require their own pricing logic rather than naive replication analogies.

## Methods and Data

- stochastic integrals and stochastic differential equations
- martingale pricing and change of measure
- term-structure and LIBOR market models
- optimal control, optimal stopping, and utility-based pricing
- incomplete-market valuation and equilibrium theory

## Why It Matters Here

This is one of the most mathematically important books in the vault. It supports future notes on derivatives, fixed income, portfolio choice, market completeness, and the theoretical limits of hedging.

## Reflection

The real strength of Björk is structural clarity. The book does not treat derivatives, interest rates, optimization, and equilibrium as disconnected silos, which makes it especially valuable for a professional quant knowledge base.

## Caveats

- The text assumes significant mathematical maturity.
- It is theory-heavy and should be paired with implementation notes when moving toward production research.

## Related Notes

- [[Derivatives Markets]]
- [[Monte Carlo Methods]]
- [[Portfolio Construction]]
- [[Math Map]]

## Sources

- [[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]
