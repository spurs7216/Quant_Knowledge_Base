---
title: Controller Attempt017 Mechanism Rerun Remote Instructions 2026-05-14
type: project
status: active
updated: 2026-05-14
tags:
  - project
  - phase4
  - alphaevolve
  - remote-run
  - qwen
  - mechanism-rerun
sources:
  - "controller_attempt017_mechanism_batch_review_20260514.md"
  - "controller_prompt_smoke_repair_20260514.md"
  - "remote_csv_execution_policy.md"
---
# Controller Attempt017 Mechanism Rerun Remote Instructions 2026-05-14

Supersession note: this dated handoff used the old 2018-2020 sample-evaluation window. Future sample evaluations must use the fixed 2011-2025 IS/OS policy in [is_os_evaluation_policy_20260519.md](is_os_evaluation_policy_20260519.md).

## Purpose

Run one small controller-only rerun after the local prompt/smoke repair.

The goal is to test direct daily-stock mechanisms that can validly access extra fields inside each EVOLVE-block scope. This is not broad validation, full validation, or test-set use.

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

If the remote machine has a local hygiene-only commit, such as ignoring `.codex/`, either push it before the research run or record in the artifact review:

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

## Controller-Only Command

```bash
python research/alphaevolve_lite/scripts/run_child_batch.py \
  --program-path artifacts/phase4_alphaevolve/controller_batch_001_diversity_topup/attempt_017/child_program.py \
  --parent-program-id PROG-20260430-CHILD-0017 \
  --evaluator-summary artifacts/phase4_alphaevolve/remote_sample_eval_controller_batch_001_topup_attempt_017_20260509/evaluator_summary.json \
  --out-dir artifacts/phase4_alphaevolve/controller_attempt017_mechanism_rerun_20260514 \
  --db-path artifacts/phase4_alphaevolve/program_database.sqlite \
  --attempts 12 \
  --surface-schedule portfolio,risk,portfolio,ranking,portfolio,risk,ranking,portfolio,risk,ranking,portfolio,risk \
  --prior-summary artifacts/phase4_alphaevolve/controller_batch_001/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_batch_001_diversity_topup/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_batch_001_attempt017_repair_20260509/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_evaluator_hardening_smoke_20260510/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_attempt017_focused_round_20260511/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_attempt017_search_control_rerun_20260511/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_attempt017_mechanism_batch_20260513/summary.json \
  --program-id-prefix PROG-20260514-A017-MECHFIX \
  --max-tokens 8192
```

If a prior-summary path is absent, record it in the artifact review and omit only that missing file.

## Review Rule

Inspect `summary.json` before any sample evaluation.

Require:

```yaml
raw_parse_pass_rate: high
compile_pass_rate: high
vector_smoke_pass_rate: materially_above_0.5
portfolio_semantic_pass_rate: materially_above_0.5
sample_eval_candidate_count: 0_or_1
candidate_should_prefer_direct_mechanism: true
```

Do not sample-evaluate signal/liquidity_adjusted_reversal again unless the artifact review gives a specific reason that it is materially different from `PROG-20260513-A017-MECH-0007`.

Sample-evaluate at most one child, only if:

```yaml
controller_decision: pass
sample_eval_eligible: true
target_intent_match: true
final_weight_delta: true
broad_controller_book: true
preferred_intent:
  - portfolio/liquidity_weighted_sides
  - portfolio/persistence_trade_gate
  - risk/liquidity_scaled_cap
  - ranking/industry_neutral_rank
```

Use attempt017 as the reference if a child qualifies:

```bash
python research/alphaevolve_lite/scripts/remote_sample_eval.py \
  --csv-path /home/b08303004/Desktop/WRDS/data/daily_stock/gago9dveytpx6922.csv \
  --program-path <selected_child_program.py> \
  --program-id <selected_child_program_id> \
  --parent-program-id PROG-20260430-CHILD-0017 \
  --reference-summary artifacts/phase4_alphaevolve/remote_sample_eval_controller_batch_001_topup_attempt_017_20260509/evaluator_summary.json \
  --out-dir <selected_child_sample_eval_out_dir> \
  --db-path artifacts/phase4_alphaevolve/program_database.sqlite \
  --start-date 2018-01-01 \
  --end-date 2020-12-31 \
  --top-n 500 \
  --total-cost-bps 2.5 \
  --null-seeds 10
```
