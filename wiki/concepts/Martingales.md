---
title: Martingales
type: concept
status: seed
updated: 2026-04-20
tags:
  - concept
  - probability
  - martingales
  - stochastic-processes
domain: statistics
sources:
  - "[[Applied Probability]]"
  - "[[Applied Probability - Ch 10 Martingales]]"
---
# Martingales

## Summary

A martingale is a stochastic process whose conditional expectation tomorrow equals its value today once today's information is fixed. The point is not independence or lack of volatility. The point is conditional fairness relative to a filtration.

## Core Objects

- filtration `F_n`
- adapted process `X_n`
- martingale, submartingale, supermartingale
- stopping time `T`
- stopped process `X_{T ^ n}`
- bounded differences

## Load-Bearing Identities

### Martingale Property

`E[X_{n+1} | F_n] = X_n`.

This is the defining relation.

### Doob Martingale

For any integrable `Z`,

`X_n = E[Z | F_n]`

is a martingale. This is why martingales appear throughout probability rather than only in gambling examples.

### Optional Stopping

Under real finiteness and integrability conditions,

`E[X_T] = E[X_0]`.

This is powerful and easy to misuse when the conditions are ignored.

### Azuma-Hoeffding

For martingales with bounded increments, tail probabilities admit exponential concentration bounds. This extends concentration logic beyond simple independent sums.

## Structural Questions

The right questions are:

- what filtration defines the information flow?
- is the process truly a martingale or only a submartingale?
- are optional-stopping conditions satisfied?
- are bounded-increment or square-integrability assumptions available?

## Why This Matters for Quant Research

Martingales matter for:

- stopping-time arguments
- concentration for sequentially revealed randomness
- no-arbitrage and fair-game intuition in pricing theory
- later continuous-time stochastic-calculus machinery

## Failure Modes

- calling a process a martingale just because its unconditional drift looks small
- using optional stopping without checking integrability
- treating a martingale as if it had independent increments
- forgetting that the filtration is part of the model

## Practical Rule

Always ask: martingale with respect to which information set? Without the filtration, the claim is incomplete.

## Related Notes

- [[Diffusion Processes]]
- [[Stochastic Calculus]]
- [[Markov Chains]]

## Sources

- [[Applied Probability]]
- [[Applied Probability - Ch 10 Martingales]]
