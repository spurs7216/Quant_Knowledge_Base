---
title: Time Series Analysis by State Space Methods - Ch 11 Importance Sampling for Smoothing
type: source
status: chapter_ingested
updated: 2026-04-21
tags:
  - source
  - state-space
  - simulation
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: chapter_scan
extraction_basis: chapter_scan_plus selected importance-sampling sections
technical_depth: moderate
ingest_stage: selective_deepen
chapter_or_section: Ch 11 Importance Sampling for Smoothing
parent_source: "[[Time Series Analysis by State Space Methods]]"
sources:
  - "[[Time Series Analysis by State Space Methods]]"
  - "[[raw/math_statistics/Time Series Analysis by State Space Methods (2012).pdf]]"
---
# Time Series Analysis by State Space Methods - Ch 11 Importance Sampling for Smoothing

## Ingest Scope and Depth

- Ingest stage: `selective_deepen`
- Pass 1: full chapter scan completed.
- Pass 2: local deepening applied to the role of the importance density, weight construction, antithetic variables, and the use of importance sampling for smoothing, likelihood estimation, and parameter work.

## Role of the chapter

This chapter turns smoothing for nonlinear / non-Gaussian models into a simulation problem based on carefully chosen proposal densities.

## Section map

- basic ideas of importance sampling
- choice of an importance density
- implementation details of importance sampling
- estimating functions of the state vector
- estimating loglikelihood and parameters
- importance-sampling weights and diagnostics

## Locally deepened subparts

### 1. The choice of importance density is the whole game

The chapter makes clear that importance sampling succeeds or fails through the gap between the proposal density and the true conditional density.

### 2. Smoothing, likelihood evaluation, and parameter estimation can all be simulation targets

Importance sampling is not just for one latent-state mean. It can be used to estimate functions of states, conditional distributions, and even the likelihood itself.

### 3. Diagnostics are mandatory because simulation error is part of the inference problem

The discussion of weights and diagnostics matters because a formally correct simulation method can still become practically useless when the weight distribution degenerates.

## Quant relevance

This chapter matters when the linear-Gaussian smoother is no longer exact but simulation-based latent inference is still feasible and preferable to brute-force MCMC.

## Promotion candidates

- a later durable note on importance sampling for state-space models

## Related notes

- [[Time Series Analysis by State Space Methods]]
- [[Simulation Smoothing]]
- [[Particle Filtering]]

## Sources

- [[Time Series Analysis by State Space Methods]]
- [[raw/math_statistics/Time Series Analysis by State Space Methods (2012).pdf]]
