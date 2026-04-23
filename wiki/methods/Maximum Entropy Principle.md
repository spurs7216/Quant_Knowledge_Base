---
title: Maximum Entropy Principle
type: method
status: seed
updated: 2026-04-22
tags:
  - method
  - probability
  - bayesian
  - entropy
domain: statistics
sources:
  - "[[Probability Theory The Logic of Science]]"
  - "[[Probability Theory The Logic of Science - Ch 11 Discrete Prior Probabilities - The Entropy Principle]]"
  - "[[Probability Theory The Logic of Science - Ch 30 Maximum Entropy - Matrix Formulation]]"
---
# Maximum Entropy Principle

## Summary

The maximum entropy principle chooses the least committal distribution consistent with the information actually supplied. It is a prior-construction method, not a replacement for Bayes' theorem.

## Core equations

For discrete probabilities `p_i`, maximize
$$H(p)=-\sum_i p_i \log p_i$$
subject to
$$\sum_i p_i=1, \qquad \sum_i p_i f_k(i)=F_k.$$

The solution is
$$p_i=\frac{1}{Z(\lambda)}\exp\paren{-\sum_k \lambda_k f_k(i)},$$
with
$$Z(\lambda)=\sum_i \exp\paren{-\sum_k \lambda_k f_k(i)}, \qquad
\frac{\partial \log Z}{\partial \lambda_k}=-F_k.$$

In matrix form, when the state of knowledge is a density matrix `\rho`,
$$S(\rho)=-\operatorname{Tr}(\rho \log \rho),$$
and under constraints `\operatorname{Tr}(\rho F_k)=\langle F_k\rangle`, the solution is
$$\rho=\frac{1}{Z(\lambda)}\exp\paren{-\sum_k \lambda_k F_k},$$
$$Z(\lambda)=\operatorname{Tr}\exp\paren{-\sum_k \lambda_k F_k}.$$

## Main logic

### 1. MaxEnt is about honest prior assignment

Use MaxEnt when the available information is partial, usually in the form of expectations, totals, or linear constraints.

### 2. Entropy is justified by consistency

Jaynes' point is not merely heuristic spread-outness. Entropy is singled out by Shannon-style composition and consistency requirements.

### 3. Updating still happens through Bayes

MaxEnt gives the prior or baseline distribution consistent with the constraint set. Once data arrive, ordinary Bayesian updating takes over.

## Typical use cases

- prior design from moment constraints
- recovering distributions from partial summary information
- building baseline ensembles or reference measures
- deriving exponential-family forms from linear constraints

## Failure modes

- using MaxEnt without stating the actual constraints
- treating entropy as a physical law in nonphysical settings
- smuggling subjective assumptions into the constraint set and then calling the result neutral
- confusing MaxEnt priors with posterior inference

## Quant relevance

MaxEnt is useful when the researcher knows only moments, marginals, exposures, or other partial structure. It is a disciplined way to stay agnostic beyond that information instead of inventing unjustified shape assumptions.

## Related notes

- [[Probability as Extended Logic]]
- [[Bayesian Model Comparison and Occam Factors]]
- [[Convex Optimization Methods]]

## Sources

- [[Probability Theory The Logic of Science]]
- [[Probability Theory The Logic of Science - Ch 11 Discrete Prior Probabilities - The Entropy Principle]]
- [[Probability Theory The Logic of Science - Ch 30 Maximum Entropy - Matrix Formulation]]
