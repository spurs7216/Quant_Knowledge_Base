---
title: Stochastic Calculus for Finance II - Ch 09 Change of Numeraire
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - stochastic-calculus
  - numeraire
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: toc_scan_plus_visual_read_of_foreign_domestic_measure_and_forward_measure_pages
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 09 Change of Numeraire
parent_source: "[[Stochastic Calculus for Finance II]]"
sources:
  - "[[Stochastic Calculus for Finance II]]"
  - "[[raw/math_statistics/Steven E. Shreve-Stochastic Calculus for Finance II_20150303200346.pdf]]"
---
# Stochastic Calculus for Finance II - Ch 09 Change of Numeraire

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed against the raw source.
- Pass 2: theorem-level extraction completed for numeraire-based measure change, foreign/domestic pricing measures, and forward measures built from zero-coupon bonds.

## Deepening Targets

- If later work needs an FX branch, deepen the exchange-rate put-call duality and Garman-Kohlhagen details into a dedicated note.

## Deepened Subparts

- `9.2` numeraire
- `9.3` foreign and domestic risk-neutral measures
- `9.4` forward measures

## Role of the chapter

This chapter teaches the right abstraction: price by dividing by a traded benchmark, then choose the measure under which that benchmark-normalized price is a martingale.

It is one of the cleanest conceptual upgrades in the book.

## Core mathematical objects

- numeraire
  $$N(t)>0$$
- numeraire-normalized asset price
  $$S^{(N)}(t)=\frac{S(t)}{N(t)}$$
- forward bond numeraire
  $$B(t,T)=\frac{1}{D(t)}\widetilde{\mathbb{E}}\bracket{D(T)\given\mathcal{F}(t)}$$
- forward price
  $$\operatorname{Fwd}_S(t,T)=\frac{S(t)}{B(t,T)}$$

## Structural map of the chapter

- define pricing relative to a generic numeraire
- use the idea in foreign/domestic currency models
- define the $T$-forward measure with a zero-coupon bond as numeraire

## Theorem and derivation spine

### Numeraire change is measure change plus normalization

The chapter's idea is that if $N$ is the numeraire, then prices divided by $N$ become martingales under the associated measure.

The rendered foreign/domestic page shows this explicitly in a multidimensional Brownian setting: the transformed normalized asset process is a martingale under the numeraire measure.

### Foreign and domestic pricing are the same structure seen from different benchmarks

Section `9.3` treats currency models by switching between domestic and foreign money-market accounts as numeraires.

That yields a clean explanation for why drift terms and "risk-neutral" measures are not absolute objects. They depend on the unit of account.

### Forward measures linearize forward contracts

The rendered forward-measure page states the bond pricing identity

$$B(t,T)=\frac{1}{D(t)}\widetilde{\mathbb{E}}\bracket{D(T)\given\mathcal{F}(t)},$$

and then the forward-contract value

$$V(t)=S(t)-KB(t,T).$$

Setting the contract value to zero gives the time-$t$ forward price

$$\operatorname{Fwd}_S(t,T)=\frac{S(t)}{B(t,T)}.$$

This is the central practical result: once the bond is the numeraire, forward prices and caplet-style payoffs become much cleaner.

## Failure modes and misuse points

- saying "the" risk-neutral measure when the numeraire has changed
- treating forward prices as expectations under the wrong measure
- forgetting that numeraire choice changes the martingale object, not the economics of no arbitrage

## Quant research relevance

This chapter matters for:

- FX pricing
- rates derivatives
- forward and futures modeling
- simplifying path-dependent pricing problems by a better benchmark choice

## What should be promoted out of this source note

- [[Change of Numeraire and Forward Measures]]

## Related notes

- [[Stochastic Calculus for Finance II]]
- [[Stochastic Calculus for Finance II - Ch 10 Term-Structure Models]]
- [[Change of Numeraire and Forward Measures]]
- [[Risk-Neutral Pricing and Fundamental Theorems of Asset Pricing]]
- [[Term-Structure Models]]

## Sources

- [[Stochastic Calculus for Finance II]]
- [[raw/math_statistics/Steven E. Shreve-Stochastic Calculus for Finance II_20150303200346.pdf]]
