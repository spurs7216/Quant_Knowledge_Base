---
title: Probability Theory The Logic of Science - Ch 07 The Central Gaussian, or Normal, Distribution
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - probability
  - statistics
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: chapter scan and central-limit / Gaussian-convolution sections via pymupdf
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 07 The Central Gaussian, or Normal, Distribution
parent_source: "[[Probability Theory The Logic of Science]]"
sources:
  - "[[Probability Theory The Logic of Science]]"
  - "[[raw/math_statistics/Probability Theory The Logic of Science.pdf]]"
---
# Probability Theory The Logic of Science - Ch 07 The Central Gaussian, or Normal, Distribution

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: deepened the Gaussian's role in inference, convolution, and asymptotic approximation.

## Role of the chapter

This chapter is Jaynes' explanation of why Gaussian structure keeps reappearing in inference. The point is not blind reverence for Normality. The point is that repeated aggregation, local curvature, and information concentration often drive posteriors and errors toward Gaussian form.

## Core mathematical objects

- Gaussian density
  $$p(x)\propto \exp\paren{-\frac{(x-\mu)^2}{2\sigma^2}}$$
- convolution of Gaussians
- central-limit behavior
- asymptotic posterior approximation

## Theorem and derivation spine

The chapter's durable claims are:

- Gaussians are stable under convolution
- many posterior or error distributions become approximately Gaussian as information accumulates
- local quadratic expansion of log-density is a key route to Gaussian approximation

That is why Gaussian approximations are often useful even when the data-generating mechanism is not literally Gaussian.

## Failure modes and misuse points

- treating Gaussian assumptions as metaphysical truth rather than approximation
- invoking the central limit theorem without checking dependence, tail behavior, or information regime
- forgetting that Gaussianity can be a posterior or aggregate consequence rather than a primitive assumption

## Quant research relevance

This chapter matters for asymptotic estimator geometry, Kalman-style linear-Gaussian models, approximate posteriors, and error propagation in measurement systems.

## What should be promoted out of this source note

- a durable note on Gaussian approximation and posterior concentration

## Related notes

- [[Probability Theory The Logic of Science]]
- [[Convergence and Limit Theory]]
- [[Kalman Filtering]]

## Sources

- [[Probability Theory The Logic of Science]]
- [[raw/math_statistics/Probability Theory The Logic of Science.pdf]]
