---
title: Stochastic Calculus for Finance II - Ch 08 American Derivative Securities
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - stochastic-calculus
  - american-options
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: toc_scan_plus_visual_read_of_stopping_time_definition_and_american_put_pages
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 08 American Derivative Securities
parent_source: "[[Stochastic Calculus for Finance II]]"
sources:
  - "[[Stochastic Calculus for Finance II]]"
  - "[[raw/math_statistics/Steven E. Shreve-Stochastic Calculus for Finance II_20150303200346.pdf]]"
---
# Stochastic Calculus for Finance II - Ch 08 American Derivative Securities

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed against the raw source.
- Pass 2: theorem-level extraction completed for stopping times, American put valuation, complementarity conditions, and the no-dividend American call result.

## Deepening Targets

- If later work needs a stronger optimal-stopping branch, deepen the Snell-envelope and free-boundary numerics beyond the current theorem spine.

## Deepened Subparts

- `8.2` stopping times
- `8.3` perpetual American put
- `8.4` finite-expiration American put
- `8.5` American call

## Role of the chapter

This chapter adds choice of exercise time to the pricing problem.

That changes the mathematics from pure replication and expectation into optimal stopping and free-boundary structure.

## Core mathematical objects

- stopping time
  $$\set{\tau \le t}\in\mathcal{F}(t), \qquad t \ge 0$$
- first passage time example
  $$\tau_m=\min\set{t\ge 0:X(t)=m}$$
- American put value
  $$v(t,x)=\max_{\tau \in \mathcal{T}_{t,T}}\widetilde{\mathbb{E}}\bracket{e^{-r(\tau-t)}\paren{K-S(\tau)}^+\given S(t)=x}$$
- complementarity system
  $$v(t,x)\ge (K-x)^+,$$
  $$rv-v_t-rxv_x-\frac{1}{2}\sigma^2x^2v_{xx}\ge 0,$$
  with equality in one of the two relations at each $(t,x)$

## Structural map of the chapter

- define stopping times rigorously
- analyze perpetual and finite-expiration American puts
- characterize stopping and continuation regions
- show when an American call collapses to its European counterpart

## Theorem and derivation spine

### Stopping times formalize admissible exercise rules

The rendered definition page states:

$$\set{\tau \le t}\in\mathcal{F}(t), \qquad t \ge 0.$$

That is the mathematical way of saying the exercise decision at time $t$ cannot use future information.

### American option pricing is a supremum over stopping times

The rendered finite-expiration section defines

$$v(t,x)=\max_{\tau \in \mathcal{T}_{t,T}}\widetilde{\mathbb{E}}\bracket{e^{-r(\tau-t)}\paren{K-S(\tau)}^+\given S(t)=x}.$$

That formula is the risk-neutral and optimal-stopping representation at the same time.

### The value solves complementarity rather than a single PDE everywhere

The rendered American-put page states the linear complementarity conditions

$$v(t,x)\ge (K-x)^+, $$
$$rv(t,x)-v_t(t,x)-rxv_x(t,x)-\frac{1}{2}\sigma^2x^2v_{xx}(t,x)\ge 0,$$

with equality in either the payoff condition or the PDE condition at each point.

This is the mathematical statement that the state space splits into:

- the stopping set
- the continuation set

### Early exercise depends on carry structure

The chapter's American-call section shows:

- for a non-dividend-paying stock, American and European calls have the same price
- when the underlying pays dividends, early exercise can become optimal

That is the economically important boundary between "American feature irrelevant" and "American feature real."

## Failure modes and misuse points

- calling any hitting rule a stopping time without filtration checks
- treating American pricing as European pricing plus a heuristic premium
- forgetting that the valuation problem is a free-boundary problem, not a single PDE on the whole state space
- applying no-dividend call intuition to dividend-paying or convenience-yield assets

## Quant research relevance

This chapter matters for:

- American equity and rates derivatives
- callable and cancelable contract logic
- optimal stopping under diffusion dynamics
- free-boundary numerics and exercise-boundary diagnostics

## What should be promoted out of this source note

- [[American Options and Optimal Stopping]]

## Related notes

- [[Stochastic Calculus for Finance II]]
- [[American Options and Optimal Stopping]]
- [[Risk-Neutral Pricing and Fundamental Theorems of Asset Pricing]]
- [[Derivatives Markets]]
- [[Monte Carlo Methods]]

## Sources

- [[Stochastic Calculus for Finance II]]
- [[raw/math_statistics/Steven E. Shreve-Stochastic Calculus for Finance II_20150303200346.pdf]]
