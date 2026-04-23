---
title: Applied Probability - Ch 06 Poisson Processes
type: source
status: chapter_ingested
updated: 2026-04-20
tags:
  - source
  - probability
  - stochastic-processes
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: chapter_text_plus_key_definitions_and_propositions
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 06 Poisson Processes
parent_source: "[[Applied Probability]]"
sources:
  - "[[Applied Probability]]"
  - "[[raw/math_statistics/Applied Probability.pdf]]"
---
# Applied Probability - Ch 06 Poisson Processes

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: theorem-level extraction completed for thinning and splitting, characterization by infinitesimal postulates, waiting-time structure, transformations and marking, and Campbell's moment formulas.

## Why this chapter is load-bearing

This is the first chapter where the book fully turns probability into process theory. It supplies the canonical model for random arrivals in time or space and builds the algebra that later supports marked events, jump models, queueing, claims processes, and rare-event approximation.

## Core objects

- Poisson random variable with mean `mu`
- intensity function `lambda(x)`
- random points in a region `R`
- counting process `N(t)`
- arrival times `T_k` and interarrival times `W_k`
- transformed and marked point sets
- random sums over points `sum_{X in Pi} f(X)`

## Structural map

- the Poisson distribution
- characterization and construction
- one-dimensional processes
- transformations
- marking and coloring
- Campbell's formulas

## Theorem and derivation spine

### 1. Thinning and splitting preserve the Poisson class

The opening proposition shows that independently classifying the outcomes of a Poisson count splits it into independent Poisson counts. This is the finite-dimensional ancestor of coloring and marking the full process.

### 2. Infinitesimal postulates characterize the process

The chapter gives the usual small-region structure:

- disjoint counts are independent
- a single point arrives with probability `lambda(x) h + o(h)`
- two or more arrivals in a small region are `o(h)`

From those postulates, the count in a region is Poisson with mean equal to the integrated intensity over the region.

### 3. The homogeneous one-dimensional process is governed by exponential waiting

For the standard one-dimensional homogeneous process, the waiting time `T_k` to the `k`th arrival is Gamma and the interarrival times `W_k` are iid exponential. The lack-of-memory property of the exponential is not incidental. It is the time-domain expression of the process being Markovian in event counts.

### 4. Transformations, coloring, and marking preserve tractability

The chapter shows that transforming a Poisson process changes its intensity by the ordinary change-of-variables logic, and that independent coloring or marking produces new Poisson processes with derived intensities. This is the durable route from simple point processes to marked event models.

### 5. Campbell's formulas convert random sums into deterministic integrals

Campbell's formulas are the computational heart of the chapter. They turn sums over random points into expectations, variances, and transforms built from intensity integrals. This is what makes compound Poisson and shot-noise calculations tractable.

## Quant relevance

This chapter is directly relevant to:

- order arrivals and trade counts
- default and claim arrivals
- marked event processes with sizes, types, or categories
- jump-time construction inside larger stochastic models
- rare-event approximations that later feed Chapter 14

## Promotion candidates

- [[Poisson Processes]]
- Poisson approximation

## Related notes

- [[Applied Probability]]
- [[Applied Probability - Ch 08 Continuous-Time Markov Chains]]
- [[All of Statistics - Ch 23 Probability Redux Stochastic Processes]]
- [[Poisson Processes]]
- [[Stochastic Calculus]]

## Sources

- [[Applied Probability]]
- [[raw/math_statistics/Applied Probability.pdf]]
