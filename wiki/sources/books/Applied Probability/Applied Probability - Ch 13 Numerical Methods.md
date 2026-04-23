---
title: Applied Probability - Ch 13 Numerical Methods
type: source
status: chapter_ingested
updated: 2026-04-20
tags:
  - source
  - probability
  - numerical-methods
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: chapter_scan
extraction_basis: chapter_scan_plus_selected_subparts
technical_depth: moderate
ingest_stage: selective_deepen
chapter_or_section: Ch 13 Numerical Methods
parent_source: "[[Applied Probability]]"
sources:
  - "[[Applied Probability]]"
  - "[[raw/math_statistics/Applied Probability.pdf]]"
---
# Applied Probability - Ch 13 Numerical Methods

## Ingest Scope and Depth

- Ingest stage: `selective_deepen`
- Pass 1: full chapter scan completed.
- Pass 2: local deepening applied to equilibrium-distribution computation, Fourier-based convolution and jump counting, stochastic simulation with intensity leaping, and numerical approximation of diffusion processes.

## Role of the chapter

This chapter is the computational counterpart to the earlier process theory. Once transition laws, generators, or first-passage objects are written down, this chapter asks how to actually compute with them.

## Section map

- computation of equilibrium distributions
- applications of the finite Fourier transform
- counting jumps in a Markov chain
- stochastic simulation and intensity leaping
- a numerical method for diffusion processes

## Locally deepened subparts

### 1. Stationary laws can be computed iteratively

The opening section treats power, Jacobi, Gauss-Seidel, and block Gauss-Seidel approaches for equilibrium distributions. The durable lesson is that stationary laws are linear-algebra objects, not only symbolic formulas.

### 2. FFT methods make convolution and renewal calculations practical

The finite Fourier transform section turns repeated convolutions and renewal-style equations into `O(n log n)` computations. That is the chapter's most reusable algorithmic theme.

### 3. Simulation of jump processes needs approximation discipline

The stochastic-simulation section moves beyond exact one-event-at-a-time simulation and discusses intensity-leaping ideas that trade exactness for speed. That is the right computational mindset for large event-driven systems.

### 4. Diffusion models need discretization, not only formulas

The diffusion section is a reminder that continuous-time models become implementable through state-space discretization and numerical propagation, not only through elegant analytic equations.

## Scan-level remainder

- the chapter contains several application-specific worked examples that remain source-bound for now
- no single numerical routine was promoted yet because the vault currently needs the conceptual process notes first

## Quant relevance

This chapter matters for:

- stationary-distribution computation
- fast convolution and renewal problems
- event-driven simulation
- numerical approximation of diffusion-style models

## Promotion candidates

- numerical methods for stochastic processes

## Related notes

- [[Applied Probability]]
- [[Applied Probability - Ch 08 Continuous-Time Markov Chains]]
- [[Applied Probability - Ch 11 Diffusion Processes]]
- [[Monte Carlo Methods]]

## Sources

- [[Applied Probability]]
- [[raw/math_statistics/Applied Probability.pdf]]
