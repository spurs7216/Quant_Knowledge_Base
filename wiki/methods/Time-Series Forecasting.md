---
title: Time-Series Forecasting
type: method
status: seed
updated: 2026-04-20
tags:
  - method
  - time-series
  - forecasting
  - statistics
domain: quant-finance
sources:
  - "[[Applied Time Series Analysis and Forecasting with Python]]"
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

- [[Applied Time Series Analysis and Forecasting with Python]] is the best current applied bridge in the vault from stationarity and ARIMA workflow into volatility, VAR, state-space, and cointegration modeling with executable diagnostics.
- [[Time Series Analysis and Its Applications]] gives the broadest statistical foundation across ARIMA, spectral methods, and state-space models.
- [[Financial Signal Processing and Machine Learning]] emphasizes filtering, denoising, and signal extraction in noisy market data.
- [[Statistics and Data Analysis for Financial Engineering]] connects forecasting problems to financial data pathologies and practical diagnostics.
- [[Financial Machine Learning Workflow]] clarifies that forecasting performance is meaningless if validation leaks or trading alignment is wrong.

## Model Families

- [[ARIMA and Box-Jenkins Modeling]] is the baseline for univariate mean dynamics after transformation and differencing.
- [[Stationarity and Unit-Root Diagnostics]] matters before model choice whenever the main question is whether the series should be modeled in levels, detrended form, or differences.
- [[GARCH Models]] matter when the main predictability is in conditional variance rather than conditional mean.
- [[Long Memory and Fractional Differencing]] matters when persistence looks too slow for short-memory ARMA structure but differencing still seems too destructive.
- [[Vector Autoregression and Impulse Response Analysis]] matters when the forecast object is a dynamic system rather than one series.
- [[Transfer Function Models]] matter when one time series drives another with delay, persistence, and a dynamic response shape.
- [[Spectral Analysis and Filtering]] matters when the predictive or diagnostic structure is horizon-specific, periodic, or fundamentally a signal-extraction problem.
- [[State Space Models]] matter when the main signal is latent, noisy, or time-varying.
- [[Cointegration and Error Correction Models]] matter when levels are nonstationary but economically meaningful spreads or equilibrium relations may still be stationary.
- [[Kalman Filtering]] is the online estimation workhorse inside the linear Gaussian state-space family.
- [[Hidden Markov Models and Switching Autoregression]] matter when the dynamics plausibly change across persistent latent regimes.

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
4. Classify the series: stationary, transformable to stationarity, volatility-driven, system-driven, latent-state-driven, or cointegrated.
5. Choose a model family consistent with that failure mode rather than by popularity.
6. Validate strictly forward in time with rolling or expanding windows.
7. Diagnose residual mean dependence, variance dependence, and regime instability.
8. Evaluate both statistical loss and downstream economic usefulness.
9. Stress the model across regimes, frequencies, and alternative feature sets.

## Diagnostics

- compare against naive baselines such as random walk, last value, or historical mean
- inspect residual autocorrelation and conditional heteroskedasticity
- check whether differencing or detrending was appropriate rather than automatic
- check forecast stability across adjacent windows
- compare performance by regime, asset class, and horizon
- inspect whether forecast gains survive transaction costs and turnover

## Failure Modes

- confusing in-sample fit with out-of-sample forecast skill
- evaluating with random cross-validation that breaks time dependence
- optimizing one horizon and trading another
- ignoring revisions, stale fundamentals, or release lags
- forcing every series into one model family instead of matching the model to the dependence structure
- treating in-sample fit as evidence that the underlying dynamic object was specified correctly
- overreacting to nonstationarity with excessive complexity instead of better framing

## Quant Use Cases

- volatility and risk forecasting
- spread and mean-reversion horizon estimation
- macro nowcasting and release-response modeling
- order-flow and execution forecasting
- latent-state and regime-based prediction pipelines

## Related Notes

- [[ARIMA and Box-Jenkins Modeling]]
- [[GARCH Models]]
- [[Vector Autoregression and Impulse Response Analysis]]
- [[State Space Models]]
- [[Cointegration and Error Correction Models]]
- [[Kalman Filtering]]
- [[Stationarity and Unit-Root Diagnostics]]
- [[Spectral Analysis and Filtering]]
- [[Long Memory and Fractional Differencing]]
- [[Transfer Function Models]]
- [[Hidden Markov Models and Switching Autoregression]]
- [[Financial Machine Learning Workflow]]
- [[Panel Data]]
- [[Stats Map]]

## Sources

- [[Applied Time Series Analysis and Forecasting with Python]]
- [[Time Series Analysis and Its Applications]]
- [[Financial Signal Processing and Machine Learning]]
- [[Statistics and Data Analysis for Financial Engineering]]
- [[Financial Machine Learning Workflow]]
