---
title: Linear Algebra for Data Science, Machine Learning, and Signal Processing
type: source
status: chapter_ingested
updated: 2026-04-20
tags:
  - source
  - linear-algebra
  - data-science
  - machine-learning
  - signal-processing
source_type: book
source_class: overview_source
read_scope: full_source
extraction_basis: preface_plus_table_of_contents_plus_selected_chapter_text
technical_depth: mixed
ingest_stage: promotion_started
source_count: 1
sources:
  - "[[raw/math_statistics/Linear Algebra for Data Science, Machine Learning, and Signal Processing (2024).pdf]]"
---
# Linear Algebra for Data Science, Machine Learning, and Signal Processing

## Citation / metadata

- Authors: Jeffrey A. Fessler and Raj Rao Nadakuditi
- Publisher: Cambridge University Press
- Year: 2024
- Role in vault: the matrix-methods bridge between basic probability/statistics and the algorithms that modern quant research actually implements

## Why this book matters

This is not a classical linear algebra book whose main purpose is solving `Ax = b` and proving abstract algebraic lemmas in isolation. The preface makes the design choice explicit: after a short foundation, the book teaches matrix methods in the language of data science, machine learning, and signal processing. That makes it unusually useful for this vault.

Its real contribution is not "teaching matrices again." Its contribution is showing how a small set of linear-algebraic objects keep reappearing inside:

- least squares and regularization
- low-rank structure and dimensionality reduction
- Markov chains and graph methods
- gradient methods and logistic regression
- matrix completion
- noise, perturbation, and phase-transition reasoning

For quant research, that is exactly the point where linear algebra stops being prerequisite material and becomes active research machinery.

## Reading logic from the source

The preface gives the correct dependency graph:

- Chapters 1 to 3 build the foundation and should be read in order.
- Chapters 4 to 12 branch from that foundation and can be revisited based on problem needs.

That structure matters for ingest. The book is not uniform in intellectual load. The shelf should therefore preserve the book's own hierarchy:

- scan all chapters
- deepen the chapters that actually carry the matrix machinery used repeatedly later
- promote the strongest reusable material into durable notes

## Stage map

Current ingest stages after the fresh reingest:

- `scan`: Chapters 1, 2, 11
- `deep`: Chapters 3, 5, 7, 9
- `selective_deepen`: Chapters 4, 6, 8, 10, 12

Selection logic:

- Chapter 3 is the algebraic spine: eigendecomposition, SVD, spectral norm, PSD structure.
- Chapter 5 is the estimation spine: least squares, pseudoinverse, minimum-norm and regularized solutions.
- Chapter 7 is the representation spine: low-rank approximation, truncation, shrinkage, and basis compression.
- Chapter 9 is the optimization spine: GD, preconditioning, acceleration, logistic regression, and SGD.

The other chapters still matter, but they are either preparatory, application-focused, or best treated as targeted revisits for later projects.

## Chapter shelf

- [[Linear Algebra for Data Science, Machine Learning, and Signal Processing - Ch 01 Getting Started]]
- [[Linear Algebra for Data Science, Machine Learning, and Signal Processing - Ch 02 Introduction to Matrices]]
- [[Linear Algebra for Data Science, Machine Learning, and Signal Processing - Ch 03 Matrix Factorization Eigendecomposition and SVD]]
- [[Linear Algebra for Data Science, Machine Learning, and Signal Processing - Ch 04 Subspaces Rank and Nearest-Subspace Classification]]
- [[Linear Algebra for Data Science, Machine Learning, and Signal Processing - Ch 05 Linear Least-Squares Regression and Binary Classification]]
- [[Linear Algebra for Data Science, Machine Learning, and Signal Processing - Ch 06 Norms and Procrustes Problems]]
- [[Linear Algebra for Data Science, Machine Learning, and Signal Processing - Ch 07 Low-Rank Approximation and Multidimensional Scaling]]
- [[Linear Algebra for Data Science, Machine Learning, and Signal Processing - Ch 08 Special Matrices Markov Chains and PageRank]]
- [[Linear Algebra for Data Science, Machine Learning, and Signal Processing - Ch 09 Optimization Basics and Logistic Regression]]
- [[Linear Algebra for Data Science, Machine Learning, and Signal Processing - Ch 10 Matrix Completion and Recommender Systems]]
- [[Linear Algebra for Data Science, Machine Learning, and Signal Processing - Ch 11 Neural Network Models]]
- [[Linear Algebra for Data Science, Machine Learning, and Signal Processing - Ch 12 Random Matrix Theory Signal Plus Noise Matrices and Phase Transitions]]

## Core objects and modeling vocabulary

- matrix and linear map `A`, with vectors living in domain and codomain spaces rather than as free-floating arrays
- eigendecomposition and SVD as the main spectral factorizations, with singular values measuring usable directions and conditioning
- column space, row space, null space, rank, orthogonality, and projection as the geometry behind identifiability and approximation
- PSD structure, norms, and condition numbers as the language of stability, error amplification, and regularization
- least-squares objectives, pseudoinverses, and ridge-style penalties as the estimation layer built on top of matrix geometry
- low-rank factors, truncation, shrinkage, and completion as the representation layer for compression and denoising
- stochastic matrices, Markov-chain operators, and graph-normalized matrices as structured linear systems
- gradients, step sizes, and preconditioners as the optimization vocabulary that turns algebra into computation

## Main themes

### 1. SVD is the central organizing object

The book keeps returning to the SVD because it unifies:

- geometry of linear transforms
- least-squares solutions
- low-rank approximation
- conditioning
- graph and matrix-completion methods
- perturbation and noise analysis

That is the right emphasis for a quant vault. In practice, many "different" methods are SVD methods with different disguises.

### 2. Representation and optimization are inseparable

The book does not treat matrix factorization as pure representation and optimization as a separate numerical chapter. Instead, Chapter 5 already turns factorization into an estimator, Chapter 7 turns it into compression and denoising, and Chapter 9 turns conditioning into convergence speed. This is exactly how quant research works in production.

### 3. Geometry controls statistical and computational behavior

Subspaces, orthogonality, singular directions, and conditioning are not decorative. They determine:

- what can be identified
- what is stable under noise
- what can be compressed
- what converges quickly
- what explodes under inversion

### 4. The book is application-oriented but still mathematically useful

The proofs are selective rather than exhaustive, but the strongest chapters still expose the main theorem spine. That makes the book a good vault source if we separate scan notes from theorem-level deep notes honestly.

## Promoted durable notes

- [[Singular Value Decomposition]]
- [[Least Squares and Pseudoinverse]]
- [[Low-Rank Approximation]]
- [[Gradient Descent and Preconditioning]]

## Next promotion targets

- subspace geometry and the four fundamental spaces
- PageRank and spectral graph methods
- matrix completion under partial observation
- random-matrix perturbation and phase-transition notes

## Caveats

- The book is strongly applied. It is excellent for matrix-method intuition, but it is not the final authority on abstract linear algebra, numerical linear algebra, or modern random matrix theory.
- Several later chapters are bridges, not exhaustive treatments.
- The implementation language is Julia. The concepts transfer; the code idioms do not need to become vault standards.

## Related notes

- [[All of Statistics]]
- [[Math Map]]
- [[ML Map]]
- [[Signal Processing Map]]
- [[Convex Optimization Methods]]
- [[Time-Series Forecasting]]
- [[Kalman Filtering]]

## Sources

- [[raw/math_statistics/Linear Algebra for Data Science, Machine Learning, and Signal Processing (2024).pdf]]
