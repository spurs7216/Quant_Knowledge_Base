---
title: Applied Probability
type: source
status: chapter_ingested
updated: 2026-04-18
tags:
  - source
  - probability
  - stochastic-processes
  - textbook
sources:
  - "[[raw/math_statistics/Applied Probability.pdf]]"
---
# Applied Probability

## Summary

This book is a broad applied-probability text that moves from probability foundations and expectations into convexity, combinatorics, Poisson processes, Markov chains, branching processes, martingales, diffusion processes, asymptotics, numerical methods, and approximation tools. It sits close to the mathematical machinery that underlies stochastic modeling in finance.

## Chapter-by-Chapter Ingest

- `Chapter 1. Basic Notions of Probability Theory`: sets up probability spaces, events, and random variables.
- `Chapter 2. Calculation of Expectations`: develops expectation as the main summary operator for random outcomes.
- `Chapter 3. Convexity, Optimization, and Inequalities`: links probabilistic reasoning with convex tools and inequality methods.
- `Chapter 4. Combinatorics`: studies counting arguments that support discrete probability.
- `Chapter 5. Combinatorial Optimization`: connects combinatorial structure with optimization problems under uncertainty.
- `Chapter 6. Poisson Processes`: introduces one of the core counting-process models for event arrivals.
- `Chapter 7. Discrete-Time Markov Chains`: develops state-transition dynamics in discrete time.
- `Chapter 8. Continuous-Time Markov Chains`: extends Markov dynamics into continuous time and intensity-driven settings.
- `Chapter 9. Branching Processes`: studies recursively evolving random systems and extinction/growth behavior.
- `Chapter 10. Martingales`: builds the fair-game framework that later supports modern asset-pricing arguments.
- `Chapter 11. Diffusion Processes`: moves from jump/count processes into continuous-path stochastic dynamics.
- `Chapter 12. Asymptotic Methods`: develops limiting approximations and large-sample reasoning.
- `Chapter 13. Numerical Methods`: addresses computational routes when closed forms are unavailable.
- `Chapter 14. Poisson Approximation`: treats approximation theory for rare-event settings.
- `Chapter 15. Number Theory`: closes with a more specialized probabilistic-number-theory excursion.

## Key Claims

- Applied probability is the bridge between abstract probability and operational stochastic models.
- Martingales, Markov structures, and diffusions are the real backbone for continuous-time finance.
- Approximation and numerical methods matter because exact distributions are rarely the endpoint in practice.

## Methods and Data

- expectation and inequality tools
- combinatorics and combinatorial optimization
- Poisson and Markov processes
- martingales and diffusions
- asymptotic and numerical approximations

## Why It Matters Here

This note strengthens the math shelf beneath option pricing, risk modeling, and state-space work. It is particularly relevant for any future vault notes on stopping times, diffusions, market microstructure event models, and credit/default processes.

## Reflection

The book's strongest contribution to this vault is not any single chapter but the way it places discrete and continuous stochastic models inside one applied-probability frame. That is exactly the mental model quants need when moving between market arrivals, state dynamics, and Monte Carlo.

## Caveats

- The book is mathematical rather than finance-specific.
- The final chapter on number theory is intellectually interesting but less central to the current vault mission than the stochastic-process material.

## Related Notes

- [[Arbitrage Theory in Continuous Time]]
- [[Monte Carlo Methods]]
- [[Math Map]]

## Sources

- [[raw/math_statistics/Applied Probability.pdf]]
