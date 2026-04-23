---
title: Extreme Value Theory for Maxima and Threshold Exceedances
type: method
status: seed
updated: 2026-04-22
tags:
  - method
  - extreme-value-theory
  - maxima
  - threshold-exceedances
domain: statistics
sources:
  - "[[Modelling Extremal Events for insurance and finance]]"
  - "[[Modelling Extremal Events for insurance and finance - Ch 03 Fluctuations of Maxima]]"
  - "[[Modelling Extremal Events for insurance and finance - Ch 05 An Approach to Extremes via Point Processes]]"
  - "[[Modelling Extremal Events for insurance and finance - Ch 06 Statistical Methods for Extremal Events]]"
---
# Extreme Value Theory for Maxima and Threshold Exceedances

## Summary

Extreme value theory provides the asymptotic modeling layer for rare events beyond the data range. It has two main operational routes:

- block maxima modeled by the generalized extreme-value family
- peaks over threshold modeled by the generalized Pareto family

## Core equations

For maxima, if suitable norming constants exist,
$$\frac{M_n-d_n}{c_n}\Rightarrow H,$$
then $H$ must be Frechet, Weibull, or Gumbel.

For threshold exceedances over a high level $u$,
$$F_u(y)=\Prob(X-u\le y \given X>u)$$
is approximated by a generalized Pareto law,
$$G_{\xi,\beta}(y)=1-\paren{1+\xi y/\beta}^{-1/\xi}.$$

## Main logic

### 1. Block maxima answer worst-case-over-horizon questions

Use the maxima route when the natural research object is one extreme per block: worst daily loss per month, yearly flood height, or quarterly maximum stress.

### 2. Threshold exceedances use more tail data

Use the threshold route when the goal is tail-shape estimation or high-quantile extrapolation and many observations above a high cutoff can be retained.

### 3. Point-process convergence unifies both views

Maxima, order statistics, and exceedances are not separate theories. They are projections of the same rare-event point-process limit.

## Workflow

1. Diagnose whether the upper tail is plausibly in an EVT regime.
2. Decide whether the target is a block maximum or a threshold exceedance problem.
3. Choose block size or threshold high enough that asymptotics are defensible.
4. Fit the tail-shape and scale parameters.
5. Stress-test the extrapolation with stability plots and sensitivity to threshold or block choice.

## Failure modes

- treating EVT as magic extrapolation rather than asymptotic approximation
- choosing thresholds or block sizes mechanically
- fitting iid EVT to clustered dependent extremes without correction
- reporting extreme quantiles without sensitivity ranges

## Quant relevance

This method matters for:

- crash-loss modeling
- extreme VaR or expected-shortfall extrapolation
- catastrophe-like stress scenarios
- blockwise worst-case calibration

## Related notes

- [[Tail Index Estimation]]
- [[Regular Variation and Heavy-Tailed Distributions]]
- [[Extremal Index and Clustering of Extremes]]

## Sources

- [[Modelling Extremal Events for insurance and finance]]
- [[Modelling Extremal Events for insurance and finance - Ch 03 Fluctuations of Maxima]]
- [[Modelling Extremal Events for insurance and finance - Ch 05 An Approach to Extremes via Point Processes]]
- [[Modelling Extremal Events for insurance and finance - Ch 06 Statistical Methods for Extremal Events]]
