---
title: Applied Time Series Analysis and Forecasting with Python - Ch 05 Nonstationary Time Series Models
type: source
status: chapter_ingested
updated: 2026-04-20
tags:
  - source
  - time-series
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: chapter_scan
extraction_basis: chapter_scan_plus_local_section_text
technical_depth: moderate
ingest_stage: selective_deepen
chapter_or_section: Ch 05 Nonstationary Time Series Models
parent_source: "[[Applied Time Series Analysis and Forecasting with Python]]"
sources:
  - "[[Applied Time Series Analysis and Forecasting with Python]]"
  - "[[raw/math_statistics/Applied Time Series Analysis and Forecasting with Python (2022).pdf]]"
---
# Applied Time Series Analysis and Forecasting with Python - Ch 05 Nonstationary Time Series Models

## Ingest Scope and Depth

- Ingest stage: `selective_deepen`
- Pass 1: full chapter scan completed.
- Pass 2: local attention applied to seasonal differencing, SARIMA notation, and regression with ARMA errors; the full chapter was not rewritten at theorem-level.

## Role of the chapter

This chapter extends the Chapter 4 workflow from nonseasonal series into seasonal and regressor-augmented settings. It is the practical bridge from plain ARIMA to the kinds of data that often show up in macro, demand, and business-cycle work.

## Section map

- the Box-Jenkins method
- SARIMA model building
- REGARMA models

## Locally deepened subparts

### 1. Seasonal differencing and SARIMA structure

The chapter formalizes seasonal differencing as

`nabla_s^D X_t = (1 - B^s)^D X_t`

and then combines it with ordinary differencing and seasonal/nonseasonal ARMA polynomials. The real point is that trend and seasonality should be stabilized algebraically before estimation, not merely "detrended by eye."

### 2. SARIMA as a seasonal extension of ARIMA rather than a different workflow

The chapter treats seasonal models as Box-Jenkins with more operators, not a different philosophy. That is the durable lesson: identification, estimation, residual checking, and forecasting stay the same; only the polynomial structure becomes richer.

### 3. REGARMA as regression plus dependent errors

The REGARMA section matters because many real series need exogenous regressors without surrendering serial dependence in the residual component. This is a good bridge toward SARIMAX and state-space models later.

## What the chapter is really doing

- seasonal differencing is a structural operation, not only a preprocessing step
- seasonal AR and MA terms let one represent repeated calendar structure parsimoniously
- exogenous predictors can be useful, but serially dependent errors still need explicit treatment

## Quant relevance

This chapter is useful for:

- quarterly and monthly macro series
- demand, seasonality, and holiday-sensitive business data
- modeling spreads or levels with known exogenous drivers but dependent residuals
- separating seasonal persistence from genuinely new predictive structure

## Promotion candidates

- seasonal ARIMA and regression-with-ARMA-errors

## Related notes

- [[Applied Time Series Analysis and Forecasting with Python]]
- [[Applied Time Series Analysis and Forecasting with Python - Ch 04 ARMA and ARIMA Modeling and Forecasting]]
- [[ARIMA and Box-Jenkins Modeling]]
- [[Time-Series Forecasting]]

## Sources

- [[Applied Time Series Analysis and Forecasting with Python]]
- [[raw/math_statistics/Applied Time Series Analysis and Forecasting with Python (2022).pdf]]
