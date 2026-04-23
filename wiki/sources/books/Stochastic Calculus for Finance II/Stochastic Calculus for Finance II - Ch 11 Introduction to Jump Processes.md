---
title: Stochastic Calculus for Finance II - Ch 11 Introduction to Jump Processes
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - stochastic-calculus
  - jump-processes
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: toc_scan_plus_visual_read_of_compensated_poisson_ito_jump_and_change_of_measure_pages
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 11 Introduction to Jump Processes
parent_source: "[[Stochastic Calculus for Finance II]]"
sources:
  - "[[Stochastic Calculus for Finance II]]"
  - "[[raw/math_statistics/Steven E. Shreve-Stochastic Calculus for Finance II_20150303200346.pdf]]"
---
# Stochastic Calculus for Finance II - Ch 11 Introduction to Jump Processes

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed against the raw source.
- Pass 2: theorem-level extraction completed for Poisson increments, compensated processes, Ito-Doeblin for jumps, and change of measure for Poisson and compound-Poisson processes.

## Deepening Targets

- If later work needs a jump-diffusion branch, deepen the compound-Poisson plus Brownian pricing formulas and the Doleans-Dade exponential machinery.

## Deepened Subparts

- `11.2` Poisson process
- `11.4` jump processes and their integrals
- `11.5` stochastic calculus for jump processes
- `11.6` change of measure
- `11.7` pricing a European call in a jump model

## Role of the chapter

This chapter breaks the diffusion-only world of the earlier book.

Its durable lesson is that once paths jump, quadratic variation and measure change gain discrete jump terms and compensators become central objects.

## Core mathematical objects

- Poisson process with intensity $\lambda$
  $$\mathbb{E}[N(t)-N(s)]=\lambda(t-s), \qquad \operatorname{Var}[N(t)-N(s)]=\lambda(t-s)$$
- compensated Poisson process
  $$M(t)=N(t)-\lambda t$$
- jump Ito-Doeblin formula
  $$f(X(t))=f(X(0))+\int_0^t f'(X(s))\,dX^c(s)+\frac{1}{2}\int_0^t f''(X(s))\,d[X^c,X^c](s)+\sum_{0<s\le t}\bracket{f(X(s))-f(X(s-))}$$
- Poisson change-of-measure density
  $$Z(t)=e^{(\lambda-\tilde{\lambda})t}\paren{\frac{\tilde{\lambda}}{\lambda}}^{N(t)}$$

## Structural map of the chapter

- Poisson and compound-Poisson processes
- jump quadratic variation and integration rules
- Ito calculus with jumps
- measure changes that alter jump intensity and jump-size law
- option pricing in jump models

## Theorem and derivation spine

### Compensated Poisson processes are martingales

The rendered Poisson page states:

$$M(t)=N(t)-\lambda t,$$

and then proves that $M(t)$ is a martingale.

That is the jump analogue of centering Brownian motion around zero drift. The compensator $\lambda t$ is what must be removed to recover the martingale structure.

### Jump Ito-Doeblin needs an explicit jump sum

The rendered theorem page states the one-jump-process formula:

$$f(X(t))=f(X(0))+\int_0^t f'(X(s))\,dX^c(s)+\frac{1}{2}\int_0^t f''(X(s))\,dX^c(s)\,dX^c(s)+\sum_{0<s\le t}\bracket{f(X(s))-f(X(s-))}.$$

Compared with diffusion Ito, the new term is the sum over jump discontinuities. That is the exact mathematical reason diffusion-only Greeks and PDEs cannot simply be reused in jump models.

### Change of measure for jumps changes intensity, not only drift

The rendered Poisson-measure-change page defines

$$Z(t)=e^{(\lambda-\tilde{\lambda})t}\paren{\frac{\tilde{\lambda}}{\lambda}}^{N(t)},$$

and proves that $Z(t)$ is a martingale.

Using $Z(T)$ as density changes the Poisson intensity from $\lambda$ to $\tilde{\lambda}$.

That is the jump analogue of Girsanov, but the economic meaning is different: one is reweighting jump arrival rates and sometimes jump-size distributions, not merely continuous drift.

## Failure modes and misuse points

- carrying diffusion intuition over to jump models without adding the jump term explicitly
- forgetting that jump times create left limits $X(t-)$ and discontinuity corrections
- talking about "risk-neutral drift adjustment" in a jump model when intensity and jump-size law may also move
- using diffusion hedging language in an incomplete jump market

## Quant research relevance

This chapter matters for:

- jump-diffusion pricing
- event-risk and earnings-gap modeling
- compensator-based martingale methods
- discrete shock modeling beyond pure Brownian noise

## What should be promoted out of this source note

- [[Jump Processes and Compensators]]

## Related notes

- [[Stochastic Calculus for Finance II]]
- [[Stochastic Calculus for Finance II - Ch 04 Stochastic Calculus]]
- [[Jump Processes and Compensators]]
- [[Risk-Neutral Pricing and Fundamental Theorems of Asset Pricing]]
- [[Diffusion Processes]]

## Sources

- [[Stochastic Calculus for Finance II]]
- [[raw/math_statistics/Steven E. Shreve-Stochastic Calculus for Finance II_20150303200346.pdf]]
