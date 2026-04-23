---
title: Singular Value Decomposition
type: concept
status: seed
updated: 2026-04-20
tags:
  - concept
  - linear-algebra
  - matrix-factorization
domain: mathematics
sources:
  - "[[Linear Algebra for Data Science, Machine Learning, and Signal Processing]]"
  - "[[Linear Algebra for Data Science, Machine Learning, and Signal Processing - Ch 03 Matrix Factorization Eigendecomposition and SVD]]"
  - "[[Linear Algebra for Data Science, Machine Learning, and Signal Processing - Ch 05 Linear Least-Squares Regression and Binary Classification]]"
  - "[[Linear Algebra for Data Science, Machine Learning, and Signal Processing - Ch 07 Low-Rank Approximation and Multidimensional Scaling]]"
---
# Singular Value Decomposition

## Summary

The SVD is the canonical factorization of a matrix into left geometry, scale, and right geometry:

`A = U Sigma V*`

It exists for every matrix, square or rectangular, and is therefore the most robust matrix factorization in the vault's core toolkit.

## Core objects

- left singular vectors `u_k`
- right singular vectors `v_k`
- singular values `sigma_k >= 0`
- compact SVD using only nonzero singular directions

Equivalent rank-one expansion:

`A = sum_k sigma_k u_k v_k*`

## Why it matters

The SVD is the language behind:

- least-squares solutions
- pseudoinverse
- conditioning
- low-rank approximation
- PCA-like compression
- spectral denoising

If eigendecomposition is the natural factorization for Hermitian matrices, the SVD is the natural factorization for everything else.

## Geometry

The SVD says that a linear operator acts in three stages:

1. rotate into a right singular basis with `V*`
2. scale along orthogonal axes with `Sigma`
3. rotate into the output basis with `U`

That is why the SVD maps spheres to ellipsoids and why singular values are directional amplification factors.

## Key facts

- `sigma_1(A) = ||A||_2`
- `sigma_min(A)` controls near-singularity
- `A* A` and `A A*` are PSD and encode the singular spectrum
- the compact SVD isolates the range and nullspace geometry cleanly

## Failure modes and caveats

- small singular values make inversion unstable
- singular vectors are not unique when singular values are repeated
- truncation decisions are modeling choices, not purely algebraic facts

## Quant relevance

The SVD appears everywhere in quantitative research:

- noisy factor extraction
- rank-reduced signals
- regularized regression
- matrix completion
- covariance stabilization

## Related notes

- [[Least Squares and Pseudoinverse]]
- [[Low-Rank Approximation]]
- [[Gradient Descent and Preconditioning]]

## Sources

- [[Linear Algebra for Data Science, Machine Learning, and Signal Processing]]
- [[Linear Algebra for Data Science, Machine Learning, and Signal Processing - Ch 03 Matrix Factorization Eigendecomposition and SVD]]
- [[Linear Algebra for Data Science, Machine Learning, and Signal Processing - Ch 05 Linear Least-Squares Regression and Binary Classification]]
- [[Linear Algebra for Data Science, Machine Learning, and Signal Processing - Ch 07 Low-Rank Approximation and Multidimensional Scaling]]
