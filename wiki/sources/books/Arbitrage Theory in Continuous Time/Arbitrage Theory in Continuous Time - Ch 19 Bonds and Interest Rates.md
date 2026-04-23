---
title: Arbitrage Theory in Continuous Time - Ch 19 Bonds and Interest Rates
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - fixed-income
  - term-structure
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: toc_scan_plus_utf8_text_extraction_and_targeted_rendered_theorem_pages
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 19 Bonds and Interest Rates
parent_source: "[[Arbitrage Theory in Continuous Time]]"
sources:
  - "[[Arbitrage Theory in Continuous Time]]"
  - "[[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]"
---
# Arbitrage Theory in Continuous Time - Ch 19 Bonds and Interest Rates

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: theorem-level extraction completed for bond-price identities, the forward-rate representation, and the term-structure equation.

## Deepening Targets

- If rates work expands, deepen the swap and duration material into a fixed-income instruments note.

## Deepened Subparts

- `19.1` zero coupon bonds
- `19.2` interest rates
- `19.3` coupon bonds, swaps, and yields

## Role of the chapter

This chapter starts the rates branch. It defines the curve objects carefully enough that later short-rate, HJM, and LIBOR chapters can be read as no-arbitrage dynamics on the same term structure.

## Core mathematical objects

- zero-coupon bond price $p(t,T)$
- continuously compounded forward rate
  $$
  p(t,T)=\exp\paren{-\int_t^T f(t,u)\,du}
  $$
- short rate
  $$
  r_t=f(t,t)
  $$
- term-structure equation

## Structural map of the chapter

- define discount bonds and rate conventions
- connect bond prices, forward rates, and the money account
- derive the bond-dynamics representation and term-structure PDE
- extend the instrument set to coupon bonds, swaps, yields, and duration

## Theorem and derivation spine

### The term structure is the integrated forward curve

The chapter's most reusable identity is
$$
p(t,T)=\exp\paren{-\int_t^T f(t,u)\,du}.
$$
It is the bridge between curve models and bond prices.

### Absence of arbitrage forces the bond-pricing PDE

The rendered theorem page states the term-structure equation:
$$
F_t^T+\paren{\mu-\lambda\sigma}F_r^T+\frac{1}{2}\sigma^2 F_{rr}^T-rF^T=0,
\qquad
F^T(T,r)=1.
$$

This is the fixed-income analogue of Black-Scholes, but with the market price of risk left as an exogenous modeling input.

## Failure modes and misuse points

- fitting yields without specifying an arbitrage-free curve dynamics
- forgetting that the market price of risk is not pinned down by bond arbitrage alone
- mixing spot, forward, and short-rate objects loosely

## Quant research relevance

This chapter is the foundational curve note for everything that follows in rates:

- short-rate models
- HJM
- LIBOR market models
- bond-option pricing

## What should be promoted out of this source note

- refresh [[Term-Structure Models]]
- support [[Heath-Jarrow-Morton Drift Condition]]

## Related notes

- [[Term-Structure Models]]
- [[Change of Numeraire and Forward Measures]]
- [[Heath-Jarrow-Morton Drift Condition]]
- [[LIBOR Market Models]]

## Sources

- [[Arbitrage Theory in Continuous Time]]
- [[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]

