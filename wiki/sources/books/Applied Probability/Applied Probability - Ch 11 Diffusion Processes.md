---
title: Applied Probability - Ch 11 Diffusion Processes
type: source
status: chapter_ingested
updated: 2026-04-20
tags:
  - source
  - probability
  - diffusion-processes
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: chapter_text_plus_key_definitions_and_examples
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 11 Diffusion Processes
parent_source: "[[Applied Probability]]"
sources:
  - "[[Applied Probability]]"
  - "[[raw/math_statistics/Applied Probability.pdf]]"
---
# Applied Probability - Ch 11 Diffusion Processes

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: deep extraction completed for infinitesimal drift and variance, Brownian exemplars, first-passage logic, the reflection principle, and equilibrium densities under no-flux conditions.

## Why this chapter is load-bearing

This chapter is the book's continuous-path bridge. It is where random evolution stops being count- or jump-based and becomes locally Gaussian with drift and diffusion coefficients.

## Core objects

- diffusion process `X_t`
- infinitesimal mean `mu(t, x)`
- infinitesimal variance `sigma^2(t, x)`
- Brownian motion
- Brownian bridge
- Ornstein-Uhlenbeck process
- first-passage time
- equilibrium density

## Structural map

- basic definitions and properties
- Brownian-motion examples
- other diffusion examples
- process moments
- first passage problems
- the reflection principle
- equilibrium distributions

## Theorem and derivation spine

### 1. Diffusions are defined locally through drift and variance

The chapter works with infinitesimal mean and variance as the main modeling inputs. That local description is what later becomes stochastic differential equation language in more formal sources.

### 2. Brownian motion is the canonical reference process

Brownian motion supplies the basic Gaussian, independent-increment, nowhere-smooth path structure from which several other examples are built.

### 3. Boundary-value problems encode first-passage questions

The first-passage section turns hitting probabilities and expected passage times into ordinary differential equations. This is a durable bridge from process questions to solvable analysis.

### 4. The reflection principle gives hitting-law control for Brownian motion

The reflection principle is the chapter's cleanest exact path argument. It converts path reflection into closed-form probabilities for first passage and maxima.

### 5. Equilibrium for one-dimensional diffusions comes from no-flux balance

The chapter derives the stationary-density formula by setting the time derivative of the forward equation to zero and imposing zero net probability flux. That is the continuous analogue of balance equations in Markov chains.

## Quant relevance

This chapter matters for:

- continuous-time state dynamics
- mean-reverting models such as Ornstein-Uhlenbeck
- first-passage default and barrier logic
- later stochastic-calculus and asset-pricing texts

## Promotion candidates

- [[Diffusion Processes]]

## Related notes

- [[Applied Probability]]
- [[Applied Probability - Ch 08 Continuous-Time Markov Chains]]
- [[Diffusion Processes]]
- [[Stochastic Calculus]]

## Sources

- [[Applied Probability]]
- [[raw/math_statistics/Applied Probability.pdf]]
