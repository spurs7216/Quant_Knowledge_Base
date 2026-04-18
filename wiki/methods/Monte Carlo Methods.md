---
title: Monte Carlo Methods
type: method
status: seed
updated: 2026-04-18
tags:
  - method
  - monte-carlo
  - numerical-methods
domain: quant-finance
sources:
  - "[[Monte Carlo Methods in Financial Engineering]]"
  - "[[Implementing Models in Quantitative Finance]]"
  - "[[Tools for Computational Finance]]"
  - "[[Murphy Probabilistic Machine Learning]]"
---
# Monte Carlo Methods

## Summary

Monte Carlo methods estimate quantities by stochastic simulation. In this vault they matter in two distinct but related ways: numerical finance uses them for pricing, Greeks, and risk; probabilistic ML uses them for inference, posterior approximation, and sequential uncertainty.

## Source Synthesis

- [[Monte Carlo Methods in Financial Engineering]] gives the cleanest finance-first simulation treatment.
- [[Implementing Models in Quantitative Finance]] broadens Monte Carlo into dynamic programming, American options, and jump-diffusion case studies.
- [[Tools for Computational Finance]] places Monte Carlo beside PDE and finite-element methods.
- [[Murphy Probabilistic Machine Learning]] extends Monte Carlo into inference, MCMC, and sequential Monte Carlo.

## What It Does

- approximates expectations
- simulates path-dependent systems
- estimates sensitivities and risk metrics
- supports posterior inference when exact computation is impossible

## Core Design Choices

- sampling mechanism
- path discretization
- variance reduction
- quasi-Monte Carlo or low-discrepancy methods
- estimator choice for sensitivities or tail metrics

## Quant Use Cases

- derivative pricing
- American-option and optimal-stopping approximations
- scenario generation
- VaR / expected shortfall estimation
- Bayesian or latent-state inference

## Failure Modes

- bad discretization overwhelming the estimator
- too few paths for tail quantities
- unstable Greeks estimators
- using simulation where a cheaper deterministic method would be more reliable
- ignoring whether simulation assumptions match market structure

## Related Notes

- [[Probabilistic Machine Learning]]
- [[Derivatives Markets]]
- [[Portfolio Construction]]

## Sources

- [[Monte Carlo Methods in Financial Engineering]]
- [[Implementing Models in Quantitative Finance]]
- [[Tools for Computational Finance]]
- [[Murphy Probabilistic Machine Learning]]
