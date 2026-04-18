---
title: Time-Series Forecasting
type: method
status: seed
updated: 2026-04-18
tags:
  - method
  - time-series
  - forecasting
  - statistics
domain: quant-finance
sources:
  - "[[Time Series Analysis and Its Applications]]"
  - "[[Financial Signal Processing and Machine Learning]]"
  - "[[Statistics and Data Analysis for Financial Engineering]]"
  - "[[Financial Machine Learning Workflow]]"
---
# Time-Series Forecasting

## Summary

Time-series forecasting is the problem of predicting future values or distributions from serially dependent data. In a quant context, that means forecasting not only prices and returns, but also volatility, spreads, order flow, macro states, realized risk, and latent components that matter for trading and risk decisions.

## What It Does

Forecasting methods help the researcher:

- convert temporal dependence into predictive structure
- separate level, trend, seasonality, and shock components
- generate horizon-specific forecasts rather than generic "predictions"
- compare model classes under realistic time ordering
- link signal extraction with trading, sizing, and risk horizons

## Source Synthesis

- [[Time Series Analysis and Its Applications]] gives the broadest statistical foundation across ARIMA, spectral methods, and state-space models.
- [[Financial Signal Processing and Machine Learning]] emphasizes filtering, denoising, and signal extraction in noisy market data.
- [[Statistics and Data Analysis for Financial Engineering]] connects forecasting problems to financial data pathologies and practical diagnostics.
- [[Financial Machine Learning Workflow]] clarifies that forecasting performance is meaningless if validation leaks or trading alignment is wrong.

## Assumptions

Assumptions vary by model, but the recurring ones are:

- the target and forecast horizon are clearly defined
- the training data represent the same decision problem as the evaluation data
- serial dependence, seasonality, and structural breaks are handled rather than ignored
- the forecast loss matches the real objective
- data timing, revisions, and publication lags are aligned correctly

## Workflow

1. Define the target, horizon, and decision use of the forecast.
2. Establish the timestamp convention and remove any look-ahead leakage.
3. Build simple baselines before escalating model complexity.
4. Inspect dependence structure, nonstationarity, seasonality, and scale changes.
5. Choose a model class consistent with the signal and horizon.
6. Validate strictly forward in time with rolling or expanding windows.
7. Evaluate both statistical loss and downstream economic usefulness.
8. Stress the model across regimes, frequencies, and alternative feature sets.

## Diagnostics

- compare against naive baselines such as random walk, last value, or historical mean
- inspect residual autocorrelation and conditional heteroskedasticity
- check forecast stability across adjacent windows
- compare performance by regime, asset class, and horizon
- inspect whether forecast gains survive transaction costs and turnover

## Failure Modes

- confusing in-sample fit with out-of-sample forecast skill
- evaluating with random cross-validation that breaks time dependence
- optimizing one horizon and trading another
- ignoring revisions, stale fundamentals, or release lags
- overreacting to nonstationarity with excessive complexity instead of better framing

## Quant Use Cases

- volatility and risk forecasting
- spread and mean-reversion horizon estimation
- macro nowcasting and release-response modeling
- order-flow and execution forecasting
- latent-state and regime-based prediction pipelines

## Related Notes

- [[Kalman Filtering]]
- [[Financial Machine Learning Workflow]]
- [[Panel Data]]
- [[Stats Map]]

## Sources

- [[Time Series Analysis and Its Applications]]
- [[Financial Signal Processing and Machine Learning]]
- [[Statistics and Data Analysis for Financial Engineering]]
- [[Financial Machine Learning Workflow]]
