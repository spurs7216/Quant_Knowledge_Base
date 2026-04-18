---
title: Hull Options Futures and Other Derivatives
type: source
status: chapter_ingested
updated: 2026-04-18
tags:
  - source
  - derivatives
  - textbook
  - risk
sources:
  - "[[raw/finance_microstructure/Options, Futures, and Other Derivatives.pdf]]"
---
# Hull Options Futures and Other Derivatives

## Summary

This is a broad derivatives textbook covering market structure, contract mechanics, pricing, risk management, and advanced interest-rate and credit topics. It spans the path from the basics of forwards, futures, and options to Black-Scholes-Merton, volatility surfaces, numerical procedures, value at risk, credit derivatives, and short-rate or forward-rate modeling.

## Chapter-by-Chapter Ingest

- `Chapter 1. Introduction`: establishes the basic contract families, venues, trader roles, and the operational vocabulary of hedging, speculation, and arbitrage.
- `Chapter 2. Futures markets and central counterparties`: moves from contract definition into clearing, margining, delivery, and the institutional mechanics of futures markets.
- `Chapter 3. Hedging strategies using futures`: treats hedging as an implementation problem with basis risk, cross hedging, and stock-index applications.
- `Chapter 4. Interest rates`: builds the term-structure foundation needed for discounting, forwards, and fixed-income derivatives.
- `Chapter 5. Determination of forward and futures prices`: ties arbitrage pricing to carry, income, yields, and delivery options.
- `Chapter 6. Interest rate futures`: applies the futures framework specifically to Treasury, Eurodollar, and SOFR contracts plus duration-based hedging.
- `Chapter 7. Swaps`: develops swaps as practical interest-rate and currency risk-transfer instruments and introduces valuation and credit-risk concerns.
- `Chapter 8. Securitization and the financial crisis of 2007-8`: uses securitization to connect derivatives machinery to systemic failure and incentive breakdown.
- `Chapter 9. XVAs`: extends pricing into funding, margin, and capital adjustments that matter in real dealer books.
- `Chapter 10. Mechanics of options markets`: shifts from futures to the market details of options trading and settlement.
- `Chapter 11. Properties of stock options`: builds the payoff geometry and arbitrage relations that later pricing models rely on.
- `Chapter 12. Trading strategies involving options`: treats option portfolios as exposure design tools rather than standalone contracts.
- `Chapter 13. Binomial trees`: introduces discrete-time valuation as the workhorse bridge between intuition and continuous-time pricing.
- `Chapter 14. Wiener processes and Itô's lemma`: supplies the stochastic-process foundation for continuous-time derivative pricing.
- `Chapter 15. The Black-Scholes-Merton model`: gives the canonical closed-form pricing framework and its assumptions.
- `Chapter 16. Employee stock options`: shows how institutional features and incentives distort plain-vanilla option intuition.
- `Chapter 17. Options on stock indices and currencies`: adapts option pricing to broader underlyings and market conventions.
- `Chapter 18. Futures options and Black's model`: connects futures underlyings to option valuation and the Black framework.
- `Chapter 19. The Greek letters`: turns pricing into risk management by decomposing sensitivities.
- `Chapter 20. Volatility smiles and volatility surfaces`: moves from constant-volatility theory to the market's actual implied-volatility structure.
- `Chapter 21. Basic numerical procedures`: introduces computational techniques for pricing problems without clean closed forms.
- `Chapter 22. Value at risk and expected shortfall`: shifts from contract pricing to portfolio risk measurement.
- `Chapter 23. Estimating volatilities and correlations`: addresses parameter estimation, which is often where model usefulness breaks down.
- `Chapter 24. Credit risk`: builds the probability-of-default and loss framework behind credit-sensitive pricing.
- `Chapter 25. Credit derivatives`: applies the credit framework to tradable transfer of credit exposure.
- `Chapter 26. Exotic options`: expands valuation logic to path dependence, barriers, and other nonstandard payoff structures.
- `Chapter 27. More on models and numerical procedures`: deepens the computational and modeling toolkit needed for harder derivative problems.
- `Chapter 28. Martingales and measures`: gives the measure-theoretic foundation for risk-neutral valuation.
- `Chapter 29. Interest rate derivatives: The standard market models`: develops market-standard pricing for caps, floors, swaptions, and related rate products.
- `Chapter 30. Convexity, timing, and quanto adjustments`: shows how small modeling details create meaningful pricing corrections.
- `Chapter 31. Equilibrium models of the short rate`: treats short-rate dynamics from an equilibrium perspective.
- `Chapter 32. No-arbitrage models of the short rate`: reframes short-rate modeling through calibration and arbitrage consistency.
- `Chapter 33. Modeling forward rates`: shifts modeling focus from short rates to the forward-rate curve itself.
- `Chapter 34. Swaps revisited`: expands the swap family into compounding, equity, nonstandard, and option-embedded structures.
- `Chapter 35. Energy and commodity derivatives`: adapts derivatives logic to physical commodity and weather-linked markets.
- `Chapter 36. Real options`: reuses option logic for corporate investment and project valuation.
- `Chapter 37. Derivatives mishaps and what we can learn from them`: closes with failure analysis, emphasizing governance, controls, and misuse.

## Key Claims

- Derivatives understanding requires both institutional market knowledge and quantitative pricing tools.
- Core concepts such as hedging, arbitrage, forward pricing, and risk-neutral reasoning connect the early and late chapters.
- Interest-rate structure and term-structure modeling matter because many derivative prices depend on discounting and curve assumptions.
- Greeks, volatility surfaces, and numerical methods are central operational tools once simple closed forms stop being enough.

## Methods and Data

The extracted contents show a progression from market mechanics to pricing theory and then to risk and model extensions. Covered areas include:

- futures markets and hedging
- interest rates and swaps
- options, binomial trees, Itô's lemma, and Black-Scholes-Merton
- Greeks and volatility smiles
- VaR and expected shortfall
- credit derivatives
- short-rate and forward-rate models
- energy, commodity, and real options

## Why It Matters Here

This source is the most direct foundation in the current `raw/finance_microstructure/` shelf for:

- understanding the options-family datasets
- interpreting Treasury and rate inputs
- reasoning about hedging, convexity, and model risk

## Reflection

For this vault, the book matters less as a single pricing manual and more as a scaffold: markets, rates, forwards, options, Greeks, volatility, rates, credit, and failure analysis all connect directly to the dataset families already mirrored in `catalog/`.

## Caveats

- Despite the folder name `finance_microstructure`, the book is broader than microstructure alone; it is a derivatives and risk text.

## Related Notes

- [[Derivatives Markets]]
- [[option_forward_price]]
- [[option_volumne]]
- [[Treasurey_Daily_Time_Series]]
- [[Treasurey_Term_structure]]

## Sources

- [[raw/finance_microstructure/Options, Futures, and Other Derivatives.pdf]]
