---
title: Bayesian Filtering and Smoothing - Ch 03 Batch and Recursive Bayesian Estimation
type: source
status: chapter_ingested
updated: 2026-04-21
tags:
  - source
  - bayesian
  - recursion
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: chapter_scan
extraction_basis: contents_plus_preface_and_chapter_intro
technical_depth: light
ingest_stage: scan
chapter_or_section: Ch 03 Batch and Recursive Bayesian Estimation
parent_source: "[[Bayesian Filtering and Smoothing]]"
sources:
  - "[[Bayesian Filtering and Smoothing]]"
  - "[[raw/math_statistics/Simo Särkkä and Lennart Svensson, Bayesian Filtering and Smoothing.pdf]]"
---
# Bayesian Filtering and Smoothing - Ch 03 Batch and Recursive Bayesian Estimation

## Ingest Scope and Depth

- Ingest stage: `scan`
- Pass 1: full chapter scan completed.
- Pass 2: no full theorem-level extraction. The chapter functions mainly as a bridge from regression algebra to recursive state estimation.

## Role of the chapter

This chapter shows that recursive Bayesian estimation is not a mysterious new object. It grows naturally out of linear regression once observations arrive sequentially and parameters are allowed to drift.

## Section map

- batch linear regression
- recursive linear regression
- batch versus recursive estimation
- drift model for linear regression
- state space model for linear regression with drift
- toward Bayesian filtering and smoothing

## Main contributions from the scan pass

- Recursive estimation is presented as a sequential alternative to repeatedly resolving an expanding batch problem.
- The drift-model sections create a clean bridge from regression to state-space modeling.
- The chapter prepares the reader to see filtering as a recursive Bayesian update over latent states rather than as a separate topic.

## Why it remains scan-level

The chapter is foundational as a bridge, but the later filtering chapters carry the reusable recursions and approximation logic the vault needs most.

## Quant relevance

This chapter matters for:

- recursive least-squares intuition
- time-varying-parameter regression
- seeing dynamic models as structured sequential estimation problems

## Promotion candidates

- later state-space regression or dynamic-parameter notes

## Related notes

- [[Bayesian Filtering and Smoothing]]
- [[Kalman Filtering]]
- [[Least Squares and Pseudoinverse]]
- [[State Space Models]]

## Sources

- [[Bayesian Filtering and Smoothing]]
- [[raw/math_statistics/Simo Särkkä and Lennart Svensson, Bayesian Filtering and Smoothing.pdf]]
