---
title: Finding Alphas
type: source
status: chapter_ingested
updated: 2026-04-18
tags:
  - source
  - quant-finance
  - alpha-research
  - strategy
sources:
  - "[[raw/quantitative_finance/Tulchinsky et al. 2020 (2E)- Finding Alphas.pdf]]"
  - "[[raw/books_cn/寻找Alpha 量化交易策略(Tulchinsky).pdf]]"
---
# Finding Alphas

## Summary

This book is an alpha-research manual organized around alpha design, robustness, risk, automated search, machine learning, data sources, momentum, news, options, analyst reports, events, intraday research, ETFs, futures, and research process. The extracted contents show a practical institutional-style alpha workflow rather than a pure theory text.

## Chapter-by-Chapter Ingest

- `Chapter 1. Introduction to Alpha Design`: frames alpha research as a repeatable design problem.
- `Chapter 2. Perspectives on Alpha Research`: places alpha discovery in an institutional research context.
- `Chapter 3. Cutting Losses`: treats drawdown control and stop logic as part of the research problem.
- `Chapter 4. Alpha Design`: develops the logic of signal construction.
- `Chapter 5. How to Develop an Alpha: A Case Study`: gives an end-to-end worked alpha example.
- `Chapter 6. Data and Alpha Design`: ties signal design directly to data properties.
- `Chapter 7. Turnover`: treats trading frequency and implementation friction explicitly.
- `Chapter 8. Alpha Correlation`: studies diversification and signal overlap.
- `Chapter 9. Backtest – Signal or Overfitting?`: focuses directly on false discovery risk.
- `Chapter 10. Controlling Biases`: handles research bias and contamination.
- `Chapter 11. The Triple-Axis Plan`: gives a multi-dimensional framework for research control.
- `Chapter 12. Techniques for Improving the Robustness of Alphas`: studies stability improvements.
- `Chapter 13. Alpha and Risk Factors`: connects signals with factor exposures.
- `Chapter 14. Risk and Drawdowns`: studies downside behavior explicitly.
- `Chapter 15. Alphas from Automated Search`: uses structured search for signal discovery.
- `Chapter 16. Machine Learning in Alpha Research`: introduces ML as one alpha-discovery tool.
- `Chapter 17. Thinking in Algorithms`: pushes the reader toward algorithmic research habits.
- `Chapter 18. Equity Price and Volume`: mines standard market data for signals.
- `Chapter 19. Financial Statement Analysis`: uses accounting data in alpha design.
- `Chapter 20. Fundamental Analysis and Alpha Research`: expands the fundamental-signal layer.
- `Chapter 21. Introduction to Momentum Alphas`: studies trend-following and continuation effects.
- `Chapter 22. The Impact of News and Social Media on Stock Returns`: uses textual and event information.
- `Chapter 23. Stock Returns Information from the Stock Options Market`: mines option-implied information.
- `Chapter 24. Institutional Research 101: Analyst Reports`: studies analyst-data alpha inputs.
- `Chapter 25. Event-Driven Investing`: handles event-based alpha generation.
- `Chapter 26. Intraday Data in Alpha Research`: extends alpha mining to shorter horizons.
- `Chapter 27. Intraday Trading`: turns intraday signals into trading workflows.
- `Chapter 28. Finding an Index Alpha`: studies benchmark- or index-level opportunities.
- `Chapter 29. ETFs and Alpha Research`: handles ETF-based research contexts.
- `Chapter 30. Finding Alphas on Futures and Forwards`: expands beyond equities.
- `Chapter 31. Introduction to WebSim`: introduces a research platform and workflow layer.
- `Chapter 32. The Seven Habits of Highly Successful Quants`: closes with research culture and process discipline.

## Key Claims

- Alpha research is a process problem as much as an idea problem.
- Robustness, bias control, and turnover awareness determine whether a signal is real.
- Data-source diversity matters because different alphas live in different information channels.

## Methods and Data

- alpha design case studies
- robustness and bias controls
- risk-factor linkage and drawdown analysis
- automated search and machine learning
- price-volume, fundamentals, news, options, analyst, event, and intraday data

## Why It Matters Here

This is one of the strongest practical source notes for the factor and strategy side of the vault. It is especially useful for creating durable notes on alpha research, turnover, and robustness.

## Reflection

The best aspect of the book is that it treats alpha generation as a disciplined search process rather than a collection of disconnected anecdotes. That makes it highly compatible with a long-term quant knowledge base.

## Caveats

- The emphasis is practical and institutional rather than theorem-heavy.
- Some workflows assume access to proprietary infrastructure or data.
- The vault also contains a Chinese-language edition in `raw/books_cn/`, which is best understood as translation coverage rather than a separate source note.

## Related Notes

- [[Alpha Research]]
- [[Backtest Overfitting]]
- [[Portfolio Construction]]
- [[Financial Machine Learning Workflow]]

## Sources

- [[raw/quantitative_finance/Tulchinsky et al. 2020 (2E)- Finding Alphas.pdf]]
