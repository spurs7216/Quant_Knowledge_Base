---
title: Point Process Methods for Extremes
type: method
status: seed
updated: 2026-04-22
tags:
  - method
  - extreme-value-theory
  - point-process
  - exceedances
domain: statistics
sources:
  - "[[Modelling Extremal Events for insurance and finance]]"
  - "[[Modelling Extremal Events for insurance and finance - Ch 05 An Approach to Extremes via Point Processes]]"
  - "[[Modelling Extremal Events for insurance and finance - Ch 08 Special Topics]]"
---
# Point Process Methods for Extremes

## Summary

Point-process methods are the cleanest unifying layer behind maxima, exceedances, upper order statistics, records, and clustered extremes. They replace one scalar extreme with a random cloud of rare events and then study the cloud's limit.

## Core equations

For high-level exceedances or normalized extremes, the basic object is
$$N_n=\sum_{i=1}^n \delta_{(i/n,\;X_i/a_n)}.$$

In the iid Pareto-type regime, $N_n$ converges to a Poisson random measure $N$ with intensity
$$\mathrm{d}t \times \nu(\mathrm{d}x), \qquad \nu(x,\infty]=x^{-\alpha}.$$

Under stronger dependence, the limit is often compound Poisson rather than simple Poisson, which is exactly where extremal clustering enters.

## Main logic

### 1. Maxima are projections of the point process

The maximum is just the top point of the cloud. So block-maximum limits can be derived from the same object that governs exceedances.

### 2. Order statistics and threshold exceedances are natural by-products

Once the full rare-event cloud is controlled, upper order statistics and exceedance counts stop looking like separate theories.

### 3. Dependence changes the limit from Poisson to compound Poisson

That is the clean route from iid EVT to clustered extremes and the extremal index.

## Workflow

1. Choose a normalization or threshold sequence that isolates rare events.
2. Construct the exceedance or extremal point process.
3. Identify whether the limiting object should be Poisson or compound Poisson.
4. Recover maxima, order statistics, cluster sizes, or record counts as projections of the same limit object.

## Failure modes

- treating block maxima and threshold exceedances as unrelated methods
- using Poisson logic when dependence clearly induces clustering
- fitting the point-process asymptotic without checking the tail normalization regime

## Quant relevance

This method matters for:

- unifying block-maxima and peaks-over-threshold workflows
- modeling clustered exceedances in dependent stress periods
- reasoning about records, upper order statistics, and extremal counts
- moving from scalar tail estimates to event-process thinking

## Related notes

- [[Extreme Value Theory for Maxima and Threshold Exceedances]]
- [[Extremal Index and Clustering of Extremes]]
- [[Tail Index Estimation]]
- [[Regular Variation and Heavy-Tailed Distributions]]

## Sources

- [[Modelling Extremal Events for insurance and finance]]
- [[Modelling Extremal Events for insurance and finance - Ch 05 An Approach to Extremes via Point Processes]]
- [[Modelling Extremal Events for insurance and finance - Ch 08 Special Topics]]
