---
title: Probability Theory The Logic of Science - Ch 18 The Ap Distribution and Rule of Succession
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - probability
  - bayesian
  - predictive
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: chapter-start and selected rule-of-succession pages via pymupdf
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 18 The Ap Distribution and Rule of Succession
parent_source: "[[Probability Theory The Logic of Science]]"
sources:
  - "[[Probability Theory The Logic of Science]]"
  - "[[raw/math_statistics/Probability Theory The Logic of Science.pdf]]"
---
# Probability Theory The Logic of Science - Ch 18 The Ap Distribution and Rule of Succession

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: deepened the predictive-count logic, the rule of succession, and the memory-compression role of conjugate updating.

## Role of the chapter

This chapter shows how repeated evidence can be summarized without keeping the full data tape forever. The mechanism is exchangeability plus a prior over the underlying success probability, leading to predictive distributions that update through counts.

## Core mathematical objects

- success probability `\theta`
- counts `r` successes and `s` failures
- beta posterior
  $$p(\theta \mid D,I) \propto \theta^r (1-\theta)^s$$
- predictive probability
  $$p(x_{n+1}=1 \mid D,I)=\int \theta\,p(\theta \mid D,I)\,\diff \theta$$

## Theorem and derivation spine

With a Bernoulli sampling model and a uniform prior on `\theta`, the posterior after `r` successes and `s` failures is
$$p(\theta \mid D,I)=\frac{\Gamma(r+s+2)}{\Gamma(r+1)\Gamma(s+1)}\,\theta^r(1-\theta)^s.$$

Integrating over that posterior gives Laplace's rule of succession:
$$p(x_{n+1}=1 \mid D,I)=\frac{r+1}{r+s+2}.$$

The same logic generalizes. With a beta prior `\theta \sim \operatorname{Beta}(a,b)`, the predictive probability is
$$p(x_{n+1}=1 \mid D,I)=\frac{r+a}{r+s+a+b}.$$

For multinomial counts, the beta law generalizes to a Dirichlet family, and the predictive update becomes "add pseudocounts then normalize." This is the real memory-compression mechanism of the chapter: the future prediction can depend on a sufficient count summary instead of the entire exchangeable sequence.

## Why this matters later

This chapter is the book's first clean predictive-Bayes chapter. It turns past counts into posterior predictive probabilities and makes the logic of pseudocounts explicit rather than heuristic.

## Failure modes and misuse points

- treating the rule of succession as universally valid outside its exchangeable setup
- forgetting that the prior contributes effective counts
- using predictive formulas without checking whether exchangeability is reasonable

## Quant research relevance

The chapter matters for default rates, event arrivals, hit-rate estimation, and any quant setting where sparse binary evidence must be turned into predictive probabilities without overfitting to small samples.

## What should be promoted out of this source note

- a durable note on rule of succession and predictive updating

## Related notes

- [[Probability Theory The Logic of Science]]
- [[Probability as Extended Logic]]
- [[Maximum Entropy Principle]]

## Sources

- [[Probability Theory The Logic of Science]]
- [[raw/math_statistics/Probability Theory The Logic of Science.pdf]]
