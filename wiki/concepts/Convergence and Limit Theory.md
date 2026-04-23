---
title: Convergence and Limit Theory
type: concept
status: seed
updated: 2026-04-19
tags:
  - concept
  - probability
  - asymptotics
  - statistics
domain: statistics
sources:
  - "[[All of Statistics]]"
  - "[[All of Statistics - Ch 04 Inequalities]]"
  - "[[All of Statistics - Ch 05 Convergence of Random Variables]]"
---
# Convergence and Limit Theory

## Summary

Convergence and limit theory explain why random estimators become stable enough to support inference. This is the mathematical layer beneath confidence intervals, Wald tests, bootstrap approximations, asymptotic likelihood theory, and most large-sample claims in econometrics and quant research.

## Core Objects

- sequence of random variables `X_n`
- convergence almost surely, in probability, in distribution, and in `L^p`
- sample average `\bar X_n`
- centered and scaled statistics such as `sqrt(n) (\hat theta_n - theta)`
- limiting distribution, usually Gaussian in first-order asymptotics

## Mode-of-Convergence Ladder

The key hierarchy is:

- `X_n -> X` almost surely implies `X_n -> X` in probability
- `X_n -> X` in probability implies `X_n => X` in distribution
- `X_n -> X` in `L^p` implies `X_n -> X` in probability

The reverse implications generally fail without extra conditions. That matters because many quant arguments quietly slide between these notions as if they were interchangeable.

## Load-Bearing Results

### Law of Large Numbers

The law of large numbers justifies replacing population expectations by sample averages:

`\bar X_n -> E[X]`

under appropriate integrability and dependence assumptions.

This is the first reason empirical averages, realized moments, sample proportions, and backtest summaries can be used at all.

### Central Limit Theorem

The central limit theorem explains first-order sampling fluctuation:

`sqrt(n) (\bar X_n - mu) / sigma => N(0, 1)`

for iid data with finite variance.

The CLT does not say the raw estimator is Normal. It says the centered and scaled error is asymptotically Normal. That distinction matters whenever one moves from estimator behavior to interval construction.

### Slutsky and Delta Method

Slutsky's theorem and the delta method let asymptotic Normality survive nonlinear transformation.

If

`sqrt(n) (\hat theta_n - theta) => N(0, V)`

and `g` is differentiable at `theta`, then

`sqrt(n) (g(\hat theta_n) - g(theta)) => N(0, G V G^T)`

where `G` is the Jacobian of `g` at `theta`.

This is why standard errors propagate from primitive estimators into functions such as Sharpe-like ratios, elasticities, transformed coefficients, and predictive probabilities.

## Why This Matters for Quant Research

Quant research routinely relies on:

- t-statistics for alphas and regression coefficients
- asymptotic covariance matrices for estimators
- likelihood-based inference in latent-state or volatility models
- large-sample approximations for portfolio and risk diagnostics

If the convergence regime is wrong, the inference layer is wrong even when the code is flawless.

## What Breaks the Usual Story

- heavy tails that destroy finite variance or make convergence slow
- serial dependence that invalidates iid scaling
- structural breaks that make the target itself unstable
- high-dimensional settings where fixed-parameter asymptotics are misleading
- ratios or tail functionals whose delta-method approximation is weak in finite samples

## Quant Research Implications

- never use asymptotic language without stating the relevant sampling assumptions
- distinguish estimator consistency from usable finite-sample precision
- treat CLT-based p-values with skepticism in dependent, heteroskedastic, or heavy-tailed settings
- use bootstrap, sandwich, or dependence-aware methods when the basic iid route is not credible

## Related Notes

- [[Bootstrap]]
- [[Maximum Likelihood Estimation]]
- [[Statistical Decision Theory]]
- [[All of Statistics]]

## Sources

- [[All of Statistics]]
- [[All of Statistics - Ch 04 Inequalities]]
- [[All of Statistics - Ch 05 Convergence of Random Variables]]
