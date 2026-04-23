---
title: Bayesian Filtering and Smoothing - Ch 10 Posterior Linearization Filtering
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - gaussian
  - posterior-linearization
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: pymupdf4llm_chapter_scan_plus_rendered_pages_for_gslr_pl_and_iplf_update_equations
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 10 Posterior Linearization Filtering
parent_source: "[[Bayesian Filtering and Smoothing]]"
sources:
  - "[[Bayesian Filtering and Smoothing]]"
  - "[[raw/math_statistics/Simo Särkkä and Lennart Svensson, Bayesian Filtering and Smoothing.pdf]]"
---
# Bayesian Filtering and Smoothing - Ch 10 Posterior Linearization Filtering

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: theorem-level and algorithm-level extraction completed for generalized SLR, posterior linearization, iterated posterior linearization, and the IPLF family.

## Deepening Targets

- If later work needs stronger optimization guidance, deepen the practical stopping, damping, and sigma-point implementation choices for IPLF and IPLS.

## Deepened Subparts

- generalized statistical linear regression
- posterior linearization as posterior-distribution SLR
- IPL as the practical fix to the posterior-unknown dilemma
- additive, non-additive, and conditional-moment IPLFs

## Role of the chapter

This is the book's most distinctive Gaussian-approximation chapter. It changes the linearization distribution from the prior or filtering law to the posterior law itself.

## Core mathematical objects

- generalized statistical linear regression with respect to a linearization law $\pi(x)$
  $$A = C_G^\top P_\pi^{-1}, \qquad b = \mu_G - A m_\pi, \qquad \Lambda = S_G - A P_\pi A^\top$$
- posterior linearization choice
  $$\pi(x)=p(x \given y)$$
- IPLF moment calculations for the measurement update
  $$\mu_k^{+,(i-1)} = \int h_k(x)\,\mathcal{N}\!\paren{x \given m_k^{(i-1)}, P_k^{(i-1)}}\,dx$$
  $$P_k^{xy,(i-1)} = \int \paren{x-m_k^{(i-1)}}\paren{h_k(x)-\mu_k^{+,(i-1)}}^\top \mathcal{N}\!\paren{x \given m_k^{(i-1)}, P_k^{(i-1)}}\,dx$$
  $$P_k^{y,(i-1)} = \int \paren{h_k(x)-\mu_k^{+,(i-1)}}\paren{h_k(x)-\mu_k^{+,(i-1)}}^\top \mathcal{N}\!\paren{x \given m_k^{(i-1)}, P_k^{(i-1)}}\,dx + R_k$$
- resulting posterior-aware linearization
  $$H_k^{(i)} = \bracket{P_k^{xy,(i-1)}}^\top \bracket{P_k^{(i-1)}}^{-1}$$
  $$b_k^{(i)} = \mu_k^{+,(i-1)} - H_k^{(i)} m_k^{(i-1)}$$
  $$\Omega_k^{(i)} = P_k^{y,(i-1)} - H_k^{(i)} P_k^{(i-1)} H_k^{(i)\top}$$

## Structural map of the chapter

- generalized statistical linear regression
- posterior linearization
- iterated posterior linearization
- IPLF recursions
- practical sigma-point and Monte Carlo IPLFs
- optimality comparisons with other linearizations

## Theorem and derivation spine

### Generalized SLR says the linearization distribution is a modeling choice

Theorem 10.2 is the chapter's foundational move. It keeps the SLR formulas from Chapter 9 but allows the expectation operator to be taken under an arbitrary distribution $\pi(x)$ instead of the prior or predictive Gaussian.

That exposes a deeper design question: not just how to linearize, but with respect to which distribution.

### Posterior linearization is SLR on the posterior support

Definition 10.4 then chooses
$$\pi(x)=p(x\given y).$$

The logic is strong: if the purpose of linearization is to approximate the region where the posterior mass actually lies, then the posterior is the natural averaging distribution.

### IPL is the practical answer to the posterior-unknown dilemma

Posterior linearization is circular if interpreted literally, because the posterior is the object we are trying to approximate. The chapter resolves that by iteration: use the current Gaussian posterior approximation as the next linearization law.

That yields the IPL algorithm and, at filtering level, the IPLF.

### IPLF is the posterior-aware analogue of IEKF

Algorithm 10.8 makes the contrast explicit.

- IEKF iterates a local Taylor approximation
- IPLF iterates an SLR approximation with respect to the current posterior approximation

The update equations
$$H_k^{(i)},\quad b_k^{(i)},\quad \Omega_k^{(i)}$$
show that the linearization is recomputed from posterior moments at each iteration, not fixed once at the prediction step.

### Posterior linearization extends naturally to sigma-point and Monte Carlo integration

The chapter also shows that posterior linearization is not tied to closed-form integrals. The required moments can be approximated by the same quadrature or Monte Carlo devices used elsewhere in the Gaussian-filter family.

## Failure modes and misuse points

- treating posterior linearization as magic when the posterior approximation is already badly wrong
- ignoring the computational cost of repeated moment recomputation
- confusing posterior-aware linearization with full non-Gaussian inference
- failing to distinguish local IEKF iteration from posterior-distribution iteration

## Quant research relevance

This chapter matters for:

- nonlinear measurement updates where prior-based linearization is too crude
- understanding how Gaussian filters differ by their linearization distribution
- posterior-aware state estimation before escalating to particle methods

## What should be promoted out of this source note

- [[Posterior Linearization in State Space Inference]]
- refreshed comparison layer in [[General Gaussian Filtering and Smoothing]]

## Related notes

- [[Bayesian Filtering and Smoothing]]
- [[General Gaussian Filtering and Smoothing]]
- [[Kalman Filtering]]
- [[Posterior Linearization in State Space Inference]]

## Sources

- [[Bayesian Filtering and Smoothing]]
- [[raw/math_statistics/Simo Särkkä and Lennart Svensson, Bayesian Filtering and Smoothing.pdf]]
