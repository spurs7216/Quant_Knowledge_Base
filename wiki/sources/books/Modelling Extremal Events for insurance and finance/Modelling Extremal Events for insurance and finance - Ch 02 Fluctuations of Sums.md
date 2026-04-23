---
title: Modelling Extremal Events for insurance and finance - Ch 02 Fluctuations of Sums
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - probability
  - heavy-tails
  - limit-theory
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: chapter_scan
extraction_basis: chapter_scan_plus_rendered_theorem_pages_for_lln_stable_clt_fclt_and_renewal_via_pymupdf
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 02 Fluctuations of Sums
parent_source: "[[Modelling Extremal Events for insurance and finance]]"
sources:
  - "[[Modelling Extremal Events for insurance and finance]]"
  - "[[raw/math_statistics/Modelling Extremal Events for insurance and finance.pdf]]"
---
# Modelling Extremal Events for insurance and finance - Ch 02 Fluctuations of Sums

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: theorem-level deepening applied to the LLN and SLLN criteria, stable-law CLT logic, the functional CLT, and renewal or random-sum results that feed the insurance interpretation of later chapters.

## Role of the chapter

This chapter is the comparison asymptotic for the rest of the book. It explains what ordinary sums do before the book pivots to what maxima and exceedances do. That comparison matters because later EVT claims are easy to misuse if one forgets that sum limits, Gaussian limits, and stable limits are structurally different regimes.

## Section map

- laws of large numbers
- central limit problem and stable domains of attraction
- refinements of the CLT
- functional CLT and stable motion
- renewal counting and random sums

## Locally deepened subparts

### 1. The WLLN and SLLN separate weak from pathwise averaging

The chapter states a useful criterion for the centered weak law:
$$\bar X_n \xrightarrow{P} 0 \quad \Longleftrightarrow \quad n\Prob\!\paren{|X|>n}\to 0 \text{ and } \E\!\bracket{X\,\mathbf{1}_{\{|X|\le n\}}}\to 0.$$

For almost-sure convergence the threshold is stricter:
$$\bar X_n \xrightarrow{\text{a.s.}} \mu \quad \Longleftrightarrow \quad \E|X|<\infty.$$

The durable point is that even basic averaging already depends on tail integrability. Heavy tails change the law-of-large-numbers regime before they ever reach EVT.

### 2. The CLT chapter is really about stable domains of attraction

The book treats Gaussian limits as only one case inside the broader stable family. Properly centered and normalized sums satisfy
$$b_n^{-1}(S_n-a_n)\Rightarrow G_\alpha,$$
where $G_\alpha$ is an $\alpha$-stable limit law and
$$b_n=n^{1/\alpha}L(n)$$
for a slowly varying function $L$ when $\alpha<2$.

The key tail characterization is Pareto-type:
$$\bar F_+(x)\sim c_+ x^{-\alpha}L(x), \qquad \bar F_-(x)\sim c_- x^{-\alpha}L(x).$$

This matters later because the book's heavy-tail time-series and stable-process sections live in precisely the regimes where finite-variance Gaussian asymptotics are no longer the right default.

### 3. The functional CLT explains why Brownian motion appears and when it should not

For finite-variance data,
$$S_n^\circ(t)=\frac{S_{\lfloor nt\rfloor}-\lfloor nt\rfloor\mu}{\sigma\sqrt{n}} \Rightarrow B(t),$$
which is the Donsker invariance principle.

The chapter then extends the same logic to stable domains of attraction:
$$n^{-1/\alpha}L(n)^{-1}\paren{S_{\lfloor nt\rfloor}-a_{\lfloor nt\rfloor}} \Rightarrow Z_\alpha(t),$$
where $Z_\alpha$ is an $\alpha$-stable motion.

The durable use is interpretive: Brownian approximations are justified by finite-variance aggregation, while stable-motion approximations belong to the heavy-tail regime.

### 4. Renewal counting and random sums connect the probability theory back to insurance

For a renewal counting process
$$N(t)=\sup\{n\ge 1:T_n\le t\}, \qquad T_n=Y_1+\cdots+Y_n,$$
the chapter gives the large-time law
$$t^{-1}N(t)\xrightarrow{\text{a.s.}} \lambda=(\E Y)^{-1}.$$

That is the structural bridge to compound-claim models and randomly indexed sums like
$$S_{N(t)}=\sum_{i=1}^{N(t)} X_i.$$

This bridge matters because later ruin and reinsurance formulas repeatedly rely on claim counts and claim sums interacting on different scales.

## Scan-level remainder

- Berry-Esseen bounds, asymptotic expansions, and several proof details were scanned but not all rewritten line by line
- the chapter contains more classical limit theory than the rest of the book strictly needs, but the stable-law and renewal parts are load-bearing for the heavy-tail interpretation

## Quant relevance

This chapter matters for:

- deciding when Gaussian approximations are structurally wrong
- recognizing when stable scaling is more plausible than variance scaling
- understanding compound-claim and renewal models
- keeping maxima and exceedance asymptotics conceptually distinct from sum asymptotics

## Promotion candidates

- [[Convergence and Limit Theory]]
- [[Applied Probability]]
- a later durable note on stable and self-similar heavy-tail process models

## Related notes

- [[Convergence and Limit Theory]]
- [[Applied Probability]]
- [[Poisson Processes]]
- [[Modelling Extremal Events for insurance and finance - Ch 03 Fluctuations of Maxima]]
- [[Heavy-Tailed Time Series Analysis]]

## Sources

- [[Modelling Extremal Events for insurance and finance]]
- [[raw/math_statistics/Modelling Extremal Events for insurance and finance.pdf]]
