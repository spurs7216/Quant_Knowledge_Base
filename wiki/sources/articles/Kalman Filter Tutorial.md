---
title: Kalman Filter Tutorial
type: source
status: section_ingested
updated: 2026-04-23
tags:
  - source
  - kalman-filter
  - state-space
  - tutorial
source_type: pdf
source_class: article_source
read_scope: full_source
extraction_basis: fitz_text_plus_rendered_pages
technical_depth: deep
ingest_stage: promoted
sources:
  - "[[raw/math_statistics/Kalman filter.pdf]]"
---
# Kalman Filter Tutorial

## Summary

Tony Lacey's short tutorial is a compact bridge note rather than a full state-space book. Its value is that it shows the same filter from four compatible angles:

- mean-squared-error minimization
- Gaussian maximum likelihood
- covariance-form recursive state estimation
- chi-square or recursive-least-squares and information-form updating

For this shelf, that makes it the cleanest short source for seeing why the Kalman filter is not just a memorized recursion but an uncertainty-weighted estimator.

## Section-by-Section Ingest

- `11.1 Introduction`: frames filtering as loss minimization and states the goal cleanly: extract the information-bearing signal while suppressing the rest.
- `11.2 Mean squared error`: starts from the scalar observation model
  $$y_k = a_k x_k + n_k,$$
  defines the estimation error $e_k = x_k - \hat{x}_k$, and makes expected squared error the optimization target:
  $$\epsilon(k) = \mathbb{E}[e_k^2].$$
- `11.3 Maximum likelihood`: shows that if the additive noise is Gaussian, maximizing likelihood is equivalent to minimizing a weighted squared-residual objective:
  $$\log P(y \mid \hat{x}) = -\frac{1}{2}\sum_k \frac{(y_k-a_k\hat{x}_k)^2}{\sigma_k^2} + \text{constant}.$$
- `11.4 Kalman filter derivation`: contrasts Kalman with Wiener filtering and motivates the state-space route as the computationally useful recursive form.
- `11.5 State space derivation`: writes the linear Gaussian model
  $$x_{k+1} = \Phi x_k + w_k, \qquad z_k = Hx_k + v_k,$$
  then derives the innovation, gain, update, and covariance recursion explicitly.
- `11.6 The Kalman filter as a chi-square merit function`: reframes the same update as recursive least squares by minimizing a rolling chi-square objective with respect to the parameter increment.
- `11.7 Model covariance update`: shows the information-form covariance update
  $$P_k^{-1} = P_k'^{-1} + H^\top R^{-1} H$$
  and proves its equivalence to the standard covariance update.

## Load-bearing equations

The tutorial's core equations are:

$$x_{k+1} = \Phi x_k + w_k, \qquad z_k = Hx_k + v_k,$$
$$Q = \mathbb{E}[w_k w_k^\top], \qquad R = \mathbb{E}[v_k v_k^\top],$$
$$P_k = \mathbb{E}[e_k e_k^\top] = \mathbb{E}\bracket{(x_k-\hat{x}_k)(x_k-\hat{x}_k)^\top},$$
$$\hat{x}_k = \hat{x}_k' + K_k(z_k - H\hat{x}_k'),$$
$$i_k = z_k - H\hat{x}_k',$$
$$K_k = P_k' H^\top \paren{H P_k' H^\top + R}^{-1},$$
$$S_k = H P_k' H^\top + R,$$
$$P_k = (I-K_kH)P_k',$$
$$\hat{x}_{k+1}' = \Phi \hat{x}_k, \qquad P_{k+1}' = \Phi P_k \Phi^\top + Q.$$

The chi-square or recursive-least-squares view gives the equivalent gain expression
$$K_k = \bracket{P_k'^{-1} + H^\top R^{-1}H}^{-1}H^\top R^{-1},$$
and the information-form covariance update
$$P_k^{-1} = P_k'^{-1} + H^\top R^{-1}H.$$

## Deepened derivation points

### 1. MSE and Gaussian likelihood coincide here

The tutorial's first important point is not just that MSE is convenient. It is that under Gaussian measurement noise, the same weighted squared residuals drive the log-likelihood. That makes the Kalman filter simultaneously:

- a minimum-MSE estimator in the linear Gaussian setup
- a maximum-likelihood update at each recursive step

### 2. The gain is a trace-minimizing uncertainty weight

The derivation expands the posterior covariance as
$$P_k = (I-K_kH)P_k'(I-K_kH)^\top + K_k R K_k^\top,$$
then minimizes $\operatorname{tr}(P_k)$ with respect to $K_k$. The result is the standard Kalman gain equation. This matters because it shows what the gain is actually doing: it balances prior uncertainty against measurement uncertainty instead of acting as an arbitrary smoothing parameter.

### 3. The innovation is the load-bearing residual

The update is driven by
$$i_k = z_k - H\hat{x}_k'.$$
This residual is not just a correction term. It is the new information entering the filter. The associated covariance
$$S_k = H P_k' H^\top + R$$
is what tells the algorithm how surprising that new information should be under the current state and noise assumptions.

### 4. Recursive least squares and information form are the same estimator

By minimizing a rolling chi-square criterion, the tutorial gets back an update of the same form as the covariance-form Kalman recursion. That makes the key bridge explicit:

- covariance form emphasizes posterior uncertainty propagation
- information form emphasizes additive precision updating
- recursive least squares emphasizes sequential parameter fitting

They are different views of the same linear Gaussian estimation problem.

## Methods and Data

- mean-squared-error minimization
- maximum likelihood under Gaussian noise
- state-space modeling
- recursive covariance propagation
- chi-square minimization and recursive least squares
- information-matrix interpretation

## Why It Matters Here

This is the shortest clean route in the raw shelf from general estimation theory into state-space filtering. It is especially useful because the large state-space books already in the vault are mathematically richer, but this tutorial is better at showing the bridge logic:

- why Gaussian MSE and likelihood point to the same update
- why the gain is an uncertainty-weighted correction
- why Kalman filtering is also recursive least squares
- why information-form updating is not a different model, only a different parameterization

## Caveats

- This is an 8-page tutorial chapter, not a full filtering text.
- The derivation stays in the linear Gaussian case and uses stationary notation.
- The covariance update is presented in the simplified $(I-K_kH)P_k'$ form, so later sources are still needed for diffuse initialization, smoothing, and broader numerical issues.

## Related Notes

- [[Kalman Filtering]]
- [[State Space Models]]
- [[Bayesian Filtering and Smoothing]]
- [[General Gaussian Filtering and Smoothing]]
- [[Financial Signal Processing and Machine Learning]]
- [[Signal Processing Map]]

## Sources

- [[raw/math_statistics/Kalman filter.pdf]]
