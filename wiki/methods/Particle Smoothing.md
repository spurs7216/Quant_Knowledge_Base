---
title: Particle Smoothing
type: method
status: seed
updated: 2026-04-22
tags:
  - method
  - particle
  - smoothing
  - sequential-monte-carlo
domain: statistics
sources:
  - "[[Bayesian Filtering and Smoothing]]"
  - "[[Bayesian Filtering and Smoothing - Ch 15 Particle Smoothing]]"
---
# Particle Smoothing

## Summary

Particle smoothing approximates latent trajectories or smoothed state marginals conditional on the full data history when Gaussian smoothers are unreliable.

## Core equations

The backward kernel is
$$p(x_k \given x_{k+1}, y_{1:T}) \propto p(x_{k+1}\given x_k)\,p(x_k \given y_{1:k}).$$

Using filtered particles, backward simulation uses the discrete approximation
$$\Prob\!\paren{x_k = x_k^{(i)} \given x_{k+1}^\star, y_{1:T}} \propto w_k^{(i)}\,p\!\paren{x_{k+1}^\star \given x_k^{(i)}}.$$

Marginal reweighting smoothers use
$$w_{k\given T}^{(i)} \propto w_k^{(i)} \sum_j \frac{w_{k+1\given T}^{(j)}\,p\!\paren{x_{k+1}^{(j)} \given x_k^{(i)}}}{\sum_\ell w_k^{(\ell)}\,p\!\paren{x_{k+1}^{(j)} \given x_k^{(\ell)}}}.$$

## Core logic

### 1. Forward filtering is not enough for smoothed paths

Filtered particles condition only on past data. Smoothing needs the full data history.

### 2. Naive path storage degenerates badly

Repeated resampling makes ancestral histories collapse, especially early in the sample.

### 3. Backward simulation is the main practical repair

Forward-filtering backward-simulation uses the filtered particle system to sample trajectories from an approximate smoothing kernel rather than trusting the stored ancestries.

### 4. Marginal and Rao-Blackwellized smoothers answer different posterior questions

Some smoothers target smoothed marginals directly, while others target sampled trajectories. Rao-Blackwellization again matters when part of the model is conditionally Gaussian.

## When this method is the right tool

- the model is too nonlinear or non-Gaussian for Gaussian smoothing
- retrospective path inference matters
- parameter learning or decision logic depends on latent trajectories rather than only filtered states

## Failure modes

- confusing filtered particles with smoothed trajectories
- ignoring path degeneracy
- applying backward simulation on top of a poor forward particle approximation
- missing easier Gaussian-smoothing solutions when the posterior is still well approximated by a Gaussian family

## Quant relevance

This method matters for:

- nonlinear latent-path reconstruction
- multimodal hidden-state models
- backward inference for volatility, tracking, or mixed-state systems

## Related notes

- [[Particle Filtering]]
- [[General Gaussian Filtering and Smoothing]]
- [[Kalman Filtering]]
- [[Bayesian Filtering and Smoothing]]

## Sources

- [[Bayesian Filtering and Smoothing]]
- [[Bayesian Filtering and Smoothing - Ch 15 Particle Smoothing]]
