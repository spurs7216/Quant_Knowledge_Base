---
title: Bayesian Filtering and Smoothing - Ch 13 Extended Rauch-Tung-Striebel Smoothing
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - smoothing
  - nonlinear
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: pymupdf4llm_chapter_scan_plus_rendered_pages_for_ertss_and_iertss_equations
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 13 Extended Rauch-Tung-Striebel Smoothing
parent_source: "[[Bayesian Filtering and Smoothing]]"
sources:
  - "[[Bayesian Filtering and Smoothing]]"
  - "[[raw/math_statistics/Simo Särkkä and Lennart Svensson, Bayesian Filtering and Smoothing.pdf]]"
---
# Bayesian Filtering and Smoothing - Ch 13 Extended Rauch-Tung-Striebel Smoothing

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: theorem-level and derivation-level extraction completed for extended RTS recursions, higher-order variants, IERTSS, and its Gauss-Newton interpretation.

## Deepening Targets

- If later work needs solver guidance, deepen the Levenberg-Marquardt and line-search IERTSS variants into a dedicated nonlinear-smoothing numerics note.

## Deepened Subparts

- extended RTS recursions
- second-order extended RTS smoothing
- IERTSS
- trajectory-level Gauss-Newton interpretation

## Role of the chapter

This chapter is the smoothing-side counterpart of the EKF chapter. It matters because it shows exactly what is lost when nonlinear smoothing is treated as just "run an EKF and smooth afterward."

## Core mathematical objects

- extended RTS smoother
  $$m_{k+1}^- = f(m_k), \qquad P_{k+1}^- = F_x(m_k) P_k F_x(m_k)^\top + Q_k$$
  $$G_k = P_k F_x(m_k)^\top \bracket{P_{k+1}^-}^{-1}$$
  $$m_k^s = m_k + G_k\paren{m_{k+1}^s - m_{k+1}^-}$$
  $$P_k^s = P_k + G_k\paren{P_{k+1}^s - P_{k+1}^-}G_k^\top$$
- IERTSS forward-backward iteration
  $$x_{0:T}^{(i)} = m_{0:T}^{s,(i)}$$

## Structural map of the chapter

- extended RTS smoother
- higher-order extended RTS smoothers
- iterated extended RTS smoother
- damping and line-search variants

## Theorem and derivation spine

### ERTSS is RTS smoothing on a Taylor-linearized nonlinear model

Algorithm 13.1 shows that the smoother gain and backward recursion still look like RTS formulas. What changes is that the predicted moments and cross-covariances now come from local Jacobian-based linearization.

### Nonlinear smoothing is stronger than nonlinear filtering

The extended smoother is not simply "EKF plus one backward pass." It is a posterior object conditioned on all observations, so it can correct states in ways that a one-step filter cannot.

### IERTSS is a full-trajectory Gauss-Newton algorithm

The chapter's strongest conceptual claim is that IERTSS is a Gauss-Newton method on the entire latent path.

That is why it iterates both the forward filter and the backward smoother and then sets
$$x_{0:T}^{(i)} = m_{0:T}^{s,(i)}.$$

### IERTSS targets a stronger object than IEKF

The book is explicit about the contrast:

- IEKF improves a single update locally
- IERTSS improves the whole latent trajectory and can converge to the MAP path under suitable conditions

That distinction matters for any inference problem where latent-path reconstruction is the real objective.

## Failure modes and misuse points

- treating a smoothed trajectory as if it came from a global nonlinear optimization when only one non-iterated pass was used
- assuming IEKF intuition automatically transfers to trajectory smoothing
- forgetting that IERTSS can still need damping or line-search stabilization
- using local Taylor smoothing in problems with strongly nonlocal or multimodal posteriors

## Quant research relevance

This chapter matters for:

- nonlinear latent-path reconstruction
- state estimation problems where the full sample path matters more than online filtering
- distinguishing local update iteration from true trajectory optimization

## What should be promoted out of this source note

- refreshed smoother-side local-linearization branch inside [[General Gaussian Filtering and Smoothing]]

## Related notes

- [[Bayesian Filtering and Smoothing]]
- [[General Gaussian Filtering and Smoothing]]
- [[Particle Smoothing]]

## Sources

- [[Bayesian Filtering and Smoothing]]
- [[raw/math_statistics/Simo Särkkä and Lennart Svensson, Bayesian Filtering and Smoothing.pdf]]
