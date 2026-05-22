---
title: Parent Zoo Curated Sample Eval Remote Instructions 20260522
type: remote_handoff
status: ready
updated: 2026-05-22
tags:
  - project
  - phase4
  - remote
  - evaluator
  - parent-zoo
  - sample-eval
sources:
  - "parent_zoo_cost_aware_review_20260522.md"
  - "remote_csv_execution_policy.md"
  - "is_os_evaluation_policy_20260519.md"
---
# Parent Zoo Curated Sample Eval Remote Instructions 20260522

## Purpose

Run data-backed `remote_sample_eval` for the three highest-information controller children from `parent_zoo_cost_aware_20260522`.

This is an evaluator-only run:

- no Qwen;
- no vLLM;
- no controller generation;
- no full validation;
- no test-set use;
- no local repair of child code during the run.

The goal is to decide whether any returned child deserves to become a next controller parent. It is not a promotion run.

## Required Git Hygiene

Run from a clean remote checkout that matches `origin/main`.

```bash
git fetch origin main
git status --short --branch
git rev-parse HEAD
git rev-parse origin/main
test "$(git rev-parse HEAD)" = "$(git rev-parse origin/main)"
test -z "$(git status --short)"
```

Do not proceed if the worktree is dirty or if `HEAD` differs from `origin/main`.

## Preflight

```bash
python -m unittest discover research/alphaevolve_lite/tests
python research/alphaevolve_lite/scripts/remote_sample_eval.py --help
```

Expected evaluator defaults:

```yaml
start_date: 2011-01-01
end_date: 2025-12-31
out_sample_start: 2023-01-01
split_id: daily_stock_top500_is_2011_2022_os_2023_2025_v1
forward_return_contract: signal_universe_t_return_source_eligible_t_plus_1_v1
total_cost_bps: 2.5
```

## Paths

```bash
CSV=/home/b08303004/Desktop/WRDS/data/daily_stock/gago9dveytpx6922.csv
ROOT=artifacts/phase4_alphaevolve
PZOO=$ROOT/parent_zoo_cost_aware_20260522

ATTEMPT017_SUMMARY=$ROOT/remote_sample_eval_attempt017_is_os_forward_repair_20260519/evaluator_summary.json
FIVE_DAY_SUMMARY=$ROOT/seed_zoo_is_os_20260521/evaluations/five_day_excess_reversal/evaluator_summary.json
VOL_NORM_SUMMARY=$ROOT/seed_zoo_is_os_20260521/evaluations/vol_norm_five_day_reversal/evaluator_summary.json
```

Confirm all paths exist before running:

```bash
test -f "$ATTEMPT017_SUMMARY"
test -f "$FIVE_DAY_SUMMARY"
test -f "$VOL_NORM_SUMMARY"
test -f "$PZOO/controller/attempt017_isos_repair/attempt_005/child_program.py"
test -f "$PZOO/controller/five_day_excess_reversal/attempt_002/child_program.py"
test -f "$PZOO/controller/five_day_excess_reversal/attempt_004/child_program.py"
```

## Run 1: Incumbent-Branch Smoothing Control

Program: `PROG-20260522-PZOO-00-0005`

```bash
python research/alphaevolve_lite/scripts/remote_sample_eval.py \
  --csv-path "$CSV" \
  --program-path "$PZOO/controller/attempt017_isos_repair/attempt_005/child_program.py" \
  --out-dir "$ROOT/remote_sample_eval_pzoo_00_0005_20260522" \
  --db-path "$ROOT/program_database.sqlite" \
  --program-id PROG-20260522-PZOO-00-0005 \
  --parent-program-id PROG-20260430-CHILD-0017-ISOSREPAIR \
  --reference-summary "$ATTEMPT017_SUMMARY" \
  --prior-sample-summary "$FIVE_DAY_SUMMARY" \
  --prior-sample-summary "$VOL_NORM_SUMMARY" \
  --start-date 2011-01-01 \
  --end-date 2025-12-31 \
  --out-sample-start 2023-01-01 \
  --null-seeds 10
```

## Run 2: Primary Five-Day Smoothing Candidate

Program: `PROG-20260522-PZOO-01-0002`

```bash
python research/alphaevolve_lite/scripts/remote_sample_eval.py \
  --csv-path "$CSV" \
  --program-path "$PZOO/controller/five_day_excess_reversal/attempt_002/child_program.py" \
  --out-dir "$ROOT/remote_sample_eval_pzoo_01_0002_20260522" \
  --db-path "$ROOT/program_database.sqlite" \
  --program-id PROG-20260522-PZOO-01-0002 \
  --parent-program-id PROG-20260521-SEEDZOO-0002 \
  --reference-summary "$FIVE_DAY_SUMMARY" \
  --prior-sample-summary "$ATTEMPT017_SUMMARY" \
  --prior-sample-summary "$VOL_NORM_SUMMARY" \
  --start-date 2011-01-01 \
  --end-date 2025-12-31 \
  --out-sample-start 2023-01-01 \
  --null-seeds 10
```

## Run 3: Five-Day Regime-Proxy Diagnostic

Program: `PROG-20260522-PZOO-01-0004`

This child is not a true HMM. It is a causal volatility-state dampener. Treat it as regime-proxy evidence only.

```bash
python research/alphaevolve_lite/scripts/remote_sample_eval.py \
  --csv-path "$CSV" \
  --program-path "$PZOO/controller/five_day_excess_reversal/attempt_004/child_program.py" \
  --out-dir "$ROOT/remote_sample_eval_pzoo_01_0004_20260522" \
  --db-path "$ROOT/program_database.sqlite" \
  --program-id PROG-20260522-PZOO-01-0004 \
  --parent-program-id PROG-20260521-SEEDZOO-0002 \
  --reference-summary "$FIVE_DAY_SUMMARY" \
  --prior-sample-summary "$ATTEMPT017_SUMMARY" \
  --prior-sample-summary "$VOL_NORM_SUMMARY" \
  --prior-sample-summary "$ROOT/remote_sample_eval_pzoo_01_0002_20260522/evaluator_summary.json" \
  --start-date 2011-01-01 \
  --end-date 2025-12-31 \
  --out-sample-start 2023-01-01 \
  --null-seeds 10
```

If Run 2 fails to produce `evaluator_summary.json`, omit the final `--prior-sample-summary` line in Run 3 and record that omission in the remote notes.

## Required Review Checks

For each run, inspect:

- `run_manifest.json`
- `evaluator_summary.json`
- `metrics.json`
- `baseline_summary.json`
- `split_manifest.yaml`
- `review.md`
- `git_status.txt`

The remote report should include:

- Git commit and whether `HEAD == origin/main`;
- whether the repaired forward-return source is active;
- IS Sharpe, OS Sharpe, search-sample Sharpe, IS turnover, OS turnover, and turnover-aware score;
- max weight and max missing-held weight;
- portfolio-day coverage and active-day count;
- parent-relative metrics;
- attempt017-relative comparison, even for five-day children;
- prior-sample equivalence flags;
- whether any result appears to come from sparse coverage or collapsed gross exposure.

## Stop Rule

Zip and return only these result directories:

```text
artifacts/phase4_alphaevolve/remote_sample_eval_pzoo_00_0005_20260522/
artifacts/phase4_alphaevolve/remote_sample_eval_pzoo_01_0002_20260522/
artifacts/phase4_alphaevolve/remote_sample_eval_pzoo_01_0004_20260522/
```

Do not run full validation. Do not promote a child on the remote machine.
