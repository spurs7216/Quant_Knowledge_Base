---
title: Controller Attempt017 Novelty Smoke Remote Instructions 2026-05-16
type: project
status: active
updated: 2026-05-16
tags:
  - project
  - phase4
  - alphaevolve
  - remote-run
  - qwen
  - novelty-smoke
sources:
  - "current_state.md"
  - "sample_eval_novelty_hardening_20260515.md"
  - "remote_sample_eval_controller_attempt017_27b_card_batch_review_20260515.md"
  - "../../../CONTEXT.md"
---
# Controller Attempt017 Novelty Smoke Remote Instructions 2026-05-16

## Purpose

Run one six-attempt **Controller-Only Novelty Smoke**.

This is a proof run for search-control wiring, not a candidate-production batch and not sample evaluation. The run should verify that the latest controller artifacts expose the new sample-eval eligibility fields, prior-summary MAP-cell state, and reproducibility fields.

Do not run 27B for this proof run. Do not run remote sample evaluation automatically.

## Scope

```yaml
parent: PROG-20260430-CHILD-0017
attempt_count: 6
surface_schedule: portfolio,portfolio,risk,risk,signal,signal
excluded_surfaces:
  - ranking
generator_model: Qwen3.5-9B
reviewer_model: none
full_validation: false
broad_validation: false
test_set_used: false
```

Preferred underfilled mechanism cells:

```yaml
preferred_cells:
  - portfolio/liquidity_weighted_sides
  - portfolio/persistence_trade_gate
  - risk/liquidity_scaled_cap
  - signal/liquidity_adjusted_reversal
```

Do not schedule `ranking`. `ranking/industry_neutral_rank` is a negative-control cell for this branch, not a preferred target for this proof run.

## Required Git Hygiene

Before running:

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

If the remote machine has a local hygiene-only commit, either push it before the research run or record in the artifact review:

```yaml
local_hygiene_commit_only: true
research_code_diff_vs_origin_main: false
unpushed_commit_reason: "hygiene-only ignore rule"
```

Do not mix hygiene-only commits with research-code changes.

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
  --out-dir artifacts/phase4_alphaevolve/controller_attempt017_novelty_smoke_20260516 \
  --db-path artifacts/phase4_alphaevolve/program_database.sqlite \
  --attempts 6 \
  --surface-schedule portfolio,portfolio,risk,risk,signal,signal \
  --prior-summary artifacts/phase4_alphaevolve/controller_batch_001/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_batch_001_diversity_topup/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_batch_001_attempt017_repair_20260509/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_evaluator_hardening_smoke_20260510/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_attempt017_focused_round_20260511/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_attempt017_search_control_rerun_20260511/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_attempt017_mechanism_batch_20260513/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_attempt017_mechanism_rerun_20260514/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_attempt017_27b_card_batch_20260514/summary.json \
  --program-id-prefix PROG-20260516-A017-NOVELTY \
  --max-tokens 8192
```

If a prior-summary path is absent, record the missing path in run notes and omit only that missing file. Keep the two most recent mechanism summaries if available:

- `controller_attempt017_mechanism_rerun_20260514/summary.json`
- `controller_attempt017_27b_card_batch_20260514/summary.json`

Do not pass a `--mechanism-card-path` for this proof run. The point is to test current prompt memory, skill memory, diversity targets, and eligibility wiring without another 27B layer.

## Required Artifact Checks

Inspect `summary.json` and at least each passing attempt's `micro_filter_result.json`.

```yaml
required_summary_fields:
  sample_eval_eligibility_version: sample_eval_candidate_eligibility_v2
  sample_eval_candidate_count: present
  sample_eval_candidate_attempts: present
  sample_eval_candidate_program_ids: present
  git_head_matches_origin_main: true_preferred
  manifest_commit_fetchable_from_github: true_preferred
schedule_checks:
  ranking_attempt_count: 0
  surface_schedule: portfolio,portfolio,risk,risk,signal,signal
eligibility_checks:
  no_final_weight_delta_children_ineligible: true
  occupied_map_cell_children_include_elite_comparison_fields: true_if_any
  target_intent_mismatch_children_ineligible: true_if_any
forbidden_actions:
  remote_sample_eval_launched: false
  full_validation_launched: false
  test_set_used: false
```

## Return Artifact

Return the controller artifact directory or zip only:

```text
artifacts/phase4_alphaevolve/controller_attempt017_novelty_smoke_20260516
```

Do not run sample evaluation from the remote machine in this proof run, even if `sample_eval_candidate_count > 0`.

After Codex reviews the controller artifact locally, we may choose at most one child for sample evaluation. That later sample-eval command must include prior sibling summaries through `--prior-sample-summary`.
