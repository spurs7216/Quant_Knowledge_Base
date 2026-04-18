---
title: Aldridge High-Frequency Trading
type: source
status: chapter_ingested
updated: 2026-04-18
tags:
  - source
  - quant-finance
  - microstructure
  - high-frequency-trading
sources:
  - "[[raw/quantitative_finance/Aldridge 2013 - High-frequency Trading.pdf]]"
  - "[[raw/books_cn/高频交易(Aldridge).pdf]]"
---
# Aldridge High-Frequency Trading

## Summary

Aldridge's book is a practical HFT text organized around modern markets, technology, order books, high-frequency data, execution costs, performance, market making, event trading, regulation, risk, and implementation. The extracted contents show a market-microstructure-and-systems view of HFT rather than a narrow alpha-only view.

## Chapter-by-Chapter Ingest

- `Chapter 1. How Modern Markets Differ from Those Past`: explains why automation, fragmentation, and electronic structure changed trading itself.
- `Chapter 2. Technological Innovations, Systems, and HFT`: treats hardware, messaging, and software as strategy prerequisites.
- `Chapter 3. Market Microstructure, Orders, and Limit Order Books`: builds the order-book and market-fragmentation foundation.
- `Chapter 4. High-Frequency Data`: studies the properties and pathologies of high-frequency market data.
- `Chapter 5. Trading Costs`: focuses on transparent and implicit execution costs and market impact.
- `Chapter 6. Performance and Capacity of High-Frequency Trading Strategies`: evaluates capacity, attribution, and performance decay.
- `Chapter 7. The Business of High-Frequency Trading`: places HFT inside market economics and firm organization.
- `Chapter 8. Statistical Arbitrage Strategies`: develops stat-arb as one major HFT family.
- `Chapter 9. Directional Trading Around Events`: handles event-based forecasting and trading.
- `Chapter 10. Automated Market Making—Naive Inventory Models`: introduces inventory-aware market making.
- `Chapter 11. Automated Market Making II`: deepens order-flow and information modeling for quoting.
- `Chapter 12. Additional HFT Strategies, Market Manipulation, and Market Crashes`: studies both legitimate and abusive tactics under market stress.
- `Chapter 13. Regulation`: surveys regulatory responses to HFT.
- `Chapter 14. Risk Management of HFT`: treats operational and market risk as first-class.
- `Chapter 15. Minimizing Market Impact`: studies slicing, routing, and execution algorithms.
- `Chapter 16. Implementation of HFT Systems`: closes with development, testing, and system deployment.

## Key Claims

- HFT is inseparable from market structure, data engineering, and execution costs.
- Order-book dynamics and fragmentation matter as much as forecasting.
- Risk management and implementation discipline are central, not peripheral.

## Methods and Data

- order-book modeling
- high-frequency data diagnostics
- execution-cost and market-impact estimation
- event-driven trading and market making
- capacity analysis and implementation workflows

## Why It Matters Here

This is a core source for the execution and microstructure side of the vault. It is especially valuable for understanding why high-frequency strategies cannot be reduced to signal generation alone.

## Reflection

The strongest lesson here is that HFT is a joint problem in markets, systems, and risk. Any quant agent that wants to discuss intraday strategies seriously needs this broader framing.

## Caveats

- Some strategy discussions are practical sketches rather than reproducible research pipelines.
- The market structure reflects the early-2010s environment and should be read with historical awareness.
- The vault also contains a Chinese-language edition in `raw/books_cn/`, which is an alternate edition rather than a separate intellectual source.

## Related Notes

- [[High-Frequency Trading]]
- [[Derivatives Markets]]
- [[Backtest Overfitting]]

## Sources

- [[raw/quantitative_finance/Aldridge 2013 - High-frequency Trading.pdf]]
