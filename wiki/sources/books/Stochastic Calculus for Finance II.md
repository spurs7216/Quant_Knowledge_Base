---
title: Stochastic Calculus for Finance II
type: source
status: overview_source
updated: 2026-04-22
tags:
  - source
  - book
  - stochastic-calculus
  - mathematical-finance
  - continuous-time
source_type: book
source_class: overview_source
read_scope: full_source
source_author:
  - Steven E. Shreve
source_year: 2004
source_order: 13
domain: quant-finance
extraction_basis: rendered_table_of_contents_plus_visual_read_of_selected_theorem_pages_via_pymupdf_page_images
technical_depth: deep
parent_source: null
sources:
  - "[[raw/math_statistics/Steven E. Shreve-Stochastic Calculus for Finance II_20150303200346.pdf]]"
---
# Stochastic Calculus for Finance II

## Citation / metadata

- Author: Steven E. Shreve
- Year: 2004
- Source type: textbook
- Read scope: `full_source`
- Shelf role: first full continuous-time finance spine on the math/statistics shelf
- Raw source: [[raw/math_statistics/Steven E. Shreve-Stochastic Calculus for Finance II_20150303200346.pdf]]

## Why this book matters

This is the clean bridge from discrete-time martingale intuition into continuous-time finance.

For the vault, the durable value is not only Black-Scholes literacy. The book gives the reusable mathematical grammar behind:

- filtrations and conditional expectation in continuous time
- Brownian motion and quadratic variation
- Ito integration, Ito-Doeblin calculus, and stochastic differential equations
- risk-neutral pricing, hedging, and the fundamental theorems of asset pricing
- PDE, numeraire, term-structure, and jump-process views of the same pricing logic

It is the right book to ingest before pushing deeper into [[Arbitrage Theory in Continuous Time]].

## Reading logic from the source

The book was ingested under the current three-step rule:

1. full chapter scan across all eleven chapters using the rendered table of contents and visually read raw pages
2. theorem-level deepening on the measure-theoretic, Brownian, Ito, pricing, PDE, American-exercise, numeraire, term-structure, and jump-process core
3. promotion of the strongest reusable material into durable stochastic-calculus and continuous-time-finance notes

The parent note stays thin. The technical detail lives in the chapter shelf and promoted notes.

## Stage map

- `selective_deepen`: [[Stochastic Calculus for Finance II - Ch 01 General Probability Theory]]
- `deep`: [[Stochastic Calculus for Finance II - Ch 02 Information and Conditioning]]
- `deep`: [[Stochastic Calculus for Finance II - Ch 03 Brownian Motion]]
- `deep`: [[Stochastic Calculus for Finance II - Ch 04 Stochastic Calculus]]
- `deep`: [[Stochastic Calculus for Finance II - Ch 05 Risk-Neutral Pricing]]
- `deep`: [[Stochastic Calculus for Finance II - Ch 06 Connections with Partial Differential Equations]]
- `selective_deepen`: [[Stochastic Calculus for Finance II - Ch 07 Exotic Options]]
- `deep`: [[Stochastic Calculus for Finance II - Ch 08 American Derivative Securities]]
- `deep`: [[Stochastic Calculus for Finance II - Ch 09 Change of Numeraire]]
- `deep`: [[Stochastic Calculus for Finance II - Ch 10 Term-Structure Models]]
- `deep`: [[Stochastic Calculus for Finance II - Ch 11 Introduction to Jump Processes]]

## Chapter shelf

- [[Stochastic Calculus for Finance II - Ch 01 General Probability Theory]]
- [[Stochastic Calculus for Finance II - Ch 02 Information and Conditioning]]
- [[Stochastic Calculus for Finance II - Ch 03 Brownian Motion]]
- [[Stochastic Calculus for Finance II - Ch 04 Stochastic Calculus]]
- [[Stochastic Calculus for Finance II - Ch 05 Risk-Neutral Pricing]]
- [[Stochastic Calculus for Finance II - Ch 06 Connections with Partial Differential Equations]]
- [[Stochastic Calculus for Finance II - Ch 07 Exotic Options]]
- [[Stochastic Calculus for Finance II - Ch 08 American Derivative Securities]]
- [[Stochastic Calculus for Finance II - Ch 09 Change of Numeraire]]
- [[Stochastic Calculus for Finance II - Ch 10 Term-Structure Models]]
- [[Stochastic Calculus for Finance II - Ch 11 Introduction to Jump Processes]]

## Core objects and modeling vocabulary

- filtration
  $$\set{\mathcal{F}(t)}_{t \ge 0}$$
- conditional expectation
  $$\mathbb{E}[X \given \mathcal{F}(t)]$$
- Brownian motion
  $$W(0)=0, \qquad W(t)-W(s) \sim \mathcal{N}(0,t-s)$$
- quadratic variation
  $$[W,W](T)=T$$
- Ito process
  $$dX(t)=\theta(t)\,dt+\Gamma(t)\,dW(t)$$
- Ito-Doeblin formula
  $$df(t,X(t))=f_t\,dt+f_x\,dX(t)+\frac{1}{2}f_{xx}\,dX(t)\,dX(t)$$
- self-financing replication
  $$dX(t)=\Delta(t)\,dS(t)+r\paren{X(t)-\Delta(t)S(t)}\,dt$$
- Radon-Nikodym density
  $$Z=\frac{d\widetilde{\mathbb{P}}}{d\mathbb{P}}$$
- risk-neutral pricing formula
  $$V(t)=\frac{1}{D(t)}\widetilde{\mathbb{E}}\bracket{D(T)V(T)\given\mathcal{F}(t)}$$
- bond and forward measure objects
  $$B(t,T), \qquad \operatorname{Fwd}_S(t,T)=\frac{S(t)}{B(t,T)}$$
- compensated Poisson process
  $$M(t)=N(t)-\lambda t$$

## Main themes

- Continuous-time finance is built on information structure first and pricing formulas second.
- Brownian motion matters because its quadratic variation changes calculus itself, not just the distribution of shocks.
- Risk-neutral pricing is not a separate trick from PDE pricing or numeraire change. They are different representations of the same no-arbitrage logic.
- American exercise, term-structure modeling, and jumps force the researcher to think in stopping-time, measure-change, and compensator language rather than only closed-form formulas.
- The book is strongest when read as a reusable modeling grammar, not as a derivatives cookbook.

## Promoted durable notes

- [[Brownian Motion and Quadratic Variation]]
- [[Ito Calculus and Stochastic Differential Equations]]
- [[Risk-Neutral Pricing and Fundamental Theorems of Asset Pricing]]
- [[American Options and Optimal Stopping]]
- [[Change of Numeraire and Forward Measures]]
- [[Term-Structure Models]]
- [[Jump Processes and Compensators]]
- [[Stochastic Calculus]]

## Next promotion targets

- a durable note on Brownian bridge and Monte Carlo path conditioning
- a durable note on free-boundary numerics for American puts and optimal stopping
- a durable note on HJM drift restrictions, calibration, and forward-LIBOR market models
- a durable note on jump-diffusion pricing and Doleans-Dade exponentials

## Caveats

- The book is self-contained, but many proofs still lean on the simpler discrete-time analogies from Volume I. The vault notes keep the continuous-time statements explicit without pretending every proof has been fully reconstructed.
- The raw PDF has weak text encoding, so the theorem pass was grounded in rendered page images rather than trusting broken extraction text.
- The book is mathematically rigorous for complete-market diffusion finance, but it is not the final word on incomplete markets, transaction costs, or market microstructure.

## Related notes

- [[Stochastic Calculus]]
- [[Applied Probability]]
- [[Martingales]]
- [[Diffusion Processes]]
- [[Derivatives Markets]]
- [[Arbitrage Theory in Continuous Time]]
- [[Math Map]]
- [[Finance Map]]

## Sources

- [[raw/math_statistics/Steven E. Shreve-Stochastic Calculus for Finance II_20150303200346.pdf]]
