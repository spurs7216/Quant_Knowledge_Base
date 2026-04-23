---
title: Convex Optimization - Ch 09 Unconstrained Minimization
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - optimization
  - convex-optimization
  - chapter-digest
  - numerical-optimization
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: pymupdf_scan_of_self_concordance_and_newton_decrement_pages_plus chapter-level solver structure
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 09 Unconstrained Minimization
parent_source: "[[Convex Optimization]]"
sources:
  - "[[Convex Optimization]]"
  - "[[raw/math_statistics/Boyd and Vandenberghe, Convex Optimization.pdf]]"
---
# Convex Optimization - Ch 09 Unconstrained Minimization

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed against the raw source.
- Pass 2: theorem-level extraction completed for gradient and Newton methods, Newton decrement, and the self-concordance analysis that gives explicit complexity bounds.

## Deepening Targets

- If the vault later formalizes optimizer diagnostics, promote Newton decrement and self-concordance into a durable note on second-order stopping logic.

## Deepened Subparts

- descent and line-search structure
- Newton's method
- `9.6` self-concordance and its complexity consequences

## Role of the chapter

This chapter explains why second-order methods are different from generic iterative descent.

The durable point is that Newton's method is not just "use the Hessian." It solves a local quadratic model, and for self-concordant functions the book gives explicit suboptimality and iteration bounds in terms of the Newton decrement.

## Core mathematical objects

- Newton step
  $$\Delta x_{\mathrm{nt}} = -\nabla^2 f(x)^{-1}\nabla f(x)$$
- Newton decrement
  $$\lambda(x)=\sqrt{\nabla f(x)^\trans \nabla^2 f(x)^{-1}\nabla f(x)}$$
- self-concordance in one dimension
  $$\abs{f'''(x)} \le 2\paren{f''(x)}^{3/2}$$
- self-concordance on $\R^n$
  $$t \mapsto f(x+tv) \text{ is self-concordant for every } x,v$$

## Structural map of the chapter

- descent methods and line search
- Newton steps from quadratic approximation
- backtracking and damped Newton
- self-concordance
- explicit complexity bounds for Newton's method

## Theorem and derivation spine

### Newton step from the quadratic model

The local quadratic approximation at $x$ is
$$\hat f_x(v)=f(x)+\nabla f(x)^\trans v + \frac{1}{2} v^\trans \nabla^2 f(x) v.$$

Minimizing the quadratic model gives the Newton step
$$\Delta x_{\mathrm{nt}} = -\nabla^2 f(x)^{-1}\nabla f(x).$$

That formula is the reason Newton's method naturally rescales by curvature instead of suffering from the same zigzag behavior as poorly conditioned first-order descent.

### Newton decrement

The chapter defines
$$\lambda(x)=\sqrt{\nabla f(x)^\trans \nabla^2 f(x)^{-1}\nabla f(x)}.$$

This quantity is not just a convenience. It is:

- an affine-invariant measure of local suboptimality
- the natural stopping statistic for Newton's method
- the quantity that enters the self-concordance complexity bounds

### Self-concordance

In one dimension, a convex function is self-concordant if
$$\abs{f'''(x)} \le 2\paren{f''(x)}^{3/2}.$$

In several dimensions, this must hold along every line. The book emphasizes why this class matters:

- many logarithmic barrier functions are self-concordant
- the property is affine invariant
- the Newton analysis becomes explicit, without unknown Lipschitz constants

### Suboptimality bound via Newton decrement

For strictly convex self-concordant $f$, if $\lambda(x)<1$, the chapter derives a bound of the form
$$p^\star \ge f(x)+\lambda(x)+\log\paren{1-\lambda(x)},$$
and hence, for $\lambda(x)\le 0.68$,
$$f(x)-p^\star \le \lambda(x)^2.$$

This is the clean durable statement: once the Newton decrement is small, the objective gap is provably small.

### Quadratic local phase

After entering the small-decrement regime, the decrement contracts essentially quadratically:
$$\lambda(x^+) \lesssim \lambda(x)^2.$$

That is the real source of Newton's practical speed near the optimum.

## Failure modes and misuse points

- applying Newton's method where Hessians are indefinite or too noisy to trust
- using raw gradient norm as if it were coordinate-free stopping logic
- ignoring conditioning and then blaming the algorithm
- reading self-concordance as a generic smoothness condition; it is a stronger and more geometric object

## Quant research relevance

This chapter matters for:

- second-order likelihood optimization
- barrier and interior-point methods
- solver diagnostics and stopping rules
- distinguishing bad conditioning from weak algorithms

## What should be promoted out of this source note

- [[Gradient Descent and Preconditioning]]
- a durable note on Newton decrement and self-concordance

## Related notes

- [[Convex Optimization]]
- [[Interior-Point Methods]]
- [[Gradient Descent and Preconditioning]]
- [[Convex Optimization Methods]]

## Sources

- [[Convex Optimization]]
- [[raw/math_statistics/Boyd and Vandenberghe, Convex Optimization.pdf]]
