---
title: CAND-20260425-002 Artifact Intake Checklist
type: project
status: active
updated: 2026-04-25
tags:
  - project
  - phase3
  - artifact-intake
  - remote-validation
sources:
  - "cand_20260425_002_remote_execution_packet.md"
---
# CAND-20260425-002 Artifact Intake Checklist

## Run Identity

- candidate_id:
- job_id:
- remote commit:
- local artifact root:
- artifact archive or transfer method:
- reviewer:
- review date:

## Completeness

- [ ] `run_manifest.yaml`
- [ ] `metrics.json`
- [ ] `scorecard.csv`
- [ ] `diagnostics.csv`
- [ ] `failure_report.md`
- [ ] `review.md`
- [ ] `subperiod_metrics.csv`
- [ ] `cost_sensitivity.csv`
- [ ] `universe_counts_by_month.csv`

## Required Diagnostics

- [ ] raw duplicate rows before policy recorded
- [ ] raw duplicate groups before policy recorded
- [ ] duplicate policy rows removed recorded
- [ ] remaining raw duplicate count equals `0`
- [ ] duplicate policy name recorded
- [ ] return timing check passes
- [ ] lookahead guard passes
- [ ] turnover-cost check passes
- [ ] code snapshot fields are filled

## Decision Questions

- Did the duplicate-policy change materially alter train / validation / test metrics?
- Did the policy remove the warning source from the Phase 1 run?
- Did the policy introduce any new failed gate?
- Is the candidate still only a data-quality revision, or did any accidental logic change enter the run?
- Should `CAND-20260425-002` be marked `reject`, `revise`, `promoted`, or kept `active`?

## Registry Update

After review, update the registry only through:

```text
python research/candidate_registry/update_candidate_status.py --manifest <status-update-manifest>
```
