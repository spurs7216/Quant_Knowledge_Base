---
title: Applied Probability - Ch 01 Basic Notions of Probability Theory
type: source
status: chapter_ingested
updated: 2026-04-20
tags:
  - source
  - probability
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: chapter_scan
extraction_basis: chapter_scan_plus_section_map
technical_depth: moderate
ingest_stage: scan
chapter_or_section: Ch 01 Basic Notions of Probability Theory
parent_source: "[[Applied Probability]]"
sources:
  - "[[Applied Probability]]"
  - "[[raw/math_statistics/Applied Probability.pdf]]"
---
# Applied Probability - Ch 01 Basic Notions of Probability Theory

## Ingest Scope and Depth

- Ingest stage: `scan`
- Pass 1: chapter scan completed from the full chapter text and section map.
- Pass 2: this chapter was not selected for theorem-level deepening because its main foundations overlap heavily with `[[All of Statistics]]`.

## Role of the chapter

This chapter builds the operating language of the rest of the book:

- probability and expectation
- conditional probability
- independence
- distributions and moments
- convolution
- random vectors and multivariate Normal structure

It is mostly a foundation reset rather than the most distinctive part of the source.

## Section map

- introduction
- probability and expectation
- conditional probability
- independence
- distributions, densities, and moments
- convolution
- random vectors
- multivariate Normal random vectors

## What the chapter is really doing

### 1. It fixes the probability vocabulary for later process chapters

The book does not linger on abstract measure theory, but it does make the basic objects explicit enough that later chapters can move quickly into Poisson, Markov, and diffusion models without redefining the language of random quantities.

### 2. It treats conditioning and independence as modeling devices

These are not only axioms. They are the structural assumptions that later determine whether arrival models, transition models, and filtering arguments actually factor in a tractable way.

### 3. It pushes toward multivariate structure early

The random-vector and multivariate Normal sections matter because later diffusion and process arguments repeatedly rely on Gaussian vectors and covariance structure rather than only on scalar random variables.

## Worth attending later

- the convolution section as a bridge from static laws to sums of increments
- the random-vector section as preparation for diffusion examples
- the multivariate Normal reminder because later Brownian arguments assume it

## Quant relevance

This chapter mainly prevents avoidable drift in notation and concepts before the book turns to process modeling. It is useful as a quick reset for:

- conditioning language
- independence claims
- convolution of shocks
- Gaussian-vector intuition

## Promotion candidates

- none from this scan pass

## Related notes

- [[Applied Probability]]
- [[All of Statistics]]
- [[All of Statistics - Ch 01 Probability]]
- [[All of Statistics - Ch 02 Random Variables]]

## Sources

- [[Applied Probability]]
- [[raw/math_statistics/Applied Probability.pdf]]
