---
title: All of Statistics - Ch 23 Probability Redux Stochastic Processes
type: source
status: chapter_ingested
updated: 2026-04-19
tags:
  - source
  - statistics
  - stochastic-processes
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: full_source
extraction_basis: full_text
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 23 Probability Redux Stochastic Processes
parent_source: "[[All of Statistics]]"
sources:
  - "[[All of Statistics]]"
  - "[[raw/math_statistics/2004 - wasserman - all of statistics.pdf]]"
---
# All of Statistics - Ch 23 Probability Redux Stochastic Processes

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed against the raw source.
- Pass 2: deep rewrite completed on Markov-chain structure, convergence, stationary laws, detailed balance, and Poisson-process mechanics.

## Deepening Targets

- Promote the Markov-chain and Poisson-process machinery into durable process notes once the vault begins using these objects directly in time-series, point-process, or MCMC work.

## Deepened Subparts

- Markov-chain transition algebra, recurrence and decomposition, ergodic convergence, detailed balance, inference for transition matrices, and Poisson-process waiting-time structure were rewritten at full note depth.

## Role of the chapter

This chapter returns to probability after the inferential middle of the book and asks what changes when randomness is indexed by time rather than represented by a single draw. The answer is that distributional questions become dynamic questions:

- how do local transition rules compose?
- which states communicate?
- when does long-run behavior exist?
- what kind of event-counting law generates arrivals over time?

The point is to move from single random variables to indexed families evolving over time.

## Core mathematical objects

- stochastic process `{X_t}`
- Markov chain
- transition probabilities
- Chapman-Kolmogorov equations
- communication classes
- recurrence and transience
- periodicity
- stationary distribution
- limiting distribution
- detailed balance
- Poisson process

## Processes as indexed random structure

The introductory examples make the right conceptual jump: a stochastic process is not one random variable but a whole family connected across time.

This is the right level of abstraction for dynamic systems, queueing, and state evolution.

## Markov chains

### Definitions 23.5 and 23.6

A Markov chain is defined by the memoryless property: the future depends on the present state, not the full past, once the present is known.

This is not a claim that the process is independent over time. It is a claim about sufficient state summarization.

### Theorem 23.9: Chapman-Kolmogorov

The Chapman-Kolmogorov equations describe how transition probabilities compose over multiple steps.

`p_ij(m + n) = sum_k p_ik(m) p_kj(n)`

and hence

`P^(m+n) = P^m P^n`.

This is one of the defining algebraic identities of Markov chains.

Lemma 23.10 then gives the marginal law:

`mu_n = mu_0 P^n`.

This is the first truly useful dynamic identity in the chapter. Once the initial law and one-step matrix are known, the entire finite-time distributional evolution is determined.

### Communication, recurrence, and decomposition

The chapter then develops:

- accessibility and communication
- recurrent versus transient states
- null versus positive recurrence
- decomposition of the state space into communicating classes

These are the structural classifications that tell you what a chain does in the long run.

Theorems 23.12 and 23.16 are the key classification results:

- communication is an equivalence relation
- recurrence / transience is constant within a communicating class
- every finite irreducible chain has recurrent states, and finite irreducible chains are fully recurrent

Theorem 23.15 gives the practical criterion:

- recurrent iff `sum_n p_ii(n) = infinity`
- transient iff `sum_n p_ii(n) < infinity`

The decomposition theorem then says the state space splits into transient states plus closed irreducible recurrent classes. This is the chapter's structural map of any finite chain.

### Periodicity, ergodicity, and stationary laws

The later sections define ergodicity and stationary distributions.

The deep lesson is that long-run behavior depends not only on one-step transitions, but on the connectivity and periodic structure of the chain.

This is where the chapter becomes directly relevant to later computation.

The stationary distribution `pi` satisfies

`pi = pi P`.

But stationarity alone does not imply convergence. Periodic chains can have stationary distributions and still fail to settle down.

Theorem 23.25 is the chapter's main convergence result:

an irreducible, ergodic chain has a unique stationary distribution, the limiting distribution exists and equals it, and sample averages satisfy a law of large numbers:

`(1/N) sum_{n=1}^N g(X_n) -> E_pi[g]`.

This is the theorem that later makes MCMC valid.

Theorem 23.26 shows that detailed balance implies stationarity:

`pi_i p_ij = p_ji pi_j`

is sufficient to guarantee `pi P = pi`.

That condition will become the design principle behind Metropolis-Hastings.

## Poisson processes

The Poisson-process section extends discrete-time state evolution to event-counting in continuous time.

The key features are:

- counting arrivals over time
- independent increments
- rate-based description of event flow

This is the canonical rare-event arrival model.

Definition 23.32 gives the structure precisely:

1. `X(0) = 0`
2. disjoint increments are independent
3. one jump in a short interval occurs with probability `lambda(t) h + o(h)`, while two or more jumps are `o(h)`

Theorem 23.33 identifies the law:

`X(s+t) - X(s) ~ Poisson(m(s+t) - m(s))`

where

`m(t) = integral_0^t lambda(u) du`.

So the entire process is pinned down by the intensity function.

For the homogeneous case `lambda(t) = lambda`, Theorem 23.35 gives the waiting-time structure:

- interarrival times are iid exponential with mean `1 / lambda`
- waiting time to the `n`th event is Gamma

This is the process-side analogue of the memoryless property.

The chapter's warning via the email example is also important: a homogeneous Poisson process is easy to test and often false in real applications because the intensity usually varies over time.

## Inference for Markov chains

The final Markov-chain section is easy to skip, but it matters. Observing transitions in a finite chain turns each row of `P` into a multinomial estimation problem.

The mle is

`\hat p_ij = n_ij / n_i`

where `n_ij` counts observed `i -> j` transitions.

The asymptotic-Normality theorem under ergodicity is the chapter's bridge from process definition to statistical inference. Dynamic models are still estimable models.

## What the chapter is really teaching

A process is governed by:

- local transition or increment rules
- structural state-space properties
- long-run behavior implied by those rules

That is the dynamic analogue of how a distribution is governed by its support and factorization.

The hierarchy is:

- transition kernel for local movement
- communication and recurrence for structural classification
- stationarity / ergodicity for long-run averages
- detailed balance as a constructive route to stationarity
- intensity functions for continuous-time counting dynamics

## Failure modes the chapter is trying to prevent

- confusing Markov with independent
- ignoring state-space decomposition and long-run classes
- interpreting stationarity as automatic rather than as a property to be checked
- using a Poisson-process intuition in settings where dependence or clustering dominates
- believing a stationary distribution guarantees convergence
- reading one-step intuition into a chain whose long-run behavior is controlled by recurrence and periodicity

## Quant research relevance

This chapter is directly relevant to quant work:

- regime-switching intuitions
- state evolution in filtering problems
- order-arrival or event-arrival modeling
- microstructure event timing
- queueing-style approximations
- MCMC foundations through ergodic averages and detailed balance

The most important lesson is that dynamic structure needs explicit modeling. One cannot infer long-run behavior from one-step intuition alone.

## Promoted durable notes

- [[Markov Chains]]

## Next promotion targets

- a durable note on stationary and limiting distributions
- a durable note on Poisson processes
- a durable note on detailed balance and ergodic averages

## Related notes

- [[All of Statistics]]
- [[Markov Chains]]
- [[Kalman Filtering]]
- [[Stochastic Calculus]]
- [[Signal Processing Map]]

## Sources

- [[All of Statistics]]
- [[raw/math_statistics/2004 - wasserman - all of statistics.pdf]]
