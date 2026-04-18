---
title: Panel Data
type: method
status: seeded
updated: 2026-04-18
tags:
  - method
  - econometrics
  - panel-data
  - causal-inference
source_count: 3
sources:
  - "[[raw/econometrics/Wooldridge - Cross-section and Panel Data.pdf]]"
  - "[[raw/econometrics/Chris Brooks, Introductory Econometrics for Finance (2019).pdf]]"
  - "[[raw/econometrics/Bruce Hansen, Econometrics.pdf]]"
---
# Panel Data

## Summary

Panel data combines a cross-sectional unit index with repeated observations over time. In quant research, that usually means securities, firms, institutions, or contracts observed across dates. The main attraction is that repeated observations allow better control of unobserved heterogeneity than a pure cross section.

## What It Does

Panel methods let the researcher:

- separate within-unit from between-unit variation
- absorb time-invariant unobserved effects through fixed effects or differencing
- model persistent heterogeneity with random effects when appropriate
- handle clustered dependence more realistically than naive OLS
- study dynamic behavior when lagged structure matters

## Source Synthesis

- From [[Wooldridge Cross Section and Panel Data]]: panel work is fundamentally about unobserved effects, endogeneity, selection, attrition, and treatment logic, not only about choosing between fixed and random effects.
- From [[Hansen Econometrics]]: panel methods sit inside a wider inferential system that connects asymptotics, bootstrap logic, difference in differences, nonlinearity, and even machine-learning-adjacent estimation.
- From [[Brooks Introductory Econometrics for Finance]]: panel methods become most useful when they are tied back to concrete finance questions, software workflows, and interpretation discipline.

## Assumptions

The main assumption set depends on the estimator, but the recurring issues are:

- correct definition of unit and time indices
- clear timing and alignment of regressors and outcomes
- explicit assumptions on exogeneity, predeterminedness, or endogeneity
- treatment of unobserved effects
- appropriate clustering or serial-correlation handling
- awareness of selection, attrition, or panel imbalance when the research sample is filtered

## Workflow

1. Define the panel keys and verify uniqueness.
2. Align entity identifiers and timestamps before estimation.
3. Decide whether the problem is descriptive, predictive, or causal.
4. Decide whether the identification is mainly within-unit, between-unit, dynamic, or treatment-based.
5. Choose an estimator such as fixed effects, random effects, first differences, dynamic-panel methods, or a design-based alternative.
6. Use robust or clustered inference that matches the dependence structure.
7. Stress-test sensitivity to filters, missingness, attrition, and alternative time alignment choices.

## Diagnostics

- check whether the panel is balanced or heavily unbalanced
- inspect within-unit variation for key regressors
- test for serial correlation and heteroskedasticity
- examine whether clustering level matches the data-generating structure
- verify that identifier linking did not introduce silent sample changes
- inspect whether selection into the panel or survival in the panel is informative

## Failure Modes

- look-ahead bias from misaligned accounting and trading dates
- stale or incorrect link tables between firms and securities
- overconfident inference from bad clustering choices
- dynamic-panel bias when lagged dependent variables are treated casually
- selection and attrition effects that silently change the population under study
- treating a prediction exercise as if it delivered causal interpretation

## Related Notes

- [[Wooldridge Cross Section and Panel Data]]
- [[Brooks Introductory Econometrics for Finance]]
- [[Hansen Econometrics]]
- [[daily_stock]]
- [[CCM]]
- [[comp_na_daily_all_annual]]
- [[ownership_13F]]

## Sources

- [[raw/econometrics/Wooldridge - Cross-section and Panel Data.pdf]]
- [[raw/econometrics/Chris Brooks, Introductory Econometrics for Finance (2019).pdf]]
- [[raw/econometrics/Bruce Hansen, Econometrics.pdf]]
