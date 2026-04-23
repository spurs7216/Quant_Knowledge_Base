---
title: All of Statistics - Ch 17 Directed Graphs and Conditional Independence
type: source
status: chapter_ingested
updated: 2026-04-19
tags:
  - source
  - statistics
  - graphical-models
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: full_source
extraction_basis: full_text
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 17 Directed Graphs and Conditional Independence
parent_source: "[[All of Statistics]]"
sources:
  - "[[All of Statistics]]"
  - "[[raw/math_statistics/2004 - wasserman - all of statistics.pdf]]"
---
# All of Statistics - Ch 17 Directed Graphs and Conditional Independence

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed against the raw source.
- Pass 2: deep rewrite completed on the graph semantics, d-separation logic, equivalence results, and intervention appendix.

## Deepening Targets

- Promote the conditional-independence and intervention machinery into durable graph and causality notes once the vault needs a formal graph-based research layer.

## Deepened Subparts

- Conditional independence properties, DAG factorization, local Markov structure, d-separation, collider logic, Markov equivalence, and the intervention appendix were rewritten at full note depth.

## Role of the chapter

This chapter gives a graph-based language for conditional-independence structure. The key move is that probabilistic structure can be compressed into a graph only when one is careful about what arrows mean and how paths are blocked or opened.

Its central contribution is not graph drawing for its own sake. It is the translation between:

- probabilistic factorization
- conditional-independence statements
- and graph structure

This is one of the book's bridges into modern machine learning and causal reasoning.

## Core mathematical objects

- conditional independence `X independent Y | Z`
- directed acyclic graph (DAG)
- factorization of the joint law
- local and global Markov properties
- d-separation
- Markov equivalence
- passive conditioning `P(Z | Y = y)`
- active conditioning / intervention `P(Z | Y := y)`

## Conditional independence as a primitive relation

### Definition 17.1 and Theorem 17.2

The chapter begins by listing properties of conditional independence. This matters because later graph semantics rest on those logical relations.

The reader should take away that conditional independence is stronger than zero partial correlation and more structural than a regression coefficient equaling zero.

Theorem 17.2 gives a semigraphoid-style algebra:

- symmetry
- stability under measurable maps
- weak union
- contraction
- and, with positivity, intersection

These are not merely formal curiosities. They are the rules that let one reason from local graph statements to larger independence claims.

## DAG factorization

### Definition 17.3

A DAG represents a factorization of the joint law into local conditional pieces.

If `G` has vertices `X_1, ..., X_k`, the distribution is Markov to `G` when

`f(v) = product_i f(x_i | pi_i)`,

where `pi_i` are the parents of `X_i`.

This is the key mathematical step:

- edges encode parent-child structure
- the joint density factorizes into conditionals given parents

So the graph is a compressed representation of the distribution's dependence architecture.

### Theorem 17.6: local Markov condition

Theorem 17.6 states that a distribution belongs to `M(G)` if and only if each variable is independent of its nondescendants outside its parents, conditional on its parents.

This theorem matters because it says the graph is not only a picture; it is an equivalence between:

- a global factorization statement
- and a family of local conditional-independence statements

That is why graphical models can scale. One does not need to list every independence relation by hand.

## Markov properties and d-separation

### Theorem 17.6 and Theorem 17.10

The chapter introduces d-separation as the graph-theoretic criterion for reading off conditional-independence implications.

This is one of the most important algorithms in the chapter because it turns graph structure into testable or interpretable independence claims.

The path logic can be stated operationally:

- a noncollider on a path blocks the path once conditioned on
- a collider blocks the path unless the collider or one of its descendants is conditioned on

That is why conditioning can either remove dependence or create it, depending on path type.

The collider examples are especially important:

- conditioning on a common effect can create dependence rather than remove it

This is one of the main conceptual shocks for people who learned only regression conditioning.

Theorem 17.10 adds an important caveat. The equivalence between d-separation and actual conditional independence requires faithfulness: the distribution should not contain accidental cancellations that create extra independences beyond those implied by the graph.

## Markov equivalence

### Theorem 17.13

Different DAGs can imply the same set of conditional-independence relations.

This means the graph is not always identifiable from observational independence structure alone.

The theorem states that two DAGs are Markov equivalent if and only if they have:

- the same skeleton
- the same unshielded colliders

That is one of the deepest lessons in the chapter. The observed law may not pin down a unique directed story. Even perfect knowledge of conditional independence may leave multiple admissible DAGs.

## Estimation and structure learning

The chapter is refreshingly honest here. If the graph is known, one can parameterize each local conditional density and estimate by likelihood. But if the graph is unknown, structure learning is both statistically and computationally hard.

The important points are:

- exhaustive search over DAGs is combinatorially explosive
- model selection criteria such as AIC can be used in principle
- reliable confidence sets for graph structure require enormous sample sizes
- prior structural information is often necessary to make the problem realistic

This matters because many applied uses of DAGs quietly skip the distinction between "drawing a plausible graph" and "estimating a graph from data."

## Conditioning versus intervention

The appendix contains one of the chapter's most important quantitative ideas. Observing `Y = y` and forcing `Y := y` are different operations.

For the graph `X -> Y -> Z` with `X -> Z`, passive conditioning gives

`P(Z = z | Y = y) = sum_x f(z | x, y) f(x | y)`,

while intervention gives

`P(Z = z | Y := y) = sum_x f(z | x, y) f(x)`.

The difference is the weighting measure:

- observation uses the conditional distribution of upstream causes given the observed event
- intervention breaks the incoming arrows into `Y` and uses the original distribution of upstream variables

This is the graph-theoretic counterpart of the counterfactual distinction in Chapter 16.

## What the chapter is really teaching

The chapter is teaching that probability structure can be represented sparsely when conditional independences exist.

That helps with:

- interpretation
- factorization
- computation
- and causal reasoning

But it also teaches the limits of what observational data can identify.

## Failure modes the chapter is trying to prevent

- equating graphical adjacency with causal certainty
- assuming conditioning always removes dependence
- forgetting collider bias
- ignoring the faithfulness caveat when translating graph separation into independence claims
- believing one can recover a unique DAG from independence facts alone
- confusing passive conditioning with intervention

## Quant research relevance

This chapter matters for quant research because graphical thinking helps with:

- causal factor stories
- feature-screening logic
- latent-variable structures
- dependence decomposition in large models

The collider lesson is especially relevant whenever signals are filtered or conditioned on a downstream selection event. The intervention appendix is also directly relevant for trading research because portfolio and execution decisions are interventions, not passive observations.

## What should be promoted out of this source note

- a durable note on conditional independence
- a durable note on DAG factorization
- a durable note on d-separation
- a durable note on collider bias and Markov equivalence
- a durable note on conditioning versus intervention

## Related notes

- [[All of Statistics]]
- [[All of Statistics - Ch 16 Causal Inference]]
- [[All of Statistics - Ch 18 Undirected Graphs]]
- [[Probabilistic Machine Learning]]
- [[Stats Map]]

## Sources

- [[All of Statistics]]
- [[raw/math_statistics/2004 - wasserman - all of statistics.pdf]]
