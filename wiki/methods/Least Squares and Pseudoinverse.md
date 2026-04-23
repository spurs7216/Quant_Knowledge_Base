---
title: Least Squares and Pseudoinverse
type: method
status: seed
updated: 2026-04-20
tags:
  - method
  - linear-algebra
  - regression
domain: mathematics
sources:
  - "[[Linear Algebra for Data Science, Machine Learning, and Signal Processing]]"
  - "[[Linear Algebra for Data Science, Machine Learning, and Signal Processing - Ch 05 Linear Least-Squares Regression and Binary Classification]]"
---
# Least Squares and Pseudoinverse

## Summary

Least squares solves the projection problem:

`x-hat = arg min_x ||Ax - y||_2^2`

The Moore-Penrose pseudoinverse gives the canonical minimum-norm solution:

`x-hat = A^+ y`

## Core logic

The gradient of the LS objective is:

`grad f(x) = A* (Ax - y)`

Setting this to zero yields the normal equations:

`A* A x = A* y`

Geometrically, the fitted residual is orthogonal to the range of `A`.

## SVD form

If `A = U_r Sigma_r V_r*`, then:

`A^+ = V_r Sigma_r^{-1} U_r*`

and the full least-squares solution set is:

`x = A^+ y + x_N`, with `x_N in N(A)`

The pseudoinverse chooses the unique solution with minimum Euclidean norm.

## Why it matters

This method is the baseline for:

- regression
- linear inverse problems
- classification by least-squares fitting
- recursive updating

It is also the cleanest way to see where instability comes from: dividing by small singular values.

## Regularized variants

- truncated SVD deletes unstable small-singular directions
- ridge / Tikhonov replaces `1 / sigma_k` with `sigma_k / (sigma_k^2 + beta)`

So regularization is most transparent in singular-value coordinates.

## Failure modes

- collinearity or near-collinearity
- tiny singular values
- assuming uniqueness when nullspace directions remain
- treating numerical solvability as statistical validity

## Quant relevance

Least squares is the default linear estimator across cross-sectional models, time-series filtering steps, factor work, and many portfolio/risk approximations. The pseudoinverse viewpoint is especially useful when panels are rank-deficient or nearly redundant.

## Related notes

- [[Singular Value Decomposition]]
- [[Low-Rank Approximation]]
- [[Gradient Descent and Preconditioning]]

## Sources

- [[Linear Algebra for Data Science, Machine Learning, and Signal Processing]]
- [[Linear Algebra for Data Science, Machine Learning, and Signal Processing - Ch 05 Linear Least-Squares Regression and Binary Classification]]
