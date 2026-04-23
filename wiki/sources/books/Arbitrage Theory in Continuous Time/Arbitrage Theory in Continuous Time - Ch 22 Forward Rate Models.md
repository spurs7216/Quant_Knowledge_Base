---
title: Arbitrage Theory in Continuous Time - Ch 22 Forward Rate Models
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - fixed-income
  - hjm
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: toc_scan_plus_utf8_text_extraction_and_targeted_rendered_theorem_pages
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 22 Forward Rate Models
parent_source: "[[Arbitrage Theory in Continuous Time]]"
sources:
  - "[[Arbitrage Theory in Continuous Time]]"
  - "[[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]"
---
# Arbitrage Theory in Continuous Time - Ch 22 Forward Rate Models

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: theorem-level extraction completed for the HJM drift condition, bond dynamics under the forward-rate framework, Gaussian models, and the Musiela parameterization.

## Deepening Targets

- If later rates work expands, deepen the infinite-dimensional state-space interpretation behind Musiela.

## Deepened Subparts

- `22.1` the Heath-Jarrow-Morton framework
- `22.2` martingale modeling
- `22.3` the general Gaussian model
- `22.4` the Musiela parameterization

## Role of the chapter

This chapter is the curve-model counterpart to short-rate models. Instead of modeling one short rate, it models the whole forward curve directly.

## Core mathematical objects

- forward-rate dynamics
  $$
  df(t,T)=\alpha(t,T)\,dt+\sigma(t,T)\,dW_t
  $$
- bond curve identity
  $$
  p(t,T)=e^{-\int_t^T f(t,s)\,ds}
  $$
- HJM drift condition
  $$
  \alpha(t,T)=\sigma(t,T)\int_t^T \sigma(t,s)^\prime ds-\sigma(t,T)\lambda(t)
  $$

## Structural map of the chapter

- specify the forward-rate family
- derive no-arbitrage restrictions on its drift
- specialize under the martingale measure
- derive Gaussian-model and Musiela forms

## Theorem and derivation spine

### HJM is a framework, not one model

The rendered theorem page explicitly says the HJM approach is a framework. Its content is the no-arbitrage drift restriction, not a single preferred volatility specification.

### No-arbitrage ties drift to volatility across the whole curve

The chapter's main theorem states:
$$
\alpha(t,T)=\sigma(t,T)\int_t^T \sigma(t,s)^\prime ds-\sigma(t,T)\lambda(t).
$$

Under the martingale measure $Q$, the market-price-of-risk term vanishes and the drift is fully pinned down by volatility.

That is one of the clearest examples in finance of "volatility is free, drift is forced."

## Failure modes and misuse points

- talking about HJM as if it were one specific model
- calibrating forward-rate volatility while ignoring the implied drift restriction
- forgetting that the framework is infinite-dimensional unless parameterized

## Quant research relevance

This chapter is core for rates modeling because it states the canonical no-arbitrage restriction at the forward-curve level.

## What should be promoted out of this source note

- [[Heath-Jarrow-Morton Drift Condition]]
- refresh [[Term-Structure Models]]

## Related notes

- [[Heath-Jarrow-Morton Drift Condition]]
- [[Term-Structure Models]]
- [[LIBOR Market Models]]
- [[Change of Numeraire and Forward Measures]]

## Sources

- [[Arbitrage Theory in Continuous Time]]
- [[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]

