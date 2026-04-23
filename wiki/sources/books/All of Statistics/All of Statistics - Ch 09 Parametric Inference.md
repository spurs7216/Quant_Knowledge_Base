---
title: All of Statistics - Ch 09 Parametric Inference
type: source
status: chapter_ingested
updated: 2026-04-19
tags:
  - source
  - statistics
  - parametric-inference
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: full_source
extraction_basis: full_text
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 09 Parametric Inference
parent_source: "[[All of Statistics]]"
sources:
  - "[[All of Statistics]]"
  - "[[raw/math_statistics/2004 - wasserman - all of statistics.pdf]]"
---
# All of Statistics - Ch 09 Parametric Inference

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed against the raw source.
- Pass 2: the chapter was rewritten around the full parametric inference spine: parameter of interest, method of moments, likelihood, KL-based consistency, Fisher information, asymptotic Normality, efficiency, delta method, multiparameter extension, parametric bootstrap, and model checking.

## Deepening Targets

- If this source becomes the main reference for estimation theory in the vault, add a dedicated durable note on M-estimation and another on regularity failures: support depending on the parameter, weak identification, boundary problems, and high-dimensional breakdown.

## Deepened Subparts

- Whole chapter reworked at theorem-oriented depth.

## Role of the chapter

This chapter is where the book commits to the classical parametric program:

1. specify a finite-dimensional statistical model
2. define the object of interest inside that model
3. estimate it from data
4. study large-sample behavior of the estimator
5. derive uncertainty and efficiency claims from the model structure

The chapter is also careful not to oversell parametrics. It begins by admitting the central objection:

- in most real problems we do not know the data-generating distribution belongs exactly to a parametric family

That warning matters. The chapter is not saying parametric models are truth. It is saying they can be useful approximations and an organizing language for inference.

## Core mathematical objects

- parametric family `F = {f(x; theta) : theta in Theta}`
- parameter `theta`
- parameter of interest `tau = T(theta)`
- nuisance parameter
- sample moments `hat alpha_j`
- method-of-moments estimator `hat theta`
- likelihood `L_n(theta)`
- log-likelihood `ell_n(theta)`
- score `s(X; theta)`
- Fisher information `I_n(theta)`
- KL divergence `D(theta, psi)`
- asymptotic standard error
- transform `g(theta)` for the delta method
- information matrix in multiparameter models

## Structural map of the chapter

The chapter has twelve working pieces:

1. parameter of interest
2. method of moments
3. maximum likelihood
4. qualitative properties of the mle
5. consistency
6. equivariance
7. asymptotic Normality
8. efficiency
9. delta method
10. multiparameter models
11. parametric bootstrap
12. checking assumptions

The appendices then add proofs, sufficiency, exponential families, and numerical maximization.

## Parameter of interest versus nuisance parameter

The chapter opens with a distinction many people skip too quickly:

- the full parameter of the model is not always the inferential target

If `theta = (mu, sigma)`, the question may concern:

- `mu`
- or a functional such as `tau = 1 - Phi((1 - mu) / sigma)`

This distinction is not bookkeeping. It determines:

- which uncertainty statement is relevant
- which transformations matter
- which nuisance quantities must be carried through the analysis

This is already a bridge to semiparametric and econometric thinking: the model may be larger than the target.

## Method of moments

### Definition 9.3

For `k` parameters, define theoretical moments

`alpha_j(theta) = E_theta(X^j)`

and sample moments

`hat alpha_j = n^{-1} sum_i X_i^j`.

The method-of-moments estimator solves

`alpha_j(hat theta_n) = hat alpha_j`

for `j = 1, ..., k`.

### Why this method matters

Method of moments is not sold here as optimal. It is sold as:

- constructive
- interpretable
- often easy to compute
- often a useful starting point for iterative likelihood methods

That is the right attitude.

### Example structure

- Bernoulli gives `hat p = bar X`
- Normal with unknown mean and variance gives
  - `hat mu = bar X`
  - `hat sigma^2 = n^{-1} sum_i (X_i - bar X)^2`

The Normal example is useful because it shows moment equations can recover familiar estimators directly.

### Theorem 9.6

Under appropriate conditions:

- the estimator exists with probability tending to one
- it is consistent
- it is asymptotically Normal

The asymptotic covariance formula is written in terms of the inverse moment map and the vector `Y = (X, X^2, ..., X^k)^T`.

### Real lesson

Method of moments is a valid asymptotic method, but it uses only selected moment restrictions. It therefore pays less attention than likelihood to the full distributional structure.

## Maximum likelihood

### Definition 9.7

`L_n(theta) = prod_i f(X_i; theta)`.

### Definition 9.8

The mle is the value of `theta` that maximizes `L_n(theta)` or equivalently `ell_n(theta) = log L_n(theta)`.

### What likelihood is and is not

Likelihood is the joint density of the observed data viewed as a function of the parameter. It is not a probability density over parameter values.

That distinction is critical. Confusing likelihood with probability over `theta` is one of the classic conceptual mistakes.

### Bernoulli example

For Bernoulli data,

`ell_n(p) = S log p + (n - S) log(1 - p)`,

and maximizing yields `hat p = S / n`.

### Normal example

For `N(mu, sigma^2)`, likelihood factorization separates:

- centered sample variability through `S^2`
- location mismatch through `(bar X - mu)^2`

The mle becomes:

- `hat mu = bar X`
- `hat sigma = S`

### Hard example: `Uniform(0, theta)`

This is one of the most important examples in the chapter because it breaks the student's reflex that likelihood estimation always comes from smooth first-order calculus.

Here:

- if `theta < X_(n)`, the likelihood is zero
- if `theta >= X_(n)`, likelihood is `theta^{-n}`

So the mle is the boundary point `hat theta = X_(n)`.

This example teaches:

- support can depend on the parameter
- regularity can fail
- maximizers can live on boundaries
- likelihood geometry is not always smooth interior optimization

## Why mle is attractive

The chapter lists the standard attractions:

- consistency
- equivariance
- asymptotic Normality
- asymptotic efficiency
- approximate Bayes optimality in regular large samples

But the chapter also states these depend on regularity conditions. That caveat is part of the content, not a footnote.

## Consistency and KL divergence

### KL divergence

For two densities `f` and `g`,

`D(f, g) = int f(x) log(f(x) / g(x)) dx`.

Write `D(theta, psi)` for the KL divergence between `f(x; theta)` and `f(x; psi)`.

### Why KL appears

Define

`M_n(theta) = n^{-1} sum_i log(f(X_i; theta) / f(X_i; theta^*))`.

By LLN, this converges to

`M(theta) = -D(theta^*, theta)`.

Since KL is minimized at the truth, the population objective is maximized at `theta^*`.

This is the real reason consistency works:

- the empirical criterion approaches a population criterion
- the population criterion is uniquely maximized at the truth

### Theorem 9.13

If:

- `sup_theta |M_n(theta) - M(theta)| ->^P 0`
- and `M(theta)` is uniquely maximized at `theta^*`

then `hat theta_n ->^P theta^*`.

### Why this theorem matters

This is already the template of modern extremum-estimation theory:

- define an objective
- prove uniform convergence
- prove identification
- transfer the argmax

The theorem is much deeper than "the mle is consistent."

## Equivariance

### Theorem 9.14

If `tau = g(theta)` and `hat theta_n` is the mle of `theta`, then

`hat tau_n = g(hat theta_n)`

is the mle of `tau`.

### Why this is useful

Once a primitive parameter estimate is available, transformed quantities inherit the likelihood logic automatically.

This is important for:

- odds
- hazard transforms
- log-volatility
- tail probabilities derived from parametric models

## Score and Fisher information

### Definition 9.16

The score is

`s(X; theta) = d log f(X; theta) / d theta`.

It measures local sensitivity of the log-likelihood.

### Fisher information

`I_n(theta) = Var_theta(sum_i s(X_i; theta))`.

For one observation, write `I(theta)`.

### Theorem 9.17

`I_n(theta) = n I(theta)`

and

`I(theta) = -E_theta[d^2 log f(X; theta) / d theta^2]`.

### Why information matters

Information is local curvature. Large curvature means the likelihood sharply distinguishes nearby parameter values, which means lower asymptotic uncertainty.

This is the chapter's geometric heart:

- score is local slope
- information is local curvature

## Asymptotic Normality

### Theorem 9.18

Under regularity,

`(hat theta_n - theta) / se => N(0,1)`

with

`se approx sqrt(1 / I_n(theta))`

and the same remains true after plugging in `hat theta_n`:

`hat se = sqrt(1 / I_n(hat theta_n))`.

### Appendix proof skeleton

Taylor expand the score equation `ell'(hat theta) = 0` around `theta`:

`0 approx ell'(theta) + (hat theta - theta) ell''(theta)`.

So

`sqrt(n) (hat theta - theta) = [n^{-1/2} ell'(theta)] / [-n^{-1} ell''(theta)]`.

Then:

- numerator obeys CLT
- denominator obeys LLN

giving asymptotic Normality.

### Why this proof matters

This is the prototype asymptotic expansion behind a huge amount of likelihood and M-estimation theory.

## Theorem 9.19: asymptotic confidence interval

The interval

`hat theta_n +- z_(alpha/2) hat se`

has asymptotic coverage `1 - alpha`.

This is the standard z-interval, but the important point is that it arises from information-based asymptotic curvature, not from a generic confidence recipe.

## Efficiency

### Theorem 9.23

For regular models,

`are(tilde theta_n, hat theta_n) <= 1`

for any well-behaved competitor `tilde theta_n`, where `are` is asymptotic relative efficiency.

### What this does and does not mean

It means:

- under the assumed model and regularity conditions, the mle is asymptotically variance-optimal

It does not mean:

- the mle is best under misspecification
- the mle is best in high dimensions
- the mle is best in finite samples

The chapter says this explicitly, and it matters.

## Delta method

### Theorem 9.24

If `tau = g(theta)` with differentiable `g`, then

`(hat tau_n - tau) / hat se(hat tau_n) => N(0,1)`

with

`hat se(hat tau_n) = |g'(hat theta)| hat se(hat theta_n)`.

### Why this matters

Most interesting parameters are not primitive coordinates of `theta`. They are transforms:

- log-odds
- log-volatility
- exceedance probabilities
- functions of several fitted parameters

The delta method transfers asymptotic Normality to these transformed targets.

## Multiparameter models

### Fisher information matrix

For vector parameter `theta = (theta_1, ..., theta_k)`, define the information matrix from expected negative Hessian terms.

Let `J_n(theta) = I_n(theta)^(-1)`.

### Theorem 9.27

Under regularity,

`hat theta - theta approx N(0, J_n)`

and the diagonal entries give asymptotic variances of components.

### Multivariate delta method

### Theorem 9.28

For scalar function `tau = g(theta_1, ..., theta_k)`,

`se^2(hat tau) approx nabla g^T J_n nabla g`.

This is the vector generalization of the scalar derivative rule.

## Parametric bootstrap

The chapter closes the inferential loop by showing an alternative to analytic delta-method variance propagation.

The parametric bootstrap:

1. fits the parametric model
2. simulates from `f(x; hat theta)`
3. recomputes the statistic
4. uses replicate variability as a standard-error estimate

This differs from the nonparametric bootstrap because it trusts the model, not the empirical distribution.

That is both its strength and its weakness.

## Checking assumptions

The chapter ends correctly:

- if you adopt a parametric model, you should check it

This can be informal:

- histograms
- shape diagnostics

or formal:

- goodness-of-fit tests

This is not optional decoration. Efficiency claims are meaningless if the model is badly wrong.

## What the chapter is really teaching

The chapter is teaching a chain:

1. model
2. target
3. estimator
4. identification
5. asymptotic law
6. transformed target
7. model check

It is a complete inference workflow, not just a list of estimators.

## Failure modes

- treating likelihood as a probability distribution on parameters
- assuming support never depends on the parameter
- using mle asymptotics without regularity
- talking about efficiency when the model is misspecified
- forgetting the difference between parameter of interest and nuisance structure
- using parametric bootstrap without confronting model error

## Quant research relevance

This chapter is central for quant work because parametric inference appears in:

- volatility and duration models
- hazard and default modeling
- point-process or arrival models
- latent-state filtering and state-space systems
- transformed probabilities, odds, or tail quantities

The main lesson for real trading research is:

- parametric structure buys efficiency only when the structure is defensible

Wrong structure can easily dominate asymptotic elegance.

## Promoted durable notes

- [[Maximum Likelihood Estimation]]

## Next promotion targets

- a durable note on method of moments
- a durable note on KL-based consistency
- a durable note on score and Fisher information
- a durable note on delta-method uncertainty propagation

## Related notes

- [[All of Statistics]]
- [[Maximum Likelihood Estimation]]
- [[All of Statistics - Ch 10 Hypothesis Testing and p-values]]
- [[All of Statistics - Ch 11 Bayesian Inference]]
- [[Stats Map]]

## Sources

- [[All of Statistics]]
- [[raw/math_statistics/2004 - wasserman - all of statistics.pdf]]
