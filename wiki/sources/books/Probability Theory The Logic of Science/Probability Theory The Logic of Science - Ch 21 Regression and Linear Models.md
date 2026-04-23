---
title: Probability Theory The Logic of Science - Ch 21 Regression and Linear Models
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - statistics
  - regression
  - bayesian
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: chapter scan and selected linear-regression pages via pymupdf
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 21 Regression and Linear Models
parent_source: "[[Probability Theory The Logic of Science]]"
sources:
  - "[[Probability Theory The Logic of Science]]"
  - "[[raw/math_statistics/Probability Theory The Logic of Science.pdf]]"
---
# Probability Theory The Logic of Science - Ch 21 Regression and Linear Models

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: deepened the straight-line model, nuisance-parameter logic, and posterior geometry of slope and intercept estimation.

## Role of the chapter

This chapter shows how regression looks when treated as Bayesian inference rather than a menu of procedural tests. It emphasizes that nuisance parameters are not a pathology if they can be integrated out coherently.

## Core mathematical objects

- measurement model
  $$x_i = X_i + e_i, \qquad y_i = Y_i + f_i$$
- straight-line relation
  $$Y_i = \alpha + \beta X_i$$
- quadratic loss surface
  $$Q(\alpha,\beta)=\frac{1}{n}\sum_{i=1}^n (y_i-\alpha-\beta x_i)^2$$
- sample moments
  $$s_x^2=\overline{x^2}-\bar x^2, \qquad s_{xy}=\overline{xy}-\bar x\,\bar y$$

## Theorem and derivation spine

In the simplest case with negligible `x` error and known `\sigma_y`, the sampling law is
$$p(y \mid \alpha,\beta,X) \propto \exp\paren{-\frac{n}{2\sigma_y^2}Q(\alpha,\beta)}.$$

Completing the square yields the natural point estimates
$$\hat \beta = \frac{s_{xy}}{s_x^2}, \qquad
\hat \alpha = \bar y - \hat \beta \bar x.$$

The joint posterior over `(\alpha,\beta)` is Gaussian around that center, with curvature determined by the quadratic form in `Q`. In particular,
$$\operatorname{Var}(\beta \mid D)=\frac{\sigma_y^2}{n\,s_x^2},$$
and the intercept variance is larger and depends on the location of the regressor cloud.

Jaynes uses this setup to make a broader point about nuisance parameters. When a scale parameter such as `\sigma` is unknown and integrated out, the point estimate may stay the same while interval width expands, often replacing Gaussian intervals with `t`-style uncertainty.

## Why this matters later

This chapter connects Bayesian inference to familiar regression formulas without pretending that classical regression theory is fundamental. It also foreshadows later model-comparison work, where parameter integration matters directly.

## Failure modes and misuse points

- acting as if nuisance parameters can be ignored with no uncertainty cost
- treating ordinary least squares formulas as model-free
- forgetting that regression estimates inherit the full assumptions of the measurement model

## Quant research relevance

This chapter matters for factor regressions, forecasting regressions, measurement-error problems, and all linear models where uncertainty about scale or latent covariates changes the reliability of slope estimates.

## What should be promoted out of this source note

- an update to durable regression and likelihood notes with nuisance-parameter penalties

## Related notes

- [[Probability Theory The Logic of Science]]
- [[Maximum Likelihood Estimation]]
- [[Panel Data]]

## Sources

- [[Probability Theory The Logic of Science]]
- [[raw/math_statistics/Probability Theory The Logic of Science.pdf]]
