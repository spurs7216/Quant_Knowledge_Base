---
title: Expression Episode Remote Instructions 20260526
type: remote_instructions
status: active
updated: 2026-05-26
tags:
  - project
  - phase4
  - remote-run
  - expression-evolution
  - qwen
  - daily-stock
sources:
  - "expression_seed_zoo_review_20260525.md"
  - "daily_stock_expression_evolution_v1.md"
  - "remote_qwen_vllm_config.md"
  - "current_state.md"
---
# Expression Episode Remote Instructions 20260526

## Purpose

Run the first population-aware Qwen-backed daily-stock expression-evolution episode after the deterministic seed-zoo baseline.

This is a search/evidence run, not promotion. The goal is to test whether Qwen can propose safe expression-level mechanisms that improve cost conversion or IS/OS stability under the fixed daily-stock evaluator contract.

The run should use expression objects, not Python patches:

- JSON-only Qwen proposals;
- safe expression DSL validation;
- repaired rolling top-500 universe and forward-return source;
- fixed 2011-2025 IS/OS split;
- 2.5 bps default total cost plus cost grid;
- trajectory diagnostics with valid ratio, pass@T, consistency, exploration, and best child;
- parent-selection records, MAP-style population descriptors, and branch stop-loss diagnostics so this is not another fixed-parent repair loop.
- run-scoped child ids and a reloadable population ledger so later expression episodes can continue from prior survivors instead of restarting from memoryless seeds.
- explicit success flags and bridge-variant diagnostics so pass@T and turnover/cost caveats are not hidden inside one scalar score.

## Required Qwen Server Preflight

This run calls Qwen. Before running the episode command, the remote agent must open a dedicated terminal or `tmux` pane, launch the Qwen3.5-9B vLLM server, and keep that terminal running.

Use the 9B fast-generator endpoint:

```bash
conda activate ae-vllm

export HF_HOME=/home/b08303004/Desktop/HF_models
export TRANSFORMERS_CACHE=$HF_HOME/transformers
export HF_HUB_CACHE=$HF_HOME/hub
export HUGGINGFACE_HUB_CACHE=$HF_HOME/hub
export VLLM_WORKER_MULTIPROC_METHOD=spawn
export NCCL_P2P_DISABLE=1
export NCCL_DEBUG=WARN

# Set this only in the remote shell/private environment.
export AE_VLLM_API_KEY="${AE_VLLM_API_KEY}"

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

If `--max-model-len 32768` OOMs, restart with `--max-model-len 16384`. Keep the client completion budget at `8192`; the prior null-content issue was fixed by disabling thinking in `model_router.py`, not by using a larger completion budget.

In a second terminal, verify:

```bash
curl -s http://127.0.0.1:8001/health
curl -s http://127.0.0.1:8001/v1/models \
  -H "Authorization: Bearer ${AE_VLLM_API_KEY}" | python -m json.tool
```

Do not call the runner if `/health` or `/v1/models` fails.

## Repository Preflight

In the runner terminal:

```bash
git fetch origin
git status --short
git rev-parse HEAD
git rev-parse origin/main
```

Stop and report if:

- the worktree is dirty before the run;
- `HEAD` does not match `origin/main`;
- the daily_stock CSV path is unknown;
- the Qwen server is not running;
- `AE_VLLM_API_KEY` is missing in the remote runner shell.

## Command

Use the real remote daily_stock CSV path:

```bash
python research/alphaevolve_lite/scripts/run_expression_episode.py \
  --csv-path /path/to/daily_stock.csv \
  --out-dir artifacts/phase4_alphaevolve/expression_episode_20260526 \
  --start-date 2011-01-01 \
  --end-date 2025-12-31 \
  --out-sample-start 2023-01-01 \
  --top-n 500 \
  --total-cost-bps 2.5 \
  --cost-grid-bps 0,1,2.5,5,10 \
  --parent-seed-id expr_smoothed_rev \
  --parent-seed-id expr_size_ind_rev \
  --parent-seed-id expr_mom_060_ind \
  --turns 2 \
  --offspring-per-turn 2 \
  --parent-sampling-mode population_mixed \
  --branch-stop-loss-min-children 4 \
  --bridge-variant-grid daily,rebalance_5,signal_decay_5,no_trade_band_0.25 \
  --model-role fast_generator \
  --temperature-grid 0.2,0.4,0.6 \
  --max-tokens 8192
```

This first run should produce 3 parent baselines and up to 12 child expressions. Turn 1 mutates each root seed; later turns should sample eligible child survivors when available. If runtime is much lower than expected and all mechanics are clean, a later run can increase to 3 turns and 3 offspring per turn.

Do not pass `--prior-population-ledger` for this first expression episode. In later expression episodes, pass the previous run's `expression_population_ledger.jsonl` to seed duplicate checks and historical parent sampling.

## Required Artifacts

Zip the output directory and return it for local review.

Required files:

- `expression_episode_summary.json`
- `expression_episode_rankings.csv`
- `expression_episode_scorecard.csv`
- `expression_episode_cost_sensitivity.csv`
- `expression_episode_candidates.jsonl`
- `expression_population_ledger.jsonl`
- `expression_population_ledger.csv`
- `expression_parent_selection.jsonl`
- `expression_population_summary.json`
- `expression_population.sqlite`
- `expression_success_flags.csv`
- `expression_bridge_variants.csv`
- `expression_population_summary.json` must include `validation_exposure_summary`
- `expression_episode_model_calls.json`
- `expression_interface.md`
- `expression_seed_library.json`
- `universe_membership_monthly.csv`
- `universe_summary.csv`
- `split_manifest.yaml`
- `git_status.txt`
- `git_diff_stat.txt`
- `run_result.json`
- `model_calls/*/system_prompt.txt`
- `model_calls/*/user_prompt.md`
- `model_calls/*/model_response.json`

## Review Questions

The local reviewer should answer:

- Did Qwen return valid JSON content, or did null/malformed output recur?
- Which children were exact duplicates, near duplicates, expression errors, sample reviews, or sample passes?
- Did any child beat its parent on turnover-aware score after 2.5 bps?
- Did any child preserve broad coverage, balanced exposure, low max weight, and missing-held tolerance?
- Did any child improve both IS and OS evidence, or is it another regime/split artifact?
- Which parent produced the best trajectory diagnostics?
- Did turn 2 sample eligible child survivors, or did it correctly fall back to the seed because no child was eligible?
- Which MAP-style cells were occupied, and did any branch trigger a population-review pause?
- Are child expression ids run-scoped, and is the population ledger complete enough to seed a later episode?
- Do success flags distinguish parent/root beat, positive after-cost behavior, positive IS/OS behavior, coverage, sparsity, and duplicate risk?
- Do bridge variants show that lower-turnover execution could rescue an otherwise cost-fragile expression?
- Does validation exposure stay marked as development OS feedback only, with no final-test use?

## Stop Conditions

Stop and return artifacts without improvising if:

- the repository or Qwen preflight fails;
- no eligible daily_stock rows remain after static eligibility;
- rolling top-500 membership is empty;
- the runner exits nonzero;
- every model call is `model_parse_error` or empty output.

Do not run full validation and do not promote any expression from this episode.
