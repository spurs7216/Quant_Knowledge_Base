---
title: Probability Theory The Logic of Science - Ch 11 Discrete Prior Probabilities - The Entropy Principle
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - probability
  - bayesian
  - entropy
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: chapter scan and selected Shannon-theorem and MaxEnt pages via pymupdf
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 11 Discrete Prior Probabilities - The Entropy Principle
parent_source: "[[Probability Theory The Logic of Science]]"
sources:
  - "[[Probability Theory The Logic of Science]]"
  - "[[raw/math_statistics/Probability Theory The Logic of Science.pdf]]"
---
# Probability Theory The Logic of Science - Ch 11 Discrete Prior Probabilities - The Entropy Principle

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: deepened the entropy characterization, the MaxEnt variational form, and the logic of prior construction from moment constraints.

## Role of the chapter

This chapter adds a second major prior-construction principle after indifference. When the available information is not symmetry but expectation constraints, Jaynes argues that the honest prior is the one that maximizes entropy subject to those constraints.

## Core mathematical objects

- entropy
  $$H(p)=-\sum_i p_i \log p_i$$
- recursive consistency condition
  $$H_3(p_1,p_2,p_3)=H_2(p_1,q)+q\,H_2\paren{\frac{p_2}{q},\frac{p_3}{q}}, \qquad q=p_2+p_3$$
- constrained MaxEnt problem
  $$\max_{p_i} -\sum_i p_i \log p_i$$
  subject to
  $$\sum_i p_i = 1, \qquad \sum_i p_i f_k(i)=F_k$$
- exponential-family solution
  $$p_i = \frac{1}{Z(\lambda)}\exp\paren{-\sum_k \lambda_k f_k(i)}$$

## Theorem and derivation spine

The chapter first rejects naive spread measures such as maximum variance or minimum $\sum_i p_i^2$ because they can force negative probabilities, zero out possibilities not excluded by the information, or create wildly unjustified edge solutions.

The constructive theorem then comes from Shannon-style consistency requirements. If uncertainty is to be represented numerically, vary continuously with the probabilities, increase with the number of equiprobable possibilities, and satisfy a composition law like
$$H_3(p_1,p_2,p_3)=H_2(p_1,q)+q\,H_2\paren{\frac{p_2}{q},\frac{p_3}{q}},$$
then the admissible uncertainty measure is entropy up to a positive multiplicative constant:
$$H(p)=-K\sum_i p_i \log p_i.$$

Once that uncertainty measure is fixed, prior design becomes a constrained variational problem. Maximizing
$$-\sum_i p_i \log p_i - \lambda_0\paren{\sum_i p_i - 1} - \sum_k \lambda_k\paren{\sum_i p_i f_k(i)-F_k}$$
with respect to the probabilities gives the stationary condition
$$\log p_i = -1-\lambda_0-\sum_k \lambda_k f_k(i),$$
hence
$$p_i = \frac{1}{Z(\lambda)}\exp\paren{-\sum_k \lambda_k f_k(i)}.$$

The multipliers are chosen so that the expectation constraints hold. In partition-function form,
$$Z(\lambda)=\sum_i \exp\paren{-\sum_k \lambda_k f_k(i)}, \qquad
\frac{\partial \log Z}{\partial \lambda_k} = -F_k.$$

## Why this matters later

This chapter is the bridge from Bayesian updating to principled prior design. It is also the template for the much later matrix MaxEnt formulation, where sums become traces and probabilities become density matrices.

## Failure modes and misuse points

- treating entropy maximization as a physical law rather than an inference rule
- using MaxEnt after silently omitting relevant constraints
- replacing explicit information constraints with vague intuition about "flatness"
- confusing posterior updating with prior assignment

## Quant research relevance

MaxEnt matters whenever a quant problem is specified by partial moments, marginal constraints, or weak structural information rather than a fully trusted generative model. It is a natural bridge into risk-neutral distributions, portfolio tilts under moment constraints, and regularized prior design.

## What should be promoted out of this source note

- [[Maximum Entropy Principle]]

## Related notes

- [[Probability Theory The Logic of Science]]
- [[Maximum Entropy Principle]]
- [[Probability as Extended Logic]]

## Sources

- [[Probability Theory The Logic of Science]]
- [[raw/math_statistics/Probability Theory The Logic of Science.pdf]]
