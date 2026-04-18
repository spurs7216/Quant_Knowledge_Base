---
title: High-Frequency Trading
type: market
status: seed
updated: 2026-04-18
tags:
  - market
  - microstructure
  - execution
  - hft
domain: quant-finance
sources:
  - "[[Aldridge High-Frequency Trading]]"
  - "[[Quantitative Trading]]"
  - "[[Foundations of Reinforcement Learning]]"
---
# High-Frequency Trading

## Summary

High-frequency trading is a microstructure-intensive trading regime where market design, order-book dynamics, execution logic, systems engineering, and risk controls are inseparable. In this vault it sits at the intersection of market structure, intraday modeling, and sequential decision making.

## Source Synthesis

- [[Aldridge High-Frequency Trading]] provides the practical market-structure and systems foundation.
- [[Quantitative Trading]] adds transaction econometrics, order-book modeling, routing, and execution control.
- [[Foundations of Reinforcement Learning]] contributes the control and decision-theoretic view for order placement and market making.

## Core Components

- fragmented electronic markets
- limit-order-book dynamics
- high-frequency data engineering
- execution-cost and impact modeling
- market making and inventory control
- routing, latency, and system design

## Why It Matters

- alpha quality at high frequency is inseparable from implementation quality
- market impact and fill uncertainty can dominate raw forecast strength
- operational risk is unusually important because systems act at machine timescales

## Failure Modes

- treating order-book data as if it were clean bar data
- ignoring queue position and routing
- overclaiming backtest performance without execution realism
- underestimating operational, regulatory, and manipulation-related risks

## Related Notes

- [[Reinforcement Learning]]
- [[Derivatives Markets]]
- [[Backtest Overfitting]]

## Sources

- [[Aldridge High-Frequency Trading]]
- [[Quantitative Trading]]
- [[Foundations of Reinforcement Learning]]
