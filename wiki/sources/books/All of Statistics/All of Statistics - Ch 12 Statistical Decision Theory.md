---
title: All of Statistics - Ch 12 Statistical Decision Theory
type: source
status: chapter_ingested
updated: 2026-04-19
tags:
  - source
  - statistics
  - decision-theory
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: full_source
extraction_basis: full_text
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 12 Statistical Decision Theory
parent_source: "[[All of Statistics]]"
sources:
  - "[[All of Statistics]]"
  - "[[raw/math_statistics/2004 - wasserman - all of statistics.pdf]]"
---
# All of Statistics - Ch 12 Statistical Decision Theory

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed against the raw source.
- Pass 2: the chapter was rewritten around loss, risk, Bayes rules, minimax rules, admissibility, the large-sample relation to mle, and Stein's paradox.

## Deepening Targets

- If this chapter becomes the main decision-theory spine for the vault, add durable notes on least favorable priors, admissibility versus practical usefulness, and James-Stein shrinkage as a bridge to modern regularization.

## Deepened Subparts

- Whole chapter reworked at theorem-oriented depth.

## Role of the chapter

This chapter asks the question that should have been hanging over every previous estimator:

- by what criterion are we calling one rule better than another?

Its answer is:

- choose a loss
- average that loss under the model
- compare procedures through their risk functions or summaries of risk

That is the right conceptual endpoint of the first twelve chapters. Probability, inference, likelihood, and Bayes all produce procedures. Decision theory says how to judge them.

## Core mathematical objects

- loss `L(theta, hat theta)`
- risk `R(theta, hat theta) = E_theta L(theta, hat theta(X))`
- maximum risk
- Bayes risk
- Bayes rule
- minimax rule
- admissibility
- least favorable prior
- James-Stein estimator

## Preliminaries: loss and risk

### Definition 12.1

Risk is

`R(theta, hat theta) = E_theta[L(theta, hat theta)]`.

Under squared-error loss,

`R(theta, hat theta) = Var_theta(hat theta) + bias_theta(hat theta)^2`.

### Why this matters

This definition exposes a truth many applied discussions hide:

- there is no estimator that is simply "best" without a loss function

The meaning of good estimation depends on what kinds of mistakes matter.

## Comparing risk functions

The early examples show why estimator comparison is hard:

- one estimator can have lower risk near one part of the parameter space
- another can have lower risk elsewhere

So pointwise risk comparison often fails to give a clean ranking.

This motivates one-number summaries.

### Definition 12.4

- maximum risk: `bar R(hat theta) = sup_theta R(theta, hat theta)`
- Bayes risk: `r(f, hat theta) = int R(theta, hat theta) f(theta) d theta`

These are different ways to collapse a risk function into a scalar objective.

### Important lesson

Neither summary is perfect:

- maximum risk is robust but can be conservative
- Bayes risk depends on the chosen prior

The chapter is not trying to eliminate judgment. It is trying to make the judgment explicit.

## Bayes estimators

### Definition 12.6

A Bayes rule minimizes Bayes risk for a prior `f`.

### Posterior risk

Define

`r(hat theta | x) = int L(theta, hat theta(x)) f(theta | x) d theta`.

### Theorem 12.7

The Bayes risk can be written as

`r(f, hat theta) = int r(hat theta | x) m(x) d x`.

Hence minimizing Bayes risk reduces to minimizing posterior risk pointwise in `x`.

### Why this theorem matters

It converts a global optimization over procedures into a local posterior optimization problem.

This is the bridge between Bayesian inference and Bayesian decision theory.

### Theorem 12.8

For common losses:

- squared error -> posterior mean
- absolute error -> posterior median
- zero-one loss -> posterior mode

### Why this theorem is deep

This result explains that "posterior mean," "posterior median," and "posterior mode" are not interchangeable stylistic choices. Each is optimal for a different loss.

That is a core decision-theoretic lesson:

- the right summary of uncertainty depends on the objective

## Minimax rules

### Definition 12.6

A minimax rule minimizes the maximum risk.

### Theorem 12.10

If a Bayes rule `hat theta_f` satisfies

`R(theta, hat theta_f) <= r(f, hat theta_f)` for all `theta`,

then it is minimax and `f` is a least favorable prior.

### Theorem 12.11

A particularly clean sufficient condition is constant risk. If a Bayes rule has risk

`R(theta, hat theta) = c`

for all `theta`, then it is minimax.

### Why these theorems matter

They build one of the chapter's main bridges:

- Bayes and minimax are not unrelated doctrines

A Bayes rule under a suitably chosen prior can produce a minimax solution.

## Normal and Bernoulli examples

The chapter uses Bernoulli examples to show how:

- the mle may have lower Bayes risk under one prior
- a different estimator may have smaller maximum risk

This is important because it demonstrates that estimator quality depends on the criterion, not on a universal ranking.

## MLE, minimax, and Bayes in large samples

The chapter then revisits the mle from a decision-theoretic viewpoint.

For regular parametric models and large `n`,

- variance dominates squared bias
- mle variance is approximately `1 / (n I(theta))`
- no regular competitor can do better in the local asymptotic sense

So the chapter summarizes:

- in most regular parametric large-sample settings, the mle is approximately minimax and approximately Bayes

### Important caveat

The chapter immediately says this breaks down when the number of parameters is large.

That caveat is not optional. It points directly toward modern high-dimensional statistics.

## Many Normal means example

The chapter's high-dimensional warning is precise.

If there are as many parameters as observations, the mle can have risk `sigma^2`, while the minimax risk can be approximately

`sigma^2 / (sigma^2 + c^2)`,

which is smaller.

This says:

- the comforting large-sample optimality of the mle is not robust to high-dimensional regimes

That is a critical lesson for quant research.

## Admissibility

### Definition 12.17

An estimator is inadmissible if another rule has risk no larger everywhere and strictly smaller somewhere.

### Why admissibility matters

Admissibility is a minimal rationality filter:

- an inadmissible rule is strictly dominated

But the chapter also shows admissibility is not enough to guarantee good practical behavior. A terrible constant rule can still be admissible in some settings.

### Theorem 12.19

Under continuity and full-support prior assumptions, Bayes rules are admissible.

### Why this matters

This is another structural bridge:

- Bayes optimality under a rich prior implies no uniform domination

## Links between minimaxity and admissibility

### Theorem 12.21

If a rule has constant risk and is admissible, then it is minimax.

### Theorem 12.23

A minimax rule cannot be strongly inadmissible.

These theorems show the concepts overlap but are not identical.

## Stein's paradox

This is the chapter's intellectual climax.

For one Normal mean under squared-error loss, `hat theta = X` is admissible.

For two independent Normal means, coordinatewise estimation is still admissible.

But for `k >= 3` Normal means, the estimator

`hat theta(X) = X`

becomes inadmissible, and the James-Stein rule

`hat theta_i^S(X) = (1 - (k - 2) / sum_i X_i^2)_+ X_i`

has smaller risk.

### Why this is shocking

It says:

- even when the coordinates are unrelated
- even when each coordinate separately looks fine

joint shrinkage can beat coordinatewise mle.

### What the theorem is really saying

The issue is not mystical. When estimating many related quantities simultaneously, borrowing strength reduces total risk enough to dominate naive separate estimation.

This is the conceptual root of:

- shrinkage
- regularization
- empirical Bayes
- high-dimensional risk estimation

## What the chapter is really teaching

The chapter is teaching that statistical procedures must be judged through an explicit decision criterion.

In particular:

1. define the loss
2. compute the induced risk
3. decide whether to optimize worst-case, prior-averaged, or dominance-based criteria
4. remember high-dimensional regimes can reverse naive optimality claims

## Failure modes

- calling an estimator good without specifying the loss
- using admissibility as if it guaranteed practical quality
- assuming mle remains optimal in high dimensions
- confusing Bayes optimality under one prior with universal superiority
- ignoring shrinkage opportunities when many parameters are estimated jointly

## Quant research relevance

This chapter is highly relevant to quant research because many live problems are fundamentally decision-theoretic:

- alpha estimates under noisy data
- shrinkage of expected returns and risk parameters
- simultaneous estimation across many assets or signals
- portfolio construction under asymmetric costs of over- and under-estimation

James-Stein is especially important conceptually. It says that in multi-asset or multi-signal settings, independent point estimation is often dominated by structured shrinkage.

That is one of the deepest bridges from mathematical statistics to deployable quant research.

## Promoted durable notes

- [[Statistical Decision Theory]]

## Next promotion targets

- a durable note on Bayes versus minimax reasoning
- a durable note on admissibility
- a durable note on James-Stein shrinkage and why it matters

## Related notes

- [[All of Statistics]]
- [[Statistical Decision Theory]]
- [[All of Statistics - Ch 11 Bayesian Inference]]
- [[Portfolio Construction]]
- [[Stats Map]]

## Sources

- [[All of Statistics]]
- [[raw/math_statistics/2004 - wasserman - all of statistics.pdf]]
