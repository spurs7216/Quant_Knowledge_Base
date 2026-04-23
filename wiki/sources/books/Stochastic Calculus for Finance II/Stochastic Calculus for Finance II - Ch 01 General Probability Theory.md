---
title: Stochastic Calculus for Finance II - Ch 01 General Probability Theory
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - stochastic-calculus
  - probability
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: toc_scan_plus_visual_read_of_expectation_and_change_of_measure_pages
technical_depth: selective_deepen
ingest_stage: selective_deepen
chapter_or_section: Ch 01 General Probability Theory
parent_source: "[[Stochastic Calculus for Finance II]]"
sources:
  - "[[Stochastic Calculus for Finance II]]"
  - "[[raw/math_statistics/Steven E. Shreve-Stochastic Calculus for Finance II_20150303200346.pdf]]"
---
# Stochastic Calculus for Finance II - Ch 01 General Probability Theory

## Ingest Scope and Depth

- Ingest stage: `selective_deepen`
- Pass 1: full chapter scan completed against the raw source and rendered contents pages.
- Pass 2: deeper treatment focused on the measure-space definitions, expectation construction, convergence logic, and change-of-measure section that later supports risk-neutral pricing.

## Deepening Targets

- If later work needs a harder proof spine, deepen the monotone-convergence and Radon-Nikodym arguments into a durable measure-theory bridge note.

## Deepened Subparts

- `1.1` infinite probability spaces
- `1.3` expectations
- `1.4` convergence of integrals
- `1.6` change of measure

## Role of the chapter

This chapter supplies the measure-theoretic substrate beneath the rest of the book.

It is not where the finance starts, but it is where the notation becomes honest enough for continuous-time finance.

## Core mathematical objects

- probability space
  $$(\Omega,\mathcal{F},\mathbb{P})$$
- probability measure
  $$\mathbb{P}\paren{\Omega}=1, \qquad \mathbb{P}\paren{\bigcup_{n=1}^{\infty}A_n}=\sum_{n=1}^{\infty}\mathbb{P}(A_n)$$
  for disjoint $A_n$
- expectation under a density $f$
  $$\mathbb{E}g(X)=\int_{-\infty}^{\infty} g(x)f(x)\,dx$$
- change of measure density
  $$\widetilde{\mathbb{P}}(A)=\int_A Z(\omega)\,d\mathbb{P}(\omega), \qquad \mathbb{E}[Z]=1$$

## Structural map of the chapter

- infinite probability spaces instead of finite sample-space arithmetic
- random variables and distributions
- expectation as integration
- convergence theorems for passing limits through integrals
- change of measure as the precursor of risk-neutral pricing

## Theorem and derivation spine

### Probability spaces and countable additivity

The chapter starts by moving from finite combinatorics to the measurable-space definition.

The rendered opening pages state the two load-bearing definitions:

$$\emptyset \in \mathcal{F}, \qquad A \in \mathcal{F} \Rightarrow A^c \in \mathcal{F}, \qquad A_n \in \mathcal{F} \Rightarrow \bigcup_{n=1}^{\infty}A_n \in \mathcal{F},$$

and then define a probability measure by

$$\mathbb{P}(\Omega)=1, \qquad \mathbb{P}\paren{\bigcup_{n=1}^{\infty}A_n}=\sum_{n=1}^{\infty}\mathbb{P}(A_n)$$

for disjoint sets.

Those definitions matter later because filtrations, stopping times, and Radon-Nikodym densities all live on top of this measurable structure.

### Expectation is integration, not weighted averaging by cases

The chapter builds expectation from simple functions and then extends it to Borel-measurable functions.

The rendered page near the end of Section `1.5` shows the extension step:

$$\mathbb{E}g_n(X)=\int_{-\infty}^{\infty} g_n(x)f(x)\,dx,$$

and then passes to the limit with the Monotone Convergence Theorem to obtain the full formula for general nonnegative measurable $g$.

That derivation matters later because every pricing formula is an expectation under either $\mathbb{P}$ or $\widetilde{\mathbb{P}}$.

### Change of measure is the pricing hinge

Section `1.6` introduces the density process idea in static form. The rendered page opens the section by warning that on uncountable spaces it is not meaningful to divide point probabilities, and instead one defines the new measure through a density:

$$\widetilde{\mathbb{P}}(A)=\int_A Z(\omega)\,d\mathbb{P}(\omega).$$

Then expectations under the new measure satisfy

$$\widetilde{\mathbb{E}}X=\mathbb{E}[XZ], \qquad \mathbb{E}X=\widetilde{\mathbb{E}}\bracket{\frac{X}{Z}}$$

when $Z>0$ almost surely.

That is the exact structural precursor of the risk-neutral reweighting formula in Chapter 5.

## Failure modes and misuse points

- treating Chapter 1 as disposable because the formulas look generic
- carrying finite-state intuition into uncountable spaces without sigma-algebra discipline
- using change-of-measure notation without checking positivity and integrability of the density
- forgetting that later martingale and pricing results are statements about integrals, not heuristics

## Quant research relevance

This chapter matters whenever a later note writes:

- a conditional expectation
- a Radon-Nikodym derivative
- a risk-neutral pricing identity
- an almost-sure statement for a pathwise model

## What should be promoted out of this source note

- the Radon-Nikodym and expectation-reweighting logic into a continuous-time pricing note

## Related notes

- [[Stochastic Calculus for Finance II]]
- [[Stochastic Calculus for Finance II - Ch 02 Information and Conditioning]]
- [[Risk-Neutral Pricing and Fundamental Theorems of Asset Pricing]]
- [[Probability as Extended Logic]]
- [[Applied Probability]]

## Sources

- [[Stochastic Calculus for Finance II]]
- [[raw/math_statistics/Steven E. Shreve-Stochastic Calculus for Finance II_20150303200346.pdf]]
