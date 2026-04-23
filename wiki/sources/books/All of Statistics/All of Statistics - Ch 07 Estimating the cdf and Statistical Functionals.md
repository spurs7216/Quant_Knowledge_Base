---
title: All of Statistics - Ch 07 Estimating the cdf and Statistical Functionals
type: source
status: chapter_ingested
updated: 2026-04-19
tags:
  - source
  - statistics
  - empirical-process
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: full_source
extraction_basis: full_text
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 07 Estimating the cdf and Statistical Functionals
parent_source: "[[All of Statistics]]"
sources:
  - "[[All of Statistics]]"
  - "[[raw/math_statistics/2004 - wasserman - all of statistics.pdf]]"
---
# All of Statistics - Ch 07 Estimating the cdf and Statistical Functionals

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed against the raw source.
- Pass 2: the chapter was rewritten around the empirical cdf, Glivenko-Cantelli, DKW, plug-in estimation, and the functional examples that matter most for later nonparametric and quant work.

## Deepening Targets

- If this source becomes the main nonparametric estimation reference, deepen the asymptotics of sample quantiles and add a durable note on functional delta methods above the current plug-in spine.

## Deepened Subparts

- Whole chapter reworked at theorem-oriented depth.

## Role of the chapter

This chapter is one of the most important conceptual turns in the book. Up to Chapter 6, the inference story is mostly phrased in terms of parameters. Chapter 7 says: estimate the whole distribution first, and then derive many quantities of interest as functionals of that estimated distribution.

The organizing move is:

1. treat the unknown population law `F` as the primitive object
2. estimate it by the empirical cdf `hat F_n`
3. represent targets as `T(F)`
4. estimate them by `T(hat F_n)`

That is the plug-in principle.

## Core mathematical objects

- empirical cdf `hat F_n(x) = n^{-1} sum_i I(X_i <= x)`
- pointwise law at fixed `x`
- uniform deviation `sup_x |hat F_n(x) - F(x)|`
- statistical functional `T(F)`
- plug-in estimator `T(hat F_n)`
- linear functional `int r(x) dF(x)`
- sample quantile `hat F_n^{-1}(p)`

The chapter moves from a function estimator to scalar estimators built out of it.

## Structural map of the chapter

The chapter has two main sections:

1. the empirical distribution function
2. statistical functionals and plug-in estimators

The first section studies the quality of `hat F_n` as an estimator of `F`. The second shows that many familiar estimators are simply evaluations of functionals at `hat F_n`.

## Definition 7.1: empirical distribution function

The empirical cdf is

`hat F_n(x) = n^{-1} sum_i I(X_i <= x)`.

At each fixed `x`, this is just the sample mean of Bernoulli indicators with success probability `F(x)`.

That observation is doing most of the mathematical work in the first half of the chapter.

## Theorem 7.3: pointwise behavior of the empirical cdf

At any fixed `x`,

- `E hat F_n(x) = F(x)`
- `Var hat F_n(x) = F(x) (1 - F(x)) / n`
- `mse = F(x) (1 - F(x)) / n -> 0`
- `hat F_n(x) ->^P F(x)`

### Why this theorem is easy and important

The theorem follows because `I(X_i <= x)` are iid Bernoulli with mean `F(x)`.

So:

- unbiasedness follows immediately
- variance is the Bernoulli variance divided by `n`
- consistency follows from either direct calculation or LLN logic

The theorem is mathematically simple but conceptually major. It says every fixed cdf value can be estimated like a binomial proportion.

## Theorem 7.4: Glivenko-Cantelli

`sup_x |hat F_n(x) - F(x)| ->^P 0`.

The book notes that a stronger almost sure statement also holds.

### Why this theorem is much stronger than Theorem 7.3

Pointwise consistency says:

- for each fixed `x`, `hat F_n(x)` converges to `F(x)`

Uniform consistency says:

- the whole estimated cdf converges to the whole true cdf at once

This is a dramatic strengthening. It says `hat F_n` is not merely right at selected points. It is globally close as a function.

### Why this matters

Uniform convergence is what makes plug-in estimation powerful. If the whole cdf is close, then many functionals of the cdf should also be close, especially continuous ones.

## Theorem 7.5: DKW inequality

For every `eps > 0`,

`P(sup_x |F(x) - hat F_n(x)| > eps) <= 2 exp(-2 n eps^2)`.

### Why this theorem is special

The DKW inequality is both:

- nonasymptotic
- uniform in `x`

That is unusually strong. It gives finite-sample control for the entire cdf estimator, not just one coordinate.

### Confidence bands

Setting

`eps_n = sqrt((1 / (2n)) log(2 / alpha))`

and defining

- `L(x) = max(hat F_n(x) - eps_n, 0)`
- `U(x) = min(hat F_n(x) + eps_n, 1)`

yields a nonparametric `1 - alpha` confidence band for `F`:

`P(L(x) <= F(x) <= U(x) for all x) >= 1 - alpha`.

This is a very different object from a pointwise confidence interval. It is a simultaneous confidence statement over the whole function.

## Statistical functionals

### Definition 7.7

If `theta = T(F)`, define the plug-in estimator by

`hat theta_n = T(hat F_n)`.

This definition is one of the most important ideas in the entire book.

It says:

- estimation is not a zoo of disconnected formulas
- many estimators are simply functionals evaluated at the empirical law

### Definition 7.8: linear functionals

If

`T(F) = int r(x) dF(x)`

for some function `r`, then `T` is called a linear functional.

### Theorem 7.9

For a linear functional,

`T(hat F_n) = int r(x) d hat F_n(x) = n^{-1} sum_i r(X_i)`.

### Why this theorem matters

This theorem turns many ordinary sample formulas into conceptual consequences of the plug-in rule.

Examples:

- mean: `r(x) = x`
- second moment: `r(x) = x^2`
- many empirical averages

So the sample average is not an isolated trick. It is the plug-in estimator for a linear functional.

## Important examples

### Mean

For

`mu = int x dF(x)`,

the plug-in estimator is

`hat mu = int x d hat F_n(x) = bar X_n`.

This is the cleanest example of the plug-in principle.

### Variance

Variance is nonlinear in `F` because it depends on both first and second moments:

`sigma^2 = int x^2 dF(x) - (int x dF(x))^2`.

Plugging in `hat F_n` gives

`hat sigma^2 = n^{-1} sum_i (X_i - bar X_n)^2`.

This is close to, but not exactly equal to, the conventional sample variance with denominator `n - 1`. The chapter is reminding the reader that different estimators can target the same parameter while differing by finite-sample correction.

### Skewness

The skewness plug-in estimator is

`hat kappa = [n^{-1} sum_i (X_i - hat mu)^3] / hat sigma^3`.

This example matters because skewness is nonlinear. It is not a linear average of raw observations, but it is still a plug-in estimator.

### Correlation

The sample correlation can be viewed as a smooth function of several linear functionals:

- `int x dF`
- `int y dF`
- `int xy dF`
- `int x^2 dF`
- `int y^2 dF`

This is conceptually important because it shows a path from primitive empirical averages to more complicated derived quantities.

### Quantiles

For the `p`th quantile,

`T(F) = F^{-1}(p)`.

Since `hat F_n` is a step function, one defines the sample quantile carefully as

`hat F_n^{-1}(p) = inf {x : hat F_n(x) >= p}`.

This example is crucial because it exposes a limit of naive plug-in comfort: not every functional is linear or equally smooth. Quantiles depend on local geometry of the cdf and, informally, on how much density sits around the target point.

## What the chapter is really teaching

The chapter teaches a general nonparametric workflow:

1. represent the target as a functional `T(F)`
2. estimate `F` by `hat F_n`
3. define the estimator by `T(hat F_n)`
4. study the estimator using:
   - pointwise asymptotics
   - uniform cdf control
   - later, bootstrap methods

This workflow is more important than any single example in the chapter.

## Uniform versus pointwise control

One of the main conceptual distinctions in the chapter is:

- pointwise estimation of `F(x)` at a fixed `x`
- uniform estimation of the whole cdf

This distinction matters because many downstream functionals depend on the shape of the entire distribution, not one cdf value.

The DKW inequality is the chapter's strongest statement because it gives simultaneous finite-sample control over the whole empirical cdf.

## Bridge to Chapter 8

The chapter explicitly stops at an important boundary:

- for some plug-in estimators, standard errors are easy
- for many nonlinear functionals, they are not

That is why the bootstrap comes next.

So Chapter 7 builds the functional viewpoint and Chapter 8 builds the generic uncertainty engine for those functionals.

## Exercises that carry the chapter

The most important exercises ask the reader to:

- prove pointwise properties of `hat F_n`
- derive the CLT for `hat F_n(x)` at fixed `x`
- compute covariance of `hat F_n(x)` and `hat F_n(y)`
- estimate interval probabilities such as `F(b) - F(a)`
- practice mean and difference-in-means intervals using plug-in logic

These exercises are training the reader to think of sample formulas as consequences of functional estimation.

## Failure modes

- treating `hat F_n` as only a plotting device rather than a genuine estimator of `F`
- confusing pointwise cdf uncertainty with simultaneous confidence bands
- treating nonlinear functionals as if they inherit the same easy variance formulas as linear ones
- ignoring that quantiles depend on local shape of the distribution
- forgetting that some plug-in estimators are smooth and others are not

## Quant research relevance

This chapter is directly relevant to quant research because empirical distributions and plug-in functionals appear everywhere:

- empirical return cdfs
- exceedance probabilities and tail frequencies
- quantile-based risk measures
- empirical moments of signals or PnL
- rank and threshold statistics
- distributional comparisons across universes, regimes, or event windows

The DKW inequality is especially valuable as a reminder that one can sometimes obtain honest finite-sample control of an entire estimated distribution, not just one summary statistic.

## What should be promoted out of this source note

- a durable note on the empirical cdf
- a durable note on Glivenko-Cantelli and DKW
- a durable note on plug-in estimation
- a durable note on linear versus nonlinear statistical functionals
- a durable note on empirical quantiles

## Related notes

- [[All of Statistics]]
- [[All of Statistics - Ch 06 Models Statistical Inference and Learning]]
- [[All of Statistics - Ch 08 The Bootstrap]]
- [[Stats Map]]

## Sources

- [[All of Statistics]]
- [[raw/math_statistics/2004 - wasserman - all of statistics.pdf]]
