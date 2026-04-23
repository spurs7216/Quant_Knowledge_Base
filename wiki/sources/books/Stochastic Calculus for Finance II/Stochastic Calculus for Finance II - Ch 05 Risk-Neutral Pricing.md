---
title: Stochastic Calculus for Finance II - Ch 05 Risk-Neutral Pricing
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - stochastic-calculus
  - risk-neutral-pricing
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: toc_scan_plus_visual_read_of_radon_nikodym_girsanov_and_ftap_pages
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 05 Risk-Neutral Pricing
parent_source: "[[Stochastic Calculus for Finance II]]"
sources:
  - "[[Stochastic Calculus for Finance II]]"
  - "[[raw/math_statistics/Steven E. Shreve-Stochastic Calculus for Finance II_20150303200346.pdf]]"
---
# Stochastic Calculus for Finance II - Ch 05 Risk-Neutral Pricing

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed against the raw source.
- Pass 2: theorem-level extraction completed for Radon-Nikodym reweighting, Girsanov, martingale representation, and the fundamental theorems of asset pricing.

## Deepening Targets

- If later work needs a stronger incomplete-market branch, deepen the sections where existence and uniqueness of the risk-neutral measure can fail.

## Deepened Subparts

- `5.2` risk-neutral measure
- `5.3` martingale representation theorem
- `5.4` fundamental theorems of asset pricing

## Role of the chapter

This chapter turns stochastic calculus into pricing theory.

The core claim is that no-arbitrage pricing works by moving to a measure under which discounted traded assets are martingales and then representing hedges with martingale integrals.

## Core mathematical objects

- Radon-Nikodym density
  $$Z=\frac{d\widetilde{\mathbb{P}}}{d\mathbb{P}}$$
- expectation reweighting
  $$\widetilde{\mathbb{E}}X=\mathbb{E}[XZ]$$
- Girsanov exponential
  $$Z(t)=\exp\bracket{-\int_0^t \theta(u)\,dW(u)-\frac{1}{2}\int_0^t \theta^2(u)\,du}$$
- Brownian shift under the new measure
  $$\widetilde{W}(t)=W(t)+\int_0^t \theta(u)\,du$$
- risk-neutral pricing identity
  $$V(t)=\frac{1}{D(t)}\widetilde{\mathbb{E}}\bracket{D(T)V(T)\given\mathcal{F}(t)}$$

## Structural map of the chapter

- build the risk-neutral measure in the one-stock model
- prove martingale representation for Brownian filtrations
- extend to multiple stocks and the two fundamental theorems
- treat dividends, forwards, and futures as applications

## Theorem and derivation spine

### Reweighting expectations is the base operation

The rendered opening of Section `5.2` restates the change of measure formulas in pricing notation:

$$\widetilde{\mathbb{P}}(A)=\int_A Z(\omega)\,d\mathbb{P}(\omega),$$
$$\widetilde{\mathbb{E}}X=\mathbb{E}[XZ],$$
$$\mathbb{E}X=\widetilde{\mathbb{E}}\bracket{\frac{X}{Z}}.$$

This is not yet risk-neutral pricing. It is only the algebraic foundation that makes the risk-neutral measure possible.

### Girsanov turns drift into measure choice

The multidimensional theorem page states:

$$Z(t)=\exp\bracket{-\int_0^t \theta(u)\cdot dW(u)-\frac{1}{2}\int_0^t \norm{\theta(u)}^2\,du},$$
$$\widetilde{W}(t)=W(t)+\int_0^t \theta(u)\,du.$$

Under the probability measure defined by $Z(T)$, the process $\widetilde{W}(t)$ is Brownian motion.

That theorem is the bridge from the actual drift to the risk-neutral drift.

### Discounted asset prices must be martingales under the pricing measure

Once the drift is removed appropriately, discounted traded assets satisfy the martingale property under $\widetilde{\mathbb{P}}$.

The pricing formula is then

$$V(t)=\frac{1}{D(t)}\widetilde{\mathbb{E}}\bracket{D(T)V(T)\given\mathcal{F}(t)}.$$

This identity is the valuation side. The martingale representation theorem is the hedging side.

### Fundamental theorems: existence and uniqueness

The chapter's fundamental-theorems section uses Girsanov plus martingale representation to show:

- existence of a risk-neutral measure implies no arbitrage
- uniqueness of the risk-neutral measure in the Brownian model implies completeness and unique hedge prices

In other words, pricing is a theorem only when the market and filtration assumptions are strong enough.

## Failure modes and misuse points

- talking about "risk-neutral expectation" without specifying the numeraire and measure change
- using the pricing measure for forecasting rather than valuation
- assuming completeness because the model is continuous-time
- forgetting that the representation theorem is the hidden source of the hedge

## Quant research relevance

This chapter is central for:

- derivative pricing
- hedging arguments
- linking PDE and expectation representations
- understanding when a model gives a unique price and when it does not

## What should be promoted out of this source note

- [[Risk-Neutral Pricing and Fundamental Theorems of Asset Pricing]]
- cross-link updates in [[Stochastic Calculus]]

## Related notes

- [[Stochastic Calculus for Finance II]]
- [[Stochastic Calculus for Finance II - Ch 04 Stochastic Calculus]]
- [[Stochastic Calculus for Finance II - Ch 06 Connections with Partial Differential Equations]]
- [[Risk-Neutral Pricing and Fundamental Theorems of Asset Pricing]]
- [[Derivatives Markets]]

## Sources

- [[Stochastic Calculus for Finance II]]
- [[raw/math_statistics/Steven E. Shreve-Stochastic Calculus for Finance II_20150303200346.pdf]]
