---
title: Applied Time Series Analysis and Forecasting with Python - Ch 03 Stationary Time Series Models
type: source
status: chapter_ingested
updated: 2026-04-20
tags:
  - source
  - time-series
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: chapter_text_plus_key_definitions_and_theorems
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 03 Stationary Time Series Models
parent_source: "[[Applied Time Series Analysis and Forecasting with Python]]"
sources:
  - "[[Applied Time Series Analysis and Forecasting with Python]]"
  - "[[raw/math_statistics/Applied Time Series Analysis and Forecasting with Python (2022).pdf]]"
---
# Applied Time Series Analysis and Forecasting with Python - Ch 03 Stationary Time Series Models

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: theorem-level extraction completed for differencing operators, MA/AR/ARMA definitions, invertibility and causality root conditions, Yule-Walker logic, and Durbin-Levinson recursion.

## Why this chapter is load-bearing

This is the first real model chapter of the book. It gives the algebraic language that later ARIMA, volatility, and multivariate chapters assume:

- backshift notation
- differencing operators
- MA and AR structure
- invertibility and causality
- ACF/PACF signatures for identification

If this chapter stays vague, later time-series modeling collapses into pattern matching.

## Core objects

- backshift operator `B`
- differencing operators `nabla = 1 - B` and `1 - B^k`
- seasonal differencing as lag-`k` differencing when `k` is the period
- moving-average polynomial `theta(z) = 1 + theta_1 z + ... + theta_q z^q`
- autoregressive polynomial `phi(z) = 1 - phi_1 z - ... - phi_p z^p`
- Yule-Walker equations
- partial autocorrelations `phi_kk`

## Structural map

- backshift operator, differencing, and stationarity testing
- moving average models
- autoregressive models
- autoregressive moving average models

## Theorem and derivation spine

### 1. Differencing is an operator, not an ad hoc subtraction trick

Definition 3.1 formalizes:

- first differencing `nabla X_t = (1 - B) X_t`
- higher-order differencing `nabla^d X_t = (1 - B)^d X_t`
- lag-`k` differencing `(1 - B^k) X_t`
- seasonal differencing as the special lag-`k` case when `k` is the seasonal period

The important point is that differencing is part of the model algebra. It is how nonstationarity gets translated into a stationary target for later ARMA work.

### 2. MA(q) models give finite-memory correlation signatures

Definition 3.2 sets

`X_t = mu + epsilon_t + theta_1 epsilon_{t-1} + ... + theta_q epsilon_{t-q}`.

The chapter then derives the key property:

- the ACF of an MA(q) model cuts off after lag `q`

This matters because the model has only finitely many lagged shocks in its construction, so correlation vanishes beyond the MA window even though the PACF generally tails off.

### 3. Invertibility is about recovering shocks from observables

The chapter's MA(1) comparison is the right intuition: two observationally similar MA parameterizations can imply the same ACF, but only one lets the innovation be written as a convergent AR-infinite expansion in past data.

Theorem 3.1 states the general result:

- an MA(q) model is invertible iff all roots of `theta(z)` lie outside the unit circle

That is not a cosmetic root test. It is what makes the latent shock sequence identifiable from the data.

### 4. AR(p) models give recursive dependence and PACF cutoff

Definition 3.6 sets

`X_t = phi_0 + phi_1 X_{t-1} + ... + phi_p X_{t-p} + epsilon_t`.

The load-bearing properties are:

- conditional mean given the last `p` values is linear in those lags
- the PACF cuts off after lag `p`
- the ACF satisfies the Yule-Walker recursion

The Yule-Walker equations,

`rho_k = phi_1 rho_{k-1} + ... + phi_p rho_{k-p}`,

are what turn sample autocorrelation estimates into moment-based AR parameter estimates.

### 5. Durbin-Levinson converts ACF information into PACF information efficiently

The chapter shows that the PACF coefficients can be recursively recovered from autocorrelations through the Durbin-Levinson algorithm. The operational lesson is:

- ACF and PACF are not unrelated plotting conveniences.
- They are algebraically linked through the best linear prediction problem.

This recursion is also why PACF estimation is computationally tractable in practice.

### 6. Causality is the AR-side analog of invertibility

For the AR(1) model the chapter compares the forward MA-infinite solution with the backward-looking solution that depends on future shocks. The model is only useful in the ordinary forecasting sense when it admits a past-shock representation.

Theorem 3.2 states the general result:

- an AR(p) model is causal iff all roots of `phi(z)` lie outside the unit circle

The chapter also makes an important distinction:

- stationarity of an AR model is weaker than causality
- causality implies stationarity, but not conversely

### 7. ARMA models inherit their stability logic from the AR and MA parts

Definition 3.8 combines the two families into the parsimonious model

`phi(B) X_t = theta(B) epsilon_t`.

Theorem 3.3 then gives the inheritance rules:

- stationarity comes from the AR side
- invertibility comes from the MA side
- causality comes from the AR side

This is the compact algebraic reason ARMA models are both expressive and diagnosable.

## Quant relevance

This chapter underlies:

- baseline return and spread models
- root checks before forecasting or signal extraction
- choosing between AR, MA, and ARMA structure via ACF/PACF
- deciding whether differencing is doing necessary stabilization or needless damage
- interpreting persistence without confusing it with nonstationarity

## Promotion candidates

- [[ARIMA and Box-Jenkins Modeling]]
- stationarity and unit-root diagnostics

## Related notes

- [[Applied Time Series Analysis and Forecasting with Python]]
- [[Applied Time Series Analysis and Forecasting with Python - Ch 04 ARMA and ARIMA Modeling and Forecasting]]
- [[ARIMA and Box-Jenkins Modeling]]
- [[Time-Series Forecasting]]

## Sources

- [[Applied Time Series Analysis and Forecasting with Python]]
- [[raw/math_statistics/Applied Time Series Analysis and Forecasting with Python (2022).pdf]]
