---
title: Quant Research Eval Suite Brief
type: project
status: active
updated: 2026-04-23
tags:
  - project
  - benchmark
  - evaluation
  - quant
  - vault
---
# Quant Research Eval Suite Brief

## Goal

Design an evaluation system that can answer the real vault question:

> Does this knowledge base make Codex better at independent quantitative research, not just better at writing plausible code or attractive backtests?

The target capability is broader than "can it generate a strategy." A useful quant-research agent should be able to:

- understand mathematical and statistical structure
- translate research ideas into correct code and experiments
- reject weak or overfit ideas instead of forcing false positives
- validate ideas under realistic costs, constraints, and regime shifts
- produce research that remains reproducible and inspectable

## Why a single benchmark is not enough

### Backtest-only evaluation is too weak

A single strategy-generation benchmark can test implementation discipline, but it does not reliably test real research skill. A model can score well by learning framework quirks, benchmark prompt discipline, or shallow pattern matches.

### Project-only evaluation is too soft

A free-form "write a decent project" task is closer to real work, but it is too subjective to track longitudinally unless the tasks, budgets, hidden data, and rubric are fixed.

### QuantCode-Bench should stay, but only as one layer

[QuantCode-Bench](../quantcode_bench/brief.md) remains useful as an implementation and framework-translation subtest. It should not be treated as the headline measure of quant research.

## Design principles

- evaluate the full research funnel, not only the final backtest
- include hidden out-of-sample data and null tasks
- separate model-only performance from vault-assisted performance
- keep web lookup off during official evaluation runs
- use the same task sets, budgets, and scoring rules across reruns
- tag tasks by domain so post-ingest local lift can be measured honestly
- store enough evidence that every score remains inspectable later

## Proposed evaluation layers

### 1. Foundation layer

Measure whether the agent can correctly use mathematical, statistical, and financial concepts that should be improved by the vault.

### 2. Implementation layer

Measure whether the agent can convert a valid idea into correct, executable research or trading code under real framework constraints.

### 3. Research layer

Measure whether the agent can form hypotheses, design tests, diagnose flaws, and decide when an idea should be rejected.

### 4. Robustness layer

Measure whether the surviving ideas remain credible after costs, regime checks, and false-discovery controls.

### 5. Prospective layer

Measure whether the system can behave sensibly after the research memo is finished, for example in frozen paper-trading or shadow-live settings.

## What success should look like

The vault is working if, over time:

- domain-aligned ingest improves domain-aligned evaluation slices
- the agent becomes better at rejecting weak ideas
- implementation errors fall
- robustness standards rise instead of being bypassed
- prospective paper portfolios become more stable and less embarrassing

The vault is **not** working if the notes get richer but the agent still:

- confuses assumptions
- overclaims from noisy backtests
- misses basic coding or data-leakage errors
- cannot transfer knowledge into new research settings

## Sources

- https://github.com/LimexAILab/QuantCode-Bench
- https://arxiv.org/abs/2602.18481
- https://arxiv.org/abs/2508.00828
- https://metr.org/blog/2024-11-22-evaluating-r-d-capabilities-of-llms/
- https://metr.org/blog/2025-08-12-research-update-towards-reconciling-slowdown-with-time-horizons/
- https://ssrn.com/abstract=2326253
- https://ssrn.com/abstract=2460551
- https://ssrn.com/abstract=2513152
- https://ssrn.com/abstract=4778909
