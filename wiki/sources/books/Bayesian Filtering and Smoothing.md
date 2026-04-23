---
title: Bayesian Filtering and Smoothing
type: source
status: overview_source
updated: 2026-04-22
tags:
  - source
  - book
  - bayesian
  - filtering
  - smoothing
  - state-space
source_type: book
source_class: overview_source
read_scope: full_source
source_author:
  - Simo Sarkka
  - Lennart Svensson
source_year: 2023
source_order: 9
domain: statistics
extraction_basis: full_toc_scan_pymupdf4llm_chapter_scan_plus_selected_theorem_page_renders_via_pymupdf_with_mathjax_rewrite
technical_depth: deep
parent_source: null
sources:
  - "[[raw/math_statistics/Simo Särkkä and Lennart Svensson, Bayesian Filtering and Smoothing.pdf]]"
---
# Bayesian Filtering and Smoothing

## Citation / metadata

- Authors: Simo Särkkä and Lennart Svensson
- Edition: second edition
- Year on raw source: 2023 pre-publication Cambridge University Press version
- Source type: textbook
- Read scope: `full_source`
- Shelf role: advanced Bayesian state-space spine after [[Time Series Analysis by State Space Methods]]
- Raw source: [[raw/math_statistics/Simo Särkkä and Lennart Svensson, Bayesian Filtering and Smoothing.pdf]]

## Why this book matters

This is the book that turns the vault's earlier state-space material into a full Bayesian inference stack instead of a mostly linear-Gaussian toolbox.

For the vault, the durable value is not only that it covers more algorithms. The book makes several high-leverage relationships explicit:

- model construction, filtering, smoothing, and parameter learning are one recursive architecture
- discrete-state HMMs and continuous-state nonlinear systems belong to the same Bayesian state-space grammar
- EKF, sigma-point filters, statistical linearization, and posterior linearization differ mainly by how they choose the Gaussian approximation
- particle methods are not just "nonlinear Kalman filters" but simulation-based posterior approximations with their own degeneracy and proposal-design logic

## Reading logic from the source

The reingest followed the current three-step rule with a stronger theorem pass than the earlier shelf version:

1. full scan of the preface, TOC, and all seventeen chapters using PyMuPDF extraction
2. targeted page renders on the chapters where notation, algorithm boundaries, and theorem statements mattered most
3. chapter rewrites and durable promotion around the model-building, Gaussian-approximation, particle, discrete-state, smoothing, and parameter-learning core

The parent note stays thin. The detailed equations, algorithm spines, and caveats now live in the chapter shelf and promoted method layer.

## Stage map

- `scan`: [[Bayesian Filtering and Smoothing - Ch 01 What Are Bayesian Filtering and Smoothing]]
- `scan`: [[Bayesian Filtering and Smoothing - Ch 02 Bayesian Inference]]
- `selective_deepen`: [[Bayesian Filtering and Smoothing - Ch 03 Batch and Recursive Bayesian Estimation]]
- `deep`: [[Bayesian Filtering and Smoothing - Ch 04 Discretization of Continuous-Time Dynamic Models]]
- `deep`: [[Bayesian Filtering and Smoothing - Ch 05 Modeling with State Space Models]]
- `deep`: [[Bayesian Filtering and Smoothing - Ch 06 Bayesian Filtering Equations and Exact Solutions]]
- `deep`: [[Bayesian Filtering and Smoothing - Ch 07 Extended Kalman Filtering]]
- `deep`: [[Bayesian Filtering and Smoothing - Ch 08 General Gaussian Filtering]]
- `deep`: [[Bayesian Filtering and Smoothing - Ch 09 Gaussian Filtering by Enabling Approximations]]
- `deep`: [[Bayesian Filtering and Smoothing - Ch 10 Posterior Linearization Filtering]]
- `deep`: [[Bayesian Filtering and Smoothing - Ch 11 Particle Filtering]]
- `deep`: [[Bayesian Filtering and Smoothing - Ch 12 Bayesian Smoothing Equations and Exact Solutions]]
- `deep`: [[Bayesian Filtering and Smoothing - Ch 13 Extended Rauch-Tung-Striebel Smoothing]]
- `deep`: [[Bayesian Filtering and Smoothing - Ch 14 General Gaussian Smoothing]]
- `deep`: [[Bayesian Filtering and Smoothing - Ch 15 Particle Smoothing]]
- `deep`: [[Bayesian Filtering and Smoothing - Ch 16 Parameter Estimation]]
- `scan`: [[Bayesian Filtering and Smoothing - Ch 17 Epilogue]]

## Chapter shelf

- [[Bayesian Filtering and Smoothing - Ch 01 What Are Bayesian Filtering and Smoothing]]
- [[Bayesian Filtering and Smoothing - Ch 02 Bayesian Inference]]
- [[Bayesian Filtering and Smoothing - Ch 03 Batch and Recursive Bayesian Estimation]]
- [[Bayesian Filtering and Smoothing - Ch 04 Discretization of Continuous-Time Dynamic Models]]
- [[Bayesian Filtering and Smoothing - Ch 05 Modeling with State Space Models]]
- [[Bayesian Filtering and Smoothing - Ch 06 Bayesian Filtering Equations and Exact Solutions]]
- [[Bayesian Filtering and Smoothing - Ch 07 Extended Kalman Filtering]]
- [[Bayesian Filtering and Smoothing - Ch 08 General Gaussian Filtering]]
- [[Bayesian Filtering and Smoothing - Ch 09 Gaussian Filtering by Enabling Approximations]]
- [[Bayesian Filtering and Smoothing - Ch 10 Posterior Linearization Filtering]]
- [[Bayesian Filtering and Smoothing - Ch 11 Particle Filtering]]
- [[Bayesian Filtering and Smoothing - Ch 12 Bayesian Smoothing Equations and Exact Solutions]]
- [[Bayesian Filtering and Smoothing - Ch 13 Extended Rauch-Tung-Striebel Smoothing]]
- [[Bayesian Filtering and Smoothing - Ch 14 General Gaussian Smoothing]]
- [[Bayesian Filtering and Smoothing - Ch 15 Particle Smoothing]]
- [[Bayesian Filtering and Smoothing - Ch 16 Parameter Estimation]]
- [[Bayesian Filtering and Smoothing - Ch 17 Epilogue]]

## Core objects and modeling vocabulary

- latent state and measurement
  $$x_k,\qquad y_k$$
- transition and likelihood laws
  $$p(x_k \given x_{k-1}), \qquad p(y_k \given x_k)$$
- predictive, filtering, and smoothing distributions
  $$p(x_k \given y_{1:k-1}), \qquad p(x_k \given y_{1:k}), \qquad p(x_k \given y_{1:T})$$
- Gaussian approximation moments
  $$m_k,\qquad P_k,\qquad C_k,\qquad S_k$$
- continuous-time dynamics and spectral-density objects
  $$dx(t)=f(x(t))\,dt + L(x(t))\,dw(t), \qquad Q_c$$
- linearization objects
  $$F_x,\qquad H_x,\qquad A,\qquad b,\qquad \Lambda,\qquad \Omega$$
- particle objects
  $$x_k^{(i)},\qquad w_k^{(i)},\qquad N_\mathrm{eff}$$
- learning objects
  $$p(y_{1:T}\given \theta),\qquad \varphi(\theta),\qquad Q(\theta,\theta^{(n)})$$

## Main themes

- Filtering, smoothing, and parameter learning are all Bayesian posterior computation problems, not disconnected engineering recipes.
- The deepest design choice in nonlinear state-space work is the approximation family: Taylor, moment matching, statistical linear regression, posterior linearization, or particle simulation.
- Discrete-state HMMs, continuous-valued diffusions, and mixed models still share the same recursive Bayesian structure.
- Smoothing is not an optional afterthought. The book repeatedly shows that trajectory-level inference changes both state reconstruction and parameter learning.
- Exact linear-Gaussian theory remains the backbone. Even the nonlinear chapters keep reducing back to Kalman or RTS recursions after choosing an approximation device.

## Promoted durable notes

- [[State Space Discretization from Continuous-Time Models]]
- [[General Gaussian Filtering and Smoothing]]
- [[Posterior Linearization in State Space Inference]]
- [[Particle Filtering]]
- [[Particle Smoothing]]
- [[Parameter Estimation in State Space Models]]
- [[Hidden Markov Models and Switching Autoregression]]

## Next promotion targets

- a dedicated note on sigma-point quadrature design and Gaussian-moment approximation error
- a dedicated note on auxiliary versus Rao-Blackwellized particle design
- a dedicated note on sensitivity equations, Fisher identity, and gradient-based parameter learning
- a dedicated note on robust, cluttered, count, and discrete observation models in state-space form

## Caveats

- The raw PDF is a pre-publication Cambridge version, so publication metadata should still be checked against the final edition if formal citation matters.
- The book is mathematically cleaner than many finance texts, but much of the example universe is tracking and engineering. Durable quant use still depends on translating the modeling choices into market-state, volatility, or regime problems.
- Gaussian approximations are presented with unusual clarity, but that does not make them universally reliable. Multimodality, severe skewness, and high-dimensional weight collapse still force method changes.
- The source gives an honest particle-method account, but it does not solve the curse of dimensionality or model misspecification for us.

## Related notes

- [[Time Series Analysis by State Space Methods]]
- [[State Space Models]]
- [[Kalman Filtering]]
- [[Posterior Linearization in State Space Inference]]
- [[Particle Filtering]]
- [[Particle Smoothing]]
- [[General Gaussian Filtering and Smoothing]]
- [[Parameter Estimation in State Space Models]]
- [[Stats Map]]
- [[Signal Processing Map]]

## Sources

- [[raw/math_statistics/Simo Särkkä and Lennart Svensson, Bayesian Filtering and Smoothing.pdf]]
