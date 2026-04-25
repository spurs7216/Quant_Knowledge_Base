---
title: Phase 2B Task 001 Representative Book Translation
type: project
status: completed
updated: 2026-04-24
tags:
  - project
  - phase2b
  - implementation
  - ibkr
  - no-send
sources:
  - "../execution_translation_smoke_test.md"
  - "../ibkr_implementation_layer.md"
  - "../phase1_remote_validation/task_001_daily_stock_short_reversal.md"
  - "../phase1_remote_validation/task_001_decision.md"
---
# Phase 2B Task 001 Representative Book Translation

## Objective

Translate the Phase 1 daily long-short reversal rule into a small representative broker-facing target book without submitting orders.

This task is intentionally narrower than real execution:

- two longs
- two shorts
- explicit gross cap
- explicit quantity cap
- explicit no-send order intents
- explicit paper-only assumption

## Source Strategy

The research source is [Task 001 Daily Stock Short-Horizon Reversal](../phase1_remote_validation/task_001_daily_stock_short_reversal.md).

The Phase 1 decision was `revise`, not `proceed`, so this task does **not** treat the strategy as production-ready alpha. It only tests whether the strategy logic is specific enough to become inspectable broker-facing artifacts.

## Translation Choice

The representative book is synthetic and implementation-oriented.

Chosen names:

- long: `AAPL`, `MSFT`
- short: `NVDA`, `TSLA`

These names are used because they are liquid, common US single-name equity contracts that keep the translation mechanics easy to inspect.

## Output Bundle

Artifact root:

`artifacts/implementation_translation_smoke/20260424_task001_representative_book_translation/`

Required files:

- `strategy_spec.md`
- `target_portfolio.csv`
- `contract_resolution_requests.csv`
- `order_intents.json`
- `risk_check_report.md`
- `implementation_caveats.md`
- `run_manifest.yaml`

## Local IBKR Boundary

This first task is allowed to run without connecting to IBKR/TWS because it only generates static no-send artifacts.

Later phases should add:

- live contract lookup
- dry-run broker validation
- paper-account lifecycle checks

## Related Notes

- [Phase 2B Implementation Translation](README.md)
- [Task 001 Local Review](task_001_local_review.md)
