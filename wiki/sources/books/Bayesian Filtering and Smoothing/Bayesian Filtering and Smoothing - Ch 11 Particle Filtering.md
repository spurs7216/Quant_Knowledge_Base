---
title: Bayesian Filtering and Smoothing - Ch 11 Particle Filtering
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - particle
  - filtering
  - sequential-monte-carlo
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: pymupdf4llm_chapter_scan_plus_rendered_pages_for_importance_sampling_and_particle_filter_algorithms
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 11 Particle Filtering
parent_source: "[[Bayesian Filtering and Smoothing]]"
sources:
  - "[[Bayesian Filtering and Smoothing]]"
  - "[[raw/math_statistics/Simo Särkkä and Lennart Svensson, Bayesian Filtering and Smoothing.pdf]]"
---
# Bayesian Filtering and Smoothing - Ch 11 Particle Filtering

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: theorem-level and algorithm-level extraction completed for importance sampling, SIS, resampling, SIR or bootstrap filters, auxiliary particle filters, and Rao-Blackwellized particle filters.

## Deepening Targets

- If later work needs implementation detail, deepen proposal adaptation, ancestor sampling, and high-dimensional failure diagnostics.

## Deepened Subparts

- Monte Carlo posterior approximation
- importance sampling and SIS weights
- resampling logic and degeneracy
- SIR and bootstrap filters
- auxiliary and Rao-Blackwellized particle filters

## Role of the chapter

This chapter is the simulation-based branch of Bayesian filtering. Its main achievement is to start from posterior expectations and derive particle methods as sequential importance approximations rather than as black-box heuristics.

## Core mathematical objects

- importance-sampling approximation
  $$\mathbb{E}[g(x)\given y_{1:T}] \approx \sum_{i=1}^N w^{(i)} g\paren{x^{(i)}}$$
- generic importance weights
  $$w^{\ast(i)} = \frac{p(y_{1:T}\given x^{(i)})\,p(x^{(i)})}{\pi(x^{(i)}\given y_{1:T})}, \qquad w^{(i)} = \frac{w^{\ast(i)}}{\sum_j w^{\ast(j)}}$$
- sequential importance update
  $$w_k^{\ast(i)} \propto w_{k-1}^{(i)} \frac{p(y_k \given x_k^{(i)})\,p(x_k^{(i)} \given x_{k-1}^{(i)})}{\pi(x_k^{(i)} \given x_{0:k-1}^{(i)}, y_{1:k})}$$
- effective sample size diagnostic
  $$N_\mathrm{eff} = \frac{1}{\sum_{i=1}^N \paren{w_k^{(i)}}^2}$$

## Structural map of the chapter

- Monte Carlo approximations
- importance sampling
- sequential importance sampling
- resampling
- SIR and bootstrap filtering
- auxiliary particle filtering
- Rao-Blackwellized particle filtering

## Theorem and derivation spine

### Particle filtering starts from posterior expectations, not from a named filter

The chapter begins with importance sampling because the real target is always a posterior expectation or posterior distribution. The particle approximation is just a weighted empirical measure for that target.

### Sequential factorization creates the recursive weight update

The move from static importance sampling to sequential importance sampling produces the incremental weight formula
$$w_k^{\ast(i)} \propto w_{k-1}^{(i)} \frac{p(y_k \given x_k^{(i)})\,p(x_k^{(i)} \given x_{k-1}^{(i)})}{\pi(x_k^{(i)} \given x_{0:k-1}^{(i)}, y_{1:k})}.$$

That equation is the core of the whole chapter. Everything else is proposal design or degeneracy management.

### Resampling exists because weight degeneracy is structural

The chapter does not treat resampling as a cosmetic implementation trick. It is there because repeated sequential weighting collapses the effective sample size.

The effective sample size
$$N_\mathrm{eff} = \frac{1}{\sum_i (w_k^{(i)})^2}$$
is the operational signal for when the empirical posterior has become too concentrated on too few particles.

### The bootstrap filter is only one proposal choice

The bootstrap filter uses the transition prior as proposal. The chapter is explicit that this is a convenient baseline, not a universally adequate design.

### Auxiliary and Rao-Blackwellized filters improve different failure modes

The auxiliary particle filter improves proposal quality by incorporating look-ahead information from the next observation, while the Rao-Blackwellized particle filter reduces Monte Carlo variance by integrating out conditionally linear-Gaussian substructure exactly.

That is why "particle filter" is a family name, not one algorithm.

## Failure modes and misuse points

- treating bootstrap filtering as the default even when a better proposal is available
- ignoring weight collapse and reading noisy particle clouds as trustworthy posteriors
- using particle methods when a Gaussian approximation is already structurally adequate
- forgetting that Rao-Blackwellization can change both stability and computational cost materially

## Quant research relevance

This chapter matters for:

- nonlinear or heavy-tailed latent-state models
- hybrid models with conditionally linear or mixed discrete-continuous structure
- deciding when Gaussian approximations are too restrictive

## What should be promoted out of this source note

- refreshed simulation-based core in [[Particle Filtering]]
- smoother-side continuation in [[Particle Smoothing]]

## Related notes

- [[Bayesian Filtering and Smoothing]]
- [[Particle Filtering]]
- [[Particle Smoothing]]
- [[General Gaussian Filtering and Smoothing]]

## Sources

- [[Bayesian Filtering and Smoothing]]
- [[raw/math_statistics/Simo Särkkä and Lennart Svensson, Bayesian Filtering and Smoothing.pdf]]
