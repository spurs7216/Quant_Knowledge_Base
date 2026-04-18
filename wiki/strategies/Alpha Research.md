---
title: Alpha Research
type: factor
status: seed
updated: 2026-04-18
tags:
  - factor
  - alpha
  - strategy-research
domain: quant-finance
sources:
  - "[[Finding Alphas]]"
  - "[[Advances in Financial Machine Learning]]"
  - "[[Algorithmic Trading Winning Strategies and Their Rationale]]"
  - "[[Causality and Factor Investing A Primer]]"
---
# Alpha Research

## Summary

Alpha research is the process of proposing, testing, interpreting, and governing a return-generating hypothesis. In this vault it includes signal design, data choice, horizon logic, turnover, validation, risk attribution, and causal caution.

## Source Synthesis

- [[Finding Alphas]] provides the most direct institutional alpha-design workflow.
- [[Advances in Financial Machine Learning]] supplies the labeling, weighting, validation, and robustness logic.
- [[Algorithmic Trading Winning Strategies and Their Rationale]] keeps the focus on tradable strategy forms such as mean reversion and momentum.
- [[Causality and Factor Investing A Primer]] adds the warning that prediction and factor association are not the same as causal understanding.

## Research Questions

- what information edge is being exploited
- why should the edge persist
- what horizon and implementation path does it require
- how much of the result is exposure versus true idiosyncratic signal
- is the result predictive, causal, or merely descriptive

## Common Inputs

- price and volume
- fundamentals
- options and implied information
- news, events, and analyst reports
- intraday and order-book features

## Failure Modes

- signal duplication disguised as novelty
- hidden factor bets mistaken for alpha
- overfitting through repeated backtest search
- ignoring turnover and execution cost
- inferring causality from correlation alone

## Related Notes

- [[Financial Machine Learning Workflow]]
- [[Backtest Overfitting]]
- [[Portfolio Construction]]

## Sources

- [[Finding Alphas]]
- [[Advances in Financial Machine Learning]]
- [[Algorithmic Trading Winning Strategies and Their Rationale]]
- [[Causality and Factor Investing A Primer]]
