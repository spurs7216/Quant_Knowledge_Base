---
title: Linear Algebra for Data Science, Machine Learning, and Signal Processing - Ch 07 Low-Rank Approximation and Multidimensional Scaling
type: source
status: chapter_ingested
updated: 2026-04-20
tags:
  - source
  - linear-algebra
  - low-rank
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: chapter_text_sampling_plus_section_theorems
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 07 Low-Rank Approximation and Multidimensional Scaling
parent_source: "[[Linear Algebra for Data Science, Machine Learning, and Signal Processing]]"
sources:
  - "[[Linear Algebra for Data Science, Machine Learning, and Signal Processing]]"
  - "[[raw/math_statistics/Linear Algebra for Data Science, Machine Learning, and Signal Processing (2024).pdf]]"
---
# Linear Algebra for Data Science, Machine Learning, and Signal Processing - Ch 07 Low-Rank Approximation and Multidimensional Scaling

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: chapter scan completed from the full section map and chapter intro.
- Pass 2: theorem-level extraction completed for Eckart-Young-Mirsky, subspace approximation, unitarily invariant formulations, hard/soft thresholding, and rank-selection logic.

## Why this chapter is load-bearing

This is the representation/compression chapter of the book. It answers a core research question:

- if a large matrix is approximately low rank, what is the best low-rank approximation, and how should one shrink noisy singular directions?

That question appears everywhere in quant work:

- factor extraction
- noise suppression
- panel compression
- latent-state approximation
- missing-data recovery

## Core objects

- rank-constrained approximation `min_{rank(B) <= K} ||A - B||`
- truncated SVD `A_K`
- singular-value hard thresholding
- singular-value soft thresholding
- MDS as a low-rank geometry problem
- stable rank and rank selection criteria

## Structural map

- Frobenius-norm low-rank approximation
- Eckart-Young-Mirsky theorem
- subspace approximation viewpoint
- implementation and scree plots
- permutation-based rank choice
- multidimensional scaling
- proximal operators
- hard/soft thresholding
- SURE and OptShrink
- PCA / autoencoders / streaming extensions

## Theorem and derivation spine

### 1. Eckart-Young-Mirsky theorem

For `A = U Sigma V*`, the best rank-`K` approximation under Frobenius norm is:

`A_K = sum_{k=1}^K sigma_k u_k v_k*`

and the error is:

`||A - A_K||_F^2 = sum_{k>K} sigma_k^2`

This is the fundamental low-rank theorem of the chapter.

The proof strategy is important:

- the truncated SVD clearly achieves the displayed error
- any other rank-`K` matrix must miss at least the discarded singular-value mass
- Weyl-type singular-value inequalities give the lower bound

So the theorem is not just a computational recipe; it is an optimality statement.

### 2. Low-rank approximation is subspace approximation

If data columns are stacked in `X`, then the rank-`K` approximation says each data point is represented inside the `K`-dimensional left singular subspace `R(U_K)`.

That is the real geometric meaning:

- approximate the cloud of points by a low-dimensional linear subspace

This is why the chapter naturally connects to PCA and subspace learning.

### 3. The theorem extends beyond Frobenius norm

The chapter states the stronger Eckart-Young-Mirsky result:

- for any unitarily invariant norm, the same truncated-SVD solution is optimal

That matters conceptually because it says the SVD is not merely Frobenius-specific. It is structurally aligned with the whole family of unitary-invariant matrix geometries.

### 4. Hard vs soft thresholding are different model choices

The rank-penalized formulation yields singular-value hard thresholding:

- keep singular values above a threshold
- set the rest to zero

The nuclear-norm relaxation yields singular-value soft thresholding:

- shrink every singular value toward zero by `beta`
- kill any singular value below the threshold

This difference is crucial:

- hard thresholding is discrete model selection
- soft thresholding is continuous shrinkage

### 5. Rank selection is the real difficulty

Once the SVD is known, truncation is easy. Choosing `K` is not.

The chapter's practical tools:

- scree plots
- permutation baselines
- SURE
- OptShrink

all address the same problem: distinguish latent signal singular directions from noise singular directions.

## What to preserve conceptually

- low-rank approximation is optimal projection in matrix space
- truncation is projection; shrinkage is regularization
- singular values are the currency of model complexity
- the approximation rank is a statistical choice, not a purely algebraic one

## Quant relevance

This chapter directly supports:

- factor compression of return panels
- denoising large covariance-like objects
- latent-structure extraction from noisy cross sections
- recommender-style and missing-data problems
- streaming low-rank updates

## Promotion candidates

- [[Low-Rank Approximation]]
- rank selection and singular-value shrinkage
- multidimensional scaling

## Related notes

- [[Linear Algebra for Data Science, Machine Learning, and Signal Processing]]
- [[Singular Value Decomposition]]
- [[Least Squares and Pseudoinverse]]

## Sources

- [[Linear Algebra for Data Science, Machine Learning, and Signal Processing]]
- [[raw/math_statistics/Linear Algebra for Data Science, Machine Learning, and Signal Processing (2024).pdf]]
