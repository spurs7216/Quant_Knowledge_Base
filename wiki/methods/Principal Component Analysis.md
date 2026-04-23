---
title: Principal Component Analysis
type: method
status: seed
updated: 2026-04-20
tags:
  - method
  - machine-learning
  - dimensionality-reduction
  - linear-algebra
domain: mathematics
sources:
  - "[[Mathematical Methods]]"
  - "[[Mathematical Methods - Ch 03 Machine Learning]]"
  - "[[Linear Algebra for Data Science, Machine Learning, and Signal Processing]]"
  - "[[Low-Rank Approximation]]"
---
# Principal Component Analysis

## Summary

Principal component analysis finds a low-dimensional subspace that captures as much variation in the data as possible, or equivalently minimizes squared reconstruction error after projection. It is one of the main bridges from covariance structure to dimensionality reduction.

## What It Does

PCA helps the researcher:

- compress high-dimensional data into a smaller set of directions
- expose dominant covariance structure
- denoise data by discarding low-variance directions
- build latent representations for visualization, factor extraction, or downstream modeling

## Source Synthesis

- [[Mathematical Methods - Ch 03 Machine Learning]] ties together the variance-maximization view, the reconstruction-error view, kernel PCA, and a latent Gaussian interpretation.
- [[Linear Algebra for Data Science, Machine Learning, and Signal Processing]] and [[Low-Rank Approximation]] provide the SVD and low-rank backbone that makes PCA computationally and geometrically transparent.

## Assumptions

PCA is most useful when:

- the data have a meaningful low-dimensional linear structure after centering
- large variance is at least a reasonable proxy for important structure
- scale differences across variables are handled deliberately
- the user is willing to accept orthogonal factors even when the true latent structure may not be orthogonal

## Workflow

1. Center the data and decide whether to standardize features.
2. Compute the covariance matrix or directly use an SVD of the centered data matrix.
3. Inspect eigenvalues or singular values and choose a working dimension `d`.
4. Project the data onto the leading principal directions.
5. Interpret loadings, reconstruction quality, and downstream usefulness.
6. Escalate to kernel PCA only when linear PCA clearly misses the geometry.

## Diagnostics

- scree plot or eigengap inspection
- variance explained versus reconstruction error
- stability of principal directions across nearby samples
- whether the leading components correspond to signal, scale artifacts, or one-off outliers
- sensitivity to centering and standardization choices

## Failure Modes

- assuming high variance automatically means useful signal
- skipping centering or mishandling scaling
- treating component signs or ordering as economically stable facts
- using static principal directions in strongly regime-dependent data without re-estimation
- confusing PCA with causal or structural factor discovery

## Quant Use Cases

- latent factor extraction
- yield-curve or volatility-surface compression
- covariance denoising
- feature compression before forecasting or classification
- exploratory geometry of alternative-data panels

## Related Notes

- [[Low-Rank Approximation]]
- [[Singular Value Decomposition]]
- [[Support Vector Machines]]
- [[Mathematical Methods]]
- [[Mathematical Methods - Ch 03 Machine Learning]]

## Sources

- [[Mathematical Methods]]
- [[Mathematical Methods - Ch 03 Machine Learning]]
- [[Linear Algebra for Data Science, Machine Learning, and Signal Processing]]
- [[Low-Rank Approximation]]
