---
title: QuantCode-Bench Plan
type: project
status: active
updated: 2026-04-23
tags:
  - project
  - benchmark
  - plan
  - backtrader
---
# QuantCode-Bench Plan

## Objective

Build a stable benchmark protocol that can answer:

> Does the knowledge base improve Codex's ability to generate executable algorithmic trading strategies?

The protocol has to separate three effects:

- raw model capability
- benchmark-specific prompt compliance
- actual help from the vault

## Benchmark layers to track

### 1. Official repo control

Run the benchmark as the repo authors designed it, with their generator prompt and their reward function.

Purpose:

- establish a control score for the underlying model or API setup
- verify that the repo and data cache work end to end

### 2. Vault-aware Codex benchmark

Use the same task dataset and the same reward function, but replace the stock generator with a Codex harness that can read the local vault.

Purpose:

- measure the actual effect of the knowledge base
- keep scoring fixed while changing the knowledge available to the agent

This second layer is the primary metric for the vault project.

## Recommended baseline protocol

### Fixed controls

Hold the following constant across reruns:

- benchmark repo version or commit
- dataset file
- judge setting
- max turns
- benchmark prompt wrapper
- market-data cache
- model version used for generation
- tool policy during evaluation

If any of these change, record it explicitly as a new regime rather than mixing it into the same score series.

### Core reported metrics

Always record:

- compilation rate
- backtest rate
- trade rate before judge
- judge pass rate
- by-difficulty breakdown
- average turns per task in agentic mode
- total wall-clock runtime

Track `total_return` only as a diagnostic field, not the primary benchmark score. The benchmark is designed around executable strategy generation, not return maximization.

### Two benchmark modes

For comparability, treat these as separate series:

1. single-shot
2. agentic

Do not merge them into one headline number. They answer different questions:

- single-shot tests first-pass competence
- agentic tests corrective workflow competence

## Practical rerun schedule

### Full benchmark

Run the full 400-task benchmark:

- at the first baseline
- after major vault milestones
- after major harness or model changes

### Shadow benchmark

For cheaper frequent checks, define a fixed stratified subset later, for example:

- balanced by difficulty
- mixed across timeframes
- mixed across equities, ETFs, crypto, and FX where possible

Use the same subset every time. This should become the quick regression test between major full runs.

## Baseline run sequence

### Phase A: benchmark control

1. install repo dependencies
2. build the yfinance cache
3. run official single-shot control
4. run official agentic control
5. store outputs under `artifacts/`

### Phase B: vault-aware baseline

1. create a Codex harness that reads one benchmark task at a time
2. allow local vault retrieval and local code execution only
3. forbid unrelated web search during evaluation
4. generate strategy code in the benchmark's required format
5. score it with the repo's reward function
6. aggregate the same official metrics

This Phase B score is the meaningful "knowledge base baseline."

## Why the harness matters

If we skip the vault-aware harness and only run the stock repo, then future score changes mostly reflect:

- model drift
- API differences
- benchmark prompt compatibility

That would not answer the user's actual question about whether the vault helps.

## Immediate next tasks

1. ingest Backtrader and QuantCode-Bench into stable notes if they become recurring benchmark infrastructure
2. install the benchmark repo dependencies locally
3. build the market-data cache
4. inspect the repo license and output format for artifact storage
5. implement the vault-aware baseline harness
6. run the first official control and first vault-aware baseline

## Open questions

- Should the judge remain enabled for all longitudinal comparisons, or should we track both `judge on` and `judge off` series?
- Should the vault-aware harness allow QMD and wiki only, or also `raw/` source reads during evaluation?
- How much benchmark-specific prompting is acceptable before we stop measuring knowledge and start measuring prompt engineering?
- Which fixed subset should become the recurring shadow benchmark after the first full run?
