---
title: Applied Probability - Ch 02 Calculation of Expectations
type: source
status: chapter_ingested
updated: 2026-04-20
tags:
  - source
  - probability
  - expectation
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: chapter_scan
extraction_basis: chapter_scan_plus_selected_subparts
technical_depth: moderate
ingest_stage: selective_deepen
chapter_or_section: Ch 02 Calculation of Expectations
parent_source: "[[Applied Probability]]"
sources:
  - "[[Applied Probability]]"
  - "[[raw/math_statistics/Applied Probability.pdf]]"
---
# Applied Probability - Ch 02 Calculation of Expectations

## Ingest Scope and Depth

- Ingest stage: `selective_deepen`
- Pass 1: full chapter scan completed.
- Pass 2: local deepening applied to indicator-variable methods, conditioning recurrences, transform composition, tail-integral formulas, and the reduction-of-degree bridge to Stein-Chen methods.

## Role of the chapter

This chapter is the calculation toolkit behind much of the book. Its message is simple: expectation is not a statistic to compute at the end. It is the main operator that turns random structure into usable algebra.

## Section map

- indicator random variables and symmetry
- conditioning
- moment transforms
- tail probability methods
- moments of reciprocals and ratios
- reduction of degree
- spherical surface measure
- Dirichlet distribution

## Locally deepened subparts

### 1. Indicator variables turn counting into linearity of expectation

The opening section repeatedly rewrites complicated counts as sums of indicators. The durable lesson is that expectation of a count is often easy even when the exact distribution of the count is not.

### 2. Conditioning is a recurrence engine

Several examples use conditioning to derive recursive equations for expectations and probabilities. That is a durable pattern for stochastic-process work: condition on the next event, then solve the resulting recursion or differential relation.

### 3. Transform composition handles compounding cleanly

The moment-transform section emphasizes that generating functions and related transforms compose naturally under random sums. This is one of the cleanest routes from static distribution algebra into process calculations.

### 4. Tail-integral formulas and reduction of degree are more reusable than they look

The tail-probability section rewrites moments as tail integrals. Later in the chapter, the reduction-of-degree arguments connect expectation identities to approximation theory and the Stein-Chen style machinery used again in Chapter 14.

## Scan-level remainder

- the spherical surface measure section is useful but not central to the current vault spine
- the Dirichlet section is mathematically valuable, but it was not promoted yet because the vault currently needs the process chapters more urgently

## Quant relevance

This chapter is useful whenever a quant problem is easier through expectation identities than through full distributional derivation:

- expected event counts
- recursive stopping calculations
- compounding and transform algebra
- moment bounds and tail-based summaries

## Promotion candidates

- expectation and transform methods
- Poisson approximation

## Related notes

- [[Applied Probability]]
- [[Applied Probability - Ch 14 Poisson Approximation]]
- [[Maximum Likelihood Estimation]]
- [[Convergence and Limit Theory]]

## Sources

- [[Applied Probability]]
- [[raw/math_statistics/Applied Probability.pdf]]
