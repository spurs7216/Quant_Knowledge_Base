---
title: Expression Bridge Robustness Remote Instructions 20260526
type: remote_instructions
status: active
updated: 2026-05-26
tags:
  - project
  - phase4
  - remote-run
  - expression-evolution
  - bridge-policy
  - robustness
  - daily-stock
sources:
  - "expression_bridge_followup_review_20260526.md"
  - "phase4_caveat_repair_ledger.md"
  - "current_state.md"
---
# Expression Bridge Robustness Remote Instructions 20260526

## Purpose

Run deterministic bridge robustness after the first bridge follow-up.

The prior result showed that the liquidity-gated smoothed-reversal child passes only under one anchored `rebalance_5` bridge. This run tests whether that bridge evidence is stable across harmless bridge implementation choices:

- all `rebalance_5` phase offsets 0 through 4;
- neighboring rebalance periods 3 and 10 with all phase offsets;
- signal-decay controls at 3, 5, and 10.

This run does not call Qwen or vLLM. It cannot promote a strategy. Positive evidence can only justify converting the expression into a reviewed bridge-aware strategy parent for a later evolution episode.

## Preflight

On the remote machine:

```bash
git fetch origin
git status --short
git rev-parse HEAD
git rev-parse origin/main
```

Stop and report if:

- the worktree is dirty before the run;
- `HEAD` does not match `origin/main`;
- the daily_stock CSV path is unknown.

Do not launch Qwen or vLLM for this run.

## Command

Use the real remote daily_stock CSV path:

```bash
python research/alphaevolve_lite/scripts/run_expression_bridge_followup.py \
  --csv-path /path/to/daily_stock.csv \
  --out-dir artifacts/phase4_alphaevolve/expression_bridge_robustness_20260526 \
  --start-date 2011-01-01 \
  --end-date 2025-12-31 \
  --out-sample-start 2023-01-01 \
  --top-n 500 \
  --total-cost-bps 2.5 \
  --cost-grid-bps 0,1,2.5,5,10 \
  --parent-seed-id expr_smoothed_rev \
  --child-expression-id expr_smoothed_rev_liq_bridge_20260526 \
  --child-expression 'rank(-rolling_mean(rolling_sum(excess_ret, 5), 3)) * rank(log1p_abs(dollar_volume))' \
  --bridge-variant-grid daily,rebalance_3,rebalance_3_offset_1,rebalance_3_offset_2,rebalance_5,rebalance_5_offset_1,rebalance_5_offset_2,rebalance_5_offset_3,rebalance_5_offset_4,rebalance_10,rebalance_10_offset_1,rebalance_10_offset_2,rebalance_10_offset_3,rebalance_10_offset_4,rebalance_10_offset_5,rebalance_10_offset_6,rebalance_10_offset_7,rebalance_10_offset_8,rebalance_10_offset_9,signal_decay_3,signal_decay_5,signal_decay_10
```

## Required Artifacts

Zip the output directory and return it for local review.

Required files:

- `expression_bridge_followup_summary.json`
- `expression_bridge_followup_candidate.json`
- `expression_bridge_followup_rankings.csv`
- `expression_bridge_followup_scorecard.csv`
- `expression_bridge_followup_comparison.csv`
- `expression_bridge_followup_robustness.csv`
- `expression_bridge_followup_cost_sensitivity.csv`
- `expression_interface.md`
- `expression_seed_library.json`
- `universe_membership_monthly.csv`
- `universe_summary.csv`
- `split_manifest.yaml`
- `git_status.txt`
- `git_diff_stat.txt`
- `run_result.json`

## Review Questions

The local reviewer should answer:

- Does the child keep positive IS and OS turnover-aware scores across all `rebalance_5` offsets?
- Does it beat the parent on search turnover-aware score across all `rebalance_5` offsets?
- Are failures isolated to one phase, or does the whole `rebalance_5` family remain strong?
- Is `rebalance_3` or `rebalance_10` more stable than `rebalance_5`?
- Do signal-decay controls confirm or contradict the rebalance evidence?
- Does the result remain fragile at 5 bps total cost?
- Does any bridge family satisfy `robust_bridge_candidate` in `expression_bridge_followup_robustness.csv`?

## Stop Conditions

Stop and return artifacts without improvising if:

- repository preflight fails;
- required daily_stock columns fail `daily_stock_contract_v1`;
- no eligible rows remain after static eligibility;
- rolling top-500 membership is empty;
- the runner exits nonzero.

Do not run Qwen, do not run full validation, do not promote, and do not start a new expression episode from this result.
