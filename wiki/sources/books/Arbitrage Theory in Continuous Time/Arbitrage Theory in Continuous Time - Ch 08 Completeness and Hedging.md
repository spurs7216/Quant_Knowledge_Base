---
title: Arbitrage Theory in Continuous Time - Ch 08 Completeness and Hedging
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - mathematical-finance
  - completeness
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: toc_scan_plus_utf8_text_extraction_and_targeted_rendered_theorem_pages
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 08 Completeness and Hedging
parent_source: "[[Arbitrage Theory in Continuous Time]]"
sources:
  - "[[Arbitrage Theory in Continuous Time]]"
  - "[[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]"
---
# Arbitrage Theory in Continuous Time - Ch 08 Completeness and Hedging

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: theorem-level extraction completed for completeness in Black-Scholes, replication from PDE solutions, and the existence-versus-uniqueness logic behind hedging.

## Deepening Targets

- If later work needs a stronger semimartingale treatment, deepen the general completeness statements beyond the Black-Scholes diffusion case.

## Deepened Subparts

- `8.2` completeness in the Black-Scholes model
- `8.3` completeness and absence of arbitrage

## Role of the chapter

This chapter upgrades Black-Scholes pricing from a heuristic PDE trick into a completeness statement: every sufficiently regular claim can actually be hedged.

## Core mathematical objects

- claim $X=\Phi(S_T)$
- replicating wealth $V_t=F(t,S_t)$
- delta hedge
  $$
  h_t^S=F_S(t,S_t)
  $$
- Black-Scholes boundary-value problem
  $$
  F_t+rSF_S+\frac{1}{2}\sigma^2 S^2 F_{SS}-rF=0,
  \qquad
  F(T,s)=\Phi(s)
  $$

## Structural map of the chapter

- state completeness as a hedge-existence problem
- derive the candidate hedge from the PDE solution
- prove that the candidate is self-financing and replicating
- connect completeness to the broader no-arbitrage architecture

## Theorem and derivation spine

### Completeness means every claim is attainable

The chapter's headline theorem says the Black-Scholes model is complete. That is stronger than arbitrage freedom: not only do prices avoid contradiction, they are uniquely pinned down by replication.

### The PDE solution is not only a price candidate

The rendered proof page shows the key identities
$$
w_t^S=\frac{S_t F_S(t,S_t)}{F(t,S_t)},
$$
and the consistency condition that collapses into the Black-Scholes PDE.

The theorem then reverses the logic: if $F$ solves the PDE with the terminal payoff, the corresponding trading strategy replicates the claim.

### Existence versus uniqueness appears again

This chapter is the diffusion-model version of the Chapter 3 duality:

- arbitrage freedom gives existence of a pricing rule
- completeness gives uniqueness through replication

## Failure modes and misuse points

- presenting Black-Scholes as a closed-form formula without the hedge theorem behind it
- confusing a PDE solution candidate with a proven replicating strategy
- assuming every continuous-time model is complete because Black-Scholes is

## Quant research relevance

This chapter matters whenever a model claim says:

- the hedge exists
- the price is unique
- the residual risk is zero under the model

Those are completeness claims and should not be smuggled in casually.

## What should be promoted out of this source note

- [[Market Completeness and Incomplete Markets]]
- refresh [[Risk-Neutral Pricing and Fundamental Theorems of Asset Pricing]]

## Related notes

- [[Market Completeness and Incomplete Markets]]
- [[Risk-Neutral Pricing and Fundamental Theorems of Asset Pricing]]
- [[Arbitrage Theory in Continuous Time - Ch 09 A Primer on Incomplete Markets]]

## Sources

- [[Arbitrage Theory in Continuous Time]]
- [[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]

