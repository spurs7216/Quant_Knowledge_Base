---
title: Time Series Analysis by State Space Methods - Ch 01 Introduction
type: source
status: chapter_ingested
updated: 2026-04-21
tags:
  - source
  - state-space
  - time-series
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: chapter_scan
extraction_basis: chapter_opening_plus_section_map
technical_depth: moderate
ingest_stage: scan
chapter_or_section: Ch 01 Introduction
parent_source: "[[Time Series Analysis by State Space Methods]]"
sources:
  - "[[Time Series Analysis by State Space Methods]]"
  - "[[raw/math_statistics/Time Series Analysis by State Space Methods (2012).pdf]]"
---
# Time Series Analysis by State Space Methods - Ch 01 Introduction

## Ingest Scope and Depth

- Ingest stage: `scan`
- Pass 1: chapter scan completed from the chapter opening and full section map.
- Pass 2: this chapter was not selected for theorem-level deepening.

## Role of the chapter

This chapter is the orientation layer of the monograph. It tells the reader how the book is organized and why the authors start from the local-level model instead of throwing the full general state-space model at the reader immediately.

## Section map

- basic ideas of state space analysis
- linear models
- non-Gaussian and nonlinear models
- prior knowledge
- notation
- other books on state space methods
- website for the book

## What the chapter is really doing

### 1. It frames state-space analysis as a unified methodology

The chapter defines the core stance of the book:

- there is an unobserved state process
- observations are generated from that hidden process
- the main task is to infer state properties, forecast, extract signal, and estimate parameters from observed data

### 2. It explains the pedagogical design

The authors explicitly begin with the local-level model so that filtering, smoothing, initialization, and forecasting become conceptually clear before the notation becomes heavy. That matters for the vault because it identifies Chapter 2 as the real conceptual gateway.

### 3. It sets the two-part architecture

The book is split into:

- a linear-Gaussian core where classical, minimum-variance, and Bayesian formulations converge to the same formulas
- a nonlinear / non-Gaussian extension layer handled by approximate or simulation-based methods

## Worth attending later

- the rationale for beginning from the local-level model
- the distinction between linear-Gaussian and nonlinear / non-Gaussian treatments
- the claim that state-space form is broader than Box-Jenkins style modeling rather than opposed to it

## Quant relevance

For quant work, the main value of this chapter is strategic: it clarifies that the book is not an applied cookbook but a state-space framework source.

## Promotion candidates

- none from this chapter directly

## Related notes

- [[Time Series Analysis by State Space Methods]]
- [[State Space Models]]
- [[Kalman Filtering]]

## Sources

- [[Time Series Analysis by State Space Methods]]
- [[raw/math_statistics/Time Series Analysis by State Space Methods (2012).pdf]]
