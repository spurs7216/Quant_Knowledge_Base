---
title: Arbitrage Theory in Continuous Time
type: source
status: source_ingested
updated: 2026-04-22
tags:
  - source
  - mathematical-finance
  - continuous-time-finance
  - textbook
source_type: book
source_class: overview_source
read_scope: full_source
extraction_basis: toc_scan_plus_utf8_text_extraction_and_targeted_rendered_theorem_pages
technical_depth: theorem_oriented_selected_chapters
sources:
  - "[[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]"
---
# Arbitrage Theory in Continuous Time

## Citation / metadata

- Author: Tomas Bjork
- Title: *Arbitrage Theory in Continuous Time*
- Edition: Fourth edition
- Publisher: Oxford University Press
- Year: 2020
- Raw source: [[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]
- Scope actually ingested: all 38 main chapters plus appendices used as background support

## Why this book matters

This is the most structurally complete continuous-time finance source on the math/statistics shelf.

Shreve gives the cleaner first bridge into Brownian pricing machinery. Bjork then widens the frame: discrete-time arbitrage, stochastic calculus, martingale pricing, term-structure theory, incomplete markets, stochastic control, utility-based pricing, and equilibrium all sit inside one coherent no-arbitrage architecture.

For this vault, the book matters because it forces the research system to keep pricing, hedging, measure change, rates, optimization, and equilibrium theory connected rather than treating them as separate toolkits.

## Reading logic from the source

- Read the full source as one finance-theory spine rather than as isolated derivative chapters.
- Use Chapters 2 to 15 as the core no-arbitrage and martingale skeleton.
- Treat Chapters 19 to 24 as the rates branch where numeraires, forward measures, HJM, and LIBOR modeling become operational.
- Treat Chapters 25 to 34 as the control and incompleteness branch where replication breaks, preferences matter, and valuation becomes set- or utility-dependent.
- Treat Chapters 35 to 38 as the equilibrium branch that links stochastic discount factors, short rates, and asset prices back to economic primitives.

## Stage map

- `scan`: Chapters 1, 16, 17, 18, 35, 37
- `selective_deepen`: Chapters 2, 6, 9, 10, 13, 20, 24, 26, 32, 33, 34
- `deep`: Chapters 3, 4, 5, 7, 8, 11, 12, 14, 15, 19, 21, 22, 23, 25, 27, 28, 29, 30, 31, 36, 38

The stage map is intentionally uneven. Shreve already covered part of the Brownian pricing bridge, so Bjork is used here to strengthen the measure-theoretic, rates, incomplete-market, control, and equilibrium branches rather than merely duplicating introductory Black-Scholes exposition.

## Chapter shelf

- `scan`: [[Arbitrage Theory in Continuous Time - Ch 01 Introduction]]
- `selective_deepen`: [[Arbitrage Theory in Continuous Time - Ch 02 The Binomial Model]]
- `deep`: [[Arbitrage Theory in Continuous Time - Ch 03 A More General One Period Model]]
- `deep`: [[Arbitrage Theory in Continuous Time - Ch 04 Stochastic Integrals]]
- `deep`: [[Arbitrage Theory in Continuous Time - Ch 05 Stochastic Differential Equations]]
- `selective_deepen`: [[Arbitrage Theory in Continuous Time - Ch 06 Portfolio Dynamics]]
- `deep`: [[Arbitrage Theory in Continuous Time - Ch 07 Arbitrage Pricing]]
- `deep`: [[Arbitrage Theory in Continuous Time - Ch 08 Completeness and Hedging]]
- `selective_deepen`: [[Arbitrage Theory in Continuous Time - Ch 09 A Primer on Incomplete Markets]]
- `selective_deepen`: [[Arbitrage Theory in Continuous Time - Ch 10 Parity Relations and Delta Hedging]]
- `deep`: [[Arbitrage Theory in Continuous Time - Ch 11 The Martingale Approach to Arbitrage Theory]]
- `deep`: [[Arbitrage Theory in Continuous Time - Ch 12 The Mathematics of the Martingale Approach]]
- `selective_deepen`: [[Arbitrage Theory in Continuous Time - Ch 13 Black-Scholes from a Martingale Point of View]]
- `deep`: [[Arbitrage Theory in Continuous Time - Ch 14 Multidimensional Models Martingale Approach]]
- `deep`: [[Arbitrage Theory in Continuous Time - Ch 15 Change of Numeraire]]
- `scan`: [[Arbitrage Theory in Continuous Time - Ch 16 Dividends]]
- `scan`: [[Arbitrage Theory in Continuous Time - Ch 17 Forward and Futures Contracts]]
- `scan`: [[Arbitrage Theory in Continuous Time - Ch 18 Currency Derivatives]]
- `deep`: [[Arbitrage Theory in Continuous Time - Ch 19 Bonds and Interest Rates]]
- `selective_deepen`: [[Arbitrage Theory in Continuous Time - Ch 20 Short Rate Models]]
- `deep`: [[Arbitrage Theory in Continuous Time - Ch 21 Martingale Models for the Short Rate]]
- `deep`: [[Arbitrage Theory in Continuous Time - Ch 22 Forward Rate Models]]
- `deep`: [[Arbitrage Theory in Continuous Time - Ch 23 LIBOR Market Models]]
- `selective_deepen`: [[Arbitrage Theory in Continuous Time - Ch 24 Potentials and Positive Interest]]
- `deep`: [[Arbitrage Theory in Continuous Time - Ch 25 Stochastic Optimal Control]]
- `selective_deepen`: [[Arbitrage Theory in Continuous Time - Ch 26 Optimal Consumption and Investment]]
- `deep`: [[Arbitrage Theory in Continuous Time - Ch 27 The Martingale Approach to Optimal Investment]]
- `deep`: [[Arbitrage Theory in Continuous Time - Ch 28 Optimal Stopping Theory and American Options]]
- `deep`: [[Arbitrage Theory in Continuous Time - Ch 29 Incomplete Markets]]
- `deep`: [[Arbitrage Theory in Continuous Time - Ch 30 The Esscher Transform and the Minimal Martingale Measure]]
- `deep`: [[Arbitrage Theory in Continuous Time - Ch 31 Minimizing f-Divergence]]
- `selective_deepen`: [[Arbitrage Theory in Continuous Time - Ch 32 Portfolio Optimization in Incomplete Markets]]
- `selective_deepen`: [[Arbitrage Theory in Continuous Time - Ch 33 Utility Indifference Pricing and Other Topics]]
- `selective_deepen`: [[Arbitrage Theory in Continuous Time - Ch 34 Good Deal Bounds]]
- `scan`: [[Arbitrage Theory in Continuous Time - Ch 35 Equilibrium Theory A Simple Production Model]]
- `deep`: [[Arbitrage Theory in Continuous Time - Ch 36 The Cox-Ingersoll-Ross Factor Model]]
- `scan`: [[Arbitrage Theory in Continuous Time - Ch 37 The Cox-Ingersoll-Ross Interest Rate Model]]
- `deep`: [[Arbitrage Theory in Continuous Time - Ch 38 Endowment Equilibrium Unit Net Supply]]

## Core objects and modeling vocabulary

- numeraire and normalized prices
- self-financing portfolios and cumulative dividend processes
- equivalent martingale measures and local martingale measures
- stochastic discount factors and state-price densities
- completeness, incompleteness, and attainable claims
- Girsanov kernels and likelihood processes
- short rates, forward rates, zero-coupon bonds, and affine term structures
- HJM drift restriction and forward-measure pricing
- LIBOR market models and Black caplet formulas
- Bellman principle, HJB equations, and verification arguments
- Snell envelopes, stopping regions, and variational inequalities
- Esscher transforms, minimal martingale measures, and divergence-based measure selection
- equilibrium short rates, equilibrium risk premia, and marginal-utility discount factors

## Main themes

- no-arbitrage pricing is a structural restriction on the whole market, not only an option-pricing trick
- measure change is useful because it preserves pricing structure while simplifying dynamics
- completeness is a rank and filtration question, not a synonym for continuous time
- rates modeling is about enforcing no-arbitrage across the whole curve, not fitting one yield
- once markets are incomplete, valuation depends on measure choice, optimization criteria, or equilibrium restrictions
- stochastic control and dual martingale methods are two linked ways to solve dynamic investment problems
- stochastic discount factors are the common thread between no-arbitrage finance and equilibrium finance

## Promoted durable notes

- [[Risk-Neutral Pricing and Fundamental Theorems of Asset Pricing]]
- [[Change of Numeraire and Forward Measures]]
- [[Term-Structure Models]]
- [[American Options and Optimal Stopping]]
- [[Stochastic Discount Factors]]
- [[Market Completeness and Incomplete Markets]]
- [[Heath-Jarrow-Morton Drift Condition]]
- [[LIBOR Market Models]]
- [[Stochastic Optimal Control and Hamilton-Jacobi-Bellman Equation]]
- [[Martingale Methods for Portfolio Optimization]]
- [[Esscher Transform and Minimal Martingale Measure]]
- [[Utility Indifference Pricing]]
- [[Good Deal Bounds]]
- [[Dynamic Equilibrium Asset Pricing]]

## Next promotion targets

- dividend-adjusted equity and FX pricing as a reusable note between numeraires and carry
- affine term-structure modeling as its own durable branch rather than a subsection inside the rates note
- mutual fund theorems and portfolio separation under dynamic investment problems
- potentials and positive-interest constructions as a rates-specific note if fixed-income work expands
- equilibrium connections between marginal utility, the short rate, and the stochastic discount factor

## Caveats

- the book is mathematically mature and often states deep results before giving all technical proof machinery
- the measure-theoretic chapters are strong on pricing structure but not designed as implementation manuals
- some rates chapters are framework chapters rather than calibrated production workflows
- the equilibrium part is valuable for conceptual structure, but it is not a substitute for empirical asset-pricing work

## Related notes

- [[Stochastic Calculus for Finance II]]
- [[Stochastic Calculus]]
- [[Derivatives Markets]]
- [[Brownian Motion and Quadratic Variation]]
- [[Ito Calculus and Stochastic Differential Equations]]
- [[Risk-Neutral Pricing and Fundamental Theorems of Asset Pricing]]
- [[Change of Numeraire and Forward Measures]]
- [[Term-Structure Models]]
- [[Finance Map]]
- [[Math Map]]

## Sources

- [[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]

