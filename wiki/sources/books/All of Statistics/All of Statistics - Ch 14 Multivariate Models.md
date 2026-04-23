---
title: All of Statistics - Ch 14 Multivariate Models
type: source
status: chapter_ingested
updated: 2026-04-19
tags:
  - source
  - statistics
  - multivariate
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: full_source
extraction_basis: full_text
technical_depth: moderate
ingest_stage: scan
chapter_or_section: Ch 14 Multivariate Models
parent_source: "[[All of Statistics]]"
sources:
  - "[[All of Statistics]]"
  - "[[raw/math_statistics/2004 - wasserman - all of statistics.pdf]]"
---
# All of Statistics - Ch 14 Multivariate Models

## Ingest Scope and Depth

- Ingest stage: `scan`
- Pass 1: full chapter scan completed against the raw source.
- Pass 2: rescan completed to identify the mathematically load-bearing pieces that are worth later deepening.

## Deepening Targets

- Deepen Theorem 14.1 so affine transformations, quadratic forms, and covariance geometry become explicit tools rather than formulas to quote.
- Deepen Fisher's `z` transform for correlation inference if later notes rely on correlation confidence intervals in serious empirical work.
- Deepen Theorems 14.2 and 14.3 if portfolio, Gaussian state-space, or high-dimensional covariance notes start depending directly on multivariate Normal likelihood structure.
- Deepen the Multinomial limit theory if later contingency-table or discrete-state notes need a stronger asymptotic base.

## Deepened Subparts

- No subpart has been rewritten at full deep-note depth yet.

## Worth Attending From The Rescan

- Theorem 14.1 is the chapter's linear-algebra core. It explains why means and covariances transform cleanly under `a^T X` and `AX`, which is the reason portfolio returns, factor combinations, and state transformations stay tractable.
- Section 14.2 is more than a recipe for a correlation interval. Fisher's transform matters because the raw sample correlation has awkward finite-sample behavior near `+-1`, while the transformed scale is closer to Gaussian.
- Theorem 14.2 is the multivariate Normal spine: affine closure and the quadratic form `(X - mu)^T Sigma^{-1} (X - mu)` generating a `chi_k^2` law are the reasons Gaussian models are computationally privileged.
- Theorem 14.3 matters because the mle for `(mu, Sigma)` shows how sample mean and covariance arise from likelihood, not only from descriptive definitions.
- Theorem 14.6 is easy to overlook, but it is the asymptotic bridge from multinomial counts to Gaussian approximations, which later powers large-sample contingency-table inference.

## Role of the chapter

This chapter revisits multivariate probability from an inferential point of view. The focus is not only on defining joint laws, but on estimating and exploiting multivariate structure.

The main models are:

- random vectors and correlation structure
- multivariate Normal
- Multinomial

## Core mathematical objects

- random vector `X in R^k`
- covariance and correlation matrices
- multivariate Normal likelihood
- Multinomial counts and probabilities

## Random vectors and linear structure

### Theorem 14.1

Linear functionals of multivariate random vectors behave in familiar ways. This carries the scalar expectation-variance logic into vector settings and prepares the reader for regression, Gaussian models, and portfolio-like linear combinations.

## Estimating correlation

This section is practically important because correlation is one of the most reused second-order summaries in applied work, but also one of the most fragile.

The chapter treats correlation as an inferential target, not just a descriptive statistic.

## Multivariate Normal

The multivariate Normal returns here as a full inferential model rather than just a distribution family.

### Theorem 14.3

The chapter derives the log-likelihood and mle structure for multivariate Normal samples.

The main point is that:

- the mean vector and covariance matrix have natural estimators
- Gaussian structure makes inference analytically tractable

This is important because the multivariate Normal is often used not because data are exactly Normal, but because its closure under conditioning and linear transformation makes it a mathematically convenient approximation.

## Multinomial

### Theorems 14.4 and 14.5

The Multinomial's marginals and mle are developed.

This is the discrete multivariate counterpart to earlier scalar count models. It is the right model when observations fall into one of several categories and the full vector of category counts matters.

## What the chapter is really teaching

Once multiple coordinates matter, statistics must track:

- dependence
- covariance geometry
- parameter growth in dimension
- constraints such as simplex structure for category probabilities

That is why multivariate modeling is qualitatively harder than repeating scalar reasoning coordinatewise.

## Failure modes the chapter is trying to prevent

- treating multivariate models as independent scalar models in disguise
- overlooking positive-definiteness and covariance constraints
- interpreting sample correlation as stable without considering sampling variability
- forgetting simplex constraints in Multinomial problems

## Quant research relevance

This chapter matters for quant work because multivariate structure is everywhere:

- covariance estimation for portfolios
- joint modeling of factors and returns
- multinomial or category models for regime or label counts
- Gaussian approximations for vector-valued estimators

The most important practical lesson is that once dependence is present, geometry matters. Matrix structure is not decoration; it controls estimation error and model feasibility.

## What should be promoted out of this source note

- a durable note on multivariate Normal inference
- a durable note on correlation estimation
- a durable note on Multinomial modeling

## Related notes

- [[All of Statistics]]
- [[All of Statistics - Ch 13 Linear and Logistic Regression]]
- [[Portfolio Construction]]
- [[Stats Map]]

## Sources

- [[All of Statistics]]
- [[raw/math_statistics/2004 - wasserman - all of statistics.pdf]]
