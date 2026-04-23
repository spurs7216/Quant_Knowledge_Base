---
title: Linear Algebra for Data Science, Machine Learning, and Signal Processing - Ch 05 Linear Least-Squares Regression and Binary Classification
type: source
status: chapter_ingested
updated: 2026-04-20
tags:
  - source
  - linear-algebra
  - least-squares
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: chapter_text_sampling_plus_section_theorems
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 05 Linear Least-Squares Regression and Binary Classification
parent_source: "[[Linear Algebra for Data Science, Machine Learning, and Signal Processing]]"
sources:
  - "[[Linear Algebra for Data Science, Machine Learning, and Signal Processing]]"
  - "[[raw/math_statistics/Linear Algebra for Data Science, Machine Learning, and Signal Processing (2024).pdf]]"
---
# Linear Algebra for Data Science, Machine Learning, and Signal Processing - Ch 05 Linear Least-Squares Regression and Binary Classification

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: chapter scan completed from the section map and chapter intro.
- Pass 2: theorem-level extraction completed for existence/uniqueness, normal equations, compact-SVD solution, pseudoinverse, minimum-norm LS, truncated SVD, and Tikhonov regularization.

## Why this chapter is load-bearing

This chapter is where the SVD becomes an estimator. The core question is no longer "what is a singular value?" but "what does the singular structure of `A` imply about solvability, uniqueness, instability, and regularization?"

That is the central quant-research question for linear models.

## Core objects

- linear system `Ax = y`
- least-squares objective `f(x) = (1/2) ||Ax - y||_2^2`
- normal equations `A* A x = A* y`
- compact SVD `A = U_r Sigma_r V_r*`
- pseudoinverse `A^+ = V_r Sigma_r^{-1} U_r*`
- condition number
- truncated-SVD and ridge/Tikhonov estimators

## Structural map

- solvability of `Ax = y`
- least-squares formulation
- gradient and normal equations
- compact-SVD solution
- pseudoinverse
- underdetermined case and minimum-norm LS
- truncated SVD
- Tikhonov / ridge regularization
- frames
- projection and least-squares classification
- recursive least squares

## Theorem and derivation spine

### 1. Exact linear systems: existence and uniqueness

The chapter starts with the basic facts:

- a solution exists iff `y in R(A)`
- a solution is unique iff `N(A) = {0}`
- unique solvability for all `y` requires square invertible `A`

These statements are elementary but they matter because the least-squares problem is what remains when one or both conditions fail.

### 2. Least squares is the projection problem behind regression

The estimator solves:

`x-hat = arg min_x (1/2) ||Ax - y||_2^2`

The gradient calculation is the first crucial derivation:

- expand the quadratic
- differentiate
- obtain `grad f(x) = A* (Ax - y)`

Setting the gradient to zero yields the normal equations:

`A* A x = A* y`

This is the algebraic heart of least squares.

### 3. The compact SVD exposes the whole solution set

Using `A = U_r Sigma_r V_r*`, the problem reduces to:

`min_x ||Sigma_r V_r* x - U_r* y||_2^2`

The clean minimizer family is:

`x = V_r Sigma_r^{-1} U_r* y + V_0 z_0`

where `V_0` spans the nullspace.

This immediately separates:

- the determined part that the data identifies
- the nullspace part that the data cannot identify

### 4. The pseudoinverse is the canonical minimum-norm solution

Definition:

`A^+ = V_r Sigma_r^{-1} U_r*`

Then the minimum-norm least-squares solution is:

`x-hat = A^+ y`

This is one of the main structural results of the chapter:

- if full column rank holds, this is the unique LS solution
- if not, this is the unique LS solution with smallest Euclidean norm

### 5. Orthogonality principle

Any least-squares residual `r = y - A x-hat` satisfies:

`A* r = 0`

equivalently, `r` is orthogonal to `R(A)`.

This is the geometric meaning of least squares: project `y` onto the range of `A`, and take the residual in the orthogonal complement.

### 6. Conditioning explains instability

The pseudoinverse solution expands coefficients by `1 / sigma_k`. Small singular values therefore amplify noise and model error. This is the real source of numerical and statistical fragility in ill-conditioned regression problems.

### 7. Truncated SVD and Tikhonov are two different stabilizations

Truncated SVD keeps only singular directions above a tolerance:

`x-hat_K = sum_{k=1}^K (1 / sigma_k) v_k (u_k* y)`

Ridge / Tikhonov instead shrinks continuously:

`x-hat_beta = (A* A + beta I)^{-1} A* y`

and in the SVD basis:

`x-hat_beta = sum_k (sigma_k / (sigma_k^2 + beta)) v_k (u_k* y)`

This makes the bias-variance tradeoff explicit in singular-value coordinates.

## What to preserve conceptually

- least squares is projection onto `R(A)`
- nullspace directions are not identified by the data
- pseudoinverse is the canonical solution because it deletes arbitrary nullspace energy
- ill-conditioning is singular-value geometry, not just a numerical nuisance
- regularization modifies the singular filter, not just the optimizer

## Quant relevance

This chapter is directly relevant to:

- cross-sectional and time-series regression
- factor-model estimation
- regularized alpha models
- signal extraction under multicollinearity
- online updating via RLS

It also explains why naive inversion is dangerous in research pipelines with noisy or nearly redundant signals.

## Promotion candidates

- [[Least Squares and Pseudoinverse]]
- ridge / Tikhonov regularization
- recursive least squares

## Related notes

- [[Linear Algebra for Data Science, Machine Learning, and Signal Processing]]
- [[Singular Value Decomposition]]
- [[Low-Rank Approximation]]
- [[Gradient Descent and Preconditioning]]

## Sources

- [[Linear Algebra for Data Science, Machine Learning, and Signal Processing]]
- [[raw/math_statistics/Linear Algebra for Data Science, Machine Learning, and Signal Processing (2024).pdf]]
