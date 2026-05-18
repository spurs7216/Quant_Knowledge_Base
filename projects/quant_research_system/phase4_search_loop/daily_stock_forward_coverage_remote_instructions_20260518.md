---
title: daily_stock Forward Coverage Remote Instructions 2026-05-18
type: project
status: active
updated: 2026-05-18
tags:
  - project
  - phase4
  - remote-run
  - daily-stock
  - data-exploration
  - forward-coverage
sources:
  - "daily_stock_data_understanding_plan_20260518.md"
  - "daily_stock_eda_full_review_20260518.md"
  - "current_state.md"
  - "daily_stock_contract_v1.md"
  - "remote_csv_execution_policy.md"
---
# daily_stock Forward Coverage Remote Instructions 2026-05-18

## Purpose

Run the recommended next data exploration after the full-file `daily_stock` EDA.

This diagnostic answers two questions:

1. What is the rolling top-500 stock coverage over the whole available timeline?
2. In the current 2018-2020 sample-evaluation window, why can evaluator-held weights miss next-day returns?

This is data exploration, not child generation. Do not start Qwen, do not launch vLLM, do not run the controller, do not run sample evaluation, do not run full validation, and do not use the test set.

## Required Git Hygiene

Run before the diagnostic:

```bash
git fetch origin
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

Do not run from an unpushed research-code commit. If a local hygiene-only commit is unavoidable, record it explicitly in the artifact review.

## Main Command

Run from the repository root on the remote Linux/data machine:

```bash
python research/alphaevolve_lite/scripts/profile_daily_stock_forward_coverage.py \
  --csv-path /home/b08303004/Desktop/WRDS/data/daily_stock/gago9dveytpx6922.csv \
  --out-dir artifacts/phase4_alphaevolve/daily_stock_forward_coverage_20260518 \
  --chunksize 1000000 \
  --top-n 500 \
  --forward-start-date 2018-01-01 \
  --forward-end-date 2020-12-31
```

Leave `--coverage-start-date`, `--coverage-end-date`, and `--max-input-rows` unset. The coverage scan should cover the whole available timeline while the forward-return diagnostic focuses on the active sample-evaluation window.

## Expected Output Files

```text
forward_coverage_summary.json
forward_coverage_summary.md
forward_availability_summary.json
held_availability_prompt_cards.md
top500_membership_monthly.csv
top500_daily_coverage.csv
top500_monthly_coverage.csv
top500_permno_coverage.csv
top500_membership_churn.csv
forward_availability_by_date.csv
forward_availability_by_bucket.csv
forward_availability_by_industry.csv
forward_availability_by_exchange.csv
forward_availability_diagnostics_head.csv
```

The most important tables for local review are:

- `top500_daily_coverage.csv`: whole-timeline daily selected-name coverage;
- `top500_monthly_coverage.csv`: whole-timeline monthly row coverage;
- `top500_permno_coverage.csv`: name-level persistence and coverage;
- `top500_membership_churn.csv`: month-to-month rolling-universe churn;
- `forward_availability_by_date.csv`: evaluator-style next-day return availability by date;
- `forward_availability_by_bucket.csv`: availability by price, dollar-volume, market-cap, and next-month membership buckets;
- `held_availability_prompt_cards.md`: compact rules for future prompts.

## Quick Artifact Checks

Before returning the artifact, inspect:

```bash
python - <<'PY'
import json
from pathlib import Path

out = Path("artifacts/phase4_alphaevolve/daily_stock_forward_coverage_20260518")
summary = json.loads((out / "forward_coverage_summary.json").read_text())
forward = summary["forward_availability"]
coverage = summary["daily_coverage"]
print("schema_version:", summary["schema_version"])
print("top_n:", summary["top_n"])
print("raw_trading_date_count:", summary.get("raw_trading_date_count"))
print("eligible_trading_date_count:", summary.get("eligible_trading_date_count"))
print("topn_month_count:", summary["topn_month_count"])
print("topn_distinct_permnos:", summary["topn_distinct_permnos"])
print("median_daily_coverage_rate:", coverage.get("median_coverage_rate"))
print("min_daily_coverage_rate:", coverage.get("min_coverage_rate"))
print("forward_availability_rate:", forward.get("availability_rate"))
print("forward_cause_counts:", forward.get("cause_counts"))
PY
```

If the command fails, return the partial output directory plus:

```text
stderr_tail.txt
stdout_tail.txt
failure_report.md
git_status.txt
git_diff_stat.txt
```

## Return Artifact

Return only the compact directory:

```text
artifacts/phase4_alphaevolve/daily_stock_forward_coverage_20260518
```

Do not sync the raw CSV, warehouse extracts, top-500 full panels beyond the compact outputs above, or large intermediate data.

## Local Review Notebook

The local review notebook is:

```text
projects/quant_research_system/phase4_search_loop/notebooks/daily_stock_forward_coverage_20260518_report.ipynb
```

It is separate from the previous full-file EDA notebook and should be executed after the returned artifact is placed under `artifacts/`.
