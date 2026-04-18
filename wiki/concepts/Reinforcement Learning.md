---
title: Reinforcement Learning
type: model
status: seed
updated: 2026-04-18
tags:
  - model
  - machine-learning
  - reinforcement-learning
domain: quant-finance
sources:
  - "[[Foundations of Reinforcement Learning]]"
  - "[[Murphy Probabilistic Machine Learning]]"
---
# Reinforcement Learning

## Summary

Reinforcement learning is the study of sequential decision making under uncertainty, typically framed through Markov decision processes, Bellman equations, dynamic programming, function approximation, and exploration-exploitation tradeoffs. In this vault, it is relevant when the research problem is genuinely an action problem, not merely a prediction problem.

## Source Synthesis

- [[Foundations of Reinforcement Learning]] provides the main foundation: MDPs, dynamic programming, TD methods, policy gradients, bandits, and finance applications such as asset allocation, derivatives, and order-book trading.
- [[Murphy Probabilistic Machine Learning]] places RL inside a broader probabilistic decision-making framework.

## What It Does

- optimizes actions over time under uncertainty
- balances immediate reward with future value
- learns from interaction, simulation, or replayed experience
- links planning and learning through Bellman-style recursion

## Quant Use Cases

- dynamic asset allocation
- execution and order placement
- market making
- inventory management
- optimal stopping and hedging approximations

## When It Is Appropriate

- the state evolves through time
- actions affect future states or rewards
- delayed consequences matter materially
- the decision problem cannot be reduced to one-shot ranking or regression

## Failure Modes

- forcing RL onto a problem that is really supervised learning
- learning on unrealistic simulators and then overclaiming real-market validity
- ignoring market impact, latency, and partial observability
- confusing good cumulative reward in simulation with deployable trading performance

## Related Notes

- [[Probabilistic Machine Learning]]
- [[High-Frequency Trading]]
- [[Portfolio Construction]]
- [[Derivatives Markets]]

## Sources

- [[Foundations of Reinforcement Learning]]
- [[Murphy Probabilistic Machine Learning]]
