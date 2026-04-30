---
title: Phase 4 Model Stack and vLLM Results
type: project
status: active
updated: 2026-04-30
tags:
  - project
  - phase4
  - qwen
  - vllm
  - model-stack
---
# Phase 4 Model Stack and vLLM Results

## Final Active Decision

Use a Qwen-only active model stack.

Gemma 4 is removed from the active loop because remote vLLM tests did not show enough incremental value relative to Qwen models. The system should not carry the operational complexity of another model family unless later evidence changes the decision.

All model serving and inference happens on the remote Linux/GPU server. The local Windows machine cannot launch Qwen because of memory constraints and must not be used for Phase 4 LLM calls.

## Model Roles

| Role | Model | Served name | Port | Status | Use |
| --- | --- | --- | ---: | --- | --- |
| `fast_generator` | `Qwen/Qwen3.5-9B` | `qwen35-9b-fast` | `8001` | primary | high-throughput SEARCH/REPLACE proposals |
| `critic_repair` | `Qwen/Qwen3.5-9B` | `qwen35-9b-fast` | `8001` | primary | malformed/oversized diff repair |
| `medium_quality_reviewer` | `Qwen/Qwen3.5-27B-FP8` | `qwen35-27b-fp8` | `8020` | optional | reviewer and medium-depth mutation-surface proposer |
| `deep_generator` | `Qwen/Qwen3.6-35B-A3B-FP8` | `qwen36-35b-a3b-deep` | `8010` | scheduled | hard prompts, deep review, search-state synthesis |
| `micro_filter` | deterministic Python | n/a | n/a | mandatory | parse, exact-match, evolve-block, AST/name, compile, vector smoke |

## Measured Remote vLLM Results

Measured model claims must be backed by exact artifacts under:

```text
artifacts/phase4_alphaevolve/model_tests/
```

Each model decision should link to `run_manifest.yaml`, `raw_terminal_log.txt`, `parsed_summary.json`, `model_endpoint.json`, `test_script_snapshot.py`, and `decision.md`. Current chat/session evidence must be formalized into that layout before these claims are treated as durable model evidence.

The 2026-04-30 remote evidence bundle also contains a lightweight model-test database record under `artifacts/phase4_alphaevolve/model_evidence_live/`. It confirms that `qwen35-9b-fast` on port `8001` responded after the remote agent launched the vLLM server, and that the hard smoke completed with one parse pass, one compile pass, and one vector-smoke pass. The first probe in `artifacts/phase4_alphaevolve/model_evidence/` failed with connection refused because the vLLM server was not running; this is an operator-preflight failure, not model evidence against Qwen.

Operational rule: before any LLM call, the remote agent must open a dedicated terminal or `tmux` pane, start the required Qwen/vLLM server, keep it running, and verify both `/health` and `/v1/models`.

| Model | Role decision | Evidence artifact |
| --- | --- | --- |
| `Qwen/Qwen3.5-9B` | primary `fast_generator` and `critic_repair` | `artifacts/phase4_alphaevolve/model_tests/qwen35_9b_hard_YYYYMMDD_HHMMSS/decision.md` |
| `Qwen/Qwen3.5-27B-FP8` | optional medium reviewer | `artifacts/phase4_alphaevolve/model_tests/qwen35_27b_fp8_YYYYMMDD_HHMMSS/decision.md` |
| `Qwen/Qwen3.6-35B-A3B-FP8` | scheduled deep reviewer/generator | `artifacts/phase4_alphaevolve/model_tests/qwen36_35b_a3b_fp8_YYYYMMDD_HHMMSS/decision.md` |

### Qwen3.5-9B

Decision: primary inner-loop model.

Observed strengths:

- strict SEARCH/REPLACE patch passed;
- oversized-patch repair passed;
- no undeclared names;
- no semantic warnings;
- compile passed;
- NumPy vector smoke passed;
- pandas vector smoke passed;
- critic JSON passed;
- medium-context JSON passed;
- 10/10 batch strict-patch quality passed.

Use cases:

- normal child generation;
- repair;
- compact JSON critic tasks;
- remote controller search loop.

### Qwen3.5-27B-FP8

Decision: optional medium reviewer, not default patch generator.

Observed behavior:

- server and basic chat passed;
- critic JSON passed;
- medium-context JSON passed;
- patch syntax parsed;
- direct patch generation produced an oversized SEARCH block including function definition and EVOLVE markers, which the safety checker correctly rejected.

Use cases:

- review `search_state_summary.json` every 30 children;
- propose mutation surfaces, not direct code patches;
- critique evaluator summaries;
- help decide whether dataset admission is worth proposing.

### Qwen3.6-35B-A3B-FP8

Decision: scheduled deep model.

Observed behavior:

- needed `NCCL_P2P_DISABLE=1` and `--disable-custom-all-reduce` on the tested server;
- server and basic chat passed;
- strict patch passed;
- vector smoke passed;
- critic JSON passed;
- medium-context JSON passed;
- slower and uses both GPUs.

Use cases:

- deep review every 50 children;
- search-state synthesis;
- higher-level strategy logic;
- hard failure-mode analysis.

Do not use it for high-throughput child generation.

## Serving Commands

Run these commands only on the remote Linux/GPU server.

### Qwen3.5-9B

```bash
conda activate ae-vllm

CUDA_VISIBLE_DEVICES=0 vllm serve Qwen/Qwen3.5-9B \
  --served-model-name qwen35-9b-fast \
  --host 127.0.0.1 \
  --port 8001 \
  --api-key "${AE_VLLM_API_KEY}" \
  --tensor-parallel-size 1 \
  --max-model-len 8192 \
  --gpu-memory-utilization 0.55 \
  --max-num-seqs 2 \
  --enforce-eager \
  --reasoning-parser qwen3 \
  --language-model-only
```

### Qwen3.5-27B-FP8

```bash
conda activate ae-vllm

CUDA_VISIBLE_DEVICES=0 vllm serve Qwen/Qwen3.5-27B-FP8 \
  --served-model-name qwen35-27b-fp8 \
  --host 127.0.0.1 \
  --port 8020 \
  --api-key "${AE_VLLM_API_KEY}" \
  --tensor-parallel-size 1 \
  --max-model-len 4096 \
  --gpu-memory-utilization 0.85 \
  --max-num-seqs 1 \
  --enforce-eager \
  --reasoning-parser qwen3 \
  --language-model-only
```

If single GPU fails, run with tensor parallel size 2 and the same NCCL workaround used for the 35B model.

### Qwen3.6-35B-A3B-FP8

```bash
conda activate ae-vllm

export NCCL_P2P_DISABLE=1
export NCCL_DEBUG=WARN

CUDA_VISIBLE_DEVICES=0,1 vllm serve Qwen/Qwen3.6-35B-A3B-FP8 \
  --served-model-name qwen36-35b-a3b-deep \
  --host 127.0.0.1 \
  --port 8010 \
  --api-key "${AE_VLLM_API_KEY}" \
  --tensor-parallel-size 2 \
  --max-model-len 16384 \
  --gpu-memory-utilization 0.80 \
  --max-num-seqs 1 \
  --enforce-eager \
  --reasoning-parser qwen3 \
  --language-model-only \
  --disable-custom-all-reduce
```

The NCCL workaround is a performance/stability deployment setting, not a model-quality change.

## Runtime Policy

```yaml
runtime_policy:
  inner_loop:
    model: Qwen3.5-9B
    max_tokens: 4096
    temperature_grid: [0.0, 0.2, 0.5]

  repair:
    model: Qwen3.5-9B
    max_attempts: 1
    temperature: 0.0

  medium_review:
    model: Qwen3.5-27B-FP8
    frequency: every_30_children
    output_type: JSON_no_code

  deep_review:
    model: Qwen3.6-35B-A3B-FP8
    frequency: every_50_children
    output_type: JSON_no_code
```

## Quality Rule

Models never directly modify project files.

Every LLM output must pass:

1. deterministic parser;
2. exact SEARCH match;
3. EVOLVE-block boundary check;
4. forbidden-edit check;
5. AST/name check;
6. compile;
7. vector smoke;
8. evaluator summary schema.
