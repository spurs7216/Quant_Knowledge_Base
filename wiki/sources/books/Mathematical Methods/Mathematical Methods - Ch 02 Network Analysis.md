---
title: Mathematical Methods - Ch 02 Network Analysis
type: source
status: chapter_ingested
updated: 2026-04-20
tags:
  - source
  - mathematics
  - networks
  - graph-theory
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: chapter_markdown_conversion_plus_selected_definition_and_theorem_checks
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 02 Network Analysis
parent_source: "[[Mathematical Methods]]"
sources:
  - "[[Mathematical Methods]]"
  - "[[raw/math_statistics/Mathematical Methods.pdf]]"
---
# Mathematical Methods - Ch 02 Network Analysis

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: deeper extraction completed for normalized graph Laplacians, spectral diagnostics of graph structure, Markov processes on graphs, stationary distributions, and centrality constructions.

## Why this chapter is load-bearing

This is the first chapter in the book where the mathematics becomes a reusable modeling workflow rather than a background review. It turns network structure into linear algebra and stochastic dynamics, which makes it directly useful for graph clustering, diffusion-style propagation, ranking, and state-transition modeling.

## Core objects

- graph `G = (V, E)` and adjacency matrix `A`
- degree matrix `T`
- normalized Laplacian `L = I - T^{-1/2} A T^{-1/2}`
- spectrum `0 = lambda_0 <= ... <= lambda_{n-1}`
- Rayleigh quotient
- transition matrix `P`
- stationary distribution `pi`
- connected components, bipartiteness, and graph cuts
- centrality functions

## Structural map

- graphs and the normalized Laplacian
- what the Laplacian spectrum says about graph structure
- Markov processes and stationary laws on graphs
- centrality measures and ranking-style summaries

## Theorem and derivation spine

### 1. The normalized Laplacian measures local disagreement

Definitions 2.9 to 2.17 and Theorem 2.18 show that the normalized Laplacian induces a positive-semidefinite quadratic form. The Rayleigh quotient becomes the central diagnostic because it measures how much a function varies across edges after degree normalization.

### 2. The spectrum encodes connectivity and bipartite structure

Theorem 2.21 is the core structural result of the chapter. It links spectral quantities to graph geometry:

- the zero eigenvalue counts connected components
- small positive eigenvalues signal weak connectivity
- the top eigenvalue is bounded by `2`
- an eigenvalue near `2` is the bipartite warning sign

That is the durable bridge from eigen-analysis to graph interpretation.

### 3. Near-disconnected and near-bipartite structure shows up before exact degeneracy

Proposition 2.24 makes the key practical point: one does not need exact disconnection or exact bipartiteness for the spectrum to be informative. Small spectral quantities already bound weak links and approximate decompositions.

### 4. Random walks on graphs inherit their geometry from `P`

Section 2.3 defines Markov processes on graphs through transition matrices and then proves convergence under irreducibility and aperiodicity. Theorem 2.40 and the Perron-Frobenius argument establish long-run convergence. Theorem 2.43 gives the canonical stationary law for the simple random walk: probability proportional to vertex degree.

### 5. Centrality is a summary of flow, access, and influence

Section 2.4 moves from global structure to node-level diagnostics. The chapter treats centrality measures as functions derived from path structure, stationary visitation, or related linear systems rather than as arbitrary scores.

## Quant relevance

This chapter is directly relevant to:

- asset-relation and correlation networks
- issuer, supply-chain, or ownership graph summaries
- market-state graphs and transition analysis
- graph-based clustering and segmentation
- PageRank-style importance scores and diffusion diagnostics

The main transferable lesson is that graph structure becomes usable once it is translated into spectra, transition operators, and linear systems.

## Promotion candidates

- [[Graph Laplacians and Spectral Graph Methods]]
- graph centrality
- random walks on graphs

## Related notes

- [[Mathematical Methods]]
- [[Graph Laplacians and Spectral Graph Methods]]
- [[Markov Chains]]
- [[Continuous-Time Markov Chains]]
- [[GraphSAGE with Deep Reinforcement Learning for Financial Portfolio Optimization]]

## Sources

- [[Mathematical Methods]]
- [[raw/math_statistics/Mathematical Methods.pdf]]
