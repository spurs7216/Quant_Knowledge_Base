---
title: Probability Theory The Logic of Science - Ch 02 The Quantitative Rules
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - probability
  - bayesian
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: chapter_start_and_rule-derivation scan via pymupdf
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 02 The Quantitative Rules
parent_source: "[[Probability Theory The Logic of Science]]"
sources:
  - "[[Probability Theory The Logic of Science]]"
  - "[[raw/math_statistics/Probability Theory The Logic of Science.pdf]]"
---
# Probability Theory The Logic of Science - Ch 02 The Quantitative Rules

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: deepened the consistency-based derivation of the product and sum rules.

## Role of the chapter

This is the mathematical birth of the book's thesis. Plausibility calculus becomes probability calculus once consistency, qualitative common sense, and numerical representation are imposed.

## Core mathematical objects

- plausibility assignments
- logical conjunction `AB`
- negation `\neg A`
- conditional plausibility

## Theorem and derivation spine

The chapter's main result is that consistency forces the core probability rules:

$$\Prob(AB \mid C)=\Prob(A \mid BC)\Prob(B \mid C)=\Prob(B \mid AC)\Prob(A \mid C)$$

and

$$\Prob(A \mid B)+\Prob(\neg A \mid B)=1.$$

These imply the extended sum rule:

$$\Prob(A+B \mid C)=\Prob(A \mid C)+\Prob(B \mid C)-\Prob(AB \mid C).$$

The durable point is not only that the rules work. It is that they are justified by consistency constraints, not by appeal to repeated random experiments.

## Why this matters later

Everything Bayesian that follows is downstream of these two rules. Bayes' theorem, predictive updating, evidence comparison, and decision theory are all corollaries of this base layer.

## Failure modes and misuse points

- using the rules mechanically without keeping the conditioning information explicit
- forgetting that the same proposition can have different plausibility under different background information
- treating Bayes' theorem as separate from the product rule

## Quant research relevance

This chapter is foundational for all later inference in the vault: model updating, signal revision, risk learning, and evidence integration.

## What should be promoted out of this source note

- [[Probability as Extended Logic]]

## Related notes

- [[Probability Theory The Logic of Science]]
- [[Probability as Extended Logic]]
- [[Maximum Entropy Principle]]

## Sources

- [[Probability Theory The Logic of Science]]
- [[raw/math_statistics/Probability Theory The Logic of Science.pdf]]
