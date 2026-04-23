---
title: Low-Rank Approximation
type: method
status: seed
updated: 2026-04-20
tags:
  - method
  - linear-algebra
  - low-rank
domain: mathematics
sources:
  - "[[Linear Algebra for Data Science, Machine Learning, and Signal Processing]]"
  - "[[Linear Algebra for Data Science, Machine Learning, and Signal Processing - Ch 07 Low-Rank Approximation and Multidimensional Scaling]]"
---
# Low-Rank Approximation

## Summary

Low-rank approximation replaces a large matrix by a matrix with fewer effective degrees of freedom while preserving the dominant singular structure.

The canonical problem is:

`A_K = arg min_{rank(B) <= K} ||A - B||`

and for Frobenius norm or any unitarily invariant norm, the solution is the truncated SVD.

## Core result

If `A = U Sigma V*`, then:

`A_K = sum_{k=1}^K sigma_k u_k v_k*`

and under Frobenius norm:

`||A - A_K||_F^2 = sum_{k>K} sigma_k^2`

This is the Eckart-Young-Mirsky theorem.

## Interpretation

Low-rank approximation is simultaneously:

- matrix compression
- subspace approximation
- denoising
- model-complexity control

The singular values decide which directions are kept and which are discarded.

## Variants

- hard thresholding: keep singular values above a cutoff
- soft thresholding: shrink singular values continuously
- factorization approaches: optimize over low-rank factors directly

## Main difficulty

The algebraic solution is easy once `K` is known. Choosing `K` is the statistical problem. Useful tools include scree plots, permutation baselines, SURE, and related singular-value shrinkage methods.

## Quant relevance

This method is important for:

- latent-factor extraction
- panel denoising
- covariance compression
- missing-data reconstruction
- regime/state representation

## Related notes

- [[Singular Value Decomposition]]
- [[Least Squares and Pseudoinverse]]

## Sources

- [[Linear Algebra for Data Science, Machine Learning, and Signal Processing]]
- [[Linear Algebra for Data Science, Machine Learning, and Signal Processing - Ch 07 Low-Rank Approximation and Multidimensional Scaling]]
