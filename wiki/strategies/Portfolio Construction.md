---
title: Portfolio Construction
type: strategy
status: seed
updated: 2026-04-18
tags:
  - strategy
  - portfolio
  - optimization
domain: quant-finance
sources:
  - "[[Portfolio Optimization]]"
  - "[[Machine Learning for Asset Managers]]"
  - "[[Statistics and Data Analysis for Financial Engineering]]"
  - "[[Quantitative Risk Management]]"
---
# Portfolio Construction

## Summary

Portfolio construction converts forecasts, signals, or risk views into weights under real constraints. In this vault, it is not just optimization; it is the joint problem of estimation quality, risk control, turnover, diversification, and implementation.

## Source Synthesis

- [[Portfolio Optimization]] gives the broadest modern map, including mean-variance, robust portfolios, risk parity, graph-based portfolios, and backtesting.
- [[Machine Learning for Asset Managers]] emphasizes covariance cleaning, clustering, and test-set overfitting.
- [[Statistics and Data Analysis for Financial Engineering]] connects statistical estimation to portfolio and factor structure.
- [[Quantitative Risk Management]] adds tail, dependence, and aggregation awareness.

## Construction Layers

- forecast layer: expected returns, signals, or scores
- risk layer: covariance, tail, and scenario structure
- constraint layer: leverage, turnover, liquidity, sector, and benchmark limits
- implementation layer: execution, costs, and rebalance logic

## Common Portfolio Families

- mean-variance portfolios
- risk parity
- robust portfolios
- index-tracking portfolios
- graph-based portfolios
- pairs or relative-value portfolios

## Failure Modes

- optimizing on noisy expected returns
- underestimating covariance instability
- ignoring turnover and costs
- mistaking in-sample diversification for robust out-of-sample diversification
- using an elegant optimizer with weak signal design

## Related Notes

- [[Alpha Research]]
- [[Backtest Overfitting]]
- [[Financial Machine Learning Workflow]]

## Sources

- [[Portfolio Optimization]]
- [[Machine Learning for Asset Managers]]
- [[Statistics and Data Analysis for Financial Engineering]]
- [[Quantitative Risk Management]]
