---
title: General Gaussian Filtering and Smoothing
type: method
status: seed
updated: 2026-04-22
tags:
  - method
  - gaussian
  - filtering
  - smoothing
domain: statistics
sources:
  - "[[Bayesian Filtering and Smoothing]]"
  - "[[Bayesian Filtering and Smoothing - Ch 07 Extended Kalman Filtering]]"
  - "[[Bayesian Filtering and Smoothing - Ch 08 General Gaussian Filtering]]"
  - "[[Bayesian Filtering and Smoothing - Ch 09 Gaussian Filtering by Enabling Approximations]]"
  - "[[Bayesian Filtering and Smoothing - Ch 10 Posterior Linearization Filtering]]"
  - "[[Bayesian Filtering and Smoothing - Ch 13 Extended Rauch-Tung-Striebel Smoothing]]"
  - "[[Bayesian Filtering and Smoothing - Ch 14 General Gaussian Smoothing]]"
---
# General Gaussian Filtering and Smoothing

## Summary

General Gaussian filtering and smoothing is the family of nonlinear state-space methods that keeps the posterior approximately Gaussian while changing how the required moments or linearizations are computed.

## Core equations

The generic Gaussian-filter update can be written from predicted and measurement moments:
$$m_k^- = \mathbb{E}[x_k \given y_{1:k-1}], \qquad P_k^- = \operatorname{Cov}[x_k \given y_{1:k-1}],$$
$$\mu_k = \mathbb{E}[y_k \given y_{1:k-1}], \qquad S_k = \operatorname{Cov}[y_k \given y_{1:k-1}], \qquad C_k = \operatorname{Cov}[x_k,y_k \given y_{1:k-1}],$$
$$K_k = C_k S_k^{-1}, \qquad m_k = m_k^- + K_k(y_k-\mu_k), \qquad P_k = P_k^- - K_k S_k K_k^\top.$$

The matching RTS-style smoother uses
$$G_k = D_{k+1}\bracket{P_{k+1}^-}^{-1},$$
$$m_k^s = m_k + G_k\paren{m_{k+1}^s - m_{k+1}^-}, \qquad P_k^s = P_k + G_k\paren{P_{k+1}^s - P_{k+1}^-}G_k^\top,$$
where $D_{k+1}=\operatorname{Cov}(x_k,x_{k+1}\given y_{1:k})$.

## Core logic

### 1. The recursion is shared; the approximation device changes

EKF, sigma-point filters, SLR filters, and posterior-linearization filters all use the same Gaussian update structure once the necessary moments or linearized coefficients are available.

### 2. The real design choice is how to compute or approximate moments

The family splits by approximation device:

- Taylor linearization
- moment matching with quadrature or sigma points
- statistical linear regression
- posterior linearization

### 3. Smoothing is the backward counterpart, not a separate theory

The same approximation families reappear on the smoothing side through RTS-style backward recursions.

### 4. Posterior-aware linearization is a genuine upgrade over prior-only linearization

Posterior linearization changes the averaging distribution used to build the Gaussian surrogate. That is why it can outperform prior-based linearizations in strongly informative update steps.

## When this method is the right tool

- the latent-state posterior is still usefully summarized by means and covariances
- the model is nonlinear, but not so non-Gaussian that Gaussian shape is obviously misleading
- recursive filtering or smoothing is needed, but particle methods would be unnecessarily expensive

## Failure modes

- treating filter names as if they were different inferential targets rather than different approximation choices
- assuming a numerically stable recursion implies a good posterior approximation
- using local Taylor methods when the posterior is clearly nonlocal
- staying in the Gaussian family after multimodality or severe skewness is already obvious

## Quant relevance

This method matters for:

- nonlinear latent-factor and volatility models
- tracking and signal-extraction problems with nonlinear measurements
- recursive state estimation problems that are richer than plain Kalman filtering but not yet particle-filter territory

## Related notes

- [[Kalman Filtering]]
- [[Posterior Linearization in State Space Inference]]
- [[Particle Filtering]]
- [[Particle Smoothing]]
- [[State Space Models]]
- [[Bayesian Filtering and Smoothing]]

## Sources

- [[Bayesian Filtering and Smoothing]]
- [[Bayesian Filtering and Smoothing - Ch 07 Extended Kalman Filtering]]
- [[Bayesian Filtering and Smoothing - Ch 08 General Gaussian Filtering]]
- [[Bayesian Filtering and Smoothing - Ch 09 Gaussian Filtering by Enabling Approximations]]
- [[Bayesian Filtering and Smoothing - Ch 10 Posterior Linearization Filtering]]
- [[Bayesian Filtering and Smoothing - Ch 13 Extended Rauch-Tung-Striebel Smoothing]]
- [[Bayesian Filtering and Smoothing - Ch 14 General Gaussian Smoothing]]
