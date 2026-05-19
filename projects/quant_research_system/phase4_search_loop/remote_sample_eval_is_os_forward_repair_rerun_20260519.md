---
title: Remote Sample Eval IS/OS Forward-Repair Rerun 2026-05-19
type: remote-handoff
status: ready
updated: 2026-05-19
tags:
  - project
  - phase4
  - remote
  - evaluator
sources:
  - "evaluator_forward_return_contract_repair_20260519.md"
  - "is_os_evaluation_policy_20260519.md"
  - "remote_csv_execution_policy.md"
---
# Remote Sample Eval IS/OS Forward-Repair Rerun 2026-05-19

## Purpose

Rerun data-backed sample evaluation after the forward-return source repair and fixed IS/OS split. This is an evaluator-only run:

- no Qwen;
- no vLLM;
- no controller generation;
- no new child patches;
- no full validation.

The goal is to replace old 2018-2020 sample evidence with repaired 2011-2025 IS/OS evidence for the seed and attempt017-family leads.

## Required Git Hygiene

Run from a clean checkout that matches `origin/main` after the local update has been pushed.

```bash
git fetch origin main
git status --short
git rev-parse HEAD
git rev-parse origin/main
```

Do not proceed if:

- `git status --short` is non-empty;
- `HEAD` differs from `origin/main`;
- the run depends on an unpushed local commit.

If the remote machine needs local artifact-only files to locate old child programs, record that explicitly in `review.md`. The evaluator code itself must come from `origin/main`.

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
```

## Data Path

Use the remote daily-stock CSV:

```bash
CSV=/home/b08303004/Desktop/WRDS/data/daily_stock/gago9dveytpx6922.csv
ROOT=artifacts/phase4_alphaevolve
```

## Run 1: Seed Baseline

```bash
python research/alphaevolve_lite/scripts/remote_sample_eval.py \
  --csv-path "$CSV" \
  --program-path research/alphaevolve_lite/seeds/kalman_reversal_seed.py \
  --out-dir "$ROOT/remote_sample_eval_seed_is_os_forward_repair_20260519" \
  --db-path "$ROOT/program_database.sqlite" \
  --program-id PROG-20260430-000000 \
  --start-date 2011-01-01 \
  --end-date 2025-12-31 \
  --out-sample-start 2023-01-01 \
  --null-seeds 10
```

Required checks:

- `evaluator_summary.json` decision is `sample_pass` or `sample_review`, not runtime error;
- `descriptors.forward_return_source` is `eligible_static_panel`;
- `metrics` contains `in_sample`, `out_sample`, `search_sample`, and `is_os_degradation`.

## Run 2: attempt017 Parent Lead

This is the known structural lead from the old curated sample eval. The usual remote path is:

```bash
ATTEMPT017=artifacts/phase4_alphaevolve/controller_batch_001_diversity_topup/attempt_017/child_program.py
SEED_SUMMARY=artifacts/phase4_alphaevolve/remote_sample_eval_seed_is_os_forward_repair_20260519/evaluator_summary.json
```

If `$ATTEMPT017` is missing, do not guess a replacement. Locate it from the old artifact manifest or report the missing path.

```bash
python research/alphaevolve_lite/scripts/remote_sample_eval.py \
  --csv-path "$CSV" \
  --program-path "$ATTEMPT017" \
  --out-dir "$ROOT/remote_sample_eval_attempt017_is_os_forward_repair_20260519" \
  --db-path "$ROOT/program_database.sqlite" \
  --program-id PROG-20260430-CHILD-0017-ISOSREPAIR \
  --parent-program-id PROG-20260430-000000 \
  --reference-summary "$SEED_SUMMARY" \
  --start-date 2011-01-01 \
  --end-date 2025-12-31 \
  --out-sample-start 2023-01-01 \
  --null-seeds 10
```

## Optional Run 3: Previously Sample-Evaluated attempt017-Family Children

Only run these if the exact child program path exists and the source artifact identifies it unambiguously:

- `PROG-20260513-A017-MECH-0007`
- `PROG-20260514-A017-MECHFIX-0009`
- `PROG-20260514-A017-27BCARD-0011`
- `PROG-20260511-A017-FOCUS-0000`

Use:

```bash
--parent-program-id PROG-20260430-CHILD-0017-ISOSREPAIR
--reference-summary "$ROOT/remote_sample_eval_attempt017_is_os_forward_repair_20260519/evaluator_summary.json"
--prior-sample-summary "$SEED_SUMMARY"
```

Write each optional result into a separate directory named:

```text
remote_sample_eval_<program_id_lower>_is_os_forward_repair_20260519
```

Skip any optional child whose path is not reproducible. Report skipped children in the final review.

## Review Checklist

For every completed run, inspect:

- `run_manifest.json`
- `evaluator_summary.json`
- `metrics.json`
- `baseline_summary.json`
- `split_manifest.yaml`
- `review.md`
- `git_status.txt`

The final remote report should include:

- Git commit and whether `HEAD == origin/main`;
- row counts after static eligibility and rolling top-500 universe construction;
- `forward_return_source` and `forward_return_contract`;
- IS Sharpe, OS Sharpe, IS turnover, OS turnover;
- search-sample Sharpe, turnover-aware score, max weight, max missing-held weight;
- seed-relative and attempt017-relative metric-equivalence flags;
- whether attempt017 still improves broad-sample economics after the repair;
- whether missing-held weight was materially reduced versus old artifacts.

Do not promote any child from this rerun alone. The next local decision is whether attempt017 remains a useful parent lead or whether the project should return to seed-level data-informed generation.
