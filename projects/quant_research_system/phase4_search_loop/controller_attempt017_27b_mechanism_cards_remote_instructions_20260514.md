---
title: Controller Attempt017 27B Mechanism Cards Remote Instructions 2026-05-14
type: project
status: active
updated: 2026-05-14
tags:
  - project
  - phase4
  - alphaevolve
  - remote-run
  - qwen
  - mechanism-cards
sources:
  - "controller_attempt017_mechanism_rerun_review_20260514.md"
  - "model_stack_and_vllm_results.md"
  - "remote_csv_execution_policy.md"
---
# Controller Attempt017 27B Mechanism Cards Remote Instructions 2026-05-14

## Purpose

Run one 27B-assisted controller-only search step.

The 27B model is used only as a medium reviewer that emits JSON mechanism cards. It must not emit direct code patches. The 9B model remains the strict SEARCH/REPLACE patch generator.

This is not broad validation, full validation, or test-set use.

## Required Git Hygiene

Before running:

```bash
git fetch origin
git status --short --branch
git rev-parse HEAD
git rev-parse origin/main
```

Preferred:

```yaml
git_dirty: false
git_head_matches_origin_main: true
manifest_commit_fetchable_from_github: true
```

Do not run from an unpushed local research-code commit.

## Step 1: Start Qwen3.5-27B-FP8

Open a persistent terminal or `tmux` pane and launch the 27B reviewer:

```bash
conda activate ae-vllm

CUDA_VISIBLE_DEVICES=0 vllm serve Qwen/Qwen3.5-27B-FP8 \
  --served-model-name qwen35-27b-fp8 \
  --host 127.0.0.1 \
  --port 8020 \
  --api-key "${AE_VLLM_API_KEY}" \
  --tensor-parallel-size 1 \
  --max-model-len 8192 \
  --gpu-memory-utilization 0.90 \
  --max-num-seqs 1 \
  --enforce-eager \
  --reasoning-parser qwen3 \
  --language-model-only
```

If memory is tight, use `--max-model-len 4096` and keep `build_mechanism_cards.py --max-tokens 1536`.

From a second terminal:

```bash
curl -sf -H "Authorization: Bearer ${AE_VLLM_API_KEY}" http://127.0.0.1:8020/v1/models
curl -sf http://127.0.0.1:8020/health
```

## Step 2: Build Mechanism Cards

```bash
python research/alphaevolve_lite/scripts/build_mechanism_cards.py \
  --out-dir artifacts/phase4_alphaevolve/qwen27b_attempt017_mechanism_cards_20260514 \
  --controller-summary artifacts/phase4_alphaevolve/controller_attempt017_mechanism_rerun_20260514/summary.json \
  --controller-summary artifacts/phase4_alphaevolve/controller_attempt017_mechanism_batch_20260513/summary.json \
  --sample-eval-summary artifacts/phase4_alphaevolve/remote_sample_eval_controller_attempt017_mechanism_rerun_20260514_attempt_009/evaluator_summary.json \
  --sample-eval-summary artifacts/phase4_alphaevolve/remote_sample_eval_controller_attempt017_mechanism_batch_20260513_attempt_007/evaluator_summary.json \
  --sample-eval-summary artifacts/phase4_alphaevolve/remote_sample_eval_controller_batch_001_topup_attempt_017_20260509/evaluator_summary.json \
  --card-limit 6 \
  --temperature 0.2 \
  --max-tokens 1536
```

Expected artifacts:

```text
mechanism_cards.json
mechanism_cards.md
prompt.json
model_response.json
raw_output.txt
git_status.txt
git_diff_stat.txt
```

If 27B outputs malformed JSON, return the mechanism-card artifact and do not continue to 9B generation.

If one of the evidence summary paths is absent, record the missing path in the artifact review and omit only that argument. Do not substitute test-set or full-validation evidence.

## Step 3: Start Qwen3.5-9B

Stop the 27B server if GPU memory requires it. Then launch the 9B generator:

```bash
conda activate ae-vllm

CUDA_VISIBLE_DEVICES=0 vllm serve Qwen/Qwen3.5-9B \
  --served-model-name qwen35-9b-fast \
  --host 127.0.0.1 \
  --port 8001 \
  --api-key "${AE_VLLM_API_KEY}" \
  --tensor-parallel-size 1 \
  --max-model-len 32768 \
  --gpu-memory-utilization 0.90 \
  --max-num-seqs 1 \
  --enforce-eager \
  --reasoning-parser qwen3 \
  --language-model-only
```

If memory is tight, use `--max-model-len 16384`. Keep child-generation completion tokens at `8192`.

Verify:

```bash
curl -sf -H "Authorization: Bearer ${AE_VLLM_API_KEY}" http://127.0.0.1:8001/v1/models
curl -sf http://127.0.0.1:8001/health
```

## Step 4: Run 9B Controller Batch With 27B Cards

```bash
python research/alphaevolve_lite/scripts/run_child_batch.py \
  --program-path artifacts/phase4_alphaevolve/controller_batch_001_diversity_topup/attempt_017/child_program.py \
  --parent-program-id PROG-20260430-CHILD-0017 \
  --evaluator-summary artifacts/phase4_alphaevolve/remote_sample_eval_controller_batch_001_topup_attempt_017_20260509/evaluator_summary.json \
  --out-dir artifacts/phase4_alphaevolve/controller_attempt017_27b_card_batch_20260514 \
  --db-path artifacts/phase4_alphaevolve/program_database.sqlite \
  --attempts 12 \
  --surface-schedule ranking,portfolio,risk,ranking,portfolio,risk,ranking,portfolio,ranking,portfolio,risk,ranking \
  --prior-summary artifacts/phase4_alphaevolve/controller_batch_001/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_batch_001_diversity_topup/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_batch_001_attempt017_repair_20260509/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_evaluator_hardening_smoke_20260510/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_attempt017_focused_round_20260511/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_attempt017_search_control_rerun_20260511/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_attempt017_mechanism_batch_20260513/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_attempt017_mechanism_rerun_20260514/summary.json \
  --mechanism-card-path artifacts/phase4_alphaevolve/qwen27b_attempt017_mechanism_cards_20260514/mechanism_cards.json \
  --mechanism-card-limit 3 \
  --program-id-prefix PROG-20260514-A017-27BCARD \
  --max-tokens 8192
```

If a prior-summary path is absent, record it in the artifact review and omit only that missing file.

## Review Rule

Return the controller artifact before launching any sample evaluation unless the local reviewer explicitly authorizes one.

At local review, require:

```yaml
controller_decision: pass
sample_eval_eligible: true
target_intent_match: true
final_weight_delta: true
broad_controller_book: true
mechanism_card_ids_present: true
known_bad_signal_dampening: false
```

The new child should be judged against both:

- attempt017 parent: stronger alpha metrics but worse implementation shape;
- attempt009 child: better turnover/missing-held/drawdown but weaker parent-relative Sharpe/return.

Do not promote a child for improving missing-held weight alone.
