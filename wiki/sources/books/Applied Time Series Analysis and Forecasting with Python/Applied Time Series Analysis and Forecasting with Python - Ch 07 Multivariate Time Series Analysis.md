---
title: Applied Time Series Analysis and Forecasting with Python - Ch 07 Multivariate Time Series Analysis
type: source
status: chapter_ingested
updated: 2026-04-20
tags:
  - source
  - time-series
  - multivariate
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: chapter_text_plus_var_varma_sections
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 07 Multivariate Time Series Analysis
parent_source: "[[Applied Time Series Analysis and Forecasting with Python]]"
sources:
  - "[[Applied Time Series Analysis and Forecasting with Python]]"
  - "[[raw/math_statistics/Applied Time Series Analysis and Forecasting with Python (2022).pdf]]"
---
# Applied Time Series Analysis and Forecasting with Python - Ch 07 Multivariate Time Series Analysis

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: deep extraction completed for vector covariance structure, vector white noise, multivariate portmanteau tests, VARMA/VAR definitions, multivariate causality and invertibility theorems, identifiability caveats, Granger causality, and impulse response analysis.

## Why this chapter is load-bearing

This chapter is the first place where "time series" becomes "dynamic system." That is essential for quant research because many relevant objects move together:

- macro variables
- multi-asset return systems
- term structures
- cross-asset predictors

## Core objects

- vector time series `X_t in R^K`
- covariance matrix function `Gamma(h)`
- correlation matrix function `rho(h)`
- vector white noise `epsilon_t ~ WN(0, Sigma)`
- VARMA(p, q) model
- VAR(p) model
- VMA-infinite representation `Psi_h`
- multivariate portmanteau statistics
- Granger causality and impulse responses

## Structural map

- basic concepts
- VARMA models
- VAR model building and analysis
- examples

## Theorem and derivation spine

### 1. Multivariate dependence is matrix-valued, not scalar

Definitions 7.1 to 7.4 generalize the univariate objects correctly:

- mean becomes a vector
- covariance becomes a matrix function across lags
- off-diagonal terms become cross-covariances and cross-correlations

That matters because dynamic dependence is no longer only "serial persistence in one line." It is also cross-series propagation.

### 2. Vector stationarity and vector white noise are stronger than componentwise stories

Proposition 7.1 shows that if the whole vector process is stationary, then each component is stationary, but the reverse is not the full story because cross-covariance structure still matters.

Definition 7.4 for vector white noise also makes an important distinction:

- there can be no lagged correlation
- but contemporaneous correlation across components can remain through `Sigma`

That is the right baseline for system residuals.

### 3. Portmanteau checks generalize to matrix residual structure

The chapter's extended trace and multivariate portmanteau statistics are useful because plotting every pairwise correlation becomes cumbersome when `K` grows. The operational lesson is:

- for multivariate models, whiteness is a matrix-level residual claim
- scalar residual checks are not enough

### 4. VARMA structure is natural but not always identifiable

Definition 7.5 gives the vector ARMA model

`X_t - Phi_1 X_{t-1} - ... - Phi_p X_{t-p} = nu + epsilon_t + Theta_1 epsilon_{t-1} + ... + Theta_q epsilon_{t-q}`.

The multivariate invertibility and causality theorems then mirror the univariate root conditions through determinant tests on the matrix polynomials. But the chapter also gives the right warning:

- a VARMA representation need not be uniquely identified from data without extra restrictions

That is why the practical focus shifts to VAR models.

### 5. VAR models are the practical workhorse because they are identifiable and interpretable

The chapter's VAR workflow is:

- stabilize the system
- choose order `p` by information criteria or FPE
- estimate coefficients
- diagnose the residual vector process
- simplify if necessary
- forecast only after the residual system looks acceptable

This is the system-level analog of Box-Jenkins.

### 6. Granger causality is predictive directionality, not structural causality

The chapter's two-dimensional VAR(1) discussion makes the right distinction:

- zero off-diagonal lag coefficients means no lagged predictive influence
- nonzero off-diagonal lag coefficients indicate predictive directionality
- contemporaneous covariance in `Sigma` is not the same thing

This is a useful forecasting notion, but it should not be confused with intervention-level causal claims.

### 7. Impulse response analysis turns coefficients into dynamic shock paths

Using the VMA representation,

- `Psi_h` gives the response at horizon `h` to a unit shock
- cumulative responses sum those effects over horizons

This is what makes system models interpretable. Rather than reading dozens of coefficient matrices directly, one asks:

- what happens to variable `j` if variable `i` is shocked now?
- how long does the effect persist?
- what is the long-run effect?

## Quant relevance

This chapter matters for:

- forecasting interacting asset or macro systems
- cross-series signal propagation
- shock transmission and scenario analysis
- differentiating own-lag persistence from cross-lag predictive influence
- checking whether a multivariate model actually removed the system dependence it claimed to model

## Promotion candidates

- [[Vector Autoregression and Impulse Response Analysis]]

## Related notes

- [[Applied Time Series Analysis and Forecasting with Python]]
- [[Vector Autoregression and Impulse Response Analysis]]
- [[Time-Series Forecasting]]
- [[Cointegration and Error Correction Models]]

## Sources

- [[Applied Time Series Analysis and Forecasting with Python]]
- [[raw/math_statistics/Applied Time Series Analysis and Forecasting with Python (2022).pdf]]
