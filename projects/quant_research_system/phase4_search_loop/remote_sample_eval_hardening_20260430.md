---
title: Phase 4 Remote Sample Eval Hardening 2026-04-30
type: project
status: archived
updated: 2026-04-30
tags: [phase4, alphaevolve, evaluator, hardening]
sources:
  - "daily_stock_contract_v1.md"
  - "remote_csv_execution_policy.md"
  - "task_004_seed_strategy_program.md"
superseded_by: "current_state.md"
---

# Phase 4 Remote Sample Eval Hardening 2026-04-30

> Current compact state: [current_state.md](current_state.md). This dated note is retained as supporting evidence for evaluator hardening before child generation.

## Why

The first remote seed sample evaluation showed that the infrastructure works, but the seed is weak and the evaluator needs stronger prompt-facing evidence before child generation.

The hardened evaluator therefore adds:

- duplicate `PERMNO, DlyCalDt` group diagnostics, including whether duplicate rows disagree on contract fields;
- `git_status.txt` and `git_diff_stat.txt` so dirty remote runs are reviewable;
- random null baselines with matched daily long/short counts;
- sign-flipped baseline;
- `turnover_aware_score` in split metrics and cost sensitivity.

## Remote Command

Run on the remote machine after pulling the latest GitHub commit:

```bash
python research/alphaevolve_lite/scripts/remote_sample_eval.py \
  --csv-path /home/b08303004/Desktop/WRDS/data/daily_stock/gago9dveytpx6922.csv \
  --out-dir artifacts/phase4_alphaevolve/remote_sample_eval_seed_v2 \
  --db-path artifacts/phase4_alphaevolve/program_database.sqlite \
  --start-date 2018-01-01 \
  --end-date 2020-12-31 \
  --null-seeds 10
```

## Interpretation

`sample_pass` remains an evaluator-readiness gate, not a claim that the seed is tradable. The seed should be judged against the sign-flipped and random baselines before using it as a parent for child generation.

Child generation remains blocked until `remote_sample_eval_seed_v2` is reviewed.
