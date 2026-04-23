---
title: Dynamic Factor Models
type: method
status: seed
updated: 2026-04-21
tags:
  - method
  - time-series
  - state-space
  - factor-model
domain: statistics
sources:
  - "[[Time Series Analysis by State Space Methods]]"
  - "[[Time Series Analysis by State Space Methods - Ch 03 Linear State Space Models]]"
---
# Dynamic Factor Models

## Summary

Dynamic factor models represent many observed series through a smaller set of latent dynamic factors plus idiosyncratic components.

In state-space language, the factors are latent states, the observations load on those states, and the factor dynamics evolve over time.

## Core logic

- many observed series share lower-dimensional common dynamics
- latent factors capture the common part
- idiosyncratic disturbances capture series-specific residual structure
- state-space form makes filtering, smoothing, forecasting, and missing-data handling natural

## Workflow

1. Decide what common dynamic structure is plausible across the observed series.
2. Specify factor dynamics and observation loadings.
3. Fit the model in state-space form.
4. Use filtered or smoothed factors to study common movement, forecasting, or latent regime evolution.
5. Check whether the idiosyncratic residual structure is still too strong for the chosen factor dimension.

## Failure modes

- using factors as a compression device without a clear interpretation of common versus idiosyncratic dynamics
- forcing too few factors and leaving common structure in the residuals
- overfitting the factor dimension because filtered factors look smooth

## Quant relevance

This note matters for:

- yield-curve and term-structure modeling
- macro nowcasting with many indicators
- multivariate risk and latent-state tracking
- reducing large systems into a smaller set of dynamic drivers

## Related notes

- [[State Space Models]]
- [[Kalman Filtering]]
- [[Time-Series Forecasting]]
- [[Time Series Analysis by State Space Methods]]

## Sources

- [[Time Series Analysis by State Space Methods]]
- [[Time Series Analysis by State Space Methods - Ch 03 Linear State Space Models]]
