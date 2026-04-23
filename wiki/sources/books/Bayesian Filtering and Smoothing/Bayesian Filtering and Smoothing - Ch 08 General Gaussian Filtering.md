---
title: Bayesian Filtering and Smoothing - Ch 08 General Gaussian Filtering
type: source
status: chapter_ingested
updated: 2026-04-21
tags:
  - source
  - gaussian
  - filtering
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: chapter_text_plus_selected_theorems_and_algorithms
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 08 General Gaussian Filtering
parent_source: "[[Bayesian Filtering and Smoothing]]"
sources:
  - "[[Bayesian Filtering and Smoothing]]"
  - "[[raw/math_statistics/Simo Särkkä and Lennart Svensson, Bayesian Filtering and Smoothing.pdf]]"
---
# Bayesian Filtering and Smoothing - Ch 08 General Gaussian Filtering

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: theorem-level extraction completed for Gaussian moment matching, Gaussian filter construction, Gauss-Hermite and cubature integration, the unscented transform, and higher-order cubature and unscented filters.

## Why this chapter is load-bearing

This chapter is the main reusable nonlinear-filtering chapter in the book. It shows that a large family of practical filters differ mainly in how they approximate Gaussian integrals.

## Core objects

- Gaussian moment matching
- approximate filtering distribution `N(x_k | m_k, P_k)`
- output moments `mu_k`, `S_k`, and cross-covariance `C_k`
- sigma points and quadrature weights
- Gauss-Hermite, cubature, and unscented integration rules

## Structural map

- Gaussian moment matching
- Gaussian filter
- Gauss-Hermite integration
- Gauss-Hermite Kalman filter
- spherical cubature integration
- cubature Kalman filter
- unscented transform
- unscented Kalman filter
- higher order cubature and unscented Kalman filters

## Theorem and derivation spine

### 1. Nonlinear Gaussian filtering can be reduced to Gaussian integral approximation

Algorithm 8.1 starts from moment matching of a transformed Gaussian variable. That is the durable abstraction:

- approximate the needed moments well
- then the filter recursion follows

### 2. The Gaussian filter is an assumed-density filter

Algorithm 8.3 defines the Gaussian filter by assuming the filtering distribution is approximately Gaussian and then updating its moments by integrals over the nonlinear transition and measurement maps.

### 3. Practical filters differ by the numerical rule used for those integrals

The chapter's strongest unifying insight is:

- Gauss-Hermite filters use product quadrature and gain accuracy at high cost
- cubature filters use spherical cubature rules
- unscented filters use the unscented transform

These are not unrelated brands. They are numerical-integration choices inside the same Gaussian-filter template.

### 4. Accuracy and cost trade off against dimension

Gauss-Hermite can be strong in low dimensions but scales poorly. Cubature and unscented methods are cheaper. Higher-order rules promise better local accuracy but at additional computational cost.

## Quant relevance

This chapter matters for:

- nonlinear observation equations
- continuous-discrete state-space models
- situations where Gaussian posterior shape is still acceptable but EKF linearization is too crude
- understanding when sigma-point filters are justified instead of particle methods

## Promotion candidates

- [[General Gaussian Filtering and Smoothing]]

## Related notes

- [[Bayesian Filtering and Smoothing]]
- [[General Gaussian Filtering and Smoothing]]
- [[Kalman Filtering]]
- [[Particle Filtering]]

## Sources

- [[Bayesian Filtering and Smoothing]]
- [[raw/math_statistics/Simo Särkkä and Lennart Svensson, Bayesian Filtering and Smoothing.pdf]]
