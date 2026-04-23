---
title: Bayesian Filtering and Smoothing - Ch 04 Discretization of Continuous-Time Dynamic Models
type: source
status: chapter_ingested
updated: 2026-04-21
tags:
  - source
  - state-space
  - discretization
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: chapter_text_plus_selected_theorems_and_algorithms
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 04 Discretization of Continuous-Time Dynamic Models
parent_source: "[[Bayesian Filtering and Smoothing]]"
sources:
  - "[[Bayesian Filtering and Smoothing]]"
  - "[[raw/math_statistics/Simo Särkkä and Lennart Svensson, Bayesian Filtering and Smoothing.pdf]]"
---
# Bayesian Filtering and Smoothing - Ch 04 Discretization of Continuous-Time Dynamic Models

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: theorem-level extraction completed for continuous-time versus discrete-time modeling, exact linear discretization, Euler-Maruyama, continuous-time linearization, constant-gradient covariance approximations, additive-noise approximation, and fast sampling.

## Why this chapter is load-bearing

This chapter fills one of the vault's clearest gaps: how a continuous-time physical or economic dynamic story becomes a usable discrete-time state-space transition model.

## Core objects

- continuous-time state `x(t)`
- discrete state `x_k = x(t_k)`
- stochastic differential equation `dx(t) / dt = a(x(t)) + L w(t)`
- sampling interval `Delta t_k`
- spectral-density matrix `Q_c`
- transition matrix `A_k`
- discrete-time process covariance `Q_k`

## Structural map

- discrete-time and continuous-time dynamic models
- discretizing linear dynamic models
- Euler-Maruyama method
- discretization via continuous-time linearization
- covariance approximation via constant gradients
- fast sampling

## Theorem and derivation spine

### 1. Continuous-time modeling is often easier than direct discrete-time modeling

The chapter starts from the point that a discrete transition model

`x_k = f_{k-1}(x_{k-1}) + q_{k-1}`

is often best built by first writing a continuous-time SDE, then discretizing it over the sampling interval.

### 2. Exact linear discretization exists for linear time-invariant SDEs

Theorem 4.3 gives the exact linear-Gaussian transition:

- `A_{k-1} = exp(F Delta t_{k-1})`
- `Q_{k-1} = integral_0^{Delta t_{k-1}} exp(F s) L Q_c L' exp(F s)' ds`

This is the clean benchmark case: when the continuous-time model is linear, discretization is not approximate hand-waving.

### 3. Euler-Maruyama is the baseline approximate discretization

When the exact transition is unavailable, Euler-Maruyama gives the low-cost first approximation. Its value is not elegance. Its value is that it makes nonlinear SDEs computationally usable when the sampling interval is small enough.

### 4. Continuous-time linearization and constant-gradient covariance approximations separate mean and covariance quality

The chapter's strongest practical idea is that different approximations can be used for:

- the deterministic mean path
- the process-noise covariance

Theorem 4.19 and Algorithm 4.20 show how to keep a stronger mean approximation while still forcing a tractable additive-noise covariance approximation.

### 5. Fast sampling is an alternative to heroic one-step approximations

If one-step Gaussian discretization is too crude over a large interval, the chapter recommends reducing the interval by introducing latent intermediate steps and skipping updates when no measurement is observed.

## Quant relevance

This chapter matters for:

- continuous-time latent-factor models sampled discretely
- dynamic fair-value or spread models built from continuous-time intuition
- state-space modeling of physical or financial systems with irregular sampling
- knowing when a crude transition approximation is driving later filtering error

## Promotion candidates

- [[State Space Discretization from Continuous-Time Models]]

## Related notes

- [[Bayesian Filtering and Smoothing]]
- [[State Space Discretization from Continuous-Time Models]]
- [[State Space Models]]
- [[Kalman Filtering]]
- [[Stochastic Calculus]]

## Sources

- [[Bayesian Filtering and Smoothing]]
- [[raw/math_statistics/Simo Särkkä and Lennart Svensson, Bayesian Filtering and Smoothing.pdf]]
