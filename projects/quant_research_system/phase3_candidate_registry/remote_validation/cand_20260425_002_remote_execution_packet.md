---
title: CAND-20260425-002 Remote Execution Packet
type: project
status: active
updated: 2026-04-25
tags:
  - project
  - phase3
  - remote-validation
  - execution-packet
sources:
  - "cand_20260425_002_manifest.yaml"
  - "../task_004_remote_validation_handoff.md"
  - "../../../../research/remote_validation/task004_duplicate_policy_reversal.py"
---
# CAND-20260425-002 Remote Execution Packet

## Purpose

This packet is the local-to-remote handoff for `CAND-20260425-002`.

It does not claim that the remote job has run. It defines exactly what must be synced, run, and returned before the candidate can receive an evaluator-backed local decision.

## Candidate

- candidate_id: `CAND-20260425-002`
- parent_id: `CAND-20260425-001`
- root_candidate_id: `CAND-20260423-001`
- environment: `remote_validation`
- job_id: `20260425_cand_20260425_002_duplicate_policy_reversal`
- remote dataset: `/home/b08303004/Desktop/WRDS/data/daily_stock/gago9dveytpx6922.csv`

## Local Snapshot At Packet Creation

- repo: `https://github.com/spurs7216/Quant_Knowledge_Base.git`
- branch: `main`
- current local HEAD before committing Task 005: `321f37b978b79aea5508e4c82d6ad18dedefeb09`
- dirty worktree at packet creation: `true`

The remote run must not use this dirty snapshot as final provenance. Before execution, create a clean commit containing the Phase 3 registry files and the `task004` research script, then fill the commit fields in [cand_20260425_002_manifest.yaml](cand_20260425_002_manifest.yaml).

## Minimum Files To Sync

The remote machine needs at least:

- `research/remote_validation/task001_daily_stock_short_reversal.py`
- `research/remote_validation/task004_duplicate_policy_reversal.py`
- `projects/quant_research_system/phase3_candidate_registry/candidate_registry.csv`
- `projects/quant_research_system/phase3_candidate_registry/candidate_event_log.csv`
- `projects/quant_research_system/phase3_candidate_registry/remote_validation/cand_20260425_002_manifest.yaml`
- `projects/quant_research_system/phase3_candidate_registry/task_004_remote_validation_handoff.md`
- `projects/quant_research_system/phase3_candidate_registry/task_005_remote_execution_packet.md`

The remote machine does not need raw local artifacts, IBKR files, broker credentials, or local Obsidian state.

## Local Pre-Sync Checklist

- [ ] Run `python research/candidate_registry/validate_candidate_registry.py`.
- [ ] Run `python -m py_compile research/remote_validation/task004_duplicate_policy_reversal.py`.
- [ ] Confirm no secrets, credentials, raw data, or generated artifact bundles are staged.
- [ ] Commit the needed Phase 3 and research-script files.
- [ ] Push only when the remote machine is ready to pull the exact commit.
- [ ] Fill the manifest snapshot fields with the clean commit.

## Remote Pull And Run

On the remote Ubuntu machine, from a clean working directory:

```text
git fetch origin
git checkout main
git pull --ff-only origin main
git rev-parse HEAD
git status --short
```

The commit printed by `git rev-parse HEAD` must match the manifest fields before the run.

Then run:

```text
python research/remote_validation/task004_duplicate_policy_reversal.py --data-root /home/b08303004/Desktop/WRDS/data --output-dir artifacts/remote_runs/20260425_cand_20260425_002_duplicate_policy_reversal --total-cost-bps 2.5
```

## Expected Local Artifact Root After Import

```text
artifacts/remote_runs/20260425_cand_20260425_002_duplicate_policy_reversal/
```

The artifact bundle should remain compact. Do not copy the full `daily_stock` warehouse file into the vault.

## Required Returned Files

- `run_manifest.yaml`
- `metrics.json`
- `scorecard.csv`
- `diagnostics.csv`
- `failure_report.md`
- `review.md`
- `subperiod_metrics.csv`
- `cost_sensitivity.csv`
- `universe_counts_by_month.csv`

Recommended returned files:

- `exchange_split_metrics.csv`
- `liquidity_bucket_metrics.csv`
- `returns_train.csv`
- `returns_validation.csv`
- `returns_test.csv`

## Required Diagnostic Checks

`diagnostics.csv` must include:

- `raw_duplicate_permno_date_rows_before_policy`
- `raw_duplicate_permno_date_groups_before_policy`
- `duplicate_policy_rows_removed`
- `duplicate_policy_remaining_raw_duplicates`
- `duplicate_policy_applied`
- `return_timing_one_trading_day`
- `signal_lookahead_guard`
- `turnover_cost_applied`
- `code_snapshots_recorded`

The run is not acceptable as Phase 3 evidence if `duplicate_policy_remaining_raw_duplicates` is nonzero or if return timing / lookahead checks fail.

## Post-Run Local Intake

After the artifact bundle returns:

1. inspect file completeness against this packet
2. compare metrics against `CAND-20260423-001`
3. check whether the duplicate-policy diagnostics removed the prior warning source
4. write a local review note under `projects/quant_research_system/phase3_candidate_registry/`
5. update `CAND-20260425-002` through `update_candidate_status.py`

Do not manually edit the registry for the result.
