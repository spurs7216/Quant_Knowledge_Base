---
title: All of Statistics - Ch 05 Convergence of Random Variables
type: source
status: chapter_ingested
updated: 2026-04-19
tags:
  - source
  - statistics
  - asymptotics
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: full_source
extraction_basis: full_text
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 05 Convergence of Random Variables
parent_source: "[[All of Statistics]]"
sources:
  - "[[All of Statistics]]"
  - "[[raw/math_statistics/2004 - wasserman - all of statistics.pdf]]"
---
# All of Statistics - Ch 05 Convergence of Random Variables

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed against the raw source.
- Pass 2: the full asymptotic backbone of the chapter was rewritten, including definitions of convergence modes, implication relations, WLLN, CLT, Berry-Esseen, multivariate CLT, and both scalar and multivariate delta methods.

## Deepening Targets

- If this book becomes a main asymptotics spine for the vault, deepen the appendix proof of the CLT and create a durable note on when iid asymptotics fail in dependent or heavy-tailed financial data.

## Deepened Subparts

- Whole chapter reworked at theorem-oriented depth.

## Role of the chapter

This chapter is where statistics acquires asymptotic language. Before this chapter, one can define estimators, distributions, and moments. After this chapter, one can justify why sample-based objects stabilize and why centered, rescaled estimators often become approximately Normal.

Without this chapter, later statements such as

- the estimator is consistent
- the statistic is asymptotically Normal
- the confidence interval is valid to first order

would be slogans rather than theorems.

## Core mathematical objects

- sequence of random variables `X_1, X_2, ...`
- limiting variable `X`
- convergence in probability `X_n ->^P X`
- convergence in distribution `X_n => X`
- convergence in quadratic mean `X_n ->^qm X`
- almost sure convergence from the appendix
- sample mean `bar X_n`
- standardized average `sqrt(n) (bar X_n - mu) / sigma`
- differentiable transform `g`
- gradient `nabla g`

The chapter's objects are not estimators alone. They are relations between sequences of random objects and their limits.

## Structural map of the chapter

The chapter has five main blocks:

1. definitions of convergence
2. implication relations among convergence modes
3. law of large numbers
4. central limit theorem and refinements
5. delta method

The appendix adds:

- almost sure and `L1` convergence
- a proof sketch of the CLT via moment generating functions

## Why convergence is subtle

The chapter opens with a useful warning: convergence of random variables is not the same thing as convergence of numbers.

If `X_n ~ N(0,1)` for every `n`, one might be tempted to say `X_n` converges to `N(0,1)`, but that cannot mean `P(X_n = X) -> 1` for some `X ~ N(0,1)`. For continuous variables, exact equality has probability zero.

So one needs several notions of convergence, each answering a different question.

## Definitions

### Definition 5.1: convergence in probability

`X_n ->^P X` if for every `eps > 0`,

`P(|X_n - X| > eps) -> 0`.

Interpretation:

- with high probability, `X_n` becomes close to `X`

This is the natural mode for consistency.

### Definition 5.1: convergence in distribution

`X_n => X` if

`F_n(t) -> F(t)`

at every continuity point of `F`.

Interpretation:

- the laws of `X_n` approach the law of `X`

This is weaker than closeness of realized values. It is primarily about approximate sampling distributions.

### Definition 5.2: convergence in quadratic mean

`X_n ->^qm X` if

`E(X_n - X)^2 -> 0`.

Interpretation:

- mean squared distance to the target vanishes

This is stronger than convergence in probability.

### Appendix notions

The appendix adds:

- almost sure convergence
- `L1` convergence

Those are not side decorations. They reveal that convergence sits in a hierarchy, not a single concept.

## Theorem 5.4: implication relations

The chapter states:

- quadratic mean convergence implies convergence in probability
- convergence in probability implies convergence in distribution
- if the limit is a constant `c`, then convergence in distribution to `c` implies convergence in probability to `c`

In general, reverse implications fail except for the constant-limit case.

### Why the theorem matters

Many asymptotic arguments in statistics quietly move through this implication chain. If one forgets which implication is one-way and which is not, one can make invalid inferences about estimators.

### Proof idea for `qm -> P`

Apply Markov to `(X_n - X)^2`:

`P(|X_n - X| > eps) = P((X_n - X)^2 > eps^2) <= E(X_n - X)^2 / eps^2`.

So vanishing mean square error implies vanishing tail probability.

### Proof idea for `P -> D`

The proof compares `F_n(x)` to `F(x + eps)` and `F(x - eps)` and uses the event `|X_n - X| > eps` as the error term. Letting `n -> infty` and then `eps -> 0` yields cdf convergence at continuity points.

The proof is important because it shows convergence in distribution is produced by control of actual random-variable proximity.

### Constant-limit special case

If the limit is the constant `c`, then cdf convergence at `c - eps` and `c + eps` forces the mass of `X_n` away from `c` to vanish. This is why distributional convergence to constants is stronger than it first appears.

## Theorem 5.5: continuous mapping logic

The chapter records that smooth or continuous transformations preserve convergence under appropriate conditions.

This theorem is one of the hidden engines of asymptotics. Once a basic estimator converges, transformed versions often inherit convergence immediately.

It is the conceptual bridge to the delta method later in the chapter.

## Example 5.3: shrinking Normal variance

For `X_n ~ N(0, 1/n)`, the chapter shows:

- `X_n => 0`
- `X_n ->^P 0`

The point is instructive:

- the variables do not equal zero
- but their distributions collapse around zero

This is a good example of why convergence is about laws or neighborhoods, not pointwise equality.

## Theorem 5.6: weak law of large numbers

For iid `X_i` with mean `mu`,

`bar X_n ->^P mu`.

### Proof skeleton in the chapter

Assuming finite variance for simplicity,

`Var(bar X_n) = sigma^2 / n`,

so by Chebyshev,

`P(|bar X_n - mu| > eps) <= sigma^2 / (n eps^2) -> 0`.

### What the theorem is really saying

The sample mean is a stable estimator of the population mean because averaging kills variance at rate `1/n`.

This is not yet a statement about the shape of the estimator's distribution. It is a statement about concentration near the truth.

### Why this matters for statistics

The WLLN is the first consistency theorem most statistical procedures ultimately rest on:

- sample means
- empirical moments
- plug-in estimators
- empirical proportions

## Theorem 5.8: central limit theorem

For iid `X_i` with mean `mu` and variance `sigma^2`,

`sqrt(n) (bar X_n - mu) / sigma => N(0,1)`.

### What it says and what it does not say

It says:

- a centered and scaled sample mean is approximately Gaussian in large samples

It does not say:

- the raw data are Gaussian
- finite-sample exact Normality holds
- every statistic is asymptotically Normal without additional work

### Why the `sqrt(n)` scaling appears

Variance of `bar X_n` is `sigma^2 / n`, so multiplying by `sqrt(n)` stabilizes fluctuation size to an `O(1)` limit.

### Why the theorem is central

The CLT is the first theorem that turns convergence into distributional approximation, which is what confidence intervals and test statistics need.

## Theorem 5.10: studentized CLT

Replacing `sigma` by the sample standard deviation still gives

`sqrt(n) (bar X_n - mu) / S_n => N(0,1)`.

This matters because population variance is almost never known in practice.

The theorem legitimizes plug-in standardization.

## Theorem 5.11: Berry-Esseen inequality

If `E |X_1|^3 < infty`, then

`sup_z |P(Z_n <= z) - Phi(z)| <= C E|X_1 - mu|^3 / (sqrt(n) sigma^3)`

with the constant written explicitly in the book.

### Why this theorem matters

The CLT is a limit statement. Berry-Esseen adds an approximation-rate statement.

That difference is critical in practice:

- asymptotic validity is not the same as accurate finite-sample Normal approximation

Berry-Esseen says the approximation error is typically `O(n^{-1/2})` under a finite third moment.

## Theorem 5.12: multivariate CLT

If `X_i` are iid random vectors with mean vector `mu` and covariance matrix `Sigma`, then

`sqrt(n) (bar X_n - mu) => N(0, Sigma)`.

This is the true gateway to real statistical work because most estimators are vector-valued:

- several moments at once
- regression coefficients
- covariance estimators
- multiple asset statistics jointly

The scalar CLT is a special case.

## The delta method

### Theorem 5.13: scalar delta method

If

`sqrt(n) (Y_n - theta) => N(0, sigma^2)`

and `g` is differentiable at `theta`, then

`sqrt(n) (g(Y_n) - g(theta)) => N(0, [g'(theta)]^2 sigma^2)`.

### Proof idea

Linearize:

`g(Y_n) = g(theta) + g'(theta) (Y_n - theta) + remainder`.

If the remainder is asymptotically negligible, the transformed statistic behaves like the derivative times the original statistic.

This is a first-order approximation theorem.

### Theorem 5.15: multivariate delta method

For vector `Y_n`, the derivative becomes the gradient, and the asymptotic variance becomes

`nabla g(mu)^T Sigma nabla g(mu)`.

### Why this matters

Many practical parameters are transformations of more primitive statistics:

- ratios
- products
- correlations
- log transforms
- Sharpe-like functionals

The delta method transports asymptotic Normality through these smooth maps.

## Appendix proof of the CLT

The appendix sketches a proof using mgfs. Standardize to `Y_i = (X_i - mu) / sigma`, form the mgf of

`Z_n = n^{-1/2} sum_i Y_i`,

expand `psi(t)` around zero, and show the mgf converges to `exp(t^2 / 2)`, the mgf of `N(0,1)`.

This proof is not fully general in modern probability terms, but it teaches the core intuition:

- centering kills the linear term
- variance determines the quadratic term
- higher-order terms vanish under `1 / sqrt(n)` scaling

## What the chapter is really teaching

The chapter teaches a four-step asymptotic workflow:

1. identify a sample object such as a mean or empirical moment
2. prove concentration or consistency via LLN-type logic
3. derive distributional fluctuation via CLT-type logic
4. transport the result through transformations via the continuous mapping theorem or delta method

That workflow becomes the backbone of later inference chapters.

## Non-implications and why they matter

The chapter explicitly warns that reverse implications fail.

This matters because one can easily confuse:

- cdf convergence with numerical closeness
- consistency with mean-square convergence
- asymptotic Normality with finite-sample Gaussianity

These confusions produce a large fraction of bad applied asymptotic arguments.

## Failure modes

- treating all convergence symbols as interchangeable
- forgetting that convergence in distribution does not imply realizations are close with high probability
- applying CLT reasoning where independence or finite-variance assumptions are not credible
- using the delta method for nonsmooth functions without checking differentiability
- treating asymptotic approximations as exact finite-sample statements

## Quant research relevance

This chapter is the mathematical base layer under:

- t-statistics for signals
- confidence intervals for means and spreads
- asymptotic variance formulas for fitted models
- transformed performance measures
- large-sample portfolio and factor inference

But it also carries a warning that is especially important in finance:

- financial data are often dependent
- tails can be much heavier than textbook iid settings assume
- regime shifts and serial dependence can destroy naive transfer of iid asymptotic results

So the chapter provides the language, not universal permission.

## Promoted durable notes

- [[Convergence and Limit Theory]]

## Next promotion targets

- a durable note on Berry-Esseen and finite-sample Normal-approximation error
- a durable note on the delta method for quant research

## Related notes

- [[All of Statistics]]
- [[Convergence and Limit Theory]]
- [[All of Statistics - Ch 04 Inequalities]]
- [[All of Statistics - Ch 06 Models Statistical Inference and Learning]]
- [[Math Map]]
- [[Stats Map]]

## Sources

- [[All of Statistics]]
- [[raw/math_statistics/2004 - wasserman - all of statistics.pdf]]
