---
title: Controller Batch 001 Review
type: project
status: revise
updated: 2026-05-09
tags:
  - project
  - phase4
  - alphaevolve
  - controller-static
  - artifact-review
sources:
  - "artifacts/controller_batch_001.zip"
  - "current_state.md"
  - "controller_batch_001_remote_instructions_20260508.md"
---
# Controller Batch 001 Review

## Decision

Do not launch child `remote_sample_eval` yet.

`controller_batch_001` proves that the controller mechanics are healthy at 50 attempts, but it does not meet the predeclared uniqueness gate. The run produced 35 unique controller-static pass children out of 50 attempts, below the target of at least 40. The remaining obstacle is duplicate generation, concentrated in `ranking/direction_flip`.

This is not a market evaluation and not an AlphaEvolve improvement round.

## Artifact

```text
artifacts/controller_batch_001.zip
```

The zip contains `summary.json`, `summary.md`, per-attempt artifacts, reasoning-memory update files, skill-library update files, and evaluator/controller diagnostic reports.

## Key Metrics

```yaml
attempt_count: 50
pass_count: 35
raw_parse_pass_rate: 1.0
exact_search_match_rate: 1.0
evolve_block_safe_rate: 1.0
apply_pass_rate: 1.0
compile_pass_rate: 1.0
vector_smoke_pass_rate: 1.0
portfolio_semantic_pass_rate: 1.0
db_insert_pass_rate: 1.0
empty_retry_rate: 0.0
reasoning_only_empty_count: 0
unique_child_pass_rate: 0.70
duplicate_child_count: 15
duplicate_patch_fingerprint_count: 0
duplicate_retry_attempt_rate: 0.60
duplicate_retry_success_rate: 0.50
map_cell_count: 12
map_cell_duplicate_count: 23
remote_sample_eval_launched: false
full_validation_launched: false
```

## Surface Breakdown

```yaml
signal:
  attempts: 13
  pass: 12
  duplicate_rejects: 1
risk:
  attempts: 12
  pass: 11
  duplicate_rejects: 1
portfolio:
  attempts: 12
  pass: 9
  duplicate_rejects: 3
ranking:
  attempts: 13
  pass: 3
  duplicate_rejects: 10
```

Intent-level concentration:

```yaml
ranking_direction_flip:
  attempts: 10
  pass: 1
  duplicate_rejects: 9
risk_side_renormalization:
  attempts: 12
  pass: 11
  duplicate_rejects: 1
signal_clipped_magnitude_dampening:
  attempts: 7
  pass: 6
  duplicate_rejects: 1
portfolio_equal_side_weight_refactor:
  attempts: 6
  pass: 5
  duplicate_rejects: 1
```

## What Worked

- Qwen returned nonempty final content; the reasoning-only null-output failure did not recur.
- SEARCH/REPLACE parsing, exact matching, evolve-block containment, marker preservation, compile, vector smoke, portfolio semantic checks, and database insertion all passed.
- The semantic gate is doing the right job: it is checking program and portfolio invariants, not pretending to test alpha.
- Reasoning-memory, diagnostic, skill-library, and group-relative controller reports were written.
- MAP-cell count reached 12, meeting the small diversity-count target, but many attempts landed in occupied cells.

## Diagnosis

The failure is search-policy diversity, not controller correctness.

The model repeatedly used the easy `ranking/direction_flip` mutation even when the target behavior cell asked for other ranking intents such as rank transform or robust center/scale. The prompt supplied a target cell, but the generic ranking guidance still described direction flipping as a suitable ranking change. That ambiguity gave Qwen a cheap repeated mutation path.

A second issue matters for the next run: a new controller batch must not start duplicate detection from an empty in-memory set. A diversity top-up should seed prior child hashes, patch fingerprints, occupied MAP cells, and accepted patches from `controller_batch_001/summary.json`; otherwise it can regenerate children that already passed in this batch.

## Applied Local Fix

The local scaffold has been patched so the next controller run can be a real diversity top-up:

- target behavior intent is now explicit in the prompt contract;
- sign or direction flips are disallowed unless `intended_patch_intent` is `direction_flip`;
- generic ranking guidance no longer encourages direction flipping for every ranking target;
- `run_child_batch.py` now accepts `--surface-schedule` for targeted top-up schedules;
- `run_child_batch.py` now accepts repeatable `--prior-summary` inputs and seeds duplicate/MAP state from prior attempt records.
- `controller_population_policy_v2` now tracks surface/intent saturation, prompt-card duplicate counts, prompt-card fitness, lazy penalties, and edit-signature near duplicates.
- Batch artifacts now report `prompt_fitness_policy_version`, `controller_search_score_mean`, `lazy_penalty_attempt_count`, `prompt_card_fitness`, and `prompt_card_lazy_penalty_sums`.

## Next Step

Run a 20-attempt controller-only diversity top-up after pulling the local patch. Do not run `remote_sample_eval` during the top-up.

Primary goal:

```yaml
aggregate_goal:
  previous_unique_children: 35
  topup_unique_children_target: "at least 12 of 20"
  aggregate_unique_children_target: "at least 45"
  duplicate_child_count_target: "materially below controller_batch_001"
  remote_sample_eval_launched: false
```

If the top-up clears the diversity gate, then select a small diverse subset of controller-static children for the first `remote_sample_eval`. Do not evaluate all generated children blindly.
