---
title: Bayesian Model Comparison and Occam Factors
type: method
status: seed
updated: 2026-04-22
tags:
  - method
  - bayesian
  - model-comparison
  - statistics
domain: statistics
sources:
  - "[[Probability Theory The Logic of Science]]"
  - "[[Probability Theory The Logic of Science - Ch 24 Model Comparison]]"
---
# Bayesian Model Comparison and Occam Factors

## Summary

Bayesian model comparison ranks models by posterior odds. The decisive quantity is model evidence, the prior-weighted average likelihood, not the likelihood at one favorite parameter value.

## Core equations

Within one model,
$$p(\theta \mid D,M,I)=\frac{p(\theta \mid M,I)\,p(D \mid \theta,M,I)}{p(D \mid M,I)}.$$

The evidence is
$$p(D \mid M,I)=\int p(D \mid \theta,M,I)\,p(\theta \mid M,I)\,\diff \theta.$$

Posterior odds between two models are
$$\frac{p(M_j \mid D,I)}{p(M_k \mid D,I)}
=
\frac{p(M_j \mid I)}{p(M_k \mid I)}
\frac{p(D \mid M_j,I)}{p(D \mid M_k,I)}.$$

When the likelihood is sharply peaked,
$$p(D \mid M,I)\approx L_{\max}(2\pi)^{m/2}\det(\Sigma)^{1/2}\,p(\hat\theta \mid M,I).$$

This decomposes the evidence into:

- goodness of fit through `L_{\max}`
- an Occam factor through the prior mass concentrated near the high-likelihood region

## Main logic

### 1. Complex models are penalized automatically

A flexible model spreads prior probability over a larger parameter region. If the data only support one narrow corner of that region, the evidence reflects that dilution.

### 2. Simplicity is not primitive

Jaynes' point is that "simpler" often just means "more plausible given prior structure." Parameter counting is only a weak shadow of the real logic.

### 3. Evidence is predictive

The evidence asks how much prior-weighted predictive mass a model gave to the observed data, not how well one tuned version of the model can fit them after the fact.

## Failure modes

- comparing models by maximized likelihood alone
- using arbitrary priors and then over-interpreting Bayes factors
- confusing evidence with posterior parameter uncertainty inside one model
- treating a complexity penalty as universal when it depends on the prior geometry

## Quant relevance

This method matters for selecting factor structures, volatility models, state-space variants, regime-switching specifications, and any model family where over-flexibility can fit noise unless it is penalized through predictive plausibility.

## Related notes

- [[Probability as Extended Logic]]
- [[Maximum Entropy Principle]]
- [[Maximum Likelihood Estimation]]
- [[Statistical Decision Theory]]

## Sources

- [[Probability Theory The Logic of Science]]
- [[Probability Theory The Logic of Science - Ch 24 Model Comparison]]
