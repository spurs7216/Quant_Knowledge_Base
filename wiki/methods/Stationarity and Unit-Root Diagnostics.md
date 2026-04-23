---
title: Stationarity and Unit-Root Diagnostics
type: method
status: seed
updated: 2026-04-21
tags:
  - method
  - time-series
  - stationarity
  - unit-root
domain: statistics
sources:
  - "[[Time Series Analysis and Its Applications]]"
  - "[[Time Series Analysis and Its Applications - Ch 01 Characteristics of Time Series]]"
  - "[[Time Series Analysis and Its Applications - Ch 05 Additional Time Domain Topics]]"
  - "[[Applied Time Series Analysis and Forecasting with Python]]"
---
# Stationarity and Unit-Root Diagnostics

## Summary

Stationarity and unit-root diagnostics answer a basic time-series question before model fitting:

- is the observed series already stable enough to model in levels?
- does it need deterministic adjustment such as detrending or seasonal removal?
- does it require differencing because the persistence is stochastic rather than deterministic?

The point is not to force every series into stationarity at any cost. The point is to define a target whose dependence structure is stable enough to support inference, forecasting, and residual diagnostics.

## Core objects

- strict stationarity versus weak stationarity
- trend stationarity versus difference stationarity
- unit root in the autoregressive polynomial
- first and seasonal differencing
- sample ACF and PACF
- unit-root null `H0: phi = 1` against a stationary alternative
- overdifferencing and underdifferencing

## Why it matters

Many downstream errors are really stationarity errors in disguise:

- fitting ARIMA to a deterministic trend that should have been removed directly
- differencing away economically meaningful long-run level information
- mistaking near-unit-root persistence for stable short-memory dynamics
- interpreting residual ACFs as model failure when the target itself was framed badly

Good diagnostics here reduce false complexity later.

## Workflow

1. Plot the raw series and identify obvious level shifts, deterministic trend, seasonality, variance changes, and missing-data pathologies.
2. Decide whether the modeling target should be the level, log-level, return, spread, or another transformed object.
3. Use the sample ACF and PACF to see whether persistence looks short-memory, near-unit-root, seasonal, or obviously unstable.
4. Remove deterministic components first when they are clearly part of the data-generating story.
5. Use unit-root tests as supporting evidence, not as the whole decision rule.
6. After differencing or detrending, re-check whether the resulting series now has a defensible mean and covariance structure.
7. Prefer the least destructive transformation that yields a stable target for the actual forecast or inference problem.

## Diagnostics

- the sample ACF should stop looking like a near-flat wall of persistence if the transformation was appropriate
- residual series after detrending or differencing should not exhibit obvious deterministic structure
- strong negative lag-1 autocorrelation after differencing can signal overdifferencing
- tests and plots should be interpreted alongside structural-break risk and domain knowledge

## Failure modes

- treating unit-root tests as automatic differencing commands
- confusing deterministic trend with stochastic trend
- ignoring seasonal nonstationarity while focusing only on lag-1 persistence
- using returns because they are fashionable even when the research object is an equilibrium spread or level relation
- declaring stationarity from one test while the plot still shows clear instability

## Quant relevance

This note is central for:

- macro and fundamental forecasting
- spread construction and mean-reversion work
- volatility and residual modeling
- deciding when price levels should become returns and when they should not
- separating persistent signal from nonstationary nuisance

## Related notes

- [[Time-Series Forecasting]]
- [[ARIMA and Box-Jenkins Modeling]]
- [[Long Memory and Fractional Differencing]]
- [[Cointegration and Error Correction Models]]
- [[Time Series Analysis and Its Applications]]

## Sources

- [[Time Series Analysis and Its Applications]]
- [[Time Series Analysis and Its Applications - Ch 01 Characteristics of Time Series]]
- [[Time Series Analysis and Its Applications - Ch 05 Additional Time Domain Topics]]
- [[Applied Time Series Analysis and Forecasting with Python]]
