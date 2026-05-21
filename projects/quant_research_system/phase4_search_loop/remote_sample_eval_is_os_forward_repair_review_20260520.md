---
title: Remote Sample Eval IS/OS Forward-Repair Review 2026-05-20
type: project
status: reviewed
updated: 2026-05-21
tags:
  - project
  - phase4
  - alphaevolve
  - sample-eval
  - is-os
sources:
  - "../../artifacts/remote_sample_eval_(1).zip"
  - "remote_sample_eval_is_os_forward_repair_rerun_20260519.md"
  - "evaluator_forward_return_contract_repair_20260519.md"
  - "is_os_evaluation_policy_20260519.md"
---
# Remote Sample Eval IS/OS Forward-Repair Review 2026-05-20

## Artifact Integrity

The useful artifact is `artifacts/remote_sample_eval_(1).zip`. The similarly named `artifacts/remote_sample_eval_.zip` is a zero-byte corrupt placeholder and should be ignored.

All six completed evaluator runs were reproducible from GitHub:

```yaml
git_commit: 82a524fd6b0903588367b6d3b1b656adb4cbadc8
git_origin_main_commit: 82a524fd6b0903588367b6d3b1b656adb4cbadc8
git_head_matches_origin_main: true
git_dirty: false
split_id: daily_stock_top500_is_2011_2022_os_2023_2025_v1
forward_return_source: eligible_static_panel
forward_return_contract: signal_universe_t_return_source_eligible_t_plus_1_v1
rows_after_static_eligibility: 14754079
universe_rows: 1862834
visible_universe_days: 3730
portfolio_days: 3690
portfolio_day_coverage: 0.9892761394101877
```

This means the rerun answered the intended evaluator question: old attempt017 evidence has now been remeasured under the repaired forward-return source and fixed 2011-2025 IS/OS split.

## Result Table

| Program | Decision | IS Sharpe | OS Sharpe | Search Sharpe | Search return | Turnover | Max missing | Max weight | Score |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `PROG-20260430-CHILD-0017-ISOSREPAIR` | `sample_pass` | 0.1589 | 0.5061 | 0.2244 | 0.0197 | 0.5602 | 0.0104 | 0.0104 | 0.0322 |
| `PROG-20260513-A017-MECH-0007` | `sample_pass` | 0.2191 | 0.1792 | 0.2111 | 0.0208 | 0.5302 | 0.0200 | 0.0104 | -0.0215 |
| `PROG-20260514-A017-27BCARD-0011` | `sample_pass` | -0.0307 | 0.0651 | -0.0108 | -0.0004 | 0.3370 | 0.0302 | 0.0102 | -0.2459 |
| `PROG-20260514-A017-MECHFIX-0009` | `sample_pass` | -0.0307 | 0.0651 | -0.0108 | -0.0004 | 0.3370 | 0.0302 | 0.0102 | -0.2459 |
| `PROG-20260511-A017-FOCUS-0000` | `sample_pass` | -1.2228 | -1.5628 | -1.2920 | -0.0578 | 1.0330 | 0.0104 | 0.0104 | -1.6023 |
| `PROG-20260430-000000` | `sample_pass` | -1.3701 | -0.3332 | -1.1553 | -0.0935 | 1.7950 | 0.0400 | 0.0104 | -1.8041 |

`Score` is the evaluator's turnover-aware search-sample score.

## Interpretation

Attempt017 remains the active parent lead. It is the only evaluated child with clearly positive OS Sharpe and positive turnover-aware score under the repaired 2011-2025 sample contract. Its old missing-held-weight problem was mostly an evaluator artifact: max missing held weight fell from the old 0.12 concern to about 0.0104.

This is not a promotion. `sample_pass` means hard gates passed, not that the strategy is validated. The search sample still includes the development OS window, and test-set use remains forbidden until a branch is frozen.

The active objective has changed. We should no longer ask Qwen to repair missing-held weight for attempt017. The useful next search problem is:

```yaml
parent_lead: PROG-20260430-CHILD-0017-ISOSREPAIR
objective: preserve attempt017 OS strength while improving IS robustness and cost sensitivity
preferred_surfaces:
  - portfolio/persistence_trade_gate
  - portfolio/no_trade_band_or_sparsity
  - portfolio/liquidity_weighted_sides
  - risk/liquidity_scaled_cap
deemphasized:
  - ranking/industry_neutral_rank
  - generic signal dampening
```

`PROG-20260513-A017-MECH-0007` is useful as a reference but not as the parent lead. It has slightly better IS Sharpe and lower turnover than attempt017, but weaker OS Sharpe and weaker turnover-aware score.

`PROG-20260514-A017-MECHFIX-0009` and `PROG-20260514-A017-27BCARD-0011` produced identical sample metrics despite different program hashes. Treat this as metric-equivalent sibling replay until proven otherwise. Future optional sample evaluations must compare against all relevant sibling summaries, not only the seed or parent.

`PROG-20260511-A017-FOCUS-0000` should be demoted as a search direction. It fixed missing-held behavior but failed parent-relative economics badly.

## Cost Sensitivity

Attempt017 remains cost-fragile:

| Total cost bps | Search Sharpe | Turnover-aware score |
| ---: | ---: | ---: |
| 0.0 | 0.6258 | 0.4336 |
| 1.0 | 0.4652 | 0.2730 |
| 2.5 | 0.2244 | 0.0322 |
| 5.0 | -0.1768 | -0.3689 |
| 10.0 | -0.9782 | -1.1703 |

That profile argues for turnover and execution-shape mechanisms before more signal-side novelty. A child that improves cost sensitivity by sparsifying the book is not enough; it must preserve broad active-day coverage, balanced long/short exposure, and parent-relative economics.

## Caveats

- The repaired OS window is development out-of-sample, not the final untouched test set.
- This rerun can keep attempt017 as a parent lead, but it does not prove tradable alpha.
- Missing-held repair is no longer the main objective for attempt017.
- The metric-equivalent pair `MECHFIX-0009` and `27BCARD-0011` shows that sample evaluation needs fuller prior-sibling comparison.
- The next generation run should be controller-only. Do not auto-launch sample evaluation from the remote machine.

## Next Step

Run a targeted controller-only attempt017 cost-robustness batch using the repaired attempt017 evaluator summary as parent context.

The remote handoff is [controller_attempt017_is_os_cost_robustness_remote_instructions_20260520.md](controller_attempt017_is_os_cost_robustness_remote_instructions_20260520.md).
