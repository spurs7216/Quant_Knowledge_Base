---
title: Maximum Likelihood Estimation
type: method
status: seed
updated: 2026-04-19
tags:
  - method
  - likelihood
  - inference
  - statistics
domain: statistics
sources:
  - "[[All of Statistics]]"
  - "[[All of Statistics - Ch 09 Parametric Inference]]"
---
# Maximum Likelihood Estimation

## Summary

Maximum likelihood estimation chooses the parameter value that makes the observed data most probable under the model. It is the default inferential engine behind much of econometrics, state-space modeling, volatility estimation, latent-variable modeling, and parametric classification.

## Core Objects

- likelihood `L(theta) = f(x | theta)`
- log-likelihood `ell(theta) = log L(theta)`
- score `s(theta) = d ell(theta) / d theta`
- Hessian or observed curvature
- Fisher information

The mle solves:

`\hat theta = argmax_theta ell(theta)`

## Why Likelihood Matters

Likelihood is not a probability distribution over `theta`. It is a function of `theta` after conditioning on the observed data. That distinction is basic and often misunderstood.

Likelihood turns modeling into optimization and asymptotic geometry:

- the peak gives the estimate
- the curvature gives local uncertainty
- likelihood ratios compare nearby parameter explanations

## First-Order Asymptotic Story

Under regularity conditions:

- `\hat theta` is consistent
- `sqrt(n) (\hat theta - theta_0)` is asymptotically Normal
- asymptotic variance is tied to the inverse Fisher information

This makes likelihood powerful, but only if the model is correctly specified or at least a useful approximation.

## What Regularity Conditions Are Doing

The regularity assumptions justify:

- differentiating under the integral sign
- local quadratic approximation of the log-likelihood
- stable behavior of the score and Hessian

When parameters lie on boundaries, identification is weak, or the model is misspecified, the usual Wald-style summary can be badly misleading.

## Why MLE Is Important in Quant Research

MLE appears directly in:

- Gaussian and non-Gaussian time-series models
- stochastic-volatility and latent-state models
- duration and point-process models
- logistic and discrete-choice models
- hidden-state and state-space estimation

In practice, many \"advanced\" estimators are still likelihood estimators with a different observation law or latent-state structure.

## Failure Modes

- treating a convenient likelihood as true rather than approximate
- reading asymptotic standard errors literally in small samples
- ignoring multimodality or flat regions in the objective
- using MLE where robustness to misspecification matters more than nominal efficiency
- forgetting that optimization success does not imply identification success

## Practical Rule

Use likelihood as a disciplined modeling language, not as an automatic stamp of correctness. Every likelihood result should be paired with:

- model-assumption scrutiny
- identification checks
- residual or fit diagnostics
- robustness to alternative specifications

## Related Notes

- [[Convergence and Limit Theory]]
- [[Bootstrap]]
- [[Statistical Decision Theory]]
- [[All of Statistics]]

## Sources

- [[All of Statistics]]
- [[All of Statistics - Ch 09 Parametric Inference]]
