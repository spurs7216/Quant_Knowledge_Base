---
title: Wiki Index
type: index
status: seed
updated: 2026-04-22
tags:
  - index
  - wiki
---
# Wiki Index

This is the curated durable map of the vault's compiled knowledge base. Use it to find stable notes, not scratch work.

It is a human gateway, not the primary machine retrieval surface once the wiki becomes large. Use exact search, Obsidian, or QMD when the target note is not already obvious.

## Navigation

- [Vault README](../README.md)
- [Agent Schema](../AGENTS.md)
- [Raw Source Library](../raw/README.md)
- [Data Catalog Mirror](../catalog/README.md)
- [Projects Layer](../projects/README.md)
- [Artifacts Layer](../artifacts/README.md)
- [[glossary]]
- [[Reading Map]]
- [[Math Map]]
- [[Stats Map]]
- [[ML Map]]
- [[Finance Map]]
- [[Microstructure Map]]
- [[Signal Processing Map]]
- [Knowledge Base Canvas](maps/knowledge_base.canvas)
- [[inbox]]
- [[log]]

## Recent Updates

```dataview
TABLE type, status, updated
FROM "wiki"
WHERE updated
SORT updated DESC, file.name ASC
LIMIT 15
```

## Core Areas

### Maps

- Folder: `wiki/maps/`
- [[Reading Map]]
- [[Math Map]]
- [[Stats Map]]
- [[ML Map]]
- [[Finance Map]]
- [[Microstructure Map]]
- [[Signal Processing Map]]
- [Knowledge Base Canvas](maps/knowledge_base.canvas)

### Datasets

- Folder: `wiki/datasets/`
- [[daily_stock]]
- [[CCM]]
- [[comp_na_daily_all_annual]]
- [[option_forward_price]]
- [[option_volumne]]
- [[ownership_13F]]
- [[risk_free_rate]]
- [[Treasurey_Daily_Time_Series]]
- [[Treasurey_Term_structure]]

### Identifiers

- Folder: `wiki/identifiers/`
- [[permno]]
- [[gvkey]]
- [[secid]]
- [[ticker]]
- [[cusip]]

### Source Notes

- Folders: `wiki/sources/books/` for overview notes, `wiki/sources/books/<Book Title>/` for chapter digests of deeply ingested books, `wiki/sources/papers/`, `wiki/sources/articles/`
- Articles: [[Karpathy LLM Knowledge Bases Thread]], [[LLM Wiki Gist]], [[LLM Wiki v2 Guide]], [[Atlan LLM Knowledge Base Guide]], [[Obsidian Spaced Repetition Plugin]], [[Obsidian CLI README]]
- Books: [[Hull Options Futures and Other Derivatives]], [[Hansen Econometrics]], [[Brooks Introductory Econometrics for Finance]], [[Wooldridge Cross Section and Panel Data]]
- [[An Introduction to Statistical Learning]]
- [[Bishop Pattern Recognition and Machine Learning]]
- [[Murphy Probabilistic Machine Learning An Introduction]]
- [[Murphy Probabilistic Machine Learning]]
- [[Bayesian Reasoning and Machine Learning]]
- [[Financial Signal Processing and Machine Learning]]
- [[Advances in Financial Machine Learning]]
- [[Machine Learning for Asset Managers]]
- [[Foundations of Reinforcement Learning]]
- [[All of Statistics]]
- [[Linear Algebra for Data Science, Machine Learning, and Signal Processing]]
- Fresh three-step ingest example: `wiki/sources/books/Linear Algebra for Data Science, Machine Learning, and Signal Processing/`
- `deep` for Chapters 3, 5, 7, 9
- `selective_deepen` for Chapters 4, 6, 8, 10, 12
- `scan` for Chapters 1, 2, 11
- [[Applied Time Series Analysis and Forecasting with Python]]
- Fresh three-step ingest example: `wiki/sources/books/Applied Time Series Analysis and Forecasting with Python/`
- `deep` for Chapters 3, 4, 6, 7, 9
- `selective_deepen` for Chapters 5, 8
- `scan` for Chapters 1, 2, 10
- Deep-ingest example: `wiki/sources/books/All of Statistics/` stores the full 24-chapter shelf under the staged ingest rule:
- `deep` for Chapters 1 to 5, 7 to 12, 16, 17, and 20 to 24
- `scan` for Chapters 6, 13 to 15, 18, 19
- [[Applied Probability]]
- Fresh three-step ingest example: `wiki/sources/books/Applied Probability/`
- `deep` for Chapters 6, 7, 8, 10, 11
- `selective_deepen` for Chapters 2, 3, 9, 12, 13, 14
- `scan` for Chapters 1, 4, 5, 15
- [[Time Series Analysis and Its Applications]]
- Fresh three-step ingest example: `wiki/sources/books/Time Series Analysis and Its Applications/`
- `deep` for Chapters 1, 3, 4, 6
- `selective_deepen` for Chapters 2, 5, 7
- [[Time Series Analysis by State Space Methods]]
- Fresh three-step ingest example: `wiki/sources/books/Time Series Analysis by State Space Methods/`
- `deep` for Chapters 2, 3, 4, 5, 7
- `selective_deepen` for Chapters 6, 9, 10, 11, 12, 13
- `scan` for Chapters 1, 8, 14
- [[Bayesian Filtering and Smoothing]]
- Fresh three-step ingest example: `wiki/sources/books/Bayesian Filtering and Smoothing/`
- `deep` for Chapters 4 to 16
- `selective_deepen` for Chapter 3
- `scan` for Chapters 1, 2, 17
- [[Arbitrage Theory in Continuous Time]]
- [[Convex Optimization]]
- Fresh three-step ingest example: `wiki/sources/books/Convex Optimization/`
- `deep` for Chapters 2, 3, 4, 5, 6, 7, 9, 11
- `selective_deepen` for Chapters 8, 10
- `scan` for Chapter 1
- [[Probability Theory The Logic of Science]]
- Fresh three-step ingest example: `wiki/sources/books/Probability Theory The Logic of Science/`
- `deep` for Chapters 1, 2, 6, 7, 8, 11, 13, 18, 19, 21, 24, 30
- `selective_deepen` for Chapters 3, 4, 5, 9, 10, 14, 15, 17, 20, 27
- `scan` for Chapter 16
- [[Modelling Extremal Events for insurance and finance]]
- Fresh three-step ingest example: `wiki/sources/books/Modelling Extremal Events for insurance and finance/`
- `deep` for Chapters 1 to 8
- [[Stochastic Calculus for Finance II]]
- Fresh three-step ingest example: `wiki/sources/books/Stochastic Calculus for Finance II/`
- `deep` for Chapters 2, 3, 4, 5, 6, 8, 9, 10, 11
- `selective_deepen` for Chapters 1 and 7
- [[Arbitrage Theory in Continuous Time]]
- Fresh three-step ingest example: `wiki/sources/books/Arbitrage Theory in Continuous Time/`
- `deep` for Chapters 3, 4, 5, 7, 8, 11, 12, 14, 15, 19, 21, 22, 23, 25, 27, 28, 29, 30, 31, 36, 38
- `selective_deepen` for Chapters 2, 6, 9, 10, 13, 20, 24, 26, 32, 33, 34
- `scan` for Chapters 1, 16, 17, 18, 35, 37
- [[Mathematical Methods]]
- Fresh three-step ingest example: `wiki/sources/books/Mathematical Methods/`
- `deep` for Chapters 2 and 3
- `selective_deepen` for Chapter 4
- `scan` for Chapter 1
- [[Aldridge High-Frequency Trading]]
- [[Algorithmic Trading Winning Strategies and Their Rationale]]
- [[Statistics and Data Analysis for Financial Engineering]]
- [[Implementing Models in Quantitative Finance]]
- [[Monte Carlo Methods in Financial Engineering]]
- [[Portfolio Optimization]]
- [[Quantitative Risk Management]]
- [[Quantitative Trading]]
- [[Tools for Computational Finance]]
- [[Finding Alphas]]
- [[Ensemble Methods in Data Mining]]
- [[Financial Risk Manager Handbook]]
- [[Quantitative Strategies for Achieving Alpha]]
- [[Heard on the Street]]
- [[A Practical Guide to Quantitative Finance Interviews]]
- [[Quant Job Interview Questions and Answers]]
- Papers: [[Causality and Factor Investing A Primer]], [[GraphSAGE with Deep Reinforcement Learning for Financial Portfolio Optimization]]
- Articles and captures: [[Kalman Filter Tutorial]], [[Target from Quant Firm]]

### Concepts, Methods, Metrics, and Strategies

- Folders: `wiki/concepts/`, `wiki/methods/`, `wiki/metrics/`, `wiki/strategies/`
- Priorities: econometrics, time series, state-space methods, factor research, portfolio construction, and evaluation discipline.
- Current method seeds: [[Panel Data]], [[Financial Machine Learning Workflow]], [[Monte Carlo Methods]], [[Time-Series Forecasting]], [[ARIMA and Box-Jenkins Modeling]], [[GARCH Models]], [[Vector Autoregression and Impulse Response Analysis]], [[State Space Models]], [[Kalman Filtering]], [[State Space Discretization from Continuous-Time Models]], [[General Gaussian Filtering and Smoothing]], [[Posterior Linearization in State Space Inference]], [[Diffuse Initialization in State Space Models]], [[Simulation Smoothing]], [[Particle Filtering]], [[Particle Smoothing]], [[Dynamic Factor Models]], [[Cointegration and Error Correction Models]], [[Stationarity and Unit-Root Diagnostics]], [[Spectral Analysis and Filtering]], [[Long Memory and Fractional Differencing]], [[Transfer Function Models]], [[Hidden Markov Models and Switching Autoregression]], [[Stochastic Calculus]], [[Ito Calculus and Stochastic Differential Equations]], [[Risk-Neutral Pricing and Fundamental Theorems of Asset Pricing]], [[American Options and Optimal Stopping]], [[Change of Numeraire and Forward Measures]], [[Term-Structure Models]], [[Heath-Jarrow-Morton Drift Condition]], [[LIBOR Market Models]], [[Stochastic Optimal Control and Hamilton-Jacobi-Bellman Equation]], [[Martingale Methods for Portfolio Optimization]], [[Esscher Transform and Minimal Martingale Measure]], [[Utility Indifference Pricing]], [[Good Deal Bounds]], [[Parameter Estimation in State Space Models]], [[Convex Optimization Methods]], [[Convex Duality and KKT Conditions]], [[Regularization and Robust Approximation]], [[Interior-Point Methods]], [[Bootstrap]], [[Maximum Likelihood Estimation]], [[Maximum Entropy Principle]], [[Bayesian Model Comparison and Occam Factors]], [[Markov Chain Monte Carlo]], [[Least Squares and Pseudoinverse]], [[Low-Rank Approximation]], [[Gradient Descent and Preconditioning]], [[Graph Laplacians and Spectral Graph Methods]], [[Support Vector Machines]], [[Principal Component Analysis]], [[Extreme Value Theory for Maxima and Threshold Exceedances]], [[Point Process Methods for Extremes]], [[Ruin Asymptotics with Small and Large Claims]], [[Tail Index Estimation]], [[Heavy-Tailed Time Series Analysis]], [[Stochastic Recurrence Equations and ARCH Tail Behavior]]
- Current concept seeds: [[Probabilistic Machine Learning]], [[Reinforcement Learning]], [[Derivatives Markets]], [[High-Frequency Trading]], [[Backtest Overfitting]], [[LLM Knowledge Base Workflow]], [[Convergence and Limit Theory]], [[Statistical Decision Theory]], [[Probability as Extended Logic]], [[Bayes Classifier]], [[Markov Chains]], [[Poisson Processes]], [[Continuous-Time Markov Chains]], [[Martingales]], [[Diffusion Processes]], [[Brownian Motion and Quadratic Variation]], [[Jump Processes and Compensators]], [[Singular Value Decomposition]], [[Regular Variation and Heavy-Tailed Distributions]], [[Extremal Index and Clustering of Extremes]], [[Stochastic Discount Factors]], [[Market Completeness and Incomplete Markets]], [[Dynamic Equilibrium Asset Pricing]]
- Current strategy seeds: [[Portfolio Construction]], [[Alpha Research]]
- Metrics layer reserved for reusable evaluation notes such as Sharpe, information coefficient, turnover, and drawdown.

## Design Sources

- [[raw/LLM Knowledge Bases/Thread by @karpathy]]
- [[raw/LLM Knowledge Bases/llm-wiki]]
- [[raw/LLM Knowledge Bases/LLM Knowledge Base Definition, Components, and Enterprise Use]]

## Dataset Table

```dataview
TABLE status, domain, updated
FROM "wiki/datasets"
WHERE type = "dataset"
SORT file.name ASC
```

## Identifier Table

```dataview
TABLE status, updated
FROM "wiki/identifiers"
WHERE type = "identifier"
SORT file.name ASC
```

## Source Table

```dataview
TABLE status, updated
FROM "wiki/sources"
WHERE type = "source"
SORT file.name ASC
```

## Initialization Notes

- `wiki/` is the durable layer. Do not use it as a scratchpad.
- Promote stable ideas from `projects/` into this folder.
- Support quantitative claims with links to `catalog/` or `artifacts/`.

## Next Gaps

- Add bridge notes for `permco`, `cik`, `linktype`, and `linkprim`.
- Add a dedicated note on spectral matrices and frequency-domain regression that sits above specific source chapters and examples.
- Add a structural-models note for trend, seasonality, and signal extraction inside state-space form.
- Review the image capture `[[Target from Quant Firm]]` manually inside Obsidian and convert it into a reusable checklist or concept note if warranted.
