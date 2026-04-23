---
title: Bootstrap
type: method
status: seed
updated: 2026-04-19
tags:
  - method
  - bootstrap
  - resampling
  - statistics
domain: statistics
sources:
  - "[[All of Statistics]]"
  - "[[All of Statistics - Ch 07 Estimating the cdf and Statistical Functionals]]"
  - "[[All of Statistics - Ch 08 The Bootstrap]]"
---
# Bootstrap

## Summary

The bootstrap replaces the unknown data-generating distribution with the empirical distribution, then uses repeated resampling to approximate the sampling behavior of an estimator or statistic. It is one of the most reusable ways to quantify uncertainty when closed-form variance algebra is messy or unavailable.

## Core Idea

Given observations `X_1, ..., X_n`, replace the unknown distribution `F` by the empirical distribution `\hat F_n`. Then:

1. resample from `\hat F_n`
2. recompute the statistic on each resample
3. use the resampled distribution as a proxy for the sampling distribution of the original statistic

The bootstrap is therefore a plug-in principle applied to distributions of estimators rather than only to point functionals.

## What It Estimates Well

- standard errors
- bias
- confidence intervals
- uncertainty for nonlinear functionals such as quantiles, correlations, and ratios

This is especially useful when the estimator is easy to compute but hard to analyze.

## Common Bootstrap Objects

- bootstrap replicate `T_n^*`
- bootstrap standard error `sd(T_n^*)`
- percentile interval
- basic interval
- studentized interval when variance estimation is available

The studentized route is often more stable because it partially corrects for scale distortion in the raw statistic.

## Why It Works

The bootstrap works when the empirical distribution is a good enough stand-in for the unknown population for the purpose of the statistic under study. The method is strongest when:

- the statistic is sufficiently smooth
- the data are close to iid
- the estimator is not dominated by boundary effects, discreteness, or unstable tails

## Failure Modes

- naive iid bootstrap under serial dependence
- poor behavior for extreme-value or highly nonsmooth statistics
- heavy tails that make resampled dispersion unstable
- using percentile intervals mechanically when skewness or bias is material
- forgetting that the bootstrap approximates the sampling law of the estimator, not the truth of the model

## Quant Research Relevance

The bootstrap is useful for:

- uncertainty around signal means and spreads
- confidence intervals for Sharpe-like ratios and ranking metrics
- finite-sample checks for portfolio statistics
- model-comparison uncertainty when asymptotic theory is fragile

For time-series or panel settings, the standard iid bootstrap is usually the wrong tool. Block, cluster, or dependence-aware resampling is often needed.

## Practical Rule

Use the bootstrap when analytic uncertainty quantification is ugly, but only after checking whether the sampling structure makes the bootstrap approximation credible.

## Related Notes

- [[Convergence and Limit Theory]]
- [[Maximum Likelihood Estimation]]
- [[Monte Carlo Methods]]
- [[All of Statistics]]

## Sources

- [[All of Statistics]]
- [[All of Statistics - Ch 07 Estimating the cdf and Statistical Functionals]]
- [[All of Statistics - Ch 08 The Bootstrap]]
