---
title: Controller Batch 001 Attempt 017 Repair Remote Instructions 2026-05-09
type: project
status: active
updated: 2026-05-09
tags:
  - phase4
  - alphaevolve
  - remote-run
  - qwen
sources:
  - "remote_sample_eval_controller_batch_001_review_20260509.md"
  - "remote_qwen_vllm_config.md"
  - "current_state.md"
---

# Controller Batch 001 Attempt 017 Repair Remote Instructions 2026-05-09

Supersession note: this dated handoff used the old 2018-2020 sample-evaluation window. Future sample evaluations must use the fixed 2011-2025 IS/OS policy in [is_os_evaluation_policy_20260519.md](is_os_evaluation_policy_20260519.md).

## Purpose

Run a small controller-only repair/generation slice around the only useful data-backed lead from the curated sample eval: `attempt_017`, the causal-smoothing child.

This is not promotion, full validation, or test-set use. The goal is to generate a few controller-safe children that preserve the broad-coverage smoothing improvement while addressing missing-held-weight risk without lookahead.

## Required Preflight

1. Pull the latest GitHub state.
2. Confirm the repo is clean or record any local patch in the artifact review.
3. Start Qwen3.5-9B in a persistent terminal or `tmux` pane and keep it running.
4. Verify `/health` and `/v1/models` from a separate terminal before running the controller.
5. Do not use evaluator-only forward-return fields such as `fwd_ret`, `fwd_date`, `fwd_vwretd`, `next_market_date`, or `one_day_forward` in generated strategy edits.

Qwen3.5-9B launch command:

```bash
CUDA_VISIBLE_DEVICES=0 vllm serve Qwen/Qwen3.5-9B \
  --served-model-name qwen35-9b-fast \
  --host 127.0.0.1 \
  --port 8001 \
  --max-model-len 32768 \
  --gpu-memory-utilization 0.90
```

Health checks:

```bash
curl -sf http://127.0.0.1:8001/health
curl -sf http://127.0.0.1:8001/v1/models
```

## Controller-Only Command

```bash
python research/alphaevolve_lite/scripts/run_child_batch.py \
  --program-path artifacts/phase4_alphaevolve/controller_batch_001_diversity_topup/attempt_017/child_program.py \
  --parent-program-id PROG-20260430-CHILD-0017 \
  --evaluator-summary artifacts/phase4_alphaevolve/remote_sample_eval_controller_batch_001_topup_attempt_017_20260509/evaluator_summary.json \
  --out-dir artifacts/phase4_alphaevolve/controller_batch_001_attempt017_repair_20260509 \
  --db-path artifacts/phase4_alphaevolve/program_database.sqlite \
  --attempts 12 \
  --surface-schedule portfolio,risk,signal,portfolio,risk,ranking \
  --prior-summary artifacts/phase4_alphaevolve/controller_batch_001/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_batch_001_diversity_topup/summary.json \
  --program-id-prefix PROG-20260509-A017-REPAIR \
  --max-tokens 8192
```

## Success Criteria

The remote run is successful if it returns compact artifacts that let local review answer:

```yaml
controller_path_healthy:
  qwen_final_content_nonempty: true
  parse_apply_compile_vector_semantic_gates: mostly_true
  db_inserted_for_attempts: true
search_quality:
  unique_nonduplicate_children: at_least_6_of_12
  no_forward_return_reference_rejects: expected_true
  target_surfaces_covered:
    - portfolio
    - risk
    - signal
review_decision:
  remote_sample_eval_launched: false
  full_validation_launched: false
  test_set_used: false
```

## After Run

Zip or otherwise return the full `controller_batch_001_attempt017_repair_20260509` artifact folder. Do not launch sample evaluation from this batch until local review selects a tiny subset.

When sample evaluation is later requested for selected children, use the hardened evaluator with the attempt017 parent reference summary:

```bash
python research/alphaevolve_lite/scripts/remote_sample_eval.py \
  --csv-path /home/b08303004/Desktop/WRDS/data/daily_stock/gago9dveytpx6922.csv \
  --program-path <selected_child_program.py> \
  --program-id <selected_child_program_id> \
  --parent-program-id PROG-20260430-CHILD-0017 \
  --reference-summary artifacts/phase4_alphaevolve/remote_sample_eval_controller_batch_001_topup_attempt_017_20260509/evaluator_summary.json \
  --out-dir <selected_child_sample_eval_out_dir> \
  --db-path artifacts/phase4_alphaevolve/program_database.sqlite \
  --start-date 2018-01-01 \
  --end-date 2020-12-31 \
  --top-n 500 \
  --total-cost-bps 2.5 \
  --null-seeds 10
```
