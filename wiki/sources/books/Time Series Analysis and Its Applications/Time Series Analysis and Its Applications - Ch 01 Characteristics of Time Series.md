---
title: Time Series Analysis and Its Applications - Ch 01 Characteristics of Time Series
type: source
status: chapter_ingested
updated: 2026-04-21
tags:
  - source
  - time-series
  - chapter-digest
  - statistics
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: chapter_text_plus_section_map_plus_key_definitions_and_large_sample_properties
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 01 Characteristics of Time Series
parent_source: "[[Time Series Analysis and Its Applications]]"
sources:
  - "[[Time Series Analysis and Its Applications]]"
  - "[[raw/math_statistics/Shumway and Stoffer, Time Series Analysis and Its Applications.pdf]]"
---
# Time Series Analysis and Its Applications - Ch 01 Characteristics of Time Series

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: theorem-level extraction completed for stochastic-process framing, dependence measures, stationarity, sample correlation estimation, and vector-valued time-series objects.

## Why this chapter is load-bearing

This chapter sets the objects that every later chapter assumes without repeating:

- what a time series is statistically
- what kinds of dependence matter
- what stationarity means
- how ACF and CCF are actually estimated from one realization
- how the univariate language lifts to vector series

If this chapter stays vague, later ARIMA, spectral, and state-space chapters collapse into recipe use without clear model objects.

## Core objects

- stochastic process and realization
- white noise, iid noise, Gaussian white noise
- mean function `mu_t`
- autocovariance `gamma(s, t)` and stationary autocovariance `gamma(h)`
- autocorrelation `rho(h)` and cross-correlation
- strict and weak stationarity
- sample ACF and sample CCF
- mean vector `mu` and autocovariance matrix `Gamma(h)` for vector series

## Structural map

- nature of time-series data
- time-series statistical models
- measures of dependence
- stationary time series
- estimation of correlation
- vector-valued and multidimensional series

## Theorem and derivation spine

### 1. A time series is a stochastic process, not just an ordered spreadsheet column

Section 1.2 formalizes the basic move:

- `x_t` is a random variable indexed by time
- the observed sequence is one realization of a process
- smoothness and serial pattern suggest dependence among nearby observations

This is the statistical boundary between iid methods and time-series methods.

### 2. White noise is the baseline null process

The chapter distinguishes:

- uncorrelated white noise
- iid white noise
- Gaussian white noise

That distinction matters because many large-sample reference results become cleaner under Gaussian or iid assumptions, but the conceptual benchmark is broader: a series with no serial structure beyond noise.

### 3. Dependence is summarized through covariance structure when full joint laws are unwieldy

The book introduces:

- autocovariance `gamma(s, t) = cov(x_s, x_t)`
- cross-covariance between two series
- standardized versions through ACF and CCF

The key statistical point is not that these objects describe everything. It is that they are the most usable summaries of temporal dependence for modeling and diagnostics.

### 4. Stationarity is the regularity condition that makes one-realization inference possible

Definition 1.6 gives strict stationarity, and the chapter then works mainly with weak stationarity:

- constant mean over time
- covariance depending only on lag

That is the operational contract that lets us average lagged products over one realization and still treat the result as learning about a stable dependence object.

### 5. Sample correlation estimators only make sense because stationarity lets time averages replace replicate averages

Section 1.5 builds the sample mean, sample autocovariance, sample ACF, and sample CCF from a single observed series. The load-bearing logic is:

- without stationarity, the same lag at different times need not represent the same object
- with stationarity, lag-based averaging becomes meaningful

The chapter also gives a large-sample white-noise benchmark:

- for fixed lags, sample ACF and sample CCF are approximately normal with standard deviation about `1 / sqrt(n)` in the white-noise reference case

That is the practical justification for the standard correlogram significance bands.

### 6. Prewhitening is required before cross-correlation can be interpreted cleanly

The chapter's discussion of cross-correlation warns that raw CCF peaks can be misleading when both series are internally autocorrelated. Prewhitening one series and filtering the other by the same filter is the right preparation before reading dynamic lead-lag structure.

### 7. Vector-valued series are not an optional extra

Section 1.6 lifts the whole setup to `x_t = (x_t1, ..., x_tp)'` with:

- mean vector `mu`
- autocovariance matrix `Gamma(h)`
- matrix-valued cross-dependence

This is the gateway to VARs, multivariate spectra, state-space systems, and dynamic-factor thinking.

## Quant relevance

This chapter prevents several recurring mistakes in quant work:

- treating prices and returns as if temporal dependence did not matter
- interpreting raw cross-correlations without removing internal serial structure
- using ACF plots without understanding what stationarity assumption makes them estimable
- forgetting that many problems are intrinsically multivariate long before they are "machine learning"

## Promotion candidates

- [[Stationarity and Unit-Root Diagnostics]]
- a durable note on Wold decomposition and linear-process approximation

## Related notes

- [[Time Series Analysis and Its Applications]]
- [[Time Series Analysis and Its Applications - Ch 03 ARIMA Models]]
- [[Stationarity and Unit-Root Diagnostics]]
- [[Time-Series Forecasting]]

## Sources

- [[Time Series Analysis and Its Applications]]
- [[raw/math_statistics/Shumway and Stoffer, Time Series Analysis and Its Applications.pdf]]
