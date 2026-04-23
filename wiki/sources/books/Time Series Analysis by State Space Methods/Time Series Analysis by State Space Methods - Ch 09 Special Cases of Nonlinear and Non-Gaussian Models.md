---
title: Time Series Analysis by State Space Methods - Ch 09 Special Cases of Nonlinear and Non-Gaussian Models
type: source
status: chapter_ingested
updated: 2026-04-21
tags:
  - source
  - state-space
  - nonlinear
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: chapter_scan
extraction_basis: chapter_scan_plus selected sections on exponential family and stochastic volatility
technical_depth: moderate
ingest_stage: selective_deepen
chapter_or_section: Ch 09 Special Cases of Nonlinear and Non-Gaussian Models
parent_source: "[[Time Series Analysis by State Space Methods]]"
sources:
  - "[[Time Series Analysis by State Space Methods]]"
  - "[[raw/math_statistics/Time Series Analysis by State Space Methods (2012).pdf]]"
---
# Time Series Analysis by State Space Methods - Ch 09 Special Cases of Nonlinear and Non-Gaussian Models

## Ingest Scope and Depth

- Ingest stage: `selective_deepen`
- Pass 1: full chapter scan completed.
- Pass 2: local deepening applied to exponential-family observation models, heavy-tailed disturbances, stochastic volatility, and the financial-model examples that motivate nonlinear / non-Gaussian state-space work.

## Role of the chapter

This chapter widens the state-space framework beyond linear Gaussian assumptions by cataloguing the main families of models that break those assumptions while keeping the latent-state structure.

## Section map

- models with a linear Gaussian signal
- exponential family models
- heavy-tailed distributions
- stochastic volatility models
- other financial models
- nonlinear models

## Locally deepened subparts

### 1. Non-Gaussian observation models can keep a linear Gaussian signal

This is the cleanest extension path because the latent dynamics remain tractable while the observation model carries the non-Gaussian behavior.

### 2. Exponential-family models are the natural discrete-data extension

Poisson, binary, binomial, negative binomial, and multinomial observation models show that state-space methods are not limited to continuous observation problems.

### 3. Stochastic volatility is a state-space model, not only a finance curiosity

The stochastic-volatility section is especially relevant for the vault because it shows how latent volatility processes fit the state-space paradigm and how GARCH can be understood as a related but different object.

### 4. Heavy-tailed and nonlinear variants motivate the later approximate and simulation chapters

The chapter's real strategic role is to define the target class that Chapters 10 to 13 then try to handle.

## Quant relevance

This chapter matters for:

- count-data and binary-state observation models
- heavy-tailed financial time series
- latent volatility modeling
- nonlinear dynamic systems that keep the state-space backbone

## Promotion candidates

- stronger updates to [[State Space Models]]
- a later durable note on stochastic volatility

## Related notes

- [[Time Series Analysis by State Space Methods]]
- [[State Space Models]]
- [[GARCH Models]]
- [[Particle Filtering]]

## Sources

- [[Time Series Analysis by State Space Methods]]
- [[raw/math_statistics/Time Series Analysis by State Space Methods (2012).pdf]]
