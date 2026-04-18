---
title: Algorithmic Trading Winning Strategies and Their Rationale
type: source
status: chapter_ingested
updated: 2026-04-18
tags:
  - source
  - quant-finance
  - trading
  - strategy
sources:
  - "[[raw/quantitative_finance/Algorithmic Trading - Winning Strategies and Their Rationale 2013.pdf]]"
  - "[[raw/books_cn/算法交易 制胜策略与原理.pdf]]"
---
# Algorithmic Trading Winning Strategies and Their Rationale

## Summary

Chan's book is a concise strategy-oriented text centered on backtesting, automated execution, mean reversion, momentum, and risk management. The extracted contents show a practical trading-research manual focused on tradable ideas rather than broad market theory.

## Chapter-by-Chapter Ingest

- `Chapter 1. Backtesting and Automated Execution`: frames research quality through backtesting discipline and executable implementation.
- `Chapter 2. The Basics of Mean Reversion`: develops the intuition and tests behind mean-reverting opportunities.
- `Chapter 3. Implementing Mean Reversion Strategies`: turns the concept into actual portfolio constructions.
- `Chapter 4. Mean Reversion of Stocks and ETFs`: applies reversion ideas to equity and ETF settings.
- `Chapter 5. Mean Reversion of Currencies and Futures`: extends the framework to other liquid asset classes.
- `Chapter 6. Interday Momentum Strategies`: studies slower momentum effects.
- `Chapter 7. Intraday Momentum Strategies`: shifts momentum thinking into shorter-horizon execution.
- `Chapter 8. Risk Management`: closes by embedding the strategies inside sizing and risk controls.

## Key Claims

- A simple, well-tested strategy can be more valuable than a complex but weakly validated one.
- Mean reversion and momentum require different research assumptions and holding-period logic.
- Execution realism is part of the strategy, not an implementation afterthought.

## Methods and Data

- backtesting and hypothesis testing
- mean-reversion and momentum strategies
- execution logic
- portfolio sizing and risk management

## Why It Matters Here

This source is useful for the strategy layer of the vault because it connects simple quantitative ideas directly to tradable workflows and risk control.

## Reflection

The main value here is not sophistication but discipline. The book keeps bringing the discussion back to whether a strategy survives basic testing, implementation, and risk controls.

## Caveats

- The emphasis is on practical strategy sketches, not on a full statistical theory of inference.
- The examples reflect a discretionary-practitioner style rather than a fully institutional research process.
- The vault also contains a Chinese-language edition in `raw/books_cn/`, which should be treated as an alternate edition of the same work.

## Related Notes

- [[Alpha Research]]
- [[Backtest Overfitting]]
- [[Portfolio Construction]]

## Sources

- [[raw/quantitative_finance/Algorithmic Trading - Winning Strategies and Their Rationale 2013.pdf]]
