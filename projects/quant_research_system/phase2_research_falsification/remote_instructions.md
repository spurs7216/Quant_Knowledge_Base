---
title: Phase 2 Remote Instructions
type: project
status: draft
updated: 2026-04-23
tags:
  - project
  - phase2
  - remote-compute
  - instructions
---
# Phase 2 Remote Instructions

## Authority Boundary

The remote runner produces evidence only.

Do not decide whether Phase 2 is closed. Report whether the run completed, whether artifacts are complete, and whether any gates failed.

The remote runner has no IBKR/TWS role. Do not attempt to access TWS, IB Gateway, IBKR account state, positions, contract lookup, market data through IBKR, paper orders, live orders, or broker credentials from the remote machine.

## Preconditions

- The remote machine has pulled the exact vault commit requested by the local machine.
- The daily-stock file exists at:

```text
/home/b08303004/Desktop/WRDS/data/daily_stock/gago9dveytpx6922.csv
```

- Python environment has at least `pandas` and `numpy`.
- No raw warehouse data should be copied into the repository or returned as artifacts.
- No IBKR, TWS, broker API, broker credential, account-state, or order-submission dependency is required or allowed for this run.

## Command

From the vault repo root on the remote Ubuntu machine:

```bash
python research/research_falsification/phase2_daily_stock_falsification_suite.py \
  --data-root /home/b08303004/Desktop/WRDS/data \
  --output-dir artifacts/remote_runs/20260423_phase2_daily_stock_falsification_suite \
  --random-seeds 5 \
  --total-cost-bps 2.5
```

## Required Checks

After the run, verify:

- `run_manifest.yaml` exists
- `metrics.json` exists
- `task_scorecard.csv` exists
- `diagnostics.csv` exists
- `failure_report.md` exists
- `review.md` exists
- `random_rank_seed_metrics.csv` exists
- `random_rank_detailed_metrics.csv` exists
- `identifier_artifact_metrics.csv` exists
- `leakage_trap_metrics.csv` exists
- `implementation_feasibility.csv` exists

Also verify:

- no raw warehouse data were copied into the artifact directory
- no broker credentials, account identifiers, TWS settings, or IBKR connection artifacts were written
- git branch and commit were recorded
- dirty flag was recorded
- failed and warning diagnostics are visible

## Return Package

Create a compact archive of the artifact directory only.

Recommended archive name:

```text
20260423_phase2_daily_stock_falsification_suite_<short_commit>_artifacts.tar.gz
```

Return the archive and its SHA256 hash through the agreed synchronization path.

## Remote Report

The remote report should contain:

- exact command run
- runtime environment
- artifact archive name
- SHA256 hash
- required-file completeness
- warning and failure counts
- non-binding recommendation: `accept_artifacts`, `revise_and_rerun`, or `blocked`
- confirmation that no IBKR/TWS access was attempted

Do not state `phase2_closed`.
