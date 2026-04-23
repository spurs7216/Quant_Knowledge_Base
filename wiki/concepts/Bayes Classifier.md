---
title: Bayes Classifier
type: concept
status: seed
updated: 2026-04-19
tags:
  - concept
  - classification
  - bayes
  - statistics
domain: statistics
sources:
  - "[[All of Statistics]]"
  - "[[All of Statistics - Ch 22 Classification]]"
---
# Bayes Classifier

## Summary

The Bayes classifier is the decision rule that minimizes classification error under 0-1 loss. It is the theoretical benchmark for all practical classifiers: no measurable rule can achieve a lower true misclassification rate when the data-generating law is fixed.

## Core Rule

For binary classification with regression function

`r(x) = P(Y = 1 | X = x)`

the Bayes rule is:

- choose class `1` if `r(x) > 1/2`
- choose class `0` otherwise

More generally:

`h*(x) = argmax_k P(Y = k | X = x) = argmax_k pi_k f_k(x)`

where `pi_k` is the class prior and `f_k(x)` is the class-conditional density.

## Why It Matters

The Bayes classifier separates two problems:

1. what is the optimal target rule if the truth were known?
2. how do we approximate that rule from finite data?

This distinction keeps model evaluation honest. A practical classifier is not judged against perfection in sample, but against the unattainable Bayes benchmark.

## Main Routes to Approximation

- estimate `P(Y = k | X = x)` directly and take the posterior argmax
- estimate `f_k(x)` and `pi_k`, then plug into Bayes' rule
- restrict the rule to a hypothesis class and minimize empirical risk

LDA, QDA, logistic regression, naive Bayes, trees, and SVMs are all different compromises around this target.

## Cost-Sensitive Extension

Under asymmetric classification costs, the threshold is not `1/2`. The decision boundary shifts with the relative cost of false positives and false negatives.

That point matters far more in trading than in textbook balanced-label examples.

## Quant Research Relevance

This note matters when classification is used for:

- regime labeling
- event prediction
- distress or default prediction
- sign prediction for returns or order flow

The most important lesson is that classification quality should be evaluated relative to decision loss, not just raw accuracy.

## Failure Modes

- confusing training accuracy with true risk
- ignoring class imbalance and asymmetric costs
- treating posterior probabilities as calibrated when the model is misspecified
- using classification scores without checking whether the economic action threshold matches the statistical threshold

## Practical Rule

Start from the Bayes rule conceptually, then ask how much structure, approximation, or regularization is needed to estimate a usable surrogate without lying to yourself about generalization.

## Related Notes

- [[Statistical Decision Theory]]
- [[Maximum Likelihood Estimation]]
- [[Financial Machine Learning Workflow]]
- [[All of Statistics]]

## Sources

- [[All of Statistics]]
- [[All of Statistics - Ch 22 Classification]]
