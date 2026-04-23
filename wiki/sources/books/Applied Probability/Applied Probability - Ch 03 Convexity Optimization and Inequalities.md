---
title: Applied Probability - Ch 03 Convexity Optimization and Inequalities
type: source
status: chapter_ingested
updated: 2026-04-20
tags:
  - source
  - probability
  - optimization
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: chapter_scan
extraction_basis: chapter_scan_plus_selected_subparts
technical_depth: moderate
ingest_stage: selective_deepen
chapter_or_section: Ch 03 Convexity Optimization and Inequalities
parent_source: "[[Applied Probability]]"
sources:
  - "[[Applied Probability]]"
  - "[[raw/math_statistics/Applied Probability.pdf]]"
---
# Applied Probability - Ch 03 Convexity Optimization and Inequalities

## Ingest Scope and Depth

- Ingest stage: `selective_deepen`
- Pass 1: full chapter scan completed.
- Pass 2: local deepening applied to convexity tests, Jensen-style reasoning, the MM algorithm, and the inequality spine around Schlomilch and Holder.

## Role of the chapter

This chapter is where the book stops treating probability as only distribution algebra and starts treating it as a source of optimization and inequality structure. It is the main bridge from stochastic modeling to reusable optimization logic.

## Section map

- convex functions
- minimization of convex functions
- the MM algorithm
- moment inequalities

## Locally deepened subparts

### 1. Convexity is the reason minimization can be trusted

The chapter emphasizes that strict convexity gives uniqueness of the minimum and that convexity can be recognized through multiple equivalent tests. That is the structural reason optimization becomes manageable rather than a numerical guessing game.

### 2. The MM algorithm is the chapter's most reusable procedural contribution

The MM idea is to replace a hard objective by a surrogate that majorizes or minorizes it and is easier to optimize. That pattern reappears later in estimation, EM-style methods, and iterative statistical optimization.

### 3. Jensen is the engine, not a decorative inequality

Jensen's inequality drives the chapter's treatment of weighted means and Holder-style inequalities. The durable point is that convexity translates random averages into deterministic bounds in a way that later controls approximation, optimization, and concentration.

## Scan-level remainder

- Bernstein's proof of Weierstrass approximation is intellectually interesting but not central to the vault's next-step quant priorities
- the chapter contains many worked inequalities, but the most reusable objects are convexity, MM, and Jensen rather than every individual example

## Quant relevance

This chapter matters for:

- surrogate optimization in estimation algorithms
- risk and moment inequalities
- regularized objective design
- understanding why convex structure makes large models computationally tractable

## Promotion candidates

- a refresh to [[Convex Optimization Methods]]
- a dedicated note on Jensen and surrogate optimization

## Related notes

- [[Applied Probability]]
- [[Convex Optimization Methods]]
- [[Gradient Descent and Preconditioning]]

## Sources

- [[Applied Probability]]
- [[raw/math_statistics/Applied Probability.pdf]]
