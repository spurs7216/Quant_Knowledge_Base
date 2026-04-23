---
title: Time Series Analysis by State Space Methods - Ch 07 Maximum Likelihood Estimation of Parameters
type: source
status: chapter_ingested
updated: 2026-04-21
tags:
  - source
  - state-space
  - likelihood
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: chapter_scan_plus selected estimation sections
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 07 Maximum Likelihood Estimation of Parameters
parent_source: "[[Time Series Analysis by State Space Methods]]"
sources:
  - "[[Time Series Analysis by State Space Methods]]"
  - "[[raw/math_statistics/Time Series Analysis by State Space Methods (2012).pdf]]"
---
# Time Series Analysis by State Space Methods - Ch 07 Maximum Likelihood Estimation of Parameters

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: theorem-level extraction completed for likelihood evaluation under known and diffuse initial conditions, score-vector and EM estimation logic, large-sample behavior of estimates, and the effect of parameter-estimation error on state inference.

## Why this chapter is load-bearing

This chapter is where state-space models become fit objects rather than only filtering devices. It translates the recursive machinery into parameter estimation and model checking.

## Core objects

- prediction-error decomposition of the likelihood
- diffuse likelihood
- score vector
- EM algorithm
- large-sample distribution of parameter estimates
- effect of parameter uncertainty on variance estimation
- goodness of fit and diagnostic checking

## Structural map

- likelihood evaluation
- parameter estimation
- goodness of fit
- diagnostic checking

## Theorem and derivation spine

### 1. Likelihood comes from the prediction-error decomposition

The chapter builds the likelihood from the sequence of forecast errors and their variances. This is the core computational fact behind maximum-likelihood state-space estimation.

### 2. Diffuse initialization changes the likelihood itself

The chapter treats diffuse likelihood separately because the early-sample contribution to the likelihood is structurally different when initial states are diffuse or partly unknown.

### 3. The score vector is available recursively

The score vector is not just an optimization convenience. It exposes how likelihood information propagates through the filter and supports principled gradient-based estimation.

### 4. The EM algorithm gives an alternative estimation path

The chapter treats EM as a state-space estimation device rather than a generic missing-data algorithm. The latent-state structure makes the E-step and M-step naturally interpretable.

### 5. Parameter uncertainty contaminates state uncertainty if ignored

The chapter explicitly studies the effect of parameter-estimation error on variance estimation. This matters because filtered and smoothed states are often over-trusted when parameter uncertainty is suppressed.

## Quant relevance

This chapter matters for:

- fitting structural and latent-factor models by likelihood
- comparing state-space specifications rather than only running one filter pass
- avoiding overconfidence in filtered or smoothed signals when parameters are estimated from limited samples

## Promotion candidates

- stronger updates to [[State Space Models]]
- a later durable note on prediction-error likelihood and EM in state-space models

## Related notes

- [[Time Series Analysis by State Space Methods]]
- [[Kalman Filtering]]
- [[State Space Models]]

## Sources

- [[Time Series Analysis by State Space Methods]]
- [[raw/math_statistics/Time Series Analysis by State Space Methods (2012).pdf]]
