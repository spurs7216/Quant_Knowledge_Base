---
title: Controller Attempt017 Search-Control Rerun Review 2026-05-13
type: project
status: active
updated: 2026-05-13
tags:
  - project
  - phase4
  - alphaevolve
  - controller
  - evaluator
sources:
  - "../../artifacts/controller_attempt017_search_control_rerun_20260511.zip"
  - "controller_attempt017_search_control_remote_instructions_20260511.md"
  - "controller_attempt017_focused_round_review_20260511.md"
  - "current_state.md"
---
# Controller Attempt017 Search-Control Rerun Review 2026-05-13

## Decision

No sample evaluation from this batch.

The rerun confirms that the remote Qwen/controller/database path is healthy after the search-control patch, but it did not produce a child worth data-backed evaluation. The batch generated four controller passes, but two were off-target and the two target-matched passes did not change final portfolio weights on the smoke panel. The only material portfolio-delta signal child was another generic magnitude dampener, exactly the family we now treat as negative evidence for the attempt017 branch.

Full validation and test-set evaluation remain forbidden.

## Run Summary

Artifact:

```text
artifacts/controller_attempt017_search_control_rerun_20260511.zip
```

Controller metrics:

```yaml
attempt_count: 12
pass_count: 4
unique_child_pass_rate: 0.3333333333333333
raw_parse_pass_rate: 1.0
exact_search_match_rate: 0.9166666666666666
evolve_block_safe_rate: 0.9166666666666666
apply_pass_rate: 0.9166666666666666
compile_pass_rate: 0.9166666666666666
vector_smoke_pass_rate: 0.9166666666666666
portfolio_semantic_pass_rate: 0.9166666666666666
behavior_delta_pass_rate: 0.4166666666666667
behavioral_noop_count: 6
duplicate_child_count: 0
duplicate_patch_fingerprint_count: 0
near_duplicate_patch_count: 1
target_intent_match_rate: 0.5
target_intent_mismatch_pass_count: 2
map_cell_count: 4
db_insert_pass_rate: 1.0
reasoning_only_empty_count: 0
lazy_penalty_score_sum: -2.6499999999999995
```

Compared with the prior focused round, this is a small mechanical improvement, not a research improvement:

- pass count moved from 3/12 to 4/12;
- behavioral no-ops moved from 7 to 6;
- target-intent match moved from 0.3333 to 0.5;
- Qwen no-thinking routing remained healthy;
- duplicate-child failures stayed at zero;
- no market-worthy child emerged.

## Pass Children

| Attempt | Program | Target | Actual intent | Target match | Portfolio effect | Smoke Sharpe | Review |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 004 | `PROG-20260511-A017-SCONTROL-0004` | `signal/history_confidence_weighting` | `clipped_magnitude_dampening` | false | material portfolio delta | -1.2166 | Do not sample-evaluate. This repeats the generic signal-dampening family with negative attempt017 evidence. |
| 007 | `PROG-20260511-A017-SCONTROL-0007` | `ranking/winsorization_quantile_change` | `winsorization_quantile_change` | true | no final-weight delta | 0.2838 | Controller-safe but likely metric-equivalent to parent in data-backed evaluation. |
| 008 | `PROG-20260511-A017-SCONTROL-0008` | `signal/history_confidence_weighting` | `history_confidence_weighting` | true | no rank or final-weight delta | 0.2838 | Target-matched, but only changes raw signal magnitudes that are absorbed downstream. |
| 011 | `PROG-20260511-A017-SCONTROL-0011` | `ranking/shrinkage_transform` | `ranking_other` | false | no final-weight delta | 0.2838 | Off-target and likely metric-equivalent to parent. |

Attempt 000 was rejected as a near duplicate of `PROG-20260430-CHILD-0028`; it again used bounded tanh-style dampening and had negative smoke Sharpe.

## What Worked

The infrastructure is now stable enough for controlled search:

- remote Qwen returned normal final content, with no reasoning-only empty outputs;
- strict SEARCH/REPLACE parsing, evolve-block safety, compile, vector smoke, and portfolio semantic gates are mostly healthy;
- reasoning memory and skill cards were loaded and retrieved;
- prior summaries were seeded, with 100 prior attempts and 61 prior passes visible to the population policy;
- near-duplicate filtering caught the repeated bounded-tanh signal dampener;
- database insertion remained at 1.0.

This means Phase 4 is no longer blocked by model routing, schema, database, or patch-format mechanics.

## Main Obstacles

### Behavioral no-ops still dominate

Six of twelve attempts were rejected because the child smoke outputs were identical to the parent. The concentration is mostly in portfolio and risk prompts:

```yaml
behavioral_noop_attempts:
  - attempt_001: portfolio/signal_weighted_sides
  - attempt_002: risk/small_book_guard
  - attempt_005: portfolio/signal_weighted_sides
  - attempt_006: risk/cap_shape_change
  - attempt_009: portfolio/signal_weighted_sides
  - attempt_010: risk/max_weight_tightening
```

The prompt now warns against no-ops, but warning is not enough. For attempt017, many portfolio/risk edits are absorbed by selection, side normalization, or already-low max weight. They should not be sampled heavily unless the target is tied to a concrete mechanism that changes final weights.

### Target intent is still too soft

Two of four controller passes were off-target:

```yaml
attempt_004:
  target: signal/history_confidence_weighting
  actual: clipped_magnitude_dampening
attempt_011:
  target: ranking/shrinkage_transform
  actual: ranking_other
```

The controller stores these as evidence, but they should not count as sample-eval candidates. For focused repair mode, target-intent mismatch should probably become a hard sample-eligibility failure, and perhaps a hard controller-pass failure for selected high-risk intents.

### Avoid skills are prompt guidance, not hard filters

Attempt 004 retrieved the attempt017 generic-dampening avoid skill, but Qwen still generated a clipped magnitude dampener. The micro-filter allowed it because the patch was syntactically safe and behaviorally nontrivial. This is useful evidence: prompt-side memory is necessary but not sufficient when an avoid rule corresponds to a known bad patch family.

### Controller passes are not portfolio-improvement evidence

Attempts 007, 008, and 011 passed controller-static gates but did not change final weights on the smoke panel. They are program-database evidence, not alpha evidence. Sample-evaluating them would likely waste remote compute and could confuse lineage with metric-equivalent children.

## Progress So Far

Phase 4 has made real infrastructure progress:

1. Daily-stock contract and remote-only Qwen execution are frozen.
2. The seed strategy has named evolve blocks and a hardened sample evaluator.
3. Qwen can generate strict SEARCH/REPLACE children through the remote vLLM server.
4. The controller can parse, repair, apply, compile, smoke test, semantically filter, classify, de-duplicate, and store children.
5. MAP-Elites-style descriptors, population policy, lazy penalties, reasoning memory, diagnostic cards, and skill cards are active.
6. A first curated sample evaluation was completed, but no child has been promoted.
7. The attempt017 branch has now produced multiple negative lessons: missing-held repair alone is insufficient, generic signal dampening is weak or negative, and many local code edits do not survive downstream portfolio construction.

The important status is:

```yaml
controller_infrastructure: healthy
program_database_loop: healthy
first_data_backed_probe: completed
promoted_child: none
iterative_evolution_round_with_improvement: not_yet
current_blocker: search_quality_and_candidate_eligibility
```

## Recommended Next Step

Do not run another remote batch immediately.

Patch the local controller policy first:

```yaml
next_local_hardening:
  sample_eval_eligibility_requires_target_intent_match: true
  sample_eval_eligibility_requires_final_weight_delta_or_explicit_reason: true
  avoid_skill_family_can_be_hard_rejected_for_focused_repair: true
  deprioritize_attempt017_portfolio_risk_noop_intents: true
  report_candidate_eligibility_summary_in_controller_artifacts: true
```

After that, the next search step should probably not be another 12 attempts from the same shallow prompt pool. The better research step is a small idea-generation / design-review slice for the attempt017 branch: identify mechanisms that can plausibly reduce missing-held exposure or turnover without destroying parent-relative economics, using only allowed daily-stock fields such as price, volume, dollar volume, market cap, trading status, exchange, and industry. Then convert one or two concrete mechanisms into controller targets.
