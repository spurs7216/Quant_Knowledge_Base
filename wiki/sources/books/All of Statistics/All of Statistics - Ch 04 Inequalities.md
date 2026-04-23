---
title: All of Statistics - Ch 04 Inequalities
type: source
status: chapter_ingested
updated: 2026-04-19
tags:
  - source
  - statistics
  - inequalities
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: full_source
extraction_basis: full_text
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 04 Inequalities
parent_source: "[[All of Statistics]]"
sources:
  - "[[All of Statistics]]"
  - "[[raw/math_statistics/2004 - wasserman - all of statistics.pdf]]"
---
# All of Statistics - Ch 04 Inequalities

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed against the raw source.
- Pass 2: the full theorem spine of the chapter was rewritten, including proof ideas for Markov, Chebyshev, Hoeffding, Mill's inequality, Cauchy-Schwarz, and Jensen.

## Deepening Targets

- If this book becomes the main concentration reference for the vault, deepen the exercise layer around exponential-vs-polynomial tails and add a dedicated durable note on mgf-based concentration arguments.

## Deepened Subparts

- Whole chapter reworked at theorem-oriented depth.

## Role of the chapter

This chapter is the first place in the book where probability becomes a control technology rather than a descriptive language.

The question is no longer:

- what is the exact distribution?

The question becomes:

- how much tail mass can exist if I only know a mean, a variance, boundedness, or convexity?

That shift is fundamental. In most real research problems, especially in quant work, one does not know the exact finite-sample law of the statistic of interest. What one often does know is some structural information:

- the variable is nonnegative
- variance exists
- summands are independent
- summands are bounded
- a payoff or loss map is convex

Inequalities convert those structural facts into usable bounds.

## Core mathematical objects

- nonnegative random variable `X`
- centered variable `X - EX`
- deviation event `{|X - EX| >= t}`
- independent bounded sum `sum_i Y_i`
- mgf-like quantity `E exp(tY)`
- convex function `g`
- expectation `Eg(X)`

The chapter should be read as a hierarchy of what can be concluded under progressively stronger assumptions.

## Structural map of the chapter

The chapter has two blocks:

1. probability inequalities
2. inequalities for expectations

The first block controls tail probabilities. The second block controls what happens when nonlinear maps interact with averaging.

## Theorem spine

### Theorem 4.1: Markov's inequality

If `X >= 0` and `E(X)` exists, then for every `t > 0`,

`P(X > t) <= E(X) / t`.

### What the statement is really saying

If a nonnegative variable keeps substantial probability mass above a high threshold `t`, then its mean must also be large. Equivalently, a fixed mean puts an upper bound on how much probability can live far into the right tail.

### Proof skeleton

Write

`E(X) = int_0^t x f(x) dx + int_t^infty x f(x) dx`.

On the tail region `x >= t`, we have `x >= t`, so

`int_t^infty x f(x) dx >= t int_t^infty f(x) dx = t P(X > t)`.

Hence `E(X) >= t P(X > t)`.

### Why this matters

This proof is primitive in the right way. It teaches a recurring pattern:

1. identify a hard event
2. dominate the indicator of that event by a scaled nonnegative variable
3. turn the probability question into an expectation question

That template reappears constantly in asymptotic theory.

### Limit of the theorem

Markov is universal but weak. A first moment alone cannot identify sharp tail behavior.

## Theorem 4.2: Chebyshev's inequality

If `mu = E(X)` and `sigma^2 = Var(X)`, then

`P(|X - mu| >= t) <= sigma^2 / t^2`.

Equivalently, for `Z = (X - mu) / sigma`,

`P(|Z| >= k) <= 1 / k^2`.

### Proof skeleton

Apply Markov to the nonnegative variable `(X - mu)^2`:

`P(|X - mu| >= t) = P((X - mu)^2 >= t^2) <= E(X - mu)^2 / t^2 = sigma^2 / t^2`.

### What changed relative to Markov

Markov uses only a first moment of a nonnegative variable.

Chebyshev gains symmetry-aware deviation control by first:

- centering
- squaring
- then applying Markov

This is the first important example of transforming the random variable before applying a generic inequality.

### Statistical meaning

Chebyshev is distribution-free once variance exists. It does not try to be sharp. It gives a worst-case concentration statement across all distributions sharing the same variance.

### Quant relevance

Chebyshev is often too loose for production use, but it is an important sanity bound when:

- only second moments are trusted
- tails may be misspecified
- one wants a conservative bound on estimator fluctuation

## Hoeffding's inequality

### Theorem 4.4

Let `Y_1, ..., Y_n` be independent with `E(Y_i) = 0` and `a_i <= Y_i <= b_i`. Then for any `t > 0` and any `eps > 0`,

`P(sum_i Y_i >= eps) <= exp(-t eps) prod_i exp(t^2 (b_i - a_i)^2 / 8)`.

This is the exponential-mgf intermediate form.

### Theorem 4.5

For Bernoulli data `X_1, ..., X_n ~ Bernoulli(p)` and sample mean `bar X_n`,

`P(|bar X_n - p| > eps) <= 2 exp(-2 n eps^2)`.

### Why Hoeffding is qualitatively different

Chebyshev gives polynomial decay:

`O(1 / (n eps^2))`.

Hoeffding gives exponential decay:

`O(exp(-c n eps^2))`.

That difference is not cosmetic. It reflects stronger assumptions:

- independence
- boundedness
- zero-mean centering

The chapter is teaching a law of probability research that never goes away:

- stronger assumptions buy stronger concentration
- but only if those assumptions are actually credible

### Proof idea in the appendix

The appendix proves Theorem 4.4 by combining:

1. Markov on an exponential transform
2. factorization from independence
3. a convexity bound on `exp(t Y_i)`
4. a Taylor bound on the resulting log-mgf surrogate

The argument starts from

`P(sum_i Y_i >= eps) = P(exp(t sum_i Y_i) >= exp(t eps))`

and then applies Markov:

`P(sum_i Y_i >= eps) <= exp(-t eps) E exp(t sum_i Y_i)`.

Independence factorizes the expectation:

`E exp(t sum_i Y_i) = prod_i E exp(t Y_i)`.

The subtle step is bounding each `E exp(t Y_i)` using the fact that `Y_i` lies in `[a_i, b_i]`. Since `exp(ty)` is convex, each `Y_i` can be represented as a convex combination of its endpoints, which yields an endpoint-based bound. The appendix then rewrites that bound as `exp(g(u))`, shows `g(0) = g'(0) = 0`, and bounds `g''(u) <= 1/4`. Taylor's theorem then gives

`g(u) <= u^2 / 8`,

which yields

`E exp(t Y_i) <= exp(t^2 (b_i - a_i)^2 / 8)`.

This is the mgf mechanism behind the concentration inequality.

### Why the proof matters

The proof is not merely a derivation for one theorem. It introduces a whole concentration paradigm:

- exponentiate
- apply Markov
- factorize by independence
- bound the mgf
- optimize or specialize

This is one of the most reusable proof strategies in probability and statistical learning.

## Mill's inequality

### Theorem 4.7

For `Z ~ N(0,1)`,

`P(|Z| > t) <= sqrt(2 / pi) exp(-t^2 / 2) / t`.

### Role in the chapter

This theorem is structurally different from Markov, Chebyshev, and Hoeffding. It is not distribution-free. It is law-specific.

That is why the bound is sharper: it exploits the exact Gaussian tail shape.

### Why it matters later

Once Normal approximations appear in Chapters 5 to 10, one needs intuition for what a tail area of `z = 2`, `3`, or `4` really means. Mill's inequality gives a clean analytic upper bound on those tail probabilities.

## Theorem 4.8: Cauchy-Schwarz

If `X` and `Y` have finite second moments, then

`E |XY| <= sqrt(E(X^2) E(Y^2))`.

### Why it matters

This is not just an inequality about expectations. It is the algebraic foundation of:

- covariance bounds
- correlation bounded by 1
- orthogonality arguments
- projection geometry in `L2`

### Conceptual meaning

Cauchy-Schwarz says the bilinear interaction `E(XY)` cannot exceed the geometric mean of the individual quadratic sizes. It is the inequality that turns variance and covariance into Euclidean-like geometry.

## Theorem 4.9: Jensen's inequality

If `g` is convex, then

`E g(X) >= g(E X)`.

If `g` is concave, the inequality reverses.

### Proof idea

Take the tangent line `L(x) = a + bx` to `g` at `EX`. Convexity implies `g(x) >= L(x)` for all `x`. Taking expectations gives

`E g(X) >= E L(X) = L(EX) = g(EX)`.

### Why this theorem is deep

Jensen explains the sign of the failure of commutation between:

- averaging
- applying a nonlinear map

That is a major structural fact, not a computational trick.

Examples:

- `E(X^2) >= (EX)^2`
- if `X > 0`, then `E(1 / X) >= 1 / EX`
- because `log` is concave, `E log X <= log EX`

### Quant relevance

Jensen is everywhere in finance:

- log returns versus simple returns
- convex option payoffs
- risk measures
- utility curvature
- bias induced by nonlinear transformations

If one does not know the sign imposed by convexity or concavity, one will repeatedly make the wrong economic interpretation.

## Hierarchy of information in the chapter

The chapter can be organized as a ladder:

1. `X >= 0` and `E(X)` finite  
   Gives Markov.
2. finite variance after centering  
   Gives Chebyshev.
3. independent bounded summands  
   Gives Hoeffding-style exponential concentration.
4. exact Gaussian law  
   Gives Mill's inequality.
5. quadratic structure in `L2`  
   Gives Cauchy-Schwarz.
6. convexity or concavity  
   Gives Jensen.

This ladder is the real content of the chapter. Each extra structural assumption changes what kind of bound becomes available.

## What the chapter is really teaching

The chapter teaches that a probability bound is always paid for by assumptions.

If the only thing known is a mean, one gets a very rough tail bound.

If variance is known, one gets a better but still loose deviation bound.

If boundedness and independence are known, one gets exponential concentration.

If convexity is known, one can reason about the direction of nonlinear bias.

The mathematical lesson is:

- the quality of the bound is determined by the structure one can defend

The research lesson is:

- never use a strong bound without asking whether its assumptions are genuinely plausible for the data-generating process

## Exercises that carry the chapter

Several exercises reveal what the chapter actually wants the reader to internalize:

- compare exact tails to Chebyshev for Exponential and Poisson laws
- compare Chebyshev and Hoeffding for Bernoulli means
- derive Hoeffding-based confidence intervals for `p`
- prove Mill's inequality
- compare moment-based Markov bounds to Gaussian-specific bounds

These exercises force the reader to confront looseness, sharpness, and assumption dependence.

## Failure modes

- treating Markov or Chebyshev as approximations rather than upper bounds
- forgetting the nonnegativity condition in Markov
- forgetting that Chebyshev is centered variance control, not exact tail modeling
- using Hoeffding when observations are dependent, heavy-tailed, or unbounded
- invoking Jensen without checking whether the map is convex or concave
- forgetting that Gaussian tail bounds are law-specific, not universal

## Quant research relevance

This chapter is foundational for quant work because almost every live-research claim has a hidden concentration argument behind it:

- how stable is a sample mean or hit rate?
- how much can a signal metric move due to sampling noise?
- how much confidence should one place in an apparently strong outperformance number?
- how much bias is introduced by a nonlinear transformation of a noisy estimate?

Concrete links:

- Hoeffding-style intuition matters for bounded classification or event-rate problems
- Jensen matters for log utility, log returns, and convex payoffs
- Cauchy-Schwarz underlies covariance and correlation reasoning used everywhere in risk and factor models
- Chebyshev gives a robust fallback when exact tails are not trusted

## What should be promoted out of this source note

- a durable note on concentration bounds by assumption level
- a durable note on the mgf proof strategy for Hoeffding
- a durable note on Jensen's inequality for quant researchers
- a durable note on Cauchy-Schwarz and covariance geometry

## Related notes

- [[All of Statistics]]
- [[All of Statistics - Ch 03 Expectation]]
- [[All of Statistics - Ch 05 Convergence of Random Variables]]
- [[Math Map]]
- [[Stats Map]]

## Sources

- [[All of Statistics]]
- [[raw/math_statistics/2004 - wasserman - all of statistics.pdf]]
