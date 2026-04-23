---
title: Bayesian Filtering and Smoothing - Ch 09 Gaussian Filtering by Enabling Approximations
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - gaussian
  - linearization
  - statistical-linear-regression
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: pymupdf4llm_chapter_scan_plus_rendered_pages_for_enabling_linearization_sl_and_slr_equations
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 09 Gaussian Filtering by Enabling Approximations
parent_source: "[[Bayesian Filtering and Smoothing]]"
sources:
  - "[[Bayesian Filtering and Smoothing]]"
  - "[[raw/math_statistics/Simo Särkkä and Lennart Svensson, Bayesian Filtering and Smoothing.pdf]]"
---
# Bayesian Filtering and Smoothing - Ch 09 Gaussian Filtering by Enabling Approximations

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: theorem-level extraction completed for enabling linearization, statistical linearization, statistical linear regression, and the chapter's proof that many named Gaussian filters are the same Kalman backbone with different approximation devices.

## Deepening Targets

- If later work needs numerical-computation detail, deepen the conditional-moment and nested-integration variants behind the practical SLR filters.

## Deepened Subparts

- generic enabling linearization filter template
- statistical linearization as MSE-optimal affine approximation
- statistical linear regression and preserved joint moments
- practical SLR filters and their relationship to sigma-point Gaussian filters

## Role of the chapter

This chapter is the conceptual hinge between generic Gaussian moment-matching filters and posterior-linearization filters. Its main achievement is to isolate the approximation problem from the Kalman algebra.

## Core mathematical objects

- enabling affine Gaussian approximation
  $$x_k \approx A_{k-1}x_{k-1}+a_{k-1}+\tilde e_{k-1}, \qquad \tilde e_{k-1}\sim \mathcal{N}(0,\Lambda_{k-1})$$
  $$y_k \approx H_k x_k + b_k + \tilde v_k, \qquad \tilde v_k\sim \mathcal{N}(0,\Omega_k)$$
- statistical linearization
  $$A = \operatorname{Cov}[y,x]\,P^{-1}, \qquad b = \mathbb{E}[y]-Am$$
- statistical linear regression
  $$y \approx Ax + b + e, \qquad e\sim \mathcal{N}(0,\Lambda)$$
  $$\Lambda = S_R - A P A^\top$$

## Structural map of the chapter

- enabling linearization
- statistical linearization
- statistically linearized filters
- statistical linear regression
- SLR filters
- practical sigma-point and Monte Carlo SLR filters
- relation to other Gaussian filters

## Theorem and derivation spine

### Enabling linearization separates approximation choice from Kalman recursion

Algorithm 9.1 is the chapter's load-bearing abstraction. It says: if a nonlinear model can be approximated by an affine Gaussian surrogate, then Kalman prediction and update equations can be run on that surrogate.

That means many "different" Gaussian filters are really choices about how to build
$$A_{k-1},\,a_{k-1},\,\Lambda_{k-1},\,H_k,\,b_k,\,\Omega_k,$$
not about the downstream recursion.

### Statistical linearization is the MSE-optimal affine map

Theorem 9.3 and Corollaries 9.4 to 9.8 formalize statistical linearization as the affine approximation that minimizes mean-squared error under the chosen distribution.

The durable result is:
$$A = \operatorname{Cov}[y,x]\,P^{-1}, \qquad b = \mathbb{E}[y]-Am.$$

That is the chapter's first major answer to the question: how should a nonlinear transform be linearized if we care about average posterior accuracy rather than only local derivatives?

### Statistical linear regression preserves the joint moments that Gaussian filters need

SLR adds a Gaussian residual term and upgrades the approximation from deterministic linearization to a joint Gaussian surrogate with matched first and second moments.

That is why
$$\Lambda = S_R - A P A^\top$$
matters: it keeps the Kalman equations honest about the part of the transformed uncertainty that cannot be explained by a linear map of the state alone.

### Many sigma-point Gaussian filters are SLR filters in disguise

One of the chapter's strongest claims is that the Gaussian filters from Chapter 8 can be reinterpreted as SLR filters whose required integrals are evaluated by Gauss-Hermite, cubature, unscented, or Monte Carlo rules.

That is a durable unification result, not a naming trick.

## Failure modes and misuse points

- treating different Gaussian filter names as fundamentally different inferential targets
- using statistical linearization without checking which distribution the expectations are taken under
- forgetting that SLR needs both cross-covariance and residual covariance
- thinking moment matching is "derivative free" and therefore automatically robust

## Quant research relevance

This chapter matters for:

- deciding what a named Gaussian filter is actually approximating
- comparing Taylor, sigma-point, and regression-based filters on first principles
- designing Gaussian approximations for awkward observation models

## What should be promoted out of this source note

- refreshed unification logic inside [[General Gaussian Filtering and Smoothing]]
- forward bridge into [[Posterior Linearization in State Space Inference]]

## Related notes

- [[Bayesian Filtering and Smoothing]]
- [[General Gaussian Filtering and Smoothing]]
- [[Kalman Filtering]]
- [[Posterior Linearization in State Space Inference]]

## Sources

- [[Bayesian Filtering and Smoothing]]
- [[raw/math_statistics/Simo Särkkä and Lennart Svensson, Bayesian Filtering and Smoothing.pdf]]
