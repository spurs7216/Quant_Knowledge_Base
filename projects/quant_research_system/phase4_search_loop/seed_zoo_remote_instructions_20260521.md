---
title: Seed Zoo Remote Instructions 2026-05-21
type: remote-handoff
status: ready
updated: 2026-05-21
tags:
  - project
  - phase4
  - remote
  - seed-zoo
  - sample-eval
sources:
  - "seed_zoo_parent_discovery_20260521.md"
  - "remote_sample_eval_is_os_forward_repair_review_20260520.md"
  - "remote_csv_execution_policy.md"
---
# Seed Zoo Remote Instructions 2026-05-21

## Purpose

Run deterministic seed-zoo parent discovery under the repaired 2011-2025 IS/OS sample evaluator.

This is not Qwen generation, not a controller batch, and not full validation. The goal is to find better parent programs before continuing AlphaEvolve.

## Scope

```yaml
task: seed_zoo_parent_discovery
qwen_required: false
vllm_required: false
controller_generation: false
remote_sample_eval: true
full_validation: false
test_set_used: false
program_count: 10
split_id: daily_stock_top500_is_2011_2022_os_2023_2025_v1
forward_return_source: eligible_static_panel
```

## Required Git Hygiene

Run from a clean checkout that matches `origin/main` after the local update is pushed.

```bash
git fetch origin main
git status --short --branch
git rev-parse HEAD
git rev-parse origin/main
```

Preferred state:

```yaml
git_dirty: false
head_matches_origin_main: true
manifest_commit_fetchable_from_github: true
```

Do not run from an unpushed research-code commit.

## Preflight

```bash
python -m unittest discover research/alphaevolve_lite/tests
python research/alphaevolve_lite/scripts/run_seed_zoo.py --help
python research/alphaevolve_lite/scripts/remote_sample_eval.py --help
```

## Data Path

```bash
CSV=/home/b08303004/Desktop/WRDS/data/daily_stock/gago9dveytpx6922.csv
ROOT=artifacts/phase4_alphaevolve
OUT="$ROOT/seed_zoo_is_os_20260521"
BENCH="$ROOT/remote_sample_eval_attempt017_is_os_forward_repair_20260519/evaluator_summary.json"
```

If `$BENCH` is missing, omit the `--benchmark-summary "$BENCH"` argument and record that in the remote report.

## Main Command

```bash
python research/alphaevolve_lite/scripts/run_seed_zoo.py \
  --csv-path "$CSV" \
  --out-dir "$OUT" \
  --db-path "$ROOT/program_database.sqlite" \
  --benchmark-summary "$BENCH" \
  --null-seeds 5
```

If runtime becomes too long, stop cleanly and return the partial artifact. Do not switch to Qwen or controller generation. If a small smoke is needed first, run:

```bash
python research/alphaevolve_lite/scripts/run_seed_zoo.py \
  --csv-path "$CSV" \
  --out-dir "$ROOT/seed_zoo_is_os_20260521_smoke" \
  --db-path "$ROOT/program_database.sqlite" \
  --benchmark-summary "$BENCH" \
  --seed-ids one_day_excess_reversal,vol_norm_five_day_reversal,kalman_ewm_reversal \
  --null-seeds 2
```

## Expected Artifacts

Root:

```text
seed_zoo_manifest.json
seed_zoo_manifest.md
seed_zoo_commands.json
seed_zoo_commands.sh
seed_zoo_results.json
seed_zoo_results.csv
seed_zoo_report.md
seed_zoo_run_manifest.json
programs/*.py
evaluations/*/evaluator_summary.json
```

Each evaluation directory should also contain the normal sample-eval artifacts:

```text
run_manifest.json
review.md
metrics.json
cost_sensitivity.csv
baseline_summary.json
split_manifest.yaml
git_status.txt
program_snapshot.py
```

## Review Checklist

Report:

- Git commit and whether `HEAD == origin/main`;
- whether all 10 seed programs completed;
- any failed seed ids and exact failure reason;
- top-ranked `candidate` rows from `seed_zoo_report.md`;
- comparison versus repaired attempt017 if `$BENCH` existed;
- IS Sharpe, OS Sharpe, turnover-aware score, turnover, max missing-held weight, and max weight for top 5 rows;
- whether any simple seed beats attempt017 on turnover-aware score or OS Sharpe;
- whether candidate evidence suggests a new parent branch before more attempt017 work.

Do not promote or full-validate any seed from this run alone. The next local decision is which seed-zoo parent or parents should enter the AlphaEvolve program database as active search parents.

## Return Artifact

Return:

```text
artifacts/phase4_alphaevolve/seed_zoo_is_os_20260521
```
