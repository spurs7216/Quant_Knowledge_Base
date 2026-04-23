---
title: State Space Models
type: method
status: seed
updated: 2026-04-21
tags:
  - method
  - time-series
  - state-space
  - kalman
domain: statistics
sources:
  - "[[Applied Time Series Analysis and Forecasting with Python]]"
  - "[[Applied Time Series Analysis and Forecasting with Python - Ch 08 State Space Models and Markov Switching Models]]"
  - "[[Time Series Analysis and Its Applications]]"
  - "[[Time Series Analysis by State Space Methods]]"
  - "[[Time Series Analysis by State Space Methods - Ch 03 Linear State Space Models]]"
  - "[[Time Series Analysis by State Space Methods - Ch 04 Filtering, Smoothing, and Forecasting]]"
  - "[[Time Series Analysis by State Space Methods - Ch 05 Initialisation of Filter and Smoother]]"
---
# State Space Models

## Summary

State-space models represent observed data through latent dynamic states plus an observation layer. They are a modeling class, not a single algorithm.

The basic split is:

- state equation: how the latent system evolves
- observation equation: how data are generated from that latent system

This language unifies structural decomposition, ARIMA embeddings, dynamic regression, dynamic factors, spline smoothing, and many nonlinear or non-Gaussian extensions.

## Core equations and objects

In the linear Gaussian case:

- `alpha_{t+1} = c_t + T_t alpha_t + R_t eta_t`
- `y_t = d_t + Z_t alpha_t + epsilon_t`

with process noise and observation noise carrying separate uncertainty roles.

Recurring objects:

- latent state `alpha_t`
- observation `y_t`
- transition matrix `T_t`
- measurement matrix `Z_t`
- disturbance loading `R_t`
- observation covariance `H_t`
- state covariance `Q_t`
- filtered, predicted, and smoothed state estimates
- innovations and their covariance matrices

## Main logic

The power of state-space form is that modeling and computation line up:

- ARIMA-type dynamics can be embedded in latent-state form
- regression models can be given dynamic coefficients
- forecasting, filtering, smoothing, and likelihood evaluation become one sequential estimation problem

The local-level model is the cleanest example: it is both a latent random-walk trend model and an `ARIMA(0,1,1)` representation after differencing. The more general lesson is that state-space form preserves interpretable latent structure while still giving an operational inference engine.

## Inference layers inside the model class

Once the model is specified, the main tasks become:

- prediction from time `t` to `t+1`
- update after the next observation arrives
- smoothing using future information
- disturbance smoothing for shock-level diagnosis
- simulation smoothing for latent-path draws
- likelihood-based parameter estimation from innovations
- exact diffuse initialization when the starting state is not properly known

This is why state-space form is more than notation. It is a computational language for latent-state inference.

## Model families this language unifies

- latent trend and fair-value estimation
- structural trend, seasonal, and cycle decomposition
- ARIMA and regression-with-ARMA-errors embeddings
- time-varying beta and exposure tracking
- dynamic regression with exogenous variables
- dynamic factor models
- spline smoothing and benchmarking
- noisy measurement systems
- nonlinear and non-Gaussian extensions such as stochastic volatility or particle-filter settings

## Assumptions and diagnostics

The linear Gaussian core assumes:

- linear transition and observation structure
- defensible disturbance covariances
- meaningful initialization of the latent state
- innovations that are structurally plausible under the model

Diagnostics should focus on:

- innovation behavior and forecast-error structure
- sensitivity to initialization choices
- whether the latent state is economically interpretable
- whether a simpler ARIMA or regression representation would do the job just as well

## Failure modes

- using state-space language without a defensible state definition
- tuning noise covariances until the filter looks smooth rather than realistic
- treating initialization as a coding detail instead of part of the model
- forgetting that filtered states are estimates with uncertainty, not truth
- hiding misspecification inside a flexible latent structure

## Quant relevance

This note sits one level above specific filters. It provides the modeling class within which Kalman filtering, diffuse initialization, simulation smoothing, dynamic-factor models, and many SARIMAX-style systems live.

## Related notes

- [[Kalman Filtering]]
- [[Diffuse Initialization in State Space Models]]
- [[Simulation Smoothing]]
- [[Dynamic Factor Models]]
- [[Particle Filtering]]
- [[Time-Series Forecasting]]
- [[Time Series Analysis by State Space Methods]]

## Sources

- [[Applied Time Series Analysis and Forecasting with Python]]
- [[Applied Time Series Analysis and Forecasting with Python - Ch 08 State Space Models and Markov Switching Models]]
- [[Time Series Analysis and Its Applications]]
- [[Time Series Analysis by State Space Methods]]
- [[Time Series Analysis by State Space Methods - Ch 03 Linear State Space Models]]
- [[Time Series Analysis by State Space Methods - Ch 04 Filtering, Smoothing, and Forecasting]]
- [[Time Series Analysis by State Space Methods - Ch 05 Initialisation of Filter and Smoother]]
