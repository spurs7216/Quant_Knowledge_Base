---
title: Expression Episode V2 Remote Instructions 20260531
type: remote_instructions
status: active
updated: 2026-05-31
tags:
  - project
  - phase4
  - expression-evolution
  - alphaevolve
  - remote-run
sources:
  - "current_state.md"
  - "phase4_caveat_repair_ledger.md"
  - "expression_episode_v2_memory_20260531.md"
  - "remote_qwen_vllm_config.md"
---
# Expression Episode V2 Remote Instructions 20260531

## Purpose

Run a second Qwen-backed expression-population episode after the bridge robustness rejection. This is a generation run, not promotion or full validation.

The goal is to resume multi-root population search with reviewed negative memory from `expression_bridge_robustness_20260526`.

## Stop Conditions

Stop and report without running generation if any of these fail:

- `git status --short` is non-empty before the run.
- `git rev-parse HEAD` differs from `git rev-parse origin/main`.
- The prior population ledger from `expression_episode_20260526` is missing.
- `projects/quant_research_system/phase4_search_loop/expression_episode_v2_memory_20260531.md` is missing.
- The Qwen server health or model-list check fails.
- The runner summary reports `status != ok`.
- The run uses any final test set evidence.

Do not run full validation. Do not promote a child.

## Git Preflight

```bash
git fetch origin
git status --short
test "$(git rev-parse HEAD)" = "$(git rev-parse origin/main)"
```

Expected: clean status and local `HEAD == origin/main`.

## Prior Artifact Preflight

The v2 run must load the prior expression population. If the prior artifact is only present as a zip, extract it first, preserving the directory name.

```bash
test -f artifacts/phase4_alphaevolve/expression_episode_20260526/expression_population_ledger.jsonl
test -f projects/quant_research_system/phase4_search_loop/expression_episode_v2_memory_20260531.md
```

If either file is absent, stop and report the missing path.

## Qwen Server

Open a dedicated terminal or `tmux` pane for the Qwen server. Keep it open while the runner executes in another terminal. A closed terminal means there is no Qwen server.

Use the active 9B fast-generator policy from [remote_qwen_vllm_config.md](remote_qwen_vllm_config.md):

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

If `--max-model-len 32768` OOMs, fall back to `16384`. Keep the completion budget at `8192` unless the artifact proves a context failure.

In the runner terminal:

```bash
curl -s http://127.0.0.1:8001/health
curl -s http://127.0.0.1:8001/v1/models \
  -H "Authorization: Bearer ${AE_VLLM_API_KEY}" | python -m json.tool
```

## Run Command

Replace the CSV path with the established remote `daily_stock` CSV path.

```bash
python research/alphaevolve_lite/scripts/run_expression_episode.py \
  --csv-path /path/to/daily_stock.csv \
  --out-dir artifacts/phase4_alphaevolve/expression_episode_v2_20260531 \
  --start-date 2011-01-01 \
  --end-date 2025-12-31 \
  --out-sample-start 2023-01-01 \
  --top-n 500 \
  --total-cost-bps 2.5 \
  --cost-grid-bps 0,1,2.5,5,10 \
  --bridge-variant-grid daily,rebalance_5,rebalance_5_offset_1,rebalance_5_offset_2,rebalance_5_offset_3,rebalance_5_offset_4,rebalance_10_offset_5,signal_decay_5,signal_decay_10 \
  --parent-seed-id expr_smoothed_rev \
  --parent-seed-id expr_mom_060_ind \
  --parent-seed-id expr_size_ind_rev \
  --turns 3 \
  --offspring-per-turn 2 \
  --parent-sampling-mode population_mixed \
  --prior-population-ledger artifacts/phase4_alphaevolve/expression_episode_20260526/expression_population_ledger.jsonl \
  --research-memory-file projects/quant_research_system/phase4_search_loop/expression_episode_v2_memory_20260531.md \
  --model-role fast_generator \
  --temperature-grid 0.3,0.5,0.7 \
  --max-tokens 8192 \
  --verify-each-call
```

## Required Artifacts

Zip the output directory and include:

- `expression_episode_summary.json`
- `expression_prompt_memory.json`
- `expression_episode_rankings.csv`
- `expression_episode_scorecard.csv`
- `expression_success_flags.csv`
- `expression_bridge_variants.csv`
- `expression_episode_cost_sensitivity.csv`
- `expression_population_ledger.jsonl`
- `expression_population_ledger.csv`
- `expression_parent_selection.jsonl`
- `expression_population_summary.json`
- `expression_population.sqlite`
- `expression_episode_model_calls.json`
- `model_calls/*/system_prompt.txt`
- `model_calls/*/user_prompt.md`
- `model_calls/*/model_response.json`
- Git reproducibility files written by the runner

Expected zip name:

```text
artifacts/expression_episode_v2_20260531.zip
```

## Review Questions

The local reviewer should answer:

- Did the run load the prior population ledger and the v2 research memory?
- Did later turns sample eligible survivors, or did all turns revert to roots?
- Is the duplicate or near-duplicate rate lower than v1?
- Did any child improve the primary daily bridge versus its parent and root?
- Does any child have positive after-cost IS and OS behavior with broad coverage?
- Do bridge diagnostics confirm robustness, or only expose a single lucky rebalance phase?
- Did any branch stop-loss trigger correctly?
- Was final test evidence unused?

