---
title: Time Series Analysis by State Space Methods - Ch 10 Approximate Filtering and Smoothing
type: source
status: chapter_ingested
updated: 2026-04-21
tags:
  - source
  - state-space
  - nonlinear
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: chapter_scan
extraction_basis: chapter_scan_plus selected sections on EKF UKF and mode estimation
technical_depth: moderate
ingest_stage: selective_deepen
chapter_or_section: Ch 10 Approximate Filtering and Smoothing
parent_source: "[[Time Series Analysis by State Space Methods]]"
sources:
  - "[[Time Series Analysis by State Space Methods]]"
  - "[[raw/math_statistics/Time Series Analysis by State Space Methods (2012).pdf]]"
---
# Time Series Analysis by State Space Methods - Ch 10 Approximate Filtering and Smoothing

## Ingest Scope and Depth

- Ingest stage: `selective_deepen`
- Pass 1: full chapter scan completed.
- Pass 2: local deepening applied to the extended Kalman filter, unscented Kalman filter, approximate nonlinear smoothing, data-transformation approximations, and mode-estimation based linearization.

## Role of the chapter

This chapter is the approximation toolbox for nonlinear or non-Gaussian state-space models when exact linear-Gaussian recursions no longer apply directly.

## Section map

- extended Kalman filter
- unscented Kalman filter
- nonlinear smoothing
- approximation via data transformation
- approximation via mode estimation
- further advances in mode estimation
- treatments for heavy-tailed distributions

## Locally deepened subparts

### 1. EKF and UKF are approximation families, not universal replacements

The chapter treats both as ways to preserve recursive filtering when exact Gaussian linearity is lost. The important practical point is that they approximate the nonlinear problem differently, with different stability and accuracy tradeoffs.

### 2. Data transformation can linearize some problems only approximately

The chapter's stochastic-volatility example makes clear that transformation-based linearization can be operationally useful but conceptually approximate.

### 3. Mode estimation produces an approximating linear-Gaussian model

The mode-estimation sections are high-value because they show how iterative linearization can be built around the conditional mode rather than only around a local Taylor expansion of the dynamics.

## Quant relevance

This chapter matters when:

- nonlinear observation equations arise
- exact inference is too expensive
- one needs a controlled approximation rather than a full particle method
- stochastic volatility or multiplicative models need a practical first pass

## Promotion candidates

- a later note on extended and unscented Kalman methods
- stronger updates to [[Kalman Filtering]]

## Related notes

- [[Time Series Analysis by State Space Methods]]
- [[Kalman Filtering]]
- [[Particle Filtering]]

## Sources

- [[Time Series Analysis by State Space Methods]]
- [[raw/math_statistics/Time Series Analysis by State Space Methods (2012).pdf]]
