---
title: Phase 2 Falsification Evaluator Checklist
type: project
status: active
updated: 2026-04-23
tags:
  - project
  - phase2
  - evaluator
  - falsification
---
# Phase 2 Falsification Evaluator Checklist

## Required Decision Rule

Every task must end with one of:

- `reject`
- `revise`
- `proceed`

The memo must state what evidence would change the decision. A task cannot pass because the story sounds plausible.

## Claim Extraction

Before looking at performance, extract:

- proposed signal or strategy rule
- decision time and return realization time
- data fields used by the signal
- universe definition
- cost, borrow, slippage, and capacity assumptions
- intended implementation path if the strategy is meant to trade

## Hard Failure Gates

Any of these is enough for `reject` unless the task explicitly asks for repair rather than evaluation:

- same-day or future return enters a signal that is claimed to be tradable before that return is known
- future security status, delisting status, or full-sample survival is used to form a historical universe
- identifiers are silently changed across time without a join policy
- train / validation / test boundaries are crossed during model or parameter selection
- transaction costs are omitted for high-turnover strategies
- short-side strategy ignores borrow, locate, or hard-to-borrow constraints when shorts are load-bearing
- strategy cannot be mapped to broker-facing instruments or order intents under the stated constraints

## Statistical Checks

For any task that is not rejected by a hard gate, require:

- explicit null model
- chronological split or justified validation design
- comparison against a random or permuted baseline when applicable
- subperiod and regime diagnostics
- cost sensitivity when turnover is material
- exposure checks for market, size, liquidity, sector, or exchange when applicable

## Implementation Feasibility Checks

IBKR/TWS access exists only on the local machine. Remote Phase 2 jobs may flag implementation concerns from historical data, but they cannot verify account state, positions, broker contract metadata, or order lifecycle behavior.

For any strategy-like task, check:

- tradable instrument definition
- identifier-to-contract resolution path
- rebalance cadence and order timing
- maximum position size and notional cap
- liquidity and capacity estimate
- short-sale and borrow assumption
- order type, time-in-force, and no-send or paper-only safety status

An idea can fail Phase 2 even if the backtest arithmetic is correct.

If broker-facing verification is needed, route it to the local `implementation_translation_smoke` or later local IBKR environment. Do not assign it to the remote data/GPU machine.

## Scoring

Record these fields at minimum:

- `task_id`
- `expected_decision`
- `agent_decision`
- `decision_correct`
- `false_accept`
- `statistical_gate`
- `leakage_gate`
- `implementation_gate`
- `primary_failure_reason`
- `evidence_path`

Null-discipline score:

$$
S_{\text{null}} = 100\left(1 - \frac{N_{\text{false accept}}}{N_{\text{reject-expected tasks}}}\right).
$$

Do not let a good-looking Sharpe override a failed hard gate.

## Memo Standard

The final memo should separate:

- evidence
- speculation
- design defects
- implementation defects
- final decision

If the task is rejected, the failure reason should still be useful for future task design.

## Related Notes

- [Phase 2 README](README.md)
- [Task Bank v0](task_bank_v0.md)
- [Quant Research Eval Suite Scorecard](../../quant_research_eval/scorecard.md)
