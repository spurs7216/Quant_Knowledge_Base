---
title: Strategy-to-IBKR Translation Smoke Test
type: project
status: active
updated: 2026-04-23
tags:
  - project
  - phase2b
  - ibkr
  - execution
  - smoke-test
---
# Strategy-to-IBKR Translation Smoke Test

## Purpose

Test whether the agent can translate research logic into broker-facing implementation artifacts without submitting orders.

This should happen early, before large candidate search. The goal is to catch strategy definitions that look valid in a backtest but are too vague, unsafe, or structurally impossible to express through IBKR.

Current infrastructure fact: IBKR TWS access exists only on the local machine. This smoke test is therefore a local-control-plane task, not a remote warehouse/GPU task.

## Boundary

Allowed:

- create target-position tables
- create target-delta tables
- create contract-resolution request tables
- create no-send order-intent JSON
- run static risk checks
- use local read-only IBKR metadata if available

Forbidden:

- require IBKR/TWS access on the remote machine
- submit paper orders
- submit live orders
- store credentials
- treat passing this task as alpha evidence

## First Task

Use Task 001 as the first strategy source, but do not attempt to trade the full 700-name long-short book.

Create a small representative target book that tests the translation mechanics:

- two long equity targets
- two short equity targets
- explicit dollar notional cap
- explicit rebalance date
- explicit order type
- explicit time-in-force
- explicit paper-account-only assumption

The target book may be synthetic if the purpose is implementation translation rather than alpha evaluation.

## Required Outputs

Store outputs under a project-specific Phase 2B folder when the task is run.

Required files:

- `strategy_spec.md`
- `target_portfolio.csv`
- `contract_resolution_requests.csv`
- `order_intents.json`
- `risk_check_report.md`
- `implementation_caveats.md`

If the task uses only static target-book and order-intent generation, it can be done without connecting to IBKR. If it uses account state, positions, contract metadata, or market-data requests from IBKR, it must run locally.

## Required Checks

The task fails if:

- account mode is missing
- a live account is allowed
- notional cap is missing
- quantity cap is missing
- order type is missing
- time-in-force is missing
- contract fields are ambiguous
- shorting assumptions are not stated
- no cancel or flattening plan exists
- the task assumes the remote machine has TWS access
- any credential appears in an output file
- an order-submission endpoint is called

## Interpretation

Passing this smoke test means:

- the strategy rule is specific enough to become broker-facing instructions
- the order intent is inspectable
- obvious safety gates exist

Passing this smoke test does not mean:

- the strategy is profitable
- the strategy should be paper traded
- IBKR order lifecycle competence has been proven

Full paper trading remains a later phase after stronger validation, risk controls, and account reconciliation infrastructure.

## Related Notes

- [IBKR Implementation Layer](ibkr_implementation_layer.md)
- [Quant Research System Build Sequence](build_sequence.md)
- [Quant Research System Environments](environments.md)
