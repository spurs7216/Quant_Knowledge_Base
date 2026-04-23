---
title: Modelling Extremal Events for insurance and finance - Ch 01 Risk Theory
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - extreme-value-theory
  - heavy-tails
  - risk-theory
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: chapter_scan
extraction_basis: chapter_scan_plus_rendered_theorem_pages_for_cramer_lundberg_and_heavy_tail_ruin_via_pymupdf
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 01 Risk Theory
parent_source: "[[Modelling Extremal Events for insurance and finance]]"
sources:
  - "[[Modelling Extremal Events for insurance and finance]]"
  - "[[raw/math_statistics/Modelling Extremal Events for insurance and finance.pdf]]"
---
# Modelling Extremal Events for insurance and finance - Ch 01 Risk Theory

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: theorem-level deepening applied to the reserve-process setup, the Cramer-Lundberg theorem, the integrated-tail representation of ruin, and the heavy-tail class lattice used later in the book.

## Role of the chapter

This chapter is the application-facing entry point for the whole book. It turns extremes into a solvency problem and makes the central regime split explicit: small claims lead to exponential ruin asymptotics, while large claims lead to integrated-tail or one-big-jump asymptotics.

## Section map

- the classical reserve process and ruin event
- Cramer-Lundberg estimate and adjustment coefficient
- ruin theory for heavy-tailed distributions
- large-claim tail classes and when the small-claim theorem fails

## Locally deepened subparts

### 1. Ruin is a path event for the reserve process

The reserve process is
$$U(t)=u+ct-S(t),$$
with initial capital $u$, premium rate $c$, and cumulative claims $S(t)$.

Finite- and infinite-horizon ruin are defined by
$$\psi(u,T)=\Prob\!\paren{\inf_{0\le t\le T} U(t)<0}, \qquad \psi(u)=\psi(u,\infty).$$

The basic actuarial point is that positive drift is only a first filter. Even when the net-profit condition holds, large claims can still dominate solvency.

### 2. The Cramer-Lundberg theorem gives the small-claim regime

Let
$$F_I(x)=\frac{1}{\mu}\int_0^x \bar F(y)\,\mathrm{d}y$$
be the integrated tail distribution and let
$$\rho=\frac{c}{\lambda\mu}-1>0$$
be the safety loading.

The chapter's key theorem states that if there exists $\nu>0$ such that
$$\hat f_I(-\nu)=\int_0^\infty e^{\nu x}\,\mathrm{d}F_I(x)=1+\rho,$$
then
$$\psi(u)\le e^{-\nu u},$$
and, under the stronger moment condition
$$\int_0^\infty x e^{\nu x}\bar F(x)\,\mathrm{d}x<\infty,$$
one has the sharper asymptotic
$$e^{\nu u}\psi(u)\to C.$$

This is the classical small-claim regime: ruin decays exponentially because the claim tail is light enough to support an adjustment coefficient.

### 3. Heavy-tailed ruin is controlled by the integrated tail

Once the small-claim condition fails, the chapter switches to the large-claim regime. The reusable asymptotic is:
$$\psi(u)\sim \frac{1}{\rho}\,\bar F_I(u), \qquad u\to\infty,$$
whenever the integrated tail is subexponential.

This is the first durable place where the book makes the one-big-jump logic operational: large-loss ruin is governed by the integrated tail mass above $u$, not by an exponential decay rate.

### 4. The heavy-tail class lattice is structurally important

The chapter does not treat regular variation, dominated variation, and subexponentiality as synonyms. Instead it builds the practical ladder:

- regular variation gives a strong Pareto-type regime
- subexponentiality gives the one-big-jump closure
- dominated variation is a convenient sufficient route into the heavy-tail ruin theorem

For regularly varying tails,
$$\bar F(x)=x^{-\alpha}L(x),$$
the chapter's convolution logic gives
$$\overline{F^{*n}}(x)\sim n\bar F(x), \qquad x\to\infty,$$
which is the reusable bridge from tail classes to ruin asymptotics.

## Scan-level remainder

- actuarial premium-principle discussion and some renewal-theoretic proof details were scanned rather than rewritten line by line
- the chapter's catalog of concrete claim-size families was preserved conceptually, not as a copied table

## Quant relevance

This chapter matters for:

- solvency and tail-capital logic
- catastrophic-loss risk where one jump dominates
- separating exponential from heavy-tail ruin regimes
- deciding whether classical Lundberg adjustments are structurally defensible

## Promotion candidates

- [[Regular Variation and Heavy-Tailed Distributions]]
- [[Ruin Asymptotics with Small and Large Claims]]

## Related notes

- [[Modelling Extremal Events for insurance and finance]]
- [[Regular Variation and Heavy-Tailed Distributions]]
- [[Ruin Asymptotics with Small and Large Claims]]
- [[Applied Probability]]

## Sources

- [[Modelling Extremal Events for insurance and finance]]
- [[raw/math_statistics/Modelling Extremal Events for insurance and finance.pdf]]
