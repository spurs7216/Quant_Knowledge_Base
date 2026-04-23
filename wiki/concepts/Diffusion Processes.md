---
title: Diffusion Processes
type: concept
status: seed
updated: 2026-04-20
tags:
  - concept
  - stochastic-processes
  - diffusion-processes
  - continuous-time
domain: statistics
sources:
  - "[[Applied Probability]]"
  - "[[Applied Probability - Ch 11 Diffusion Processes]]"
  - "[[Stochastic Calculus for Finance II]]"
---
# Diffusion Processes

## Summary

A diffusion process is a continuous-time stochastic process with continuous paths whose local evolution is described by an infinitesimal drift and variance. It is the continuous-path counterpart to jump and count processes.

## Core Objects

- state process `X_t`
- drift `mu(t, x)`
- infinitesimal variance `sigma^2(t, x)`
- Brownian motion
- first-passage time
- stationary density

## Load-Bearing Identities

### Local Description

Diffusions are specified locally through their infinitesimal mean and variance rather than through one-step transition matrices.

### Forward Equation

The density `f(t, x)` evolves through a Kolmogorov forward equation of the form

`partial_t f = -partial_x[mu f] + (1/2) partial_x^2[sigma^2 f]`.

### First-Passage Logic

Hitting probabilities and expected passage times are often found by solving boundary-value problems rather than by direct path enumeration.

### No-Flux Equilibrium

For one-dimensional time-homogeneous diffusions, a stationary density under zero probability flux has the generic form

`f(x) proportional to sigma^{-2}(x) exp(integral 2 mu(x) / sigma^2(x) dx)`.

## Structural Questions

The right questions are:

- what are the state variables?
- what drift and variance structure is being assumed?
- are boundaries absorbing, reflecting, or natural?
- is a jump model more appropriate than a diffusion?
- does an equilibrium density exist and make economic sense?

## Why This Matters for Quant Research

Diffusions matter for:

- continuous-time state dynamics
- mean-reversion models such as Ornstein-Uhlenbeck
- barrier and first-passage events
- the bridge into stochastic calculus and asset-pricing models

## Failure Modes

- treating diffusion paths as smooth trajectories
- forcing diffusions onto clearly jump-driven data
- ignoring boundary behavior
- confusing descriptive real-world dynamics with pricing dynamics under a changed measure

## Practical Rule

If the model claim is continuous-time and continuous-path, the drift, variance, and boundary conditions need to be explicit.

## Related Notes

- [[Poisson Processes]]
- [[Continuous-Time Markov Chains]]
- [[Martingales]]
- [[Stochastic Calculus]]

## Sources

- [[Applied Probability]]
- [[Applied Probability - Ch 11 Diffusion Processes]]
- [[Stochastic Calculus for Finance II]]
