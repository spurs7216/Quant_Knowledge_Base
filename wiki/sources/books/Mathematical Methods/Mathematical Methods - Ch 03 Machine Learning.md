---
title: Mathematical Methods - Ch 03 Machine Learning
type: source
status: chapter_ingested
updated: 2026-04-20
tags:
  - source
  - machine-learning
  - statistics
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: chapter_markdown_conversion_plus_selected_definition_and_theorem_checks
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 03 Machine Learning
parent_source: "[[Mathematical Methods]]"
sources:
  - "[[Mathematical Methods]]"
  - "[[raw/math_statistics/Mathematical Methods.pdf]]"
---
# Mathematical Methods - Ch 03 Machine Learning

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: deeper extraction completed for the learning setup, linear and Bayesian regression, support vector machines, kernelization, and PCA.

## Why this chapter is load-bearing

This chapter is the main reason the book belongs on the shelf as a book rather than a bridge note. It gives one compact mathematical route from supervised learning setup to regularized regression, Bayesian regression, SVMs, kernels, dimensionality reduction, and latent Gaussian modeling.

## Core objects

- deterministic model versus statistical model
- empirical risk, likelihood, posterior, and validation split
- feature matrix `Omega`
- regularization parameter `lambda`
- neural-network layers and activation functions
- separating hyperplane, margin, slack variables `xi_k`, and dual weights `alpha_k`
- kernel map `kappa`
- covariance matrix `Sigma`, eigensystem, principal components, and projection subspace `U`
- latent Gaussian variable `zeta` and generative PCA model

## Structural map

- data, models, learning, and validation
- regression and Bayesian regression
- nonlinear regression and neural networks
- support vector machines and the dual/kernel form
- principal component analysis and its statistical extension

## Theorem and derivation spine

### 1. The chapter makes the learning problem explicit before solving any one model

Definitions 3.4 to 3.6 separate deterministic ERM from statistical MLE and MAP. This is important because later sections are not just a list of algorithms. They are all instances of the same modeling template: choose a model class, define loss or likelihood, fit parameters, then validate.

### 2. Linear regression, ridge regression, and Gaussian likelihood line up algebraically

Theorems 3.8, 3.11, and 3.12 show the standard chain:

- least squares gives the pseudoinverse solution
- ridge regularization stabilizes the problem and adds a shrinkage term
- Gaussian-noise MLE leads back to the same algebra as least squares

This is the first major place where Chapter 1's pseudoinverse machinery is reused.

### 3. Bayesian regression turns regularization into prior structure

Theorems 3.15 and 3.17 interpret Gaussian priors as MAP shrinkage and give a posterior Gaussian law for the parameter. Proposition 3.18 then gives the predictive distribution. The durable point is that Bayesian regression is not a different geometric object from regularized regression. It is the same object with probabilistic interpretation layered on top.

### 4. SVMs are margin optimization plus kernelization

The SVM section builds cleanly:

- Lemmas 3.22 and 3.23 connect the sign rule to geometric margin
- Definitions 3.24 and 3.25 give hard- and soft-margin formulations
- Definition 3.27 gives the dual problem
- Proposition 3.29 reconstructs the separating hyperplane from the dual solution
- Lemma 3.31 and Algorithm 3.2 show how the kernel trick replaces explicit feature expansion

This is the strongest reusable classification block in the chapter.

### 5. PCA is both a variance-maximization problem and a reconstruction problem

Theorems 3.39 and 3.41 prove the two classic PCA characterizations:

- maximize explained variance along a `d`-dimensional subspace
- equivalently minimize squared reconstruction error

The later kernel and latent-Gaussian parts show two extensions:

- kernel PCA uses only kernel evaluations through `W^T W`
- the latent Gaussian model interprets PCA as a generative model with posterior inference for the latent variable

## Quant relevance

This chapter is directly relevant to:

- cross-sectional or event classification via SVM-style margins
- regularized forecasting and signal estimation
- latent-factor extraction and dimensionality reduction
- nonlinear feature expansion through kernels
- generative latent-state representations for noisy data

## Promotion candidates

- [[Support Vector Machines]]
- [[Principal Component Analysis]]
- Bayesian regression
- kernel methods

## Related notes

- [[Mathematical Methods]]
- [[Support Vector Machines]]
- [[Principal Component Analysis]]
- [[Least Squares and Pseudoinverse]]
- [[Low-Rank Approximation]]
- [[Probabilistic Machine Learning]]
- [[Gradient Descent and Preconditioning]]

## Sources

- [[Mathematical Methods]]
- [[raw/math_statistics/Mathematical Methods.pdf]]
