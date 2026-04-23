---
title: Convex Optimization - Ch 10 Equality Constrained Minimization
type: source
status: chapter_ingested
updated: 2026-04-21
tags:
  - source
  - optimization
  - convex-optimization
  - chapter-digest
  - algorithms
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: chapter_text_plus_section_map_plus_kkt_linear_system_sections
technical_depth: mixed
ingest_stage: selective_deepen
chapter_or_section: Ch 10 Equality Constrained Minimization
parent_source: "[[Convex Optimization]]"
sources:
  - "[[Convex Optimization]]"
  - "[[raw/math_statistics/Boyd and Vandenberghe, Convex Optimization.pdf]]"
---
# Convex Optimization - Ch 10 Equality Constrained Minimization

## Ingest Scope and Depth

- Ingest stage: `selective_deepen`
- Pass 1: full chapter scan completed.
- Pass 2: local deepening completed around equality-constrained Newton steps, infeasible-start Newton, and the KKT linear-system structure.

## Why this chapter still matters

This chapter is narrower than Chapters 9 and 11, but it provides the clean bridge from unconstrained Newton methods to constrained solver systems.

## Core objects

- equality-constrained problem
- feasible and infeasible Newton step
- KKT linear system
- primal residual
- dual residual
- line search under equality structure

## Structural map

- equality constrained convex problems
- Newton's method with equality constraints
- infeasible-start Newton method
- implementation

## What the chapter is really doing

### 1. Equality constraints turn Newton updates into linear saddle-point systems

The main lesson is structural: once equalities are present, the Newton step is no longer just a curvature-rescaled gradient step. It becomes a coupled system for primal and multiplier variables.

### 2. Feasibility and optimality residuals should be tracked separately

The infeasible-start method is valuable because it teaches the reader to distinguish primal feasibility from stationarity rather than collapsing both into one vague convergence notion.

### 3. This chapter is the local algebra behind later interior-point methods

The numerical structure here is the immediate precursor to the primal-dual linear systems solved in Chapter 11.

## Quant relevance

This chapter matters when:

- portfolio or exposure constraints are enforced exactly
- one needs to understand the KKT system solved by second-order methods
- solver diagnostics should separate feasibility failure from poor descent

## Promotion candidates

- [[Convex Duality and KKT Conditions]]
- equality-constrained Newton systems and KKT linear algebra

## Related notes

- [[Convex Optimization]]
- [[Convex Optimization - Ch 05 Duality]]
- [[Convex Optimization - Ch 09 Unconstrained Minimization]]
- [[Interior-Point Methods]]

## Sources

- [[Convex Optimization]]
- [[raw/math_statistics/Boyd and Vandenberghe, Convex Optimization.pdf]]
