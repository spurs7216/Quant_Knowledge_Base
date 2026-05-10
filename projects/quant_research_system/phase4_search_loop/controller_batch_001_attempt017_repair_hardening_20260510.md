---
title: Controller Batch 001 Attempt017 Repair Hardening
type: project
status: active
updated: 2026-05-10
tags:
  - project
  - phase4
  - alphaevolve
  - controller
  - evaluator
sources:
  - "controller_batch_001_attempt017_repair_remote_instructions_20260509.md"
  - "remote_sample_eval_controller_batch_001_review_20260509.md"
  - "../../../wiki/methods/AlphaEvolve Lite Quant Search Workflow.md"
  - "../../../wiki/methods/AlphaEvolve Extension Methods for Quant Search.md"
  - "../../../wiki/methods/Reasoning Memory for AlphaEvolve Search.md"
---
# Controller Batch 001 Attempt017 Repair Hardening

## Decision

The next step is controller/evaluator hardening before another remote generation or sample-evaluation run.

The attempt017 repair artifact showed healthy Qwen/controller mechanics, but the pass children were still weak search evidence:

- several children were gross-exposure dampeners rather than true alpha or missing-held-weight repairs;
- one portfolio sparsity edit was effectively a no-op under the controller smoke panel;
- target-intent mismatch remained high;
- prior summaries without explicit `parent_id` were counted as offspring of the active attempt017 parent.

The AlphaEvolve extension notes support treating this as a search-control/database issue, not as a reason to weaken duplicate or semantic gates.

## Implemented Slice

Implemented locally on 2026-05-10:

1. `controller_population_policy.py`
   - Missing historical `parent_id` values now fall back to the seed parent, not the active parent passed to the new run.
   - Prompt cards with repeated duplicate, low-fitness, or no-nonduplicate-pass evidence receive an explicit reroute penalty during target selection.

2. `micro_filter.py`
   - Controller static filtering now compares parent and child behavior on the deterministic smoke panel.
   - Exact smoke no-ops are rejected as `behavioral_noop`.
   - Non-no-op children report signal, ranked-signal, weight, active-position, gross-exposure, and net-exposure deltas.

3. `diversity.py`
   - MAP cells now include behavior-delta buckets for portfolio, ranking, and gross-exposure change.
   - This makes MAP diversity more functional and less patch-text-only.

4. `sample_eval_metrics.py` and `remote_sample_eval.py`
   - Remote sample evaluation now reports exposure diagnostics:
     - mean/max gross exposure;
     - mean/max absolute net exposure;
     - long/short exposure;
     - long/short name counts.
   - These metrics are included in split metrics, reference comparisons, evaluator summaries, and review output.

5. Controller artifacts and diagnostics
   - Batch summaries now report `behavior_delta_pass_rate` and `behavioral_noop_count`.
   - Diagnostic cards include `diag_behavioral_noop_children` when smoke no-ops appear.
   - Reasoning-memory updates retain behavioral-noop failures as lazy-search evidence.

## Consequence

The controller should now distinguish:

- syntax-different but behavior-identical children;
- target-compliant children with real portfolio/ranking behavior change;
- gross-only exposure dampeners that need evaluator scrutiny;
- prompt cards that should be rerouted because they are repeatedly duplicate or lazy.

This does not prove alpha. It only makes the next AlphaEvolve-style loop closer to the intended four-module design:

- prompt sampler sees better population-state evidence;
- Qwen receives sharper negative examples;
- evaluator pools expose de-grossing and no-op artifacts;
- program database lineage is no longer distorted by missing historical parent IDs.

## Next Remote Step

After pushing and pulling this patch, run a small remote check before market evaluation:

1. Controller-static smoke/top-up with this hardening enabled.
2. Inspect:
   - `parent_offspring_counts`;
   - `behavior_delta_pass_rate`;
   - `behavioral_noop_count`;
   - `prompt_card_reroute_policy`;
   - MAP cells with delta buckets.
3. If controller mechanics remain healthy, sample-evaluate only the most behaviorally nontrivial child, likely the signal smoothing / volatility-scaling family, using attempt017 as the active reference summary.

Do not evaluate all pass children and do not promote a de-grossing child unless exposure-normalized and parent-relative evidence supports it.
