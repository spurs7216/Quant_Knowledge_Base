---
title: Controller Attempt017 Mechanism Batch Remote Instructions 2026-05-13
type: project
status: active
updated: 2026-05-13
tags:
  - phase4
  - alphaevolve
  - remote-run
  - qwen
  - mechanism-batch
sources:
  - "attempt017_mechanism_design_20260513.md"
  - "controller_attempt017_search_control_rerun_review_20260513.md"
  - "current_state.md"
---
# Controller Attempt017 Mechanism Batch Remote Instructions 2026-05-13

## Purpose

Run one small controller-only attempt017 mechanism batch after the mechanism-target patch.

This run should test concrete daily-stock-only mechanisms, not generic signal dampening:

```yaml
priority_targets:
  - portfolio/liquidity_weighted_sides
  - portfolio/persistence_trade_gate
  - ranking/industry_neutral_rank
  - signal/liquidity_adjusted_reversal
  - risk/liquidity_scaled_cap
avoid_targets:
  - signal/bounded_tanh_dampening
  - signal/clipped_magnitude_dampening
```

This is not full validation, broad validation, or test-set use.

## Required Preflight

1. Pull the latest GitHub state.
2. Confirm the repo is clean or record any local patch in the artifact review.
3. Open a persistent terminal or `tmux` pane for Qwen/vLLM.
4. Launch Qwen3.5-9B and keep the server running.
5. From a separate terminal, verify both `/health` and `/v1/models`.
6. Only then run the controller command.

Qwen3.5-9B launch command:

```bash
CUDA_VISIBLE_DEVICES=0 vllm serve Qwen/Qwen3.5-9B \
  --served-model-name qwen35-9b-fast \
  --host 127.0.0.1 \
  --port 8001 \
  --max-model-len 32768 \
  --gpu-memory-utilization 0.90
```

If memory is tight, fall back to `--max-model-len 16384`. Keep child-generation completion tokens at `8192`.

Health checks from a different terminal:

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
  --out-dir artifacts/phase4_alphaevolve/controller_attempt017_mechanism_batch_20260513 \
  --db-path artifacts/phase4_alphaevolve/program_database.sqlite \
  --attempts 12 \
  --surface-schedule portfolio,ranking,portfolio,signal,risk,portfolio,ranking,signal,risk,portfolio,ranking,signal \
  --prior-summary artifacts/phase4_alphaevolve/controller_batch_001/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_batch_001_diversity_topup/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_batch_001_attempt017_repair_20260509/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_evaluator_hardening_smoke_20260510/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_attempt017_focused_round_20260511/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_attempt017_search_control_rerun_20260511/summary.json \
  --program-id-prefix PROG-20260513-A017-MECH \
  --max-tokens 8192
```

If an older prior-summary path is absent, record that in run notes and omit only that missing file. Keep the search-control rerun prior summary if available.

## Review Targets

Inspect the new eligibility fields before any sample evaluation:

```yaml
required_artifact_fields:
  sample_eval_eligibility_version: present
  sample_eval_candidate_count: present
  sample_eval_candidate_attempts: present
  sample_eval_candidate_program_ids: present
controller_mechanics:
  raw_parse_pass_rate: high
  compile_pass_rate: high
  vector_smoke_pass_rate: high
  portfolio_semantic_pass_rate: high
search_quality:
  target_intent_match_rate: higher_than_search_control_rerun
  behavioral_noop_count: lower_than_search_control_rerun
  sample_eval_candidate_count: 0_or_1_is_expected
forbidden_actions:
  full_validation_launched: false
  test_set_used: false
```

## Sample-Eval Rule

Do not sample-evaluate the whole batch.

Sample-evaluate at most one child, and only if:

```yaml
candidate_requirements:
  controller_decision: pass
  sample_eval_eligible: true
  target_intent_match: true
  final_weight_delta: true
  known_bad_dampening_family: false
  broad_controller_book: true
```

If no child satisfies those requirements, return only the controller artifact zip.

If one child qualifies, use attempt017 as the parent reference:

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
