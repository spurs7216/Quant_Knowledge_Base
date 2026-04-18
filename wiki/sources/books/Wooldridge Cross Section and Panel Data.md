---
title: Wooldridge Cross Section and Panel Data
type: source
status: chapter_ingested
updated: 2026-04-18
tags:
  - source
  - econometrics
  - panel-data
  - textbook
sources:
  - "[[raw/econometrics/Wooldridge - Cross-section and Panel Data.pdf]]"
---
# Wooldridge Cross Section and Panel Data

## Summary

This book is an advanced cross-section and panel-data econometrics text with strong emphasis on causality, endogeneity, unobserved effects, instrumental variables, and policy-relevant estimation. The extracted preface and contents show that panel-data methods are a central theme rather than a short appendix.

## Chapter-by-Chapter Ingest

- `Chapter 1. Introduction`: frames causal relationships, ceteris paribus logic, stochastic assumptions, and core data structures.
- `Chapter 2. Conditional Expectations and Related Concepts in Econometrics`: makes conditional expectations and linear projections foundational for applied work.
- `Chapter 3. Basic Asymptotic Theory`: supplies the convergence machinery needed for modern estimator behavior.
- `Chapter 4. The Single-Equation Linear Model and OLS Estimation`: develops OLS with emphasis on omitted variables and measurement error.
- `Chapter 5. Instrumental Variables Estimation of Single-Equation Linear Models`: treats IV and 2SLS as the main solution to endogeneity in single-equation settings.
- `Chapter 6. Additional Single-Equation Topics`: expands into generated regressors, specification tests, and alternative sampling schemes.
- `Chapter 7. Estimating Systems of Equations by OLS and GLS`: handles multivariate systems, FGLS, SUR, and a revisited linear panel model.
- `Chapter 8. System Estimation by Instrumental Variables`: generalizes system estimation through GMM and system-IV logic.
- `Chapter 9. Simultaneous Equations Models`: studies identification and estimation in structural systems.
- `Chapter 10. Basic Linear Unobserved Effects Panel Data Models`: makes FE, RE, and first-difference methods central to omitted-variable control in panels.
- `Chapter 11. More Topics in Linear Unobserved Effects Models`: extends panel work beyond strict exogeneity and basic FE/RE frameworks.
- `Chapter 12. M-Estimation`: generalizes estimation to objective-function based frameworks.
- `Chapter 13. Maximum Likelihood Methods`: develops conditional MLE and panel-related likelihood methods.
- `Chapter 14. Generalized Method of Moments and Minimum Distance Estimation`: systematizes moment-based estimation beyond OLS and IV.
- `Chapter 15. Discrete Response Models`: handles binary, multinomial, ordered, and panel discrete outcomes.
- `Chapter 16. Corner Solution Outcomes and Censored Regression Models`: studies Tobit-style limited observability and corner solutions.
- `Chapter 17. Sample Selection, Attrition, and Stratified Sampling`: addresses selection bias, attrition, and sample-design complications.
- `Chapter 18. Estimating Average Treatment Effects`: puts treatment-effect logic and counterfactual reasoning directly into the econometric core.
- `Chapter 19. Count Data and Related Models`: covers Poisson-style and related exponential-family responses.
- `Chapter 20. Duration Analysis`: closes with time-to-event modeling and hazard-based reasoning.

## Key Claims

- Cross-section and panel methods deserve dedicated treatment rather than being treated as minor extensions of the classical linear model.
- Identification, endogeneity, and unobserved heterogeneity are fundamental applied problems.
- Panel data is valuable because repeated observations let the researcher handle omitted-variable problems more credibly.
- Advanced applied work must handle selection, attrition, limited dependent variables, count data, and nonlinear response models.

## Methods and Data

The extracted contents show explicit coverage of:

- conditional expectation and asymptotic theory
- OLS, IV, 2SLS, GLS, and GMM
- simultaneous equations
- linear unobserved-effects panel models
- fixed effects, random effects, first differencing, and dynamic panels
- binary response, Tobit, sample selection, and attrition
- count data and fractional response models

The preface also makes clear that the book is motivated by modern empirical practice and policy evaluation, not only formal derivation.

## Why It Matters Here

This source is the strongest current anchor in the vault for:

- panel regressions over securities, firms, or institutions
- endogeneity-aware empirical design
- fixed-effects reasoning
- selection and attrition concerns in filtered research samples

## Reflection

Wooldridge is the most important single source in the current vault for disciplined panel and causal thinking. If a quant project uses linked firm-security data, nonrandom filtering, or potentially endogenous regressors, this is the book that forces the researcher to state the design honestly.

## Caveats

- The book is not a finance-only text, so market-specific interpretation still needs to come from finance sources and project work.

## Related Notes

- [[Panel Data]]
- [[Hansen Econometrics]]
- [[Brooks Introductory Econometrics for Finance]]
- [[CCM]]
- [[comp_na_daily_all_annual]]
- [[ownership_13F]]

## Sources

- [[raw/econometrics/Wooldridge - Cross-section and Panel Data.pdf]]
