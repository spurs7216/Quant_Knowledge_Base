---
title: Posterior Linearization in State Space Inference
type: method
status: seed
updated: 2026-04-22
tags:
  - method
  - state-space
  - gaussian
  - posterior-linearization
domain: statistics
sources:
  - "[[Bayesian Filtering and Smoothing]]"
  - "[[Bayesian Filtering and Smoothing - Ch 10 Posterior Linearization Filtering]]"
  - "[[Bayesian Filtering and Smoothing - Ch 14 General Gaussian Smoothing]]"
---
# Posterior Linearization in State Space Inference

## Summary

Posterior linearization is the Gaussian-approximation strategy that linearizes a nonlinear transformation with respect to the posterior distribution rather than the prior or filtering distribution. Iterated posterior linearization makes that idea usable in filtering and smoothing.

## Core equations

For generalized statistical linear regression with respect to a linearization law $\pi(x)$,
$$A = C_G^\top P_\pi^{-1}, \qquad b = \mu_G - A m_\pi, \qquad \Lambda = S_G - A P_\pi A^\top.$$

Posterior linearization chooses
$$\pi(x)=p(x\given y).$$

In the iterated posterior linearization filter, the measurement moments at iteration $i-1$ are
$$\mu_k^{+,(i-1)} = \int h_k(x)\,\mathcal{N}\!\paren{x \given m_k^{(i-1)}, P_k^{(i-1)}}\,dx,$$
$$P_k^{xy,(i-1)} = \int \paren{x-m_k^{(i-1)}}\paren{h_k(x)-\mu_k^{+,(i-1)}}^\top \mathcal{N}\!\paren{x \given m_k^{(i-1)}, P_k^{(i-1)}}\,dx,$$
$$P_k^{y,(i-1)} = \int \paren{h_k(x)-\mu_k^{+,(i-1)}}\paren{h_k(x)-\mu_k^{+,(i-1)}}^\top \mathcal{N}\!\paren{x \given m_k^{(i-1)}, P_k^{(i-1)}}\,dx + R_k,$$
which define
$$H_k^{(i)} = \bracket{P_k^{xy,(i-1)}}^\top \bracket{P_k^{(i-1)}}^{-1}, \qquad b_k^{(i)} = \mu_k^{+,(i-1)} - H_k^{(i)}m_k^{(i-1)},$$
$$\Omega_k^{(i)} = P_k^{y,(i-1)} - H_k^{(i)} P_k^{(i-1)} H_k^{(i)\top}.$$

## Core logic

### 1. The linearization distribution is itself a design choice

Posterior linearization becomes visible only after generalized SLR makes explicit that linearization depends on which distribution is used for averaging.

### 2. Posterior linearization targets the region where the posterior mass actually lies

That is why it can outperform prior-based linearization when the measurement update is highly informative.

### 3. Iteration resolves the circularity

The true posterior is unknown, so practical algorithms iterate by using the current Gaussian posterior approximation as the next linearization law.

### 4. The same idea extends from filtering to smoothing

On the smoothing side, iterated posterior linearization smoothers choose linearizations using the smoothed trajectory distribution rather than only the filtering distribution.

## When this method is the right tool

- a Gaussian approximation is still plausible
- prior-based or Taylor-based linearization is too crude near the informative posterior region
- particle methods are still more expensive than warranted

## Failure modes

- treating posterior linearization as if it were exact non-Gaussian inference
- iterating a poor initial Gaussian approximation without checking convergence behavior
- ignoring the computational cost of repeated moment evaluations
- confusing IEKF-style local iteration with posterior-distribution iteration

## Quant relevance

This method matters for:

- nonlinear measurement updates where local Taylor linearization is too brittle
- posterior-aware state estimation in moderate dimensions
- comparing Gaussian filters by what distribution they linearize against

## Related notes

- [[General Gaussian Filtering and Smoothing]]
- [[Kalman Filtering]]
- [[Particle Filtering]]
- [[Particle Smoothing]]
- [[Bayesian Filtering and Smoothing]]

## Sources

- [[Bayesian Filtering and Smoothing]]
- [[Bayesian Filtering and Smoothing - Ch 10 Posterior Linearization Filtering]]
- [[Bayesian Filtering and Smoothing - Ch 14 General Gaussian Smoothing]]
