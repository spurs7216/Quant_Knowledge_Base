---
title: Controller Evaluator Hardening Remote Instructions 2026-05-10
type: project
status: active
updated: 2026-05-10
tags:
  - phase4
  - alphaevolve
  - remote-run
  - qwen
sources:
  - "controller_batch_001_attempt017_repair_hardening_20260510.md"
  - "controller_batch_001_attempt017_repair_remote_instructions_20260509.md"
  - "current_state.md"
---
# Controller Evaluator Hardening Remote Instructions 2026-05-10

Supersession note: this dated handoff used the old 2018-2020 sample-evaluation window. Future sample evaluations must use the fixed 2011-2025 IS/OS policy in [is_os_evaluation_policy_20260519.md](is_os_evaluation_policy_20260519.md).

## Purpose

Run a small controller-only smoke/top-up after the 2026-05-10 hardening patch.

This is not market validation, full validation, or test-set use. The goal is to verify that the remote Qwen/controller path still works after:

- parent-offspring seeding fix;
- exact smoke no-op rejection;
- behavior-delta MAP buckets;
- prompt-card reroute policy;
- sample-eval exposure diagnostics.

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
  --out-dir artifacts/phase4_alphaevolve/controller_evaluator_hardening_smoke_20260510 \
  --db-path artifacts/phase4_alphaevolve/program_database.sqlite \
  --attempts 6 \
  --surface-schedule signal,portfolio,risk,ranking \
  --prior-summary artifacts/phase4_alphaevolve/controller_batch_001/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_batch_001_diversity_topup/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_batch_001_attempt017_repair_20260509/summary.json \
  --program-id-prefix PROG-20260510-A017-HARDEN \
  --max-tokens 8192
```

## Review Targets

Inspect these fields before any sample evaluation:

```yaml
controller_mechanics:
  raw_parse_pass_rate: high
  exact_search_match_rate: high
  evolve_block_safe_rate: high
  compile_pass_rate: high
  vector_smoke_pass_rate: high
  portfolio_semantic_pass_rate: high
new_hardening_fields:
  parent_offspring_counts: "attempt017 should not inherit old missing-parent children"
  behavior_delta_pass_rate: reported
  behavioral_noop_count: reported
  prompt_card_reroute_policy: reported
  map_cell_key: "should include portfolio_delta/rank_delta/gross_delta buckets"
forbidden_actions:
  remote_sample_eval_launched: false
  full_validation_launched: false
  test_set_used: false
```

## Later Sample-Eval Rule

If this controller smoke is healthy, select only one behaviorally nontrivial child for sample evaluation. Prefer a signal smoothing / volatility-scaling child over gross-only dampening.

Use attempt017 as the active reference, because these children mutate attempt017:

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

The seed-reference summary remains useful context, but attempt017 is the correct parent-relative comparison for this repair family.
