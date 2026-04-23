---
title: Poisson Processes
type: concept
status: seed
updated: 2026-04-20
tags:
  - concept
  - stochastic-processes
  - point-processes
  - probability
domain: statistics
sources:
  - "[[Applied Probability]]"
  - "[[Applied Probability - Ch 06 Poisson Processes]]"
  - "[[All of Statistics]]"
  - "[[All of Statistics - Ch 23 Probability Redux Stochastic Processes]]"
---
# Poisson Processes

## Summary

A Poisson process is the canonical stochastic model for random event arrivals in time or space. Its central feature is not merely that counts are Poisson-distributed, but that disjoint regions contribute independent increments and the whole process is pinned down by an intensity function.

## Core Objects

- counting process `N(t)` or counting measure `N(A)`
- intensity function `lambda(x)` or constant rate `lambda`
- mean measure `Lambda(A) = integral_A lambda(x) dx`
- arrival times `T_k`
- interarrival times `W_k`
- marks attached to events

## Load-Bearing Identities

### Count Law

For a region `A`, the event count satisfies

`N(A) ~ Poisson(Lambda(A))`.

### Independent Increments

Counts on disjoint regions are independent. This is what turns local rate information into tractable global counting behavior.

### Homogeneous Waiting-Time Structure

For a homogeneous one-dimensional process with rate `lambda`:

- `T_k ~ Gamma(k, lambda)`
- `W_k` are iid `Exp(lambda)`

This is the path-level form of memorylessness.

### Campbell's Formula

For a suitable deterministic function `f`,

`E[sum_{X in Pi} f(X)] = integral f(x) lambda(x) dx`.

This is the key identity for random sums over Poisson points.

## Structural Questions

The right questions are:

- is the process homogeneous or inhomogeneous?
- are the increments plausibly independent?
- does the model need marks, colors, or superposition?
- is clustering present, making a Poisson model too thin?

## Why This Matters for Quant Research

Poisson processes are useful as first models for:

- trade and order arrivals
- claims and default events
- news or jump arrivals
- marked event streams with sizes, venues, or types

Even when the final model is richer, the Poisson process is often the baseline from which dependence, seasonality, or self-excitation is diagnosed.

## Failure Modes

- fitting a homogeneous rate where strong time-of-day or regime variation exists
- confusing a Poisson marginal count fit with full process adequacy
- ignoring marks when event size or type is economically material
- using Poisson independence in obviously clustered or self-exciting data

## Practical Rule

Start with the intensity and the increment assumptions. If either is wrong, a Poisson-looking count distribution alone is not enough.

## Related Notes

- [[Continuous-Time Markov Chains]]
- [[Diffusion Processes]]
- [[Stochastic Calculus]]

## Sources

- [[Applied Probability]]
- [[Applied Probability - Ch 06 Poisson Processes]]
- [[All of Statistics]]
- [[All of Statistics - Ch 23 Probability Redux Stochastic Processes]]
