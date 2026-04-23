---
title: Probability Theory The Logic of Science - Ch 17 Principles and Pathology of Orthodox Statistics
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
extraction_basis: chapter-start and selected critique sections via pymupdf
technical_depth: medium
ingest_stage: selective_deepen
chapter_or_section: Ch 17 Principles and Pathology of Orthodox Statistics
parent_source: "[[Probability Theory The Logic of Science]]"
sources:
  - "[[Probability Theory The Logic of Science]]"
  - "[[raw/math_statistics/Probability Theory The Logic of Science.pdf]]"
---
# Probability Theory The Logic of Science - Ch 17 Principles and Pathology of Orthodox Statistics

## Ingest Scope and Depth

- Ingest stage: `selective_deepen`
- Pass 1: full chapter scan completed.
- Pass 2: deepened the chapter's critique of significance testing, sample reuse, and hidden loss assumptions.

## Role of the chapter

This chapter is Jaynes' direct attack on orthodox procedures. The main claim is not that frequentist tools are always numerically useless, but that they often solve the wrong logical problem and then hide that mismatch behind ritual vocabulary.

## Core objects

- significance level
- rejection region
- confidence procedure
- likelihood principle
- stopping rule

## Key results

The load-bearing point is conceptual: procedures built around long-run sampling behavior do not automatically answer the scientist's or trader's actual question about the current hypothesis, parameter, or model.

Jaynes' recurring pathologies are:

- treating fixed rejection thresholds as if they were evidence measures
- allowing stopping rules to dominate inference when the realized data are unchanged
- handling nuisance parameters through procedural tricks instead of integration
- pretending objectivity by refusing to state priors or loss functions explicitly

## Why this matters later

The chapter sharpens the need for Bayesian model comparison and posterior decision rules. It also explains why likelihood, evidence, and posterior odds keep reappearing as the book's preferred inferential currency.

## Failure modes and misuse points

- reading a p-value as a posterior probability
- treating confidence coverage as a belief statement about one realized interval
- using orthodox procedures for model comparison without a coherent penalty for complexity

## Quant research relevance

In quant research this critique hits common bad habits directly: p-hacked factor screening, data-dependent stopping, interval statements with no conditioning clarity, and model-selection pipelines that treat significance as sufficient evidence.

## What should be promoted out of this source note

- a durable note on why evidence measures differ from significance procedures

## Related notes

- [[Probability Theory The Logic of Science]]
- [[Bayesian Model Comparison and Occam Factors]]
- [[Statistical Decision Theory]]

## Sources

- [[Probability Theory The Logic of Science]]
- [[raw/math_statistics/Probability Theory The Logic of Science.pdf]]
