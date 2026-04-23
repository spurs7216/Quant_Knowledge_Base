---
title: Parameter Estimation in State Space Models
type: method
status: seed
updated: 2026-04-22
tags:
  - method
  - state-space
  - estimation
  - likelihood
domain: statistics
sources:
  - "[[Bayesian Filtering and Smoothing]]"
  - "[[Bayesian Filtering and Smoothing - Ch 16 Parameter Estimation]]"
---
# Parameter Estimation in State Space Models

## Summary

Parameter estimation in state-space models fits unknown transition, observation, and noise parameters by reusing the filtering and smoothing machinery that already defines the latent-state inference problem.

## Core equations

The predictive likelihood factorization is
$$p(y_{1:T}\given \theta)=\prod_{k=1}^T p(y_k \given y_{1:k-1},\theta).$$

The recursive term is
$$p(y_k \given y_{1:k-1},\theta)=\int p(y_k \given x_k,\theta)\,p(x_k \given y_{1:k-1},\theta)\,dx_k.$$

The energy function takes the form
$$\varphi(\theta) = -\log p(\theta) - \sum_{k=1}^T \log p(y_k \given y_{1:k-1},\theta).$$

The EM auxiliary function is
$$Q(\theta,\theta^{(n)}) = \mathbb{E}\bracket{\log p(x_{0:T},y_{1:T}\given \theta)\given y_{1:T},\theta^{(n)}}.$$

## Core logic

### 1. Filtering already computes the building blocks of likelihood recursion

Once the predictive state distribution is available, the one-step predictive likelihood is obtained by integrating through the measurement model.

### 2. MAP, ML, EM, and MCMC are different ways to use the same recursion

The book's durable point is not to pick one optimizer. It is to expose the shared posterior and likelihood structure underneath these approaches.

### 3. The approximation family used in estimation should match deployment

If the final model will be filtered with Gaussian approximations or particle methods, the fitting workflow should usually use the same approximation family.

### 4. Smoothing matters because many learning rules need latent-state expectations

EM and related gradient identities depend on smoothed expectations or trajectory draws, not only filtered one-step summaries.

## When this method is the right tool

- model parameters are genuinely unknown rather than hand-tuned
- latent-state structure matters for prediction or interpretation
- the fitted model will actually be used in the same inference family

## Failure modes

- fitting with one approximation family and deploying with another
- confusing likelihood optimization with identification
- ignoring sensitivity to initialization, constraints, or local optima
- hand-tuning noise covariances when a recursive objective is already available

## Quant relevance

This method matters for:

- fitting latent-volatility and hidden-state models
- learning process and measurement noise levels
- calibrating state-space models instead of tuning them by eye

## Related notes

- [[Maximum Likelihood Estimation]]
- [[Markov Chain Monte Carlo]]
- [[General Gaussian Filtering and Smoothing]]
- [[Particle Filtering]]
- [[Particle Smoothing]]
- [[Bayesian Filtering and Smoothing]]

## Sources

- [[Bayesian Filtering and Smoothing]]
- [[Bayesian Filtering and Smoothing - Ch 16 Parameter Estimation]]
