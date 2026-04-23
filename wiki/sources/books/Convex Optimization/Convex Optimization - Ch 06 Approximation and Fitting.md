---
title: Convex Optimization - Ch 06 Approximation and Fitting
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - optimization
  - convex-optimization
  - chapter-digest
  - approximation
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: pymupdf_scan_of_regularization_and_robust_approximation_pages_plus least_norm sections
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 06 Approximation and Fitting
parent_source: "[[Convex Optimization]]"
sources:
  - "[[Convex Optimization]]"
  - "[[raw/math_statistics/Boyd and Vandenberghe, Convex Optimization.pdf]]"
---
# Convex Optimization - Ch 06 Approximation and Fitting

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed against the raw source.
- Pass 2: theorem-level extraction completed for norm approximation, least-norm problems, regularization, Tikhonov smoothing, sparse surrogates, and robust penalty design.

## Deepening Targets

- If robust optimization becomes a larger branch in the vault, deepen the uncertainty-set reformulations beyond the fitting examples in this chapter.

## Deepened Subparts

- `6.1` norm approximation
- `6.2` least-norm problems
- `6.3` regularized approximation
- selected robust penalty material around the Huber loss

## Role of the chapter

This chapter is where convex optimization starts acting like an estimation language instead of a pure solver chapter.

Its durable contribution is the exact trade-off logic between fit and structure:

- fit versus size
- fit versus smoothness
- fit versus sparsity surrogate
- fit versus robustness to outliers or perturbation

## Core mathematical objects

- bi-criterion fitting problem
  $$\min \text{ w.r.t. } \R_+^2 \quad \paren{\norm{Ax-b},\;\norm{x}}$$
- weighted regularization
  $$\min_x \; \norm{Ax-b} + \lambda \norm{x}, \qquad \lambda>0$$
- Tikhonov regularization
  $$\min_x \; \norm{Ax-b}_2^2 + \lambda \norm{x}_2^2$$
- smoothing regularization
  $$\min_x \; \norm{Ax-b}_2^2 + \lambda \norm{Dx}_2^2$$
- sparse convex surrogate
  $$\min_x \; \norm{Ax-b}_2 + \lambda \norm{x}_1$$

## Structural map of the chapter

- norm approximation and penalty functions
- least-norm solutions of underdetermined systems
- regularization as scalarization of a two-objective trade-off
- smoothing and structure penalties
- robust losses and outlier resistance

## Theorem and derivation spine

### Bi-criterion formulation

The chapter frames regularization as the two-objective problem
$$\min \text{ w.r.t. } \R_+^2 \quad \paren{\norm{Ax-b},\;\norm{x}}.$$

This matters because it prevents a common mistake: regularization is not a random extra term. It is a scalarization of a real Pareto trade-off between data fit and structural simplicity.

### Weighted regularization

One scalarization is
$$\min_x \; \norm{Ax-b} + \lambda \norm{x}, \qquad \lambda>0.$$

The parameter $\lambda$ is the exchange rate between residual reduction and structure. In quant work, that is usually not a mere numerical knob; it prices model complexity, smoothness, or robustness.

### Tikhonov regularization

With Euclidean norms, the chapter's canonical problem is
$$\min_x \; \norm{Ax-b}_2^2 + \lambda \norm{x}_2^2.$$

Differentiating gives the normal equation
$$\paren{A^\trans A + \lambda I}x = A^\trans b,$$
so the solution is
$$x = \paren{A^\trans A + \lambda I}^{-1} A^\trans b.$$

The durable point is that $A^\trans A + \lambda I \succ 0$ for every $\lambda>0$, so regularization is simultaneously:

- statistical shrinkage
- numerical stabilization
- a statement that large coefficients are costly

### Smoothing regularization

The size penalty generalizes to a structural penalty:
$$\min_x \; \norm{Ax-b}_2^2 + \lambda \norm{Dx}_2^2.$$

When $D$ approximates a first or second derivative operator, the regularizer penalizes roughness rather than raw magnitude. This is the right objective when "simple" means smooth.

### Least-norm and sparse solutions

For underdetermined systems $Ax=b$, the least-norm problem
$$\min_x \; \norm{x} \quad \text{s.t.} \quad Ax=b$$
chooses the smallest feasible solution under the chosen geometry.

The least-$\ell_1$ problem
$$\min_x \; \norm{x}_1 \quad \text{s.t.} \quad Ax=b$$
often yields sparse solutions, not because $\ell_1$ counts support exactly, but because it is the tightest widely tractable convex surrogate that still pushes mass toward zero.

### Robust penalties and Huber loss

The chapter emphasizes that large-residual sensitivity depends on how fast the penalty grows in the tails.

The Huber penalty is
$$
\phi_{\text{hub}}(u)=
\begin{cases}
u^2, & \abs{u}\le M, \\
M\paren{2\abs{u}-M}, & \abs{u}>M.
\end{cases}
$$

It agrees with least squares near zero but grows only linearly in the tails, so outliers are not allowed to dominate the fit as aggressively as under a pure quadratic loss.

## Failure modes and misuse points

- treating $\lambda$ as a technical tuning constant instead of a structural modeling choice
- using ridge penalties when the real desideratum is smoothness or sparsity
- calling a problem robust without specifying what perturbation or outlier model is being defended against
- over-reading sparse solutions from $\ell_1$ relaxations as if they solved exact cardinality selection

## Quant research relevance

This chapter is directly useful for:

- shrinkage of noisy estimators
- smooth signal and state reconstruction
- sparse factor or signal combination
- robust regression under outliers
- numerically stable inverse problems

## What should be promoted out of this source note

- [[Regularization and Robust Approximation]]
- a durable note on uncertainty sets and robust reformulation logic

## Related notes

- [[Convex Optimization]]
- [[Convex Optimization - Ch 07 Statistical Estimation]]
- [[Regularization and Robust Approximation]]
- [[Least Squares and Pseudoinverse]]
- [[Portfolio Optimization]]

## Sources

- [[Convex Optimization]]
- [[raw/math_statistics/Boyd and Vandenberghe, Convex Optimization.pdf]]
