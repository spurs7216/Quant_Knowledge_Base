---
title: Probability Theory The Logic of Science - Ch 24 Model Comparison
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - bayesian
  - model-comparison
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: chapter scan and selected evidence-and-occam-factor pages via pymupdf
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 24 Model Comparison
parent_source: "[[Probability Theory The Logic of Science]]"
sources:
  - "[[Probability Theory The Logic of Science]]"
  - "[[raw/math_statistics/Probability Theory The Logic of Science.pdf]]"
---
# Probability Theory The Logic of Science - Ch 24 Model Comparison

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: deepened the evidence integral, posterior odds ratio, Laplace approximation, and Jaynes' Occam-factor interpretation.

## Role of the chapter

This chapter is the book's clearest answer to how hypotheses or models should be compared. The crucial quantity is not a p-value and not raw maximized likelihood. It is the integrated model evidence.

## Core mathematical objects

- posterior within a model
  $$p(\theta \mid D,M,I)=\frac{p(\theta \mid M,I)\,p(D \mid \theta,M,I)}{p(D \mid M,I)}$$
- model evidence
  $$p(D \mid M,I)=\int p(D \mid \theta,M,I)\,p(\theta \mid M,I)\,\diff \theta$$
- posterior odds
  $$\frac{p(M_j \mid D,I)}{p(M_k \mid D,I)}
  = \frac{p(M_j \mid I)}{p(M_k \mid I)}
  \frac{p(D \mid M_j,I)}{p(D \mid M_k,I)}$$

## Theorem and derivation spine

The governing update for model choice is posterior odds:
$$\frac{p(M_j \mid D,I)}{p(M_k \mid D,I)}
= \frac{p(M_j \mid I)}{p(M_k \mid I)}
\frac{p(D \mid M_j,I)}{p(D \mid M_k,I)}.$$

Inside each model, the evidence is the prior average of the likelihood:
$$p(D \mid M,I)=\int p(D \mid \theta,M,I)\,p(\theta \mid M,I)\,\diff \theta.$$

If the likelihood is sharply peaked near `\hat\theta`, Jaynes uses a Gaussian approximation to show
$$p(D \mid M,I)\approx L_{\max}(2\pi)^{m/2}\det(\Sigma)^{1/2}\,p(\hat\theta \mid M,I).$$

He then interprets
$$W \approx (2\pi)^{m/2}\det(\Sigma)^{1/2}p(\hat\theta \mid M,I)$$
as the prior probability mass concentrated in the high-likelihood region. The model-comparison rule becomes
$$\frac{p(M_j \mid D,I)}{p(M_k \mid D,I)}
\approx
\frac{p(M_j \mid I)}{p(M_k \mid I)}
\frac{(L_j)_{\max}}{(L_k)_{\max}}
\frac{W_j}{W_k}.$$

That final factor is Jaynes' Occam factor. A flexible model spreads prior mass over a larger parameter manifold, so unless the data move the likelihood peak far enough, the extra flexibility is penalized automatically.

## Why this matters later

This is a durable foundation for Bayesian evidence, marginal likelihoods, and the logic behind principled complexity penalties. It also clarifies why "simplicity" is not primitive. Plausibility is.

## Failure modes and misuse points

- comparing models by maximized likelihood alone
- interpreting Occam's razor as pure parameter counting
- using unnormalized or arbitrary parameter priors and then trusting Bayes factors
- forgetting that evidence depends on the predictive mass a model assigns to the observed data

## Quant research relevance

The chapter matters for factor-model selection, state-space specification choice, regime-model comparison, and any workflow where complexity control should emerge from predictive plausibility rather than ad hoc penalty tuning.

## What should be promoted out of this source note

- [[Bayesian Model Comparison and Occam Factors]]

## Related notes

- [[Probability Theory The Logic of Science]]
- [[Bayesian Model Comparison and Occam Factors]]
- [[Maximum Likelihood Estimation]]

## Sources

- [[Probability Theory The Logic of Science]]
- [[raw/math_statistics/Probability Theory The Logic of Science.pdf]]
