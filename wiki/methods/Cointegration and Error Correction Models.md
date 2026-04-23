---
title: Cointegration and Error Correction Models
type: method
status: seed
updated: 2026-04-20
tags:
  - method
  - time-series
  - cointegration
  - vecm
domain: econometrics
sources:
  - "[[Applied Time Series Analysis and Forecasting with Python]]"
  - "[[Applied Time Series Analysis and Forecasting with Python - Ch 09 Nonstationarity and Cointegrations]]"
---
# Cointegration and Error Correction Models

## Summary

Cointegration is the correct way to model long-run relationships among nonstationary variables. If a vector process is `I(1)` but some linear combination `beta' X_t` is stationary, then the variables share an equilibrium relation even though their levels individually wander.

The practical dynamic form is the vector error-correction model:

`nabla X_t = alpha beta' X_{t-1} + sum Gamma_h nabla X_{t-h} + epsilon_t`

## Core logic

The method exists to solve a specific problem:

- regressions on unrelated nonstationary levels can look significant
- differencing everything can destroy long-run equilibrium information

Cointegration is the middle path:

- preserve the long-run relation through `beta' X_t`
- model short-run adjustments through differenced terms and loading matrix `alpha`

## Workflow

1. Check whether the component series are plausibly `I(1)`.
2. Test whether some stationary linear combination exists.
3. Estimate the cointegrating relation and cointegration rank.
4. Fit an error-correction form if cointegration is supported.
5. Interpret `alpha` as adjustment speed and `beta` as equilibrium structure.

## What it protects against

- spurious regression on levels
- false economic stories driven by shared stochastic trends that are not equilibrium relations
- over-differencing away the very spread or equilibrium object that matters

## Failure modes

- assuming similar-looking level series must be cointegrated
- skipping unit-root checks
- treating Granger causality as a substitute for cointegration logic
- interpreting one cointegrating vector as economically unique when normalization choices matter

## Quant relevance

This method is central when the research object is a spread, basis, parity relation, yield linkage, or macro equilibrium story. It is especially important whenever a forecast thesis depends on "mean reversion in levels" rather than only in returns or differences.

## Related notes

- [[Vector Autoregression and Impulse Response Analysis]]
- [[Time-Series Forecasting]]
- [[Applied Time Series Analysis and Forecasting with Python]]

## Sources

- [[Applied Time Series Analysis and Forecasting with Python]]
- [[Applied Time Series Analysis and Forecasting with Python - Ch 09 Nonstationarity and Cointegrations]]
