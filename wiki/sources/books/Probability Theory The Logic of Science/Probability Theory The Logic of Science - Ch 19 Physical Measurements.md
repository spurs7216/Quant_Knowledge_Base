---
title: Probability Theory The Logic of Science - Ch 19 Physical Measurements
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - statistics
  - estimation
  - linear-algebra
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: chapter scan and selected linear-measurement pages via pymupdf
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 19 Physical Measurements
parent_source: "[[Probability Theory The Logic of Science]]"
sources:
  - "[[Probability Theory The Logic of Science]]"
  - "[[raw/math_statistics/Probability Theory The Logic of Science.pdf]]"
---
# Probability Theory The Logic of Science - Ch 19 Physical Measurements

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: deepened the Bayesian linear inverse problem, Gaussian error model, and normal-equation solution.

## Role of the chapter

This chapter turns noisy measurement aggregation into a Bayesian estimation problem. It is the clean bridge from Bayes theory to weighted least squares, linear inverse problems, and posterior covariance estimation.

## Core mathematical objects

- linearized measurement model
  $$y = Ax + \delta$$
- Gaussian error model
  $$p(\delta) \propto \exp\paren{-\frac{1}{2}\delta^\trans W \delta}$$
- posterior for unknown parameters
  $$p(x \mid y) \propto \exp\paren{-\frac{1}{2}(y-Ax)^\trans W (y-Ax)}$$
- normal-equation matrices
  $$K=A^\trans W A, \qquad L=A^\trans W y$$

## Theorem and derivation spine

With linear equations of condition
$$y=Ax+\delta,$$
and independent Gaussian measurement errors with weight matrix `W`, Bayes' theorem yields
$$p(x \mid y) \propto \exp\paren{-\frac{1}{2}(y-Ax)^\trans W (y-Ax)}.$$

Expanding the quadratic form isolates the parameter dependence through
$$K=A^\trans W A, \qquad L=A^\trans W y,$$
so the posterior mode and mean are determined by the linear system
$$K\hat x = L.$$

When `K` is nonsingular,
$$\hat x = (A^\trans W A)^{-1}A^\trans W y.$$

This is the weighted least-squares solution, but Jaynes' point is stronger than the algebraic coincidence: the estimator comes from posterior inference, not from an independent least-squares doctrine.

The same posterior kernel also gives uncertainty:
$$p(x \mid y) \propto \exp\paren{-\frac{1}{2}(x-\hat x)^\trans K (x-\hat x)},$$
so the posterior covariance is
$$\operatorname{Cov}(x \mid y)=K^{-1},$$
when the Gaussian approximation is exact.

## Why this matters later

This chapter is a durable bridge into regression, Kalman filtering, state-space estimation, and linear inverse problems. It also contains Jaynes' important reminder that Gaussian error models can be justified as MaxEnt descriptions of limited knowledge, not only as exact frequency laws.

## Failure modes and misuse points

- treating least squares as fundamental rather than as a special Bayesian/Gaussian case
- using the estimator while ignoring the posterior covariance
- pretending the Gaussian error model is disproved whenever empirical error frequencies are imperfectly Gaussian

## Quant research relevance

The chapter matters for cross-sectional factor estimation, signal extraction, measurement-error problems, state estimation, and all weighted linear systems where the researcher wants both point estimates and coherent uncertainty.

## What should be promoted out of this source note

- a durable note on Bayesian linear inverse problems and weighted least squares

## Related notes

- [[Probability Theory The Logic of Science]]
- [[Maximum Likelihood Estimation]]
- [[Linear Algebra for Data Science, Machine Learning, and Signal Processing]]

## Sources

- [[Probability Theory The Logic of Science]]
- [[raw/math_statistics/Probability Theory The Logic of Science.pdf]]
