---
title: Arbitrage Theory in Continuous Time - Ch 21 Martingale Models for the Short Rate
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - fixed-income
  - short-rate
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: toc_scan_plus_utf8_text_extraction_and_targeted_rendered_theorem_pages
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 21 Martingale Models for the Short Rate
parent_source: "[[Arbitrage Theory in Continuous Time]]"
sources:
  - "[[Arbitrage Theory in Continuous Time]]"
  - "[[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]"
---
# Arbitrage Theory in Continuous Time - Ch 21 Martingale Models for the Short Rate

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: theorem-level extraction completed for positivity in CIR-type models, affine term structures, and tractable bond-pricing formulas for classical short-rate models.

## Deepening Targets

- If a dedicated fixed-income branch is built later, deepen the model-comparison section across Vasicek, Ho-Lee, CIR, and Hull-White.

## Deepened Subparts

- `21.1` Q-dynamics
- `21.2` properties of short-rate models
- `21.4` affine term structures
- `21.5` analytical results for standard models

## Role of the chapter

This chapter turns the general short-rate framework into concrete tractable model families.

## Core mathematical objects

- Vasicek, CIR, Ho-Lee, and Hull-White dynamics
- positivity condition for CIR-type models
  $$
  2b\ge \sigma^2
  $$
- affine bond-pricing form
  $$
  p(t,T)=A(t,T)e^{-B(t,T)r_t}
  $$

## Structural map of the chapter

- specify short-rate dynamics under the martingale measure
- compare linear, mean-reverting, lognormal, and square-root classes
- derive affine term-structure formulas
- compute closed-form bond prices and bond-option results for standard models

## Theorem and derivation spine

### Positivity is model-specific, not automatic

The chapter's CIR positivity result shows that square-root diffusions can remain strictly positive under the condition
$$
2b\ge \sigma^2.
$$

That matters because negative-rate exclusion is not free; it must be built into the chosen dynamics.

### Affine term structure is the tractability class

The chapter's main reusable theorem is the affine bond-pricing form
$$
p(t,T)=A(t,T)e^{-B(t,T)r_t},
$$
with model-specific Riccati-type equations or closed forms for $A$ and $B$.

That form is why Vasicek, CIR, and Hull-White stay central in rates work despite their limitations.

## Failure modes and misuse points

- assuming positivity because the rate is called "CIR-like"
- confusing statistical realism with analytic tractability
- forgetting which measure the short-rate dynamics are written under

## Quant research relevance

This chapter is the reusable rates core for:

- bond pricing
- bond options
- calibration discussions
- comparing affine short-rate models with HJM or market-model approaches

## What should be promoted out of this source note

- refresh [[Term-Structure Models]]
- potential future note on affine term-structure models

## Related notes

- [[Term-Structure Models]]
- [[Heath-Jarrow-Morton Drift Condition]]
- [[LIBOR Market Models]]

## Sources

- [[Arbitrage Theory in Continuous Time]]
- [[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]

