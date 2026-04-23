---
title: Applied Probability - Ch 14 Poisson Approximation
type: source
status: chapter_ingested
updated: 2026-04-20
tags:
  - source
  - probability
  - approximation
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: chapter_scan
extraction_basis: chapter_scan_plus_selected_subparts
technical_depth: moderate
ingest_stage: selective_deepen
chapter_or_section: Ch 14 Poisson Approximation
parent_source: "[[Applied Probability]]"
sources:
  - "[[Applied Probability]]"
  - "[[raw/math_statistics/Applied Probability.pdf]]"
---
# Applied Probability - Ch 14 Poisson Approximation

## Ingest Scope and Depth

- Ingest stage: `selective_deepen`
- Pass 1: full chapter scan completed.
- Pass 2: local deepening applied to the Chen-Stein setup, the coupling bound, the neighborhood method, and the proof skeleton through the Stein equation.

## Role of the chapter

This chapter studies when a sum of rare, weakly dependent Bernoulli indicators can be treated as approximately Poisson with explicit error control.

## Section map

- applications of the coupling method
- applications of the neighborhood method
- proof of the Chen-Stein estimates

## Locally deepened subparts

### 1. The target is total-variation control, not vague asymptotics

The chapter measures approximation quality in total variation distance. That is stronger and more operational than a loose statement that something is "approximately Poisson."

### 2. Coupling gives one route to explicit error bounds

The coupling method constructs comparison variables whose difference from the target sum is controllable after forcing one indicator to be active.

### 3. Dependency neighborhoods give a second route

The neighborhood method exploits local dependency structure by identifying, for each indicator, the set of other indicators that actually matter for its dependence.

### 4. Stein's equation is the proof engine underneath both methods

The final section shows how the approximation bounds come from solving a special equation whose expectation vanishes exactly for Poisson laws.

## Scan-level remainder

- the many application examples were scanned but not extracted individually into separate notes
- the proof details remain source-bound until the vault needs a dedicated durable note on Poisson approximation

## Quant relevance

This chapter matters for:

- rare-event count approximation
- sparse default or jump-event settings
- explicit approximation error rather than heuristic distribution matching

## Promotion candidates

- Poisson approximation

## Related notes

- [[Applied Probability]]
- [[Applied Probability - Ch 06 Poisson Processes]]
- [[Poisson Processes]]

## Sources

- [[Applied Probability]]
- [[raw/math_statistics/Applied Probability.pdf]]
