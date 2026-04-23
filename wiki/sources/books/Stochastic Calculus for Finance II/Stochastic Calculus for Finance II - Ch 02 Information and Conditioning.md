---
title: Stochastic Calculus for Finance II - Ch 02 Information and Conditioning
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - stochastic-calculus
  - probability
  - conditioning
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: toc_scan_plus_visual_read_of_general_conditional_expectation_pages
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 02 Information and Conditioning
parent_source: "[[Stochastic Calculus for Finance II]]"
sources:
  - "[[Stochastic Calculus for Finance II]]"
  - "[[raw/math_statistics/Steven E. Shreve-Stochastic Calculus for Finance II_20150303200346.pdf]]"
---
# Stochastic Calculus for Finance II - Ch 02 Information and Conditioning

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed against the raw source.
- Pass 2: theorem-level extraction focused on sigma-algebras as information, independence, and general conditional expectation.

## Deepening Targets

- If later work needs a stronger optional-stopping proof spine, deepen the projection interpretation of conditional expectation and the filtration examples into a dedicated durable note.

## Deepened Subparts

- `2.1` information and sigma-algebras
- `2.2` independence
- `2.3` general conditional expectations

## Role of the chapter

This chapter supplies the language of evolving information.

Without it, Brownian motion is only a process and not a process relative to a filtration, martingales are only slogans, and stopping times are undefined.

## Core mathematical objects

- sub-sigma-algebra
  $$\mathcal{G}\subseteq \mathcal{F}$$
- conditional expectation
  $$Y=\mathbb{E}[X \given \mathcal{G}]$$
- defining property
  $$\int_A Y\,d\mathbb{P}=\int_A X\,d\mathbb{P}, \qquad A \in \mathcal{G}$$
- filtration
  $$\mathcal{F}(s)\subseteq \mathcal{F}(t), \qquad s \le t$$
- martingale prototype
  $$\mathbb{E}[M(t)\given\mathcal{F}(s)]=M(s)$$

## Structural map of the chapter

- sigma-algebras as information sets
- independence as informational irrelevance
- conditional expectation as the best estimate given the current information
- path from discrete-time conditioning formulas toward continuous-time filtrations

## Theorem and derivation spine

### Sigma-algebras encode what is known

The chapter recasts information as a sub-sigma-algebra $\mathcal{G}$.

That change in language is not cosmetic. It means "known at time $t$" becomes a measurable-structure statement rather than an English phrase.

### Conditional expectation is a measurable estimator

The rendered opening of Section `2.3` starts from the finite-horizon conditioning formula

$$\mathbb{E}_n[X](\omega_1\cdots\omega_n)=\sum_{\omega_{n+1}\cdots\omega_N} p^{\#H}q^{\#T} X(\omega_1\cdots\omega_N),$$

and then generalizes it to the continuous-time setting.

The abstract definition is:

- $Y=\mathbb{E}[X\given\mathcal{G}]$ is $\mathcal{G}$-measurable
- for every $A \in \mathcal{G}$,
  $$\int_A Y\,d\mathbb{P}=\int_A X\,d\mathbb{P}$$

That is the load-bearing statement because it is what survives when no density or finite partition exists.

### Independence collapses conditioning

If $X$ is independent of $\mathcal{G}$, then
$$\mathbb{E}[X\given\mathcal{G}]=\mathbb{E}X.$$

This is the exact mathematical version of "the information in $\mathcal{G}$ adds nothing about $X$."

### Tower and known-factor properties

The chapter's conditioning rules are the later working algebra of stochastic calculus:

$$\mathbb{E}\bracket{\mathbb{E}[X\given\mathcal{G}]}=\mathbb{E}X,$$
$$\mathbb{E}\bracket{\mathbb{E}[X\given\mathcal{G}_2]\given\mathcal{G}_1}=\mathbb{E}[X\given\mathcal{G}_1], \qquad \mathcal{G}_1 \subseteq \mathcal{G}_2,$$
$$\mathbb{E}[YX\given\mathcal{G}]=Y\mathbb{E}[X\given\mathcal{G}]$$
when $Y$ is $\mathcal{G}$-measurable.

Those identities become the engine of martingales, stopped processes, and pricing under changed measures.

## Failure modes and misuse points

- talking about "information at time $t$" without specifying the filtration
- using conditional expectation formulas that only hold under densities or finite partitions
- confusing independence of variables with independence of sigma-algebras
- forgetting that many later pricing identities are just conditional-expectation identities under a different measure

## Quant research relevance

This chapter is load-bearing for:

- martingale pricing formulas
- stopping-time definitions for American derivatives
- filtering, state estimation, and optional-sampling arguments
- change-of-measure calculations under Brownian and jump dynamics

## What should be promoted out of this source note

- a durable filtration and conditional-expectation note if optional stopping or filtering becomes a larger research branch

## Related notes

- [[Stochastic Calculus for Finance II]]
- [[Stochastic Calculus for Finance II - Ch 03 Brownian Motion]]
- [[Martingales]]
- [[American Options and Optimal Stopping]]
- [[General Gaussian Filtering and Smoothing]]

## Sources

- [[Stochastic Calculus for Finance II]]
- [[raw/math_statistics/Steven E. Shreve-Stochastic Calculus for Finance II_20150303200346.pdf]]
