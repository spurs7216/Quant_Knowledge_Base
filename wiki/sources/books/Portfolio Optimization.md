---
title: Portfolio Optimization
type: source
status: chapter_ingested
updated: 2026-04-18
tags:
  - source
  - quant-finance
  - portfolio
  - optimization
sources:
  - "[[raw/quantitative_finance/portfolio-optimization-book.pdf]]"
---
# Portfolio Optimization

## Summary

Daniel Palomar's book organizes portfolio optimization from stylized facts and data models into modern portfolio theory, backtesting, alternative risk measures, risk parity, graph-based portfolios, robust portfolios, pairs trading, and deep-learning portfolios. The extracted contents show a portfolio text that treats data structure and evaluation as seriously as optimization itself.

## Chapter-by-Chapter Ingest

- `Chapter 1. Introduction`: frames portfolio optimization as a broad modeling and engineering problem.
- `Chapter 2. Financial Data: Stylized Facts`: studies empirical regularities that any portfolio model must respect.
- `Chapter 3. Financial Data: I.I.D. Modeling`: develops classical return modeling assumptions.
- `Chapter 4. Financial Data: Time Series Modeling`: introduces dynamic return structure.
- `Chapter 5. Financial Data: Graphs`: treats network structure as a representation for financial dependence.
- `Chapter 6. Portfolio Basics`: builds the notation and mechanics of portfolio returns and risk.
- `Chapter 7. Modern Portfolio Theory`: develops the mean-variance baseline.
- `Chapter 8. Portfolio Backtesting`: makes evaluation and realistic testing central to portfolio research.
- `Chapter 9. High-Order Portfolios`: moves beyond mean and variance.
- `Chapter 10. Portfolios with Alternative Risk Measures`: broadens the risk objective set.
- `Chapter 11. Risk Parity Portfolios`: studies allocation by balancing risk contributions.
- `Chapter 12. Graph-Based Portfolios`: uses network structure directly in portfolio design.
- `Chapter 13. Index Tracking Portfolios`: handles benchmark replication and constrained allocation.
- `Chapter 14. Robust Portfolios`: addresses estimation error and instability.
- `Chapter 15. Pairs Trading Portfolios`: treats relative-value portfolios as an optimization problem.
- `Chapter 16. Deep Learning Portfolios`: connects newer representation methods to portfolio construction.

## Key Claims

- Portfolio construction begins with empirical structure, not only optimization formulas.
- Backtesting and robustness are integral to portfolio design.
- Alternative risk measures, graph methods, and robust formulations matter because estimation error is unavoidable.

## Methods and Data

- stylized facts and return modeling
- mean-variance and alternative-risk optimization
- risk parity and index tracking
- graph-based and robust portfolios
- pairs trading and deep-learning portfolios

## Why It Matters Here

This is one of the most important portfolio texts in the vault. It is especially useful as the anchor source for a reusable `Portfolio Construction` note.

## Reflection

The strongest point of the book is its refusal to isolate optimization from data quality and backtesting. That is exactly the right posture for professional quant research.

## Caveats

- The book spans many portfolio families, so no single technique is treated exhaustively.
- Deep-learning portfolio chapters should be read with the same skepticism applied to all financial ML claims.

## Related Notes

- [[Portfolio Construction]]
- [[Backtest Overfitting]]
- [[Alpha Research]]

## Sources

- [[raw/quantitative_finance/portfolio-optimization-book.pdf]]
