---
title: Particle Filtering
type: method
status: seed
updated: 2026-04-22
tags:
  - method
  - state-space
  - particle-filter
  - sequential-monte-carlo
domain: statistics
sources:
  - "[[Bayesian Filtering and Smoothing]]"
  - "[[Bayesian Filtering and Smoothing - Ch 11 Particle Filtering]]"
  - "[[Time Series Analysis by State Space Methods]]"
  - "[[Time Series Analysis by State Space Methods - Ch 12 Particle Filtering]]"
---
# Particle Filtering

## Summary

Particle filtering is a sequential Monte Carlo method for nonlinear or non-Gaussian state-space models. It represents the filtering distribution by a weighted cloud of particles that are propagated, reweighted, and resampled through time.

## Core equations

The particle approximation to a posterior expectation is
$$\mathbb{E}[g(x_k)\given y_{1:k}] \approx \sum_{i=1}^N w_k^{(i)} g\paren{x_k^{(i)}}.$$

Generic sequential-importance weights satisfy
$$w_k^{\ast(i)} \propto w_{k-1}^{(i)} \frac{p(y_k \given x_k^{(i)})\,p(x_k^{(i)} \given x_{k-1}^{(i)})}{\pi(x_k^{(i)} \given x_{0:k-1}^{(i)}, y_{1:k})}, \qquad w_k^{(i)} = \frac{w_k^{\ast(i)}}{\sum_j w_k^{\ast(j)}}.$$

The usual degeneracy diagnostic is
$$N_\mathrm{eff} = \frac{1}{\sum_{i=1}^N \paren{w_k^{(i)}}^2}.$$

## Core logic

### 1. Particle filters approximate the posterior by a weighted empirical measure

The target is always the filtering distribution. The particles are only a numerical representation of it.

### 2. Proposal design drives weight quality

The transition prior gives the bootstrap filter, but more informative proposals can materially reduce weight collapse.

### 3. Resampling is required because sequential weights degenerate

Without resampling, a few particles quickly dominate and the empirical posterior loses support.

### 4. Auxiliary and Rao-Blackwellized designs fix different problems

Auxiliary filters use future observation information to improve proposals. Rao-Blackwellized filters analytically integrate conditionally linear-Gaussian substructure to reduce variance.

## When this method is the right tool

- the posterior is too nonlinear, skewed, or multimodal for Gaussian approximations
- the model can be simulated forward
- recursive state estimation is still desired

## Failure modes

- using the bootstrap filter by default when proposal quality is the real bottleneck
- ignoring effective sample size and weight collapse
- using too few particles for a sharply concentrated posterior
- overlooking Rao-Blackwellization opportunities in mixed models

## Quant relevance

This method matters for:

- stochastic-volatility and heavy-tailed latent-state models
- nonlinear observation equations
- online filtering where Gaussian approximations are too crude

## Related notes

- [[General Gaussian Filtering and Smoothing]]
- [[Particle Smoothing]]
- [[Kalman Filtering]]
- [[Bayesian Filtering and Smoothing]]

## Sources

- [[Bayesian Filtering and Smoothing]]
- [[Bayesian Filtering and Smoothing - Ch 11 Particle Filtering]]
- [[Time Series Analysis by State Space Methods]]
- [[Time Series Analysis by State Space Methods - Ch 12 Particle Filtering]]
