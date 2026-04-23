---
title: Probability Theory The Logic of Science - Ch 04 Elementary Hypothesis Testing
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - statistics
  - bayesian
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: chapter scan and prior/posterior testing sections via pymupdf
technical_depth: selective_deepen
ingest_stage: selective_deepen
chapter_or_section: Ch 04 Elementary Hypothesis Testing
parent_source: "[[Probability Theory The Logic of Science]]"
sources:
  - "[[Probability Theory The Logic of Science]]"
  - "[[raw/math_statistics/Probability Theory The Logic of Science.pdf]]"
---
# Probability Theory The Logic of Science - Ch 04 Elementary Hypothesis Testing

## Ingest Scope and Depth

- Ingest stage: `selective_deepen`
- Pass 1: full chapter scan completed.
- Pass 2: selected the posterior-testing logic and prior-probability emphasis.

## Role of the chapter

This chapter states the book's working rule for testing: evaluate the posterior plausibility of hypotheses given all the evidence, not only a tail-area summary.

## Core objects

- prior odds
- likelihood ratio
- posterior odds
- all available evidence `E_1,E_2,\dots`

## Selected technical spine

The durable formula is posterior odds:

$$\frac{\Prob(H_1 \mid D,I)}{\Prob(H_0 \mid D,I)}=\frac{\Prob(H_1 \mid I)}{\Prob(H_0 \mid I)}\cdot \frac{\Prob(D \mid H_1,I)}{\Prob(D \mid H_0,I)}.$$

Jaynes' insistence is that no honest test may discard relevant prior information or side information.

## Failure modes and misuse points

- pretending prior odds are irrelevant
- replacing posterior comparison with significance ritual
- treating test output as action without a loss model

## Quant research relevance

This chapter matters whenever a quant hypothesis must be judged by combined evidence rather than one stylized p-value.

## Related notes

- [[Probability Theory The Logic of Science]]
- [[Statistical Decision Theory]]
- [[Bayesian Model Comparison and Occam Factors]]

## Sources

- [[Probability Theory The Logic of Science]]
- [[raw/math_statistics/Probability Theory The Logic of Science.pdf]]
