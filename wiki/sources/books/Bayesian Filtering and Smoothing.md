---
title: Bayesian Filtering and Smoothing
type: source
status: chapter_ingested
updated: 2026-04-18
tags:
  - source
  - bayesian
  - filtering
  - state-space
sources:
  - "[[raw/math_statistics/Simo Särkkä and Lennart Svensson, Bayesian Filtering and Smoothing.pdf]]"
---
# Bayesian Filtering and Smoothing

## Summary

Särkkä and Svensson present a modern state-space estimation text that moves from Bayesian inference and recursive estimation into discretization, state-space modeling, exact filtering equations, extended and Gaussian filters, particle methods, smoothing, and parameter estimation. It is one of the most important books in the raw shelf for any future latent-state, regime, or tracking workflow.

## Chapter-by-Chapter Ingest

- `Chapter 1. What Are Bayesian Filtering and Smoothing?`: frames the estimation problem and its main use cases.
- `Chapter 2. Bayesian Inference`: sets up posterior reasoning as the general logic of filtering.
- `Chapter 3. Batch and Recursive Bayesian Estimation`: contrasts one-shot estimation with sequential updating.
- `Chapter 4. Discretization of Continuous-Time Dynamic Models`: links continuous dynamics with discrete-time computation.
- `Chapter 5. Modeling with State Space Models`: formalizes latent-state and observation equations.
- `Chapter 6. Bayesian Filtering Equations and Exact Solutions`: derives the core recursive equations.
- `Chapter 7. Extended Kalman Filtering`: introduces first-order nonlinear Gaussian approximation.
- `Chapter 8. General Gaussian Filtering`: broadens Gaussian filtering beyond the classic EKF.
- `Chapter 9. Gaussian Filtering by Sigma-Point Approximations`: uses deterministic transforms to propagate moments.
- `Chapter 10. Posterior Linearization Filtering`: develops an alternative approximation strategy.
- `Chapter 11. Particle Filtering`: handles non-Gaussian and strongly nonlinear settings by simulation.
- `Chapter 12. Bayesian Smoothing Equations and Exact Solutions`: turns sequential filtering into full-path posterior recovery.
- `Chapter 13. Extended Rauch-Tung-Striebel Smoothing`: extends smoothing into nonlinear settings.
- `Chapter 14. General Gaussian Smoothing`: generalizes smoothing under Gaussian approximations.
- `Chapter 15. Particle Smoothing`: extends simulation-based ideas to posterior path reconstruction.
- `Chapter 16. Parameter Estimation`: treats learning model parameters alongside latent states.
- `Chapter 17. Epilogue`: closes with scope, limits, and broader positioning of the methods.

## Key Claims

- Filtering and smoothing are just sequential and pathwise forms of Bayesian inference.
- Nonlinear state-space problems require approximation choices that directly affect robustness and interpretation.
- Parameter estimation cannot be separated cleanly from latent-state modeling in serious applications.

## Methods and Data

- recursive Bayesian estimation
- discretization of continuous-time models
- Kalman, extended Kalman, and Gaussian filters
- particle filtering and smoothing
- parameter estimation in state-space models

## Why It Matters Here

This book is a major anchor for the vault's signal-processing and hidden-state frontier. It is relevant for forecasting, market-state estimation, execution-state tracking, volatility inference, and regime modeling.

## Reflection

The strongest contribution here is architectural. The book shows that many apparently different filters are just different approximation choices inside the same Bayesian state-space template.

## Caveats

- The text is method-heavy and assumes comfort with linear algebra, probability, and matrix calculus.
- The connection to finance is indirect and needs crystallization into market-specific notes.

## Related Notes

- [[Kalman Filtering]]
- [[Kalman Filter Tutorial]]
- [[Financial Signal Processing and Machine Learning]]
- [[Signal Processing Map]]

## Sources

- [[raw/math_statistics/Simo Särkkä and Lennart Svensson, Bayesian Filtering and Smoothing.pdf]]
