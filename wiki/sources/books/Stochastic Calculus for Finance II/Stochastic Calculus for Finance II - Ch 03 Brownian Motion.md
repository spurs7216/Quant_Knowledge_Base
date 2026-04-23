---
title: Stochastic Calculus for Finance II - Ch 03 Brownian Motion
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - stochastic-calculus
  - brownian-motion
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: toc_scan_plus_visual_read_of_definition_quadratic_variation_and_reflection_principle_pages
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 03 Brownian Motion
parent_source: "[[Stochastic Calculus for Finance II]]"
sources:
  - "[[Stochastic Calculus for Finance II]]"
  - "[[raw/math_statistics/Steven E. Shreve-Stochastic Calculus for Finance II_20150303200346.pdf]]"
---
# Stochastic Calculus for Finance II - Ch 03 Brownian Motion

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed against the raw source.
- Pass 2: theorem-level extraction completed for the Brownian-motion definition, quadratic variation, first-passage logic, and reflection-principle consequences.

## Deepening Targets

- If later work needs pathwise Monte Carlo control notes, deepen Brownian bridge and passage-time distributions further.

## Deepened Subparts

- `3.3` Brownian motion
- `3.4` quadratic variation
- `3.6` first passage time distribution
- `3.7` reflection principle

## Role of the chapter

This chapter introduces the noise process that changes the rules of calculus.

Brownian motion is not just Gaussian noise indexed by time. Its quadratic variation is why the chain rule gains a second-order term and why hedging PDEs appear later.

## Core mathematical objects

- Brownian motion
  $$W(0)=0, \qquad W(t_i)-W(t_{i-1}) \text{ independent}, \qquad W(t)-W(s)\sim\mathcal{N}(0,t-s)$$
- quadratic variation
  $$[f,f](T)=\lim_{\norm{\Pi}\to 0}\sum_{j=0}^{n-1}\bracket{f(t_{j+1})-f(t_j)}^2$$
- Brownian quadratic variation
  $$[W,W](T)=T$$
- first passage time
  $$\tau_m=\min\set{t\ge 0: W(t)=m}$$

## Structural map of the chapter

- scaled random walks and Brownian limits
- definition and filtration of Brownian motion
- quadratic variation as the key path property
- Markov and passage-time properties
- reflection principle for maxima and hitting events

## Theorem and derivation spine

### Brownian motion definition

The rendered definition page states the central object directly.

For $0=t_0<t_1<\cdots<t_m$, the increments

$$W(t_1), \quad W(t_2)-W(t_1), \quad \dots, \quad W(t_m)-W(t_{m-1})$$

are independent and each satisfies

$$\mathbb{E}\bracket{W(t_{i+1})-W(t_i)}=0, \qquad \operatorname{Var}\bracket{W(t_{i+1})-W(t_i)}=t_{i+1}-t_i.$$

That independence plus variance scaling is the object-level content that later drives Ito isometry and Girsanov transformations.

### Quadratic variation distinguishes Brownian paths from smooth paths

The chapter defines

$$[f,f](T)=\lim_{\norm{\Pi}\to 0}\sum_{j=0}^{n-1}\bracket{f(t_{j+1})-f(t_j)}^2.$$

The rendered page shows the key contrast:

- if $f$ has a continuous derivative, then
  $$[f,f](T)=0$$
- for Brownian motion,
  $$[W,W](T)=T$$

That single fact is why ordinary calculus fails and Ito-Doeblin needs the extra $\frac{1}{2}f_{xx}\,dt$ term.

### Geometric Brownian motion inherits the Ito correction in the log

The chapter derives, via scaled random walks and Taylor expansion,

$$\log S(t)=\log S(0)+\sigma W(t)-\frac{1}{2}\sigma^2 t.$$

That $-\frac{1}{2}\sigma^2 t$ correction is already the future Ito term showing up before Chapter 4 formalizes the calculus.

### First passage times and reflection logic

The rendered theorem page states:

$$\mathbb{E}e^{-\alpha \tau_m}=e^{-|m|\sqrt{2\alpha}}, \qquad \alpha>0,$$

for the first passage time $\tau_m$ of Brownian motion to level $m$.

This chapter then uses reflection arguments to turn path-counting problems into distribution identities for maxima and barrier hits.

## Failure modes and misuse points

- treating Brownian motion as merely iid Gaussian shocks laid end to end
- forgetting that Brownian paths are continuous but almost surely nowhere differentiable
- importing smooth-path calculus into a process with nonzero quadratic variation
- using Brownian passage-time intuition in jump or discrete-trading settings without adjustment

## Quant research relevance

This chapter matters for:

- diffusion modeling
- Greeks and delta-hedging logic
- barrier and lookback pricing
- Monte Carlo path simulation
- any result that depends on quadratic variation or hitting probabilities

## What should be promoted out of this source note

- [[Brownian Motion and Quadratic Variation]]

## Related notes

- [[Stochastic Calculus for Finance II]]
- [[Stochastic Calculus for Finance II - Ch 04 Stochastic Calculus]]
- [[Brownian Motion and Quadratic Variation]]
- [[Diffusion Processes]]
- [[Monte Carlo Methods]]

## Sources

- [[Stochastic Calculus for Finance II]]
- [[raw/math_statistics/Steven E. Shreve-Stochastic Calculus for Finance II_20150303200346.pdf]]
