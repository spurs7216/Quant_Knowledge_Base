---
title: Convex Optimization - Ch 11 Interior-Point Methods
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - optimization
  - convex-optimization
  - chapter-digest
  - interior-point
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: pymupdf_scan_of_barrier_central_path_and_complexity_pages
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 11 Interior-Point Methods
parent_source: "[[Convex Optimization]]"
sources:
  - "[[Convex Optimization]]"
  - "[[raw/math_statistics/Boyd and Vandenberghe, Convex Optimization.pdf]]"
---
# Convex Optimization - Ch 11 Interior-Point Methods

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed against the raw source.
- Pass 2: theorem-level extraction completed for the logarithmic barrier, central path, perturbed KKT system, and barrier-method convergence logic.

## Deepening Targets

- If cone programming becomes a larger vault branch, deepen the generalized-inequality and primal-dual extensions beyond the standard nonlinear-inequality treatment here.

## Deepened Subparts

- `11.2` logarithmic barrier and central path
- `11.3` barrier method
- selected modified-KKT and complexity sections

## Role of the chapter

This chapter explains how constrained convex programs are solved by turning hard boundaries into smooth interior geometry and then using Newton systems on that geometry.

The durable point is that the method is not "add a penalty and hope." The barrier formulation produces a structured family of equality-constrained problems whose central points carry explicit dual certificates.

## Core mathematical objects

- original problem
  $$\begin{aligned}
  \min_x \quad & f_0(x) \\
  \text{subject to} \quad & f_i(x)\le 0,\quad i=1,\dots,m \\
  & Ax=b
  \end{aligned}$$
- logarithmic barrier
  $$\phi(x)=-\sum_{i=1}^m \log\paren{-f_i(x)}$$
- barrier subproblem
  $$\min_x \; t f_0(x)+\phi(x) \quad \text{s.t.} \quad Ax=b$$
- central-path dual variables
  $$\lambda_i(t) = -\frac{1}{t f_i(x(t))}$$
- central-path complementarity
  $$-\lambda_i(t) f_i(x(t))=\frac{1}{t}$$

## Structural map of the chapter

- log-barrier approximation of inequalities
- central path and its KKT interpretation
- barrier method as a sequence of centering problems
- modified KKT system and Newton steps
- complexity discussion

## Theorem and derivation spine

### Logarithmic barrier

The indicator of the inequality constraints is replaced by the smooth barrier
$$\phi(x)=-\sum_{i=1}^m \log\paren{-f_i(x)},$$
whose domain is the strict interior
$$\set{x \mid f_i(x)<0,\; i=1,\dots,m}.$$

The associated subproblem is
$$\min_x \; t f_0(x)+\phi(x) \quad \text{s.t.} \quad Ax=b.$$

As $t$ increases, the barrier weight relative to the objective decreases, so the solution moves closer to the true constrained optimum.

### Central path

Let $x(t)$ denote the minimizer of the barrier subproblem. Then there exists $\nu(t)$ such that
$$t\nabla f_0(x(t)) + \nabla \phi(x(t)) + A^\trans \nu(t)=0,$$
with strict feasibility
$$Ax(t)=b,\qquad f_i(x(t))<0.$$

Using
$$\nabla \phi(x)=\sum_{i=1}^m -\frac{1}{f_i(x)} \nabla f_i(x),$$
the book defines
$$\lambda_i(t)=-\frac{1}{t f_i(x(t))},$$
which is dual feasible and satisfies
$$-\lambda_i(t)f_i(x(t))=\frac{1}{t}.$$

So the central path solves a perturbed KKT system.

### Explicit duality gap along the central path

The associated dual feasible point has objective value
$$g\paren{\lambda(t),\nu(t)} = f_0(x(t))-\frac{m}{t},$$
so
$$f_0(x(t)) - p^\star \le \frac{m}{t}.$$

This is the chapter's key quantitative fact: every central point carries a duality-gap certificate with closed-form size $m/t$.

### Barrier method

The method computes central points for an increasing sequence $t, \mu t, \mu^2 t,\dots$:

1. approximately solve the barrier subproblem for current $t$
2. use that point to initialize the next centering step
3. stop when $m/t < \eps$

The practical idea is continuation: each centering problem is warm-started from the previous one, so high-accuracy constrained solutions are obtained by a chain of easier interior problems.

### Modified KKT interpretation

The central-path equations are the original KKT system with complementarity
$$\lambda_i f_i(x)=0$$
replaced by
$$\lambda_i f_i(x) = -\frac{1}{t}.$$

That is the precise mathematical meaning of "interior-point": the method follows perturbed complementarity until the perturbation vanishes.

## Failure modes and misuse points

- treating the barrier term as an arbitrary penalty instead of a structured interior approximation
- ignoring that strict feasibility is part of the geometry
- using interior-point methods on badly scaled models and then blaming the solver for linear-algebra stress
- treating low duality gap as a substitute for checking whether the model encodes the right economics

## Quant research relevance

This chapter matters for:

- constrained portfolio optimization
- high-accuracy risk or exposure problems
- convex programs where dual variables and active constraints are economically meaningful
- understanding why solver logs expose primal residual, dual residual, and gap

## What should be promoted out of this source note

- [[Interior-Point Methods]]
- a durable note on central path, perturbed complementarity, and primal-dual residuals

## Related notes

- [[Convex Optimization]]
- [[Convex Optimization - Ch 05 Duality]]
- [[Convex Optimization - Ch 09 Unconstrained Minimization]]
- [[Interior-Point Methods]]
- [[Convex Duality and KKT Conditions]]

## Sources

- [[Convex Optimization]]
- [[raw/math_statistics/Boyd and Vandenberghe, Convex Optimization.pdf]]
