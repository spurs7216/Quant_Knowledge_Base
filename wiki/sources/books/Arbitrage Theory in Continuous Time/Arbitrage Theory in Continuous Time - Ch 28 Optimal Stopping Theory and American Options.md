---
title: Arbitrage Theory in Continuous Time - Ch 28 Optimal Stopping Theory and American Options
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - optimal-stopping
  - american-options
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: toc_scan_plus_utf8_text_extraction_and_targeted_rendered_theorem_pages
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 28 Optimal Stopping Theory and American Options
parent_source: "[[Arbitrage Theory in Continuous Time]]"
sources:
  - "[[Arbitrage Theory in Continuous Time]]"
  - "[[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]"
---
# Arbitrage Theory in Continuous Time - Ch 28 Optimal Stopping Theory and American Options

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: theorem-level extraction completed for stopping-time value processes, the Snell envelope theorem, variational inequalities, and American-option examples.

## Deepening Targets

- If later work needs numerical stopping methods, deepen the discrete-time recursion and Markov dynamic-programming branch into a Monte Carlo implementation note.

## Deepened Subparts

- `28.2` generalities
- `28.4` discrete time
- `28.5` continuous time
- `28.6` American options

## Role of the chapter

This chapter unifies stopping theory and American-option pricing. The stopping-time machinery is the real method; American options are the most visible finance application.

## Core mathematical objects

- stopping time $\tau$
- reward process $Z$
- Snell envelope recursion
  $$
  V_n=\max\bracket{Z_n,\E[V_{n+1}\given\mathcal{F}_n]}
  $$
- American-option value
  $$
  V_t=\sup_{\tau\in\mathcal{T}_{t,T}}\E^Q\bracket{e^{-\int_t^\tau r_u\,du}\Phi(S_\tau)\given\mathcal{F}_t}
  $$

## Structural map of the chapter

- define admissible stopping-time problems
- solve the discrete-time problem by backward recursion
- identify the Snell envelope
- move to continuous time and variational inequalities
- apply the method to American calls and puts

## Theorem and derivation spine

### The Snell envelope is the value process

The rendered theorem page states that the optimal value process is the Snell envelope of the reward process. That gives the minimal supermartingale dominating the payoff process and turns stopping into a dynamic-programming object.

### American pricing is a stopping problem, not merely a PDE

The PDE or variational-inequality representation is downstream. The underlying object is the supremum over stopping times.

### Early exercise depends on carry, not on "American" as a label

The chapter's examples keep the classical point explicit:

- a non-dividend-paying American call is not exercised early
- puts and dividend-paying claims can have genuine early-exercise regions

## Failure modes and misuse points

- pricing American claims as Europeans plus an arbitrary premium
- discussing exercise rules without checking stopping-time admissibility
- forgetting that the Snell envelope is the discrete-time backbone behind many numerical methods

## Quant research relevance

This chapter matters for:

- American options
- callable claims
- dynamic-programming numerics
- free-boundary intuition

## What should be promoted out of this source note

- refresh [[American Options and Optimal Stopping]]

## Related notes

- [[American Options and Optimal Stopping]]
- [[Stochastic Optimal Control and Hamilton-Jacobi-Bellman Equation]]
- [[Derivatives Markets]]

## Sources

- [[Arbitrage Theory in Continuous Time]]
- [[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]

