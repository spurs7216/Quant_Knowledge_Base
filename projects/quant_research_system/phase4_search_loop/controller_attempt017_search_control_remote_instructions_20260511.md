---
title: Controller Attempt017 Search-Control Remote Instructions 2026-05-11
type: project
status: active
updated: 2026-05-11
tags:
  - phase4
  - alphaevolve
  - remote-run
  - qwen
sources:
  - "controller_attempt017_focused_round_review_20260511.md"
  - "current_state.md"
  - "remote_qwen_vllm_config.md"
---
# Controller Attempt017 Search-Control Remote Instructions 2026-05-11

## Purpose

Run one small controller-only focused attempt017 round after the search-control patch.

This is not broad validation, full validation, or test-set use. The patch adds parent-relative search rules, attempt017 negative sample-eval memory, and explicit avoid skills for generic signal dampening and portfolio/risk no-ops.

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

If memory is tight, fall back to `--max-model-len 16384`. Keep child-generation completion tokens at `8192`; the prior null-content issue was fixed by no-thinking routing, not by raising completion tokens.

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
  --out-dir artifacts/phase4_alphaevolve/controller_attempt017_search_control_rerun_20260511 \
  --db-path artifacts/phase4_alphaevolve/program_database.sqlite \
  --attempts 12 \
  --surface-schedule signal,portfolio,risk,ranking,signal,portfolio,risk,ranking \
  --prior-summary artifacts/phase4_alphaevolve/controller_batch_001/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_batch_001_diversity_topup/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_batch_001_attempt017_repair_20260509/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_evaluator_hardening_smoke_20260510/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_attempt017_focused_round_20260511/summary.json \
  --program-id-prefix PROG-20260511-A017-SCONTROL \
  --max-tokens 8192
```

If one of the older prior-summary paths is absent, record that in the run notes and omit only the missing file. Do not omit the focused-round prior summary if it is available, because it carries the latest no-op and dampening failure evidence.

## Review Targets

Inspect these before launching any data-backed sample evaluation:

```yaml
controller_mechanics:
  raw_parse_pass_rate: high
  exact_search_match_rate: high
  evolve_block_safe_rate: high
  compile_pass_rate: high
  vector_smoke_pass_rate: high
  portfolio_semantic_pass_rate: high
search_quality:
  behavioral_noop_count: lower_than_focused_round
  target_intent_match_rate: materially_above_focused_round
  duplicate_child_count: low
  near_duplicate_patch_count: low
  retrieved_reasoning_memory: includes_attempt017_negative_memory_when_relevant
  retrieved_skill_cards: includes_missing_held_or_noop_avoid_rules_when_relevant
forbidden_actions:
  full_validation_launched: false
  test_set_used: false
```

## Sample-Eval Rule

Do not sample-evaluate the whole batch.

Sample-evaluate at most one child, and only if it satisfies all of these:

```yaml
candidate_requirements:
  controller_decision: pass
  target_intent_match: true
  behavior_delta: nontrivial
  active_day_coverage: broad_in_smoke
  not_metric_equivalent_to_parent: plausible
  missing_held_mechanism: "not only generic bounded/clipped signal dampening"
  parent_relative_economics: "plausibly preserves or improves return and turnover-aware score"
```

If no child satisfies those requirements, return only the controller artifact zip and do not run sample evaluation.

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
