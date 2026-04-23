---
title: Convex Optimization - Ch 07 Statistical Estimation
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - optimization
  - convex-optimization
  - chapter-digest
  - statistical-estimation
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: pymupdf_scan_of_ml_map_logistic_and_covariance_estimation_pages
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 07 Statistical Estimation
parent_source: "[[Convex Optimization]]"
sources:
  - "[[Convex Optimization]]"
  - "[[raw/math_statistics/Boyd and Vandenberghe, Convex Optimization.pdf]]"
---
# Convex Optimization - Ch 07 Statistical Estimation

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed against the raw source.
- Pass 2: theorem-level extraction completed for maximum likelihood, MAP estimation, logistic regression, and covariance estimation via the information matrix.

## Deepening Targets

- If the vault later deepens probabilistic modeling, promote the convex-statistics bridge here into a durable note on likelihood geometry.

## Deepened Subparts

- `7.1` parametric distribution estimation
- selected ML examples for Gaussian, Laplace, Poisson, and logistic models
- covariance estimation and inverse-covariance parameterization
- MAP estimation as penalized likelihood

## Role of the chapter

This chapter translates estimation problems into convex programs.

Its durable contribution is not that "statistics uses optimization." The sharper point is that likelihood, prior structure, and parameterization choices determine whether the problem is convex, and therefore whether estimation is certifiable and computationally reliable.

## Core mathematical objects

- maximum likelihood estimator
  $$x_{\mathrm{ML}} \in \argmax_x \; \ell(x) = \argmax_x \log p_x(y)$$
- linear measurements with IID noise
  $$y_i = a_i^\trans x + v_i,\qquad i=1,\dots,m$$
- resulting log-likelihood
  $$\ell(x)=\sum_{i=1}^m \log p\paren{y_i-a_i^\trans x}$$
- MAP estimator
  $$x_{\mathrm{MAP}} \in \argmax_x \; \log p_{y|x}(y|x)+\log p_x(x)$$
- covariance estimation in inverse-covariance variable
  $$\max_{S \succ 0} \; \log\det S - \tr(SY)$$

## Structural map of the chapter

- maximum likelihood in convex form
- canonical noise-model examples
- logistic regression
- covariance estimation
- MAP estimation as prior-augmented likelihood

## Theorem and derivation spine

### Maximum likelihood as convex optimization

Given one observation $y$ from a parametric density $p_x$, the ML estimator solves
$$x_{\mathrm{ML}} \in \argmax_x \log p_x(y).$$

When the log-likelihood is concave in the parameter and the feasible set is convex, ML is a convex optimization problem.

### Linear measurements with IID noise

For the model
$$y_i = a_i^\trans x + v_i,\qquad i=1,\dots,m,$$
with IID noise density $p$, the log-likelihood is
$$\ell(x)=\sum_{i=1}^m \log p\paren{y_i-a_i^\trans x}.$$

This creates a direct bridge to approximation theory:

- Gaussian noise gives least squares
  $$x_{\mathrm{ML}} \in \argmin_x \norm{Ax-y}_2^2$$
- Laplace noise gives $\ell_1$ approximation
  $$x_{\mathrm{ML}} \in \argmin_x \norm{Ax-y}_1$$

So the penalty function is statistically interpretable as negative log-density.

### Logistic regression

Under the logistic model
$$p_i=\Prob(y_i=1 \given u_i)=\frac{\exp(a^\trans u_i+b)}{1+\exp(a^\trans u_i+b)},$$
the log-likelihood can be written as
$$\ell(a,b)=\sum_{i=1}^q \paren{a^\trans u_i+b} - \sum_{i=1}^m \log\paren{1+\exp(a^\trans u_i+b)}.$$

This is concave in $(a,b)$, so logistic regression is a convex optimization problem rather than a heuristic classifier fit.

### Covariance estimation through the information matrix

For Gaussian samples with sample covariance $Y$, the log-likelihood in covariance variable $R$ is not concave. The book's key move is to reparameterize with
$$S=R^{-1}.$$

Then the objective becomes
$$\ell(S)=\frac{N}{2}\log\det S - \frac{N}{2}\tr(SY) + \text{constant},$$
so the ML estimator solves
$$\max_{S \succ 0} \; \log\det S - \tr(SY),$$
possibly with additional convex constraints on $S$.

This is a durable modeling lesson: sometimes convexity is hidden until the right variable is chosen.

### MAP estimation as penalized likelihood

If $x$ itself has prior density $p_x$, then
$$x_{\mathrm{MAP}} \in \argmax_x \; \log p_{y|x}(y|x)+\log p_x(x).$$

So MAP is ML plus a prior-induced penalty. In the linear IID noise case,
$$x_{\mathrm{MAP}} \in \argmax_x \; \log p_x(x)+\sum_{i=1}^m \log p_v\paren{y_i-a_i^\trans x}.$$

That is the statistical counterpart of regularization from Chapter 6.

## Failure modes and misuse points

- assuming an estimation problem is convex before checking parameterization
- forgetting that priors change the estimator, not only the computation
- treating logistic or covariance models as black-box routines instead of explicit convex programs
- using likelihood fit as a substitute for model validation or domain realism

## Quant research relevance

This chapter matters for:

- probabilistic regression and classification
- robust noise modeling
- inverse-covariance estimation and precision structure
- understanding regularization as prior structure

## What should be promoted out of this source note

- a durable note on likelihood geometry and convex estimation
- a durable note on logistic regression and convex classification
- a durable note on covariance and information-matrix estimation

## Related notes

- [[Convex Optimization]]
- [[Convex Optimization - Ch 06 Approximation and Fitting]]
- [[Regularization and Robust Approximation]]
- [[Maximum Likelihood Estimation]]
- [[Logistic Regression]]

## Sources

- [[Convex Optimization]]
- [[raw/math_statistics/Boyd and Vandenberghe, Convex Optimization.pdf]]
