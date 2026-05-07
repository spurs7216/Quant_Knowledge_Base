---
title: Phase 4 Controller Child Dry Run
type: project
status: archived
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
superseded_by: "current_state.md"
---
# Phase 4 Controller Child Dry Run

> Current compact state: [current_state.md](current_state.md). This dated note is retained as supporting evidence for the first child dry-run protocol.

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

After `controller_batch_001_small`, the controller was tightened:

- generation prompts now expose only one target evolve-block body per attempt, not the whole seed program;
- target surfaces rotate across `signal`, `ranking`, `portfolio`, and `risk`;
- the prompt asks for exactly one SEARCH/REPLACE block;
- rejected repairable patches get one `critic_repair` pass;
- summaries report `repair_attempt_rate` and `repair_success_rate`.

After `controller_batch_001_small_repair_v1`, the controller was tightened again:

- `micro_filter` now enforces that SEARCH blocks are inside the requested target surface, not merely inside any evolve block;
- vector smoke now includes long/short semantic gates for net exposure, both-side presence, side-sign consistency, gross exposure, and max weight;
- `run_child_batch.py` detects duplicate child-program hashes;
- generation prompts include previous accepted patches for the same target surface to reduce repeated sign flips;
- `remote_sample_eval.py` accepts `--program-path` so generated children can be evaluated without hardcoding the seed.

After `controller_batch_001_small_semantic_v2`, the controller was tightened again:

- direct vLLM requests now send `chat_template_kwargs.enable_thinking=false` at the top level of the HTTP body;
- `model_router` records `content_was_null` and `reasoning_length`;
- empty final content gets one retry that explicitly asks for final SEARCH/REPLACE content;
- summaries report `reasoning_only_empty_count` and max initial reasoning length;
- vector-smoke and portfolio-semantic failures are now repairable once;
- prompts explicitly forbid hidden reasoning/scratchpad output and warn against saturated/tied signals or one-sided portfolios.

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
  --out-dir artifacts/phase4_alphaevolve/controller_batch_001_small_semantic_v3 \
  --db-path artifacts/phase4_alphaevolve/program_database.sqlite \
  --attempts 10 \
  --model-role fast_generator \
  --max-tokens 4096
```

Expected artifacts:

```text
artifacts/phase4_alphaevolve/controller_batch_001_small_semantic_v3/summary.md
artifacts/phase4_alphaevolve/controller_batch_001_small_semantic_v3/summary.json
artifacts/phase4_alphaevolve/controller_batch_001_small_semantic_v3/attempt_*/prompt.json
artifacts/phase4_alphaevolve/controller_batch_001_small_semantic_v3/attempt_*/raw_output.txt
artifacts/phase4_alphaevolve/controller_batch_001_small_semantic_v3/attempt_*/micro_filter_result.json
artifacts/phase4_alphaevolve/controller_batch_001_small_semantic_v3/attempt_*/child_program.py
```

If a repair is attempted, also inspect:

```text
artifacts/phase4_alphaevolve/controller_batch_001_small_semantic_v3/attempt_*/micro_filter_initial_result.json
artifacts/phase4_alphaevolve/controller_batch_001_small_semantic_v3/attempt_*/repair_prompt.json
artifacts/phase4_alphaevolve/controller_batch_001_small_semantic_v3/attempt_*/repair_output.txt
artifacts/phase4_alphaevolve/controller_batch_001_small_semantic_v3/attempt_*/repair_micro_filter_result.json
artifacts/phase4_alphaevolve/controller_batch_001_small_semantic_v3/attempt_*/empty_retry_*_response.json
```

## Review Gates

Review the small batch before launching child data evaluation.

Minimum things to check:

- Qwen server preflight passed and `/v1/models` served `qwen35-9b-fast`;
- raw outputs are strict SEARCH/REPLACE blocks or `NO_VALID_PATCH`;
- exact-match failures are explainable;
- all accepted SEARCH blocks are strictly inside evolve blocks;
- vector smoke failures are informative rather than infrastructure failures;
- portfolio semantic failures catch long-only, net-long, sign-inverted, or one-sided books;
- duplicate children are marked and not counted as unique passes;
- repair attempts preserve intended semantics instead of inventing unrelated patches;
- database insertion rate is measured;
- no child `remote_sample_eval`, stage-0 eval, full validation, or test-set evaluation was launched.

If the small dry run is healthy, the next scale-up is 50 controller attempts. Only after that should the best controller-static-passing children reach small `remote_sample_eval`.
