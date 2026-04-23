---
title: Convex Optimization
type: source
status: overview_source
updated: 2026-04-22
tags:
  - source
  - book
  - optimization
  - convex-optimization
source_type: book
source_class: overview_source
read_scope: full_source
source_author:
  - Stephen Boyd
  - Lieven Vandenberghe
source_year: 2004
source_order: 10
domain: mathematics
extraction_basis: full_toc_plus_selected_theorem_pages_via_pymupdf_plus_mathjax_reingest_of_deep_chapters
technical_depth: deep
parent_source: null
sources:
  - "[[raw/math_statistics/Boyd and Vandenberghe, Convex Optimization.pdf]]"
---
# Convex Optimization

## Citation / metadata

- Authors: Stephen Boyd and Lieven Vandenberghe
- Year: 2004
- Source type: textbook
- Read scope: `full_source`
- Shelf role: optimization spine for convex modeling, duality, statistical estimation, and interior-point methods
- Raw source: [[raw/math_statistics/Boyd and Vandenberghe, Convex Optimization.pdf]]

## Why this book matters

This is the main mathematical spine for writing optimization problems in a way that is globally certifiable, algorithmically solvable, and economically interpretable.

For this vault, the durable value is not only solver literacy. The book gives the modeling grammar behind:

- convex feasible sets and convex objectives
- dual certificates and KKT systems
- regularized estimation and robust approximation
- Newton, self-concordance, and interior-point logic

## Reading logic from the source

The book was reingested under the current three-step rule:

1. full chapter scan across all eleven chapters
2. theorem-level deepening on the load-bearing chapters for convex sets, convex functions, convex problem form, duality, approximation/fitting, statistical estimation, unconstrained minimization, and interior-point methods
3. promotion of the most reusable mathematical material into durable method notes

The parent note stays thin. The actual technical spine lives in the chapter shelf and promoted notes.

## Stage map

- `scan`: [[Convex Optimization - Ch 01 Introduction]]
- `deep`: [[Convex Optimization - Ch 02 Convex Sets]]
- `deep`: [[Convex Optimization - Ch 03 Convex Functions]]
- `deep`: [[Convex Optimization - Ch 04 Convex Optimization Problems]]
- `deep`: [[Convex Optimization - Ch 05 Duality]]
- `deep`: [[Convex Optimization - Ch 06 Approximation and Fitting]]
- `deep`: [[Convex Optimization - Ch 07 Statistical Estimation]]
- `selective_deepen`: [[Convex Optimization - Ch 08 Geometric Problems]]
- `deep`: [[Convex Optimization - Ch 09 Unconstrained Minimization]]
- `selective_deepen`: [[Convex Optimization - Ch 10 Equality Constrained Minimization]]
- `deep`: [[Convex Optimization - Ch 11 Interior-Point Methods]]

## Chapter shelf

- [[Convex Optimization - Ch 01 Introduction]]
- [[Convex Optimization - Ch 02 Convex Sets]]
- [[Convex Optimization - Ch 03 Convex Functions]]
- [[Convex Optimization - Ch 04 Convex Optimization Problems]]
- [[Convex Optimization - Ch 05 Duality]]
- [[Convex Optimization - Ch 06 Approximation and Fitting]]
- [[Convex Optimization - Ch 07 Statistical Estimation]]
- [[Convex Optimization - Ch 08 Geometric Problems]]
- [[Convex Optimization - Ch 09 Unconstrained Minimization]]
- [[Convex Optimization - Ch 10 Equality Constrained Minimization]]
- [[Convex Optimization - Ch 11 Interior-Point Methods]]

## Core objects and modeling vocabulary

- primal convex program
  $$\begin{aligned}
  \min_x \quad & f_0(x) \\
  \text{subject to} \quad & f_i(x) \le 0, \quad i=1,\dots,m \\
  & Ax = b
  \end{aligned}$$
- convex set and convex combination
  $$\theta x + (1-\theta) y, \qquad 0 \le \theta \le 1$$
- convexity inequality
  $$f\paren{\theta x + (1-\theta)y} \le \theta f(x) + (1-\theta)f(y)$$
- Lagrangian
  $$L(x,\lambda,\nu)=f_0(x)+\sum_{i=1}^m \lambda_i f_i(x)+\nu^\trans(Ax-b)$$
- dual function and dual problem
  $$g(\lambda,\nu)=\inf_x L(x,\lambda,\nu), \qquad \max_{\lambda \succeq 0,\nu} g(\lambda,\nu)$$
- KKT system
  $$\lambda_i \ge 0,\quad f_i(x^\star)\le 0,\quad \lambda_i f_i(x^\star)=0,\quad \nabla f_0(x^\star)+\sum_i \lambda_i \nabla f_i(x^\star)+A^\trans \nu^\star = 0$$
- Tikhonov regularization
  $$\min_x \norm{Ax-b}_2^2 + \lambda \norm{x}_2^2$$
- Newton decrement
  $$\lambda(x)=\sqrt{\nabla f(x)^\trans \nabla^2 f(x)^{-1}\nabla f(x)}$$
- log barrier and central path
  $$\phi(x)=-\sum_{i=1}^m \log\paren{-f_i(x)}, \qquad \min_x \; t f_0(x)+\phi(x) \;\; \text{s.t.} \;\; Ax=b$$

## Main themes

- Convexity is valuable because it converts local information into global guarantees.
- Duality is not auxiliary theory. It is the certificate layer that turns numerical output into interpretable optimality, sensitivity, and stopping logic.
- Regularization is a modeling choice about what kind of solution should be preferred, not a numerical patch.
- Statistical estimation problems often become convex once likelihoods, priors, and inverse-covariance parameterizations are written correctly.
- Newton and interior-point methods matter because they exploit convex geometry rather than fighting it.

## Promoted durable notes

- [[Convex Optimization Methods]]
- [[Convex Duality and KKT Conditions]]
- [[Regularization and Robust Approximation]]
- [[Interior-Point Methods]]
- [[Gradient Descent and Preconditioning]]

## Next promotion targets

- a durable note on separating hyperplanes, support functions, and generalized inequalities
- a durable note on self-concordance and Newton decrement as an optimizer-facing diagnostic language
- a durable note on logistic regression and covariance estimation as convex statistical programs

## Caveats

- The parent book note is not the right place for proof details, KKT derivations, or barrier-system algebra. Those belong in the deep chapter notes and promoted method notes.
- The book is broad. Some chapters are conceptually important but not yet promoted because the vault benefits more from a strong method spine than from exhaustive textbook restatement.
- Theorems and equations here are paraphrased into vault notation; the raw PDF remains the source of truth.

## Related notes

- [[Convex Optimization Methods]]
- [[Convex Duality and KKT Conditions]]
- [[Regularization and Robust Approximation]]
- [[Interior-Point Methods]]
- [[Gradient Descent and Preconditioning]]
- [[Portfolio Optimization]]

## Sources

- [[raw/math_statistics/Boyd and Vandenberghe, Convex Optimization.pdf]]
