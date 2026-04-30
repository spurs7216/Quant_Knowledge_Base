---
title: Phase 4 Controller Child Dry Run
type: project
status: active
updated: 2026-04-30
tags:
  - project
  - phase4
  - alphaevolve
  - controller-static
  - qwen
sources:
  - "task_004_seed_strategy_program.md"
  - "prompt_contracts.md"
  - "remote_sample_eval_hardening_20260430.md"
---
# Phase 4 Controller Child Dry Run

## Purpose

The next milestone is a small remote controller child dry run, not child historical evaluation.

The seed `remote_sample_eval_seed_v2` result verified the daily-stock contract, duplicate handling, rolling universe, split handling, null controls, max-weight reporting, and prompt-ready evaluator summary. It also showed that the generation-zero seed is not an alpha yet: it loses after costs, has high turnover, and the sign-flipped baseline is better. That is enough evidence to ask Qwen for controlled strategy-code mutations, but not enough to evaluate generated children on historical data without first inspecting controller output quality.

## Implemented Controller Pieces

Code:

```text
research/alphaevolve_lite/prompt_builder.py
research/alphaevolve_lite/model_router.py
research/alphaevolve_lite/micro_filter.py
research/alphaevolve_lite/scripts/run_child_batch.py
```

The dry-run path builds a strict SEARCH/REPLACE prompt, calls the remote Qwen/vLLM server, applies deterministic controller-static filtering, writes per-attempt artifacts, and inserts every attempt into the SQLite program database when `--db-path` is supplied.

The child batch script intentionally writes:

```yaml
remote_sample_eval_launched: false
full_validation_launched: false
```

## Remote Preflight

Before running a non-mock batch, the remote agent must:

1. Open a dedicated remote terminal or `tmux` pane.
2. Launch the Qwen3.5-9B vLLM server there and keep it running.
3. Set `AE_VLLM_API_KEY` only in the remote shell or scheduler environment.
4. From a separate terminal, verify:

```text
http://127.0.0.1:8001/health
http://127.0.0.1:8001/v1/models
```

A connection-refused result is an operator-preflight failure, not a strategy failure.

## First Remote Command

Run:

```bash
python research/alphaevolve_lite/scripts/run_child_batch.py \
  --program-path research/alphaevolve_lite/seeds/kalman_reversal_seed.py \
  --evaluator-summary artifacts/phase4_alphaevolve/remote_sample_eval_seed_v2/evaluator_summary.json \
  --out-dir artifacts/phase4_alphaevolve/controller_batch_001_small \
  --db-path artifacts/phase4_alphaevolve/program_database.sqlite \
  --attempts 5 \
  --model-role fast_generator \
  --max-tokens 4096
```

Expected artifacts:

```text
artifacts/phase4_alphaevolve/controller_batch_001_small/summary.md
artifacts/phase4_alphaevolve/controller_batch_001_small/summary.json
artifacts/phase4_alphaevolve/controller_batch_001_small/attempt_*/prompt.json
artifacts/phase4_alphaevolve/controller_batch_001_small/attempt_*/raw_output.txt
artifacts/phase4_alphaevolve/controller_batch_001_small/attempt_*/micro_filter_result.json
artifacts/phase4_alphaevolve/controller_batch_001_small/attempt_*/child_program.py
```

## Review Gates

Review the small batch before launching child data evaluation.

Minimum things to check:

- Qwen server preflight passed and `/v1/models` served `qwen35-9b-fast`;
- raw outputs are strict SEARCH/REPLACE blocks or `NO_VALID_PATCH`;
- exact-match failures are explainable;
- all accepted SEARCH blocks are strictly inside evolve blocks;
- vector smoke failures are informative rather than infrastructure failures;
- database insertion rate is measured;
- no child `remote_sample_eval`, stage-0 eval, full validation, or test-set evaluation was launched.

If the small dry run is healthy, the next scale-up is 50 controller attempts. Only after that should the best controller-static-passing children reach small `remote_sample_eval`.
