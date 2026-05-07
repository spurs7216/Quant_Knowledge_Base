---
title: Phase 4 Controller Batch 001 Small Review
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
  - "controller_child_dry_run_20260430.md"
  - "prompt_contracts.md"
superseded_by: "current_state.md"
---
# Phase 4 Controller Batch 001 Small Review

> Current compact state: [current_state.md](current_state.md). This dated note is retained as supporting evidence for the first failed controller batch.

## Artifact

Reviewed local artifact:

```text
artifacts/controller_batch_001_small.zip
```

Extracted review copy:

```text
artifacts/controller_batch_001_small_review_20260430_v2/controller_batch_001_small
```

## Result

The remote interpretation is mostly correct: the Qwen/router/database path worked, but no child was controller-safe.

Summary:

```yaml
attempt_count: 5
pass_count: 0
raw_parse_pass_rate: 1.0
exact_search_match_rate: 1.0
evolve_block_safe_rate: 0.0
apply_pass_rate: 0.0
compile_pass_rate: 0.0
vector_smoke_pass_rate: 0.0
db_insert_pass_rate: 1.0
failure_categories:
  outside_evolve_block: 5
```

The useful evidence is that Qwen generated parseable SEARCH/REPLACE blocks, the exact-match stage worked, and all attempts were inserted into the program database. The failure was concentrated at the evolve-block boundary.

## Failure Pattern

Attempt-level pattern:

```yaml
attempt_000:
  parsed_blocks: 2
  reason: SEARCH block includes EVOLVE marker
  note: plausible signal/portfolio idea, but copied marker lines

attempt_001:
  parsed_blocks: 1
  reason: SEARCH block is not strictly inside an EVOLVE block
  note: edited helper function `_kalman_innovation_reversal`, outside allowed surface

attempt_002:
  parsed_blocks: 5
  reason: SEARCH block is not strictly inside an EVOLVE block
  note: mixed helper/default-param edits with one inside-block edit; too many changes

attempt_003:
  parsed_blocks: 2
  reason: SEARCH block includes EVOLVE marker
  note: ranking idea was plausible, but copied marker lines; second block also misplaced marker handling

attempt_004:
  parsed_blocks: 2
  reason: SEARCH block is not strictly inside an EVOLVE block
  note: helper edit plus marker-including portfolio edit
```

## Diagnosis

This is not evidence that Qwen cannot generate useful patches. It is evidence that the first prompt exposed too much code and did not route repair.

Specific causes:

- the prompt displayed the full seed program, including helpers and `DEFAULT_PARAMS`;
- the model copied `# EVOLVE-BLOCK-START` / `# EVOLVE-BLOCK-END` despite the instruction not to;
- multiple SEARCH/REPLACE blocks increased the chance that one unsafe block rejected the whole child;
- the controller had `repair_attempt_rate: 0.0`, even though Task 004 expected one repair attempt for malformed or oversized patches.

The micro-filter should stay strict. The right fix is to improve prompt sampling and add the missing repair module.

## Implemented Fix

Controller update:

- child-generation prompts now expose only the editable body of one target evolve block;
- target surfaces rotate deterministically across `signal`, `ranking`, `portfolio`, and `risk`;
- the generation prompt asks for exactly one SEARCH/REPLACE block;
- `run_child_batch.py` now performs one `critic_repair` call for repairable failures;
- summary output now includes `repair_attempt_rate` and `repair_success_rate`;
- attempt artifacts now preserve both initial and final micro-filter results.

Local mock verification:

```yaml
marker_oversize_mock:
  initial_result: outside_evolve_block
  repair_attempt_rate: 1.0
  repair_success_rate: 1.0
  final_pass_count: 1
  vector_smoke_pass_rate: 1.0
```

## Next Remote Run

Run a second small controller batch, still without child historical evaluation:

```bash
python research/alphaevolve_lite/scripts/run_child_batch.py \
  --program-path research/alphaevolve_lite/seeds/kalman_reversal_seed.py \
  --evaluator-summary artifacts/phase4_alphaevolve/remote_sample_eval_seed_v2/evaluator_summary.json \
  --out-dir artifacts/phase4_alphaevolve/controller_batch_001_small_repair_v1 \
  --db-path artifacts/phase4_alphaevolve/program_database.sqlite \
  --attempts 5 \
  --model-role fast_generator \
  --max-tokens 4096
```

Do not run child `remote_sample_eval`, stage-0 evaluation, full validation, or test-set evaluation from this batch.
