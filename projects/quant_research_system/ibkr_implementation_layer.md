---
title: IBKR Implementation Layer
type: project
status: active
updated: 2026-04-23
tags:
  - project
  - ibkr
  - implementation
  - execution
  - paper-trading
---
# IBKR Implementation Layer

## Role

IBKR should evaluate execution-facing implementation skill, not alpha discovery.

Current infrastructure fact: IBKR TWS access exists only on the local machine. The remote Linux/GPU machine is for data and compute work, not broker-facing tasks.

The agent's implementation skill should be tested at two levels:

- early no-send translation: can the agent turn a strategy rule into target positions, contract-resolution requests, order intents, and static risk checks?
- later paper execution: can the agent manage account state, order submission, cancellation, fills, and reconciliation in a paper account?

The first level should be examined early because it catches non-implementable research logic. The second level should wait until a strategy survives historical validation and safety gates.

## Why IBKR improves the implementation layer

Backtrader is useful as a cheap framework-coding subtest, but it is not realistic enough to be the main implementation exam.

IBKR is better for testing:

- contract resolution
- market-data request discipline
- order object construction
- account and position reconciliation
- paper-trading safety
- live-system failure handling

## Current tool state

The current IBKR MCP surface is read-only:

- historical market data
- fundamental data
- account summary
- positions

That is enough for read-only checks, but not enough for a full execution benchmark.

A full implementation layer needs a local harness around one of:

- TWS API / IB Gateway
- IBKR Client Portal Web API

Do not assign IBKR/TWS tasks to the remote machine. Remote jobs can produce historical feasibility evidence, such as turnover, liquidity, short-side concentration, and candidate target books, but local tooling must handle account state, positions, contract metadata, order construction against broker constraints, dry-runs, and paper order lifecycle checks.

## Safety hierarchy

Use four stages:

1. `read_only`
   Inspect account, positions, contract metadata, and historical data.
2. `dry_run`
   Construct orders and validate risk rules without sending them.
3. `paper_trade`
   Submit orders only to a paper account under strict limits.
4. `live_trade`
   Out of scope unless the human explicitly approves a separate live-trading protocol.

All four stages are local-only under the current setup. Remote compute may support them with data artifacts, but it is not an IBKR execution host.

## Early strategy-to-order smoke test

This belongs near Phase 2B, before large candidate search.

Purpose:

- check whether a strategy specification has enough detail to become broker-facing logic
- expose missing assumptions about target sizing, rebalance timing, instruments, shorting, order type, and risk limits
- produce reviewable artifacts without connecting to an order-submission endpoint
- run locally if any IBKR/TWS metadata, account state, or position state is needed

Required no-send outputs:

- target portfolio or target-delta table
- contract-resolution request table
- order-intent JSON with explicit `paper_account_required` and no-send semantics such as `transmit=false`
- static risk-check report
- implementation caveat report

Failure gates:

- attempting to use the remote machine for IBKR/TWS access under the current setup
- missing account mode
- missing notional and quantity caps
- ambiguous contract fields
- no cancel or flattening plan
- use of live-order submission
- credentials written to the vault
- strategy requires instruments or shorting assumptions not supported by the declared account constraints

This smoke test does not prove alpha and does not prove paper-execution competence. It only proves that the research logic is specific enough to be translated into broker-facing artifacts.

## Execution evaluator cascade

### Stage 1. Static safety

Checks:

- no live-trading flag
- account target is paper
- max order size set
- max notional set
- cancel path exists
- no credentials are written to the vault

### Stage 2. Contract resolution

Checks:

- symbol maps to intended instrument
- exchange, currency, and security type are explicit
- ambiguous contracts are rejected
- options include expiry, strike, right, and multiplier when relevant

### Stage 3. Market-data discipline

Checks:

- request type is explicit
- bar size and duration are compatible
- pacing limits are respected
- missing or delayed data are handled

### Stage 4. Order construction

Checks:

- order side, quantity, type, time-in-force, and limit fields are explicit
- risk checks run before order submission
- generated order can be serialized or logged without secrets

### Stage 5. Paper submission

Checks:

- order submitted to paper account only
- order id lifecycle is tracked
- open order and status events are recorded
- rejected orders produce useful diagnostics

### Stage 6. Reconciliation

Checks:

- fills match expected order state
- positions update as expected
- cash and buying power are inspected
- cancellation or flattening path works

## Evaluation tasks

Initial task bank:

- resolve and inspect AAPL stock contract
- request recent historical data for SPY and detect missing bars
- construct a paper limit order under a notional cap
- cancel an unfilled paper order
- reconcile paper positions after a fill
- reject an ambiguous option contract
- generate a trade blotter artifact from paper events

## What counts as success

An implementation task passes only if:

- it uses a paper account or read-only mode
- it records the requested lifecycle evidence
- it handles failure modes explicitly
- it leaves the system in a safe state

Profit is not the point of this layer. Correctness, safety, and reconciliation are.

## Sources

- https://interactivebrokers.github.io/tws-api/order_submission.html
- https://interactivebrokers.github.io/tws-api/historical_limitations.html
- https://ibkrcampus.com/campus/ibkr-api-page/webapi-doc/
