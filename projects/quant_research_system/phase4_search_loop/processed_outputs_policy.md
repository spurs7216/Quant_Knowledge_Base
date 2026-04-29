---
title: Phase 4 Processed Outputs Policy
type: project
status: active
updated: 2026-04-27
tags:
  - project
  - phase4
  - processed-outputs
  - reproducibility
sources:
  - "csv_data_catalog.md"
  - "dataset_context.md"
  - "phase4_sampling_policy_v1.md"
---
# Phase 4 Processed Outputs Policy

## Purpose

The catalog contains many processed research outputs. They are valuable, but they are not automatically valid parent programs.

This policy defines how processed CSV outputs can be used in the AlphaEvolve-style loop.

## Decision

Processed outputs can be used as:

1. inspiration;
2. evaluator calibration;
3. failure-mode memory;
4. reproducibility targets.

Processed outputs cannot become parent programs unless their source scripts are found, inspected, and validated.

## Allowed Roles

### Role A. Inspiration

Use processed summaries to tell the prompt sampler what prior work tried.

Example prompt-card:

```yaml
processed_inspiration_card:
  source_file: "data/processed/research/fast_reversion_v4_short_summary.csv"
  family: "fast_reversion"
  what_it_suggests: "short-horizon reversal variants were tested"
  limitations: "CSV output only; source script not yet validated"
  allowed_use: "inspiration_only"
```

### Role B. Evaluator calibration

Use processed outputs to calibrate what normal metrics look like:

- typical Sharpe range;
- typical turnover range;
- typical cost drag;
- how sector neutralization changes results;
- how event coverage shrinkage appears;
- how many rows/features are normal for a feature panel.

### Role C. Failure memory

Processed failed or weak results can be useful negative context:

- cost fragility;
- high turnover;
- low coverage;
- sector concentration;
- event-only coverage collapse;
- null similarity.

### Role D. Reproducibility target

A processed output can become a target for reconstruction. It becomes a parent only after validation.

## Source-Script Validation Checklist

Before using a processed strategy as a parent program, Codex must locate and inspect its source script.

Required checks:

```yaml
source_script_validation:
  source_script_exists: true
  script_compiles: true
  data_paths_declared: true
  no_hardcoded_future_dates: true
  split_policy_explicit: true
  universe_policy_explicit: true
  cost_model_explicit: true
  point_in_time_joins_explicit: true
  nulls_or_controls_present: true
  output_reproducible_on_sample: true
  artifact_schema_known: true
  code_quality_decision: "pass|revise|reject"
```

If source quality is poor but idea quality is useful, create a new clean seed program rather than mutating the old script.

## Processed Output Status Enum

```yaml
processed_output_status:
  - inspiration_only
  - calibration_only
  - source_script_missing
  - source_script_found_pending_review
  - source_script_validated
  - reproducibility_target
  - eligible_as_parent_program
  - rejected_as_parent_program
```

## Prompt-Sampler Restrictions

When using processed outputs in prompts:

- do not paste large CSV content;
- render a compact prompt-card;
- state whether source script is validated;
- state whether the output is inspiration-only;
- do not ask the LLM to copy unknown logic from processed files;
- do not treat processed output metrics as official unless artifact provenance is clear.

## Program Database Rule

A processed output without validated source code may be inserted into an `external_artifacts` table or prompt-card store, but not into the `programs` table as an executable parent.

## Recommended `external_artifacts` Table

```sql
CREATE TABLE IF NOT EXISTS external_artifacts (
    artifact_id TEXT PRIMARY KEY,
    artifact_type TEXT NOT NULL,
    source_path TEXT NOT NULL,
    family TEXT,
    status TEXT NOT NULL,
    source_script_path TEXT,
    source_script_status TEXT,
    prompt_card_json TEXT NOT NULL,
    metrics_json TEXT,
    limitations TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
```

## First Implementation

Codex should create an artifact-renderer that reads selected processed summaries and emits prompt-cards like:

```json
{
  "artifact_id": "EXT-FASTREV-001",
  "source_path": "data/processed/research/fast_reversion_v4_short_summary.csv",
  "family": "fast_reversion",
  "status": "inspiration_only",
  "source_script_status": "unknown",
  "takeaway": "short-horizon reversal variants exist as prior diagnostics",
  "limitations": ["processed CSV only", "source script not validated"]
}
```
