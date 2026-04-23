---
title: Time Series Analysis by State Space Methods - Ch 12 Particle Filtering
type: source
status: chapter_ingested
updated: 2026-04-21
tags:
  - source
  - state-space
  - particle-filter
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: chapter_scan
extraction_basis: chapter_scan_plus selected particle-filter sections
technical_depth: moderate
ingest_stage: selective_deepen
chapter_or_section: Ch 12 Particle Filtering
parent_source: "[[Time Series Analysis by State Space Methods]]"
sources:
  - "[[Time Series Analysis by State Space Methods]]"
  - "[[raw/math_statistics/Time Series Analysis by State Space Methods (2012).pdf]]"
---
# Time Series Analysis by State Space Methods - Ch 12 Particle Filtering

## Ingest Scope and Depth

- Ingest stage: `selective_deepen`
- Pass 1: full chapter scan completed.
- Pass 2: local deepening applied to sequential importance sampling, degeneracy and resampling, bootstrap and auxiliary particle filters, and Rao-Blackwellisation.

## Role of the chapter

This chapter is the sequential Monte Carlo extension of the state-space toolbox. It replaces full latent-path proposals with recursive particle updates over time.

## Section map

- filtering by importance sampling
- sequential importance sampling
- bootstrap particle filter
- auxiliary particle filter
- other implementations of particle filtering
- Rao-Blackwellisation

## Locally deepened subparts

### 1. Particle filtering is sequential importance sampling with resampling

The chapter's core message is that online nonlinear filtering can be handled by propagating weighted particles through time, then resampling when degeneracy becomes severe.

### 2. Degeneracy is the central computational failure mode

Resampling is not a minor implementation detail. It is the response to the weight-collapse problem that otherwise kills sequential importance sampling.

### 3. Different particle filters differ mainly through proposal and resampling design

Bootstrap, auxiliary, and other particle methods are variations on the same sequential-Monte-Carlo skeleton with different tradeoffs between simplicity and efficiency.

### 4. Rao-Blackwellisation can lower variance by integrating analytically where possible

This is one of the most reusable ideas in the chapter because it shows how linear-Gaussian substructure can still be exploited inside a particle method.

## Quant relevance

This chapter matters for:

- nonlinear latent-state models
- online filtering under non-Gaussian observations
- stochastic-volatility and regime-style models where linear-Gaussian approximations are inadequate

## Promotion candidates

- [[Particle Filtering]]

## Related notes

- [[Time Series Analysis by State Space Methods]]
- [[Particle Filtering]]
- [[Kalman Filtering]]
- [[Simulation Smoothing]]

## Sources

- [[Time Series Analysis by State Space Methods]]
- [[raw/math_statistics/Time Series Analysis by State Space Methods (2012).pdf]]
