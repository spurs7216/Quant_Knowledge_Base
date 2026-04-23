---
title: All of Statistics - Ch 11 Bayesian Inference
type: source
status: chapter_ingested
updated: 2026-04-19
tags:
  - source
  - statistics
  - bayesian
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: full_source
extraction_basis: full_text
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 11 Bayesian Inference
parent_source: "[[All of Statistics]]"
sources:
  - "[[All of Statistics]]"
  - "[[raw/math_statistics/2004 - wasserman - all of statistics.pdf]]"
---
# All of Statistics - Ch 11 Bayesian Inference

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed against the raw source.
- Pass 2: the chapter was rewritten around the Bayesian postulates, posterior construction, conjugate examples, posterior intervals, simulation, Bernstein-von-Mises style large-sample logic, flat and improper priors, multiparameter marginalization, Bayesian testing, and the chapter's own failure examples.

## Deepening Targets

- If Bayesian methods become a primary vault spine, add durable notes on posterior consistency, prior sensitivity, and the difference between Bayesian coherence and frequentist operating guarantees.

## Deepened Subparts

- Whole chapter reworked at theorem-oriented depth.

## Role of the chapter

This chapter takes Bayes' theorem from Chapter 1 and turns it into a full inferential program.

But the chapter is stronger than a generic "Bayesians update beliefs" presentation. It does three things:

1. states the Bayesian postulates clearly
2. shows the mechanical workflow of prior times likelihood gives posterior
3. spends real effort on where Bayesian inference can fail or become misleading

That third part is essential. Wasserman is not presenting Bayesianism as an unquestioned upgrade over frequentist inference.

## Core mathematical objects

- prior `f(theta)`
- likelihood `f(x | theta)` or `L_n(theta)`
- posterior `f(theta | x^n)`
- posterior mean
- posterior interval
- function of parameter `tau = g(theta)`
- posterior simulation draws
- improper prior
- Jeffreys prior
- marginal posterior in multiparameter models
- posterior probability of hypotheses

## Bayesian and frequentist postulates

The chapter states the contrast explicitly.

Frequentist view:

- probability is limiting frequency
- parameters are fixed unknown constants
- procedures should have long-run frequency guarantees

Bayesian view:

- probability measures degree of belief
- probability statements about parameters are allowed
- inference proceeds by the posterior distribution over parameters

### Why this matters

This is not just philosophy. It determines what kinds of statements are considered meaningful:

- frequentist confidence statement about the procedure
- Bayesian probability statement about the parameter under the model

Those are different inferential objects.

## Bayesian method

The chapter writes the posterior as

`f(theta | x^n) = L_n(theta) f(theta) / c_n`

with

`c_n = int L_n(theta) f(theta) d theta`.

The standard slogan is:

- posterior proportional to likelihood times prior

### Why this formula matters

Everything else in the chapter is downstream of this one identity:

- point estimates
- intervals
- posterior for transformed parameters
- posterior simulation
- Bayesian tests

## Posterior summaries

### Posterior mean

`bar theta_n = int theta f(theta | x^n) d theta`.

This is the Bayes estimator under squared-error loss, a point the next chapter makes formal.

### Posterior interval

Choose `a` and `b` so that posterior tail areas are `alpha / 2`, giving

`P(theta in (a,b) | x^n) = 1 - alpha`.

This is a direct probability statement about `theta` under the posterior.

That is exactly the part many people find psychologically appealing.

## Conjugate examples

### Bernoulli-Beta

With uniform prior `f(p) = 1`, posterior becomes

`p | x^n ~ Beta(s + 1, n - s + 1)`.

With `Beta(alpha, beta)` prior, posterior becomes

`Beta(alpha + s, beta + n - s)`.

### What this teaches

The posterior mean can be written as

`bar p = lambda_n hat p + (1 - lambda_n) p_0`

where `p_0` is the prior mean.

This is shrinkage in its clearest form:

- data estimate
- prior center
- data-dependent weighting

### Normal-Normal

With known variance and Normal prior, the posterior is again Normal with mean

`bar theta = w bar X + (1 - w) a`

and variance `tau^2`.

Again the lesson is shrinkage and precision pooling:

- the posterior mean is a precision-weighted average of prior center and sample mean

## Functions of parameters

If `tau = g(theta)`, the posterior cdf is

`H(tau | x^n) = P(g(theta) <= tau | x^n)`.

The chapter works an explicit transformed-parameter example with the Bernoulli log-odds.

### Why this matters

Bayesian inference naturally extends to transformed parameters because once the full posterior over `theta` exists, any deterministic transform of `theta` inherits a posterior law.

This is conceptually simpler than re-deriving separate asymptotics for every transformed target.

## Simulation

If one can draw

`theta_1, ..., theta_B ~ f(theta | x^n)`,

then:

- histogram of draws approximates the posterior
- sample mean approximates posterior mean
- empirical quantiles approximate posterior intervals

And if `tau_b = g(theta_b)`, then `tau_1, ..., tau_B` approximate the posterior law of `tau`.

### Why this is important

Simulation shifts the burden from symbolic integration to algorithmic sampling. That is one of the practical strengths of Bayesian workflows, especially for nonlinear functionals.

## Large-sample properties

### Theorem 11.5

Under appropriate regularity conditions, the posterior is approximately Normal with:

- mean near the mle `hat theta_n`
- standard deviation near the frequentist standard error

and the usual asymptotic frequentist confidence interval is also approximately a Bayesian posterior interval.

### Appendix proof idea

The appendix says:

1. prior influence becomes negligible as `n` grows
2. log posterior is approximately log likelihood
3. Taylor expand around the mle
4. exponentiate the resulting quadratic form

This yields an approximately Gaussian posterior centered at the mle.

### Why this matters

This is the chapter's explanation for why Bayesian and frequentist procedures often agree in regular large samples. The agreement is not philosophical. It is asymptotic local curvature.

## Flat priors, improper priors, and noninformative priors

This is one of the strongest sections in the chapter because it refuses to romanticize "uninformative priors."

### Improper priors

A flat prior on an unbounded parameter may fail to integrate to one. Such an improper prior can still be useful if the resulting posterior is proper.

The chapter gives the Normal-location example where the improper flat prior reproduces the frequentist answer.

### Flat priors are not invariant

This is the really important conceptual point.

A flat prior on `p` does not induce a flat prior on `psi = log(p / (1-p))`.

So "flat" is coordinate-dependent, not intrinsically noninformative.

This matters because many users casually treat a flat prior as a neutral prior. The chapter correctly says that is not generally coherent.

### Jeffreys prior

Jeffreys proposes

`f(theta) proportional to I(theta)^(1/2)`,

which is transformation-invariant.

This does not solve every prior problem, but it is a principled answer to the invariance objection.

## Multiparameter problems

When `theta = (theta_1, ..., theta_p)`, interest usually focuses on one coordinate or one functional. Then the relevant inferential object is the marginal posterior:

`f(theta_1 | x^n) = int ... int f(theta_1, ..., theta_p | x^n) d theta_2 ... d theta_p`.

The chapter emphasizes simulation as the practical solution:

- draw from the joint posterior
- keep the coordinate of interest

This avoids hard integration.

## Bayesian testing

For testing

`H_0 : theta = theta_0`

versus

`H_1 : theta != theta_0`,

the Bayesian object is

`P(H_0 | x^n)`.

This requires:

- prior mass on the null
- prior density under the alternative

The chapter writes the posterior null probability in terms of:

- likelihood at the null
- integrated likelihood under the alternative

### Why this matters

This is fundamentally different from a p-value. It is model-and-prior dependent.

The chapter also notes a crucial practical point:

- improper priors cannot be used carelessly in testing because the denominator becomes undefined

So testing is much more prior-sensitive than estimation.

## Strengths and weaknesses

The chapter gives a balanced account.

### Strengths

- natural incorporation of prior information
- direct probabilistic statements about parameters under the model
- easy propagation to functions of parameters
- simulation-friendly inference

### Weaknesses

- prior sensitivity
- nontrivial meaning of "noninformative"
- absence of guaranteed long-run operating properties in general
- vulnerability in high-dimensional or nonparametric problems

## Failure examples

The last part of the chapter is unusually important because it shows specific regimes where Bayesian likelihood-centered inference can behave badly.

### Example 11.9

In a high-dimensional missing-data style problem, the likelihood effectively contains almost no information about many coordinates, so the posterior remains close to the prior and learns little about the target `psi`.

Meanwhile a frequentist Horvitz-Thompson style estimator can have small mse.

### Example 11.10

In a normalizing-constant problem, the Bayesian posterior can fail to extract information about the constant because the likelihood is proportional to `c^n`, making the data uninformative in the posterior sense, while a frequentist density-estimation route can still estimate `c`.

### Why these examples matter

The chapter's lesson is explicit:

- Bayesian methods are slaves to the likelihood

That phrase is intentionally sharp. It means Bayesian coherence does not protect you when the likelihood is structurally unhelpful for the inferential task.

## What the chapter is really teaching

The chapter is teaching two different things at once:

1. Bayesian inference is a coherent and powerful workflow
2. coherence does not imply universal reliability

That is the right lesson for a quant vault.

## Failure modes

- treating prior choice as harmless
- calling flat priors noninformative without checking parameterization
- confusing posterior probability with frequentist coverage
- ignoring likelihood weakness in high dimensions
- using Bayesian tests without realizing how prior-sensitive they are

## Quant research relevance

This chapter matters for quant research because Bayesian methods naturally support:

- shrinkage of noisy alpha estimates
- hierarchical pooling across assets, sectors, or signals
- posterior uncertainty for latent states
- simulation-based uncertainty for nonlinear payoffs or risk summaries

But the chapter's warning also matters:

- if the likelihood is weak, misspecified, or high-dimensional, posterior elegance can hide poor inferential behavior

That is especially relevant in modern quant workflows with many parameters, latent structure, and scarce effective sample sizes.

## What should be promoted out of this source note

- a durable note on Bayesian updating
- a durable note on conjugate shrinkage
- a durable note on posterior inference for transformed parameters
- a durable note on flat versus Jeffreys priors
- a durable note on when Bayesian inference can fail in high-dimensional settings

## Related notes

- [[All of Statistics]]
- [[All of Statistics - Ch 09 Parametric Inference]]
- [[All of Statistics - Ch 12 Statistical Decision Theory]]
- [[Probabilistic Machine Learning]]
- [[Stats Map]]

## Sources

- [[All of Statistics]]
- [[raw/math_statistics/2004 - wasserman - all of statistics.pdf]]
