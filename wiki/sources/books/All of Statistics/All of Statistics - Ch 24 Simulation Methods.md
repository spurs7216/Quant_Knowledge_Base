---
title: All of Statistics - Ch 24 Simulation Methods
type: source
status: chapter_ingested
updated: 2026-04-19
tags:
  - source
  - statistics
  - simulation
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: full_source
extraction_basis: full_text
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 24 Simulation Methods
parent_source: "[[All of Statistics]]"
sources:
  - "[[All of Statistics]]"
  - "[[raw/math_statistics/2004 - wasserman - all of statistics.pdf]]"
---
# All of Statistics - Ch 24 Simulation Methods

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed against the raw source.
- Pass 2: deep rewrite completed on Monte Carlo error, importance sampling, Metropolis-Hastings, Gibbs sampling, and the probabilistic logic that makes these algorithms work.

## Deepening Targets

- Promote the simulation methods here into durable computational notes once the vault needs them directly for Bayesian inference, rare-event estimation, pricing, or latent-state models.

## Deepened Subparts

- Monte Carlo integration, posterior simulation, importance sampling, Metropolis-Hastings detailed balance, tuning and mixing, Gibbs sampling, and Metropolis-within-Gibbs were rewritten at full note depth.

## Role of the chapter

This final chapter turns probability and inference into computational procedures. Earlier chapters defined expectations, posterior means, and process averages as mathematical objects. This chapter asks how to compute them when analytic integration is no longer feasible.

Its main topics are:

- Monte Carlo integration
- importance sampling
- Metropolis-Hastings
- Gibbs and related MCMC methods

This chapter is the computational endpoint of the book: once analytic formulas fail, simulation becomes the practical route.

## Core mathematical objects

- target integral `I = E[h(X)]`
- Monte Carlo estimator
- importance-sampling proposal
- Metropolis-Hastings acceptance rule
- Gibbs sampling
- Markov-chain Monte Carlo output
- detailed balance
- mixing

## Basic Monte Carlo integration

The chapter begins from the simplest simulation principle:

- if an expectation is hard to integrate analytically
- sample from the target law
- average the integrand

This is conceptually just the law of large numbers turned into an algorithm.

Writing

`I = integral h(x) f(x) dx = E_f[h(X)]`,

the estimator is

`\hat I = (1 / N) sum_i h(X_i)`.

The important point is not only consistency, but uncertainty quantification:

the Monte Carlo estimate comes with a standard error of order `N^{-1/2}`.

That rate is both the strength and weakness of basic Monte Carlo:

- it is dimension-agnostic in a way grid-based quadrature is not
- but naive sampling can be catastrophically inefficient if most draws miss the important region of the integrand

The Bayesian examples matter because they show how posterior expectations and posterior intervals can be reduced to simulation from the posterior law.

## Importance sampling

### Theorem 24.5

Importance sampling changes the sampling distribution and corrects by weights.

If direct sampling from `f` is hard, choose a proposal `g` and write

`I = integral h(x) f(x) dx = integral [h(x) f(x) / g(x)] g(x) dx = E_g[W]`

with weight

`W = h(X) f(X) / g(X)`.

The theorem characterizes the variance-minimizing proposal in principle.

This is a crucial result because it shows that Monte Carlo efficiency depends heavily on where simulation effort is allocated.

Theorem 24.5 says the optimal proposal is proportional to `|h(x)| f(x)`.

This is theoretically clean and practically revealing:

- a good proposal should look like the target times the integrand magnitude
- a bad proposal gives huge or unstable weights

The rule-of-thumb the chapter emphasizes is correct: choose `g` with thicker tails than `f` and a shape similar to where `|h| f` concentrates.

The tail-probability example makes the main point vivid: naive sampling is wasteful for rare events, and a better proposal can reduce variance dramatically.

This matters far beyond textbook integration. It is the same design problem that appears in rare-event finance, tail-risk estimation, and likelihood weighting.

## Metropolis-Hastings

The chapter then introduces MCMC when direct sampling from the target is hard.

The core idea is:

- propose a move
- accept or reject with a probability that preserves the target distribution

This turns simulation into a Markov-chain design problem.

The key conceptual point is that exact iid samples are replaced by dependent samples whose stationary distribution is the target.

The Metropolis-Hastings rule is:

1. propose `Y ~ q(y | X_i)`
2. accept with probability

`r(x, y) = min{ [f(y) / f(x)] [q(x | y) / q(y | x)], 1 }`

3. otherwise stay at the current state

The load-bearing argument is not the algorithmic recipe but why it works:

- the resulting transition kernel satisfies detailed balance with respect to `f`
- therefore `f` is stationary
- then Chapter 23's ergodic theorem justifies empirical averages along the chain

So MCMC is not a numerical hack. It is an engineered stochastic process.

The tuning discussion in the Cauchy example is also important. Proposal scale controls mixing:

- too small and the chain explores too slowly
- too large and the chain rejects too often and gets stuck

That is the first serious warning that dependent simulation requires design judgment, not just more iterations.

## Gibbs and other flavors

The Gibbs section shows how conditional distributions can be used as computational building blocks.

This is one of the major practical payoffs of the Bayesian and graphical-model chapters:

- if conditionals are easy, joint simulation may become feasible even when the joint law is analytically hard

The chapter's hierarchical-model example matters because it shows what Gibbs is really buying:

- break a hard joint posterior into simpler conditional updates
- iterate those conditional draws
- use the resulting chain to approximate posterior means, intervals, and shrinkage behavior

Metropolis-within-Gibbs is the natural generalization when some conditionals are still not directly samplable. That hybrid structure is more important in practice than the pure textbook Gibbs setting.

## What the chapter is really teaching

Simulation methods are not merely numerical tricks. They are probabilistic constructions:

- Monte Carlo uses iid sampling and the law of large numbers
- importance sampling uses change of measure
- MCMC uses invariant distributions of Markov chains

So each computational method is grounded in a probabilistic principle from earlier chapters.

The chapter is also teaching an efficiency hierarchy:

- if direct iid sampling from the target is possible, use it
- if not, but a good proposal exists, use importance sampling
- if even that is hard, construct a Markov chain with the right stationary law

That ordering is pragmatic and mathematically clean.

## Failure modes the chapter is trying to prevent

- treating Monte Carlo averages as exact without variance analysis
- using bad importance proposals that create unstable weights
- forgetting MCMC samples are dependent
- assuming apparent convergence of a chain proves true convergence
- using simulation without understanding the target distribution being approximated
- thinking a theoretically correct stationary distribution automatically means practically useful mixing
- ignoring proposal tuning and burn-in questions in dependent simulation

## Quant research relevance

This chapter is highly relevant to quant work:

- Monte Carlo pricing and risk estimation
- rare-event and tail-probability estimation
- Bayesian posterior computation
- simulation for hierarchical and latent-state models
- MCMC for latent-volatility, state-space, and hierarchical risk models

The chapter's main practical lesson is that computational feasibility depends on probabilistic design. A simulation method is only as good as its proposal, weighting, or transition kernel.

## Promoted durable notes

- [[Markov Chain Monte Carlo]]

## Next promotion targets

- a durable note on Monte Carlo integration
- a durable note on importance sampling
- a durable note on Metropolis-Hastings
- a durable note on Gibbs sampling
- a durable note on detailed balance and mixing

## Related notes

- [[All of Statistics]]
- [[Monte Carlo Methods]]
- [[Markov Chain Monte Carlo]]
- [[Probabilistic Machine Learning]]
- [[Signal Processing Map]]

## Sources

- [[All of Statistics]]
- [[raw/math_statistics/2004 - wasserman - all of statistics.pdf]]
