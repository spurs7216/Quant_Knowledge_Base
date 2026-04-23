---
title: Stochastic Calculus for Finance II - Ch 07 Exotic Options
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - stochastic-calculus
  - exotic-options
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: toc_scan_plus_visual_read_of_asian_option_state_augmentation_and_numeraire_pages
technical_depth: selective_deepen
ingest_stage: selective_deepen
chapter_or_section: Ch 07 Exotic Options
parent_source: "[[Stochastic Calculus for Finance II]]"
sources:
  - "[[Stochastic Calculus for Finance II]]"
  - "[[raw/math_statistics/Steven E. Shreve-Stochastic Calculus for Finance II_20150303200346.pdf]]"
---
# Stochastic Calculus for Finance II - Ch 07 Exotic Options

## Ingest Scope and Depth

- Ingest stage: `selective_deepen`
- Pass 1: full chapter scan completed against the raw source.
- Pass 2: selective theorem-level treatment focused on the state augmentation and numeraire tricks that generalize beyond the individual option formulas.

## Deepening Targets

- If later work needs a dedicated path-dependent-derivatives branch, deepen the barrier and lookback constructions into standalone durable notes.

## Deepened Subparts

- `7.3` knock-out barriers
- `7.4` lookbacks
- `7.5` Asian options

## Role of the chapter

This chapter shows how path dependence changes the state space and forces more creative measure changes.

The main durable lesson is not any single closed form. It is the modeling move from one-dimensional state to augmented state.

## Core mathematical objects

- path-dependent state augmentation
  $$Y(T)=y+\int_t^T S(u)\,du$$
- discounted hedge identity for Asian options
  $$d\paren{e^{-rt}v(t,S(t),Y(t))}=e^{-rt}\sigma S(t)v_x(t,S(t),Y(t))\,d\widetilde{W}(t)$$
- delta hedge
  $$\Delta(t)=v_x(t,S(t),Y(t))$$

## Structural map of the chapter

- maxima and barriers from Brownian hitting arguments
- lookback pricing via dimension reduction
- Asian options via state augmentation and numeraire change

## Theorem and derivation spine

### Path dependence forces state augmentation

For Asian options, the payoff depends on an integral of the underlying path, not only on $S(T)$.

The chapter introduces the accumulated state

$$Y(T)=y+\int_t^T S(u)\,du,$$

so the pricing problem can be rewritten as a Markov problem in $(S,Y)$ instead of a non-Markov problem in $S$ alone.

### Hedging survives if the right state variables are chosen

The rendered Asian-option page shows the discounted option-value dynamics

$$d\paren{e^{-rt}v(t,S(t),Y(t))}=e^{-rt}\sigma S(t)v_x(t,S(t),Y(t))\,d\widetilde{W}(t),$$

and the discounted hedge portfolio

$$d\paren{e^{-rt}X(t)}=e^{-rt}\sigma S(t)\Delta(t)\,d\widetilde{W}(t).$$

Equating the two gives

$$\Delta(t)=v_x(t,S(t),Y(t)).$$

So even for a path-dependent claim, the hedge still comes from matching the stochastic term once the state is enlarged correctly.

### Change of numeraire simplifies some path-dependent claims

The chapter then uses numeraire change to derive PDEs and pricing formulas for Asian options with nonzero interest rates.

That makes Chapter 7 a bridge into the more systematic numeraire treatment in Chapter 9.

## Failure modes and misuse points

- hunting for closed forms before checking whether the state has been specified correctly
- treating a path-dependent claim as Markov in the wrong state variable
- forgetting that barrier and lookback formulas depend sensitively on path continuity and monitoring assumptions

## Quant research relevance

This chapter matters for:

- path-dependent derivatives
- state augmentation in pricing and control
- barrier-hitting intuition
- numeraire tricks beyond vanilla options

## What should be promoted out of this source note

- later durable notes on path-dependent state augmentation and Brownian-bridge Monte Carlo corrections

## Related notes

- [[Stochastic Calculus for Finance II]]
- [[Stochastic Calculus for Finance II - Ch 03 Brownian Motion]]
- [[Stochastic Calculus for Finance II - Ch 09 Change of Numeraire]]
- [[Change of Numeraire and Forward Measures]]
- [[Monte Carlo Methods]]

## Sources

- [[Stochastic Calculus for Finance II]]
- [[raw/math_statistics/Steven E. Shreve-Stochastic Calculus for Finance II_20150303200346.pdf]]
