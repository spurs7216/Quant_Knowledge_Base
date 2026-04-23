---
title: Bayesian Filtering and Smoothing - Ch 15 Particle Smoothing
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - particle
  - smoothing
  - sequential-monte-carlo
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: pymupdf4llm_chapter_scan_plus_rendered_pages_for_backward_simulation_and_reweighting_smoothers
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 15 Particle Smoothing
parent_source: "[[Bayesian Filtering and Smoothing]]"
sources:
  - "[[Bayesian Filtering and Smoothing]]"
  - "[[raw/math_statistics/Simo Särkkä and Lennart Svensson, Bayesian Filtering and Smoothing.pdf]]"
---
# Bayesian Filtering and Smoothing - Ch 15 Particle Smoothing

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: theorem-level and algorithm-level extraction completed for the SIR particle smoother, backward simulation, rejection-sampling acceleration, reweighting smoothers, and Rao-Blackwellized particle smoothers.

## Deepening Targets

- If later work needs implementation detail, deepen the complexity trade-offs between backward simulation, rejection sampling, and marginal smoothing.

## Deepened Subparts

- direct SIR particle smoothing and path degeneracy
- backward-simulation particle smoothing
- rejection-sampling acceleration
- marginal reweighting smoothers
- Rao-Blackwellized particle smoothing

## Role of the chapter

This chapter is the backward-inference branch of sequential Monte Carlo. Its main problem is not how to sample paths once, but how to avoid the path degeneracy created by repeated resampling in the forward filter.

## Core mathematical objects

- backward smoothing kernel
  $$p(x_k \given x_{k+1}, y_{1:T}) \propto p(x_{k+1} \given x_k)\,p(x_k \given y_{1:k})$$
- discrete backward-simulation approximation
  $$\Prob\!\paren{x_k = x_k^{(i)} \given x_{k+1}^\star, y_{1:T}} \propto w_k^{(i)}\,p\!\paren{x_{k+1}^\star \given x_k^{(i)}}$$
- marginal smoother recursion
  $$w_{k\given T}^{(i)} \propto w_k^{(i)} \sum_j \frac{w_{k+1\given T}^{(j)}\,p\!\paren{x_{k+1}^{(j)} \given x_k^{(i)}}}{\sum_\ell w_k^{(\ell)}\,p\!\paren{x_{k+1}^{(j)} \given x_k^{(\ell)}}}$$

## Structural map of the chapter

- direct SIR particle smoother
- backward-simulation particle smoother
- rejection-sampling acceleration
- reweighting or marginal particle smoother
- Rao-Blackwellized particle smoothers

## Theorem and derivation spine

### Direct path storage degenerates quickly

The chapter starts from the straightforward idea of retaining the full ancestral histories from the SIR particle filter. The problem is that resampling repeatedly collapses those histories, so the early part of the path becomes nearly deterministic.

### Backward simulation fixes the path-degeneracy problem at the right conditional level

The key practical idea is to sample backward from the approximate kernel
$$p(x_k \given x_{k+1}, y_{1:T}) \propto p(x_{k+1} \given x_k)\,p(x_k \given y_{1:k}),$$
using the filtered particles and weights from the forward pass.

That is the load-bearing chapter result because it turns the forward filter output into non-degenerate trajectory draws.

### Rejection and reweighting smoothers trade cost for different summary targets

The rejection-sampling variant tries to accelerate backward simulation when a useful upper bound is available, while the reweighting smoother focuses on marginal smoothing distributions instead of sampled trajectories.

These are not interchangeable variants. They answer slightly different posterior questions.

### Rao-Blackwellized smoothers matter when part of the model is conditionally Gaussian

As in the filtering chapter, analytic marginalization of linear-Gaussian substructure reduces Monte Carlo variance and often changes the computational feasibility of smoothing.

## Failure modes and misuse points

- confusing filtered particles with smoothed trajectories
- ignoring path degeneracy in direct SIR smoothing
- using backward simulation without checking whether the forward particle approximation is already poor
- overlooking Rao-Blackwellization opportunities in mixed models

## Quant research relevance

This chapter matters for:

- nonlinear latent-path reconstruction
- backward inference in multimodal, heavy-tailed, or mixed discrete-continuous state models
- state estimation problems where sampled trajectories matter for learning or counterfactual analysis

## What should be promoted out of this source note

- refreshed backward-inference core in [[Particle Smoothing]]

## Related notes

- [[Bayesian Filtering and Smoothing]]
- [[Particle Filtering]]
- [[Particle Smoothing]]
- [[General Gaussian Filtering and Smoothing]]

## Sources

- [[Bayesian Filtering and Smoothing]]
- [[raw/math_statistics/Simo Särkkä and Lennart Svensson, Bayesian Filtering and Smoothing.pdf]]
