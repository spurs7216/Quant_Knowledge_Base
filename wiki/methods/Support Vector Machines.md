---
title: Support Vector Machines
type: method
status: seed
updated: 2026-04-20
tags:
  - method
  - machine-learning
  - classification
  - support-vector-machines
domain: machine-learning
sources:
  - "[[Mathematical Methods]]"
  - "[[Mathematical Methods - Ch 03 Machine Learning]]"
  - "[[Bishop Pattern Recognition and Machine Learning]]"
  - "[[An Introduction to Statistical Learning]]"
---
# Support Vector Machines

## Summary

Support vector machines classify data by finding a separating hyperplane with maximal margin, then softening that objective with regularization and, when needed, moving the problem into a richer feature space through kernels.

## What It Does

SVMs help the researcher:

- turn binary classification into a convex optimization problem
- control fit through margin size and slack penalties
- separate linear and nonlinear decision boundaries cleanly
- express nonlinear structure with kernels rather than explicit feature expansion

## Source Synthesis

- [[Mathematical Methods - Ch 03 Machine Learning]] gives the cleanest current derivation in the vault from geometric margin to hard-margin, soft-margin, dual, and kernelized SVMs.
- [[Bishop Pattern Recognition and Machine Learning]] and [[An Introduction to Statistical Learning]] provide the broader statistical and applied ML context around margin classifiers and tuning practice.

## Assumptions

The method works best when:

- classes are at least moderately separable in the chosen feature space
- feature scaling is handled explicitly
- the loss of misclassification is closer to a margin problem than to calibrated probability estimation
- the kernel choice matches the actual geometry of the problem

## Workflow

1. Encode labels consistently, often as `-1` and `+1`.
2. Standardize features before fitting.
3. Choose linear versus kernelized SVM based on the expected geometry.
4. Tune the regularization parameter `C` and any kernel hyperparameters.
5. Inspect support vectors, margin violations, and out-of-sample performance.
6. Recheck class imbalance and score calibration if the downstream use needs probabilities.

## Diagnostics

- fraction of observations becoming support vectors
- stability of results under nearby `C` or kernel choices
- class imbalance and asymmetric error rates
- whether the model is fitting noise via an overly flexible kernel
- whether decision scores need calibration before use in ranking or sizing

## Failure Modes

- skipping feature scaling
- choosing a fashionable kernel without a geometric reason
- interpreting raw margin scores as calibrated probabilities
- using kernel SVMs on large datasets without checking computational cost
- ignoring nonstationarity when the classifier is applied to market data over time

## Quant Use Cases

- event versus non-event classification
- distress, default, or fraud screening
- binary regime classification
- cross-sectional security filtering
- nonlinear decision boundaries in factor or alternative-data feature spaces

## Related Notes

- [[Principal Component Analysis]]
- [[Probabilistic Machine Learning]]
- [[Mathematical Methods]]
- [[Mathematical Methods - Ch 03 Machine Learning]]
- [[Financial Machine Learning Workflow]]

## Sources

- [[Mathematical Methods]]
- [[Mathematical Methods - Ch 03 Machine Learning]]
- [[Bishop Pattern Recognition and Machine Learning]]
- [[An Introduction to Statistical Learning]]
