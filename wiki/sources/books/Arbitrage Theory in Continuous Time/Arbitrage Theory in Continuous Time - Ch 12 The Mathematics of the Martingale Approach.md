---
title: Arbitrage Theory in Continuous Time - Ch 12 The Mathematics of the Martingale Approach
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - mathematical-finance
  - martingale-pricing
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: toc_scan_plus_utf8_text_extraction_and_targeted_rendered_theorem_pages
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 12 The Mathematics of the Martingale Approach
parent_source: "[[Arbitrage Theory in Continuous Time]]"
sources:
  - "[[Arbitrage Theory in Continuous Time]]"
  - "[[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]"
---
# Arbitrage Theory in Continuous Time - Ch 12 The Mathematics of the Martingale Approach

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: theorem-level extraction completed for representation of Wiener functionals, martingale representation, Girsanov, and the converse Girsanov direction.

## Deepening Targets

- If later work needs a more rigorous stochastic-analysis layer, deepen the integrability and filtration assumptions behind representation and change-of-measure results.

## Deepened Subparts

- `12.1` stochastic integral representations
- `12.2` Girsanov theorem heuristics
- `12.3` the Girsanov theorem
- `12.4` the converse of the Girsanov theorem

## Role of the chapter

This chapter supplies the hidden theorem machinery behind the previous chapter's finance statements.

## Core mathematical objects

- martingale representation
  $$
  X=\E[X]+\int_0^T g_t\,dW_t
  $$
- likelihood process
  $$
  L_t=\exp\bracket{-\int_0^t \phi_u\,dW_u-\frac{1}{2}\int_0^t \norm{\phi_u}^2\,du}
  $$
- Girsanov drift shift
  $$
  dW_t=\phi_t\,dt+dW_t^Q
  $$

## Structural map of the chapter

- represent square-integrable Wiener functionals
- upgrade the representation to conditional martingales
- show how absolute-continuity reweighting changes drift
- connect those results back to finance pricing arguments

## Theorem and derivation spine

### Martingale representation is the hedging theorem in disguise

The chapter's core theorem says every sufficiently integrable Wiener-filtration martingale admits a stochastic-integral representation. In finance terms, that theorem is what lets discounted claim values be replicated by trading in Brownian risk sources.

### Girsanov changes drift without changing volatility scale

The rendered Girsanov pages show the canonical drift shift:
$$
dW_t=\phi_t\,dt+dW_t^Q.
$$

The measure change reweights paths so the same underlying noise can be viewed under a pricing measure with altered drift.

### Converse Girsanov explains which martingale measures are even possible

The converse direction matters because not every arbitrary drift manipulation corresponds to an equivalent measure. The theorem characterizes exactly which absolutely continuous measure changes preserve the Wiener structure.

## Failure modes and misuse points

- using Girsanov without checking Novikov-type or integrability assumptions
- talking about hedging in Brownian models without recognizing the role of martingale representation
- treating measure change as a purely formal substitution

## Quant research relevance

This chapter is load-bearing for:

- FTAP in diffusion models
- change of numeraire
- forward measures
- incomplete-market measure selection

## What should be promoted out of this source note

- refresh [[Risk-Neutral Pricing and Fundamental Theorems of Asset Pricing]]
- support [[Change of Numeraire and Forward Measures]]

## Related notes

- [[Risk-Neutral Pricing and Fundamental Theorems of Asset Pricing]]
- [[Change of Numeraire and Forward Measures]]
- [[Stochastic Discount Factors]]
- [[Arbitrage Theory in Continuous Time - Ch 11 The Martingale Approach to Arbitrage Theory]]

## Sources

- [[Arbitrage Theory in Continuous Time]]
- [[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]

