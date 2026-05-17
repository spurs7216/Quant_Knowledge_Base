---
title: Controller Attempt017 Forced-Cell Smoke Remote Instructions 2026-05-17
type: project
status: active
updated: 2026-05-17
tags:
  - project
  - phase4
  - alphaevolve
  - remote-run
  - qwen
  - forced-cell
sources:
  - "controller_attempt017_novelty_smoke_review_20260517.md"
  - "forced_target_cell_schedule_patch_20260517.md"
  - "current_state.md"
---
# Controller Attempt017 Forced-Cell Smoke Remote Instructions 2026-05-17

## Purpose

Run one six-attempt **controller-only forced-cell smoke** after pulling the latest GitHub sync.

This is not sample evaluation and not a 27B mechanism-card run. It tests whether `--target-cell-schedule` can force the intended underfilled mechanism cells and avoid the surface-only routing failure seen in `controller_attempt017_novelty_smoke_20260516`.

## Scope

```yaml
parent: PROG-20260430-CHILD-0017
attempt_count: 6
generator_model: Qwen3.5-9B
reviewer_model: none
target_cell_schedule:
  - portfolio/liquidity_weighted_sides
  - portfolio/persistence_trade_gate
  - risk/liquidity_scaled_cap
  - risk/liquidity_scaled_cap
  - signal/liquidity_adjusted_reversal
  - signal/liquidity_adjusted_reversal
excluded_surfaces:
  - ranking
remote_sample_eval_auto_launch: false
broad_validation: false
full_validation: false
test_set_used: false
```

## Required Git Hygiene

```bash
git fetch origin
git status --short --branch
git rev-parse HEAD
git rev-parse origin/main
```

Preferred state:

```yaml
git_dirty: false
head_matches_origin_main: true
manifest_commit_fetchable_from_github: true
```

Do not run the research command from an unpushed research-code commit. Hygiene-only commits must be either pushed first or explicitly documented in the artifact.

## Qwen Preflight

Open a persistent terminal or `tmux` pane and launch Qwen3.5-9B:

```bash
CUDA_VISIBLE_DEVICES=0 vllm serve Qwen/Qwen3.5-9B \
  --served-model-name qwen35-9b-fast \
  --host 127.0.0.1 \
  --port 8001 \
  --max-model-len 32768 \
  --gpu-memory-utilization 0.90
```

If memory is tight, use `--max-model-len 16384`. Keep child-generation completion tokens at `8192`.

From a separate terminal:

```bash
curl -sf http://127.0.0.1:8001/health
curl -sf http://127.0.0.1:8001/v1/models
```

Only run the controller command after both checks pass.

## Controller-Only Command

```bash
python research/alphaevolve_lite/scripts/run_child_batch.py \
  --program-path artifacts/phase4_alphaevolve/controller_batch_001_diversity_topup/attempt_017/child_program.py \
  --parent-program-id PROG-20260430-CHILD-0017 \
  --evaluator-summary artifacts/phase4_alphaevolve/remote_sample_eval_controller_batch_001_topup_attempt_017_20260509/evaluator_summary.json \
  --out-dir artifacts/phase4_alphaevolve/controller_attempt017_forced_cell_smoke_20260517 \
  --db-path artifacts/phase4_alphaevolve/program_database.sqlite \
  --attempts 6 \
  --target-cell-schedule portfolio/liquidity_weighted_sides,portfolio/persistence_trade_gate,risk/liquidity_scaled_cap,risk/liquidity_scaled_cap,signal/liquidity_adjusted_reversal,signal/liquidity_adjusted_reversal \
  --prior-summary artifacts/phase4_alphaevolve/controller_batch_001/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_batch_001_diversity_topup/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_batch_001_attempt017_repair_20260509/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_evaluator_hardening_smoke_20260510/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_attempt017_focused_round_20260511/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_attempt017_search_control_rerun_20260511/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_attempt017_mechanism_batch_20260513/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_attempt017_mechanism_rerun_20260514/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_attempt017_27b_card_batch_20260514/summary.json \
  --program-id-prefix PROG-20260517-A017-FORCEDCELL \
  --max-tokens 8192
```

If a prior-summary path is absent, record the missing path in run notes and omit only that missing file.

## Required Artifact Checks

Inspect `summary.json`, `summary.md`, and each passing attempt's `micro_filter_result.json`.

```yaml
required_summary_fields:
  target_cell_schedule_enabled: true
  target_cell_schedule: present_and_matches_command
  sample_eval_eligibility_version: sample_eval_candidate_eligibility_v2
  git_head_matches_origin_main: true_preferred
  manifest_commit_fetchable_from_github: true_preferred
schedule_checks:
  ranking_attempt_count: 0
  forced_target_cell_present_on_each_attempt: true
  actual_target_surface_and_intent_match_forced_cell: true
eligibility_checks:
  no_final_weight_delta_children_ineligible: true
  occupied_map_cell_children_include_elite_comparison_fields: true_if_any
  target_intent_mismatch_children_ineligible: true_if_any
diagnostic_checks:
  duplicate_retry_terminal_failure_category_present: true_if_retry_attempted
  duplicate_retry_terminal_reason_present: true_if_retry_attempted_and_failed
forbidden_actions:
  remote_sample_eval_launched: false
  full_validation_launched: false
  test_set_used: false
```

## Return Artifact

Return the controller artifact directory or zip only:

```text
artifacts/phase4_alphaevolve/controller_attempt017_forced_cell_smoke_20260517
```

Do not run sample evaluation from the remote machine in this proof run, even if `sample_eval_candidate_count > 0`.
