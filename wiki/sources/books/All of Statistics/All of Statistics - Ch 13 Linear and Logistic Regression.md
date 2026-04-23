---
title: All of Statistics - Ch 13 Linear and Logistic Regression
type: source
status: chapter_ingested
updated: 2026-04-19
tags:
  - source
  - statistics
  - regression
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: full_source
extraction_basis: full_text
technical_depth: moderate
ingest_stage: scan
chapter_or_section: Ch 13 Linear and Logistic Regression
parent_source: "[[All of Statistics]]"
sources:
  - "[[All of Statistics]]"
  - "[[raw/math_statistics/2004 - wasserman - all of statistics.pdf]]"
---
# All of Statistics - Ch 13 Linear and Logistic Regression

## Ingest Scope and Depth

- Ingest stage: `scan`
- Pass 1: full chapter scan completed against the raw source.
- Pass 2: rescan completed to identify which subparts are load-bearing enough to justify a later deep rewrite.

## Deepening Targets

- Deepen least squares as projection in Euclidean space, not just as an optimization formula.
- Deepen Theorem 13.11 so prediction intervals are derived as "estimation uncertainty plus new-noise uncertainty" rather than memorized as a template.
- Deepen Theorem 13.15 and the AIC / Cp / cross-validation / BIC discussion if this chapter becomes a main model-selection spine for the vault.
- Deepen logistic regression if the vault needs a tighter bridge from statistical inference into classification and event-probability models.

## Deepened Subparts

- No subpart has been rewritten at full deep-note depth yet.

## Worth Attending From The Rescan

- Theorem 13.7 is the key bridge between squared-error fitting and likelihood: under Gaussian errors, least squares is maximum likelihood. This is the point where geometry and probability become the same estimator.
- Theorem 13.8 is more important than it first appears because the sampling variance of the coefficients is governed by the design geometry through `s_X^2` and, in multiple regression, through `(X^T X)^{-1}`. The matrix is not bookkeeping; it is the source of variance inflation and collinearity fragility.
- Theorem 13.11 is load-bearing because it separates prediction for a future observation from confidence for a conditional mean. In quant work, confusing these two is one of the easiest ways to understate uncertainty.
- Section 13.6 is worth special attention even without a full deep rewrite. Theorem 13.15 shows exactly why training error is optimistic, and the chapter's Cp / AIC / cross-validation / BIC discussion is the first concrete warning against naive in-sample model search.
- The logistic-regression section is structurally important even though it is short: it replaces linear modeling of a conditional mean on `R` with link-based modeling of a conditional probability on `[0,1]`.

## Role of the chapter

This chapter brings the earlier inferential machinery into one of the central statistical workhorses: regression.

It covers:

- simple linear regression
- least squares and its likelihood interpretation
- prediction
- multiple regression in matrix form
- model selection
- logistic regression

This is one of the most directly applicable chapters in the book.

## Core mathematical objects

- regression function `E(Y | X=x)`
- linear model `Y = beta_0 + beta_1 x + epsilon`
- least squares estimates
- design matrix `X`
- fitted values and residuals
- prediction intervals
- AIC and model-selection criteria
- logistic link for binary outcomes

## Simple linear regression

### Definitions 13.1 and 13.3

The simple linear regression model imposes a linear conditional mean, and least squares estimates are defined by minimizing the sum of squared residuals.

### Theorem 13.4

The explicit formula for the least squares slope and intercept is given.

This matters because it reveals what the regression is doing geometrically:

- center the variables
- scale by variation in the regressor
- project the response onto the span of the regressor and intercept

## Least squares and likelihood

### Theorem 13.7

Under Normal errors, least squares equals maximum likelihood.

This is an important structural bridge:

- optimization by squared residuals
- and probabilistic estimation by likelihood

coincide under a Gaussian noise model.

### Theorem 13.8 and 13.9

The chapter gives distributional properties of the least-squares estimators and their large-sample behavior.

The main lesson is that regression uncertainty is inherited from both:

- the noise scale
- the geometry of the design

## Prediction

### Theorem 13.11

Prediction intervals are wider than confidence intervals for the mean because they include:

- uncertainty about the estimated mean relationship
- irreducible noise in a new draw

This distinction is often neglected in applied work.

## Multiple regression

### Theorem 13.13

The matrix formula

`hat beta = (X^T X)^{-1} X^T Y`

is the core result of the chapter.

This formula is not just computational. It explains:

- why collinearity matters through invertibility of `X^T X`
- why the geometry of the regressors controls variance
- why orthogonality simplifies estimation

## Model selection

### Theorem 13.15 and Theorem 13.18

The chapter emphasizes that training error is downward biased as an estimate of predictive error and introduces AIC as an approximately unbiased predictive-risk criterion.

This is a crucial lesson. It prevents the researcher from mistaking in-sample fit for generalization quality.

## Logistic regression

The chapter then treats binary response modeling through the logistic link.

The important conceptual move is:

- linear regression models the conditional mean directly on the real line
- logistic regression models the conditional probability through a link that keeps predictions in `[0,1]`

This is not just a change of formula. It is a change in the geometry of the model.

## What the chapter is really teaching

Regression is not only a line-fitting exercise. It is:

- a conditional mean model
- an estimation problem
- a prediction problem
- and a model-selection problem

All four aspects have to be kept separate.

## Failure modes the chapter is trying to prevent

- confusing explanation of a conditional mean with prediction of a new observation
- treating training error as predictive error
- ignoring collinearity and design geometry
- using linear regression for binary outcomes without thinking about range constraints
- forgetting that model-selection uncertainty is real even after a model is chosen

## Quant research relevance

This chapter is central to quant research:

- cross-sectional factor regressions
- time-series predictive regressions
- logistic default or event-probability models
- feature selection and predictive model comparison
- forecast intervals versus realized outcome uncertainty

The biggest practical lesson is that regression coefficients are not enough. One must also track design geometry, prediction error, and model-selection bias.

## What should be promoted out of this source note

- a durable note on least squares as projection
- a durable note on regression uncertainty and prediction intervals
- a durable note on multiple regression geometry
- a durable note on AIC and model selection
- a durable note on logistic regression

## Related notes

- [[All of Statistics]]
- [[All of Statistics - Ch 14 Multivariate Models]]
- [[Panel Data]]
- [[Time-Series Forecasting]]
- [[Stats Map]]

## Sources

- [[All of Statistics]]
- [[raw/math_statistics/2004 - wasserman - all of statistics.pdf]]
