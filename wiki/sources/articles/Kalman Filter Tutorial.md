---
title: Kalman Filter Tutorial
type: source
status: section_ingested
updated: 2026-04-18
tags:
  - source
  - kalman-filter
  - state-space
  - tutorial
sources:
  - "[[raw/math_statistics/Kalman filter.pdf]]"
---
# Kalman Filter Tutorial

## Summary

This short tutorial chapter by Tony Lacey presents the Kalman filter as an optimal recursive estimator under linear Gaussian assumptions. It derives the filter first through mean-squared-error minimization and then through a maximum-likelihood / chi-square perspective, ending with the recursive algorithm in state-space form.

## Section-by-Section Ingest

- `11.1 Introduction`: frames filtering as information extraction under an explicit loss function and motivates the Kalman filter as an optimal estimator in common tracking and prediction tasks.
- `11.2 Mean Squared Error`: defines the estimation problem through expected squared error and makes MSE the optimization target.
- `11.3 Maximum Likelihood`: shows that Gaussian-noise maximum likelihood leads to the same driving objective as MSE minimization.
- `11.4 Kalman Filter Derivation`: positions Kalman relative to Wiener filtering and motivates the state-space approach.
- `11.5 State Space Derivation`: derives the recursive update equations for the state estimate, innovation, Kalman gain, and covariance recursion.
- `11.6 The Kalman Filter as a Chi-Square Merit Function`: reinterprets the filter as recursive least squares and links it to parameter-fitting logic.
- `11.7 Model Covariance Update`: shows the equivalence between covariance and information-matrix update views.

## Key Claims

- Under linear Gaussian assumptions, MSE minimization and maximum likelihood point to the same recursive estimator.
- The state-space formulation is what makes the Kalman filter computationally attractive and extensible.
- The Kalman filter is best understood as recursive least squares with explicit uncertainty propagation.

## Methods and Data

- mean-squared-error minimization
- maximum likelihood under Gaussian noise
- state-space modeling
- recursive covariance propagation
- information-filter interpretation

## Why It Matters Here

This is the shortest clean route in the raw shelf from general statistics into state-space estimation. It is especially useful as a bridge note before deeper work on Bayesian filtering, regime models, signal extraction, and execution-state tracking.

## Reflection

The tutorial's main strength is conceptual economy. It strips the Kalman filter back to the minimum set of statistical ideas needed to use it intelligently rather than as a memorized formula sheet.

## Caveats

- This is a short tutorial chapter rather than a full state-space text.
- The derivation assumes linear Gaussian structure; nonlinear and non-Gaussian extensions require follow-up material.

## Related Notes

- [[Kalman Filtering]]
- [[Bayesian Filtering and Smoothing]]
- [[Financial Signal Processing and Machine Learning]]
- [[Signal Processing Map]]

## Sources

- [[raw/math_statistics/Kalman filter.pdf]]
