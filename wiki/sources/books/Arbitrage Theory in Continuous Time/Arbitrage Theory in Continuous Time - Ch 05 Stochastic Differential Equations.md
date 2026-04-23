---
title: Arbitrage Theory in Continuous Time - Ch 05 Stochastic Differential Equations
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - stochastic-calculus
  - chapter-digest
  - mathematical-finance
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: toc_scan_plus_utf8_text_extraction_and_targeted_rendered_theorem_pages
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 05 Stochastic Differential Equations
parent_source: "[[Arbitrage Theory in Continuous Time]]"
sources:
  - "[[Arbitrage Theory in Continuous Time]]"
  - "[[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]"
---
# Arbitrage Theory in Continuous Time - Ch 05 Stochastic Differential Equations

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: theorem-level extraction completed for existence and uniqueness, explicit GBM and linear-SDE solutions, generators, Feynman-Kac, and Kolmogorov equations.

## Deepening Targets

- If later work needs stronger diffusion numerics, deepen the link between infinitesimal generators and boundary-value problems.

## Deepened Subparts

- `5.1` stochastic differential equations
- `5.2` geometric Brownian motion
- `5.4` the infinitesimal operator
- `5.5` partial differential equations
- `5.6` the Kolmogorov equations

## Role of the chapter

This chapter turns the stochastic-calculus machinery into dynamic state models and then ties those dynamics back to PDEs.

## Core mathematical objects

- generic SDE
  $$
  dX_t=\mu(t,X_t)\,dt+\sigma(t,X_t)\,dW_t
  $$
- generator
  $$
  \mathcal{A}f=\mu f_x+\frac{1}{2}\sigma^2 f_{xx}
  $$
- geometric Brownian motion
  $$
  dX_t=\mu X_t\,dt+\sigma X_t\,dW_t
  $$
- Feynman-Kac representation
  $$
  F(t,x)=\E_{t,x}\bracket{\Phi(X_T)}
  $$
  for the associated boundary-value problem

## Structural map of the chapter

- state existence and uniqueness conditions
- solve benchmark SDEs explicitly
- define the infinitesimal operator
- connect diffusions to backward and forward PDEs

## Theorem and derivation spine

### Well-posedness comes first

The chapter starts with the standard existence-and-uniqueness theorem under Lipschitz and growth-type control conditions. That result is what makes later pricing and control equations meaningful rather than formal.

### GBM is the finance benchmark because it is explicitly solvable

The explicit GBM solution explains why lognormal equity models dominate the early pricing chapters and why Black-Scholes has analytic leverage.

### Feynman-Kac is the pricing bridge between PDEs and expectations

The rendered theorem page gives the stochastic representation:
$$
F(t,x)=\E_{t,x}\bracket{\Phi(X_T)}
$$
when $F$ solves the backward PDE
$$
F_t+\mu F_x+\frac{1}{2}\sigma^2 F_{xx}=0,
\qquad
F(T,x)=\Phi(x).
$$

This is one of the most durable results in the book. It reappears later inside derivative pricing, term-structure modeling, and control.

### The backward and forward Kolmogorov equations organize diffusion law evolution

The chapter makes explicit that diffusion dynamics can be studied either through test-function expectations or through transition densities. That dual viewpoint becomes important once rates and equilibrium models start changing state variables.

## Failure modes and misuse points

- using Feynman-Kac without checking the associated model or boundary conditions
- forgetting that the generator depends on the chosen dynamics and measure
- treating analytical PDE solutions as generic when most models do not admit them

## Quant research relevance

This chapter is load-bearing for:

- pricing PDEs
- term-structure PDEs
- HJB equations
- transition-density intuition for simulation and filtering

## What should be promoted out of this source note

- strengthen [[Ito Calculus and Stochastic Differential Equations]]
- support later rates and control notes rather than creating a separate durable note here

## Related notes

- [[Ito Calculus and Stochastic Differential Equations]]
- [[Stochastic Calculus]]
- [[Arbitrage Theory in Continuous Time - Ch 07 Arbitrage Pricing]]
- [[Arbitrage Theory in Continuous Time - Ch 25 Stochastic Optimal Control]]

## Sources

- [[Arbitrage Theory in Continuous Time]]
- [[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]

