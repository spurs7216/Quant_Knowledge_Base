---
title: Applied Probability - Ch 09 Branching Processes
type: source
status: chapter_ingested
updated: 2026-04-20
tags:
  - source
  - probability
  - branching-processes
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: chapter_scan
extraction_basis: chapter_scan_plus_selected_subparts
technical_depth: moderate
ingest_stage: selective_deepen
chapter_or_section: Ch 09 Branching Processes
parent_source: "[[Applied Probability]]"
sources:
  - "[[Applied Probability]]"
  - "[[raw/math_statistics/Applied Probability.pdf]]"
---
# Applied Probability - Ch 09 Branching Processes

## Ingest Scope and Depth

- Ingest stage: `selective_deepen`
- Pass 1: full chapter scan completed.
- Pass 2: local deepening applied to generating-function evolution, extinction fixed points, multitype criticality, and the reproduction-number logic in the HIV example.

## Role of the chapter

This chapter studies recursively reproducing random systems. Its central questions are not parameter estimation questions but structural ones:

- does the process die out?
- does it grow?
- what determines the critical threshold?

## Section map

- examples of branching processes
- elementary theory
- extinction
- immigration
- multitype branching processes
- viral reproduction in HIV
- basic reproduction numbers

## Locally deepened subparts

### 1. Generating functions encode the full one-generation update

The chapter repeatedly uses progeny generating functions because they translate reproduction rules into fixed-point and recursion problems.

### 2. Extinction is a fixed-point problem, not only a simulation outcome

The ultimate extinction probability is characterized as a solution of algebraic equations derived from the generating function. That makes criticality analyzable before running any simulation.

### 3. Multitype branching replaces a scalar mean by spectral structure

In the multitype setting, criticality depends on the dominant eigenvalue of the offspring-mean structure rather than on a single scalar mean.

### 4. Basic reproduction numbers are the chapter's main applied takeaway

The HIV section makes the point explicit: `R_0` is a structural threshold. Below it extinction is certain; above it extinction is no longer guaranteed.

## Scan-level remainder

- many biological examples were scanned but not extracted at theorem depth
- immigration and some multitype details remain source-bound until the vault needs a dedicated branching-process note

## Quant relevance

This chapter is useful for thinking about:

- contagion and cascade models
- extinction versus explosion thresholds
- recursive growth under uncertainty
- rare-event and epidemic-style propagation analogies

## Promotion candidates

- branching processes

## Related notes

- [[Applied Probability]]
- [[Applied Probability - Ch 10 Martingales]]
- [[Poisson Processes]]

## Sources

- [[Applied Probability]]
- [[raw/math_statistics/Applied Probability.pdf]]
