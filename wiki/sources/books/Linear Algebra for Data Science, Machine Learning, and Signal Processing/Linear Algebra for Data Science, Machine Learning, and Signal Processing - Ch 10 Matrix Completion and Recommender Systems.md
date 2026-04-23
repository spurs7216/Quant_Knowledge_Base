---
title: Linear Algebra for Data Science, Machine Learning, and Signal Processing - Ch 10 Matrix Completion and Recommender Systems
type: source
status: chapter_ingested
updated: 2026-04-20
tags:
  - source
  - linear-algebra
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: chapter_scan
extraction_basis: chapter_opening_pages_plus_section_map
technical_depth: moderate
ingest_stage: selective_deepen
chapter_or_section: Ch 10 Matrix Completion and Recommender Systems
parent_source: "[[Linear Algebra for Data Science, Machine Learning, and Signal Processing]]"
sources:
  - "[[Linear Algebra for Data Science, Machine Learning, and Signal Processing]]"
  - "[[raw/math_statistics/Linear Algebra for Data Science, Machine Learning, and Signal Processing (2024).pdf]]"
---
# Linear Algebra for Data Science, Machine Learning, and Signal Processing - Ch 10 Matrix Completion and Recommender Systems

## Ingest Scope and Depth

- Ingest stage: `selective_deepen`
- Pass 1: chapter scan completed from the section map and chapter opening pages.
- Pass 2: local attention applied to the sampling-mask formulation, alternating projections, and noisy low-rank matrix completion variants.

## Role of the chapter

This chapter takes the low-rank tools of Chapter 7 and puts them into the partial-observation setting:

- only some entries are observed
- the latent matrix is assumed low rank
- reconstruction becomes a constrained inverse problem

## Section map

- measurement model
- noiseless LRMC
- alternating projection
- noisy LRMC
- MM methods
- iterative hard / soft singular-value thresholding
- debiasing
- factorization approaches
- robust PCA
- nonnegative matrix factorization

## What the chapter is really doing

### 1. It separates observation from latent structure

The sampling mask is the key formal object. Missingness is not represented by "blank entries" conceptually; it is represented by a masking operator that keeps track of what the data constraints actually are.

### 2. It rewrites completion as intersection of two sets

In the noiseless case:

- one set enforces data consistency
- one set enforces low rank

Alternating projections then becomes a natural computational baseline.

### 3. It connects matrix completion to the low-rank shrinkage toolkit

The noisy methods reintroduce:

- iterative low-rank approximation
- singular-value hard and soft thresholding
- factorization-based optimization

So the chapter is best viewed as a structured application of Chapters 7 and 9.

## Worth attending

- sampling-mask formulation
- alternating projection between data-consistency and low-rank sets
- noisy LRMC via singular-value thresholding
- robust PCA and NMF as nearby variants

## Quant relevance

This chapter matters whenever quant data are:

- sparse
- asynchronous
- partially missing
- naturally low rank after demeaning or factor extraction

## Promotion candidates

- matrix completion under partial observation

## Related notes

- [[Linear Algebra for Data Science, Machine Learning, and Signal Processing]]
- [[Low-Rank Approximation]]

## Sources

- [[Linear Algebra for Data Science, Machine Learning, and Signal Processing]]
- [[raw/math_statistics/Linear Algebra for Data Science, Machine Learning, and Signal Processing (2024).pdf]]
