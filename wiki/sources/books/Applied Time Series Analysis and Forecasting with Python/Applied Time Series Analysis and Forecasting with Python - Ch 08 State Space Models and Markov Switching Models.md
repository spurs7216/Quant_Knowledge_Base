---
title: Applied Time Series Analysis and Forecasting with Python - Ch 08 State Space Models and Markov Switching Models
type: source
status: chapter_ingested
updated: 2026-04-20
tags:
  - source
  - time-series
  - state-space
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: chapter_scan
extraction_basis: chapter_scan_plus_kalman_sections
technical_depth: moderate
ingest_stage: selective_deepen
chapter_or_section: Ch 08 State Space Models and Markov Switching Models
parent_source: "[[Applied Time Series Analysis and Forecasting with Python]]"
sources:
  - "[[Applied Time Series Analysis and Forecasting with Python]]"
  - "[[raw/math_statistics/Applied Time Series Analysis and Forecasting with Python (2022).pdf]]"
---
# Applied Time Series Analysis and Forecasting with Python - Ch 08 State Space Models and Markov Switching Models

## Ingest Scope and Depth

- Ingest stage: `selective_deepen`
- Pass 1: full chapter scan completed.
- Pass 2: local deepening applied to linear state-space form, Kalman recursions, the local-level model, and the SARIMAX bridge; the Markov-switching section remains scan-level.

## Role of the chapter

This chapter is the latent-state bridge of the book. It moves from directly modeled series to systems where the main object of interest is hidden and only observed through noisy measurements.

## Section map

- state-space models and representations
- Kalman recursions
- local-level model and SARIMAX models
- Markov switching models

## Locally deepened subparts

### 1. Linear state-space form

Definition 8.1 gives the canonical pair:

- state equation `X_{t+1} = c_t + F_t X_t + D_t u_t + R_t eta_t`
- observation equation `Y_t = d_t + Z_t X_t + B_t u_t + epsilon_t`

The durable insight is that this is a unifying representation class, not merely another named model. MA, ARMA, SARIMA, time-varying-parameter regressions, and many latent-trend models can all be put into this form.

### 2. Kalman filtering, forecasting, and smoothing

The chapter defines:

- filtered estimate `X_{t|t}`
- one-step prediction `X_{t+1|t}`
- smoothing estimates `X_{s|t}`
- innovation `nu_t`
- Kalman gain

The filter update,

`X_{t|t} = X_{t|t-1} + P_{t|t-1} Z_t' V_t^{-1} nu_t`,

and the prediction step,

`X_{t+1|t} = c_t + F_t X_{t|t}`,

are the load-bearing recursions. They are the sequential-estimation backbone of the whole state-space family.

### 3. Local-level model as the clean bridge to ARIMA

The local-level model

- `Y_t = mu_t + epsilon_t`
- `mu_{t+1} = mu_t + eta_t`

is the chapter's most reusable conceptual example because differencing shows it induces an `ARIMA(0,1,1)` representation. That is a strong bridge:

- state-space models are not an alien alternative to ARIMA
- they can strictly contain ARIMA-style dynamics while preserving latent-state interpretation

### 4. SARIMAX as regression plus dynamic latent error structure

The chapter's SARIMAX discussion is useful because it puts exogenous regressors into the state-space machinery without pretending the residual dynamics disappear. This is the practical route from classical regression to dynamic regression with structured errors.

## Scan-level remainder

The Markov-switching section is important, but in this ingest it remains scan-level:

- regime changes are represented by a latent Markov chain
- coefficients and/or variances can switch by regime
- expected duration and regime probabilities become part of the interpretation

That section deserves later deepening as a dedicated regime-model note.

## Quant relevance

This chapter matters for:

- latent trend and fair-value estimation
- time-varying beta and dynamic factor exposures
- signal extraction under measurement noise
- macro nowcasting with exogenous information
- regime-aware extensions once linear Gaussian assumptions break

## Promotion candidates

- [[State Space Models]]
- Markov switching models

## Related notes

- [[Applied Time Series Analysis and Forecasting with Python]]
- [[State Space Models]]
- [[Kalman Filtering]]
- [[Time-Series Forecasting]]

## Sources

- [[Applied Time Series Analysis and Forecasting with Python]]
- [[raw/math_statistics/Applied Time Series Analysis and Forecasting with Python (2022).pdf]]
