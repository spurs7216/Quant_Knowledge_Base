---
title: Long Memory and Fractional Differencing
type: method
status: seed
updated: 2026-04-21
tags:
  - method
  - time-series
  - long-memory
  - arfima
domain: statistics
sources:
  - "[[Time Series Analysis and Its Applications]]"
  - "[[Time Series Analysis and Its Applications - Ch 05 Additional Time Domain Topics]]"
---
# Long Memory and Fractional Differencing

## Summary

Long-memory models describe series whose dependence decays too slowly for standard short-memory ARMA behavior, but not so strongly that a full unit-root model is the right description.

The basic device is fractional differencing:

`(1 - B)^d x_t = w_t`

with `0 < d < .5` as the canonical stationary long-memory case.

## Core logic

- short-memory ARMA models have exponentially decaying autocorrelation
- unit-root models have nonstationary persistence
- fractional differencing interpolates between these cases through a non-integer `d`
- ARFIMA extends the idea by combining fractional differencing with ARMA structure

## Workflow

1. Start from the plot and ACF and check whether persistence decays unusually slowly.
2. Rule out simpler deterministic trend or seasonal explanations first.
3. Compare the behavior of a differenced model against a fractional-difference candidate.
4. Estimate `d` and inspect whether the fitted residuals still show substantial structure.
5. Only keep long-memory structure if it materially improves the explanation over simpler short-memory or integrated alternatives.

## Assumptions

- the persistence pattern is stable enough to model
- slow decay is not merely a symptom of structural breaks or bad preprocessing
- the data length is long enough to separate long memory from near-unit-root behavior

## Failure modes

- diagnosing long memory from one slow-looking ACF without ruling out breaks
- using fractional differencing where a deterministic trend or regime change is the real issue
- treating estimated `d` as economically meaningful when it is only compensating for bad target construction

## Quant relevance

This note matters for:

- macro or environmental series with persistent dependence
- volatility or flow series that look more persistent than ARMA but less than random walk
- deciding when first differencing is too destructive

## Related notes

- [[Stationarity and Unit-Root Diagnostics]]
- [[ARIMA and Box-Jenkins Modeling]]
- [[Time-Series Forecasting]]
- [[Time Series Analysis and Its Applications]]

## Sources

- [[Time Series Analysis and Its Applications]]
- [[Time Series Analysis and Its Applications - Ch 05 Additional Time Domain Topics]]
