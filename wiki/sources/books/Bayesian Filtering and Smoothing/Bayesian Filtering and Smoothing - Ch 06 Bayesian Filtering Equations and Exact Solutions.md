---
title: Bayesian Filtering and Smoothing - Ch 06 Bayesian Filtering Equations and Exact Solutions
type: source
status: chapter_ingested
updated: 2026-04-21
tags:
  - source
  - bayesian
  - filtering
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: chapter_text_plus_selected_theorems
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 06 Bayesian Filtering Equations and Exact Solutions
parent_source: "[[Bayesian Filtering and Smoothing]]"
sources:
  - "[[Bayesian Filtering and Smoothing]]"
  - "[[raw/math_statistics/Simo Särkkä and Lennart Svensson, Bayesian Filtering and Smoothing.pdf]]"
---
# Bayesian Filtering and Smoothing - Ch 06 Bayesian Filtering Equations and Exact Solutions

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: theorem-level extraction completed for probabilistic state-space models, Markov and conditional-independence structure, Bayesian filtering equations, the Kalman filter, affine extension, and the discrete-state Bayesian filter.

## Why this chapter is load-bearing

This chapter states the exact recursive target that every later approximate filter is trying to mimic.

## Core objects

- probabilistic state-space model `x_k ~ p(x_k | x_{k-1}), y_k ~ p(y_k | x_k)`
- filtering distribution `p(x_k | y_{1:k})`
- predictive distribution `p(x_k | y_{1:k-1})`
- likelihood `p(y_k | x_k)`
- normalization constant `Z_k`
- Kalman gain and innovation in the linear-Gaussian specialization

## Structural map

- probabilistic state space models
- Bayesian filtering equations
- Kalman filter
- affine Kalman filter
- Bayesian filter for discrete state space

## Theorem and derivation spine

### 1. The state-space model is defined by conditional distributions plus Markov structure

The chapter starts from the abstract formulation

- `x_k ~ p(x_k | x_{k-1})`
- `y_k ~ p(y_k | x_k)`

and makes the two structural assumptions explicit:

- the states are Markov
- the measurement is conditionally independent of the past given the current state

### 2. The exact Bayesian filter is prediction plus update

Theorem 6.5 gives the recursive core:

- prediction by Chapman-Kolmogorov integration
- update by Bayes rule and normalization

This is the load-bearing recursion of the whole book.

### 3. The Kalman filter is the exact linear-Gaussian closed form

Theorem 6.6 shows that when the transition and measurement models are linear Gaussian, the Bayesian filter stays Gaussian and the recursion closes in means and covariances.

### 4. Affine and discrete-state models are exact specializations too

The chapter matters because it does not treat exact filtering as equivalent only to the basic Kalman filter. Affine and discrete-state models also admit exact recursive structure.

## Quant relevance

This chapter matters for:

- understanding what approximate filters are approximating
- grounding innovations-based likelihood logic
- separating exact linear-Gaussian inference from approximation layers
- regime and discrete-state filtering in hidden-state systems

## Promotion candidates

- stronger support for [[Kalman Filtering]]
- stronger support for [[Parameter Estimation in State Space Models]]

## Related notes

- [[Bayesian Filtering and Smoothing]]
- [[Kalman Filtering]]
- [[State Space Models]]
- [[Parameter Estimation in State Space Models]]

## Sources

- [[Bayesian Filtering and Smoothing]]
- [[raw/math_statistics/Simo Särkkä and Lennart Svensson, Bayesian Filtering and Smoothing.pdf]]
