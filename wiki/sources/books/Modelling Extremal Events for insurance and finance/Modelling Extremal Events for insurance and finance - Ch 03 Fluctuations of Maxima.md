---
title: Modelling Extremal Events for insurance and finance - Ch 03 Fluctuations of Maxima
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - extreme-value-theory
  - maxima
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: pymupdf_scan_of_fisher_tippett_and_mda_sections_plus_norming_examples
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 03 Fluctuations of Maxima
parent_source: "[[Modelling Extremal Events for insurance and finance]]"
sources:
  - "[[Modelling Extremal Events for insurance and finance]]"
  - "[[raw/math_statistics/Modelling Extremal Events for insurance and finance.pdf]]"
---
# Modelling Extremal Events for insurance and finance - Ch 03 Fluctuations of Maxima

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: theorem-level extraction completed for max-stable laws, Fisher-Tippett classification, maximum domains of attraction, and the role of regular variation in norming maxima.

## Deepening Targets

- If the vault later needs stronger proof detail, deepen the convergence-to-types argument and the von Mises conditions into a dedicated durable note.

## Deepened Subparts

- max-stable laws
- Fisher-Tippett theorem
- maximum domains of attraction
- norming constants and worked distribution examples

## Role of the chapter

This is the first core EVT chapter. It does for maxima what the central-limit chapter does for sums: it classifies the only possible nondegenerate limit laws after affine normalization.

## Core mathematical objects

- maxima
  $$M_n=\max(X_1,\dots,X_n)$$
- affine normalization
  $$\frac{M_n-d_n}{c_n}$$
- max stability
  $$\max(Y_1,\dots,Y_n)\overset{d}=c_nY+d_n$$
- maximum domain of attraction
  $$F\in \mathrm{MDA}(H) \quad \Longleftrightarrow \quad \frac{M_n-d_n}{c_n}\Rightarrow H$$

## Structural map of the chapter

- max-stable laws as the fixed-point class for maxima
- Fisher-Tippett classification
- domains of attraction and norming constants
- worked examples for exponential, Cauchy, normal, and bounded-support tails

## Theorem and derivation spine

### Max-stable laws are exactly the possible limits of normalized maxima

The chapter first defines max stability and then states the limit-property theorem: the class of max-stable laws coincides with the class of all nondegenerate limits of properly normalized maxima of iid variables.

That is the maximum-side counterpart of stable laws for sums.

### Fisher-Tippett theorem

If there exist constants $c_n>0$ and $d_n\in\R$ such that
$$\frac{M_n-d_n}{c_n}\Rightarrow H,$$
for a nondegenerate limit law $H$, then $H$ must belong to one of three types:

- Frechet
  $$\Phi_\alpha(x)=\exp\paren{-x^{-\alpha}}, \qquad x>0$$
- Weibull
  $$\Psi_\alpha(x)=\exp\paren{-\paren{-x}^{\alpha}}, \qquad x\le 0$$
- Gumbel
  $$\Lambda(x)=\exp\paren{-e^{-x}}, \qquad x\in\R$$

This is the load-bearing classification theorem for univariate EVT.

### Domain-of-attraction criterion

The chapter then turns the classification into a usable modeling question:
$$F\in \mathrm{MDA}(H) \iff n\bar F(c_nx+d_n)\to -\log H(x)$$
for suitable norming constants.

This criterion is what converts tail asymptotics into a statement about maxima.

### Regular variation implies Frechet attraction

For heavy-tailed distributions with
$$\bar F(x)=x^{-\alpha}L(x), \qquad \alpha>0,$$
the chapter places $F$ in the Frechet domain of attraction. The durable conclusion is that regular variation is the clean route from tail-index language to extreme-value limits for block maxima.

### Norming constants are model-dependent

The chapter's examples show why one should not treat normalization as cosmetic:

- exponential tails lead to Gumbel normalization with logarithmic centering
- Cauchy-type tails lead to Frechet scaling
- bounded-right-support models fall into Weibull attraction
- the normal law is in the Gumbel domain, but with subtle norming constants

## Failure modes and misuse points

- fitting a block-maxima model without checking which domain-of-attraction story is plausible
- calling every heavy right tail Frechet without looking at support or effective tail shape
- treating norming constants as arbitrary nuisance terms
- forgetting that maxima have a different asymptotic grammar from sums

## Quant research relevance

This chapter matters whenever the research target is a block maximum or worst-case event:

- annual or monthly risk maxima
- stress-test envelopes
- extreme-loss calibration
- return-level estimation

## What should be promoted out of this source note

- [[Extreme Value Theory for Maxima and Threshold Exceedances]]
- [[Regular Variation and Heavy-Tailed Distributions]]

## Related notes

- [[Modelling Extremal Events for insurance and finance]]
- [[Modelling Extremal Events for insurance and finance - Ch 04 Fluctuations of Upper Order Statistics]]
- [[Extreme Value Theory for Maxima and Threshold Exceedances]]
- [[Regular Variation and Heavy-Tailed Distributions]]

## Sources

- [[Modelling Extremal Events for insurance and finance]]
- [[raw/math_statistics/Modelling Extremal Events for insurance and finance.pdf]]
