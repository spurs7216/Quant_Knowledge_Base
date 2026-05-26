---
title: Phase 4 Caveat Repair Ledger
type: project_ledger
status: active
updated: 2026-05-26
tags:
  - project
  - phase4
  - caveats
  - alphaevolve
sources:
  - "current_state.md"
  - "daily_stock_expression_evolution_v1.md"
  - "phase4_sampling_policy_v1.md"
  - "alphaevolve_method_translation.md"
---
# Phase 4 Caveat Repair Ledger

This ledger records plan-level caveats that can derail Phase 4 if they stay only in conversation memory.

## Status Table

| Issue | Risk | Current repair | Remaining caveat |
| --- | --- | --- | --- |
| Attempt017 became too central | Overfit engineering effort to one modest branch | Expression episodes now use multiple root seeds and branch stop-loss enforcement from population records | Historical attempt017 notes remain useful evidence, but should not drive the next expression run |
| Multi-turn but not generational | Turns rewrite the same seed rather than evolving survivors | `population_mixed` samples eligible child survivors; prior population ledgers can seed later episodes | Full island scheduling remains later than the first expression pilot |
| No persistent expression population database | Search memory dies after one artifact | Expression episodes now write JSONL/CSV plus `expression_population.sqlite`, and can reload prior ledgers | This is an expression-population store, not yet the full executable-program SQLite database |
| Expression-only search may miss turnover/cost solution | Fixed daily top/bottom bridge may hide lower-turnover ideas | Runner now writes bridge-variant diagnostics, and `run_expression_bridge_followup.py` promotes bridge choice into an explicit parent-vs-child evaluation contract | Bridge follow-up evidence can justify strategy conversion only; it is not promotion or full validation |
| OS overuse risk | Repeated Qwen loops can overfit 2023-2025 development OS | Population records carry validation-exposure fields, and `expression_population_summary.json` reports development-OS and final-test exposure counts | A final untouched test interval is still undefined and must remain unused until branch freeze |
| Pass@T threshold underdefined | "Beats parent" can pass economically weak children | Runner now writes explicit success flags: parent/root beat, positive after cost, positive IS/OS, broad coverage, sparse/null/duplicate checks | Promotion still requires later reviewed strategy-program conversion and stronger validation |

## Operating Rule

Before any new remote generation run, check this file and `current_state.md`.

If a caveat is closed by code, record the file and artifact contract that closes it. If it is not closed, it must appear in the remote instruction as an explicit review question or stop condition.

## Current Remote Implication

The next remote action should be deterministic bridge-policy follow-up, not another expression episode:

- run `run_expression_bridge_followup.py`;
- not call Qwen or vLLM;
- compare `expr_smoothed_rev` and the liquidity-gated child under the same `daily`, `rebalance_5`, and `signal_decay_5` bridge contracts;
- return `expression_bridge_followup_summary.json`, `expression_bridge_followup_comparison.csv`, `expression_bridge_followup_scorecard.csv`, and cost-sensitivity artifacts;
- treat 2023-2025 OS as development feedback only;
- avoid promotion or full validation.
