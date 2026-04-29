---
title: Phase 4 Sampling Policy V1
type: project
status: active
updated: 2026-04-29
tags:
  - project
  - phase4
  - sampling-policy
  - map-elites
  - islands
  - validation-overuse
sources:
  - "README.md"
  - "program_database_schema.md"
  - "universe_and_split_policy.md"
  - "dataset_admission_policy.md"
  - "evaluator_contract.md"
  - "dataset_context.md"
  - "AlphaEvolve - A coding agent for scientific and algorithmic discovery.pdf"
---
# Phase 4 Sampling Policy V1

## Purpose

This note defines the program-database sampling policy for the first production AlphaEvolve-style quant-research loop.

The policy is deliberately not “sample the best validation Sharpe.” That would overfit the validation interval. The database should sample useful parents and inspirations by combining score, diversity, mutation surface, data scope, failure type, and validation exposure.

## Core Decision

Use a **data-aware MAP-Elites + island population policy**.

```yaml
sampling_policy_name: phase4_sampling_v1
search_style: data_aware_map_elites_plus_islands
primary_goal: useful_quant_research_not_raw_sharpe
first_data_scope: daily_stock_only
first_universe: rolling_top500_market_cap
split_policy: chronological_70_15_15
```

This follows AlphaEvolve's key database idea: candidates are stored with evaluation results, and the database resurfaces prior programs in future prompts while balancing exploration and exploitation.

## Why This Is Needed For Quant

Quant alpha evaluation is noisy. A candidate can look good because of:

- validation-period luck
- repeated validation probing
- higher turnover
- implicit liquidity loading
- sector concentration
- hidden universe changes
- coverage shrinkage
- point-in-time leakage
- cost-model weakening

Therefore, parent sampling must use a penalized and diversity-aware score, not a raw validation metric.

## Islands

### Island A. `baseline_controls`

Purpose:

- keep parent, null, and negative-control programs visible in prompts
- prevent the LLM from forgetting the benchmark
- provide falsification examples

Contains:

- parent reversal
- matched-turnover random-rank controls
- randomized-signal controls
- frictionless parent
- cost-adjusted parent
- ablations

Sampling rule:

- Use often as inspiration.
- Rarely use as parent, except for explicit negative-control or ablation tasks.

### Island B. `daily_stock_signal`

Purpose:

- main early island for signal construction under daily-stock-only data

Allowed surfaces:

- `latent_state_definition`
- `observation_model`
- `innovation_scoring`
- `noise_parameter_estimation`
- `raw_reversal_scoring`
- `shock_reversal_scoring`

Examples:

- Kalman innovation clipping
- volatility-scaled innovation
- adaptive innovation saturation
- local-level versus beta-residual innovation
- return shock reversal

### Island C. `ranking_transform`

Purpose:

- mutate how raw scores become cross-sectional ranks or weights

Allowed surfaces:

- `ranking_transform`
- `winsorization`
- `rank_within_group`
- `score_decay`
- `score_blending`

Examples:

- rank within SICCD group
- z-score then clipped rank
- robust cross-sectional median/MAD transform
- blend reversal score with low-volatility dampener

### Island D. `portfolio_risk_turnover`

Purpose:

- separate alpha signal changes from portfolio-construction changes

Allowed surfaces:

- `holding_period`
- `buy_hold_banding`
- `turnover_control`
- `concentration_control`
- `portfolio_construction`
- `risk_control`

Examples:

- no-trade band
- max single-name cap
- smoother target-weight update
- long/short side balancing
- reduce turnover while preserving rank exposure

### Island E. `neutralization_liquidity`

Purpose:

- daily-stock-only improvements using native grouping and liquidity fields

Allowed surfaces:

- `sector_neutralization`
- `beta_neutralization`
- `liquidity_filter`
- `exchange_filter`
- `minimum_group_size_policy`

Examples:

- rank within SICCD
- neutralize market beta estimated from past returns
- liquidity-aware score dampening
- group-size fallback from SICCD to broader industry code

### Island F. `dataset_feature_addition`

Purpose:

- later-stage feature islands after dataset admission gates are implemented

Initial status:

```yaml
status: locked
unlock_after:
  - daily_stock_loop_has_100_controller_static_pass_children
  - at_least_20_sample_eval_children
  - null_and_cost_artifacts_are_stable
  - dataset_admission_registry_exists
```

When unlocked, this island must admit one dataset family at a time. Each dataset addition must have a join plan, availability lag, coverage estimate, and same-candidate-without-dataset ablation.

### Island G. `repair_near_miss`

Purpose:

- recover useful candidates that failed local formatting or narrow safety checks

Contains:

- malformed SEARCH/REPLACE
- oversized SEARCH blocks
- compile failures
- vector-smoke failures
- undeclared-name failures
- promising but cost-fragile candidates

Sampling rule:

- Use Qwen3.5-9B with temperature 0.
- Allow one repair attempt per child.
- Do not let repaired candidates skip deterministic checks.

### Island H. `negative_control`

Purpose:

- preserve falsification logic as part of the search state

Contains:

- randomized signals
- within-date permuted ranks
- lag-shifted or future-shift trap tests
- matched-turnover random ranks
- same-candidate-without-added-dataset ablations

Sampling rule:

- Use as inspiration to keep prompts honest.
- Use as parent only for explicit falsification tasks.

## Active Stage 0 Island Weights

Use these weights for the first 200 to 300 children:

```yaml
active_islands:
  daily_stock_signal: 0.45
  ranking_transform: 0.15
  portfolio_risk_turnover: 0.20
  neutralization_liquidity: 0.10
  repair_near_miss: 0.05
  negative_control: 0.05
  dataset_feature_addition: 0.00
```

Review these weights after 200 children or after 20 sample-evaluation passes, whichever comes first.

## Parent Sampling Mixture

For normal child generation:

```yaml
parent_sampling:
  top_adjusted_same_island: 0.45
  map_elite_underexplored_cell: 0.20
  novelty_survivor: 0.15
  recent_local_pass: 0.10
  random_survivor_same_island: 0.05
  repair_candidate: 0.05
```

Definitions:

- `top_adjusted_same_island`: high `selection_score` after penalties, within the chosen island.
- `map_elite_underexplored_cell`: a candidate from a valid but underpopulated MAP cell.
- `novelty_survivor`: a candidate with low return/signal/position overlap with current elites.
- `recent_local_pass`: recently generated candidate passing `controller_static` gates, sampled before remote data evaluation.
- `repair_candidate`: near-miss candidate eligible for one repair attempt.

Rejected candidates with leakage, split changes, cost removal, broker logic, or point-in-time violations are not eligible as parents. They may appear only as negative examples in prompt context.

## Inspiration Sampling

Each prompt should include 2 to 6 inspirations. Default is 4.

```yaml
inspiration_sampling:
  required:
    - parent_program
    - same_island_elite
    - global_elite_or_baseline
    - failure_or_negative_control
  optional:
    - diverse_island_program
    - near_miss_with_failure_reason
    - processed_output_prompt_card
    - dataset_context_card
```

The prompt sampler should include compact prompt-cards, not full artifact bundles.

## MAP-Elites Descriptors

Store many descriptors, but use only 3 or 4 active dimensions per island.

### Global descriptors

```yaml
descriptors:
  strategy_family:
    - reversal
    - kalman_innovation
    - event_drift
    - fundamental_quality
    - options_pressure
    - ownership_crowding
    - macro_conditioned
    - portfolio_only
    - negative_control

  signal_class:
    - raw_reversal
    - kalman_level_innovation
    - kalman_beta_residual
    - shock_reversal
    - volatility_scaled_reversal
    - rank_transform_only
    - portfolio_only
    - negative_control

  mutation_surface:
    - latent_state_definition
    - observation_model
    - innovation_scoring
    - noise_parameter_estimation
    - ranking_transform
    - holding_period
    - buy_hold_banding
    - liquidity_filter
    - sector_neutralization
    - beta_neutralization
    - turnover_control
    - concentration_control
    - dataset_feature_addition
    - portfolio_construction
    - risk_control
    - negative_control

  data_scope:
    - daily_stock_only
    - daily_stock_plus_market
    - daily_stock_plus_factor
    - daily_stock_plus_vix_or_rates
    - ccm_compustat
    - ibes_or_event
    - ownership_13f
    - options
    - cross_asset

  turnover_bucket:
    - very_low
    - low
    - medium
    - high
    - extreme

  cost_fragility_bucket:
    - robust
    - moderate
    - fragile
    - broken
    - unknown

  liquidity_bucket:
    - large_liquid
    - mixed
    - small_illiquid
    - unknown

  concentration_bucket:
    - safe
    - warning
    - fail
    - unknown

  null_delta_bucket:
    - below_null
    - near_null
    - above_null
    - above_null_p95

  stability_bucket:
    - unstable
    - mixed
    - stable
    - unknown

  validation_exposure_bucket:
    - fresh
    - moderate
    - overused
    - frozen
```

### Active dimensions by island

```yaml
daily_stock_signal:
  map_dimensions:
    - signal_class
    - mutation_surface
    - turnover_bucket
    - null_delta_bucket

ranking_transform:
  map_dimensions:
    - signal_class
    - mutation_surface
    - turnover_bucket
    - correlation_redundancy_bucket

portfolio_risk_turnover:
  map_dimensions:
    - mutation_surface
    - turnover_bucket
    - concentration_bucket
    - cost_fragility_bucket

neutralization_liquidity:
  map_dimensions:
    - mutation_surface
    - liquidity_bucket
    - sector_exposure_bucket
    - null_delta_bucket

dataset_feature_addition:
  map_dimensions:
    - data_scope
    - mutation_surface
    - coverage_loss_bucket
    - null_delta_bucket

repair_near_miss:
  map_dimensions:
    - failure_category
    - mutation_surface
    - model_id
    - generation

negative_control:
  map_dimensions:
    - control_type
    - turnover_bucket
    - data_scope
    - failure_category
```

## Selection Score

Store raw metrics separately. Parent sampling uses an adjusted score.

Initial formula:

```python
def compute_selection_score(metrics, diagnostics, descriptors, exposure):
    score = 0.0

    score += 0.30 * z_in_island(metrics.get("validation_net_sharpe"))
    score += 0.20 * z_in_island(metrics.get("null_delta_validation_sharpe"))
    score += 0.15 * z_in_island(metrics.get("subperiod_stability"))
    score += 0.10 * z_in_island(metrics.get("validation_net_return"))
    score += 0.10 * z_in_island(metrics.get("cost_robustness_score"))
    score += 0.05 * z_in_island(metrics.get("liquidity_robustness_score"))
    score += 0.05 * z_in_island(metrics.get("concentration_safety_score"))
    score += 0.05 * z_in_island(metrics.get("novelty_score"))

    score -= validation_overuse_penalty(exposure)
    score -= complexity_penalty(diagnostics, descriptors)
    score -= surface_count_penalty(descriptors)
    score -= coverage_shrinkage_penalty(diagnostics)
    score -= correlation_redundancy_penalty(diagnostics)

    if diagnostics.get("hard_gate_pass") is False:
        score -= 100.0

    return score
```

`z_in_island` should normalize using comparable candidates inside the same island. Do not compare an options-feature candidate directly to a daily-stock-only portfolio-control candidate.

## Required Penalties

### Validation-overuse penalty

```python
def validation_overuse_penalty(exposure):
    n_branch = exposure.get("num_prior_remote_validations_from_same_branch", 0)
    n_root = exposure.get("num_prior_remote_validations_from_same_root", 0)
    return 0.02 * (n_branch ** 0.5) + 0.01 * (n_root ** 0.5)
```

### Complexity penalty

Triggers:

- new import
- new dataset
- new global parameter
- large diff
- more than allowed mutation surfaces
- new dependency not in seed environment

### Coverage-shrinkage penalty

Triggers:

- fewer names per day
- fewer trading dates
- large missingness increase
- edge appears only after coverage collapse

### Correlation-redundancy penalty

Triggers:

- high daily return correlation with elite candidate
- high signal rank correlation with parent
- high long/short overlap
- materially identical behavior with different constant

## Prompt Modes

```yaml
prompt_modes:
  conservative_patch:
    parent: top_adjusted_same_island
    inspirations:
      - parent
      - top_same_island
      - negative_control
    model: Qwen3.5-9B
    temperature: 0.0

  normal_mutation:
    parent: map_elite_or_high_score
    inspirations:
      - global_elite
      - same_island_elite
      - diverse_island_program
      - failure_summary
    model: Qwen3.5-9B
    temperature_grid: [0.2, 0.5]

  repair:
    parent: near_miss_or_failed_candidate
    inspirations:
      - repair_examples
      - failure_report
    model: Qwen3.5-9B
    temperature: 0.0
    max_attempts: 1

  medium_review:
    parent: branch_summary
    inspirations:
      - top_program_cards
      - failures
      - nulls
      - data_scope_summary
    model: Qwen3.5-27B-FP8
    frequency: every_30_children
    output: mutation_surface_suggestions_only

  deep_review:
    parent: search_state_summary
    inspirations:
      - top_10_summaries
      - underexplored_map_cells
      - null_failures
      - dataset_catalog_summary
    model: Qwen3.6-35B-A3B-FP8
    frequency: every_50_children
    output: mutation_surface_suggestions_only
```

## Dataset Additions

Dataset additions are disabled in Stage 0.

```yaml
dataset_addition:
  stage_0_status: disabled
  unlock_conditions:
    - daily_stock_loop_has_100_controller_static_pass_children
    - at_least_20_sample_eval_children
    - matched_turnover_null_artifacts_exist
    - cost_grid_artifacts_exist
    - dataset_admission_registry_exists
```

When dataset additions are unlocked, the dataset-feature island must admit one dataset family at a time.

## First Review Checkpoint

After 200 children, produce `phase4_sampling_review_001.md` with:

- island counts
- controller_static pass rates
- sample eval pass rates
- top MAP cells
- empty MAP cells
- validation exposure counts
- repair success rate
- null failure rate
- cost fragility distribution
- whether dataset additions can remain locked or should be proposed for admission

Do not unlock the test set during this review.
