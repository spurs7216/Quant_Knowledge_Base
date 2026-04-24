---
title: Phase 2 Falsification Task Bank v0
type: project
status: active
updated: 2026-04-23
tags:
  - project
  - phase2
  - task-bank
  - falsification
---
# Phase 2 Falsification Task Bank v0

## Scope

This is the first visible calibration bank for Phase 2.

The tasks are intentionally adversarial. The correct behavior is usually to reject, not to improve the story until it looks tradable.

## Task Table

| Task ID | Name | Data family | Expected decision | Primary trap | Required failure mode |
| --- | --- | --- | --- | --- | --- |
| `FAL-001` | Random-rank daily-stock null | `daily_stock` | `reject` | random cross-sectional ranks can still generate noisy attractive subperiods | statistical null failure |
| `FAL-002` | Same-day return leakage trap | `daily_stock` | `reject` | signal uses return information from the same day it claims to trade | leakage failure |
| `FAL-003` | Future survivorship universe trap | `daily_stock` | `reject` | universe uses future security status or end date | lookahead / survivorship failure |
| `FAL-004` | Static identifier artifact | `daily_stock` | `reject` | signal is a PERMNO or ticker hash with no economic mechanism | statistical and rationale failure |
| `FAL-005` | Microcap shorting implementation trap | `daily_stock` | `reject` or `revise` | high-turnover short book depends on hard-to-borrow, low-liquidity names | implementation-feasibility failure |

## FAL-001 Random-Rank Daily-Stock Null

Candidate:

- Use the same daily common-stock universe as Task 001.
- Each day, assign random ranks to eligible names.
- Long the top decile and short the bottom decile.
- Use the same gross exposure and baseline cost model as Task 001.

Correct reasoning:

- A random signal has no ex ante predictive content.
- Any attractive split is evidence about noise, multiple testing, and evaluator fragility.
- The result should be compared against random seeds and should not be promoted as alpha.

Expected decision: `reject`.

## FAL-002 Same-Day Return Leakage Trap

Candidate:

- Rank stocks using `DlyRetx_t` or another field only known after the close on date $t$.
- Claim the strategy earns date-$t$ returns from positions supposedly formed before or during date $t$.

Correct reasoning:

- The strategy uses information that is not available at decision time.
- Headline metrics are irrelevant after a timing gate fails.

Expected decision: `reject`.

## FAL-003 Future Survivorship Universe Trap

Candidate:

- Filter the historical universe using `SecurityActiveFlg == "Y"` or `SecurityEndDt` relative to the full-sample end date.
- Run a return or reversal rule only on names that survived to the end of the sample.

Correct reasoning:

- Full-sample survival is future information.
- Delisting and inactive names are part of the historical opportunity set and failure distribution.
- A backtest that removes future failures can overstate performance.

Expected decision: `reject`.

## FAL-004 Static Identifier Artifact

Candidate:

- Use `PERMNO % k`, ticker lexical rank, or a hash of an identifier as a cross-sectional signal.
- Backtest the signal as if it were a meaningful factor.

Correct reasoning:

- A static identifier is not an economic state variable by itself.
- Any measured spread is likely an artifact of listing era, exchange, size, sector, or sample composition.
- It requires strong null comparison and exposure controls before any interpretation.

Expected decision: `reject`.

## FAL-005 Microcap Shorting Implementation Trap

Candidate:

- Form a high-turnover long-short book where the short leg concentrates in low-price, low-volume, hard-to-borrow names.
- Ignore locate availability, borrow fees, price impact, and position caps.

Correct reasoning:

- The backtest may be arithmetically valid but implementation-incomplete.
- A strategy whose economics depend on unavailable shorts or unrealistic capacity cannot proceed as alpha.
- The right answer is `reject` or `revise` until borrow, capacity, and orderability are specified.
- The remote machine can flag this from warehouse proxies, but actual IBKR/TWS feasibility checks must run locally because TWS access is local-only.

Expected decision: `reject` for an alpha claim; `revise` only if the task is explicitly reframed as a feasibility study.

## Versioning

Task bank version: `phase2_falsification_v0`.

This bank is visible. Hidden benchmark tasks should not be derived by trivial renaming only; they should preserve the same failure categories while changing the surface form.

## Related Notes

- [Evaluator Checklist](evaluator_checklist.md)
- [Task 001 Daily-Stock Falsification Suite](task_001_daily_stock_falsification_suite.md)
