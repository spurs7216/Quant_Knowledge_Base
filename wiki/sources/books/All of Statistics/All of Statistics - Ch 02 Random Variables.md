---
title: All of Statistics - Ch 02 Random Variables
type: source
status: chapter_ingested
updated: 2026-04-19
tags:
  - source
  - statistics
  - probability
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: full_source
extraction_basis: full_text
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 02 Random Variables
parent_source: "[[All of Statistics]]"
sources:
  - "[[All of Statistics]]"
  - "[[raw/math_statistics/2004 - wasserman - all of statistics.pdf]]"
---
# All of Statistics - Ch 02 Random Variables

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed against the raw source.
- Pass 2: Full deep rewrite completed across the chapter.

## Deepening Targets

- Push the multivariate normal and change-of-variables pieces into durable method and concept notes.

## Deepened Subparts

- Whole chapter reworked at theorem-oriented depth.

## Role of the chapter

Chapter 1 builds probability on events. Chapter 2 explains how statistics gets from events to data.

The central move is this:

- the primitive object is still the probability space in the background
- a random variable is a measurable map from that space into the real line
- the distribution of the random variable is the induced law on the real line

Once that induced law is available, the sample space can recede from the surface. Statistics then works mainly with cdfs, pmfs, pdfs, joint laws, marginals, conditional laws, independence, and transformations. This chapter is therefore the real gateway from probability language to statistical modeling language.

## Core mathematical objects

- `X : Omega -> R`: random variable
- `X^{-1}(A) = {omega : X(omega) in A}`: preimage of a set `A subset R`
- `F_X(x) = P(X <= x)`: cumulative distribution function
- `f_X(x)`: pmf in the discrete case or pdf in the continuous case
- `F^{-1}(q) = inf{x : F(x) >= q}` as a quantile-type inverse cdf object
- `f_{X,Y}(x,y)`: joint pmf or joint pdf
- `f_X(x), f_Y(y)`: marginal laws
- `f_{X|Y}(x|y)`: conditional mass function or conditional density
- `X_1, ..., X_n iid`: independent and identically distributed sample
- `X in R^k`: random vector
- `N(mu, Sigma)`: multivariate normal law
- `Y = r(X)` or `Z = r(X,Y)`: transformed random variables

The whole chapter is about how these objects are defined, recognized, and manipulated correctly.

## The conceptual move from sample space to law

### Definition 2.1: random variable

A random variable is a mapping

`X : Omega -> R`.

The important correction is that the randomness is not in the function itself. The function is deterministic. The uncertainty comes from the random outcome `omega`.

This matters because it keeps clear the distinction between:

- the underlying experiment
- the measurable quantity extracted from that experiment
- the probability law induced on observed values

The book states the measurable-map caveat only in a footnote and appendix, but it is mathematically essential: for every threshold event `{omega : X(omega) <= x}` to have a probability, that event must belong to the admissible event class.

### Preimage logic

For any set `A subset R`,

`P(X in A) = P(X^{-1}(A))`.

This is one of the deepest sentences in the chapter. It says every probability statement about `X` is really an event statement on the original sample space, transported through the map `X`.

That is why later transformations, cdfs, conditional laws, and statistics all remain anchored in probability rather than floating as formal recipes.

## Cumulative distribution functions

### Definition 2.5: cdf

`F_X(x) = P(X <= x)`.

The cdf is the first truly universal description of a real-valued random variable. It works for:

- discrete laws
- continuous laws
- mixed laws with atoms and continuous parts

Unlike a pmf or pdf, the cdf always exists.

### Theorem 2.7: the cdf determines the law

If two random variables have the same cdf at every real `x`, then they have the same distribution on all measurable sets.

This is the key identification statement of the chapter. Once the cdf is known, the law is known.

The practical meaning is:

- a distribution is not just a name like Normal or Binomial
- it is an entire probability operator on subsets of the real line
- the cdf is one complete encoding of that operator

### Theorem 2.8: characterization of cdfs

A function `F : R -> [0,1]` is a cdf if and only if:

1. `F` is nondecreasing
2. `lim_{x -> -infinity} F(x) = 0` and `lim_{x -> +infinity} F(x) = 1`
3. `F` is right-continuous

This theorem is structurally important because it tells us exactly what kind of function can represent a distribution.

#### Why right continuity appears

The proof in the text derives right continuity from Theorem 1.8, continuity of probabilities for monotone event sequences.

If `y_i downarrow x`, then the events `(-infinity, y_i]` decrease to `(-infinity, x]`, so

`P(X <= y_i) -> P(X <= x)`.

Therefore `F(y_i) -> F(x)`, which is right continuity.

So right continuity is not an arbitrary convention. It is forced by the way probabilities interact with decreasing event limits.

## Discrete and continuous laws

### Definition 2.9: discrete random variable and pmf

If `X` takes countably many values `{x_1, x_2, ...}`, then

`f_X(x) = P(X = x)`

is the probability mass function.

The cdf is then

`F_X(x) = sum_{x_i <= x} f_X(x_i)`.

The distribution is encoded as jumps in the cdf.

### Definition 2.11: continuous random variable and pdf

`X` is continuous if there exists a nonnegative function `f_X` with integral one such that

`P(a < X < b) = integral_a^b f_X(x) dx`

for every interval `(a,b)`.

Then

`F_X(x) = integral_{-\infty}^x f_X(t) dt`

and where differentiable,

`f_X(x) = F'_X(x)`.

### Critical warning: a pdf is not a point probability

The chapter emphasizes a common but serious confusion:

- for discrete variables, `f_X(x) = P(X = x)`
- for continuous variables, `f_X(x)` is not `P(X = x)`

In fact, if `X` is continuous then `P(X = x) = 0` for every `x`.

So the density is local mass per unit length, not mass at a point.

This matters later in likelihood theory, continuous-time modeling, and conditional densities. Confusing density with point probability corrupts interpretation immediately.

### Density values can exceed one

Another important correction: a pdf may be greater than one, and even unbounded, provided its integral is one. Height is not probability; area is probability.

This is basic but easy to forget when thinking visually about densities.

## Lemma 2.15: extracting probabilities from the cdf

The chapter gives a useful lemma:

1. `P(X = x) = F(x) - F(x-)`
2. `P(x < X <= y) = F(y) - F(x)`
3. `P(X > x) = 1 - F(x)`
4. if `X` is continuous, endpoint choices on intervals do not matter

This lemma is where the practical relationship between:

- jumps
- atoms
- intervals
- tails

becomes operational.

The first identity is especially important. It shows that atoms of the law are exactly the jump sizes of the cdf.

## Quantile function and equality in distribution

### Definition 2.16: inverse cdf

The inverse cdf is defined by

`F^{-1}(q) = inf{x : F(x) >= q}`.

For strictly increasing continuous `F`, it is the unique solution to `F(x) = q`.

This object matters for:

- medians and quartiles
- simulation by inverse transform
- risk quantiles such as VaR-like tail summaries

### Equality in distribution

`X d= Y` means `F_X = F_Y`.

This does not mean `X = Y` pointwise. It means all distributional statements agree.

This distinction is essential in asymptotics, simulation, and distributional approximations. Many results later in statistics are statements of equality or convergence in distribution, not pathwise equality.

## Important named distributions in the chapter

The chapter catalogs standard discrete and continuous laws:

- point mass
- discrete uniform
- Bernoulli
- Binomial
- Geometric
- Poisson
- Uniform
- Normal
- Exponential
- Gamma
- Beta
- t
- Cauchy
- chi-square

This section is not just vocabulary. It teaches the difference between:

- random variables
- realized values
- fixed parameters

The warning in the Binomial section is important: `X` is random, `x` is a realized value, and parameters like `n` and `p` are fixed. Quant work frequently becomes confused precisely when parameters, latent states, and observed variables are mixed informally.

## Joint distributions

### Definition 2.19: joint law

For two variables `(X,Y)`, the joint cdf is

`F_{X,Y}(x,y) = P(X <= x, Y <= y)`.

In the discrete case the joint law is the table

`f(x,y) = P(X=x, Y=y)`.

In the continuous case, a joint pdf `f(x,y)` must:

1. be nonnegative
2. integrate to one over `R^2`
3. give probabilities by integrating over subsets of the plane

The main conceptual shift is that probability regions are now geometric subsets of `R^2`, not only intervals on the line.

### Support geometry matters

Examples 2.21 and 2.22 show the real difficulty in multivariate work:

- the integration region may be nonrectangular
- the support can impose dependence of limits on the other variable
- careless rectangular integration is wrong when the support is curved or triangular

This is one of the most practically relevant lessons of the chapter. In multivariate probability, support geometry is part of the law.

## Marginal distributions

### Definitions 2.23 and 2.25

Marginalization means integrating or summing out variables:

- discrete: `f_X(x) = sum_y f(x,y)`
- continuous: `f_X(x) = integral f(x,y) dy`

This operation is conceptually simple but mathematically important. It means:

- the joint law contains the full dependence structure
- univariate laws are projections of that joint law

Many quant workflows fail because people jump between joint and marginal thinking without keeping track of what dependence information has been discarded.

## Independence

### Definition 2.29

`X` and `Y` are independent if for every sets `A` and `B`,

`P(X in A, Y in B) = P(X in A) P(Y in B)`.

This is a distribution-level condition, not a correlation slogan.

### Theorem 2.30: factorization criterion

For densities, independence is equivalent to

`f_{X,Y}(x,y) = f_X(x) f_Y(y)`.

This theorem is what allows independence to be checked algebraically instead of over every measurable rectangle.

### Theorem 2.33: rectangle criterion

If the support is a rectangle and

`f(x,y) = g(x) h(y)`

for some functions `g` and `h`, then `X` and `Y` are independent.

The rectangle condition matters. Pure factorization is not enough if the support itself couples the variables.

This is a subtle point that often gets missed. Dependence can live in the support as well as in the formula.

## Conditional distributions

### Definition 2.35 and 2.36

For discrete variables,

`f_{X|Y}(x|y) = f_{X,Y}(x,y) / f_Y(y)`.

For continuous variables, the same algebraic formula defines the conditional density:

`f_{X|Y}(x|y) = f_{X,Y}(x,y) / f_Y(y)`.

The continuous case carries a conceptual warning: conditioning on `Y = y` is conditioning on a probability-zero event. The text deals with this by taking the density formula as the definition rather than trying to justify it fully at this level.

That is mathematically honest. It signals that conditional density is not just naive division on zero-probability events; it belongs to a deeper theory.

### Product decomposition

From the definition,

`f_{X,Y}(x,y) = f_{X|Y}(x|y) f_Y(y) = f_{Y|X}(y|x) f_X(x)`.

This identity is one of the core modeling templates in statistics:

- specify marginals and conditionals
- reconstruct the joint law
- infer one variable from another through conditioning

## Random vectors and iid samples

### Definition 2.41: iid

`X_1, ..., X_n` are iid with law `F` if:

- they are independent
- each has the same marginal distribution `F`

The chapter states explicitly that much of statistical theory begins here.

This is one of the most important modeling regimes in the whole subject, and later chapters depend heavily on it. The iid assumption is not reality by default; it is a simplifying structure that must be justified or criticized in applications.

## Multinomial and multivariate normal

### Multinomial

The Multinomial extends the Binomial from two outcomes to `k` categories. Its pmf is

`f(x) = n! / (x_1! ... x_k!) p_1^{x_1} ... p_k^{x_k}`

under the constraint `sum_j x_j = n`.

The marginal law of each component is Binomial with the corresponding category probability.

This is a canonical count model for categorical data and partitions of observations.

### Multivariate Normal

If `X ~ N(mu, Sigma)`, then

`f(x) = (2pi)^{-k/2} |Sigma|^{-1/2} exp( -1/2 (x-mu)^T Sigma^{-1} (x-mu) )`.

This chapter gives several structural facts:

1. affine generation: if `Z ~ N(0,I)` and `X = mu + Sigma^{1/2} Z`, then `X ~ N(mu, Sigma)`
2. marginals of a multivariate normal are normal
3. conditionals of a multivariate normal are normal
4. linear combinations are normal
5. the Mahalanobis quadratic form becomes chi-square

These are not ornamental properties. They explain why the multivariate normal is analytically dominant:

- closed under projection
- closed under conditioning
- closed under affine transformation

The conditional-normal formula in Theorem 2.44 is especially important for later regression, Kalman filtering, Gaussian state-space models, and Bayesian updating.

## Transformations of one random variable

The chapter gives the correct three-step workflow:

1. identify the set `A_y = {x : r(x) <= y}`
2. compute the cdf `F_Y(y) = P(r(X) <= y)`
3. differentiate to obtain `f_Y`

This is the general method.

### Formula (2.12): monotone change of variables

If `r` is strictly monotone with inverse `s = r^{-1}`, then

`f_Y(y) = f_X(s(y)) |ds(y)/dy|`.

This is the one-dimensional Jacobian rule.

The examples in the chapter show why the cdf-first approach is safer than memorizing formulas:

- if the map is not one-to-one, multiple branches contribute
- the transformed support can split into cases
- forgetting support restrictions gives the wrong density

The `Y = X^2` example on `X ~ Uniform(-1,3)` is exactly the kind of case where naive one-line substitution fails.

## Transformations of several random variables

For `Z = r(X,Y)`, the chapter again recommends:

1. identify the region `A_z = {(x,y) : r(x,y) <= z}`
2. compute `F_Z(z)` by integrating the joint density over that region
3. differentiate to obtain `f_Z`

The sum of two independent Uniform(0,1) variables is the canonical example. The resulting triangular density is not mysterious; it is a support-geometry calculation.

This is a central lesson:

- transformed densities are often geometry problems first and algebra problems second

## Appendix: measurability

The appendix states the correct foundational point:

`X` is a random variable only if it is measurable, meaning `{omega : X(omega) <= x}` lies in the sigma-field for every `x`.

This matters because the cdf is only well-defined if those threshold events are legitimate events.

So the chapter's full logical chain is:

1. probability lives on a sigma-field over `Omega`
2. random variables are measurable maps
3. measurable maps induce distributions on `R`
4. statistics studies those induced laws

## Failure modes the chapter is trying to prevent

- treating a random variable as an unstructured "random number" rather than a measurable map
- forgetting that cdfs exist for all laws, while pdfs and pmfs are special representations
- confusing pdf values with probabilities at points
- ignoring jump sizes and atoms in the cdf
- checking density factorization while ignoring support restrictions
- using conditional-density formulas without checking the denominator support
- applying change-of-variables formulas without verifying monotonicity or one-to-one structure
- forgetting that iid is an assumption, not a default truth about data
- conflating equality in distribution with equality of random variables

## Quant research relevance

This chapter is where probability becomes modelable data, and that makes it foundational for quant research.

### Returns, spreads, volumes, and latent states

Once market quantities are represented as random variables or random vectors, their laws become the objects of estimation, simulation, and conditioning.

### Support awareness

Many finance variables have constrained support:

- volatilities are nonnegative
- probabilities lie in `[0,1]`
- counts are integer-valued
- durations are positive

Using the wrong distribution class is often a support mistake before it is an estimation mistake.

### Joint and conditional structure

Cross-sectional alpha work, portfolio risk, options, and microstructure all rely on joint laws and conditional laws, not just univariate summaries.

### Transformations

Log returns, standardized residuals, rank transforms, volatility scaling, and latent-to-observed mappings are all transformation problems. If change-of-variables logic is weak, downstream inference is weak.

### Multivariate Gaussian structure

The conditional and affine-closure properties of the multivariate normal are central to:

- linear regression
- Gaussian Bayes updates
- Kalman filtering
- factor models
- many state-space approximations

## What should be promoted out of this source note

- a durable note on random variables as measurable maps and induced laws
- a durable note on cdfs, atoms, and quantiles
- a durable note on joint, marginal, and conditional distributions
- a durable note on independence and support-aware factorization
- a durable note on one-dimensional and multivariate change of variables
- a durable note on iid sampling as a modeling regime
- later, a dedicated multivariate normal note because its conditional structure is too important to remain source-bound

## Related notes

- [[All of Statistics]]
- [[All of Statistics - Ch 01 Probability]]
- [[All of Statistics - Ch 03 Expectation]]
- [[Stats Map]]
- [[Math Map]]

## Sources

- [[All of Statistics]]
- [[raw/math_statistics/2004 - wasserman - all of statistics.pdf]]
