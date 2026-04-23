---
title: Bayesian Filtering and Smoothing - Ch 12 Bayesian Smoothing Equations and Exact Solutions
type: source
status: chapter_ingested
updated: 2026-04-21
tags:
  - source
  - smoothing
  - state-space
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: chapter_text_plus_selected_theorems
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 12 Bayesian Smoothing Equations and Exact Solutions
parent_source: "[[Bayesian Filtering and Smoothing]]"
sources:
  - "[[Bayesian Filtering and Smoothing]]"
  - "[[raw/math_statistics/Simo Särkkä and Lennart Svensson, Bayesian Filtering and Smoothing.pdf]]"
---
# Bayesian Filtering and Smoothing - Ch 12 Bayesian Smoothing Equations and Exact Solutions

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: theorem-level extraction completed for Bayesian smoothing equations, the RTS smoother, affine RTS smoothing, discrete-state smoothing, and the Viterbi algorithm.

## Why this chapter is load-bearing

This chapter gives the exact backward recursion target for smoothing just as Chapter 6 did for filtering.

## Core objects

- smoothing distribution `p(x_k | y_{1:T})`
- forward-backward recursion
- RTS gain `G_k`
- smoothed mean `m_k^s` and covariance `P_k^s`
- discrete-state smoothing recursion
- MAP path and Viterbi value function

## Structural map

- Bayesian smoothing equations
- Rauch-Tung-Striebel smoother
- affine Rauch-Tung-Striebel smoother
- Bayesian smoother for discrete state spaces
- Viterbi algorithm

## Theorem and derivation spine

### 1. Smoothing is backward recursion on top of filtering

Theorem 12.1 states the Bayesian smoothing equations. The structural lesson is simple:

- filtering computes `p(x_k | y_{1:k})`
- smoothing reuses that forward pass and then moves backward using the transition structure plus future information

### 2. RTS is the exact linear-Gaussian smoother

Theorem 12.2 gives the closed-form fixed-interval smoother. It is the smoothing counterpart of the Kalman filter and the backbone behind later approximate smoothers.

### 3. Affine and discrete-state specializations remain exact

The chapter extends the exact smoothing story beyond the strict linear homogeneous case and also shows how discrete-state smoothing fits the same Bayesian logic.

### 4. Viterbi solves MAP path estimation, not marginal state smoothing

The Viterbi algorithm matters because it estimates the most likely trajectory. That is a different inferential object from choosing statewise marginal modes.

## Quant relevance

This chapter matters for:

- latent-state reconstruction using future information
- separating online filtering from retrospective inference
- hidden-regime path estimation
- understanding what later Gaussian and particle smoothers are approximating

## Promotion candidates

- [[General Gaussian Filtering and Smoothing]]
- future durable note on the Viterbi algorithm

## Related notes

- [[Bayesian Filtering and Smoothing]]
- [[Kalman Filtering]]
- [[Particle Smoothing]]
- [[General Gaussian Filtering and Smoothing]]

## Sources

- [[Bayesian Filtering and Smoothing]]
- [[raw/math_statistics/Simo Särkkä and Lennart Svensson, Bayesian Filtering and Smoothing.pdf]]
