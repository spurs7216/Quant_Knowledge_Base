---
title: Task 001 Manual Remote Steps
type: project
status: active
updated: 2026-04-23
tags:
  - project
  - remote-validation
  - ubuntu
  - manual-steps
---
# Task 001 Manual Remote Steps

## Purpose

These are the manual steps to run Task 001 on the remote Ubuntu machine.

The remote data fact provided by the human:

```text
/home/b08303004/Desktop/WRDS/data/daily_stock
```

The expected full file path is:

```text
/home/b08303004/Desktop/WRDS/data/daily_stock/gago9dveytpx6922.csv
```

## 1. Verify The Data File

On the remote Ubuntu machine:

```bash
ls -lh /home/b08303004/Desktop/WRDS/data/daily_stock
ls -lh /home/b08303004/Desktop/WRDS/data/daily_stock/gago9dveytpx6922.csv
```

If the file name differs, do not rename it. Record the actual file name and update the manifest.

## 2. Pull The GitHub Repo

Use the GitHub repository that contains this vault or the research code mirror.

Example:

```bash
cd ~/Desktop
git clone <REPO_URL> quant_resource
cd quant_resource
git checkout <BRANCH>
git pull
```

If the repo already exists:

```bash
cd ~/Desktop/quant_resource
git fetch
git checkout <BRANCH>
git pull
```

## 3. Create Python Environment

Task 001 does not need GPU.

Simple environment:

```bash
cd ~/Desktop/quant_resource
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r research/remote_validation/requirements.txt
```

If the remote machine uses conda or micromamba, that is also acceptable:

```bash
conda create -n quant_remote_validation python=3.11 -y
conda activate quant_remote_validation
python -m pip install -r research/remote_validation/requirements.txt
```

## 4. Run Task 001

From the repo root:

```bash
python research/remote_validation/task001_daily_stock_short_reversal.py \
  --data-root /home/b08303004/Desktop/WRDS/data \
  --output-dir artifacts/remote_runs/20260423_task001_daily_stock_short_reversal
```

This script should write:

- `run_manifest.yaml`
- `metrics.json`
- `scorecard.csv`
- `diagnostics.csv`
- `failure_report.md`
- `review.md`
- `universe_counts_by_month.csv`
- `cost_sensitivity.csv`
- `returns_train.csv`
- `returns_validation.csv`
- `returns_test.csv`

## 5. Review The Output On Remote

Run:

```bash
ls -lh artifacts/remote_runs/20260423_task001_daily_stock_short_reversal
cat artifacts/remote_runs/20260423_task001_daily_stock_short_reversal/failure_report.md
cat artifacts/remote_runs/20260423_task001_daily_stock_short_reversal/metrics.json
```

If the run failed, keep the error and do not hide the failed attempt.

## 6. Bring Back The Artifact Bundle Manually

For now, artifact import is manual review.

Options:

- zip the artifact folder and move it back to the local machine
- copy only the compact files back into local `artifacts/remote_runs/20260423_task001_daily_stock_short_reversal/`
- do not copy the raw warehouse CSV

Example on remote:

```bash
tar -czf task001_daily_stock_short_reversal_artifacts.tar.gz \
  artifacts/remote_runs/20260423_task001_daily_stock_short_reversal
```

## 7. Local Follow-Up

After the artifact bundle is copied back locally:

1. inspect `review.md`, `failure_report.md`, and `metrics.json`
2. decide `proceed`, `revise`, or `reject`
3. update the project decision note
4. only promote durable lessons into `wiki/` if they are reusable

## Notes

- Do not push raw data to GitHub.
- Do not store credentials in the vault.
- If the remote repo has uncommitted changes during the run, `run_manifest.yaml` will mark `dirty: true`.
