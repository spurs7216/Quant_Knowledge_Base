---
title: All of Statistics
type: source
status: chapter_ingested
updated: 2026-04-18
tags:
  - source
  - statistics
  - probability
  - textbook
sources:
  - "[[raw/math_statistics/2004 - wasserman - all of statistics.pdf]]"
---
# All of Statistics

## Summary

Wasserman's text is a compact statistics-and-probability foundation that moves from probability and convergence into inference, resampling, regression, multivariate models, causal inference, graphical models, nonparametrics, classification, stochastic processes, and simulation. It is unusually well suited to a quant vault because it treats both classical inference and modern learning ideas as one continuous toolkit.

## Chapter-by-Chapter Ingest

- `Chapter 1. Probability`: defines probability as the base language for uncertainty and inference.
- `Chapter 2. Random Variables`: builds the object layer of distributions, transformations, and dependence.
- `Chapter 3. Expectation`: turns probability laws into estimable functionals and risk summaries.
- `Chapter 4. Inequalities`: provides concentration and comparison tools needed for bounds and consistency arguments.
- `Chapter 5. Convergence of Random Variables`: develops the asymptotic backbone behind estimators and limiting approximations.
- `Chapter 6. Models, Statistical Inference and Learning`: frames the transition from probability objects to data-generating models and estimators.
- `Chapter 7. Estimating the cdf and Statistical Functionals`: studies empirical distributions and plug-in estimation.
- `Chapter 8. The Bootstrap`: treats resampling as a practical route to uncertainty quantification.
- `Chapter 9. Parametric Inference`: covers finite-dimensional model estimation and interval construction.
- `Chapter 10. Hypothesis Testing and p-values`: studies model-based testing discipline and its interpretation.
- `Chapter 11. Bayesian Inference`: introduces posterior updating and probabilistic decision-making.
- `Chapter 12. Statistical Decision Theory`: connects estimation and testing to loss functions and optimal actions.
- `Chapter 13. Linear and Logistic Regression`: places prediction and interpretation inside common generalized linear frameworks.
- `Chapter 14. Multivariate Models`: extends univariate inference into higher-dimensional dependence structures.
- `Chapter 15. Inference About Independence`: treats dependence testing as a first-class modeling question.
- `Chapter 16. Causal Inference`: introduces causal targets and identification beyond pure association.
- `Chapter 17. Directed Graphs and Conditional Independence`: uses graphical structure to reason about dependence and causality.
- `Chapter 18. Undirected Graphs`: expands graphical modeling into Markov-network style representations.
- `Chapter 19. Log-Linear Models`: handles structured dependence in contingency-type settings.
- `Chapter 20. Nonparametric Curve Estimation`: develops flexible function estimation when parametric structure is weak.
- `Chapter 21. Smoothing Using Orthogonal Functions`: studies basis expansions as a systematic smoothing device.
- `Chapter 22. Classification`: turns supervised learning into a formal decision problem.
- `Chapter 23. Probability Redux: Stochastic Processes`: returns to time-dependent randomness in a process setting.
- `Chapter 24. Simulation Methods`: closes with Monte Carlo and related computational probability tools.

## Key Claims

- Statistical inference is inseparable from probability theory and asymptotics.
- Resampling, nonparametrics, and classification belong in the same core toolkit as regression and testing.
- Causal inference and graphical models are not optional side topics once the goal is explanation rather than prediction alone.

## Methods and Data

- probability, expectation, and concentration tools
- bootstrap and parametric inference
- regression, multivariate models, and classification
- causal inference and graphical models
- nonparametric smoothing and simulation

## Why It Matters Here

This is one of the strongest foundation texts for the vault's statistics shelf. It is especially useful for keeping quant research grounded when moving from econometrics into machine learning and from prediction into causal or decision-theoretic reasoning.

## Reflection

The value of this book is its compression. It does not linger on any one frontier, but it shows how the main statistical ideas hang together, which is exactly what a long-term quant knowledge base needs before specialization fragments the view.

## Caveats

- The treatment is broad and compact, so many topics need follow-up texts for full depth.
- Financial applications are not the focus; the book provides the statistical base rather than market-specific workflows.

## Related Notes

- [[Panel Data]]
- [[Financial Machine Learning Workflow]]
- [[Backtest Overfitting]]
- [[Stats Map]]

## Sources

- [[raw/math_statistics/2004 - wasserman - all of statistics.pdf]]
