---
title: Probability as Extended Logic
type: concept
status: seed
updated: 2026-04-22
tags:
  - concept
  - probability
  - bayesian
  - logic
domain: statistics
sources:
  - "[[Probability Theory The Logic of Science]]"
  - "[[Probability Theory The Logic of Science - Ch 01 Plausible Reasoning]]"
  - "[[Probability Theory The Logic of Science - Ch 02 The Quantitative Rules]]"
---
# Probability as Extended Logic

## Summary

Probability, in the Jaynes-Cox view, is not primarily a frequency calculus. It is the extension of logic to situations of incomplete information. Deductive logic handles certainty; probability handles graded plausibility while preserving consistency.

## Core objects

- proposition `A`
- background information `I`
- plausibility assignment `p(A \mid I)`
- conjunction `AB`
- negation `\neg A`

## Load-bearing rules

The consistency rules are the ordinary probability rules:

$$p(AB \mid C)=p(A \mid BC)\,p(B \mid C),$$
$$p(A \mid B)+p(\neg A \mid B)=1,$$
$$p(A+B \mid C)=p(A \mid C)+p(B \mid C)-p(AB \mid C).$$

Bayes' theorem is just a rearrangement of the product rule:
$$p(H \mid D,I)=\frac{p(H \mid I)\,p(D \mid H,I)}{p(D \mid I)}.$$

## Main logic

### 1. Probability is conditional logic

Every probability statement is conditional on information. There is no context-free probability attached to a proposition.

### 2. Bayesian updating is not a separate trick

If probability is logic under uncertainty, Bayes' theorem is simply the rule for revising plausibility when new information arrives.

### 3. Subjectivity is not arbitrariness

Probabilities can depend on information without being arbitrary. Different information states can imply different probabilities, but the update rules relating them are still objective consistency rules.

## Why this note matters

This concept is the foundation for the whole Bayesian branch of the vault:

- prior design becomes part of logic, not an embarrassment
- posterior inference becomes coherent updating, not a special method
- model comparison and decision theory become downstream layers of one calculus

## Failure modes

- treating probability as meaningful only in long-run repeatable experiments
- dropping the conditioning information and then calling the result objective
- confusing different information states with inconsistent reasoning

## Quant relevance

Quant research almost never operates under certainty. Signals, models, structural breaks, and data quality are all uncertain. This note justifies using posterior beliefs and evidence updates as the research system's native logic.

## Related notes

- [[Maximum Entropy Principle]]
- [[Statistical Decision Theory]]
- [[Bayesian Model Comparison and Occam Factors]]
- [[Convergence and Limit Theory]]

## Sources

- [[Probability Theory The Logic of Science]]
- [[Probability Theory The Logic of Science - Ch 01 Plausible Reasoning]]
- [[Probability Theory The Logic of Science - Ch 02 The Quantitative Rules]]
