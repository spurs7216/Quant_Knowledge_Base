---
title: Transfer Function Models
type: method
status: seed
updated: 2026-04-21
tags:
  - method
  - time-series
  - transfer-function
  - dynamic-regression
domain: statistics
sources:
  - "[[Time Series Analysis and Its Applications]]"
  - "[[Time Series Analysis and Its Applications - Ch 05 Additional Time Domain Topics]]"
  - "[[Time Series Analysis and Its Applications - Ch 04 Spectral Analysis and Filtering]]"
---
# Transfer Function Models

## Summary

Transfer function models are dynamic regressions in which the output depends on filtered lagged values of one or more input series plus its own noise model.

They are useful when the effect of an input is delayed, distributed over time, or dynamically damped rather than purely contemporaneous.

## Core logic

- static regression is too weak when the input-output relation is delayed or persistent
- the transfer function captures delay and dynamic response through lag polynomials
- the remaining unexplained component still needs its own time-series noise model
- prewhitening is often needed before cross-correlation can identify the dynamic relation cleanly

## Workflow

1. Define the output and candidate input series clearly.
2. Model and prewhiten the input series.
3. Filter the output through the same prewhitening filter.
4. Inspect the cross-correlation structure of the filtered series to detect delay and dynamic shape.
5. Propose a parsimonious transfer function plus a separate noise model.
6. Diagnose whether residual serial dependence remains after fitting.

## Assumptions

- the input-output relation is approximately linear over the modeled range
- timing is correctly aligned
- the noise model is strong enough that remaining residual dependence is not being mistaken for input effect

## Failure modes

- reading raw CCF peaks without prewhitening
- fitting distributed lags while residual dynamics are still misspecified
- confusing contemporaneous correlation with a dynamic causal input effect
- using too many lag terms when a lower-order transfer function is enough

## Quant relevance

This note matters for:

- macro release or policy transmission problems
- delayed market-impact or order-flow effects
- input-output forecasting where one series drives another with lag and persistence

## Related notes

- [[Spectral Analysis and Filtering]]
- [[Time-Series Forecasting]]
- [[Vector Autoregression and Impulse Response Analysis]]
- [[Time Series Analysis and Its Applications]]

## Sources

- [[Time Series Analysis and Its Applications]]
- [[Time Series Analysis and Its Applications - Ch 05 Additional Time Domain Topics]]
- [[Time Series Analysis and Its Applications - Ch 04 Spectral Analysis and Filtering]]
