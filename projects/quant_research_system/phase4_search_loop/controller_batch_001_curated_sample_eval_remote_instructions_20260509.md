---
title: Controller Batch 001 Curated Sample Eval Remote Instructions
type: project
status: active
updated: 2026-05-09
tags:
  - project
  - phase4
  - alphaevolve
  - remote-run
  - sample-eval
sources:
  - "controller_batch_001_diversity_topup_review_20260509.md"
  - "daily_stock_contract_v1.md"
  - "cost_model_policy.md"
---
# Controller Batch 001 Curated Sample Eval Remote Instructions

## Purpose

Run the first data-backed child evaluation on a small, diverse subset of controller-static pass children.

This is not full validation and must not touch the test set. The goal is to compare a few target-compliant children against the seed and null baselines on the same remote sample-eval contract.

## Preflight

1. Pull the latest GitHub state after the local descriptor/accounting patch is pushed.
2. Confirm these controller artifacts exist on the remote machine:

```text
artifacts/phase4_alphaevolve/controller_batch_001_diversity_topup/attempt_000/child_program.py
artifacts/phase4_alphaevolve/controller_batch_001_diversity_topup/attempt_004/child_program.py
artifacts/phase4_alphaevolve/controller_batch_001_diversity_topup/attempt_010/child_program.py
artifacts/phase4_alphaevolve/controller_batch_001_diversity_topup/attempt_011/child_program.py
artifacts/phase4_alphaevolve/controller_batch_001_diversity_topup/attempt_017/child_program.py
```

3. Qwen/vLLM is not required for `remote_sample_eval.py`; this is evaluator execution only.
4. Do not run full validation, test-set evaluation, IBKR, TWS, account-state, position, order, or credential logic.

## Command

Run from the repository root on the remote Linux/data machine:

```bash
CSV_PATH=/home/b08303004/Desktop/WRDS/data/daily_stock/gago9dveytpx6922.csv
DB_PATH=artifacts/phase4_alphaevolve/program_database.sqlite

python research/alphaevolve_lite/scripts/remote_sample_eval.py \
  --csv-path "$CSV_PATH" \
  --program-path research/alphaevolve_lite/seeds/kalman_reversal_seed.py \
  --out-dir artifacts/phase4_alphaevolve/remote_sample_eval_controller_batch_001_seed_reference_20260509 \
  --db-path "$DB_PATH" \
  --start-date 2018-01-01 \
  --end-date 2020-12-31 \
  --top-n 500 \
  --total-cost-bps 2.5 \
  --cost-grid-bps 0,1,2.5,5,10 \
  --null-seeds 10 \
  --program-id PROG-20260430-000000 \
  --run-id remote_sample_eval_controller_batch_001_seed_reference_20260509

for ATTEMPT in attempt_000 attempt_004 attempt_010 attempt_011 attempt_017; do
  case "$ATTEMPT" in
    attempt_000) PROGRAM_ID=PROG-20260430-CHILD-0000 ;;
    attempt_004) PROGRAM_ID=PROG-20260430-CHILD-0004 ;;
    attempt_010) PROGRAM_ID=PROG-20260430-CHILD-0010 ;;
    attempt_011) PROGRAM_ID=PROG-20260430-CHILD-0011 ;;
    attempt_017) PROGRAM_ID=PROG-20260430-CHILD-0017 ;;
  esac

  python research/alphaevolve_lite/scripts/remote_sample_eval.py \
    --csv-path "$CSV_PATH" \
    --program-path "artifacts/phase4_alphaevolve/controller_batch_001_diversity_topup/${ATTEMPT}/child_program.py" \
    --out-dir "artifacts/phase4_alphaevolve/remote_sample_eval_controller_batch_001_topup_${ATTEMPT}_20260509" \
    --db-path "$DB_PATH" \
    --start-date 2018-01-01 \
    --end-date 2020-12-31 \
    --top-n 500 \
    --total-cost-bps 2.5 \
    --cost-grid-bps 0,1,2.5,5,10 \
    --null-seeds 10 \
    --program-id "$PROGRAM_ID" \
    --run-id "remote_sample_eval_controller_batch_001_topup_${ATTEMPT}_20260509"
done
```

## Return Artifacts

Return a compact archive with one folder per eval run containing:

```text
evaluator_summary.json
review.md
metrics.json
baseline_summary.json
scorecard.csv
diagnostics.csv
cost_sensitivity.csv
null_baselines.csv
duplicate_diagnostics.csv
universe_summary.csv
split_manifest.yaml
run_manifest.json
git_status.txt
git_diff_stat.txt
failure_report.md
```

## Review Gates

```yaml
remote_sample_eval_controller_batch_001_curated:
  child_count: 5
  seed_reference_rerun: true
  test_set_used: false
  full_validation_launched: false
  total_cost_bps: 2.5
  cost_grid_bps: [0, 1, 2.5, 5, 10]
  null_seeds: 10
  compare_against_seed_reference: true
  compare_against_null_baselines: true
  report_turnover_aware_score: true
  report_max_weight: true
  report_max_missing_held_weight: true
  report_cost_sensitivity: true
```

Do not promote any child from this run alone. Use it to decide which behavior families deserve another evolution round.
