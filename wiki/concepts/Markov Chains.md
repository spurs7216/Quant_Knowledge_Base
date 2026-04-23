---
title: Markov Chains
type: concept
status: seed
updated: 2026-04-20
tags:
  - concept
  - stochastic-processes
  - markov-chains
  - statistics
domain: statistics
sources:
  - "[[All of Statistics]]"
  - "[[All of Statistics - Ch 23 Probability Redux Stochastic Processes]]"
  - "[[Applied Probability]]"
  - "[[Applied Probability - Ch 07 Discrete-Time Markov Chains]]"
---
# Markov Chains

## Summary

A Markov chain is a stochastic process whose future evolution depends on the present state once the present is known. The point is not independence. The point is state sufficiency: all relevant predictive information is compressed into the current state.

## Core Objects

- state space
- transition matrix or transition kernel `P`
- initial distribution `mu_0`
- marginal evolution `mu_n = mu_0 P^n`
- communicating classes
- recurrent and transient states
- stationary distribution `pi`
- hitting probabilities and hitting times

## Load-Bearing Identities

### Chapman-Kolmogorov

`P^(m+n) = P^m P^n`

This is the algebra of multi-step propagation. It is what lets one-step local dynamics generate long-run behavior.

### Stationarity

`pi = pi P`

A stationary distribution is invariant under one-step propagation.

### Detailed Balance

`pi_i p_ij = pi_j p_ji`

Detailed balance is stronger than stationarity and is the easiest constructive route to reversible chains.

### Ergodic Averaging

Under irreducibility and aperiodicity, time averages converge to expectations under the stationary distribution.

This is the bridge from process dynamics to empirical averaging.

## Structural Questions

The right questions for a chain are:

- which states communicate?
- which classes are closed?
- is the chain recurrent or transient?
- is it periodic?
- does a unique stationary distribution exist?
- do trajectories converge in distribution or only in average?
- what are the hitting probabilities and mean hitting times for the target set?

These are not decorative classification labels. They determine what long-run inference is even possible.

## Why This Matters for Quant Research

Markov chains are useful as a conceptual template for:

- latent regime models
- state-transition approximations
- queue and order-book state evolution
- discrete-state credit or event dynamics
- MCMC construction

Even when the real system is not exactly Markov, the Markov language is often the first approximation to dynamic dependence.

Coupling, reversibility, and hitting-time calculations are often the difference between a descriptive chain and a usable one.

## Failure Modes

- confusing Markov with iid
- assuming stationarity without checking communication structure and periodicity
- reading one-step intuition into a process whose long-run behavior depends on the whole state-space geometry
- using discrete-state models when the chosen state definition omits material memory

## Practical Rule

Define the state carefully. A model is only as Markovian as its state representation is sufficient.

## Related Notes

- [[Markov Chain Monte Carlo]]
- [[Continuous-Time Markov Chains]]
- [[Poisson Processes]]
- [[Stochastic Calculus]]
- [[Kalman Filtering]]
- [[All of Statistics]]

## Sources

- [[All of Statistics]]
- [[All of Statistics - Ch 23 Probability Redux Stochastic Processes]]
- [[Applied Probability]]
- [[Applied Probability - Ch 07 Discrete-Time Markov Chains]]
