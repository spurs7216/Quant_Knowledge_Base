---
title: Convex Optimization - Ch 04 Convex Optimization Problems
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - optimization
  - convex-optimization
  - chapter-digest
  - convex-problems
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: pymupdf_scan_of_standard_form_and_optimality_pages_plus epigraph and reformulation sections
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 04 Convex Optimization Problems
parent_source: "[[Convex Optimization]]"
sources:
  - "[[Convex Optimization]]"
  - "[[raw/math_statistics/Boyd and Vandenberghe, Convex Optimization.pdf]]"
---
# Convex Optimization - Ch 04 Convex Optimization Problems

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed against the raw source.
- Pass 2: theorem-level extraction completed for standard form, epigraph form, local-global optimality, and first-order optimality over convex feasible sets.

## Deepening Targets

- If the vault later standardizes a convex-modeling checklist, promote the reformulation tricks from this chapter into a method note on convex problem design.

## Deepened Subparts

- `4.1` optimization problem form
- `4.2` convex optimization and first-order optimality
- selected reformulation logic from epigraph and equivalent-problem sections

## Role of the chapter

This chapter defines what the book means by a convex optimization problem and why that stricter definition matters.

The durable point is that "minimize a convex function over a convex set" is not enough for solver design. The feasible set must also be expressed through convex inequalities and affine equalities so the problem can be certified and manipulated structurally.

## Core mathematical objects

- standard form
  $$\begin{aligned}
  \min_x \quad & f_0(x) \\
  \text{subject to} \quad & f_i(x) \le 0,\quad i=1,\dots,m \\
  & h_i(x)=0,\quad i=1,\dots,p
  \end{aligned}$$
- convex standard form
  $$\begin{aligned}
  \min_x \quad & f_0(x) \\
  \text{subject to} \quad & f_i(x) \le 0,\quad i=1,\dots,m \\
  & a_i^\trans x = b_i,\quad i=1,\dots,p
  \end{aligned}$$
- epigraph form
  $$\begin{aligned}
  \min_{x,t} \quad & t \\
  \text{subject to} \quad & f_0(x) \le t \\
  & f_i(x) \le 0,\quad i=1,\dots,m \\
  & Ax=b
  \end{aligned}$$

## Structural map of the chapter

- problem terminology
- convex standard form
- local versus global optimality
- first-order optimality condition
- equivalent convex reformulations

## Theorem and derivation spine

### Convex standard form

The book's convex standard form is
$$\begin{aligned}
  \min_x \quad & f_0(x) \\
  \text{subject to} \quad & f_i(x) \le 0,\quad i=1,\dots,m \\
  & a_i^\trans x = b_i,\quad i=1,\dots,p,
\end{aligned}$$
where $f_0,\dots,f_m$ are convex.

The feasible set is convex because it is the intersection of:

- the common domain
- convex sublevel sets $\set{x \mid f_i(x)\le 0}$
- affine hyperplanes $\set{x \mid a_i^\trans x=b_i}$

### Local optimum equals global optimum

If $x$ is locally optimal for a convex optimization problem, then $x$ is globally optimal.

The proof logic is simple and reusable: if there were a better feasible point $y$, then any sufficiently near convex combination
$$z=(1-\theta)x+\theta y$$
would remain feasible and satisfy
$$f_0(z) \le (1-\theta)f_0(x)+\theta f_0(y) < f_0(x),$$
contradicting local optimality.

This is the precise reason convexity makes local search meaningful.

### First-order optimality over a convex feasible set

Let $X$ be the feasible set and assume $f_0$ is differentiable. Then $x^\star \in X$ is optimal if and only if
$$\nabla f_0(x^\star)^\trans (y-x^\star) \ge 0 \quad \text{for all } y \in X.$$

The geometric meaning is that the gradient defines a supporting hyperplane to the feasible set at the optimizer.

### Important special cases

For unconstrained problems, the condition reduces to
$$\nabla f_0(x^\star)=0.$$

For equality-constrained problems,
$$\min_x f_0(x) \quad \text{s.t.} \quad Ax=b,$$
the optimality condition becomes
$$\nabla f_0(x^\star)+A^\trans \nu^\star = 0, \qquad Ax^\star=b,$$
which is the basic Lagrange multiplier system later absorbed into KKT.

### Epigraph form is structurally important

The epigraph reformulation
$$\min_{x,t}\; t \quad \text{s.t.} \quad f_0(x)\le t$$
turns nonlinear objectives into linear objectives plus one convex inequality. This is one of the most durable reformulation moves in the book because it keeps convexity visible to the solver.

## Failure modes and misuse points

- calling a problem "convex" because the objective is convex while hiding nonconvex equalities in the constraints
- forgetting that convex feasible geometry alone is not the same as convex standard form
- using first-order optimality without checking differentiability and feasibility assumptions
- treating local search output as globally meaningful outside convex structure

## Quant research relevance

This chapter is the vault's modeling grammar for:

- portfolio programs
- constrained estimators
- regularized fitting
- likelihood problems with parameter restrictions
- any later use of duality or interior-point methods

## What should be promoted out of this source note

- a durable note on convex reformulation patterns
- a durable note on first-order optimality as supporting-hyperplane geometry

## Related notes

- [[Convex Optimization]]
- [[Convex Optimization - Ch 03 Convex Functions]]
- [[Convex Optimization - Ch 05 Duality]]
- [[Convex Optimization Methods]]

## Sources

- [[Convex Optimization]]
- [[raw/math_statistics/Boyd and Vandenberghe, Convex Optimization.pdf]]
