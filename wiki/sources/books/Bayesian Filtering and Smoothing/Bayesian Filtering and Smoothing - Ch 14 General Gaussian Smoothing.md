---
title: Bayesian Filtering and Smoothing - Ch 14 General Gaussian Smoothing
type: source
status: chapter_ingested
updated: 2026-04-21
tags:
  - source
  - gaussian
  - smoothing
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: chapter_text_plus_selected_theorems_and_algorithms
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 14 General Gaussian Smoothing
parent_source: "[[Bayesian Filtering and Smoothing]]"
sources:
  - "[[Bayesian Filtering and Smoothing]]"
  - "[[raw/math_statistics/Simo Särkkä and Lennart Svensson, Bayesian Filtering and Smoothing.pdf]]"
---
# Bayesian Filtering and Smoothing - Ch 14 General Gaussian Smoothing

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: theorem-level extraction completed for Gaussian RTS smoothing, sigma-point smoothers, statistical-linear-regression smoothers, and posterior-linearization smoothers.

## Why this chapter is load-bearing

This chapter completes the nonlinear Gaussian approximation story by showing that the same approximation families used in filtering have backward-smoothing analogues.

## Core objects

- Gaussian RTS smoother
- cross-covariance `D_{k+1}`
- sigma-point smoother variants
- statistical-linear-regression smoothers
- posterior-linearization smoothers

## Structural map

- general Gaussian Rauch-Tung-Striebel smoother
- Gauss-Hermite Rauch-Tung-Striebel smoother
- cubature Rauch-Tung-Striebel smoother
- unscented Rauch-Tung-Striebel smoother
- higher order cubature and unscented RTS smoothers
- statistical linear regression smoothers
- posterior linearization smoothers

## Theorem and derivation spine

### 1. Moment matching extends naturally from filtering to smoothing

Algorithm 14.1 shows the general Gaussian RTS smoother: approximate the needed transition moments and cross-covariances, then run an RTS-style backward pass.

### 2. Sigma-point filters have sigma-point smoother counterparts

The chapter makes the family structure explicit:

- Gauss-Hermite
- cubature
- unscented

all yield smoother variants once their moment approximations are inserted into the backward recursion.

### 3. Statistical linear regression and posterior linearization survive the backward pass

The smoothing story is not limited to moment-matching sigma-point methods. The later sections show that SLR and posterior-linearization approximations also induce Gaussian smoothers.

## Quant relevance

This chapter matters for:

- retrospective inference in nonlinear latent-state systems
- smoothing noisy trajectories when forward-only filtering is too myopic
- understanding that smoothing quality depends on the same approximation choices as filtering quality

## Promotion candidates

- [[General Gaussian Filtering and Smoothing]]

## Related notes

- [[Bayesian Filtering and Smoothing]]
- [[General Gaussian Filtering and Smoothing]]
- [[Particle Smoothing]]
- [[Kalman Filtering]]

## Sources

- [[Bayesian Filtering and Smoothing]]
- [[raw/math_statistics/Simo Särkkä and Lennart Svensson, Bayesian Filtering and Smoothing.pdf]]
