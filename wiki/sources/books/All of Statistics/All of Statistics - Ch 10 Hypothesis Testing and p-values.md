---
title: All of Statistics - Ch 10 Hypothesis Testing and p-values
type: source
status: chapter_ingested
updated: 2026-04-19
tags:
  - source
  - statistics
  - hypothesis-testing
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: full_source
extraction_basis: full_text
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 10 Hypothesis Testing and p-values
parent_source: "[[All of Statistics]]"
sources:
  - "[[All of Statistics]]"
  - "[[raw/math_statistics/2004 - wasserman - all of statistics.pdf]]"
---
# All of Statistics - Ch 10 Hypothesis Testing and p-values

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed against the raw source.
- Pass 2: the chapter was rewritten around the full testing sequence: rejection regions, power and size, Wald tests, p-values, chi-square tests, permutation tests, likelihood-ratio tests, multiple-testing corrections, goodness-of-fit, and the Neyman-Pearson appendix.

## Deepening Targets

- If this source becomes a core testing reference for the vault, add a durable note that separates test calibration, effect size, and scientific relevance, and another focused specifically on multiple-testing control in alpha mining.

## Deepened Subparts

- Whole chapter reworked at theorem-oriented depth.

## Role of the chapter

This chapter formalizes one of the most abused parts of applied statistics: testing.

It does two things at once:

1. it builds the classical test machinery
2. it repeatedly warns the reader not to overuse it

That warning is central. The chapter explicitly says estimation and confidence intervals are often better tools. Hypothesis testing should be used when there is a well-defined null hypothesis worth challenging.

## Core mathematical objects

- null hypothesis `H_0`
- alternative `H_1`
- rejection region `R`
- test statistic `T`
- critical value `c`
- power function `beta(theta)`
- size `alpha`
- type I and type II error
- Wald statistic
- p-value
- chi-square statistic
- permutation distribution
- likelihood-ratio statistic
- familywise-error control
- false discovery rate

## Structural map of the chapter

The chapter proceeds through:

1. general testing framework
2. Wald test
3. p-values
4. chi-square methods
5. permutation test
6. likelihood-ratio test
7. multiple testing
8. goodness-of-fit
9. Neyman-Pearson appendix
10. t-test appendix

This is not accidental. The structure moves from generic test logic to concrete test families, then to modern scale problems such as multiplicity.

## Basic setup

The null and alternative partition the parameter space:

`H_0 : theta in Theta_0`

versus

`H_1 : theta in Theta_1`.

Testing means choosing a rejection region `R` in the sample space. If `X in R`, reject `H_0`; otherwise retain it.

### Definition 10.1: power and size

The power function is

`beta(theta) = P_theta(X in R)`.

The size is

`alpha = sup_(theta in Theta_0) beta(theta)`.

### Why this matters

This definition forces the reader to see that a test is not just a p-value-producing button. A test is a procedure with operating characteristics across the entire parameter space.

Type I error and Type II error are then consequences of the power function restricted to null and alternative regions.

## Wald test

### Definition 10.3

For scalar parameter `theta`, estimate `hat theta` and estimated standard error `hat se`, define

`W = (hat theta - theta_0) / hat se`.

Reject in a two-sided test when `|W| > z_(alpha/2)`.

### Theorem 10.4

Asymptotically, the Wald test has size `alpha`.

This is immediate from asymptotic Normality under the null.

### Theorem 10.6: approximate power

If the true parameter is `theta^* != theta_0`, the chapter gives an explicit approximate power expression in terms of the Normal cdf.

### What the Wald test really is

The Wald test converts:

- estimated discrepancy from the null

into:

- discrepancy measured in standard-error units

So Wald testing is only as good as:

- the estimator
- the standard-error estimate
- the asymptotic approximation behind both

### Theorem 10.10: duality with confidence intervals

The Wald test rejects `H_0 : theta = theta_0` if and only if `theta_0` is outside the asymptotic confidence interval

`hat theta +- z_(alpha/2) hat se`.

This theorem matters because it shows the test is often a less informative repackaging of an interval estimate.

## Statistical significance versus scientific significance

The chapter's warning here is excellent:

- rejecting `H_0` does not imply the effect is large or important

If the confidence interval excludes the null by a tiny amount, the result may be statistically significant yet practically unimportant.

This is a major lesson for quant work, where huge samples can make negligible effects look "significant."

## p-values

### Definition 10.11

The p-value is the smallest significance level at which the observed test would reject.

### Theorem 10.12

If the rejection rule is of the form `T(X_n) >= c_alpha`, then the p-value is the null probability of seeing a test statistic at least as extreme as the observed one.

For a simple null:

`p-value = P_(theta_0)(T(X_n) >= T(x_n))`.

### Theorem 10.13

For the Wald test with observed statistic `w`,

`p-value approx 2 Phi(-|w|)`.

### Theorem 10.14

If the test statistic has a continuous null distribution, then under `H_0` the p-value is `Uniform(0,1)`.

### Why this theorem matters

This is the real calibration statement behind p-values. It explains exactly why the rule

- reject when `p < alpha`

has type I error `alpha`.

### What p-values are not

The chapter is explicit:

- not `P(H_0 | data)`
- not the probability the null is true
- not a general "probability the result happened by chance"

They are null-calibrated extremeness measures.

## Chi-square methods

### Pearson chi-square statistic

For multinomial data under null probabilities `p_0j`,

`T = sum_j (X_j - n p_0j)^2 / (n p_0j)`.

### Theorem 10.17

Under `H_0`, `T => chi^2_(k-1)`.

This is the prototype for discrete goodness-of-fit and contingency-table testing.

### Why this matters

Chi-square methods move beyond scalar z-testing into multi-cell discrepancy measures. The statistic measures total standardized deviation between observed and expected counts.

## Permutation test

The permutation test is one of the chapter's most conceptually important tools because it does not rely on asymptotic Normality.

Under

`H_0 : F_X = F_Y`,

if the two samples are exchangeable under the null, then every permutation of the pooled data is equally plausible.

### Core idea

1. choose a statistic `T`
2. compute `t_obs`
3. generate the permutation distribution under the null by relabeling
4. compute the tail area beyond `t_obs`

### Why it matters

This is an exact or near-exact finite-sample calibration method when exchangeability is justified. It is a strong alternative to asymptotic approximations in small samples.

### Limitation

The validity is tied to exchangeability under the null. If the design or dependence structure breaks exchangeability, the permutation logic breaks too.

## Likelihood-ratio test

### Definition 10.21

For

`H_0 : theta in Theta_0`

versus unrestricted `Theta`,

the likelihood-ratio statistic is

`lambda = 2 log( sup_(theta in Theta) L(theta) / sup_(theta in Theta_0) L(theta) )`.

### Theorem 10.22

When `Theta_0` imposes `r - q` restrictions, under `H_0`

`lambda => chi^2_(r-q)`.

### Why LRT differs from Wald

Wald asks:

- how far is the estimate from the null, measured in standard-error units?

LRT asks:

- how much likelihood is lost by forcing the null restrictions?

This is a geometry-of-fit perspective rather than a geometry-of-distance perspective.

## Multiple testing

This is one of the most important sections for quantitative research.

If one runs many tests, even valid level-`alpha` marginal tests will produce false positives with high probability somewhere in the family.

### Bonferroni

Reject `H_0i` if

`P_i < alpha / m`.

### Theorem 10.24

This controls the probability of at least one false rejection by `alpha`.

### Why it is conservative

It protects against any false positive in the family, so it often loses power badly when many hypotheses are tested.

### Benjamini-Hochberg

Order the p-values `P_(1) <= ... <= P_(m)` and find the largest `i` with

`P_(i) < i alpha / (C_m m)`.

Reject up to that threshold.

### Theorem 10.26

This controls false discovery rate:

`FDR = E(FDP) <= alpha`.

### Why this matters

For large-scale discovery problems, controlling expected false-discovery proportion is often more appropriate than insisting on almost no false positives at all.

This is exactly the regime of factor libraries, feature searches, and large signal-mining exercises.

## Goodness-of-fit

The chapter also gives a grouped-data goodness-of-fit test for a parametric family by binning the data, estimating expected cell probabilities, and forming

`Q = sum_j (N_j - n p_j(hat theta))^2 / (n p_j(hat theta))`.

### Theorem 10.29

Under `H_0`,

`Q => chi^2_(k-1-s)`

where `s` is the number of estimated parameters.

### Important caveat

Failure to reject does not validate the model. It may simply indicate low power.

The chapter says this explicitly, and it should be taken seriously.

## Neyman-Pearson appendix

### Theorem 10.30

For simple null versus simple alternative, the likelihood-ratio rejection region is the most powerful size-`alpha` test.

This is the exact setting where a strongest test can be characterized cleanly.

This theorem is conceptually foundational because it explains why likelihood ratios are not arbitrary. They arise from optimality in the simplest testing problem.

## t-test appendix

For Normal data with unknown variance and small samples, replace the standard Normal cutoff by a `t_(n-1)` distribution. The appendix notes that for moderate `n`, this is practically close to the Wald test.

## What the chapter is really teaching

The chapter is teaching three separate layers:

1. tests are procedures with calibrated error rates
2. p-values are one reporting device for those procedures, not the ontology of evidence
3. when many hypotheses are tested, calibration must be redesigned

That third point is where the chapter becomes especially modern.

## Failure modes

- treating a p-value as a posterior probability of the null
- using hypothesis testing where interval estimation would answer the question better
- confusing statistical significance with practical significance
- using many tests without multiplicity control
- applying permutation logic when exchangeability fails
- trusting likelihood or Wald asymptotics when the approximation regime is weak

## Quant research relevance

This chapter is directly relevant to quant research because almost every alpha or model-evaluation pipeline touches it:

- testing factor significance
- comparing signal hit rates or means
- permutation-based robustness checks
- goodness-of-fit of discrete event models
- large-scale multiple testing across candidate factors, features, or hyperparameter families

The key lesson for real trading research is:

- significance without multiplicity control or effect-size interpretation is mostly noise management theater

## What should be promoted out of this source note

- a durable note on power, size, and rejection regions
- a durable note on p-value interpretation
- a durable note on Wald versus likelihood-ratio testing
- a durable note on permutation testing
- a durable note on multiple testing for quant research

## Related notes

- [[All of Statistics]]
- [[All of Statistics - Ch 09 Parametric Inference]]
- [[Backtest Overfitting]]
- [[Stats Map]]

## Sources

- [[All of Statistics]]
- [[raw/math_statistics/2004 - wasserman - all of statistics.pdf]]
