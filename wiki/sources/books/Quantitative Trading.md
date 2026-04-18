---
title: Quantitative Trading
type: source
status: chapter_ingested
updated: 2026-04-18
tags:
  - source
  - quant-finance
  - trading
  - microstructure
sources:
  - "[[raw/quantitative_finance/Quantitative trading _.pdf]]"
---
# Quantitative Trading

## Summary

This book organizes quantitative trading around statistical models, active portfolio management, transaction econometrics, limit-order-book analytics, execution, market making, routing, informatics, regulation, and risk management. The extracted contents show a market-structure-aware trading text rather than a pure signal-mining book.

## Chapter-by-Chapter Ingest

- `Chapter 1. Introduction`: frames the purpose and scope of quantitative trading.
- `Chapter 2. Statistical Models and Methods for Quantitative Trading`: provides the main statistical toolkit for strategy development.
- `Chapter 3. Active Portfolio Management and Investment Strategies`: connects modeling to portfolio-level decisions.
- `Chapter 4. Econometrics of Transactions in Electronic Platforms`: studies transaction-level behavior in electronic markets.
- `Chapter 5. Limit Order Book: Data Analytics and Dynamic Models`: treats the order book as a dynamic stochastic object.
- `Chapter 6. Optimal Execution and Placement`: focuses on execution control in electronic markets.
- `Chapter 7. Market Making and Smart Order Routing`: develops dealer-style and routing logic.
- `Chapter 8. Informatics, Regulation and Risk Management`: closes by tying the trading stack to governance and controls.

## Key Claims

- Transaction-level econometrics and order-book dynamics are central to modern trading.
- Portfolio ideas, execution, routing, and market making are linked layers of the same system.
- Regulation and risk management are part of the trading design problem.

## Methods and Data

- statistical trading models
- transaction econometrics
- order-book analytics
- optimal execution and routing
- market making and risk controls

## Why It Matters Here

This is a strong source for the intraday and execution side of the vault, especially when paired with Aldridge and the RL finance book.

## Reflection

The main value here is the explicit link between statistical modeling and the microstructure layer. That helps prevent the common mistake of treating alpha and execution as independent.

## Caveats

- The book spans multiple subfields, so each one should eventually be expanded into its own wiki notes.

## Related Notes

- [[High-Frequency Trading]]
- [[Portfolio Construction]]
- [[Reinforcement Learning]]

## Sources

- [[raw/quantitative_finance/Quantitative trading _.pdf]]
