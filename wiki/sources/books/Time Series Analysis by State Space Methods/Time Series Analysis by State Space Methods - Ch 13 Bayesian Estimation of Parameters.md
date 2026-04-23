---
title: Time Series Analysis by State Space Methods - Ch 13 Bayesian Estimation of Parameters
type: source
status: chapter_ingested
updated: 2026-04-21
tags:
  - source
  - state-space
  - bayesian
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: chapter_scan
extraction_basis: chapter_scan_plus selected posterior-analysis sections
technical_depth: moderate
ingest_stage: selective_deepen
chapter_or_section: Ch 13 Bayesian Estimation of Parameters
parent_source: "[[Time Series Analysis by State Space Methods]]"
sources:
  - "[[Time Series Analysis by State Space Methods]]"
  - "[[raw/math_statistics/Time Series Analysis by State Space Methods (2012).pdf]]"
---
# Time Series Analysis by State Space Methods - Ch 13 Bayesian Estimation of Parameters

## Ingest Scope and Depth

- Ingest stage: `selective_deepen`
- Pass 1: full chapter scan completed.
- Pass 2: local deepening applied to posterior analysis for linear-Gaussian and nonlinear / non-Gaussian models, non-informative priors, and the role of MCMC relative to importance sampling.

## Role of the chapter

This chapter is the parameter-level Bayesian layer of the monograph. It asks how the state-space toolkit changes once parameters themselves are treated as random objects.

## Section map

- posterior analysis for linear Gaussian model
- posterior analysis for a nonlinear non-Gaussian model
- Markov chain Monte Carlo methods

## Locally deepened subparts

### 1. Bayesian parameter analysis can still reuse the state-space machinery

The chapter uses importance sampling and state-space calculations to evaluate posterior objects rather than replacing the whole framework.

### 2. Linear-Gaussian and nonlinear / non-Gaussian cases separate naturally

The linear-Gaussian case permits cleaner posterior calculations, while the nonlinear / non-Gaussian case needs more simulation-heavy treatment.

### 3. MCMC is presented as an alternative, not the only route

The chapter's stance is pragmatic: importance sampling can remain attractive for the problems considered, with MCMC included mainly for comparison and broader applicability.

## Quant relevance

This chapter matters when parameter uncertainty itself is material and one wants posterior rather than plug-in inference for latent-state models.

## Promotion candidates

- stronger links to [[Bayesian Filtering and Smoothing]]
- a later note on Bayesian parameter inference in state-space models

## Related notes

- [[Time Series Analysis by State Space Methods]]
- [[Bayesian Filtering and Smoothing]]
- [[Particle Filtering]]

## Sources

- [[Time Series Analysis by State Space Methods]]
- [[raw/math_statistics/Time Series Analysis by State Space Methods (2012).pdf]]
