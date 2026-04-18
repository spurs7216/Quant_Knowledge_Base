---
title: Stochastic Calculus
type: method
status: seed
updated: 2026-04-18
tags:
  - method
  - stochastic-calculus
  - mathematical-finance
  - continuous-time
domain: quant-finance
sources:
  - "[[Stochastic Calculus for Finance II]]"
  - "[[Arbitrage Theory in Continuous Time]]"
  - "[[Hull Options Futures and Other Derivatives]]"
  - "[[Monte Carlo Methods in Financial Engineering]]"
---
# Stochastic Calculus

## Summary

Stochastic calculus is the continuous-time mathematical framework for modeling random paths, dynamic trading strategies, and derivative valuation under uncertainty. In quant finance it is the language behind diffusion models, risk-neutral pricing, hedging, term-structure models, and many state-dynamic portfolio problems.

## What It Does

Stochastic calculus gives the researcher a way to:

- model continuously evolving random systems
- define integration against Brownian motion and related processes
- derive dynamic equations for prices, states, and self-financing portfolios
- move between physical and risk-neutral measures
- connect probabilistic models with PDE-based pricing and control views

## Source Synthesis

- [[Stochastic Calculus for Finance II]] is the clearest direct route from probability and Brownian motion into pricing, PDEs, and term-structure models.
- [[Arbitrage Theory in Continuous Time]] broadens the framework into completeness, numeraire changes, optimal control, incomplete markets, and equilibrium.
- [[Hull Options Futures and Other Derivatives]] supplies intuition and market interpretation for the models.
- [[Monte Carlo Methods in Financial Engineering]] shows how continuous-time models become numerical estimators rather than only formal derivations.

## Assumptions

Any stochastic-calculus application needs clarity on:

- the filtration, or information flow, being modeled
- the path properties assumed for the state process
- whether dynamics are diffusive, jump-driven, or mixed
- whether the goal is descriptive modeling, pricing, hedging, or control
- whether the measure and numeraire choice matches the problem

## Workflow

1. Define the state variables and the information filtration.
2. Specify the continuous-time dynamics, including drift, diffusion, and jump terms if needed.
3. Decide whether the objective is pricing, hedging, risk measurement, or control.
4. Choose the relevant measure and numeraire framework.
5. Derive the dynamic equations for the claim, portfolio, or value function.
6. Translate the continuous-time result into a numerical method when closed forms are unavailable.
7. Check whether the model assumptions survive market microstructure, discrete trading, and calibration reality.

## Diagnostics

- confirm that the chosen dynamics match the economic object being modeled
- inspect whether hedging or pricing conclusions are measure-consistent
- compare diffusion-only conclusions against jump or incomplete-market alternatives
- test numerical implementations for discretization sensitivity
- inspect whether calibration is stable or only cosmetically accurate

## Failure Modes

- using continuous-time elegance to hide weak market assumptions
- confusing risk-neutral dynamics with real-world forecasting dynamics
- assuming replication where markets are effectively incomplete
- treating the PDE and martingale views as competing rather than complementary
- ignoring discrete trading, costs, and liquidity when drawing hedge conclusions

## Quant Use Cases

- derivative pricing and Greeks
- dynamic hedging and replication
- term-structure and rates modeling
- optimal execution or control problems
- jump-diffusion and incomplete-market valuation

## Related Notes

- [[Derivatives Markets]]
- [[Monte Carlo Methods]]
- [[Arbitrage Theory in Continuous Time]]
- [[Math Map]]

## Sources

- [[Stochastic Calculus for Finance II]]
- [[Arbitrage Theory in Continuous Time]]
- [[Hull Options Futures and Other Derivatives]]
- [[Monte Carlo Methods in Financial Engineering]]
