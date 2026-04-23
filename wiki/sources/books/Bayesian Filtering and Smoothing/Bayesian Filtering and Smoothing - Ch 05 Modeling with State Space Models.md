---
title: Bayesian Filtering and Smoothing - Ch 05 Modeling with State Space Models
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - state-space
  - modeling
  - hidden-markov-models
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: pymupdf4llm_chapter_scan_plus_targeted_modeling_sections_for_non_gaussian_observations_and_hmms
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 05 Modeling with State Space Models
parent_source: "[[Bayesian Filtering and Smoothing]]"
sources:
  - "[[Bayesian Filtering and Smoothing]]"
  - "[[raw/math_statistics/Simo Särkkä and Lennart Svensson, Bayesian Filtering and Smoothing.pdf]]"
---
# Bayesian Filtering and Smoothing - Ch 05 Modeling with State Space Models

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: object-level deepening completed for Gaussian versus non-Gaussian observation laws, inputs, linear-in-parameters embeddings, autoregressive companion-form models, and discrete-state HMM structure.

## Deepening Targets

- If later work needs a stronger observation-model branch, deepen the clutter, robust, and count-measurement examples into a dedicated note on non-Gaussian state-space likelihoods.

## Deepened Subparts

- nonlinear Gaussian and non-Gaussian state-space grammar
- measurements as inputs and regression-like embeddings
- linear-in-parameters models via state augmentation
- autoregressive models in companion state form
- discrete-state HMMs as exact Bayesian state-space models

## Role of the chapter

This chapter is the modeling grammar chapter. It explains which structural choices create a linear-Gaussian problem, which ones create a nonlinear-Gaussian problem, and which ones force a truly non-Gaussian inference problem.

## Core mathematical objects

- additive-noise state-space model
  $$x_k = f_{k-1}(x_{k-1}) + q_{k-1}, \qquad q_{k-1}\sim \mathcal{N}(0,Q_{k-1})$$
  $$y_k = h_k(x_k) + r_k, \qquad r_k\sim \mathcal{N}(0,R_k)$$
- general observation model
  $$y_k \sim p(y_k \given x_k)$$
- autoregressive state embedding
  $$z_k = \sum_{j=1}^p a_j z_{k-j} + q_k, \qquad x_k = \begin{bmatrix} z_k & z_{k-1} & \cdots & z_{k-p+1}\end{bmatrix}^\top$$
- discrete-state Bayesian recursion
  $$p(x_k=j \given y_{1:k}) \propto p(y_k \given x_k=j)\sum_i p(x_k=j \given x_{k-1}=i)\,p(x_{k-1}=i \given y_{1:k-1})$$

## Structural map of the chapter

- linear and nonlinear Gaussian state-space models
- non-Gaussian observation laws
- input-driven models
- parameter and regression embeddings
- autoregressive models in state form
- discrete-state HMMs

## Theorem and modeling spine

### State-space modeling means separating latent dynamics from observation law

The chapter's most durable lesson is that a state-space model is not defined by "Kalman filter syntax." It is defined by two conditional objects:

- a transition law for the hidden state
- a measurement law linking observations to that state

Once those two objects are explicit, the algorithm question can be asked honestly.

### Non-Gaussian observations change the inferential target, not only the implementation

The book uses robust, mixture, and clutter-style measurements to show that the observation law
$$p(y_k \given x_k)$$
is part of the model, not an afterthought.

If that law is not Gaussian, then exact Kalman recursions are no longer the right target even if the latent dynamics are simple.

### Inputs and parameter embeddings turn classical regression into state-space inference

The chapter shows that exogenous signals and unknown coefficients can be absorbed into a state-space representation rather than treated as a separate methodology.

That matters because it is the gateway to:

- dynamic regression
- time-varying coefficients
- recursive parameter tracking

### Autoregressive models are state-space models in companion form

The AR section is structurally important because it shows that familiar time-series models can be rewritten as first-order latent-state systems by augmenting the state vector.

That is the finite-dimensional bridge between classical time-series notation and recursive Bayesian estimation.

### Hidden Markov models are exact discrete-state Bayesian filters

The HMM section is one of the book's distinctive statistical angles. The same Bayesian recursion used for continuous states survives on a discrete state space, with integrals replaced by sums.

That makes regime-switching, channel-state, and event-state models part of the same Bayesian architecture rather than a separate toolbox.

## Failure modes and misuse points

- treating Gaussian observation noise as default even when outliers, counts, or clutter are structurally present
- forgetting that the state definition itself is a modeling choice that can absorb lags, inputs, and parameters
- using state augmentation casually without checking identifiability or scale
- treating HMMs as pattern-recognition objects rather than exact Bayesian state-space models

## Quant research relevance

This chapter matters for:

- dynamic regression and latent-factor tracking
- robust measurement design under outliers or contaminated prints
- hidden-regime or event-state models
- classical AR structure recast into Bayesian state-space form

## What should be promoted out of this source note

- refreshed modeling support in [[State Space Models]]
- refreshed discrete-state machinery in [[Hidden Markov Models and Switching Autoregression]]

## Related notes

- [[Bayesian Filtering and Smoothing]]
- [[State Space Models]]
- [[Hidden Markov Models and Switching Autoregression]]
- [[Kalman Filtering]]

## Sources

- [[Bayesian Filtering and Smoothing]]
- [[raw/math_statistics/Simo Särkkä and Lennart Svensson, Bayesian Filtering and Smoothing.pdf]]
