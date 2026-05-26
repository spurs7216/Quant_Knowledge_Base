---
title: Expression Bridge Follow-Up Remote Instructions 20260526
type: remote_instructions
status: active
updated: 2026-05-26
tags:
  - project
  - phase4
  - remote-run
  - expression-evolution
  - bridge-policy
  - daily-stock
sources:
  - "expression_episode_20260526_review.md"
  - "phase4_caveat_repair_ledger.md"
  - "current_state.md"
---
# Expression Bridge Follow-Up Remote Instructions 20260526

## Purpose

Run a deterministic bridge-policy follow-up for the strongest non-duplicate clue from `expression_episode_20260526`.

This run does not call Qwen. It compares the smoothed-reversal parent and the liquidity-gated child under the same bridge contracts:

- `daily`
- `rebalance_5`
- `signal_decay_5`

The question is not "can we promote the expression?" The question is whether the child only becomes interesting when the portfolio bridge is slower, and whether it beats the parent under that same bridge. Positive evidence can justify a reviewed bridge-aware strategy conversion. It cannot justify promotion or full validation by itself.

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
  --out-dir artifacts/phase4_alphaevolve/expression_bridge_followup_20260526 \
  --start-date 2011-01-01 \
  --end-date 2025-12-31 \
  --out-sample-start 2023-01-01 \
  --top-n 500 \
  --total-cost-bps 2.5 \
  --cost-grid-bps 0,1,2.5,5,10 \
  --parent-seed-id expr_smoothed_rev \
  --child-expression-id expr_smoothed_rev_liq_bridge_20260526 \
  --child-expression 'rank(-rolling_mean(rolling_sum(excess_ret, 5), 3)) * rank(log1p_abs(dollar_volume))' \
  --bridge-variant-grid daily,rebalance_5,signal_decay_5
```

## Required Artifacts

Zip the output directory and return it for local review.

Required files:

- `expression_bridge_followup_summary.json`
- `expression_bridge_followup_candidate.json`
- `expression_bridge_followup_rankings.csv`
- `expression_bridge_followup_scorecard.csv`
- `expression_bridge_followup_comparison.csv`
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

- Does the child beat `expr_smoothed_rev` under the same `rebalance_5` bridge?
- Does the child beat `expr_smoothed_rev` under the same `signal_decay_5` bridge?
- Are IS and OS turnover-aware scores both positive after 2.5 bps under either slow bridge?
- Does the child remain broad-coverage, dollar-neutral, max-weight compliant, and below missing-held tolerance?
- Is the daily bridge still negative, confirming this is a bridge-policy issue rather than pure expression alpha?
- Does cost sensitivity stay acceptable at 5 bps, or is the result fragile to modest cost changes?

## Stop Conditions

Stop and return artifacts without improvising if:

- repository preflight fails;
- required daily_stock columns fail `daily_stock_contract_v1`;
- no eligible rows remain after static eligibility;
- rolling top-500 membership is empty;
- the runner exits nonzero.

Do not run Qwen, do not run another expression episode, do not run full validation, and do not promote any expression from this follow-up.
