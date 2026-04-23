---
title: Vector Autoregression and Impulse Response Analysis
type: method
status: seed
updated: 2026-04-20
tags:
  - method
  - time-series
  - var
  - impulse-response
domain: econometrics
sources:
  - "[[Applied Time Series Analysis and Forecasting with Python]]"
  - "[[Applied Time Series Analysis and Forecasting with Python - Ch 07 Multivariate Time Series Analysis]]"
---
# Vector Autoregression and Impulse Response Analysis

## Summary

VAR models extend univariate autoregression to systems:

`X_t = nu + Phi_1 X_{t-1} + ... + Phi_p X_{t-p} + epsilon_t`

They are useful when several time series evolve jointly and each variable may depend on its own lags and the lags of the others.

## Core logic

The point of a VAR is not only joint forecasting. It is also structured dynamic interpretation:

- which variables help predict which others?
- how do shocks propagate through the system?
- how persistent are those effects?

The practical answer comes from two tools:

- Granger-causality tests for predictive directionality
- impulse response analysis for horizon-by-horizon shock propagation

## Workflow

1. Stabilize the system so the modeled target is stationary enough.
2. Choose a candidate order `p` using information criteria or FPE.
3. Estimate the coefficient matrices.
4. Diagnose the residual vector process with multivariate whiteness checks.
5. Only then interpret Granger-causality or impulse-response outputs.

## Why impulse responses matter

A VAR coefficient table is hard to interpret directly. The VMA representation

`X_t = sum_h Psi_h epsilon_{t-h}`

turns the coefficients into shock paths:

- `Psi_h` gives the response at horizon `h`
- cumulative responses describe medium- and long-run effects

This is the system-level analog of asking what one unexpected shock does to future states.

## Failure modes

- fitting VARs to nonstationary levels without cointegration logic
- confusing Granger causality with structural or intervention causality
- interpreting impulse responses before residual adequacy is established
- using high-dimensional VARs without respecting parameter explosion

## Quant relevance

This method matters for:

- macro and cross-asset forecasting systems
- shock propagation analysis
- understanding dynamic relationships among yields, spreads, flows, and returns
- turning multivariate predictive structure into interpretable horizon effects

## Related notes

- [[Time-Series Forecasting]]
- [[Cointegration and Error Correction Models]]
- [[Applied Time Series Analysis and Forecasting with Python]]

## Sources

- [[Applied Time Series Analysis and Forecasting with Python]]
- [[Applied Time Series Analysis and Forecasting with Python - Ch 07 Multivariate Time Series Analysis]]
