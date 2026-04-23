---
title: Remote Validation Preflight Checklist
type: project
status: active
updated: 2026-04-23
tags:
  - project
  - preflight
  - remote-validation
  - checklist
---
# Remote Validation Preflight Checklist

## Purpose

Check a remote validation job before it is sent to the Ubuntu machine.

The preflight is designed to catch preventable failures locally:

- incomplete manifests
- wrong dataset paths
- vague universe rules
- hidden leakage
- missing cost assumptions
- unreviewable output plans

## 1. Manifest Completeness

- [ ] `job_id` is unique and stable.
- [ ] `environment` is `remote_validation`.
- [ ] `candidate_artifact` is named and typed.
- [ ] GitHub sync channel is stated.
- [ ] Remote OS is stated as Ubuntu.
- [ ] Vault snapshot fields are filled or explicitly marked pending.
- [ ] Remote research code snapshot fields are filled or explicitly marked pending.
- [ ] Artifact import policy is `manual_review`.

## 2. Dataset And Catalog Checks

- [ ] Every remote dataset path appears in `catalog/csv_data_inventory.csv` or `catalog/csv_data_catalog.md`.
- [ ] Every catalog sample path exists locally.
- [ ] Required columns are visible in the catalog sample or dataset note.
- [ ] Dataset row-count expectation is recorded when known.
- [ ] Legacy physical spelling is preserved exactly.

For Task 001, the required dataset path is:

```text
data/daily_stock/gago9dveytpx6922.csv
```

## 3. Universe Checks

- [ ] Working grain is explicit.
- [ ] Primary identifier is explicit.
- [ ] Date column is explicit.
- [ ] Security-type filters are explicit.
- [ ] Liquidity and price filters are explicit.
- [ ] Missing-return handling is explicit.
- [ ] Delisting or inactive-status handling is acknowledged.

## 4. Timestamp And Leakage Checks

- [ ] Signal uses only data available before the rebalance decision.
- [ ] Formation lag is stated.
- [ ] Holding-period return is not included in signal construction.
- [ ] Cross-sectional ranking uses same-date available signals only.
- [ ] Train, validation, and test splits are chronological.
- [ ] Hidden test data are not used for parameter choice.

## 5. Portfolio And Cost Checks

- [ ] Portfolio construction rule is explicit.
- [ ] Rebalance frequency is explicit.
- [ ] Gross and net exposure targets are explicit.
- [ ] Position caps are stated or deliberately omitted.
- [ ] Commission/slippage/borrow assumptions are explicit.
- [ ] Turnover cost application is explicit.

## 6. Evaluation Checks

- [ ] Primary metrics are listed.
- [ ] Robustness checks are listed.
- [ ] Null or benchmark comparison is listed.
- [ ] Failure gates are listed.
- [ ] Expected output files match the artifact schema.

## 7. Remote Execution Checks

- [ ] Remote branch / commit to pull is specified or deliberately pending.
- [ ] Environment file is specified or deliberately pending.
- [ ] Resource request is plausible.
- [ ] GPU requirement is stated.
- [ ] No secrets are present in the manifest.
- [ ] No raw data are marked for GitHub upload.

## 8. Approval

- [ ] Human approves sending this job to the remote machine.
- [ ] Human understands artifacts will be manually reviewed before local import.

## Preflight Outcome

Use one of:

- `ready_for_remote`
- `blocked_missing_manifest_fields`
- `blocked_dataset_unclear`
- `blocked_leakage_risk`
- `blocked_output_unclear`
- `blocked_security_risk`
