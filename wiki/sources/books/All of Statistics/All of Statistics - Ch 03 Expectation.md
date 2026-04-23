---
title: All of Statistics - Ch 03 Expectation
type: source
status: chapter_ingested
updated: 2026-04-19
tags:
  - source
  - statistics
  - expectation
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: full_source
extraction_basis: full_text
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 03 Expectation
parent_source: "[[All of Statistics]]"
sources:
  - "[[All of Statistics]]"
  - "[[raw/math_statistics/2004 - wasserman - all of statistics.pdf]]"
---
# All of Statistics - Ch 03 Expectation

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed against the raw source.
- Pass 2: Full deep rewrite completed across the chapter.

## Deepening Targets

- Extend proof-level follow-up on conditional expectation and mgf existence if later notes depend heavily on them.

## Deepened Subparts

- Whole chapter reworked with theorem-level focus on expectation, variance, conditional expectation, and mgfs.

## Role of the chapter

This chapter turns distributions into numerical functionals. Probability in Chapters 1 and 2 says how mass is assigned. Expectation says how to average functions with respect to that mass.

That move is foundational because most statistical targets are expectations in disguise:

- means
- moments
- variances
- covariances
- regression functions
- risks
- likelihood derivatives

The chapter also introduces the two most important conditional-averaging identities in the book:

- the rule of iterated expectations
- the law of total variance

## Core mathematical objects

- `E(X) = integral x dF(x)`: expectation
- `E[r(X)]`: expectation of a transformed variable
- `V(X) = E[(X - mu)^2]`: variance
- `Cov(X,Y) = E[(X - EX)(Y - EY)]`: covariance
- `E(X | Y = y)` and `E(X | Y)`: conditional expectation
- `V(Y | X = x)` and `V(Y | X)`: conditional variance
- `phi_X(t) = E[e^{tX}]`: moment generating function

The appendix also makes clear that expectation is really an integral with respect to a distribution, not just a weighted average formula.

## Expectation as an integral operator

### Definition 3.1

Expectation is defined as

- `sum_x x f(x)` in the discrete case
- `integral x f(x) dx` in the continuous case
- more generally `integral x dF(x)`

The chapter explicitly requires absolute integrability to guarantee the expectation exists.

This is not a technical nuisance. The Cauchy example shows what fails when the tail is too heavy: the average of repeated draws does not stabilize in the usual way because the mean itself is undefined.

## The rule of the lazy statistician

### Theorem 3.6

If `Y = r(X)`, then

`E(Y) = E[r(X)] = integral r(x) dF_X(x)`.

This theorem is one of the most useful computational rules in probability.

Its real content is conceptual:

- do not first find the distribution of `r(X)` unless necessary
- push the function through the original distribution
- compute the expectation directly

This is the correct way to handle payoffs, nonlinear transforms, indicator events, and many loss functions.

One of the most important special cases is

`E[I_A(X)] = P(X in A)`.

So probability itself is a special case of expectation.

## Properties of expectation

### Existence of lower-order moments

### Theorem 3.10

If the `k`th moment exists and `j < k`, then the `j`th moment exists.

This matters because asymptotic arguments often assume existence of enough moments. The theorem says higher-order integrability is stronger than lower-order integrability.

### Linearity

### Theorem 3.11

Expectation is linear:

`E(sum_i a_i X_i) = sum_i a_i E(X_i)`.

This does not require independence.

That point is critical. Many students mistakenly associate additivity of expectation with independence, but linearity is unconditional. Independence becomes important later for variance and mgf factorization, not for expectation itself.

### Expectations of products under independence

### Theorem 3.13

If random variables are independent, then expectation factorizes across products.

This is one of the bridges from independence assumptions to tractable calculations.

## Variance and covariance

### Definition 3.14

Variance is

`V(X) = E[(X - mu)^2]`

where `mu = E(X)`.

The chapter then emphasizes the computational identity

`V(X) = E(X^2) - [E(X)]^2`.

This is often the more useful formula algebraically, though not always the more stable one numerically.

### Theorem 3.17

For iid variables with mean `mu` and variance `sigma^2`,

`E(bar X_n) = mu`

and

`V(bar X_n) = sigma^2 / n`.

This is one of the first structural explanations for why averaging reduces noise.

### Definition 3.18 and Theorem 3.19

Covariance measures linear comovement:

`Cov(X,Y) = E[(X - EX)(Y - EY)]`.

The chapter records the usual bilinear properties and then gives

`V(X + Y) = V(X) + V(Y) + 2 Cov(X,Y)`.

So independence or uncorrelatedness is precisely what removes the cross term in quadratic risk.

### Lemma 3.21

For a random vector `X` with mean `mu` and covariance matrix `Sigma`,

- `E(a^T X) = a^T mu`
- `V(a^T X) = a^T Sigma a`
- `E(AX) = A mu`
- `V(AX) = A Sigma A^T`

This is the matrix form of linear propagation of mean and variance. It is one of the most reusable results in the book.

## Conditional expectation

### Definition 3.22

Conditional expectation is defined by averaging with the conditional law:

`E(X | Y = y) = integral x f_{X|Y}(x|y) dx`

or the discrete analogue.

The book highlights the key subtlety:

- `E(X)` is a number
- `E(X | Y = y)` is a function of `y`
- before `Y` is observed, `E(X | Y)` is itself a random variable

This is not just notation. Conditional expectation is an estimator-like object: it updates a mean after seeing information.

### Theorem 3.24: rule of iterated expectations

`E[E(Y | X)] = E(Y)`

and more generally

`E[E(r(X,Y) | X)] = E(r(X,Y))`.

This is one of the central tower identities of probability. It says averaging in stages gives the same result as averaging all at once.

### Theorem 3.27: law of total variance

`V(Y) = E[V(Y | X)] + V[E(Y | X)]`.

This decomposition is extremely important:

- the first term is average within-group noise
- the second term is between-group variation in the conditional mean

The chapter's hierarchical Binomial example shows exactly why this matters. Extra heterogeneity in the latent county-level prevalence inflates total variability beyond a simple Binomial model.

## Moment generating functions

### Definition 3.29

`phi_X(t) = E[e^{tX}]`

when finite on an open interval around zero.

The mgf packages the moments into derivatives at the origin:

`phi_X^{(k)}(0) = E(X^k)`.

### Lemma 3.31

Two structural properties make mgfs useful:

1. affine transformation:
   `phi_{aX+b}(t) = e^{bt} phi_X(at)`
2. sums of independent variables:
   `phi_{sum X_i}(t) = product_i phi_{X_i}(t)`

The second property is why mgfs are so effective for proving distributional results for sums.

### Theorem 3.33

If two mgfs agree on an open interval around zero, then the distributions agree.

So the mgf is a distribution-characterizing transform, at least when it exists locally.

## What the chapter is really building

At a deeper level, this chapter builds three reusable operators:

1. expectation as linear averaging
2. conditional expectation as information-adaptive averaging
3. mgf as transform-based compression of the full law

These become the workhorses of later inference.

## Failure modes the chapter is trying to prevent

- treating expectation as guaranteed to exist for every distribution
- believing linearity of expectation needs independence
- forgetting that variance depends on covariance terms
- treating `E(X | Y)` as a number instead of a random variable
- forgetting the decomposition in the law of total variance
- using mgfs where they do not exist
- assuming sample averages stabilize without checking moment conditions

## Quant research relevance

This chapter is directly relevant to quantitative research because:

- expected return, expected loss, and expected utility are expectation objects
- portfolio variance and factor covariance live in the variance-covariance block
- hierarchical and latent-state models rely on conditional expectation and total variance
- simulation-based pricing and risk decompositions often use the rule of iterated expectations
- mgfs and characteristic-style transforms appear in option pricing, large deviations, and distributional approximations

The hierarchical disease-count example has a direct analogue in finance: if event probabilities vary across firms, regimes, or time, unconditional dispersion is larger than the naive conditional model suggests.

## What should be promoted out of this source note

- a durable note on expectation as integration
- a durable note on variance and covariance identities
- a durable note on conditional expectation as an information projection
- a durable note on the rule of iterated expectations
- a durable note on the law of total variance
- a durable note on moment generating functions and when they are useful

## Related notes

- [[All of Statistics]]
- [[All of Statistics - Ch 02 Random Variables]]
- [[All of Statistics - Ch 04 Inequalities]]
- [[Stats Map]]
- [[Math Map]]

## Sources

- [[All of Statistics]]
- [[raw/math_statistics/2004 - wasserman - all of statistics.pdf]]
