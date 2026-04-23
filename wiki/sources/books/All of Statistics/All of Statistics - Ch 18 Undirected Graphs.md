---
title: All of Statistics - Ch 18 Undirected Graphs
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
technical_depth: moderate
ingest_stage: scan
chapter_or_section: Ch 18 Undirected Graphs
parent_source: "[[All of Statistics]]"
sources:
  - "[[All of Statistics]]"
  - "[[raw/math_statistics/2004 - wasserman - all of statistics.pdf]]"
---
# All of Statistics - Ch 18 Undirected Graphs

## Ingest Scope and Depth

- Ingest stage: `scan`
- Pass 1: full chapter scan completed against the raw source.
- Pass 2: rescan completed to identify the graph-theoretic pieces that are worth later deepening.

## Deepening Targets

- Deepen the separation theorem and the equivalence `M_pair(G) = M_global(G)` if the vault starts relying on Markov-network style dependence arguments.
- Deepen clique-potential factorization if probabilistic graphical models become a live modeling tool rather than background structure.
- Deepen the contrast with DAGs if later notes need a precise "symmetric dependence versus directed causality" distinction.

## Deepened Subparts

- No subpart has been rewritten at full deep-note depth yet.

## Worth Attending From The Rescan

- Theorem 18.1 is the chapter's main operational rule: separation in an undirected graph implies conditional independence. This is the undirected analogue of d-separation, but the logic is simpler because there are no colliders.
- Theorem 18.3 is more important than it first appears. The equivalence of pairwise and global Markov properties means one can build the graph from local missing-edge statements and then safely read richer separation statements from it.
- The clique-potential representation in equation (18.1) is the chapter's computational core. It says the joint law factorizes over maximal cliques rather than over directed parent sets.
- The chapter is quietly preparing the reader for sparse dependence modeling. The graph is not just a picture of who interacts with whom; it is a structured factorization device.

## Role of the chapter

This chapter develops the undirected analogue of the DAG framework. Instead of asymmetric parent-child structure, it models symmetric neighborhood dependence.

The main ideas are:

- pairwise and global Markov properties
- factorization through cliques and potentials

## Core mathematical objects

- undirected graph
- pairwise Markov property
- global Markov property
- clique
- potential function

## Pairwise and global Markov structure

### Theorems 18.1 and 18.3

The chapter links graph separation in undirected graphs to conditional-independence structure, showing that pairwise and global Markov views coincide under the relevant assumptions.

This is a structural analogue of the DAG chapter, but for symmetric dependence.

## Cliques and potentials

The clique-and-potential representation is the heart of the chapter. It says the joint law can be built from local functions on maximal cliques rather than from one huge unconstrained object.

This is the main computational payoff of the graphical viewpoint.

## What the chapter is really teaching

Undirected graphical models are useful when dependence is relational and symmetric rather than naturally directional.

They are less directly causal than DAGs, but often better suited to structured dependence representation.

## Failure modes the chapter is trying to prevent

- assuming all graphical structure should be directed
- forgetting that factorization may live at the clique level rather than at the variable level
- confusing symmetric dependence modeling with causal direction

## Quant research relevance

This chapter is less central than regression or causality for most quant work, but still useful conceptually for:

- structured dependence models
- local interaction systems
- sparse precision or neighborhood ideas

It is also valuable as a conceptual precursor to more modern graphical and sparse dependence methods.

## What should be promoted out of this source note

- a durable note on undirected graphical models
- a durable note on clique factorization

## Related notes

- [[All of Statistics]]
- [[All of Statistics - Ch 17 Directed Graphs and Conditional Independence]]
- [[Probabilistic Machine Learning]]

## Sources

- [[All of Statistics]]
- [[raw/math_statistics/2004 - wasserman - all of statistics.pdf]]
