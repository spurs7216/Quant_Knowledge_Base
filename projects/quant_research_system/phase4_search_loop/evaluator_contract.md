---
title: Phase 4 Evaluator Contract
type: project
status: active
updated: 2026-05-09
tags:
  - project
  - phase4
  - evaluator
  - search-loop
  - validation-overuse
sources:
  - "README.md"
  - "cost_model_policy.md"
  - "universe_and_split_policy.md"
  - "phase4_sampling_policy_v1.md"
  - "program_database_schema.md"
---

# Phase 4 Evaluator Contract

## Purpose

This contract defines the minimum gates for Phase 4 child candidates.

The evaluator should make it hard for search to win by overfitting, leaking information, hiding turnover, changing the universe, weakening costs, shrinking coverage, or repeatedly probing the same validation period.

## AlphaEvolve-Compatible Evaluator Shape

Every evolved program should eventually be callable through:

```python
def evaluate(eval_inputs) -> dict[str, float]:
    ...
```

The returned dictionary uses scalar metrics where larger is better. Penalties are transformed into maximization-compatible scores, while hard gates remain explicit diagnostics.

## Initial Scalar Scores

```yaml
scalar_scores:
  validation_net_sharpe: maximize
  validation_net_return: maximize
  negative_turnover: maximize
  negative_cost_drag: maximize
  negative_max_abs_weight: maximize
  negative_p99_max_abs_weight: maximize
  parent_delta_validation_sharpe: maximize
  null_delta_validation_sharpe: maximize
  subperiod_stability: maximize
  cost_robustness_score: maximize
  liquidity_robustness_score: maximize
  concentration_safety_score: maximize
  novelty_score: maximize
```

Do not optimize only one metric.

## Hard Gates

A candidate cannot move beyond `controller_static` if any cheap static hard gate fails. This stage runs on the remote controller, not on local Windows.

```yaml
controller_static_hard_gates:
  manifest_exists: true
  program_compiles: true
  search_replace_parse_pass: true
  exact_unique_search_match: true
  search_inside_evolve_block: true
  forbidden_file_edit_absent: true
  split_policy_unchanged: true
  universe_policy_unchanged: true
  cost_policy_unchanged: true
  duplicate_policy_unchanged: true
  no_forward_return_availability_filter: true
  no_raw_warehouse_copy_to_vault: true
  no_broker_or_ibkr_logic: true
  undeclared_name_check_pass: true
  vector_smoke_pass: true
```

Remote data-evaluation hard gates:

```yaml
remote_hard_gates:
  date_coverage_reported: true
  split_manifest_matches_policy: true
  rolling_top500_universe_manifest_exists: true
  duplicate_identifier_date_check_pass: true
  lookahead_guard_pass: true
  one_day_or_declared_holding_period_timing_pass: true
  nonfinite_return_check_pass: true
  active_portfolio_day_coverage_pass: true
  reference_metric_equivalence_check_pass: true
  turnover_cost_application_check_pass: true
  max_single_name_weight_check_pass: true
  minimum_names_per_side_check_pass: true
  artifact_bundle_complete: true
code_snapshot_recorded: true
dirty_flag_recorded: true
git_head_matches_origin_main_recorded: true
program_sha256_recorded: true
```

Dataset-added gates, locked until dataset admission exists:

```yaml
dataset_added_hard_gates:
  dataset_admission_id_exists: true
  catalog_path_declared: true
  join_key_declared: true
  join_grain_declared: true
  timestamp_field_declared: true
  availability_lag_declared: true
  expected_coverage_loss_declared: true
  point_in_time_join_check_pass: true
  same_candidate_without_dataset_ablation_exists: true
```

## Null Baselines

Every remote validation should compare candidates against:

- parent candidate metrics;
- cost-adjusted parent metrics;
- frictionless parent metrics for diagnostic only;
- matched-turnover random-rank decile portfolios;
- randomized-signal negative control when candidate uses a fitted or stateful signal;
- same-candidate ablation without added dataset when a candidate introduces a new feature source.

Matched-turnover nulls should be distributional.

```yaml
matched_turnover_random_rank_null:
  minimum_seeds: 100
  report:
    - mean
    - p50
    - p90
    - p95
    - p99
    - candidate_percentile
```

Promotion normally requires validation Sharpe above null p95 and validation net return above null p90. Exceptions require explicit review.

## Cost Model

Use the Phase 4 cost grid:

```yaml
cost_grid_bps_total:
  - 0.0
  - 2.5
  - 5.0
  - 10.0
```

`0.0` bps is diagnostic only. `2.5` bps is the current continuity baseline. `10.0` bps is a severe stress scenario, not the default estimate.

High-turnover candidates must show cost robustness, not only raw Sharpe improvement.

## Validation-Overuse Controls

The evaluator must record validation exposure.

```yaml
validation_exposure:
  split_id: "daily_stock_top500_chrono_70_15_15_v1"
  root_candidate_id: "CAND-..."
  branch_id: "BRANCH-..."
  num_prior_children_from_same_root: 0
  num_prior_children_from_same_branch: 0
  num_prior_remote_validations_from_same_root: 0
  num_prior_remote_validations_from_same_branch: 0
  num_prior_promotions_from_same_root: 0
  num_prior_promotions_from_same_branch: 0
  branch_frozen: false
```

Policy:

```yaml
validation_overuse_policy:
  max_remote_validations_per_branch_before_review: 25
  max_remote_validations_per_root_before_review: 100
  max_promotions_per_root_before_freeze_review: 5
  test_evaluation_requires_branch_freeze: true
  forbid_mutation_after_test_evaluation: true
```

## Decision Layers

Do not use one vague `proceed` decision.

```yaml
decisions:
  survive_for_mutation: false
  promote_to_candidate_registry: false
  unlock_test_evaluation: false
  decision_reason: ""
```

### `survive_for_mutation = true` only if

- hard gates pass;
- candidate is not much worse than matched-turnover null;
- changed surface is interpretable;
- artifact bundle is sufficient for prompt feedback;
- candidate is not severe cost/concentration/liquidity failure.

### `promote_to_candidate_registry = true` only if

- hard gates pass;
- candidate beats parent after realistic costs;
- candidate beats matched-turnover null;
- performance is not driven by one subperiod;
- liquidity buckets do not show the edge exists only in hard-to-trade names;
- concentration gates are clean or only minor warnings;
- review artifact gives an economically coherent rationale.

### `unlock_test_evaluation = true` only if

- branch is frozen;
- no further child mutation will use test results;
- `review.md` exists;
- validation-overuse exposure is reported;
- human or explicit review-agent approval exists.

## Required Remote Artifact Bundle

Every remote run must produce:

```text
run_manifest.yaml
metrics.json
scorecard.csv
diagnostics.csv
evaluator_summary.json
failure_report.md
review.md
cost_sensitivity.csv
program_snapshot.py
subperiod_metrics.csv
liquidity_bucket_metrics.csv
concentration_metrics.csv
universe_summary.csv
split_manifest.yaml
```

For dataset-added candidates, also produce:

```text
join_diagnostics.csv
coverage_diagnostics.csv
same_candidate_without_dataset_ablation.csv
point_in_time_join_report.md
```

## Required `evaluator_summary.json`

The summary file is the prompt-facing evaluator artifact. It must be compact and schema-valid.

See [artifact_renderer_contract.md](artifact_renderer_contract.md).

## Rejection Categories

```yaml
failure_category:
  - malformed_diff
  - outside_evolve_block
  - local_compile_failure
  - vector_smoke_failure
  - leakage
  - split_policy_change
  - universe_policy_change
  - cost_policy_change
  - duplicate_policy_change
  - no_broker_rule_violation
  - nonfinite_returns
  - too_few_names
  - concentration_failure
  - cost_fragile
  - below_parent
  - below_null
  - subperiod_unstable
  - liquidity_fragile
  - coverage_shrinkage
  - point_in_time_join_failure
  - missing_required_artifact
  - remote_runtime_error
```

## Candidate Requirements

Each candidate must declare:

- parent program ID;
- root candidate ID;
- branch ID;
- mutation surface;
- signal definition;
- portfolio construction;
- universe policy ID;
- split ID;
- cost model;
- dataset sources;
- join keys and timing assumptions if any dataset is added;
- concentration policy;
- expected artifact bundle;
- falsification condition.
