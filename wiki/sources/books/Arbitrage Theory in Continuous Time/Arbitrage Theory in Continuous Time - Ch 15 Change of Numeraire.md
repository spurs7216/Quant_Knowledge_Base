---
title: Arbitrage Theory in Continuous Time - Ch 15 Change of Numeraire
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - mathematical-finance
  - numeraire
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: toc_scan_plus_utf8_text_extraction_and_targeted_rendered_theorem_pages
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 15 Change of Numeraire
parent_source: "[[Arbitrage Theory in Continuous Time]]"
sources:
  - "[[Arbitrage Theory in Continuous Time]]"
  - "[[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]"
---
# Arbitrage Theory in Continuous Time - Ch 15 Change of Numeraire

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: theorem-level extraction completed for the invariance lemma, the general numeraire pricing theorem, forward measures, exchange options, and the numeraire portfolio.

## Deepening Targets

- If later work needs a stronger FX or commodity carry branch, deepen the examples rather than the general theorem again.

## Deepened Subparts

- `15.2` generalities
- `15.3` changing the numeraire
- `15.5` forward measures
- `15.6` a general option pricing formula
- `15.7` the numeraire portfolio

## Role of the chapter

This chapter systematizes a technique that appears informally throughout mathematical finance: choose the traded benchmark that makes the claim easiest to price.

## Core mathematical objects

- numeraire $\beta_t$
- normalized prices $Z_t=S_t/\beta_t$
- invariance of self-financing
  $$
  dV_t^S=h_t\,dS_t
  \iff
  dV_t^Z=h_t\,dZ_t
  $$
- numeraire pricing formula
  $$
  \Pi_t[X]=N_t\E^N\bracket{\frac{X}{N_T}\given\mathcal{F}_t}
  $$

## Structural map of the chapter

- prove that self-financing is invariant under normalization
- restate FTAP with a generic positive traded numeraire
- specialize to bond numeraires and forward measures
- use the method on exchange options and rates claims

## Theorem and derivation spine

### The invariance lemma is the key structural result

The rendered lemma page states that if $Z=S/\beta$ for any strictly positive Ito process $\beta$, then self-financing in $S$ is equivalent to self-financing in $Z$.

That result is small in appearance but huge in consequence. It is what allows the entire pricing problem to be reformulated under a more convenient benchmark without changing the trading structure.

### FTAP is numeraire-invariant

The theorem page makes the general pricing statement explicit:
$$
\Pi_t[X]=S_t^0 E^0\bracket{\frac{X}{S_T^0}\given\mathcal{F}_t},
$$
and the same logic works for any strictly positive traded numeraire.

### Forward measures are the rates-specialized version

Once a zero-coupon bond is used as numeraire, forward-measure pricing becomes natural. The chapter then uses this to simplify exchange-option and bond-option calculations.

## Failure modes and misuse points

- speaking about "the" risk-neutral measure without naming the numeraire
- changing benchmark algebraically while forgetting the benchmark must be traded and strictly positive
- using the method as a shortcut without verifying the corresponding filtration and asset structure

## Quant research relevance

This chapter is one of the most reusable in the whole book because the technique appears everywhere:

- FX pricing
- bond-option pricing
- LIBOR and forward-rate modeling
- stochastic discount factor intuition

## What should be promoted out of this source note

- [[Change of Numeraire and Forward Measures]]
- support [[Term-Structure Models]]

## Related notes

- [[Change of Numeraire and Forward Measures]]
- [[Term-Structure Models]]
- [[Risk-Neutral Pricing and Fundamental Theorems of Asset Pricing]]
- [[Arbitrage Theory in Continuous Time - Ch 22 Forward Rate Models]]

## Sources

- [[Arbitrage Theory in Continuous Time]]
- [[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]

