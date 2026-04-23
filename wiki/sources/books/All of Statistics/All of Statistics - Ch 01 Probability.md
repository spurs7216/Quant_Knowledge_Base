---
title: All of Statistics - Ch 01 Probability
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
chapter_or_section: Ch 01 Probability
parent_source: "[[All of Statistics]]"
sources:
  - "[[All of Statistics]]"
  - "[[raw/math_statistics/2004 - wasserman - all of statistics.pdf]]"
---
# All of Statistics - Ch 01 Probability

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed against the raw source.
- Pass 2: Full deep rewrite completed across the chapter.

## Deepening Targets

- Keep extending proof-level extraction from the appendix and the high-value exercises if this chapter becomes a primary teaching spine.

## Deepened Subparts

- Whole chapter reworked at theorem-oriented depth.

## Role of the chapter

This chapter does not merely introduce notation. It fixes the logical order of the whole book:

1. define uncertainty at the event level
2. impose coherence through the probability axioms
3. derive identities from those axioms
4. define conditioning and Bayes updating on top of that structure
5. only later move to random variables, expectation, convergence, and inference

That order matters. If probability is treated as a bag of formulas instead of a coherent set function on events, later statistics becomes fragile. Hypothesis testing, likelihood, Bayesian updating, asymptotics, graphical models, and stochastic-process arguments all inherit their logic from this chapter.

## Core mathematical objects

- `Omega`: sample space
- `omega in Omega`: realized outcome
- `A, B subset Omega`: events
- `A^c`: complement
- `A union B`: union
- `AB` or `A intersection B`: intersection
- `A - B`: set difference
- `A subset B`: inclusion
- `emptyset`: null event
- `I_A(omega)`: indicator of event `A`
- `A_1, A_2, ...`: partition or sequence of events
- `P(A)`: probability assigned to event `A`
- `P(A | B)`: conditional probability when `P(B) > 0`

The chapter works mostly on the full event class for intuition, but the appendix states the mathematically correct object: a probability measure is defined on a sigma-field `A`, not necessarily on every subset of `Omega`.

## Structural map of the chapter

The chapter has six conceptual blocks:

1. sample spaces and events
2. axiomatic probability
3. finite sample spaces and counting
4. independence
5. conditional probability
6. Bayes theorem and the law of total probability

The appendix then introduces sigma-fields and measurable spaces, which is the measure-theoretic repair behind the informal presentation.

## Definitions and theorem spine

### Sample space and events

The book starts with `Omega` as the set of possible outcomes and events as subsets of `Omega`.

This is mathematically basic but conceptually nontrivial. A probability model is not first a density, a table, or a random variable. It is first:

- a set of possible states of the world
- a collection of admissible events
- a rule assigning probabilities to those events

This framing is what later makes conditioning, partitions, and set limits rigorous.

### Definition 1.5: probability measure

`P` is a probability measure if:

1. `P(A) >= 0` for every event `A`
2. `P(Omega) = 1`
3. if `A_1, A_2, ...` are disjoint, then `P(union_i A_i) = sum_i P(A_i)`

These are not arbitrary bookkeeping rules. They encode:

- impossibility of negative mass
- certainty of the whole sample space
- coherence under disjoint decomposition

Everything important in the chapter is derived from these axioms plus set identities.

### Definition 1.9: independence

Two events `A` and `B` are independent if

`P(AB) = P(A) P(B)`.

For a family `{A_i : i in I}`, independence means

`P(intersection_{i in J} A_i) = product_{i in J} P(A_i)`

for every finite subset `J` of the index set.

This is the correct strong notion. Independence of a family is not merely pairwise independence.

### Definition 1.12: conditional probability

For `P(B) > 0`,

`P(A | B) = P(AB) / P(B)`.

This is the restriction-and-renormalization operation that turns the event `B` into the effective sample space.

### Theorem 1.8: continuity of probabilities

If `A_n -> A` monotonically, then

`P(A_n) -> P(A)`.

This result is easy to overlook, but it is one of the deepest structural statements in the chapter. It says the probability measure respects monotone set limits. Later, this principle sits behind convergence arguments, tail events, and limiting approximations.

### Theorem 1.16: law of total probability

If `A_1, ..., A_k` is a partition of `Omega`, then for any event `B`,

`P(B) = sum_i P(B | A_i) P(A_i)`.

This is the canonical regime-decomposition identity.

### Theorem 1.17: Bayes theorem

If `A_1, ..., A_k` is a partition with `P(A_i) > 0` and `P(B) > 0`, then

`P(A_i | B) = P(B | A_i) P(A_i) / sum_j P(B | A_j) P(A_j)`.

This is not a separate law of nature. It is conditional probability plus partitioning.

## What the axioms already imply

Several identities in the chapter are not postulates. They are consequences of the axioms and therefore part of what the axioms mean.

### `P(emptyset) = 0`

Proof idea:

- `Omega = Omega union emptyset`
- the two sets are disjoint
- additivity gives `P(Omega) = P(Omega) + P(emptyset)`
- therefore `P(emptyset) = 0`

This is the first example of the axioms forcing structure.

### Monotonicity

If `A subset B`, then `P(A) <= P(B)`.

Proof idea:

- write `B = A union (B - A)`
- the pieces are disjoint
- `P(B) = P(A) + P(B - A) >= P(A)`

This is why set inclusion corresponds to probability ordering.

### Complement rule

`P(A^c) = 1 - P(A)`.

Proof idea:

- `Omega = A union A^c`
- the pieces are disjoint
- `1 = P(Omega) = P(A) + P(A^c)`

This identity is simple but essential. Many tail probabilities and error probabilities are more tractable through complements.

### Addition formula for disjoint events

If `AB = emptyset`, then

`P(A union B) = P(A) + P(B)`.

This is immediate from additivity, but the disjointness condition matters.

### Lemma 1.6: inclusion-exclusion for two sets

For any events `A` and `B`,

`P(A union B) = P(A) + P(B) - P(AB)`.

Proof structure:

- decompose `A union B` into three disjoint pieces:
  - `AB^c`
  - `AB`
  - `A^cB`
- add their probabilities
- regroup into `P(A)` and `P(B)`
- subtract `P(AB)` once because the overlap is counted twice

This is the first real correction formula in the chapter. It teaches that naive addition fails whenever overlap is present.

## Theorem 1.8 in detail: continuity of probabilities

This theorem deserves more attention than the book gives it in prose.

### Increasing case

Suppose

`A_1 subset A_2 subset ...`

and define

`A = union_i A_i`.

The proof creates disjoint increments:

- `B_1 = A_1`
- `B_2 = A_2 - A_1`
- `B_3 = A_3 - A_2`
- and so on

Then:

- the `B_i` are disjoint
- `A_n = union_{i=1}^n B_i`
- `A = union_{i=1}^\infty B_i`

So additivity gives

`P(A_n) = sum_{i=1}^n P(B_i)`

and taking limits gives

`lim_n P(A_n) = sum_{i=1}^\infty P(B_i) = P(A)`.

The main insight is that monotone growth can be rewritten as accumulation of disjoint increments.

### Decreasing case

If

`A_1 superset A_2 superset ...`

and `A = intersection_i A_i`, then apply the increasing case to complements:

- `A_1^c subset A_2^c subset ...`
- `union_i A_i^c = A^c`

Hence

`P(A_i^c) -> P(A^c)`

and therefore

`P(A_i) = 1 - P(A_i^c) -> 1 - P(A^c) = P(A)`.

This is the cleanest way to see why continuity from above is not an extra theorem once complements are available.

### Why this theorem matters

This theorem is the first bridge from finite set algebra to limiting arguments. Without it, probability would not interact correctly with increasing approximations, tail events, stopping events, and later asymptotic reasoning.

## Finite sample spaces and counting

The chapter then specializes to finite `Omega`.

If all outcomes are equally likely, then

`P(A) = |A| / |Omega|`.

This is the uniform distribution on a finite sample space.

The chapter then introduces:

- `n!`
- `n choose k = n! / (k! (n-k)!)`

This section is not just combinatorics for its own sake. It identifies a general workflow:

1. construct the sample space correctly
2. identify whether the probability measure is uniform
3. count the event size
4. divide by total sample-space size

Many beginner errors in probability are not algebra mistakes but sample-space construction mistakes.

## Independence

The chapter distinguishes two ways independence appears:

- assumed independence, such as separate fair coin tosses
- derived independence, where one verifies `P(AB) = P(A)P(B)`

That distinction is important. Independence is not a visual property of the sets alone and not a vague statement of "no connection." It is a precise multiplicative factorization of joint probability.

### Disjointness is usually the opposite of independence

If `A` and `B` are disjoint and both have positive probability, then

- `P(AB) = 0`
- but `P(A)P(B) > 0`

so they cannot be independent.

This is one of the most important conceptual corrections in elementary probability. "Mutually exclusive" and "independent" are structurally different:

- disjointness says the events cannot happen together
- independence says learning one event occurred does not change the probability of the other

### Independence as invariance under conditioning

Lemma 1.14 later shows:

if `A` and `B` are independent, then `P(A | B) = P(A)`.

So independence is equivalently the statement that conditioning on `B` does not update the probability of `A`.

That is the operational interpretation that later becomes crucial in graphical models, factorization, and causal thinking.

## Conditional probability

The definition

`P(A | B) = P(AB) / P(B)`

contains several ideas at once:

- first restrict attention to the event `B`
- then renormalize so total mass on `B` becomes one
- then ask what fraction of that renormalized mass lies in `A`

The chapter emphasizes a very important logical rule:

- for fixed `B`, `P(. | B)` is a probability measure in the left argument
- in general, `P(A | B union C)` is not equal to `P(A | B) + P(A | C)`

So the usual probability rules apply to what is left of the bar, not to the conditioning event.

### Product rule

From the definition,

`P(AB) = P(A | B) P(B) = P(B | A) P(A)`.

This identity is one of the real computational engines of the chapter. It allows sequential decomposition of joint events.

### Prosecutor's fallacy

The medical-test example is structurally more important than it first appears. It teaches:

- `P(+ | D)` can be large while `P(D | +)` is small
- the base rate `P(D)` matters through the denominator
- intuitive reversal of conditionals is often disastrously wrong

This is not merely a public misunderstanding. In research, it reappears as:

- confusion between hit rate and posterior class probability
- confusion between likelihood and posterior
- confusion between correlation-like evidence and conditional decision relevance

## Law of total probability and Bayes theorem

### Theorem 1.16: law of total probability

If `A_1, ..., A_k` partition the sample space, then

`P(B) = sum_i P(B | A_i) P(A_i)`.

Proof idea:

- define `C_i = BA_i`
- the `C_i` are disjoint
- `B = union_i C_i`
- add the probabilities and rewrite each `P(BA_i)` as `P(B | A_i) P(A_i)`

This theorem is the correct way to aggregate across latent regimes, classes, or states.

### Theorem 1.17: Bayes theorem

Bayes theorem follows immediately by combining:

1. `P(A_i | B) = P(A_i B) / P(B)`
2. `P(A_i B) = P(B | A_i) P(A_i)`
3. the law of total probability for `P(B)`

The structure is:

- numerator = likelihood times prior
- denominator = evidence, obtained by averaging likelihood over the partition

The chapter's language of prior and posterior is minimal, but the mathematical content is already complete.

### Why Bayes is powerful

Bayes theorem converts forward modeling into inverse inference:

- forward direction: if state `A_i` were true, how likely would evidence `B` be?
- inverse direction: after seeing `B`, how plausible is state `A_i`?

That inversion is fundamental to:

- signal filtering
- classification
- spam detection
- default prediction
- latent-state modeling
- many forms of online learning

## Appendix: sigma-fields and measurable spaces

The appendix repairs the informal simplification made at the start of the chapter.

For large sample spaces, one generally cannot assign probabilities to every subset. Instead one works with a sigma-field `A` satisfying:

1. `Omega in A`
2. closed under countable unions
3. closed under complements

Then:

- `(Omega, A)` is a measurable space
- `(Omega, A, P)` is a probability space

This matters because the elementary event language is only fully correct after one specifies the measurable event class. The chapter does not develop measure theory, but it honestly signals where the simplification lies.

## Exercises that carry the real lessons

Several exercises are not routine practice. They reveal the conceptual load-bearing beams of the chapter.

- Exercise 1: complete the proof of continuity and handle the decreasing case
- Exercise 6: prove there is no uniform distribution on the countably infinite set `{0,1,2,...}`
- Exercise 7: derive the union bound by disjointification
- Exercise 9: prove `P(. | B)` satisfies the probability axioms
- Exercise 10: Monty Hall, which forces careful specification of the sample space and conditioning
- Exercise 12: the three-card problem, another base-rate and conditioning trap
- Exercise 14: show `A` is independent of itself only when `P(A)` is `0` or `1`
- Exercise 18: if one posterior probability in a partition decreases after observing `B`, some other posterior must increase

These are not side exercises. They are conceptual stress tests for whether the chapter has actually been understood.

## Common failure modes

- treating the sample space as obvious instead of constructing it explicitly
- adding probabilities without checking disjointness
- confusing disjointness with independence
- reversing `P(A | B)` and `P(B | A)`
- ignoring base rates in posterior reasoning
- using Bayes theorem as a slogan without specifying the partition
- assuming one can define a uniform distribution on any infinite set
- overlooking the measurable-space issue and acting as though every subset is automatically an admissible event

## Quant research relevance

This chapter is basic in the correct sense: later quant work breaks if this layer is fuzzy.

### Event-level modeling

Many trading and risk questions are event questions before they are random-variable questions:

- default before maturity
- barrier hit before expiry
- stop-loss hit before take-profit
- limit order filled before cancellation
- drawdown exceeds threshold
- earnings surprise falls in a tail set

If the event algebra is sloppy, every later computation is compromised.

### Conditioning and regime decomposition

The law of total probability is the prototype for state-mixture reasoning:

- bull / neutral / bear regimes
- liquid / stressed microstructure states
- default / survival branches
- latent signal classes

Many practical quant models are just complicated versions of partitioning plus conditional probabilities.

### Base rates and class imbalance

Bayes theorem is where one learns not to confuse:

- high true-positive rate with high posterior event probability
- predictive likelihood with posterior probability of a state
- rare-event detection with reliable rare-event inference

This is directly relevant in fraud detection, default prediction, crash forecasting, and event-driven signals where base rates are small.

### Independence assumptions

Research code often multiplies probabilities, factorizes likelihoods, or treats observations as iid with very little scrutiny. This chapter gives the exact condition under which that step is legal. If independence is false, many textbook simplifications collapse.

## What should be promoted out of this source note

- a durable note on probability spaces and event algebra
- a durable note on independence versus disjointness
- a durable note on conditional probability and the product rule
- a durable note on Bayes theorem and base-rate reasoning
- later, a bridge note connecting partition-based probability to hidden-state and regime models

## Related notes

- [[All of Statistics]]
- [[All of Statistics - Ch 02 Random Variables]]
- [[Stats Map]]
- [[Math Map]]
- [[Probabilistic Machine Learning]]

## Sources

- [[All of Statistics]]
- [[raw/math_statistics/2004 - wasserman - all of statistics.pdf]]
