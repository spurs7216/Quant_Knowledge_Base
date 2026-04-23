---
title: Linear Algebra for Data Science, Machine Learning, and Signal Processing - Ch 09 Optimization Basics and Logistic Regression
type: source
status: chapter_ingested
updated: 2026-04-20
tags:
  - source
  - linear-algebra
  - optimization
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: chapter_text_sampling_plus_section_theorems
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 09 Optimization Basics and Logistic Regression
parent_source: "[[Linear Algebra for Data Science, Machine Learning, and Signal Processing]]"
sources:
  - "[[Linear Algebra for Data Science, Machine Learning, and Signal Processing]]"
  - "[[raw/math_statistics/Linear Algebra for Data Science, Machine Learning, and Signal Processing (2024).pdf]]"
---
# Linear Algebra for Data Science, Machine Learning, and Signal Processing - Ch 09 Optimization Basics and Logistic Regression

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: chapter scan completed from the full section map and chapter intro.
- Pass 2: theorem-level extraction completed for preconditioned GD on least squares, Lipschitz-gradient convex GD theory, accelerated methods, logistic-regression gradients, and SGD.

## Why this chapter is load-bearing

This chapter answers the next obvious question after Chapters 5 and 7:

- what do we do when the closed-form solution is unavailable or too expensive?

Its answer is gradient-based optimization, but crucially the chapter interprets convergence through linear algebra rather than treating optimization as a separate black box.

## Core objects

- least-squares objective `f(x) = (1/2) ||Ax - y||_2^2`
- preconditioned GD iteration `x_{k+1} = x_k - P grad f(x_k)`
- transformed error dynamics
- Lipschitz gradient constant `L`
- convexity through Hessian PSD
- Nesterov FGM, OGM
- logistic-regression cost and gradient
- SGD

## Structural map

- preconditioned GD for LS
- matrix square root
- convergence-rate analysis
- ideal and diagonal preconditioners
- smooth convex GD
- Nesterov and optimized gradient methods
- gradient projection
- logistic regression
- stochastic gradient descent

## Theorem and derivation spine

### 1. Least-squares GD is a spectral problem

For `f(x) = (1/2) ||Ax - y||_2^2`,

- `grad f(x) = A* (Ax - y)`

and preconditioned GD uses:

`x_{k+1} = x_k - P A* (Ax_k - y)`

The chapter's main algebraic move is to transform the error by `P^{-1/2}` so that convergence is controlled by a single matrix:

`G = I - P^{1/2} A* A P^{1/2}`

Convergence is then a spectral-radius question.

### 2. Classical GD step-size rule

With `P = alpha I`, convergence requires:

`0 < alpha < 2 / ||A||_2^2 = 2 / sigma_1(A)^2`

The best fixed step size for asymptotic convergence is:

`alpha* = 2 / (sigma_1(A)^2 + sigma_N(A)^2)`

This is an important result because it shows directly how conditioning governs GD speed.

### 3. Ideal preconditioning

The ideal preconditioner is:

`P_ideal = (A* A)^{-1}`

which yields one-step convergence in the full-rank least-squares case. This is more than a curiosity: it explains what preconditioning is trying to imitate. A practical preconditioner is good to the extent that it approximates `A* A` while staying cheap to apply.

### 4. Diagonal majorization gives a cheap practical preconditioner

The chapter uses a diagonal majorizer of `A* A` to build a usable preconditioner:

- replace the full curvature with an easily invertible diagonal upper bound

This is a strong practical idea because it converts a hard inverse into scaled coordinate normalization.

### 5. Smooth convex GD theory

The chapter then generalizes from least squares to smooth convex functions:

- if `grad f` is `L`-Lipschitz
- and `0 < alpha < 2 / L`

then GD converges, with cost decrease on the order of `O(1/k)`.

The book's route to this result is through:

- Lipschitz continuity of the gradient
- Hessian PSD / bounded curvature
- monotonic descent and worst-case bounds

### 6. Acceleration

Nesterov FGM improves the cost bound to `O(1/k^2)`, and OGM improves the constant further. The real lesson is not memorizing the recursion. The lesson is:

- momentum exploits curvature information more efficiently than fixed-step GD

### 7. Logistic regression is where linear algebra meets classification optimization

The logistic-loss objective is:

`f(x) = (1/M) sum_m log(1 + exp(-a_m* x)) + beta ||x||_2^2 / 2`

with gradient:

`grad f(x) = A* h'(Ax) + beta x`

The chapter's point is that once the loss is smooth and convex, the earlier gradient machinery applies almost unchanged.

### 8. SGD changes the gradient oracle, not the basic logic

SGD replaces the full gradient with a minibatch approximation. The objective may no longer decrease monotonically, but the update is still gradient-driven. This is the bridge from exact first-order methods to practical large-scale training.

## What to preserve conceptually

- least-squares GD is governed by the spectrum of `A* A`
- preconditioning is curvature normalization
- Lipschitz gradients convert local smoothness into global step-size guarantees
- acceleration changes convergence rate class
- logistic regression is a smooth convex optimization problem before it is an ML buzzword

## Quant relevance

This chapter matters directly for:

- large-scale regression where normal equations are too costly
- penalized models
- classification pipelines
- online/streaming optimization
- feature scaling and convergence tuning

## Promotion candidates

- [[Gradient Descent and Preconditioning]]
- logistic regression as smooth convex ERM

## Related notes

- [[Linear Algebra for Data Science, Machine Learning, and Signal Processing]]
- [[Least Squares and Pseudoinverse]]
- [[Low-Rank Approximation]]

## Sources

- [[Linear Algebra for Data Science, Machine Learning, and Signal Processing]]
- [[raw/math_statistics/Linear Algebra for Data Science, Machine Learning, and Signal Processing (2024).pdf]]
