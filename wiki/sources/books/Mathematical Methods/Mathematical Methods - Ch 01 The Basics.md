---
title: Mathematical Methods - Ch 01 The Basics
type: source
status: chapter_ingested
updated: 2026-04-20
tags:
  - source
  - mathematics
  - probability
  - linear-algebra
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: full_chapter
extraction_basis: chapter_markdown_conversion_plus_contents_check
technical_depth: scan
ingest_stage: scan
chapter_or_section: Ch 01 The Basics
parent_source: "[[Mathematical Methods]]"
sources:
  - "[[Mathematical Methods]]"
  - "[[raw/math_statistics/Mathematical Methods.pdf]]"
---
# Mathematical Methods - Ch 01 The Basics

## Ingest Scope and Depth

- Ingest stage: `scan`
- Pass 1: full chapter scan completed.
- Pass 2: no full theorem-by-theorem rewrite was done because the chapter mostly reviews material already covered by stronger direct shelf sources.

## Why this chapter is here

This chapter is the shared language layer for the rest of the book. It gives the algebraic and probabilistic primitives that Chapter 2 uses for graph spectra and Markov processes, Chapter 3 uses for regression, kernels, and PCA, and Chapter 4 uses for linear-algebraic homology.

## Core objects

- image `Im(A)` and kernel `ker(A)`
- orthogonal complements and four-subspace decomposition
- pseudoinverse `A^dagger`
- singular value decomposition
- probability space, random variable, conditional probability, and density
- expectation, covariance, and conditional expectation
- Gaussian and multivariate Gaussian distributions

## Structural map

- linear algebra from four subspaces to least-squares geometry
- pseudoinverse and minimum-norm projection logic
- spectral theorem and SVD
- probability spaces, Bayes rule, and densities
- expectation, covariance, conditioning, and Gaussian transformations

## Load-bearing results kept from the scan

### 1. Four-subspace geometry organizes linear inverse problems

Theorem 1.4 gives the orthogonal-complement relations between `Im(A)`, `Im(A^T)`, `ker(A)`, and `ker(A^T)`. That is the geometric basis for least-squares projection and minimum-norm solutions.

### 2. The pseudoinverse is the least-squares bridge

Definition 1.6 and Proposition 1.8 treat `A^dagger` as the map that projects onto the column space and then returns the minimum-norm solution. This is the algebra later used for linear regression in Chapter 3.

### 3. SVD compresses operator structure into singular directions

Theorem 1.10 and Lemma 1.11 give the compact SVD and the relation between SVD and pseudoinverse. That becomes the background for PCA and low-rank structure later in the book.

### 4. Bayes and Gaussian identities are the reusable probability core

The probability section builds from conditional probability and Bayes' theorem up to conditional densities, covariance identities, and affine transforms of Gaussian vectors.

## Quant relevance

- least-squares and pseudoinverse logic recur in regression, state-space estimation, and factor extraction
- SVD is the computational backbone for dimensionality reduction and denoising
- Bayes and Gaussian rules feed directly into Bayesian regression and latent-variable PCA later in Chapter 3
- the Poisson rare-event exercise is a useful hint that the book's probability language can connect back to process modeling

## Promotion candidates

- none from this chapter as a first durable batch because the strongest reusable material is already better covered elsewhere in the shelf

## Related notes

- [[Mathematical Methods]]
- [[Least Squares and Pseudoinverse]]
- [[Singular Value Decomposition]]
- [[Low-Rank Approximation]]
- [[Maximum Likelihood Estimation]]
- [[Probabilistic Machine Learning]]

## Sources

- [[Mathematical Methods]]
- [[raw/math_statistics/Mathematical Methods.pdf]]
