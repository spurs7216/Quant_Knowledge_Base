---
title: Applied Probability - Ch 08 Continuous-Time Markov Chains
type: source
status: chapter_ingested
updated: 2026-04-20
tags:
  - source
  - probability
  - markov-chains
  - continuous-time
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: chapter_text_plus_key_definitions_and_propositions
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 08 Continuous-Time Markov Chains
parent_source: "[[Applied Probability]]"
sources:
  - "[[Applied Probability]]"
  - "[[raw/math_statistics/Applied Probability.pdf]]"
---
# Applied Probability - Ch 08 Continuous-Time Markov Chains

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: deep extraction completed for infinitesimal rates, backward equations, equilibrium via the generator, reversibility, matrix exponentials, and Kendall's birth-death-immigration process.

## Why this chapter is load-bearing

This chapter is the continuous-time extension of the Markov-chain language and one of the most important bridges toward stochastic calculus, queueing, and intensity-based modeling.

## Core objects

- finite-time transition probabilities `p_ij(t)`
- transition intensities `lambda_ij`
- total exit rate `lambda_i`
- infinitesimal generator `Lambda`
- matrix exponential `P(t) = e^{t Lambda}`
- equilibrium distribution `pi`
- detailed balance `pi_i lambda_ij = pi_j lambda_ji`
- birth, death, and immigration rates

## Structural map

- finite-time transition probabilities
- derivation of the backward equations
- equilibrium distributions and reversibility
- examples
- calculation of matrix exponentials
- Kendall's birth-death-immigration process

## Theorem and derivation spine

### 1. Continuous time replaces one-step probabilities by rates

The main conceptual move is simple but decisive: instead of asking for one-step transition probabilities, the model specifies exponential holding behavior and transition intensities away from the current state.

### 2. The generator drives finite-time evolution

The backward equations summarize the finite-time law in matrix form and lead to the matrix-exponential solution `P(t) = e^{t Lambda}`. This is the core algebraic identity of the chapter.

### 3. Stationarity becomes `pi Lambda = 0`

The discrete-time condition `pi = pi P` is replaced by the generator balance condition. That is the durable equilibrium equation for continuous-time chains.

### 4. Reversibility survives intact after replacing probabilities by rates

Detailed balance now reads `pi_i lambda_ij = pi_j lambda_ji`. The same constructive logic used in discrete time still works, but now it is expressed through probabilistic flow between states.

### 5. Matrix exponentials are not optional implementation detail

Even when the generator is known, extracting finite-time transition probabilities requires a matrix exponential or a numerical scheme equivalent to it. That is where the theoretical object becomes computational.

### 6. Infinite-state birth-death-immigration models connect generators to generating functions

Kendall's process shows how infinite-state chains require more than matrix algebra alone. Generating-function arguments and Poisson immigration structure become the main solution route.

## Quant relevance

This chapter matters for:

- intensity-based state models
- queueing and inventory-style systems
- credit-state and default-transition models
- continuous-time regime models
- the bridge from discrete Markov structure to diffusions and jump processes

## Promotion candidates

- [[Continuous-Time Markov Chains]]

## Related notes

- [[Applied Probability]]
- [[Applied Probability - Ch 07 Discrete-Time Markov Chains]]
- [[Applied Probability - Ch 11 Diffusion Processes]]
- [[Continuous-Time Markov Chains]]
- [[Markov Chains]]
- [[Stochastic Calculus]]

## Sources

- [[Applied Probability]]
- [[raw/math_statistics/Applied Probability.pdf]]
