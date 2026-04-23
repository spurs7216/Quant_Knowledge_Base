---
title: Arbitrage Theory in Continuous Time - Ch 23 LIBOR Market Models
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - fixed-income
  - libor
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: toc_scan_plus_utf8_text_extraction_and_targeted_rendered_theorem_pages
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 23 LIBOR Market Models
parent_source: "[[Arbitrage Theory in Continuous Time]]"
sources:
  - "[[Arbitrage Theory in Continuous Time]]"
  - "[[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]"
---
# Arbitrage Theory in Continuous Time - Ch 23 LIBOR Market Models

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: theorem-level extraction completed for forward-LIBOR dynamics, caplet pricing, terminal-measure dynamics, and calibration/simulation considerations.

## Deepening Targets

- If the vault later develops a practical rates-pricing branch, deepen the simulation and calibration material beyond the book's first-pass treatment.

## Deepened Subparts

- `23.2` the LIBOR market model
- `23.3` pricing caps in the LIBOR model
- `23.4` terminal measure dynamics and existence
- `23.5` calibration and simulation

## Role of the chapter

This chapter moves from continuous curve frameworks to market-observed discrete forward rates. It is the rates-market-model analogue of pricing directly in the quote space traders actually use.

## Core mathematical objects

- forward LIBOR rate $L_i(t)$
- forward-measure martingale property
- caplet Black-type pricing formula
  $$
  \mathrm{Capl}_i(t)=\alpha_i p_i(t)\bracket{L_i(t)N(d_1)-RN(d_2)}
  $$

## Structural map of the chapter

- define caps and caplets
- specify LIBOR dynamics under the appropriate forward measures
- price caplets by Black-style formulas
- discuss measure changes, existence, calibration, and simulation

## Theorem and derivation spine

### LIBOR rates are martingales under the correct forward measure

That is the conceptual core of the chapter. Once the benchmark maturity is chosen correctly, the model is built directly on tradable forward-rate quantities.

### Caplet pricing becomes a Black formula

The rendered proposition page shows the chapter's main operational formula:
$$
\mathrm{Capl}_i(t)=\alpha_i p_i(t)\bracket{L_i(t)N(d_1)-RN(d_2)}.
$$

This is why the market-model approach is so practical: it aligns the model with observed caplet and swaption conventions.

## Failure modes and misuse points

- using the wrong forward measure for the chosen tenor claim
- forgetting that existence of the LIBOR model is not automatic for arbitrary volatility specifications
- treating calibration convenience as if it solved all structural no-arbitrage issues

## Quant research relevance

This chapter matters for rates desks because it ties no-arbitrage theory directly to quoted caplet-style products.

## What should be promoted out of this source note

- [[LIBOR Market Models]]
- refresh [[Term-Structure Models]]

## Related notes

- [[LIBOR Market Models]]
- [[Term-Structure Models]]
- [[Change of Numeraire and Forward Measures]]

## Sources

- [[Arbitrage Theory in Continuous Time]]
- [[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]

