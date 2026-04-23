---
title: Simulation Smoothing
type: method
status: seed
updated: 2026-04-21
tags:
  - method
  - state-space
  - simulation
  - smoothing
domain: statistics
sources:
  - "[[Time Series Analysis by State Space Methods]]"
  - "[[Time Series Analysis by State Space Methods - Ch 02 Local Level Model]]"
  - "[[Time Series Analysis by State Space Methods - Ch 04 Filtering, Smoothing, and Forecasting]]"
  - "[[Time Series Analysis by State Space Methods - Ch 05 Initialisation of Filter and Smoother]]"
---
# Simulation Smoothing

## Summary

Simulation smoothing samples latent states or disturbances from their joint distribution conditional on the observed data.

It is the sampling counterpart to deterministic state smoothing. Instead of returning only a conditional mean and variance, it returns full latent trajectories or disturbance sequences.

## Core logic

- filtering updates latent-state beliefs sequentially
- smoothing uses all observations to summarize latent states or disturbances
- simulation smoothing goes one step further and draws whole latent paths conditional on the data
- this becomes a core building block for Bayesian analysis, importance sampling, and nonlinear state-space methods

## Workflow

1. Specify the linear-Gaussian state-space model and fit or condition on parameter values.
2. Run the required filter and smoother quantities.
3. Draw from the latent structure using a simulation-smoothing algorithm rather than only using conditional means.
4. Use the simulated paths for posterior summaries, scenario analysis, missing-data completion, or proposal construction in more complex algorithms.

## Why it matters

Many later methods are impossible or awkward without latent-path simulation:

- Bayesian posterior inference
- importance sampling for nonlinear / non-Gaussian models
- disturbance-level scenario generation
- uncertainty propagation beyond one conditional mean path

## Failure modes

- confusing a smoothed mean with a representative latent path
- simulating states while ignoring the distinction between state smoothing and disturbance smoothing
- forgetting that initialization treatment changes simulation when diffuse states are present

## Quant relevance

This note matters for:

- latent-state scenario generation
- Bayesian or simulation-based state-space inference
- imputation and pathwise uncertainty analysis
- stochastic-volatility and nonlinear extensions that depend on latent-path draws

## Related notes

- [[Kalman Filtering]]
- [[State Space Models]]
- [[Particle Filtering]]
- [[Diffuse Initialization in State Space Models]]
- [[Time Series Analysis by State Space Methods]]

## Sources

- [[Time Series Analysis by State Space Methods]]
- [[Time Series Analysis by State Space Methods - Ch 02 Local Level Model]]
- [[Time Series Analysis by State Space Methods - Ch 04 Filtering, Smoothing, and Forecasting]]
- [[Time Series Analysis by State Space Methods - Ch 05 Initialisation of Filter and Smoother]]
