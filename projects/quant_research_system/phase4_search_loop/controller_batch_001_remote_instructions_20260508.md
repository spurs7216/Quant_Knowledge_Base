---
title: Controller Batch 001 Remote Instructions
type: project
status: active
updated: 2026-05-08
tags:
  - project
  - phase4
  - alphaevolve
  - remote-run
  - controller-static
sources:
  - "controller_batch_001_small_semantic_v4_review_20260508.md"
  - "remote_qwen_vllm_config.md"
  - "codex_implementation_tasks.md"
---
# Controller Batch 001 Remote Instructions

## Purpose

Run the first larger Phase 4 controller-only batch after `controller_batch_001_small_semantic_v4` passed the small controller-static gate.

This is still not a market evaluation and not a full AlphaEvolve evolution round. The goal is to verify that the Qwen/controller path remains stable at 50 attempts and produces enough unique, semantically valid, diverse child programs for later selective `remote_sample_eval`.

## Non-Goals

Do not launch:

- child `remote_sample_eval`
- `remote_stage0_eval`
- `remote_full_validation`
- test-set evaluation
- IBKR, TWS, account, position, order, or broker tasks

## Remote Preflight

Run on the remote Linux/GPU/data server only.

1. Pull the latest GitHub state.
2. Activate the remote environment.
3. Open a dedicated terminal or `tmux` pane for vLLM.
4. Launch Qwen3.5-9B there and keep the server running.
5. From a separate terminal, verify `/health` and `/v1/models`.
6. Only after health and model-list checks pass, run the controller command.

Qwen3.5-9B launch command:

```bash
conda activate ae-vllm

export HF_HOME=/home/b08303004/Desktop/HF_models
export TRANSFORMERS_CACHE=$HF_HOME/transformers
export HF_HUB_CACHE=$HF_HOME/hub
export HUGGINGFACE_HUB_CACHE=$HF_HOME/hub
export VLLM_WORKER_MULTIPROC_METHOD=spawn
export NCCL_P2P_DISABLE=1
export NCCL_DEBUG=WARN

CUDA_VISIBLE_DEVICES=0 vllm serve Qwen/Qwen3.5-9B \
  --served-model-name qwen35-9b-fast \
  --dtype bfloat16 \
  --host 127.0.0.1 \
  --port 8001 \
  --api-key "${AE_VLLM_API_KEY}" \
  --tensor-parallel-size 1 \
  --max-model-len 32768 \
  --gpu-memory-utilization 0.55 \
  --max-num-seqs 1 \
  --enforce-eager \
  --reasoning-parser qwen3 \
  --language-model-only
```

Health checks from a separate terminal:

```bash
curl -s http://127.0.0.1:8001/health

curl -s http://127.0.0.1:8001/v1/models \
  -H "Authorization: Bearer ${AE_VLLM_API_KEY}" | python -m json.tool
```

If `--max-model-len 32768` fails due GPU memory, restart with `--max-model-len 16384` and keep the controller completion budget at `8192`.

## Controller Command

```bash
python research/alphaevolve_lite/scripts/run_child_batch.py \
  --program-path research/alphaevolve_lite/seeds/kalman_reversal_seed.py \
  --evaluator-summary artifacts/phase4_alphaevolve/remote_sample_eval_refactor_smoke_20260507/evaluator_summary.json \
  --out-dir artifacts/phase4_alphaevolve/controller_batch_001 \
  --db-path artifacts/phase4_alphaevolve/program_database.sqlite \
  --attempts 50 \
  --model-role fast_generator \
  --max-tokens 8192 \
  --memory-card-limit 3 \
  --diagnostic-card-limit 4 \
  --skill-card-limit 3 \
  --duplicate-retry-attempts 1
```

If `remote_sample_eval_refactor_smoke_20260507/evaluator_summary.json` is missing on the remote machine, use the behavior-equivalent seed-v2 evaluator summary:

```bash
--evaluator-summary artifacts/phase4_alphaevolve/remote_sample_eval_seed_v2/evaluator_summary.json
```

## Required Artifacts

The returned artifact bundle should include:

```text
artifacts/phase4_alphaevolve/controller_batch_001/summary.md
artifacts/phase4_alphaevolve/controller_batch_001/summary.json
artifacts/phase4_alphaevolve/controller_batch_001/reasoning_memory_loaded.json
artifacts/phase4_alphaevolve/controller_batch_001/reasoning_memory_update.md
artifacts/phase4_alphaevolve/controller_batch_001/reasoning_memory_update.json
artifacts/phase4_alphaevolve/controller_batch_001/skill_library_loaded.json
artifacts/phase4_alphaevolve/controller_batch_001/skill_update.md
artifacts/phase4_alphaevolve/controller_batch_001/skill_update.json
artifacts/phase4_alphaevolve/controller_batch_001/evaluator_diagnostic_report.md
artifacts/phase4_alphaevolve/controller_batch_001/controller_diagnostic_report.md
artifacts/phase4_alphaevolve/controller_batch_001/attempt_*/prompt.json
artifacts/phase4_alphaevolve/controller_batch_001/attempt_*/raw_output.txt
artifacts/phase4_alphaevolve/controller_batch_001/attempt_*/micro_filter_initial_result.json
artifacts/phase4_alphaevolve/controller_batch_001/attempt_*/micro_filter_result.json
artifacts/phase4_alphaevolve/controller_batch_001/attempt_*/child_program.py
```

If repair or retry happens, include the matching `repair_*`, `empty_retry_*`, and `duplicate_retry_*` artifacts.

## Review Gates

```yaml
expected:
  attempt_count: 50
  remote_sample_eval_launched: false
  full_validation_launched: false

controller_quality_targets:
  raw_parse_pass_rate: ">= 0.90"
  exact_search_match_rate: ">= 0.90"
  evolve_block_safe_rate: ">= 0.90"
  apply_pass_rate: ">= 0.90"
  compile_pass_rate: ">= 0.90"
  vector_smoke_pass_rate: ">= 0.85"
  portfolio_semantic_pass_rate: ">= 0.85"
  unique_child_pass_rate: ">= 0.80"
  db_insert_pass_rate: "near 1.0"

failure_targets:
  empty_retry_rate: "reported"
  reasoning_only_empty_count: 0
  duplicate_child_count: "low after retry"
  duplicate_patch_fingerprint_count: "low after retry"

diversity_targets:
  duplicate_retry_success_rate: "reported"
  map_cell_count: ">= 12 if descriptor space permits"
  map_cell_duplicate_count: "reported"
```

## If It Passes

Do not immediately evaluate all 50 children. First select a compact candidate set:

- top group-relative controller siblings;
- MAP-cell-diverse children;
- nontrivial strategy-logic changes;
- at most one representative from near-duplicate or shallow-refactor families.

Then run selective `remote_sample_eval` as the first data-backed child evaluation milestone.

## If It Fails

Do not weaken gates first. Inspect:

- `summary.json`
- failure categories
- raw outputs for malformed or reasoning-only responses
- repair outputs
- duplicate retry artifacts
- `micro_filter_initial_result.json`
- `micro_filter_result.json`
- map-cell occupancy and duplicate fingerprints

Change prompts or controller logic only after the failure category is clear.
