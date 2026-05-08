---
title: Controller Batch 001 Small Semantic v4 Review
type: project
status: accepted
updated: 2026-05-08
tags:
  - project
  - phase4
  - alphaevolve
  - controller-static
  - artifact-review
sources:
  - "artifacts/controller_batch_001_small_semantic_v4.zip"
  - "current_state.md"
  - "codex_implementation_tasks.md"
---
# Controller Batch 001 Small Semantic v4 Review

## Decision

Accept `controller_batch_001_small_semantic_v4` as the small-batch controller-static pass.

This decision does not mean that a child strategy has market alpha. It only means the remote Qwen/controller path is now healthy enough to scale from a 10-attempt controller batch to a 50-attempt controller batch.

## Artifact

```text
artifacts/controller_batch_001_small_semantic_v4.zip
```

The zip contains `summary.json`, `summary.md`, per-attempt artifacts, reasoning-memory update files, skill-library update files, and evaluator/controller diagnostic reports.

## Key Metrics

```yaml
attempt_count: 10
pass_count: 10
raw_parse_pass_rate: 1.0
exact_search_match_rate: 1.0
evolve_block_safe_rate: 1.0
apply_pass_rate: 1.0
compile_pass_rate: 1.0
vector_smoke_pass_rate: 1.0
portfolio_semantic_pass_rate: 1.0
unique_child_pass_rate: 1.0
db_insert_pass_rate: 1.0
empty_retry_rate: 0.0
reasoning_only_empty_count: 0
duplicate_child_count: 0
duplicate_patch_fingerprint_count: 0
duplicate_retry_attempt_rate: 0.2
duplicate_retry_success_rate: 1.0
map_cell_count: 8
map_cell_duplicate_count: 2
remote_sample_eval_launched: false
full_validation_launched: false
```

## What Worked

- Qwen returned usable final content; the earlier null-content / reasoning-only failure did not recur.
- SEARCH/REPLACE parsing, exact matching, evolve-block boundary checks, compile, vector smoke, portfolio semantic checks, and database insertion all passed.
- Duplicate retry was exercised and succeeded.
- MAP-cell tracking reported diversity rather than only child-hash uniqueness.
- Reasoning-memory, diagnostic, and skill-library artifacts were produced.

## Caveats

- This is controller-static evidence only. No generated child has been evaluated on historical market data.
- The toy vector-smoke Sharpe values are not market evidence.
- MAP diversity is improved but not perfect: 10 children occupied 8 cells, and 2 attempts landed in already occupied cells.
- Some generated patches may be shallow or close to no-op refactors. Do not evaluate all children blindly.
- Candidate memory and skill updates remain low-confidence until supported by larger controller evidence and later data-backed evaluator evidence.
- The parent seed remains weak under the sample evaluator: cost/turnover fragility, negative net Sharpe, sign-flip-better diagnostics, and missing-held-weight caveats remain active.

## Next Step

Run `controller_batch_001`, a 50-attempt controller-only remote batch using the same Qwen3.5-9B fast-generator path, reasoning-memory cards, diagnostic cards, skill cards, duplicate retry, and MAP-cell reporting.

Do not launch child `remote_sample_eval`, stage-0 evaluation, full validation, or test-set evaluation during this batch.

After the 50-attempt batch, review `summary.json`, group-relative controller report, diagnostics, and skill updates. If the larger batch passes, select a smaller diverse set of nontrivial children for the first data-backed `remote_sample_eval`.
