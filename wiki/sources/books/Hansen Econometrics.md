---
title: Hansen Econometrics
type: source
status: chapter_ingested
updated: 2026-04-18
tags:
  - source
  - econometrics
  - textbook
  - theory
sources:
  - "[[raw/econometrics/Bruce Hansen, Econometrics.pdf]]"
---
# Hansen Econometrics

## Summary

Hansen's text is a broad, rigorous econometrics reference organized around probability, conditional expectations, projection methods, asymptotics, and modern estimation. The extracted contents show a progression from foundational regression theory into bootstrap methods, maximum likelihood, instrumental variables, GMM, time series, panel data, nonparametrics, and quantile methods.

## Chapter-by-Chapter Ingest

- `Chapter 1. Introduction`: frames econometrics through probability, observational data, replication, and standard data structures.
- `Chapter 2. Conditional Expectation and Projection`: builds the conceptual core around conditional expectation, best prediction, and causal caution.
- `Chapter 3. The Algebra of Least Squares`: formalizes OLS as a projection problem and develops the matrix machinery behind regression.
- `Chapter 4. Least Squares Regression`: turns algebra into estimation, variance formulas, robust covariance logic, and clustered-sample concerns.
- `Chapter 5. Normal Regression`: shows what exact finite-sample distributional results require when normality is imposed.
- `Chapter 6. A Review of Large Sample Asymptotics`: lays out the convergence tools needed for modern inference.
- `Chapter 7. Asymptotic Theory for Least Squares`: connects asymptotics directly to OLS consistency, normality, and robust standard errors.
- `Chapter 8. Restricted Estimation`: studies estimation under constraints, minimum distance, and misspecification.
- `Chapter 9. Hypothesis Testing`: organizes classical and modern testing logic as an inferential framework rather than a bag of procedures.
- `Chapter 10. Resampling Methods`: makes bootstrap methods part of the main inferential toolkit instead of an appendix.
- `Chapter 11. Multivariate Regression`: extends the linear framework to systems and multivariate outcomes.
- `Chapter 12. Instrumental Variables`: develops IV and 2SLS as the standard response to endogeneity and measurement error.
- `Chapter 13. Generalized Method of Moments`: generalizes estimation through orthogonality conditions and efficiency considerations.
- `Chapter 14. Time Series`: treats dependence, regression, and forecasting in explicitly dynamic data.
- `Chapter 15. Multivariate Time Series`: moves into multiple-equation dynamics and joint dependence.
- `Chapter 16. Non-Stationary Time Series`: handles unit roots, stochastic trends, and nonstationary behavior.
- `Chapter 17. Panel Data`: covers repeated-observation structures, fixed effects, dynamic panels, and panel bootstrap logic.
- `Chapter 18. Difference in Differences`: treats causal panel and policy designs explicitly rather than leaving them implicit inside FE models.
- `Chapter 19. Nonparametric Regression`: relaxes rigid functional-form assumptions through flexible regression methods.
- `Chapter 20. Series Regression`: develops basis-function and approximation approaches to nonlinear modeling.
- `Chapter 21. Regression Discontinuity`: introduces discontinuity-based causal identification.
- `Chapter 22. M-Estimators`: generalizes estimation to loss-based frameworks beyond least squares.
- `Chapter 23. Nonlinear Least Squares`: handles estimation when the model is nonlinear in parameters.
- `Chapter 24. Quantile Regression`: shifts focus from means to conditional distribution structure.
- `Chapter 25. Binary Choice`: covers discrete-response modeling for yes/no outcomes.
- `Chapter 26. Multiple Choice`: extends discrete response to multinomial and ordered settings.
- `Chapter 27. Censoring and Selection`: studies limited observability, selection bias, and related corrections.
- `Chapter 28. Model Selection, Stein Shrinkage, and Model Averaging`: turns model uncertainty into an estimation problem rather than ignoring it.
- `Chapter 29. Machine Learning`: bridges econometric thinking with high-dimensional regression, regularization, trees, forests, and double machine learning.

## Key Claims

- Econometrics should be grounded in probability and explicit assumptions.
- Replication and data structure are first-class concerns, not afterthoughts.
- Robust inference, asymptotics, and bootstrap methods are central tools, not peripheral topics.
- Time series, panel data, and nonparametric methods all fit within one coherent framework rather than separate intellectual silos.

## Methods and Data

The extracted contents and targeted chapter search show explicit coverage of:

- conditional expectation and projection
- least squares and regression algebra
- asymptotic theory
- bootstrap methods
- maximum likelihood
- instrumental variables and GMM
- time series and multivariate time series
- non-stationary time series
- panel data, dynamic panels, and panel bootstrap
- nonparametric and quantile methods

## Why It Matters Here

This is the strongest general econometrics foundation currently in the `raw/econometrics/` shelf. For the vault, it anchors:

- identification and causal caution
- robust standard errors and clustering
- panel-data reasoning
- time-series and GMM-oriented quantitative workflows

## Reflection

Hansen is the clearest bridge in the current vault between classical econometrics and modern quant tooling. It gives one continuous line from projection and asymptotics to panels, causal designs, nonparametrics, and machine learning, which is exactly the breadth a quantitative researcher needs.

## Caveats

- It is a general econometrics text, not a finance-specific playbook.

## Related Notes

- [[Panel Data]]
- [[Brooks Introductory Econometrics for Finance]]
- [[Wooldridge Cross Section and Panel Data]]

## Sources

- [[raw/econometrics/Bruce Hansen, Econometrics.pdf]]
