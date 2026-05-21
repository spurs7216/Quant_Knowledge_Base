---
title: Controller Attempt017 IS/OS Cost-Robustness Remote Instructions 2026-05-20
type: remote-handoff
status: ready
updated: 2026-05-21
tags:
  - project
  - phase4
  - alphaevolve
  - remote-run
  - qwen
  - forced-cell
sources:
  - "remote_sample_eval_is_os_forward_repair_review_20260520.md"
  - "controller_execution_effect_hardening_20260517.md"
  - "current_state.md"
---
# Controller Attempt017 IS/OS Cost-Robustness Remote Instructions 2026-05-20

## Purpose

Run one targeted controller-only batch from the repaired attempt017 parent lead.

This is not sample evaluation and not full validation. The purpose is to generate controller-safe children that try to preserve attempt017's OS strength while improving IS robustness, turnover, and cost sensitivity.

## Scope

```yaml
parent: PROG-20260430-CHILD-0017-ISOSREPAIR
attempt_count: 12
generator_model: Qwen3.5-9B
reviewer_model: none
remote_sample_eval_auto_launch: false
broad_validation: false
full_validation: false
test_set_used: false
target_cell_schedule:
  - portfolio/persistence_trade_gate
  - portfolio/no_trade_band_or_sparsity
  - portfolio/liquidity_weighted_sides
  - risk/liquidity_scaled_cap
  - portfolio/persistence_trade_gate
  - portfolio/no_trade_band_or_sparsity
  - portfolio/liquidity_weighted_sides
  - risk/liquidity_scaled_cap
  - portfolio/persistence_trade_gate
  - portfolio/no_trade_band_or_sparsity
  - portfolio/liquidity_weighted_sides
  - risk/liquidity_scaled_cap
deemphasized:
  - ranking/industry_neutral_rank
  - generic signal dampening
```

Do not run sample evaluation automatically even if the controller reports `sample_eval_candidate_count > 0`. Return the controller artifact first for local review.

## Required Git Hygiene

Run from a clean checkout that matches `origin/main`.

```bash
git fetch origin main
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

Do not run from an unpushed research-code commit. If local artifact-only files are needed to locate old child programs, record that explicitly in `review.md`; the executable research code must still come from `origin/main`.

## Qwen Preflight

Open a persistent terminal or `tmux` pane and launch Qwen3.5-9B. Keep this terminal open for the full run.

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
  --parent-program-id PROG-20260430-CHILD-0017-ISOSREPAIR \
  --evaluator-summary artifacts/phase4_alphaevolve/remote_sample_eval_attempt017_is_os_forward_repair_20260519/evaluator_summary.json \
  --out-dir artifacts/phase4_alphaevolve/controller_attempt017_is_os_cost_robustness_20260520 \
  --db-path artifacts/phase4_alphaevolve/program_database.sqlite \
  --attempts 12 \
  --target-cell-schedule portfolio/persistence_trade_gate,portfolio/no_trade_band_or_sparsity,portfolio/liquidity_weighted_sides,risk/liquidity_scaled_cap,portfolio/persistence_trade_gate,portfolio/no_trade_band_or_sparsity,portfolio/liquidity_weighted_sides,risk/liquidity_scaled_cap,portfolio/persistence_trade_gate,portfolio/no_trade_band_or_sparsity,portfolio/liquidity_weighted_sides,risk/liquidity_scaled_cap \
  --prior-summary artifacts/phase4_alphaevolve/controller_batch_001/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_batch_001_diversity_topup/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_batch_001_attempt017_repair_20260509/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_evaluator_hardening_smoke_20260510/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_attempt017_focused_round_20260511/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_attempt017_search_control_rerun_20260511/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_attempt017_mechanism_batch_20260513/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_attempt017_mechanism_rerun_20260514/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_attempt017_27b_card_batch_20260514/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_attempt017_novelty_smoke_20260516/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_attempt017_forced_cell_smoke_20260517/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_attempt017_execution_effect_smoke_20260517/summary.json \
  --program-id-prefix PROG-20260520-A017-ISOSCOST \
  --population-policy-version v2 \
  --duplicate-retry-attempts 1 \
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
forced_cell_checks:
  actual_target_surface_and_intent_match_forced_cell: true
  ranking_attempt_count: 0
  signal_attempt_count: 0
execution_effect_checks:
  pass_children_have_execution_effect_pass: true
  no_final_weight_delta_children_ineligible: true
portfolio_checks:
  broad_active_book: required_for_any_candidate
  both_long_and_short_books: required
  max_weight_discipline: required
  no_sparse_few_day_artifacts: required
forbidden_actions:
  remote_sample_eval_launched: false
  full_validation_launched: false
  test_set_used: false
```

## Candidate Review Rule

After the artifact returns, local review should consider sample evaluation only for children that satisfy all of:

- target cell matched the forced cell;
- execution-effect gate passed;
- broad active book;
- not a duplicate or near-duplicate of an occupied MAP-cell elite;
- no forbidden forward-return fields;
- no one-sided or materially net-exposed portfolio;
- plausible improvement path for turnover or cost sensitivity without simply shrinking the book.

When a later sample evaluation is launched, it must compare against the seed, repaired attempt017, and all prior attempt017-family sample summaries:

```text
remote_sample_eval_seed_is_os_forward_repair_20260519/evaluator_summary.json
remote_sample_eval_attempt017_is_os_forward_repair_20260519/evaluator_summary.json
remote_sample_eval_prog-20260513-a017-mech-0007_is_os_forward_repair_20260519/evaluator_summary.json
remote_sample_eval_prog-20260514-a017-mechfix-0009_is_os_forward_repair_20260519/evaluator_summary.json
remote_sample_eval_prog-20260514-a017-27bcard-0011_is_os_forward_repair_20260519/evaluator_summary.json
remote_sample_eval_prog-20260511-a017-focus-0000_is_os_forward_repair_20260519/evaluator_summary.json
```

This is required so metric-equivalent sibling replay is flagged.

## Return Artifact

Return only:

```text
artifacts/phase4_alphaevolve/controller_attempt017_is_os_cost_robustness_20260520
```

Do not run sample evaluation from the remote machine in this controller batch.
