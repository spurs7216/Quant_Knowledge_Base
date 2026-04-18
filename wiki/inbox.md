---
title: Wiki Inbox
type: system
status: seed
updated: 2026-04-18
tags:
  - inbox
  - ingest
  - system
---
# Wiki Inbox

Use this note to queue candidate sources and note targets before full ingest. Keep it shallow: list what to process next, not deep summaries.

## Candidate Sources

- [x] `[[raw/LLM Knowledge Bases/Thread by @karpathy]]` -> crystallized into [[LLM Knowledge Base Workflow]] and [[Karpathy LLM Knowledge Bases Thread]].
- [x] `[[raw/LLM Knowledge Bases/llm-wiki]]` -> crystallized into [[LLM Knowledge Base Workflow]] and [[LLM Wiki Gist]].
- [x] `[[raw/econometrics/Wooldridge - Cross-section and Panel Data.pdf]]` -> crystallized into [[Panel Data]] and [[Wooldridge Cross Section and Panel Data]].
- [x] `[[raw/math_statistics/Kalman filter.pdf]]` -> logged as [[Kalman Filter Tutorial]] and linked into the signal-processing shelf.
- [x] `[[raw/machine_learning/Financial Signal Processing and Machine Learning 2016.pdf]]` -> crystallized into [[Financial Signal Processing and Machine Learning]] and fed into [[Financial Machine Learning Workflow]].
- [x] `[[raw/quantitative_finance/Tulchinsky et al. 2020 (2E)- Finding Alphas.pdf]]` -> crystallized into [[Finding Alphas]] and [[Alpha Research]].
- [x] `[[raw/quantitative_finance/portfolio-optimization-book.pdf]]` -> crystallized into [[Portfolio Optimization]] and [[Portfolio Construction]].
- [x] `[[raw/finance_microstructure/Options, Futures, and Other Derivatives.pdf]]` -> crystallized into [[Derivatives Markets]] and [[Hull Options Futures and Other Derivatives]].
- [x] `[[raw/machine_learning/GraphSAGE with deep reinforcement learning for financial portfolio.pdf]]` -> added as [[GraphSAGE with Deep Reinforcement Learning for Financial Portfolio Optimization]].
- [x] `[[raw/machine_learning/Ensemble Methods in Data Mining - Improving Accuracy Through Combining Predictions 2010.pdf]]` -> added as [[Ensemble Methods in Data Mining]].
- [x] `[[raw/quantitative_finance/Financial risk manager handbook-Wiley (2003).pdf]]` -> added as [[Financial Risk Manager Handbook]].
- [x] `[[raw/math_statistics/2004 - wasserman - all of statistics.pdf]]` -> added as [[All of Statistics]].
- [x] `[[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]` -> added as [[Arbitrage Theory in Continuous Time]].
- [x] `[[raw/math_statistics/Boyd and Vandenberghe, Convex Optimization.pdf]]` -> added as [[Convex Optimization]].
- [x] `[[raw/math_statistics/Shumway and Stoffer, Time Series Analysis and Its Applications.pdf]]` -> added as [[Time Series Analysis and Its Applications]].
- [x] `[[raw/math_statistics/Simo Särkkä and Lennart Svensson, Bayesian Filtering and Smoothing.pdf]]` -> added as [[Bayesian Filtering and Smoothing]].
- [x] `[[raw/math_statistics/Steven E. Shreve-Stochastic Calculus for Finance II_20150303200346.pdf]]` -> added as [[Stochastic Calculus for Finance II]].
- [x] `[[raw/interview_questions/Crack - Heard on The Street (2021).pdf]]` -> added as [[Heard on the Street]].
- [x] `[[raw/interview_questions/a-practical-guide-to-quantitative-finance-interviews.pdf]]` -> added as [[A Practical Guide to Quantitative Finance Interviews]].
- [x] `[[raw/interview_questions/[Mark Joshi]Quant Job Interview Questions And Answers.pdf]]` -> added as [[Quant Job Interview Questions and Answers]].
- [x] `[[raw/books_cn/量化投资策略 如何实现超额收益Alpha.pdf]]` -> added as [[Quantitative Strategies for Achieving Alpha]].
- [ ] `[[raw/Target_from_quant_firm.png]]` -> source-registration note created as [[Target from Quant Firm]], but the image still needs manual visual review in Obsidian.

## Candidate Dataset Follow-ups

- [x] Add `ownership_13F` dataset documentation from the catalog mirror.
- [x] Add `option_volumne` dataset documentation and preserve the mirror spelling.
- [x] Add Treasury dataset notes and clarify exact date alignment for excess-return work.
- [ ] Add bridge notes for `permco`, `cik`, `linktype`, and `linkprim`.

## Current Deep-Ingest Batch

- [x] `raw/machine_learning/` core books ingested chapter by chapter into source notes.
- [x] `raw/quantitative_finance/` core books and primers ingested chapter by chapter or section by section into source notes.
- [x] `raw/math_statistics/` core books and tutorials ingested chapter by chapter or section by section into source notes.
- [x] `raw/interview_questions/` core prep books ingested as candidate-facing source notes.
- [x] Cross-source syntheses created for probabilistic ML, RL, financial ML workflow, Monte Carlo methods, portfolio construction, alpha research, HFT, and backtest overfitting.

## Intake Rule

When a candidate source is ingested:

1. Create or update the durable note in `wiki/`.
2. Add supporting links to `catalog/`, `projects/`, or `artifacts/` if relevant.
3. Move the completed item out of this queue or mark it done.
