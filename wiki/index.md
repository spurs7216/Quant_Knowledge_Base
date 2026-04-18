---
title: Wiki Index
type: index
status: seed
updated: 2026-04-19
tags:
  - index
  - wiki
---
# Wiki Index

This is the durable map of the vault's compiled knowledge base. Use it to find stable notes, not scratch work.

## Navigation

- [Vault README](../README.md)
- [Agent Schema](../agent.md)
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

- Folders: `wiki/sources/books/`, `wiki/sources/papers/`, `wiki/sources/articles/`
- Articles: [[Karpathy LLM Knowledge Bases Thread]], [[LLM Wiki Gist]], [[Atlan LLM Knowledge Base Guide]], [[Obsidian Spaced Repetition Plugin]], [[Obsidian CLI README]]
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
- [[Applied Probability]]
- [[Arbitrage Theory in Continuous Time]]
- [[Convex Optimization]]
- [[Time Series Analysis and Its Applications]]
- [[Bayesian Filtering and Smoothing]]
- [[Stochastic Calculus for Finance II]]
- [[Mathematical Methods]]
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
- Current method seeds: [[Panel Data]], [[Financial Machine Learning Workflow]], [[Monte Carlo Methods]], [[Kalman Filtering]], [[Time-Series Forecasting]], [[Stochastic Calculus]], [[Convex Optimization Methods]]
- Current concept seeds: [[Probabilistic Machine Learning]], [[Reinforcement Learning]], [[Derivatives Markets]], [[High-Frequency Trading]], [[Backtest Overfitting]], [[LLM Knowledge Base Workflow]]
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
- Add a dedicated state-space modeling note that sits one level above specific filters.
- Review the image capture `[[Target from Quant Firm]]` manually inside Obsidian and convert it into a reusable checklist or concept note if warranted.
