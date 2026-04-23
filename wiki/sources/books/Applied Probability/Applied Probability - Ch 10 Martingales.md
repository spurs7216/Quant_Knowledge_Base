---
title: Applied Probability - Ch 10 Martingales
type: source
status: chapter_ingested
updated: 2026-04-20
tags:
  - source
  - probability
  - martingales
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: chapter_text_plus_key_definitions_and_propositions
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 10 Martingales
parent_source: "[[Applied Probability]]"
sources:
  - "[[Applied Probability]]"
  - "[[raw/math_statistics/Applied Probability.pdf]]"
---
# Applied Probability - Ch 10 Martingales

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: deep extraction completed for martingale definitions and examples, convergence with bounded second moments, optional stopping, Wald's identity, and Azuma-Hoeffding concentration.

## Why this chapter is load-bearing

Martingales are one of the most reusable probability objects in the entire shelf. They connect process structure, stopping arguments, concentration, and later no-arbitrage language in continuous-time finance.

## Core objects

- filtration `F_n`
- martingale, submartingale, and supermartingale
- Doob martingale `E(Z | F_n)`
- stopping time `T`
- stopped process `X_{T ^ n}`
- bounded differences

## Structural map

- definition and examples
- martingale convergence
- optional stopping
- large deviation bounds

## Theorem and derivation spine

### 1. The definition is conditional-expectation invariance, not zero drift folklore

The chapter defines martingales relative to a filtration and keeps the conditioning structure explicit. That is the only way optional stopping and convergence results make sense.

### 2. Doob martingales explain why martingales are everywhere

The example `X_n = E(Z | F_n)` shows that martingales are not exotic objects. They arise whenever information is progressively revealed about a fixed integrable target.

### 3. Kolmogorov-type bounds lead to convergence

The chapter proves a maximal inequality and then uses bounded second moments to obtain almost sure convergence of square-integrable martingales. This is the basic route from local conditional structure to long-run path behavior.

### 4. Optional stopping works only under real conditions

The optional stopping theorem is given with explicit hypotheses on finiteness and integrability. The chapter also uses it to recover familiar identities such as Wald's identity and hitting-probability calculations.

### 5. Azuma-Hoeffding turns martingales into concentration tools

The bounded-difference inequality is one of the chapter's most reusable results. It extends concentration logic beyond simple independent sums to functions revealed incrementally through a filtration.

## Quant relevance

This chapter matters for:

- stopping-time arguments
- concentration bounds for random constructions
- sequential estimation and online updates
- later martingale pricing intuition in continuous-time finance

## Promotion candidates

- [[Martingales]]

## Related notes

- [[Applied Probability]]
- [[Applied Probability - Ch 11 Diffusion Processes]]
- [[Martingales]]
- [[Stochastic Calculus]]

## Sources

- [[Applied Probability]]
- [[raw/math_statistics/Applied Probability.pdf]]
