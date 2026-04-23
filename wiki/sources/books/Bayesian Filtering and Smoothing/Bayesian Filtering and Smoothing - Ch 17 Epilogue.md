---
title: Bayesian Filtering and Smoothing - Ch 17 Epilogue
type: source
status: chapter_ingested
updated: 2026-04-21
tags:
  - source
  - bayesian
  - method-selection
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: chapter_scan
extraction_basis: contents_plus_selected_chapter_text
technical_depth: light
ingest_stage: scan
chapter_or_section: Ch 17 Epilogue
parent_source: "[[Bayesian Filtering and Smoothing]]"
sources:
  - "[[Bayesian Filtering and Smoothing]]"
  - "[[raw/math_statistics/Simo Särkkä and Lennart Svensson, Bayesian Filtering and Smoothing.pdf]]"
---
# Bayesian Filtering and Smoothing - Ch 17 Epilogue

## Ingest Scope and Depth

- Ingest stage: `scan`
- Pass 1: full chapter scan completed.
- Pass 2: no deeper extraction applied. This chapter is a method-selection and outlook chapter.

## Role of the chapter

This chapter closes the source by turning the method zoo into decision guidance.

## Section map

- which method should I choose?
- further topics

## Main contributions from the scan pass

- Linear-Gaussian models remain the clean default when they are adequate.
- Gaussian approximation methods are appropriate when nonlinear structure is moderate and posterior shape stays reasonably unimodal.
- Particle methods become the serious option when the posterior geometry is too nonlinear, discrete, heavy-tailed, or multimodal for Gaussian approximations.
- Parameter estimation should generally be aligned with the inference family used in the final application.

## Why it remains scan-level

The chapter is mostly synthesis and outlook. Its durable value lies in guiding later method choice rather than introducing new technical objects.

## Quant relevance

This chapter matters because it prevents method shopping by fashion alone. It forces the question: what approximation family is actually justified by the model and data geometry?

## Promotion candidates

- none yet; the chapter mainly informs routing between existing durable notes

## Related notes

- [[Bayesian Filtering and Smoothing]]
- [[General Gaussian Filtering and Smoothing]]
- [[Particle Filtering]]
- [[Particle Smoothing]]
- [[Parameter Estimation in State Space Models]]

## Sources

- [[Bayesian Filtering and Smoothing]]
- [[raw/math_statistics/Simo Särkkä and Lennart Svensson, Bayesian Filtering and Smoothing.pdf]]
