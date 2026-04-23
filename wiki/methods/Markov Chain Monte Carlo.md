---
title: Markov Chain Monte Carlo
type: method
status: seed
updated: 2026-04-19
tags:
  - method
  - mcmc
  - monte-carlo
  - bayesian
domain: statistics
sources:
  - "[[All of Statistics]]"
  - "[[All of Statistics - Ch 23 Probability Redux Stochastic Processes]]"
  - "[[All of Statistics - Ch 24 Simulation Methods]]"
  - "[[Monte Carlo Methods]]"
---
# Markov Chain Monte Carlo

## Summary

Markov chain Monte Carlo constructs a Markov chain whose stationary distribution is the target distribution, then estimates expectations by ergodic averages along the simulated path. It is the main route for computation when direct sampling or analytic integration is unavailable.

## Core Idea

If the target density is `pi(x)` and direct draws are difficult, build a chain `{X_t}` such that:

- `pi` is stationary for the chain
- the chain is ergodic enough to explore the target
- sample averages approximate target expectations

Then estimate:

`E_pi[h(X)] approx (1 / T) sum_{t=1}^T h(X_t)`

The validity of this approximation comes from Markov-chain convergence, not from iid sampling.

## Main Algorithms

### Metropolis-Hastings

Propose `Y ~ q(. | X_t)` and accept with probability

`alpha(x, y) = min(1, [pi(y) q(x | y)] / [pi(x) q(y | x)])`

This acceptance rule enforces detailed balance with respect to `pi`.

### Gibbs Sampling

Sample each block from its full conditional distribution.

Gibbs is attractive when the full conditionals are simpler than the joint distribution.

### Metropolis within Gibbs

Use a Metropolis step for blocks whose full conditionals are not directly sampleable.

## What Actually Matters in Practice

- irreducibility and support coverage
- mixing speed
- autocorrelation
- tuning of proposal scale
- effective sample size
- whether the chain explores all relevant regions of the target

The algorithm is correct only if the chain is both theoretically valid and practically able to move.

## Diagnostics

- trace plots across multiple starting values
- autocorrelation and effective sample size
- acceptance-rate sanity checks for Metropolis-type samplers
- sensitivity to reparameterization or blocking choice
- posterior summaries that are stable across long-enough runs

## Failure Modes

- treating correlated draws as if they were iid
- confusing stationarity in theory with usable finite-run convergence
- poor proposal tuning leading to sticky chains
- multimodal targets where the chain almost never transitions between modes
- reporting posterior precision without checking Monte Carlo error

## Quant Research Relevance

MCMC is relevant when quant research needs:

- Bayesian latent-state estimation
- hierarchical shrinkage
- posterior uncertainty for model parameters
- rare-event or complex-structure integration

It is less attractive when a simpler deterministic or direct-sampling method is available and more reliable.

## Practical Rule

Treat MCMC as a stochastic numerical method with statistical assumptions, not as a black-box posterior button.

## Related Notes

- [[Markov Chains]]
- [[Monte Carlo Methods]]
- [[Maximum Likelihood Estimation]]
- [[Probabilistic Machine Learning]]

## Sources

- [[All of Statistics]]
- [[All of Statistics - Ch 23 Probability Redux Stochastic Processes]]
- [[All of Statistics - Ch 24 Simulation Methods]]
- [[Monte Carlo Methods]]
