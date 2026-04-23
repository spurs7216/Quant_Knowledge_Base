---
title: Continuous-Time Markov Chains
type: concept
status: seed
updated: 2026-04-20
tags:
  - concept
  - stochastic-processes
  - markov-chains
  - continuous-time
domain: statistics
sources:
  - "[[Applied Probability]]"
  - "[[Applied Probability - Ch 08 Continuous-Time Markov Chains]]"
---
# Continuous-Time Markov Chains

## Summary

A continuous-time Markov chain is a state process that waits an exponential amount of time in its current state and then jumps to a new state according to transition intensities. The main object is the generator, not a one-step transition matrix.

## Core Objects

- finite-time transition matrix `P(t)`
- transition intensities `lambda_ij`
- total exit rate `lambda_i = sum_{j != i} lambda_ij`
- infinitesimal generator `Lambda`
- stationary distribution `pi`
- detailed balance relation

## Load-Bearing Identities

### Generator Evolution

Finite-time transition probabilities satisfy a differential system of the form

`P'(t) = Lambda P(t)`,

with solution

`P(t) = exp(t Lambda)`.

### Stationarity

The stationary law satisfies

`pi Lambda = 0`.

This is the continuous-time analogue of `pi = pi P`.

### Detailed Balance

For a reversible chain,

`pi_i lambda_ij = pi_j lambda_ji`.

This guarantees stationarity and gives a constructive route to equilibrium.

### Holding-Time Law

Conditional on being in state `i`, the holding time is exponential with rate `lambda_i`.

## Structural Questions

The right questions are:

- what are the states and which jumps are allowed?
- what generator is economically or physically plausible?
- is the chain irreducible or decomposable?
- does a stationary law exist?
- is reversibility available or inappropriate?

## Why This Matters for Quant Research

Continuous-time Markov chains are useful for:

- intensity-based credit or default-state models
- queueing and inventory systems
- continuous-time regime models
- jump-state approximations that sit between discrete chains and diffusions

## Failure Modes

- confusing transition intensities with transition probabilities
- assuming stationarity without checking communication structure
- using the right states but the wrong jump architecture
- ignoring numerical issues in computing `exp(t Lambda)`

## Practical Rule

Build the generator first. Once the generator is coherent, finite-time behavior, equilibrium, and simulation follow from it.

## Related Notes

- [[Markov Chains]]
- [[Poisson Processes]]
- [[Diffusion Processes]]
- [[Stochastic Calculus]]

## Sources

- [[Applied Probability]]
- [[Applied Probability - Ch 08 Continuous-Time Markov Chains]]
