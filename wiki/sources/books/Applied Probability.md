---
title: Applied Probability
type: source
status: chapter_ingested
updated: 2026-04-20
tags:
  - source
  - probability
  - stochastic-processes
  - textbook
  - applied-probability
source_type: book
source_class: overview_source
read_scope: full_source
extraction_basis: preface_plus_full_chapter_scan_plus_selected_chapter_text
technical_depth: mixed
ingest_stage: promotion_started
source_count: 1
sources:
  - "[[raw/math_statistics/Applied Probability.pdf]]"
---
# Applied Probability

## Citation / metadata

- Author: Kenneth Lange
- Title: *Applied Probability*
- Edition: second edition
- Publisher: Springer, *Springer Texts in Statistics*
- Year: 2010
- Role in vault: the first serious applied-probability bridge from broad statistical foundations into reusable stochastic-process machinery

## Why this book matters

This book matters because it does not treat probability as a static list of distributions. It turns probability into a modeling language for:

- event arrivals
- state transitions
- extinction and growth
- stopping and concentration
- continuous-path dynamics
- approximation and computation

For this vault, that is the right bridge between `[[All of Statistics]]` and the later continuous-time, filtering, and finance shelves. The preface also makes the design choice explicit: theory and applications should stay together, and computational probability should be part of the toolkit rather than an afterthought.

## Reading logic from the source

The book has a clear internal dependency structure:

- Chapters 1 to 5 build the foundational toolkit: probability spaces, expectations, transforms, convexity, and counting arguments.
- Chapters 6 to 11 are the real stochastic-process spine: Poisson processes, discrete and continuous Markov chains, branching, martingales, and diffusions.
- Chapters 12 to 14 broaden that spine into asymptotic approximation, numerical probability, and Chen-Stein Poisson approximation.
- Chapter 15 is a specialized epilogue in probabilistic number theory rather than a main dependency for later quant work.

That same structure is the right ingest logic. The full shelf should be preserved, but the deep treatment belongs mainly to the chapters that supply reusable stochastic-process objects for later books.

## Stage map

Current ingest stages after the fresh reingest:

- `scan`: Chapters 1, 4, 5, 15
- `deep`: Chapters 6, 7, 8, 10, 11
- `selective_deepen`: Chapters 2, 3, 9, 12, 13, 14

Selection logic:

- Chapters 6 to 11 are the process spine and deserve theorem-level or derivation-level treatment.
- Chapters 2 and 3 were selectively deepened because expectation tricks, convexity, Jensen, and MM-style reasoning recur across later work.
- Chapters 9, 12, 13, and 14 were selectively deepened because they contain reusable extinction criteria, asymptotic tools, numerical methods, and Chen-Stein logic without all needing full theorem-by-theorem extraction.

## Chapter shelf

- [[Applied Probability - Ch 01 Basic Notions of Probability Theory]]
- [[Applied Probability - Ch 02 Calculation of Expectations]]
- [[Applied Probability - Ch 03 Convexity Optimization and Inequalities]]
- [[Applied Probability - Ch 04 Combinatorics]]
- [[Applied Probability - Ch 05 Combinatorial Optimization]]
- [[Applied Probability - Ch 06 Poisson Processes]]
- [[Applied Probability - Ch 07 Discrete-Time Markov Chains]]
- [[Applied Probability - Ch 08 Continuous-Time Markov Chains]]
- [[Applied Probability - Ch 09 Branching Processes]]
- [[Applied Probability - Ch 10 Martingales]]
- [[Applied Probability - Ch 11 Diffusion Processes]]
- [[Applied Probability - Ch 12 Asymptotic Methods]]
- [[Applied Probability - Ch 13 Numerical Methods]]
- [[Applied Probability - Ch 14 Poisson Approximation]]
- [[Applied Probability - Ch 15 Number Theory]]

## Core objects and modeling vocabulary

- probability space, conditional probability, independence, and transforms as the calculation language for random objects
- convex functions, Jensen-style inequalities, and MM surrogates as the bridge between probability and optimization
- counting processes, intensity functions, waiting times, and marked points in the Poisson-process layer
- transition matrices `P`, generators `Lambda`, equilibrium laws `pi`, and detailed balance in the Markov-chain layer
- progeny generating functions, extinction probabilities, and basic reproduction numbers in the branching-process layer
- filtrations, stopping times, and bounded-difference concentration in the martingale layer
- infinitesimal drift `mu(t, x)` and variance `sigma^2(t, x)` in the diffusion layer
- asymptotic expansions, Laplace methods, Fourier methods, and Chen-Stein error bounds in the approximation layer

## Main themes

### 1. Probability becomes process theory

The middle of the book is not about isolated random variables but about dynamic objects indexed by time: arrivals, transitions, stopping events, and continuous paths.

### 2. Reversibility and transform methods recur everywhere

Detailed balance, generating functions, Fourier transforms, and moment transforms keep reappearing because they compress stochastic structure into solvable algebra.

### 3. Approximation and computation are part of probability

The second edition explicitly adds asymptotic and numerical chapters. That is important for the vault because exact closed forms are rarely the endpoint in quant work.

### 4. Continuous-time ideas begin here, but they do not end here

This book reaches continuous-time Markov chains and diffusions, but it is still an applied-probability bridge rather than the final word on stochastic calculus or arbitrage pricing.

## Promoted durable notes

- [[Poisson Processes]]
- [[Continuous-Time Markov Chains]]
- [[Martingales]]
- [[Diffusion Processes]]
- [[Markov Chains]]

## Next promotion targets

- expectation and transform methods
- convexity, Jensen, and MM-style surrogate optimization
- branching processes and extinction criteria
- Poisson approximation and Chen-Stein bounds
- numerical methods for Markov and diffusion models

## Caveats

- The book is mathematical and modeling-oriented, not finance-specific.
- The strongest chapters often prefer proof skeletons and worked examples over full measure-theoretic formality.
- The appendix contains mathematical review material, but it was not promoted into a separate shelf note because the vault already has stronger direct sources for most of that background.
- Chapter 15 is worth knowing exists, but it is not central to the current quant-research spine.

## Related notes

- [[All of Statistics]]
- [[Math Map]]
- [[Stats Map]]
- [[Markov Chains]]
- [[Poisson Processes]]
- [[Continuous-Time Markov Chains]]
- [[Martingales]]
- [[Diffusion Processes]]
- [[Stochastic Calculus]]
- [[Stochastic Calculus for Finance II]]

## Sources

- [[raw/math_statistics/Applied Probability.pdf]]
