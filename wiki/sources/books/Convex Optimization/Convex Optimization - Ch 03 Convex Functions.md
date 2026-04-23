---
title: Convex Optimization - Ch 03 Convex Functions
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - optimization
  - convex-optimization
  - chapter-digest
  - convex-functions
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: pymupdf_scan_of_definition_and_characterization_pages_plus supporting examples
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 03 Convex Functions
parent_source: "[[Convex Optimization]]"
sources:
  - "[[Convex Optimization]]"
  - "[[raw/math_statistics/Boyd and Vandenberghe, Convex Optimization.pdf]]"
---
# Convex Optimization - Ch 03 Convex Functions

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed against the raw source.
- Pass 2: theorem-level extraction completed for the definition of convexity, first- and second-order tests, epigraph logic, and core closure operations.

## Deepening Targets

- If the vault later deepens convex analysis as its own branch, promote conjugates and epigraph transforms into a dedicated durable note.

## Deepened Subparts

- `3.1` basic properties and examples
- `3.2` operations that preserve convexity
- selected durable examples from support functions, log-sum-exp, and spectral functions

## Role of the chapter

This chapter turns convexity from geometry of sets into geometry of objectives.

The durable lesson is that convexity is not a vague "nice shape." It is an inequality class with exact differential tests and exact closure rules, which later justify why optimization formulations stay tractable after reformulation.

## Core mathematical objects

- convexity definition
  $$f\paren{\theta x + (1-\theta)y} \le \theta f(x) + (1-\theta)f(y), \qquad 0 \le \theta \le 1$$
- first-order characterization for differentiable $f$
  $$f(y) \ge f(x) + \nabla f(x)^\trans (y-x)$$
- second-order characterization for twice differentiable $f$
  $$\nabla^2 f(x) \succeq 0$$
- epigraph
  $$\operatorname{epi} f = \set{(x,t) \mid f(x) \le t}$$
- pointwise supremum closure
  $$g(x)=\sup_{y \in A} f(x,y)$$

## Structural map of the chapter

- definition and geometric meaning
- first-order and second-order tests
- operations that preserve convexity
- conjugate function and quasiconvexity
- log-convex and generalized-inequality variants

## Theorem and derivation spine

### Definition and chord inequality

A function $f:\R^n \to \R$ is convex if its domain is convex and
$$f\paren{\theta x + (1-\theta)y} \le \theta f(x) + (1-\theta) f(y)$$
for all $x,y$ in the domain and $0 \le \theta \le 1$.

Geometrically, the chord between $(x,f(x))$ and $(y,f(y))$ lies above the graph. That picture becomes algebra later.

### First-order characterization

For differentiable $f$, convexity is equivalent to
$$f(y) \ge f(x) + \nabla f(x)^\trans (y-x) \quad \text{for all } x,y.$$

This says the tangent affine function at $x$ is a global underestimator. That is the single most reusable formula in the book, because it is what turns gradients into global certificates instead of local heuristics.

### Second-order characterization

For twice differentiable $f$, convexity is equivalent to
$$\nabla^2 f(x) \succeq 0 \quad \text{for all } x \in \operatorname{dom} f.$$

Strict positivity of the Hessian,
$$\nabla^2 f(x) \succ 0,$$
is a clean sufficient condition for strict convexity on convex domains, and later underpins uniqueness and the Newton-system geometry.

### Epigraph criterion

Convexity of $f$ is equivalent to convexity of its epigraph:
$$\operatorname{epi} f = \set{(x,t)\mid f(x)\le t}.$$

This is why epigraph reformulations are not cosmetic. They preserve convexity because they literally replace a function by its convex upper set in one more dimension.

### Closure rules that matter later

The chapter's most useful closure rules for vault work are:

- nonnegative weighted sums of convex functions are convex
- composition with affine maps preserves convexity
- pointwise supremum of convex functions is convex
- intersection of convex epigraphs remains convex

These rules explain why support functions, norms, log-sum-exp, and many barrier or penalty constructions remain convex after reformulation.

### Support function example

For any nonempty set $C \subseteq \R^n$, the support function
$$S_C(x)=\sup_{y \in C} x^\trans y$$
is convex because it is the pointwise supremum of linear functions in $x$.

That one example is conceptually large: many dual objects, norm formulas, and robust bounds are support functions in disguise.

## Failure modes and misuse points

- checking convexity by plotting only one slice of a multivariate function
- confusing Jensen-style inequalities with strict convexity or strong convexity
- using Hessian tests when the domain or differentiability assumptions fail
- forgetting that closure rules have sign restrictions, especially for weighted sums and composition

## Quant research relevance

This chapter matters because most convex quant formulations are built by function calculus, not by starting from a finished theorem:

- likelihood objectives
- regularizers and penalties
- barrier terms
- norm and spectral risk measures
- robust support-function bounds

## What should be promoted out of this source note

- a durable note on first-order convexity and tangent underestimators
- a durable note on epigraph reformulation and closure rules for model construction

## Related notes

- [[Convex Optimization]]
- [[Convex Optimization - Ch 02 Convex Sets]]
- [[Convex Optimization - Ch 04 Convex Optimization Problems]]
- [[Convex Optimization Methods]]

## Sources

- [[Convex Optimization]]
- [[raw/math_statistics/Boyd and Vandenberghe, Convex Optimization.pdf]]
