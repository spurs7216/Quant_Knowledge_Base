---
title: Phase 4 Dataset Admission Policy
type: project
status: active
updated: 2026-04-29
tags:
  - project
  - phase4
  - datasets
  - point-in-time
  - admission-gates
sources:
  - "dataset_context.md"
  - "csv_data_catalog.md"
  - "program_database_schema.md"
---
# Phase 4 Dataset Admission Policy

## Purpose

This note controls how non-primary datasets enter the AlphaEvolve-style search loop.

The first production loop is daily-stock-only. Dataset additions are not allowed until the evaluator, program database, sampling policy, and null controls are stable.

Codex may inspect data and write dataset-admission reviews, join plans, coverage reports, and recommendations. Codex may not unlock executable multi-dataset generation unless the human explicitly approves it.

## Data Stages

```yaml
data_stages:
  stage_0_daily_stock:
    status: active
    allowed:
      - daily_stock
      - native daily_stock SICCD/NAICS/ICBIndustry group fields
      - daily_market_index for diagnostics only when already present in evaluator
      - risk_free_rate for excess-return accounting when already present in evaluator
    disallowed_as_alpha_features:
      - Compustat
      - options
      - ownership_13F
      - IBES/event features
      - bonds
      - macro cross-asset features

  stage_1_date_level_diagnostics:
    status: locked
    allowed_after_review:
      - Fama-French diagnostics
      - cboe_vix regime splits
      - Treasury/rate regime splits
    default_role: diagnostics_and_robustness_not_primary_alpha

  stage_2_classification_and_sector:
    status: locked
    allowed_after_review:
      - CCM/Compustat sector classification after join audit
    default_role: neutralization_and_bucket_tests

  stage_3_fundamental_event_ownership:
    status: locked
    allowed_after_review:
      - Compustat fundamentals
      - ownership_13F
      - IBES/revision/event features where source scripts exist
    default_role: interpretable overlays with ablations

  stage_4_options:
    status: locked
    allowed_after_review:
      - option_forward_price
      - option_volumne
    default_role: pressure_crowding_volatility_features

  stage_5_cross_asset:
    status: locked
    allowed_after_review:
      - bond_return
      - reit
      - broader macro panels
    default_role: regime_or_cross_asset_extensions
```

## Admission Object

Every non-primary dataset must create a `dataset_admission` record before any generated child can use it.

```yaml
dataset_admission:
  admission_id: "DATASET-ADMIT-YYYYMMDD-000001"
  dataset_family: "ccm_compustat"
  catalog_path: "data/CCM/...csv"
  sample_path: "catalog/samples/CCM/...csv"
  join_key: "PERMNO -> CCM.LPERMNO -> GVKEY"
  join_grain: "security-date to firm-fiscal-period"
  timestamp_field: "datadate"
  availability_lag: "at least declared reporting lag; exact policy required before production"
  expected_coverage_loss: null
  expected_bias_direction: "unknown"
  required_ablation: "same_candidate_without_dataset"
  point_in_time_check_status: "pending"
  status: "proposed"
```

Status enum:

```yaml
admission_status:
  - proposed
  - sample_read_pass
  - join_plan_pass
  - coverage_estimated
  - point_in_time_pass
  - admitted_for_sample_eval
  - admitted_for_remote_eval
  - rejected
```

## Five Required Declarations

A feature proposal using a new dataset must declare:

1. dataset source and physical catalog path;
2. join key and grain;
3. timestamp field and availability lag;
4. expected coverage loss;
5. ablation plan versus the same candidate without the added dataset.

If any item is missing, the candidate is `revise`, not `remote_candidate`.

## Dataset-Specific Rules

### `daily_stock`

Allowed in Stage 0.

Native uses:

- returns and excess returns
- price and volume
- dollar volume
- shares outstanding
- exchange/security filters
- SICCD/NAICS/ICBIndustry grouping when present
- market-adjusted returns if `vwretd`, `ewretd`, or index fields are present

Forbidden:

- changing global universe logic inside evolve blocks
- filtering to survivors after the fact
- requiring future price/share information

### `daily_market_index`, `risk_free_rate`, `Fama-French`

Allowed first as diagnostics and risk/excess-return accounting.

Feature use requires:

- date join only;
- declared availability timing;
- ablation versus same candidate without the regime/factor feature.

### `CCM` and `comp_na_daily_all_annual`

Requires:

```yaml
join_path: "PERMNO -> CCM.LPERMNO -> GVKEY"
valid_link_dates_required: true
fundamental_timestamp_required: true
reporting_lag_required: true
coverage_report_required: true
ablation_required: true
```

Do not use Compustat sector/fundamental fields until the CCM join is validated.

### `ownership_13F`

Requires:

```yaml
join_key: CUSIP
reporting_date_lag_required: true
same_quarter_before_filing_forbidden: true
coverage_report_required: true
ablation_required: true
```

### `option_forward_price` and `option_volumne`

Options are locked until Stage 4.

Requirements before use:

- date-aware identifier join plan;
- ticker-only joins marked exploratory;
- CUSIP/secid mapping validation;
- option-to-equity aggregation rule;
- coverage-loss report;
- same-candidate-without-option ablation;
- liquidity and stale-contract diagnostics.

### `bond_return`, `reit`, macro panels

Locked until Stage 5.

Use as regime context only until a separate cross-asset evaluator exists.

## Dataset Unlock Conditions

A stage may unlock only after a review note records:

```yaml
unlock_review:
  daily_stock_loop_local_pass_count: >=100
  remote_sample_eval_pass_count: >=20
  matched_turnover_null_artifacts_exist: true
  cost_grid_artifacts_exist: true
  split_policy_locked: true
  universe_policy_locked: true
  dataset_admission_registry_exists: true
  human_approval_required: true
```

Executable multi-dataset generation requires an approval file:

```text
projects/quant_research_system/phase4_search_loop/dataset_unlocks/<dataset_family>_unlock_approval.yaml
```

Codex may draft review artifacts, but it may not create a final approval file unless explicitly instructed by the human.

## Candidate Rules

A child candidate using a non-primary dataset must include:

```yaml
candidate_dataset_declaration:
  data_scope: "ccm_compustat"
  admission_id: "DATASET-ADMIT-..."
  feature_names:
    - "..."
  join_plan_hash: "..."
  expected_coverage_loss: 0.0
  ablation_program_id: null
```

A candidate may not introduce a dataset in the same generation as a major signal-class rewrite unless explicitly approved by the mutation-surface policy.

## Dataset Feature Promotion Gates

Dataset-added candidates cannot be promoted unless:

- all normal evaluator gates pass;
- point-in-time join check passes;
- coverage loss is reported;
- candidate beats its same-candidate-without-dataset ablation;
- candidate beats matched-turnover null;
- performance is not solely explained by coverage shrinkage;
- feature missingness is not concentrated in one period, sector, exchange, or liquidity bucket.

## Prompt-Sampler Rule

Until a dataset is admitted and the human approval file exists, prompt cards may mention it only as a future idea or restriction. The LLM must not be asked to write executable feature code for that dataset.
