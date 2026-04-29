---
title: Phase 4 Remote Qwen/vLLM Runtime Configuration
type: project
status: active
updated: 2026-04-29
tags: [phase4, alphaevolve, vllm, qwen, remote-runtime]
---

# Phase 4 Remote Qwen/vLLM Runtime Configuration

## Purpose

This file defines the remote-only LLM runtime policy for the Phase 4 AlphaEvolve-style quant research loop.

The local Windows machine is used for editing, Git operations, project planning, and artifact review. Any task that calls an LLM or runs heavy data work should execute on the remote Linux/GPU server.

## Security note

Do not commit Hugging Face tokens, broker credentials, API keys, SSH keys, or account information.

Set `HF_TOKEN` only in the remote shell, a private untracked `.env`, or the remote scheduler environment. If a real token was pasted into a committed file or shared text, rotate it on Hugging Face and replace it with `${HF_TOKEN}`.

## Remote entry

```bash
ssh -o LogLevel=ERROR b08303004@140.112.176.245 -p 2030
conda activate ae-vllm
```

## Environment variables

Use this in the remote terminal before launching any vLLM server.

```bash
conda activate ae-vllm

export HF_HOME=/home/b08303004/Desktop/HF_models
export TRANSFORMERS_CACHE=$HF_HOME/transformers
export HF_HUB_CACHE=$HF_HOME/hub
export HUGGINGFACE_HUB_CACHE=$HF_HOME/hub

# Set this interactively or through a private untracked remote .env.
# Do not commit a real token.
export HF_TOKEN=${HF_TOKEN}

export VLLM_WORKER_MULTIPROC_METHOD=spawn

# Required on this machine for multi-GPU Qwen deep models based on observed testing.
export NCCL_P2P_DISABLE=1
export NCCL_DEBUG=WARN

env | grep -E "HF_|HUGGINGFACE|TRANSFORMERS|XDG_CACHE|NCCL|VLLM"
```

## Active model stack

Gemma 4 is removed from the active stack.

| Role | Model | Served name | Port | GPU mode | Use |
|---|---|---:|---:|---|---|
| `fast_generator` | `Qwen/Qwen3.5-9B` | `qwen35-9b-fast` | `8001` | single GPU | default SEARCH/REPLACE generation and repair |
| `critic_repair` | `Qwen/Qwen3.5-9B` | `qwen35-9b-fast` | `8001` | single GPU | malformed patch repair, oversized SEARCH shrinkage |
| `medium_quality_reviewer` | `Qwen/Qwen3.5-27B-FP8` | `qwen35-27b-fp8` | `8020` | two GPUs | periodic medium-depth review; not default patch generator |
| `deep_generator` | `Qwen/Qwen3.6-35B-A3B-FP8` | `qwen36-35b-a3b-deep` | `8010` | two GPUs | scheduled deep review / mutation-surface synthesis |

## Launch policy

Run only the model needed for the current stage.

Default inner-loop mode uses only Qwen3.5-9B. The 27B and 35B models use both GPUs and should normally be launched only for scheduled review windows. Stop the 9B server before launching two-GPU models if GPU memory is constrained.

Before any command that calls Qwen, the remote agent must open a dedicated terminal or `tmux` pane, launch the required vLLM server there, and keep that server process running while the client/controller runs in a separate terminal. A closed terminal means there is no Qwen server. If `/health` or `/v1/models` fails, do not call the LLM; start or restart the matching server first.

Check GPU state first:

```bash
nvidia-smi
nvidia-smi --query-compute-apps=pid,process_name,gpu_uuid,used_memory --format=csv
ps -u $USER -f | grep -E "vllm|EngineCore|python" | grep -v grep
```

Stop old vLLM servers owned by the user:

```bash
pkill -TERM -u $USER -f "vllm|VLLM::EngineCore"
sleep 10
nvidia-smi
```

## Qwen3.5-9B fast generator

```bash
CUDA_VISIBLE_DEVICES=0 vllm serve Qwen/Qwen3.5-9B \
  --served-model-name qwen35-9b-fast \
  --dtype bfloat16 \
  --host 127.0.0.1 \
  --port 8001 \
  --api-key "${AE_VLLM_API_KEY}" \
  --tensor-parallel-size 1 \
  --max-model-len 16384 \
  --gpu-memory-utilization 0.55 \
  --max-num-seqs 2 \
  --enforce-eager \
  --reasoning-parser qwen3 \
  --language-model-only
```

## Qwen3.5-27B-FP8 medium reviewer

```bash
export NCCL_P2P_DISABLE=1
export NCCL_DEBUG=WARN

CUDA_VISIBLE_DEVICES=0,1 vllm serve Qwen/Qwen3.5-27B-FP8 \
  --served-model-name qwen35-27b-fp8 \
  --host 127.0.0.1 \
  --port 8020 \
  --api-key "${AE_VLLM_API_KEY}" \
  --tensor-parallel-size 2 \
  --max-model-len 16384 \
  --gpu-memory-utilization 0.40 \
  --max-num-seqs 1 \
  --enforce-eager \
  --reasoning-parser qwen3 \
  --language-model-only \
  --disable-custom-all-reduce
```

## Qwen3.6-35B-A3B-FP8 scheduled deep model

```bash
export NCCL_P2P_DISABLE=1
export NCCL_DEBUG=WARN

CUDA_VISIBLE_DEVICES=0,1 vllm serve Qwen/Qwen3.6-35B-A3B-FP8 \
  --served-model-name qwen36-35b-a3b-deep \
  --host 127.0.0.1 \
  --port 8010 \
  --api-key "${AE_VLLM_API_KEY}" \
  --tensor-parallel-size 2 \
  --max-model-len 16384 \
  --gpu-memory-utilization 0.40 \
  --max-num-seqs 1 \
  --enforce-eager \
  --reasoning-parser qwen3 \
  --language-model-only \
  --disable-custom-all-reduce
```

## Smoke tests

Health:

```bash
curl -s http://127.0.0.1:8001/health
```

Model list:

```bash
curl -s http://127.0.0.1:8001/v1/models \
  -H "Authorization: Bearer ${AE_VLLM_API_KEY}" | python -m json.tool
```

Chat:

```bash
curl -s http://127.0.0.1:8001/v1/chat/completions \
  -H "Authorization: Bearer ${AE_VLLM_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen35-9b-fast",
    "messages": [
      {"role": "user", "content": "Return exactly: qwen remote works"}
    ],
    "temperature": 0,
    "max_tokens": 32,
    "extra_body": {
      "chat_template_kwargs": {"enable_thinking": false}
    }
  }' | python -m json.tool
```

## Phase 4 controller policy

The AlphaEvolve-lite controller should run remotely, not locally.

The local Windows machine should not run Qwen calls, large data scans, or remote warehouse evaluators. The local machine writes code/specs, commits to GitHub, and reviews compact artifacts.

Remote controller stages:

1. `controller_static`: parse SEARCH/REPLACE, exact match, EVOLVE-block boundary, compile, vector smoke.
2. `toy_eval`: synthetic small-array validation.
3. `remote_sample_eval`: small remote daily-stock sample.
4. `remote_stage0_eval`: rolling top-500 validation subset.
5. `remote_full_validation`: full Stage 0 daily-stock validation with cost/null/stability diagnostics.
