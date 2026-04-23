---
title: Applied Probability - Ch 07 Discrete-Time Markov Chains
type: source
status: chapter_ingested
updated: 2026-04-20
tags:
  - source
  - probability
  - markov-chains
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: chapter_text_plus_key_definitions_and_propositions
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 07 Discrete-Time Markov Chains
parent_source: "[[Applied Probability]]"
sources:
  - "[[Applied Probability]]"
  - "[[raw/math_statistics/Applied Probability.pdf]]"
---
# Applied Probability - Ch 07 Discrete-Time Markov Chains

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: deep extraction completed for equilibrium structure, reversibility, coupling-based convergence, spectral rates for reversible chains, hitting probabilities and times, and the MCMC / simulated-annealing bridge.

## Why this chapter is load-bearing

This chapter turns Markov chains from a basic stochastic-process definition into a usable toolbox for convergence, inference, and computation. It is one of the main bridges from probability theory into MCMC and state-based modeling.

## Core objects

- transition matrix `P`
- stationary distribution `pi`
- detailed balance and reversibility
- total variation distance
- coupling time
- transient block `Q` and absorbing block `R`
- hitting probabilities and mean hitting times
- Metropolis-Hastings and Gibbs-type transition construction

## Structural map

- definitions and elementary theory
- examples
- coupling
- convergence rates for reversible chains
- hitting probabilities and hitting times
- Markov chain Monte Carlo
- simulated annealing

## Theorem and derivation spine

### 1. Stationarity and ergodicity separate local motion from long-run behavior

The chapter starts from `pi = pi P` and then stresses that uniqueness and convergence require ergodicity rather than only a candidate stationary law. The ergodic theorem links time averages to expectations under `pi`, which is the first real justification for Monte Carlo by simulation along a path.

### 2. Detailed balance is the easiest constructive route to equilibrium

For reversible chains, `pi_i p_ij = pi_j p_ji` implies stationarity and gives a practical way to build invariant laws. This is the key algebra later reused by Metropolis-Hastings.

### 3. Coupling gives an operational proof of convergence

The chapter's highlighted result proves convergence of finite-state ergodic chains by coupling two copies until they meet. This is more than a proof trick: it gives quantitative total-variation control and a reusable way to think about mixing.

### 4. Reversible chains admit spectral convergence bounds

Once reversibility holds, eigenstructure controls convergence rates. The chapter's reversible-chain bounds are the main bridge from abstract transition rules to usable statements about how fast equilibrium is approached.

### 5. Hitting probabilities and mean hitting times are linear-system objects

The chapter derives `H = (I - Q)^(-1) R` for hitting probabilities and the related linear systems for hitting times. This is the practical computational payoff of splitting transient and absorbing states.

### 6. MCMC and simulated annealing are Markov-chain design problems

The MCMC section shows how to construct a chain with a prescribed equilibrium law, while the simulated-annealing section turns that idea into stochastic optimization by slowly sharpening the target distribution.

## Quant relevance

This chapter matters for:

- discrete regime models
- latent-state approximation
- MCMC-based computation
- hitting-time problems in credit, queueing, and state models
- understanding convergence rather than assuming it

## Promotion candidates

- [[Markov Chains]]
- [[Markov Chain Monte Carlo]]

## Related notes

- [[Applied Probability]]
- [[Applied Probability - Ch 08 Continuous-Time Markov Chains]]
- [[Markov Chains]]
- [[Markov Chain Monte Carlo]]

## Sources

- [[Applied Probability]]
- [[raw/math_statistics/Applied Probability.pdf]]
