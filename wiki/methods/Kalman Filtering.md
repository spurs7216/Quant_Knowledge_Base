---
title: Kalman Filtering
type: method
status: seed
updated: 2026-04-18
tags:
  - method
  - kalman-filter
  - state-space
  - signal-processing
domain: quant-finance
sources:
  - "[[Kalman Filter Tutorial]]"
  - "[[Bayesian Filtering and Smoothing]]"
  - "[[Time Series Analysis and Its Applications]]"
  - "[[Financial Signal Processing and Machine Learning]]"
---
# Kalman Filtering

## Summary

Kalman filtering is a recursive state-estimation method for linear Gaussian state-space models. In quant research it matters because many important objects are latent rather than directly observed: trend, volatility state, fair value, signal strength, inventory pressure, and hidden regime components.

## What It Does

Kalman filtering lets the researcher:

- combine a dynamic state model with noisy observations
- update latent-state estimates sequentially as new data arrives
- propagate uncertainty through both prediction and update steps
- smooth noisy signals without fully discarding model structure
- turn hidden-state modeling into an online estimation workflow

## Source Synthesis

- [[Kalman Filter Tutorial]] gives the shortest derivation through mean-squared-error minimization and the recursive least-squares view.
- [[Bayesian Filtering and Smoothing]] places the Kalman filter inside the larger Bayesian state-space family and clarifies when extensions are needed.
- [[Time Series Analysis and Its Applications]] ties Kalman filtering to broader time-series and state-space practice.
- [[Financial Signal Processing and Machine Learning]] shows why filtering matters for noisy financial signals and sequential decision problems.

## Assumptions

The classic Kalman filter relies on:

- a linear state transition model
- a linear observation model
- Gaussian process and observation noise
- correctly specified noise covariance structure, or at least a tolerable approximation
- a sensible initial state and covariance

When those assumptions fail badly, the model often needs an extended, unscented, Gaussian-approximate, or particle-filter alternative.

## Workflow

1. Define the latent state you actually care about.
2. Write the state transition equation for how that latent state evolves.
3. Write the observation equation connecting noisy data to the latent state.
4. Choose or estimate the process-noise and measurement-noise covariances.
5. Initialize the state estimate and uncertainty.
6. Run the prediction step forward.
7. Incorporate the next observation through the update step.
8. Inspect filtered states, innovations, and parameter sensitivity.
9. If needed, run a smoothing pass or estimate parameters jointly.

## Diagnostics

- innovation sequence should be centered and structurally plausible
- filtered state should not move only because the noise covariances were tuned aggressively
- parameter estimates should be stable across nearby windows and initializations
- one-step-ahead forecast errors should improve on naive alternatives
- the latent state should correspond to an interpretable economic or trading object

## Failure Modes

- using the filter as a generic smoother without a defensible state model
- overfitting process and measurement variances to one sample period
- treating filtered estimates as truth instead of posterior summaries with uncertainty
- ignoring structural breaks that invalidate transition dynamics
- applying the linear Gaussian filter where nonlinear or heavy-tailed structure dominates

## Quant Use Cases

- trend and fair-value extraction
- time-varying beta or spread estimation
- latent volatility or regime proxies
- microstructure noise filtering
- inventory-aware execution state tracking

## Related Notes

- [[Bayesian Filtering and Smoothing]]
- [[Time Series Analysis and Its Applications]]
- [[Financial Signal Processing and Machine Learning]]
- [[Signal Processing Map]]

## Sources

- [[Kalman Filter Tutorial]]
- [[Bayesian Filtering and Smoothing]]
- [[Time Series Analysis and Its Applications]]
- [[Financial Signal Processing and Machine Learning]]
