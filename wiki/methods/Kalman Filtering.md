---
title: Kalman Filtering
type: method
status: active
updated: 2026-04-23
tags:
  - method
  - kalman-filter
  - state-space
  - signal-processing
domain: quant-finance
sources:
  - "[[Kalman Filter Tutorial]]"
  - "[[Applied Time Series Analysis and Forecasting with Python]]"
  - "[[Bayesian Filtering and Smoothing]]"
  - "[[Time Series Analysis and Its Applications]]"
  - "[[Time Series Analysis by State Space Methods]]"
  - "[[Time Series Analysis by State Space Methods - Ch 02 Local Level Model]]"
  - "[[Time Series Analysis by State Space Methods - Ch 04 Filtering, Smoothing, and Forecasting]]"
  - "[[Time Series Analysis by State Space Methods - Ch 05 Initialisation of Filter and Smoother]]"
  - "[[Financial Signal Processing and Machine Learning]]"
---
# Kalman Filtering

## Summary

Kalman filtering is the recursive state-estimation method for linear Gaussian state-space models. It turns latent-state inference into a sequence of predictions, innovations, and updates.

In quant work it matters because many important objects are latent rather than directly observed: trend, fair value, exposure, signal strength, inventory pressure, or hidden volatility components.

## Core equations

In a linear Gaussian state-space model,
$$x_k = F_k x_{k-1} + w_k, \qquad z_k = H_k x_k + v_k,$$
with
$$w_k \sim (0,Q_k), \qquad v_k \sim (0,R_k).$$

Using the standard predicted-filtered notation, the Kalman filter recursion is
$$\hat{x}_{k \mid k-1} = F_k \hat{x}_{k-1 \mid k-1},$$
$$P_{k \mid k-1} = F_k P_{k-1 \mid k-1} F_k^\top + Q_k,$$
$$\nu_k = z_k - H_k \hat{x}_{k \mid k-1}, \qquad S_k = H_k P_{k \mid k-1} H_k^\top + R_k,$$
$$K_k = P_{k \mid k-1} H_k^\top S_k^{-1},$$
$$\hat{x}_{k \mid k} = \hat{x}_{k \mid k-1} + K_k \nu_k,$$
$$P_{k \mid k} = (I-K_kH_k)P_{k \mid k-1}.$$

The tutorial source uses prime notation for predicted quantities:
$$\hat{x}_k' \equiv \hat{x}_{k \mid k-1}, \qquad P_k' \equiv P_{k \mid k-1}.$$

## Core recursion logic

At each step the filter does four things:

- propagate the previous state forward
- form the one-step-ahead prediction error or innovation
- scale that innovation by the Kalman gain
- update both the state estimate and its uncertainty

The innovation is the load-bearing object. It drives both state updating and likelihood evaluation.

## What the filter is actually solving

In the linear Gaussian case, the filter gives the exact conditional mean and covariance of the latent state given data observed so far.

In a broader linear-estimation reading, it is the recursive minimum-variance linear unbiased update. That distinction matters because the recursions keep their value even when the Gaussian story is only approximate.

The short Tony Lacey tutorial makes the bridge explicit: if measurement noise is Gaussian, minimizing mean squared error and maximizing likelihood are driven by the same weighted residual logic.

## Gain, innovation, and uncertainty weighting

The gain is not a tuning knob in the original derivation. It is the solution to a covariance minimization problem. In the tutorial's notation,
$$K_k = P_k' H^\top \paren{H P_k' H^\top + R}^{-1},$$
and the posterior covariance update becomes
$$P_k = (I-K_kH)P_k'.$$

This makes the weighting logic transparent:

- larger prior uncertainty in the observed direction increases responsiveness
- larger measurement noise decreases responsiveness
- the innovation covariance
  $$S_k = H P_k' H^\top + R$$
  sets the scale of how surprising the incoming observation is

## Recursive least squares and information form

One of the strongest bridges from the tutorial is that the Kalman filter can be read as recursive least squares. The same update emerges from minimizing a rolling chi-square objective under linear Gaussian assumptions.

The equivalent information-form expressions are
$$K_k = \bracket{P_k'^{-1} + H^\top R^{-1} H}^{-1} H^\top R^{-1},$$
$$P_k^{-1} = P_k'^{-1} + H^\top R^{-1} H.$$

This matters because it gives three compatible readings of the same estimator:

- covariance form for uncertainty propagation
- information form for additive precision updating
- recursive least squares for sequential parameter fitting

## Source synthesis

- [[Kalman Filter Tutorial]] gives the shortest derivation through mean-squared-error minimization and the recursive least-squares view.
- [[Applied Time Series Analysis and Forecasting with Python]] gives a compact applied bridge from general state-space form to Kalman recursions, local-level models, and SARIMAX implementation.
- [[Bayesian Filtering and Smoothing]] places the Kalman filter inside the larger Bayesian state-space family and clarifies when extensions are needed.
- [[Time Series Analysis and Its Applications]] ties Kalman filtering to broader time-series and state-space practice.
- [[Time Series Analysis by State Space Methods]] is now the vault's most detailed technical source on the subject. It strengthens the local-level derivation, general multivariate recursions, disturbance smoothing, exact diffuse initialization, missing-observation handling, simulation smoothing, and innovations likelihood.
- [[Financial Signal Processing and Machine Learning]] shows why filtering matters for noisy financial signals and sequential decision problems.

## Assumptions

The classic Kalman filter relies on:

- a linear state transition model
- a linear observation model
- Gaussian process and observation noise
- correctly specified noise covariance structure, or at least a tolerable approximation
- a sensible initial state and covariance

When those assumptions fail badly, the model often needs an extended, unscented, Gaussian-approximate, or particle-filter alternative. Even before that, bad initialization can already corrupt early-sample inference, so exact diffuse treatment matters when the starting state is not properly known.

## Workflow

1. Define the latent state you actually care about.
2. Write the state transition equation for how that latent state evolves.
3. Write the observation equation connecting noisy data to the latent state.
4. Choose or estimate the process-noise and measurement-noise covariances.
5. Initialize the state estimate and uncertainty.
6. Run the prediction step forward.
7. Incorporate the next observation through the update step.
8. Inspect filtered states, innovations, and parameter sensitivity.
9. If needed, run smoothing, disturbance smoothing, or simulation smoothing on top of the filter output.
10. Use the innovation sequence for likelihood evaluation and diagnostics when fitting parameters.

## Diagnostics

- innovation sequence should be centered and structurally plausible
- innovation covariance and residual pattern should match the assumed model scale
- filtered state should not move only because the noise covariances were tuned aggressively
- parameter estimates should be stable across nearby windows and initializations
- one-step-ahead forecast errors should improve on naive alternatives
- the latent state should correspond to an interpretable economic or trading object

## Failure modes

- using the filter as a generic smoother without a defensible state model
- overfitting process and measurement variances to one sample period
- treating diffuse or uncertain starting states as harmless fixed constants
- treating filtered estimates as truth instead of posterior summaries with uncertainty
- ignoring structural breaks that invalidate transition dynamics
- applying the linear Gaussian filter where nonlinear or heavy-tailed structure dominates

## Quant use cases

- trend and fair-value extraction
- time-varying beta or spread estimation
- latent volatility or regime proxies
- microstructure noise filtering
- inventory-aware execution state tracking

## Related notes

- [[State Space Models]]
- [[Diffuse Initialization in State Space Models]]
- [[Simulation Smoothing]]
- [[Particle Filtering]]
- [[Bayesian Filtering and Smoothing]]
- [[Time Series Analysis by State Space Methods]]
- [[Time Series Analysis and Its Applications]]
- [[Financial Signal Processing and Machine Learning]]
- [[Signal Processing Map]]

## Sources

- [[Kalman Filter Tutorial]]
- [[Applied Time Series Analysis and Forecasting with Python]]
- [[Bayesian Filtering and Smoothing]]
- [[Time Series Analysis and Its Applications]]
- [[Time Series Analysis by State Space Methods]]
- [[Time Series Analysis by State Space Methods - Ch 02 Local Level Model]]
- [[Time Series Analysis by State Space Methods - Ch 04 Filtering, Smoothing, and Forecasting]]
- [[Time Series Analysis by State Space Methods - Ch 05 Initialisation of Filter and Smoother]]
- [[Financial Signal Processing and Machine Learning]]
