---
title: Linear Algebra for Data Science, Machine Learning, and Signal Processing - Ch 03 Matrix Factorization Eigendecomposition and SVD
type: source
status: chapter_ingested
updated: 2026-04-20
tags:
  - source
  - linear-algebra
  - matrix-factorization
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: chapter_text_sampling_plus_section_theorems
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 03 Matrix Factorization Eigendecomposition and SVD
parent_source: "[[Linear Algebra for Data Science, Machine Learning, and Signal Processing]]"
sources:
  - "[[Linear Algebra for Data Science, Machine Learning, and Signal Processing]]"
  - "[[raw/math_statistics/Linear Algebra for Data Science, Machine Learning, and Signal Processing (2024).pdf]]"
---
# Linear Algebra for Data Science, Machine Learning, and Signal Processing - Ch 03 Matrix Factorization Eigendecomposition and SVD

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: chapter scan completed from the full section map.
- Pass 2: theorem-level extraction completed for the spectral theorem, normal matrices, SVD existence/geometry, spectral norm characterization, and PSD structure.

## Why this chapter is load-bearing

This is the algebraic spine of the book. After this chapter, matrices stop being raw arrays and become decomposable operators with canonical directions and scales.

Everything later depends on this:

- least squares uses the SVD to expose solvability and instability
- low-rank approximation literally truncates the SVD
- optimization uses eigenvalue/singular-value bounds for step sizes and conditioning
- graph, Markov, and random-matrix chapters all reason through spectra

## Core objects

- eigendecomposition `A = V Lambda V^{-1}` when it exists
- unitary eigendecomposition `A = V Lambda V*` for normal matrices
- singular value decomposition `A = U Sigma V*`
- singular values `sigma_1 >= ... >= sigma_min(M,N) >= 0`
- spectral norm `||A||_2 = sigma_1`
- positive semidefinite matrices and Gram matrices `X*X`, `XX*`

## Structural map

- catalog of matrix factorizations
- spectral theorem for symmetric / Hermitian matrices
- normal matrices and diagonalizability
- singular value decomposition
- spectral norm as an optimization problem
- relation between SVD and eigendecomposition
- positive semidefinite matrices

## Theorem and derivation spine

### 1. Spectral theorem for symmetric / Hermitian matrices

For `A = A*`:

- all eigenvalues are real
- there exists an orthonormal basis of eigenvectors
- therefore `A = V Lambda V*` with `V` unitary and `Lambda` real diagonal

The chapter's proof idea for reality of eigenvalues is the standard one:

- if `Av = lambda v`
- then `v*Av = lambda v*v`
- but also `v*Av = (Av)*v = lambda-bar v*v`
- so `lambda = lambda-bar`

Orthogonality of eigenvectors with distinct eigenvalues follows from comparing `u*Av` and `v*Au`.

This theorem is the reason covariance, Gram, Hessian, and Laplacian-type matrices are so tractable.

### 2. Normal matrices are exactly the matrices with unitary diagonalization

Definition:

- `A` is normal iff `A*A = AA*`

Key statement:

- `A` is diagonalizable by a unitary matrix iff `A` is normal

This matters because the symmetric/Hermitian case is only one special case. Many structured matrices in signal processing and graph settings are normal without being symmetric.

### 3. SVD exists for every matrix

For any `X in F^{M x N}`, there exist unitary `U`, `V` and rectangular diagonal `Sigma` such that:

`X = U Sigma V* = sum_k sigma_k u_k v_k*`

This theorem is stronger operationally than eigendecomposition because:

- it always exists
- it applies to nonsquare matrices
- it separates left geometry, scale, and right geometry

The hidden proof idea is to diagonalize `X*X`:

- `X*X` is Hermitian PSD
- its eigenvalues are nonnegative
- take their square roots as singular values
- construct the left singular vectors from `u_k = X v_k / sigma_k`

### 4. Spectral norm as optimization

The matrix 2-norm is not just a definition; it has an extremal characterization:

- `||A||_2 = max_{||x||_2 = 1} ||Ax||_2 = sigma_1`

Equivalently:

- `||A||_2^2 = lambda_max(A*A)`

This turns the spectral norm into a Rayleigh-quotient problem on `A*A`. The smallest singular value plays the opposite role:

- `sigma_min(A) = min_{||x||_2 = 1} ||Ax||_2`

Those two extrema govern conditioning and numerical stability.

### 5. Positive semidefinite structure

The chapter ties PSD matrices to eigendecomposition:

- `A >= 0` iff its eigenvalues are nonnegative
- Gram matrices `X*X` and outer-product matrices `XX*` are always PSD

This is the bridge from arbitrary data matrices to spectral tools. Even if `X` is rectangular, the matrices `X*X` and `XX*` live in the spectral-theorem world.

## Geometry that matters

The chapter's 2D geometry is simple but important:

- `V*` rotates into a singular/eigen basis
- `Sigma` scales along orthogonal axes
- `U` rotates back out

That is the cleanest interpretation of why SVD maps spheres to ellipsoids and why singular values quantify directional amplification.

## What later chapters inherit from here

- Chapter 5 inherits the compact SVD as the clean language of least squares
- Chapter 7 inherits truncated SVD and singular-value shrinkage
- Chapter 9 inherits spectral norm and PSD reasoning for convergence bounds
- Chapter 12 inherits perturbation reasoning in terms of singular values

## Quant relevance

This chapter is central for quant work because it underlies:

- covariance eigensystems and PCA
- low-rank factor structure
- regularized regression and ill-conditioning diagnostics
- stable inversion and risk decomposition
- latent-signal extraction from noisy panels

Without this chapter, later quant methods become recipes instead of structured arguments.

## Promotion candidates

- [[Singular Value Decomposition]]
- spectral norm and conditioning
- positive semidefinite matrix geometry

## Related notes

- [[Linear Algebra for Data Science, Machine Learning, and Signal Processing]]
- [[Least Squares and Pseudoinverse]]
- [[Low-Rank Approximation]]
- [[Gradient Descent and Preconditioning]]

## Sources

- [[Linear Algebra for Data Science, Machine Learning, and Signal Processing]]
- [[raw/math_statistics/Linear Algebra for Data Science, Machine Learning, and Signal Processing (2024).pdf]]
