---
title: Bayesian Filtering and Smoothing - Ch 07 Extended Kalman Filtering
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - kalman
  - nonlinear
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: pymupdf4llm_chapter_scan_plus_rendered_pages_for_ekf_iekf_and_gauss_newton_update_equations
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 07 Extended Kalman Filtering
parent_source: "[[Bayesian Filtering and Smoothing]]"
sources:
  - "[[Bayesian Filtering and Smoothing]]"
  - "[[raw/math_statistics/Simo Särkkä and Lennart Svensson, Bayesian Filtering and Smoothing.pdf]]"
---
# Bayesian Filtering and Smoothing - Ch 07 Extended Kalman Filtering

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: theorem-level and derivation-level extraction completed for Taylor linearization, first-order EKF recursions, second-order extensions, IEKF, and the chapter's Gauss-Newton interpretation.

## Deepening Targets

- If later work needs numerics guidance, deepen the Levenberg-Marquardt and line-search stabilization rules together with automatic-differentiation implementation details.

## Deepened Subparts

- Gaussian approximation from first-order Taylor expansion
- additive and non-additive EKF recursions
- second-order EKF
- IEKF as local Gauss-Newton refinement
- convergence-control variants

## Role of the chapter

This chapter is the classical local-linearization branch of nonlinear Bayesian filtering. It matters because later Gaussian filters and smoothers can all be compared to it.

## Core mathematical objects

- first-order linearization of a nonlinear transform
  $$g(x) \approx g(m) + G_x(m)(x-m)$$
- additive-noise EKF prediction and update
  $$m_k^- = f(m_{k-1})$$
  $$P_k^- = F_x(m_{k-1})P_{k-1}F_x(m_{k-1})^\top + Q_{k-1}$$
  $$\mu_k = h(m_k^-), \qquad S_k = H_x(m_k^-)P_k^-H_x(m_k^-)^\top + R_k$$
  $$K_k = P_k^- H_x(m_k^-)^\top S_k^{-1}$$
  $$m_k = m_k^- + K_k\paren{y_k-\mu_k}, \qquad P_k = P_k^- - K_k S_k K_k^\top$$
- local MAP objective behind IEKF
  $$\varphi(x_k)=\frac{1}{2}(x_k-m_k^-)^\top (P_k^-)^{-1}(x_k-m_k^-) + \frac{1}{2}\paren{y_k-h(x_k)}^\top R_k^{-1}\paren{y_k-h(x_k)}$$

## Structural map of the chapter

- Gaussian approximation from Taylor expansion
- additive and non-additive EKF recursions
- higher-order EKF corrections
- IEKF update iteration
- Levenberg-Marquardt and line-search variants
- automatic-differentiation support

## Theorem and derivation spine

### EKF is Kalman filtering after local Taylor expansion

The chapter derives the EKF by approximating nonlinear transforms of Gaussian variables with first-order Taylor expansions. The resulting algorithm is not exact Bayesian filtering. It is Kalman algebra applied to a locally linearized model.

### The Jacobian enters because the method is local

All of the chapter's first-order formulas come from Jacobians of the dynamic and measurement maps. That is why the quality of the filter depends directly on the geometry around the current expansion point.

### IEKF is a local Gauss-Newton method, not just repeated EKF

The chapter makes an important conceptual move: the IEKF iterates the measurement update because it is improving the local posterior approximation around a better point.

The load-bearing fact is that the IEKF update corresponds to a Gauss-Newton refinement of the local objective
$$\varphi(x_k),$$
not to a full trajectory optimization.

### Higher-order terms buy accuracy at algebraic and numerical cost

The second-order EKF keeps Hessian information and changes both the predicted mean and covariance. The book is honest that the gain is not free: the algebra is heavier and implementation becomes much less attractive than sigma-point or posterior-linearization alternatives.

### Convergence control is needed because local geometry can be bad

The Levenberg-Marquardt and line-search variants are not cosmetic additions. They are there because naive iteration can diverge when the current Gaussian approximation is poor or the measurement nonlinearity is too sharp.

## Failure modes and misuse points

- using EKF when the posterior is clearly multimodal, skewed, or strongly nonlocal
- forgetting that Jacobian choice is expansion-point choice
- treating IEKF convergence as convergence to the global posterior mode
- ignoring covariance pathologies when repeated linearization is numerically unstable

## Quant research relevance

This chapter matters for:

- mildly nonlinear latent-state models
- understanding the difference between local linearization and posterior-aware approximation
- deciding when EKF is still acceptable before escalating to sigma-point or particle methods

## What should be promoted out of this source note

- refreshed local-linearization branch inside [[General Gaussian Filtering and Smoothing]]
- comparison support for [[Posterior Linearization in State Space Inference]]

## Related notes

- [[Bayesian Filtering and Smoothing]]
- [[Kalman Filtering]]
- [[General Gaussian Filtering and Smoothing]]
- [[Posterior Linearization in State Space Inference]]

## Sources

- [[Bayesian Filtering and Smoothing]]
- [[raw/math_statistics/Simo Särkkä and Lennart Svensson, Bayesian Filtering and Smoothing.pdf]]
