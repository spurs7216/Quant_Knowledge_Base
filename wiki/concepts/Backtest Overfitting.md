---
title: Backtest Overfitting
type: risk
status: seed
updated: 2026-04-18
tags:
  - risk
  - backtesting
  - overfitting
domain: quant-finance
sources:
  - "[[Advances in Financial Machine Learning]]"
  - "[[Finding Alphas]]"
  - "[[Algorithmic Trading Winning Strategies and Their Rationale]]"
  - "[[Portfolio Optimization]]"
---
# Backtest Overfitting

## Summary

Backtest overfitting occurs when research choices are optimized to historical noise rather than persistent structure. In quant work it is one of the main ways a plausible-looking research process produces non-repeatable results.

## Source Synthesis

- [[Advances in Financial Machine Learning]] treats overfitting as a central workflow problem and emphasizes purged validation, embargoes, and synthetic-data checks.
- [[Finding Alphas]] focuses on bias control, robustness, and the distinction between true signal and historical accident.
- [[Algorithmic Trading Winning Strategies and Their Rationale]] stresses basic backtesting discipline and executable realism.
- [[Portfolio Optimization]] reminds us that portfolio design can overfit just as easily as signal design.

## Typical Causes

- repeated strategy search on the same historical sample
- leakage across folds or time
- overly flexible model classes with weak economic framing
- ignoring transaction costs, slippage, or borrowing frictions
- selecting parameters to maximize in-sample Sharpe without stability checks

## Diagnostics

- walk-forward and purged validation
- sensitivity to start and end dates
- turnover and cost stress tests
- exposure and correlation decomposition
- robustness to alternative data structures and label definitions

## Why It Matters

Backtest overfitting is not a minor hygiene issue. It is the main mechanism by which a large research library turns into a library of false positives.

## Related Notes

- [[Financial Machine Learning Workflow]]
- [[Alpha Research]]
- [[Portfolio Construction]]

## Sources

- [[Advances in Financial Machine Learning]]
- [[Finding Alphas]]
- [[Algorithmic Trading Winning Strategies and Their Rationale]]
- [[Portfolio Optimization]]
