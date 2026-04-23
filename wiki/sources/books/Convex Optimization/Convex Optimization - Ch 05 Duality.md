---
title: Convex Optimization - Ch 05 Duality
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - optimization
  - convex-optimization
  - chapter-digest
  - duality
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: pymupdf_scan_of_weak_and_strong_duality_pages_plus_slater_and_geometric_interpretation_sections
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 05 Duality
parent_source: "[[Convex Optimization]]"
sources:
  - "[[Convex Optimization]]"
  - "[[raw/math_statistics/Boyd and Vandenberghe, Convex Optimization.pdf]]"
---
# Convex Optimization - Ch 05 Duality

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed against the raw source.
- Pass 2: theorem-level extraction completed for the Lagrangian, weak and strong duality, Slater's condition, complementary slackness, KKT conditions, and the geometric interpretation via supporting hyperplanes.

## Deepening Targets

- If the vault later needs a stronger proof spine, deepen the separating-hyperplane proof of strong duality and the perturbation-sensitivity section into dedicated durable notes.

## Deepened Subparts

- `5.2` the Lagrange dual problem
- `5.3` geometric interpretation of duality
- `5.5` KKT conditions and sensitivity logic

## Role of the chapter

This is the theoretical center of the book.

The chapter explains how a constrained primal problem generates a second optimization problem whose feasible points are certificates. Weak duality gives lower bounds. Strong duality makes the bounds exact. KKT turns that relationship into an operational optimality system.

## Core mathematical objects

- primal problem
  $$\begin{aligned}
  \min_x \quad & f_0(x) \\
  \text{subject to} \quad & f_i(x) \le 0,\quad i=1,\dots,m \\
  & Ax=b
  \end{aligned}$$
- Lagrangian
  $$L(x,\lambda,\nu)=f_0(x)+\sum_{i=1}^m \lambda_i f_i(x)+\nu^\trans (Ax-b)$$
- dual function
  $$g(\lambda,\nu)=\inf_x L(x,\lambda,\nu)$$
- duality gap
  $$p^\star-d^\star$$
- KKT complementarity
  $$\lambda_i^\star f_i(x^\star)=0$$

## Structural map of the chapter

- Lagrange dual function
- weak duality
- strong duality under Slater-type conditions
- geometric interpretation through supporting hyperplanes
- KKT optimality conditions
- perturbation and sensitivity interpretation

## Theorem and derivation spine

### Lagrangian and dual function

For the convex program
$$\begin{aligned}
\min_x \quad & f_0(x) \\
\text{subject to} \quad & f_i(x) \le 0,\quad i=1,\dots,m \\
& Ax=b,
\end{aligned}$$
the Lagrangian is
$$L(x,\lambda,\nu)=f_0(x)+\sum_{i=1}^m \lambda_i f_i(x)+\nu^\trans(Ax-b),$$
and the dual function is
$$g(\lambda,\nu)=\inf_x L(x,\lambda,\nu).$$

The dual problem is
$$\max_{\lambda \succeq 0,\nu} g(\lambda,\nu).$$

### Weak duality

If $\lambda \succeq 0$, then for any primal-feasible $\tilde x$,
$$L(\tilde x,\lambda,\nu) \le f_0(\tilde x),$$
because $f_i(\tilde x)\le 0$ and $A\tilde x=b$.

Taking infimum over $x$ gives
$$g(\lambda,\nu) \le f_0(\tilde x).$$
Since this holds for every feasible $\tilde x$,
$$g(\lambda,\nu) \le p^\star.$$

That inequality is the whole lower-bound engine.

### Strong duality under Slater's condition

For the convex problem, if there exists $x \in \operatorname{relint} D$ such that
$$f_i(x) < 0,\quad i=1,\dots,m, \qquad Ax=b,$$
then strong duality holds:
$$d^\star = p^\star.$$

The book's geometric point is that strong duality means the epigraph-style value set admits a nonvertical supporting hyperplane at the primal optimum.

### Complementary slackness

If $x^\star$ and $(\lambda^\star,\nu^\star)$ are primal-dual optimal with zero duality gap, then
$$\lambda_i^\star f_i(x^\star)=0,\qquad i=1,\dots,m.$$

So each inequality is either active or carries zero multiplier. This is the exact mathematical statement behind "which constraints are binding?"

### KKT conditions

For differentiable convex problems, under strong duality the primal-dual optimum satisfies:
$$f_i(x^\star)\le 0,\qquad Ax^\star=b,\qquad \lambda^\star \succeq 0,$$
$$\lambda_i^\star f_i(x^\star)=0,\qquad i=1,\dots,m,$$
$$\nabla f_0(x^\star)+\sum_{i=1}^m \lambda_i^\star \nabla f_i(x^\star)+A^\trans \nu^\star = 0.$$

For convex problems, these conditions are also sufficient.

### Suboptimality certificate

For any primal-feasible $x$ and dual-feasible $(\lambda,\nu)$,
$$f_0(x)-g(\lambda,\nu)$$
is a certified upper bound on primal suboptimality.

That expression is why duality matters operationally: it turns an optimizer's current iterate into something auditable.

### Sensitivity interpretation

The perturbation sections justify reading multipliers as marginal values or shadow prices of constraints. This is not always an economic interpretation, but it is a correct directional-derivative interpretation of the value function under constraint perturbation.

## Failure modes and misuse points

- assuming strong duality because the problem "looks convex" without checking regularity
- applying KKT outside convex or differentiable structure
- reading multipliers as economically meaningful when the model itself is poorly posed
- confusing a tiny duality gap with a good research problem

## Quant research relevance

This chapter is central whenever a constrained quant result must be certified:

- portfolio exposure and leverage constraints
- regularization viewed as penalized constraints
- active-constraint diagnostics
- solver stopping criteria
- sensitivity of the optimum to risk or turnover caps

## What should be promoted out of this source note

- [[Convex Duality and KKT Conditions]]
- a durable note on sensitivity, shadow prices, and active-set interpretation

## Related notes

- [[Convex Optimization]]
- [[Convex Optimization - Ch 04 Convex Optimization Problems]]
- [[Convex Optimization - Ch 10 Equality Constrained Minimization]]
- [[Convex Duality and KKT Conditions]]
- [[Interior-Point Methods]]

## Sources

- [[Convex Optimization]]
- [[raw/math_statistics/Boyd and Vandenberghe, Convex Optimization.pdf]]
