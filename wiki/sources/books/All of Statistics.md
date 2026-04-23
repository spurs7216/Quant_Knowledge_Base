---
title: All of Statistics
type: source
status: full_chapter_ingested
updated: 2026-04-20
tags:
  - source
  - statistics
  - probability
  - textbook
  - mathematical-statistics
source_type: book
source_class: overview_source
read_scope: full_source
extraction_basis: full_text
technical_depth: mixed
ingest_stage: promotion_started
source_count: 1
sources:
  - "[[raw/math_statistics/2004 - wasserman - all of statistics.pdf]]"
---
# All of Statistics

## Citation / metadata

- Author: Larry Wasserman
- Title: *All of Statistics: A Concise Course in Statistical Inference*
- Publisher: Springer
- Date in source front matter: July 2003 preface; published 2004
- Role in vault: compact mathematical statistics foundation that connects probability, inference, learning, and simulation before later econometrics and finance specialization

## Why this book matters

This book is one of the best statistics foundation texts for the vault because it gives a single operating language for uncertainty, inference, learning, and computation without pretending that those are separate subjects. The preface design choices are exactly why it matters here:

- concepts over calculation drills
- nonparametric inference introduced before heavy parametric machinery
- advanced topics such as bootstrap, density estimation, graphical models, and causation brought in early
- explicit bridges between statistics and machine-learning vocabulary

For quant research, that structure enforces the habits that prevent bad work:

- separate the data-generating model from the estimator
- state the target of inference before choosing a procedure
- track assumptions, nuisance parameters, and loss functions explicitly
- distinguish predictive association from causal language
- use asymptotics, resampling, and simulation as inferential tools rather than decorative extras

## Reading logic from the source

The book has a clean three-part dependency order:

- `Part I: Probability` builds events, random variables, expectation, concentration, and convergence.
- `Part II: Statistical Inference` moves from population objects to estimation, confidence sets, testing, Bayesian updating, and decision theory.
- `Part III: Statistical Models and Methods` applies that language to regression, dependence, causality, graphical models, smoothing, classification, stochastic processes, and simulation.

That is the right ingest logic too: preserve the full 24-chapter shelf, deepen the chapters that carry reusable theorem-level probability and inference structure, and keep the parent note as the stable shelf controller rather than a second textbook-sized digest.

## Stage map

Current shelf state after the reingest:

- `deep`: Chapters 1 to 5, 7 to 12, 16, 17, 20 to 24
- `scan`: Chapters 6, 13 to 15, 18, 19

Current basis:

- full source text read chapter by chapter
- full 24-chapter shelf built under `wiki/sources/books/All of Statistics/`
- promotion already started into durable concept and method notes

## Chapter shelf

Part I:

- [[All of Statistics - Ch 01 Probability]]
- [[All of Statistics - Ch 02 Random Variables]]
- [[All of Statistics - Ch 03 Expectation]]
- [[All of Statistics - Ch 04 Inequalities]]
- [[All of Statistics - Ch 05 Convergence of Random Variables]]

Part II:

- [[All of Statistics - Ch 06 Models Statistical Inference and Learning]]
- [[All of Statistics - Ch 07 Estimating the cdf and Statistical Functionals]]
- [[All of Statistics - Ch 08 The Bootstrap]]
- [[All of Statistics - Ch 09 Parametric Inference]]
- [[All of Statistics - Ch 10 Hypothesis Testing and p-values]]
- [[All of Statistics - Ch 11 Bayesian Inference]]
- [[All of Statistics - Ch 12 Statistical Decision Theory]]

Part III:

- [[All of Statistics - Ch 13 Linear and Logistic Regression]]
- [[All of Statistics - Ch 14 Multivariate Models]]
- [[All of Statistics - Ch 15 Inference About Independence]]
- [[All of Statistics - Ch 16 Causal Inference]]
- [[All of Statistics - Ch 17 Directed Graphs and Conditional Independence]]
- [[All of Statistics - Ch 18 Undirected Graphs]]
- [[All of Statistics - Ch 19 Log-Linear Models]]
- [[All of Statistics - Ch 20 Nonparametric Curve Estimation]]
- [[All of Statistics - Ch 21 Smoothing Using Orthogonal Functions]]
- [[All of Statistics - Ch 22 Classification]]
- [[All of Statistics - Ch 23 Probability Redux Stochastic Processes]]
- [[All of Statistics - Ch 24 Simulation Methods]]

## Core objects and modeling vocabulary

- `Omega` as the sample space, `A subset Omega` as an event, and `X : Omega -> R` as the basic map from outcomes to data
- `F` for a distribution function and `f` for a density or mass function
- `E(X)`, `Var(X)`, and `Cov(X, Y)` as the population functionals that later become inferential targets
- `X_1, ..., X_n ~ F` as the iid sampling frame that anchors much of the book
- `\hat F_n(x) = n^{-1} \sum_{i=1}^n I(X_i \le x)` as the empirical cdf and prototype nonparametric estimator
- `theta`, `Theta`, and `L(theta)` as the parameter-space and likelihood vocabulary
- `r(x) = E(Y | X = x)` as the regression target, `h : X -> Y` as the classifier, and `R(theta, \hat theta)` as the decision-theoretic risk object
- `f(theta | X^n) proportional to L(theta) f(theta)` as the Bayesian updating template
- statistics / machine-learning crosswalk kept explicit in the preface: estimation = learning, classification = supervised learning, covariates = features, classifier = hypothesis, DAG = Bayes net

## Main themes

### 1. Probability and inference are one pipeline

The book's central picture is probability as the forward data-generating story and inference as the inverse problem of learning that story from data. Forecasting, estimation, classification, and simulation all sit inside that same frame.

### 2. Nonparametrics deserve to come early

Wasserman intentionally introduces empirical-distribution and bootstrap reasoning before leaning too hard on parametric confidence. That is a strong fit for quant work, where exploratory structure and misspecification risk are common.

### 3. Asymptotics and resampling are essential

LLN, CLT, delta-method reasoning, and bootstrap logic are treated as core inferential machinery. That is the right emphasis for a research vault that has to survive noisy finite samples.

### 4. Statistics and machine learning live in one statistical universe

The book's vocabulary bridge is still useful: classification, graphical models, learning, and simulation are not external add-ons but extensions of the same probabilistic and inferential language.

### 5. Computation is part of inference

Bootstrap, Monte Carlo integration, and MCMC appear as inferential methods, not numerical side quests. That is the right discipline for later work in Bayesian modeling, state-space methods, and simulation-heavy finance problems.

## Promoted durable notes

- [[Convergence and Limit Theory]]
- [[Bootstrap]]
- [[Maximum Likelihood Estimation]]
- [[Statistical Decision Theory]]
- [[Bayes Classifier]]
- [[Markov Chains]]
- [[Markov Chain Monte Carlo]]

## Next promotion targets

- concentration inequalities
- empirical cdf and plug-in inference
- multiple testing discipline
- Bayesian vs frequentist inference
- regression and model selection
- nonparametric density / regression estimation
- graphical models
- causal inference
- Monte Carlo integration beyond MCMC

## Caveats

- The book is intentionally concise. That makes it excellent for structure and dangerous for overconfidence if treated as exhaustive.
- It is a statistics foundation, not an econometrics, time-series, asset-pricing, or market-microstructure text.
- The classification and machine-learning material is foundational rather than modern frontier material.
- The stochastic-process coverage is introductory; a quant researcher will need deeper follow-up for diffusion models, filtering, or modern time-series inference.
- The book often states results without full proof in order to keep pace. That is a feature for overview learning, but a limitation for rigorous theorem-level mastery.

## Related notes

- [[Stats Map]]
- [[Math Map]]
- [[Convergence and Limit Theory]]
- [[Bootstrap]]
- [[Maximum Likelihood Estimation]]
- [[Statistical Decision Theory]]
- [[Bayes Classifier]]
- [[Markov Chains]]
- [[Markov Chain Monte Carlo]]
- [[Monte Carlo Methods]]
- [[Time-Series Forecasting]]
- [[Financial Machine Learning Workflow]]
- [[Probabilistic Machine Learning]]
- [[Backtest Overfitting]]

## Sources

- [[raw/math_statistics/2004 - wasserman - all of statistics.pdf]]
