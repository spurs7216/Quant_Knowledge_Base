---
title: All of Statistics - Ch 21 Smoothing Using Orthogonal Functions
type: source
status: chapter_ingested
updated: 2026-04-19
tags:
  - source
  - statistics
  - smoothing
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: full_source
extraction_basis: full_text
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 21 Smoothing Using Orthogonal Functions
parent_source: "[[All of Statistics]]"
sources:
  - "[[All of Statistics]]"
  - "[[raw/math_statistics/2004 - wasserman - all of statistics.pdf]]"
---
# All of Statistics - Ch 21 Smoothing Using Orthogonal Functions

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed against the raw source.
- Pass 2: deep rewrite completed on the basis-expansion viewpoint, coefficient-risk decomposition, and the wavelet thresholding logic.

## Deepening Targets

- Promote orthogonal-series and wavelet smoothing into durable notes once the vault needs a stronger bridge from statistics into signal processing and sparse denoising.

## Deepened Subparts

- Orthogonal-basis geometry, coefficient-risk decomposition, orthogonal-series density and regression estimation, and Haar-wavelet thresholding were rewritten at full note depth.

## Role of the chapter

This chapter develops an alternative smoothing paradigm. Instead of smoothing directly in the data domain, it transforms the unknown function into coefficients relative to an orthonormal basis and then smooths by truncating or thresholding those coefficients.

- represent the unknown function in an orthogonal basis
- estimate coefficients
- truncate or threshold the expansion

This is the series-estimation view of nonparametrics and a natural bridge to signal processing.

## Core mathematical objects

- orthonormal basis in `L2`
- series coefficients
- truncated estimator
- wavelet basis
- thresholding
- Parseval identity
- scaling and detail coefficients

## Orthogonal expansions

The early sections matter because they turn infinite-dimensional function estimation into coefficient estimation.

Equation (21.5) writes

`f(x) = sum_{j=1}^\infty beta_j phi_j(x)`

for an orthonormal basis `{\phi_j}` in `L^2`, with coefficients

`beta_j = integral f(x) phi_j(x) dx`.

Parseval's relation

`||f||^2 = sum_j beta_j^2`

is the key structural identity. It says approximation error in function space can be measured coefficient by coefficient.

This is conceptually important because it turns function estimation into coefficient estimation.

The chapter also makes an important smoothness claim: for the cosine basis, if `f` has many square-integrable derivatives, then high-frequency coefficients `beta_j` must decay. Smoothness is therefore encoded as coefficient sparsity or decay in the right basis.

## Density and regression estimation

### Theorems 21.4, 21.5, 21.8, 21.9

For density estimation, the coefficient estimator is

`\hat beta_j = (1 / n) sum_i phi_j(X_i)`.

Theorem 21.4 gives:

- `E(\hat beta_j) = beta_j`
- `Var(\hat beta_j) = sigma_j^2 / n`

so the coefficient estimates are unbiased and noisy at scale `n^{-1/2}`.

The truncated density estimator is

`\hat f(x) = sum_{j=1}^J \hat beta_j phi_j(x)`.

Theorem 21.5 gives the exact structure of its risk:

`R(J) = sum_{j=1}^J sigma_j^2 / n + sum_{j > J} beta_j^2`.

This is one of the cleanest bias-variance decompositions in the book.

- the first term is estimation variance from the retained coefficients
- the second term is truncation bias from the discarded tail

There is no mystery about smoothing here. Choosing `J` is directly choosing how many coordinates of the function to keep.

For regression on an approximately regular grid, the coefficient estimator becomes

`\hat beta_j = (1 / n) sum_i Y_i phi_j(x_i)`.

Theorem 21.8 gives approximate Normality:

`\hat beta_j approx N(beta_j, sigma^2 / n)`.

Theorem 21.9 gives the parallel risk decomposition:

`R(J) = J sigma^2 / n + sum_{j > J} beta_j^2`.

The main structural idea is:

- low-frequency coefficients often carry signal
- high-frequency coefficients often carry noise

So truncation is a smoothing device.

This chapter is powerful because it makes the bias-variance tradeoff almost embarrassingly explicit. Smoothing is coefficient selection.

## Confidence envelopes

The confidence bands again target the truncated object, not the full function:

- `f_J(x)` for density estimation
- `r_J(x)` for regression

Theorem 21.6 uses a chi-square bound on the retained coefficient error to produce a uniform band for `f_J`.

Theorem 21.11 does the same for regression, with local width

`a(x) = sqrt(sum_{j=1}^J phi_j(x)^2)`.

This is important because it shows that basis methods are not only about point estimation; they also support uncertainty quantification.

The same caveat as in Chapter 20 remains: the confidence band is for the smoothed target implied by truncation, not automatically for the true underlying function.

## Wavelets

### Theorems 21.13 and 21.15

Wavelets extend the orthogonal-function idea by adding localization in both scale and position.

This matters because many signals are not globally smooth. They have:

- local bursts
- edges
- multiscale structure

Wavelets can represent those features more efficiently than global polynomial or Fourier-like bases.

The Haar system is built from:

- a father wavelet / scaling function `phi`
- a mother wavelet `psi`
- shifted and rescaled details `psi_{j,k}(x) = 2^{j/2} psi(2^j x - k)`

Theorem 21.13 states that `{phi, W_0, W_1, ...}` is an orthonormal basis for `L^2(0,1)`.

The conceptual leap is that wavelets do not smooth by keeping only low frequencies. They smooth by retaining only coefficients that are large enough to look like signal.

The hard universal-threshold rule is:

- keep `D_{j,k}` if it exceeds the threshold
- set it to zero otherwise

The MAD-based noise estimator in equation (21.37) is important because it uses the finest-scale coefficients, where pure noise should dominate, and estimates `sigma` robustly.

Theorem 21.15 formalizes the intuition: if there is no true signal in the detail coefficients, universal thresholding kills them all with probability tending to one.

That is the chapter's sparsity principle in its simplest form.

## What the chapter is really teaching

The chapter is teaching that smoothing can be done either in the data domain or in a transformed coefficient domain.

Kernel methods smooth by local averaging.

Orthogonal and wavelet methods smooth by:

- decomposing
- shrinking or truncating
- reconstructing

The deeper lesson is basis dependence: what counts as "simple" or "smooth" depends on the coordinate system. Cosine bases reward global smoothness. Wavelets reward local sparsity and multiscale structure.

## Failure modes the chapter is trying to prevent

- assuming all function estimation should be kernel-based
- forgetting basis choice encodes assumptions about function structure
- using too many coefficients and fitting noise
- treating wavelets as a black-box transform rather than a sparsity device
- forgetting that confidence bands are for the truncated or thresholded target
- using a global basis on a spatially inhomogeneous signal without realizing what distortion that induces

## Quant research relevance

This chapter is directly relevant to quant and signal work:

- denoising high-frequency or microstructure-like signals
- sparse representation of latent curves or volatility shapes
- basis expansions for nonlinear regression or filtering
- multiscale decomposition of irregular market signals
- robust noise suppression when informative structure is local rather than global

It is also conceptually aligned with modern shrinkage and regularization thinking: represent, threshold, reconstruct.

## What should be promoted out of this source note

- a durable note on orthogonal-series estimators
- a durable note on wavelet smoothing
- a durable note on basis-domain bias-variance tradeoffs
- a durable note on coefficient decay as a smoothness signal

## Related notes

- [[All of Statistics]]
- [[All of Statistics - Ch 20 Nonparametric Curve Estimation]]
- [[Financial Signal Processing and Machine Learning]]
- [[Signal Processing Map]]

## Sources

- [[All of Statistics]]
- [[raw/math_statistics/2004 - wasserman - all of statistics.pdf]]
