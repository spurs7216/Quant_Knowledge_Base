---
title: Arbitrage Theory in Continuous Time - Ch 24 Potentials and Positive Interest
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - fixed-income
  - positive-rates
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: toc_scan_plus_utf8_text_extraction
technical_depth: selective_deepen
ingest_stage: selective_deepen
chapter_or_section: Ch 24 Potentials and Positive Interest
parent_source: "[[Arbitrage Theory in Continuous Time]]"
sources:
  - "[[Arbitrage Theory in Continuous Time]]"
  - "[[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]"
---
# Arbitrage Theory in Continuous Time - Ch 24 Potentials and Positive Interest

## Ingest Scope and Depth

- Ingest stage: `selective_deepen`
- Pass 1: full chapter scan completed.
- Pass 2: selective deepening focused on potentials, the Flesaker-Hughston framework, and positive-interest constructions.

## Deepening Targets

- This chapter is specialized enough that it should only be promoted further if the vault builds a deeper fixed-income shelf.

## Deepened Subparts

- `24.2` the Flesaker-Hughston framework
- `24.5` the Markov potential approach of Rogers

## Role of the chapter

This chapter is a specialization note inside the rates branch. Its purpose is to show how positivity of rates can be baked into the model architecture rather than added as an afterthought.

## Core mathematical objects

- potential processes
- positive-interest term structures
- measure changes inside potential frameworks

## Structural map of the chapter

- generalities
- Flesaker-Hughston
- change of base measure
- decomposition of a potential
- Rogers' Markov potential approach

## Theorem and derivation spine

The chapter's durable idea is structural:

- by modeling bond prices through potential processes, one can guarantee positivity properties that are harder to enforce in generic short-rate or forward-rate specifications

## Failure modes and misuse points

- treating positive-rate enforcement as a cosmetic add-on
- using specialized positive-rate structures without understanding their modeling constraints

## Quant research relevance

This chapter is currently a rates-specialization branch rather than a core reusable method note.

## What should be promoted out of this source note

- no durable note yet; keep as future rates-expansion candidate

## Related notes

- [[Term-Structure Models]]
- [[Heath-Jarrow-Morton Drift Condition]]
- [[LIBOR Market Models]]

## Sources

- [[Arbitrage Theory in Continuous Time]]
- [[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]
