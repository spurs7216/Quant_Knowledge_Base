---
title: State Space Discretization from Continuous-Time Models
type: method
status: seed
updated: 2026-04-22
tags:
  - method
  - state-space
  - discretization
  - continuous-time
domain: statistics
sources:
  - "[[Bayesian Filtering and Smoothing]]"
  - "[[Bayesian Filtering and Smoothing - Ch 04 Discretization of Continuous-Time Dynamic Models]]"
---
# State Space Discretization from Continuous-Time Models

## Summary

State-space discretization turns a continuous-time stochastic dynamic law into a discrete-time transition model that a filter or smoother can actually run. In serious latent-state work, this is part of the model, not a preprocessing nuisance.

## Core equations

For a continuous-time linear SDE,
$$dx(t)=F x(t)\,dt + L\,dw(t), \qquad \mathbb{E}\bracket{dw(t)\,dw(t)^\top}=Q_c\,dt,$$
the exact discrete-time model over sampling interval $\Delta t$ is
$$x_k = A x_{k-1} + q_{k-1}, \qquad A = e^{F\Delta t}, \qquad q_{k-1}\sim \mathcal{N}(0,Q_d),$$
with covariance
$$Q_d=\int_0^{\Delta t} e^{F(\Delta t-\tau)} L Q_c L^\top e^{F^\top(\Delta t-\tau)}\,d\tau.$$

For nonlinear dynamics, Euler-Maruyama gives the first approximation
$$x_k \approx x_{k-1} + f(x_{k-1})\,\Delta t + L(x_{k-1})\sqrt{\Delta t}\,\varepsilon_k, \qquad \varepsilon_k \sim \mathcal{N}(0,I).$$

## Core logic

### 1. Transition mean and transition covariance must be discretized together

It is not enough to discretize the deterministic drift correctly and then guess a covariance. The filter sees both.

### 2. Linear-Gaussian models often admit exact discretization

For linear SDEs the exact matrix-exponential transition is usually the right benchmark. Approximate schemes should be treated as compromises, not defaults.

### 3. Nonlinear discretization is an approximation design problem

Outside the linear case, the real question becomes which approximation regime is acceptable:

- Euler-Maruyama
- continuous-time linearization
- additive-noise approximation
- finer latent-time grid with skipped measurement updates

### 4. Discretization error propagates into every later inference stage

Prediction bias, process-noise misspecification, and smoother instability can all originate here. A better filter cannot repair a bad transition model.

## When this method is the right tool

- the latent-state model is motivated in continuous time
- the observations arrive at discrete times
- process-noise structure matters for identification or uncertainty quantification

## Failure modes

- using Euler-Maruyama with a sampling interval that is too coarse
- approximating the mean carefully but using an unrealistic process covariance
- forgetting that the discretization rule can change the state dependence of the noise
- blaming the filter for what is really a transition-model error

## Quant relevance

This method matters for:

- continuous-time latent factors observed on discrete market grids
- nonlinear state-space models built from economic or physical intuition
- separating model misspecification from numerical transition error

## Related notes

- [[State Space Models]]
- [[Kalman Filtering]]
- [[General Gaussian Filtering and Smoothing]]
- [[Bayesian Filtering and Smoothing]]

## Sources

- [[Bayesian Filtering and Smoothing]]
- [[Bayesian Filtering and Smoothing - Ch 04 Discretization of Continuous-Time Dynamic Models]]
