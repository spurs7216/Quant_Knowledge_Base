---
title: Advances in Financial Machine Learning
type: source
status: chapter_ingested
updated: 2026-04-18
tags:
  - source
  - machine-learning
  - quant-finance
  - research-workflow
sources:
  - "[[raw/machine_learning/Marcos Lopez de Prado - Advances in Financial Machine Learning (2018).pdf]]"
---
# Advances in Financial Machine Learning

## Summary

Lopez de Prado's book is a financial-ML workflow text focused on data structures, labeling, sample weights, fractional differentiation, cross-validation under dependence, feature importance, bet sizing, backtesting, synthetic data, strategy risk, and microstructural features. The extracted contents show that the book is less about a single model class and more about correcting the research pipeline around financial data.

## Chapter-by-Chapter Ingest

- `Chapter 1. Financial Machine Learning as a Distinct Subject`: argues that financial ML needs its own workflow because financial data are noisy, non-iid, and adversarial.
- `Chapter 2. Financial Data Structures`: studies event-based bars and alternative sampling structures for market data.
- `Chapter 3. Labeling`: develops event-aware and path-aware labeling, including the triple-barrier idea.
- `Chapter 4. Sample Weights`: adjusts learning for unequal information content and dependent observations.
- `Chapter 5. Fractionally Differentiated Features`: seeks stationarity without discarding long-memory information.
- `Chapter 6. Ensemble Methods`: studies bagging-style robustness in noisy financial settings.
- `Chapter 7. Cross-Validation in Finance`: develops purging and embargo logic for leakage control.
- `Chapter 8. Feature Importance`: emphasizes understanding signal contribution rather than only predictive score.
- `Chapter 9. Hyper-Parameter Tuning with Cross-Validation`: treats tuning as part of the leakage-control problem.
- `Chapter 10. Bet Sizing`: connects prediction quality with capital allocation.
- `Chapter 11. The Dangers of Backtesting`: focuses directly on backtest overfitting.
- `Chapter 12. Backtesting through Cross-Validation`: reframes validation as the main defense against false discovery.
- `Chapter 13. Backtesting on Synthetic Data`: uses simulated data to stress strategies beyond historical accidents.
- `Chapter 14. Backtest Statistics`: formalizes evaluation metrics for historical tests.
- `Chapter 15. Understanding Strategy Risk`: treats risk decomposition as part of the research process.
- `Chapter 16. Machine Learning Asset Allocation`: applies ML to allocation decisions rather than only signals.
- `Chapter 17. Structural Breaks`: studies regime shifts and instability explicitly.
- `Chapter 18. Entropy Features`: introduces information-theoretic features.
- `Chapter 19. Microstructural Features`: mines trading-process variables for predictive structure.
- `Chapter 20. Multiprocessing and Vectorization`: addresses computational efficiency in research loops.
- `Chapter 21. Brute Force and Quantum Computers`: frames computational search as part of strategy discovery.
- `Chapter 22. High-Performance Computational Intelligence and Forecasting`: closes with scalable computational forecasting themes.

## Key Claims

- Financial ML fails when it ignores dependence, leakage, and the mechanics of labeling and validation.
- Event-based sampling and purged validation are more important than adding ever more complex models.
- Bet sizing, risk, and backtest design belong inside the modeling workflow.

## Methods and Data

- event-based bars and financial data structures
- triple-barrier labeling and sample weighting
- purged cross-validation and embargo
- feature importance and hyperparameter tuning
- bet sizing, synthetic data, and backtest statistics
- microstructural and entropy features

## Why It Matters Here

This is one of the most directly useful books in the vault for professional quant research workflow. It is especially relevant for how the agent should reason about labels, validation, dependence, and research hygiene.

## Reflection

The deepest contribution here is methodological rather than algorithmic. The book keeps returning to the same hard point: in finance, a bad research protocol can destroy a good model, and a careful protocol can make a simple model valuable.

## Caveats

- The workflow is opinionated and not always aligned with mainstream statistical orthodoxy.
- Some sections are better treated as research heuristics than universal doctrine.

## Related Notes

- [[Financial Machine Learning Workflow]]
- [[Backtest Overfitting]]
- [[Alpha Research]]
- [[High-Frequency Trading]]

## Sources

- [[raw/machine_learning/Marcos Lopez de Prado - Advances in Financial Machine Learning (2018).pdf]]
