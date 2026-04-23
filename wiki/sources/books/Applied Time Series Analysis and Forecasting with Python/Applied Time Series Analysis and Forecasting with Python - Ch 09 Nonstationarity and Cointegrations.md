---
title: Applied Time Series Analysis and Forecasting with Python - Ch 09 Nonstationarity and Cointegrations
type: source
status: chapter_ingested
updated: 2026-04-20
tags:
  - source
  - time-series
  - cointegration
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: chapter_text_plus_unit_root_and_cointegration_sections
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 09 Nonstationarity and Cointegrations
parent_source: "[[Applied Time Series Analysis and Forecasting with Python]]"
sources:
  - "[[Applied Time Series Analysis and Forecasting with Python]]"
  - "[[raw/math_statistics/Applied Time Series Analysis and Forecasting with Python (2022).pdf]]"
---
# Applied Time Series Analysis and Forecasting with Python - Ch 09 Nonstationarity and Cointegrations

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: deep extraction completed for trend versus difference stationarity, Dickey-Fuller asymptotics, integrated processes, spurious regression, cointegration, and Granger's representation theorem with VECM form.

## Why this chapter is load-bearing

This chapter handles one of the highest-risk areas in applied time-series work: nonstationary data that look related but may be statistically meaningless when regressed naively. For quant research, that is a direct safeguard against false spread models, false macro relationships, and false long-run equilibrium claims.

## Core objects

- trend-stationary process
- difference-stationary process
- unit root
- integrated order `I(d)`
- Brownian-motion limits for Dickey-Fuller statistics
- cointegrating vector `beta`
- loading matrix `alpha`
- vector error correction model

## Structural map

- stochastic trend and stochastic seasonality
- Brownian motions and simulation
- stationarity, nonstationarity, and unit root tests
- cointegrations and Granger's representation theorem

## Theorem and derivation spine

### 1. Trend-stationary and difference-stationary are not the same pathology

Definition 9.8 separates:

- deterministic-trend plus stationary noise
- stochastic-trend processes whose differenced series are stationary

The distinction is crucial because detrending and differencing are not interchangeable. The chapter explicitly shows that a random walk with drift can look linearly trending while still remaining nonstationary after deterministic trend removal.

### 2. Unit-root testing has nonstandard asymptotics

The chapter derives the Dickey-Fuller logic from the AR(1) null

`X_t = alpha X_{t-1} + epsilon_t`

under `H_0: alpha = 1`.

The important derivation is that the usual t-statistic does not converge to a standard normal law. Instead, scaled least-squares estimates converge to functionals of Brownian motion such as

- `int B(t) dB(t)`
- `int B(t)^2 dt`

That is why unit-root critical values are special and why naive OLS intuition fails here.

### 3. ADF and PP tests are operational fixes, not cosmetic variants

The chapter explains how the simple unit-root regression expands to the augmented Dickey-Fuller form by adding lagged differences, and it notes Phillips-Perron as the route that adjusts for serial correlation and conditional heteroskedasticity in a different way. The durable lesson is:

- unit-root testing is about the dependence structure of the null, not only about one coefficient being near one

### 4. Integrated order formalizes how many times differencing is justified

Definition 9.9 introduces `I(0)` and `I(d)` processes. The important caution is that not every stationary series is `I(0)` in the representation sense the chapter uses, and differencing a stationary process can create the wrong object.

### 5. Spurious regression is the default risk for unrelated I(1) series

Example 9.10 is one of the most reusable parts of the chapter: two independent random walks can generate apparently significant regression slopes, decent `R^2`, and entirely false economic narratives. The residual nonstationarity is what exposes the fraud.

That is a core quant safeguard.

### 6. Cointegration rescues long-run relationships by making the spread stationary

Definition 9.10 says an `I(1)` vector process is cointegrated if some nonzero linear combination `beta' X_t` is stationary.

This is the right long-run equilibrium idea:

- components can wander
- but certain spreads or combinations remain bounded

That is the formal statistical backbone behind many spread and macro-equilibrium stories.

### 7. Granger's representation theorem turns cointegration into VECM structure

Theorem 9.3 is the load-bearing result:

- under the rank condition `Phi = alpha beta'`
- an `I(1)` VAR system is cointegrated iff it admits a decomposition into stochastic-trend and stationary parts
- the system satisfies the vector error-correction equation

`nabla X_t = alpha beta' X_{t-1} + sum Gamma_h nabla X_{t-h} + epsilon_t`

This is the main practical payoff of the chapter. Cointegration is not only a test label; it implies a constrained dynamic form with long-run error correction and short-run adjustment.

## Quant relevance

This chapter directly supports:

- spread and pairs-trading research
- yield-curve and macro system modeling
- avoiding spurious regressions on levels data
- deciding when to difference and when to preserve long-run equilibrium structure
- interpreting error-correction dynamics as adjustment speed rather than generic autoregression

## Promotion candidates

- [[Cointegration and Error Correction Models]]

## Related notes

- [[Applied Time Series Analysis and Forecasting with Python]]
- [[Vector Autoregression and Impulse Response Analysis]]
- [[Cointegration and Error Correction Models]]
- [[Time-Series Forecasting]]

## Sources

- [[Applied Time Series Analysis and Forecasting with Python]]
- [[raw/math_statistics/Applied Time Series Analysis and Forecasting with Python (2022).pdf]]
