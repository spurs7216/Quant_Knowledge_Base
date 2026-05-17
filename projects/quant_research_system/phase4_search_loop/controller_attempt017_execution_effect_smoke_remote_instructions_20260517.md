---
title: Controller Attempt017 Execution-Effect Smoke Remote Instructions 2026-05-17
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
  - "controller_attempt017_forced_cell_smoke_review_20260517.md"
  - "controller_execution_effect_hardening_20260517.md"
  - "current_state.md"
---
# Controller Attempt017 Execution-Effect Smoke Remote Instructions 2026-05-17

## Purpose

Run one six-attempt controller-only smoke after pulling the execution-effect hardening patch.

This is not sample evaluation and not a 27B mechanism-card run. It tests whether the controller now rejects raw-signal-only or downstream-absorbed edits and whether Qwen can produce at least one target-matched child with observable final-book effect.

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

Do not run from an unpushed research-code commit.

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
  --out-dir artifacts/phase4_alphaevolve/controller_attempt017_execution_effect_smoke_20260517 \
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
  --prior-summary artifacts/phase4_alphaevolve/controller_attempt017_forced_cell_smoke_20260517/summary.json \
  --program-id-prefix PROG-20260517-A017-EXEFFECT \
  --max-tokens 8192
```

If a prior-summary path is absent, record it and omit only that missing path.

## Required Artifact Checks

```yaml
required_summary_fields:
  target_cell_schedule_enabled: true
  target_cell_schedule: present_and_matches_command
  execution_effect_pass_rate: present
  sample_eval_eligibility_version: sample_eval_candidate_eligibility_v2
  git_head_matches_origin_main: true_preferred
  manifest_commit_fetchable_from_github: true_preferred
schedule_checks:
  ranking_attempt_count: 0
  forced_target_cell_present_on_each_attempt: true
  actual_target_surface_and_intent_match_forced_cell: true
execution_effect_checks:
  raw_signal_only_liquidity_adjustment_rejected: true_if_generated
  execution_effect_failed_category_present: true_if_absorbed_patch_generated
  pass_children_have_execution_effect_pass: true
eligibility_checks:
  no_final_weight_delta_children_ineligible: true
  target_intent_mismatch_children_ineligible: true_if_any
forbidden_actions:
  remote_sample_eval_launched: false
  full_validation_launched: false
  test_set_used: false
```

## Return Artifact

Return only:

```text
artifacts/phase4_alphaevolve/controller_attempt017_execution_effect_smoke_20260517
```

Do not run sample evaluation from the remote machine in this proof run, even if `sample_eval_candidate_count > 0`.
