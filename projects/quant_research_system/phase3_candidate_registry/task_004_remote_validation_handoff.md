---
title: Phase 3 Task 004 Remote Validation Handoff
type: project
status: completed
updated: 2026-04-25
tags:
  - project
  - phase3
  - candidate-registry
  - remote-validation
sources:
  - "candidate_registry.csv"
  - "candidate_event_log.csv"
  - "manifests/cand_20260425_002_executable_duplicate_policy_revision.yaml"
  - "remote_validation/cand_20260425_002_manifest.yaml"
  - "../../../research/remote_validation/task004_duplicate_policy_reversal.py"
---
# Phase 3 Task 004 Remote Validation Handoff

## Objective

Turn the duplicate-policy revision into an executable remote-validation handoff while preserving candidate lineage.

Task 003 made `CAND-20260425-001` ready for remote-manifest construction. During Task 004, that planning-level candidate was converted into an executable child rather than mutating its definition fields.

## Candidate Lineage

Current lineage:

```text
CAND-20260423-001
  -> CAND-20260425-001
      -> CAND-20260425-002
```

Meaning:

- `CAND-20260423-001`: original Phase 1 reversal baseline, still `active` with local decision `revise`.
- `CAND-20260425-001`: planning-level duplicate-policy revision, now `superseded`.
- `CAND-20260425-002`: executable duplicate-policy revision, now `active` and ready for remote validation.

## Intended Research Change

Keep fixed:

- Phase 1 reversal signal
- daily rebalance
- equal-weighted long-short decile construction
- chronological train / validation / test split
- baseline transaction-cost model

Change only:

- duplicate `PERMNO` by `DlyCalDt` handling

The new policy resolves raw duplicate rows before universe filters and signal formation.

Policy:

1. group by `PERMNO` and `DlyCalDt`
2. among duplicate rows, keep the row with the highest nonmissing count across required market and classification fields
3. break ties by highest `abs(DlyPrc) * DlyVol`
4. break remaining ties by earliest original row order

The remote run should report duplicate rows, duplicate groups, removed rows, and remaining duplicate count in `diagnostics.csv`.

## Handoff Files

- candidate manifest: [manifests/cand_20260425_002_executable_duplicate_policy_revision.yaml](manifests/cand_20260425_002_executable_duplicate_policy_revision.yaml)
- remote job manifest: [remote_validation/cand_20260425_002_manifest.yaml](remote_validation/cand_20260425_002_manifest.yaml)
- research script: [../../../research/remote_validation/task004_duplicate_policy_reversal.py](../../../research/remote_validation/task004_duplicate_policy_reversal.py)

## Remote Command

Run from the repository root on the remote Ubuntu warehouse machine after committing and syncing the needed files:

```text
python research/remote_validation/task004_duplicate_policy_reversal.py --data-root /home/b08303004/Desktop/WRDS/data --output-dir artifacts/remote_runs/20260425_cand_20260425_002_duplicate_policy_reversal --total-cost-bps 2.5
```

## Required Pre-Run Fill-Ins

Before remote execution, fill in the draft fields in [remote_validation/cand_20260425_002_manifest.yaml](remote_validation/cand_20260425_002_manifest.yaml):

- vault repo, branch, commit, dirty flag
- research code repo, branch, commit, dirty flag
- remote Python version
- remote environment file or package manager
- expected wall time if known

Do not run this as a search job. It is a one-variable revision.

## Registry Update

Task 004 adds:

- `CAND-20260425-002`
- `EVT-20260425-003`
- `EVT-20260425-004`

It also supersedes `CAND-20260425-001` because the executable child now carries the actual code and remote-validation manifest.

## Next Work

Task 005 should run the remote validation job or prepare the exact GitHub synchronization request. After artifacts return, local review should update `CAND-20260425-002` through the status-update path rather than editing the registry manually.
