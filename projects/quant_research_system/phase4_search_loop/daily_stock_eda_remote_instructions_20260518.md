---
title: daily_stock EDA Remote Instructions 2026-05-18
type: project
status: active
updated: 2026-05-19
tags:
  - project
  - phase4
  - remote-run
  - daily-stock
  - data-exploration
sources:
  - "daily_stock_data_understanding_plan_20260518.md"
  - "daily_stock_contract_v1.md"
  - "remote_csv_execution_policy.md"
---
# daily_stock EDA Remote Instructions 2026-05-18

## Purpose

Run a full-file empirical profile of `daily_stock` and return compact artifacts for local review.

This is data exploration, not AlphaEvolve child generation. Do not start Qwen, do not launch vLLM, do not run sample evaluation, do not run full validation, and do not use the test set.

## Required Git Hygiene

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
python research/alphaevolve_lite/scripts/profile_daily_stock_data.py \
  --csv-path /home/b08303004/Desktop/WRDS/data/daily_stock/gago9dveytpx6922.csv \
  --out-dir artifacts/phase4_alphaevolve/daily_stock_eda_full_20260518 \
  --chunksize 1000000 \
  --sample-modulus 200 \
  --max-sample-rows 300000 \
  --deep-start-date 2011-01-01 \
  --deep-end-date 2025-12-31 \
  --deep-top-n 500
```

Leave `--start-date`, `--end-date`, and `--max-input-rows` unset for this run. The full scan should cover the whole file; the deep profile should focus on the active 2011-2025 IS/OS sample-evaluation window.

## Expected Output Files

Top-level:

```text
daily_stock_eda_summary.json
daily_stock_eda_summary.md
daily_stock_prompt_guidance.json
prompt_data_cards.md
numeric_summary.csv
eligible_numeric_summary.csv
sample_quantiles.csv
eligible_sample_quantiles.csv
categorical_counts.csv
eligible_categorical_counts.csv
daily_counts.csv
deterministic_sample_head.csv
```

Deep window:

```text
deep_window/deep_window_summary.json
deep_window/universe_summary.csv
deep_window/universe_membership_head.csv
deep_window/daily_cross_section_profile.csv
deep_window/industry_coverage_profile.csv
deep_window/transform_profile.csv
```

## Quick Artifact Checks

Before returning the artifact, inspect:

```bash
python - <<'PY'
import json
from pathlib import Path

out = Path("artifacts/phase4_alphaevolve/daily_stock_eda_full_20260518")
summary = json.loads((out / "daily_stock_eda_summary.json").read_text())
deep = json.loads((out / "deep_window" / "deep_window_summary.json").read_text())
print("rows_scanned_after_date_filter:", summary["summary"]["rows_scanned_after_date_filter"])
print("unique_permnos:", summary["summary"]["unique_permnos"])
print("eligible_rows:", summary["summary"]["eligibility_steps"].get("eligible_static_return"))
print("deep_tradable_dates:", deep.get("tradable_dates"))
print("deep_tradable_permnos:", deep.get("tradable_permnos"))
print("deep_median_daily_tradable_count:", deep.get("median_daily_tradable_count"))
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

## Optional Follow-Up Windows

Do not run these until the main artifact succeeds unless specifically asked. They are useful if the first review shows strong regime dependence.

```bash
python research/alphaevolve_lite/scripts/profile_daily_stock_data.py \
  --csv-path /home/b08303004/Desktop/WRDS/data/daily_stock/gago9dveytpx6922.csv \
  --out-dir artifacts/phase4_alphaevolve/daily_stock_eda_2008_2009_20260518 \
  --chunksize 1000000 \
  --sample-modulus 200 \
  --max-sample-rows 200000 \
  --deep-start-date 2008-01-01 \
  --deep-end-date 2009-12-31 \
  --deep-top-n 500
```

```bash
python research/alphaevolve_lite/scripts/profile_daily_stock_data.py \
  --csv-path /home/b08303004/Desktop/WRDS/data/daily_stock/gago9dveytpx6922.csv \
  --out-dir artifacts/phase4_alphaevolve/daily_stock_eda_2020_2022_20260518 \
  --chunksize 1000000 \
  --sample-modulus 200 \
  --max-sample-rows 200000 \
  --deep-start-date 2020-01-01 \
  --deep-end-date 2022-12-31 \
  --deep-top-n 500
```

## Return Artifact

Return only the compact directory:

```text
artifacts/phase4_alphaevolve/daily_stock_eda_full_20260518
```

Do not sync the raw CSV, warehouse extracts, or large intermediate data.
