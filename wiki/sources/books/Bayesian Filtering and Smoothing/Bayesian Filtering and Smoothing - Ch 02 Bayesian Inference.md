---
title: Bayesian Filtering and Smoothing - Ch 02 Bayesian Inference
type: source
status: chapter_ingested
updated: 2026-04-21
tags:
  - source
  - bayesian
  - inference
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: chapter_scan
extraction_basis: contents_plus_preface_and_chapter_intro
technical_depth: light
ingest_stage: scan
chapter_or_section: Ch 02 Bayesian Inference
parent_source: "[[Bayesian Filtering and Smoothing]]"
sources:
  - "[[Bayesian Filtering and Smoothing]]"
  - "[[raw/math_statistics/Simo Särkkä and Lennart Svensson, Bayesian Filtering and Smoothing.pdf]]"
---
# Bayesian Filtering and Smoothing - Ch 02 Bayesian Inference

## Ingest Scope and Depth

- Ingest stage: `scan`
- Pass 1: full chapter scan completed.
- Pass 2: no standalone theorem-level deepening applied because the chapter is mostly a compressed prerequisite refresher.

## Role of the chapter

This chapter aligns the notation and computational philosophy of the rest of the book. It compresses prior, likelihood, posterior, point estimation, and numerical Bayes computation into the notation later chapters use for filtering, smoothing, and parameter estimation.

## Section map

- philosophy of Bayesian inference
- connection to maximum likelihood estimation
- building blocks of Bayesian models
- Bayesian point estimates
- numerical methods

## Main contributions from the scan pass

- The chapter makes the ML versus MAP distinction explicit before state-space estimation starts.
- It shows why point estimates such as MAP and MMSE are summaries of posterior structure rather than substitutes for it.
- It previews the numerical toolkit later reused in the book: Gaussian approximations, Monte Carlo methods, and MCMC.

## Why it remains scan-level

The vault already has broader probability and inference notes. This chapter matters mainly because it standardizes the notation and decision language that later state-space chapters rely on.

## Quant relevance

The main quant value is conceptual discipline:

- posterior uncertainty is not the same thing as one point estimate
- likelihood optimization and Bayesian estimation are related but not identical
- numerical approximation is part of the statistical method, not an implementation detail

## Promotion candidates

- [[Parameter Estimation in State Space Models]]

## Related notes

- [[Bayesian Filtering and Smoothing]]
- [[Maximum Likelihood Estimation]]
- [[Markov Chain Monte Carlo]]

## Sources

- [[Bayesian Filtering and Smoothing]]
- [[raw/math_statistics/Simo Särkkä and Lennart Svensson, Bayesian Filtering and Smoothing.pdf]]
