---
title: Bayesian Filtering and Smoothing - Ch 16 Parameter Estimation
type: source
status: chapter_ingested
updated: 2026-04-21
tags:
  - source
  - estimation
  - state-space
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: chapter_text_plus_selected_theorems
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 16 Parameter Estimation
parent_source: "[[Bayesian Filtering and Smoothing]]"
sources:
  - "[[Bayesian Filtering and Smoothing]]"
  - "[[raw/math_statistics/Simo Särkkä and Lennart Svensson, Bayesian Filtering and Smoothing.pdf]]"
---
# Bayesian Filtering and Smoothing - Ch 16 Parameter Estimation

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: theorem-level extraction completed for parameter posteriors, recursive marginal likelihood, energy-function recursion, and the chapter's direct-optimization, EM, and MCMC estimation workflows.

## Why this chapter is load-bearing

This chapter turns filtering and smoothing from fixed-parameter inference into a real model-fitting workflow.

## Core objects

- parameter vector `theta`
- marginal likelihood `p(y_{1:T} | theta)`
- predictive likelihood factors `p(y_k | y_{1:k-1}, theta)`
- energy function `phi_T(theta)`
- MAP, ML, EM, and MCMC estimators
- filter- and smoother-based approximations

## Structural map

- Bayesian estimation of parameters in state space models
- computational methods for parameter estimation
- practical parameter estimation in state space models

## Theorem and derivation spine

### 1. Parameter learning can be reduced to recursive marginal likelihood evaluation

Theorem 16.1 gives the book's main structural result for estimation:

- factor the marginal likelihood into predictive likelihood terms
- compute those terms recursively using the same filtering structure

### 2. The energy function turns posterior estimation into optimization

Definition 16.2 and Theorem 16.4 give the recursive negative log-posterior or energy function, which becomes the workhorse object for ML and MAP fitting.

### 3. EM and MCMC are not separate worlds from filtering and smoothing

The chapter's practical point is that state-space estimation methods reuse the same inference family chosen for the state problem:

- Kalman and RTS in the linear-Gaussian case
- Gaussian approximations in nonlinear Gaussian settings
- particle methods in non-Gaussian or strongly nonlinear settings

### 4. Approximation discipline matters

The chapter explicitly warns that parameter estimation should generally use the same approximation family that will be used in the final application, otherwise the fitted model and deployed model can solve different problems.

## Quant relevance

This chapter matters for:

- fitting latent-volatility or hidden-state models
- learning process-noise and observation-noise structure
- turning a filtering model into a calibrated research object rather than a hand-tuned recursion

## Promotion candidates

- [[Parameter Estimation in State Space Models]]

## Related notes

- [[Bayesian Filtering and Smoothing]]
- [[Parameter Estimation in State Space Models]]
- [[Maximum Likelihood Estimation]]
- [[Markov Chain Monte Carlo]]

## Sources

- [[Bayesian Filtering and Smoothing]]
- [[raw/math_statistics/Simo Särkkä and Lennart Svensson, Bayesian Filtering and Smoothing.pdf]]
