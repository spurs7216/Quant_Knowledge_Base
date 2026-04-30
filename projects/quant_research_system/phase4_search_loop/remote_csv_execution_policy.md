---
title: Phase 4 Remote CSV Execution Policy
type: project
status: active
updated: 2026-04-29
tags:
  - project
  - phase4
  - remote-execution
  - csv
  - artifacts
sources:
  - "README.md"
  - "dataset_context.md"
  - "csv_data_catalog.md"
  - "universe_and_split_policy.md"
---
# Phase 4 Remote CSV Execution Policy

## Purpose

The remote server contains the heavy warehouse data, currently in CSV format. The local vault must not become the warehouse.

This policy defines how Phase 4 jobs should run on remote CSV data and return compact evidence artifacts.

## Non-Negotiable Rules

```yaml
remote_execution_rules:
  heavy_data_stays_remote: true
  local_sync_only_compact_artifacts: true
  no_external_exe_assumption: true
  no_broker_or_ibkr_logic_remote: true
  csv_is_current_source_format: true
  remote_jobs_need_manifest: true
```

Remote jobs must not call IBKR, TWS, IB Gateway, account APIs, position APIs, contract lookup APIs, paper-order APIs, live-order APIs, or broker credential paths.

## Storage Tools

Preferred:

```yaml
storage_stack:
  metadata: SQLite
  audit: JSONL
  large_metric_panels: Parquet
  analysis: DuckDB
```

Fallbacks:

```yaml
fallbacks:
  duckdb_unavailable: use SQLite plus pandas/chunked CSV
  parquet_unavailable: use compressed CSV or JSONL for compact panels
  pyarrow_unavailable: do not block controller_static; block only large-panel optimization
```

Do not require system-level installation of `.exe` files or external services.

## Remote Job Manifest

Every remote job must have a manifest before execution.

Minimum manifest:

```yaml
run_id: "RUN-YYYYMMDD-000001"
program_id: "PROG-YYYYMMDD-000123"
parent_program_id: "PROG-YYYYMMDD-000001"
root_candidate_id: "CAND-20260423-001"
branch_id: "BRANCH-CAND-20260423-001-001"
split_id: "daily_stock_top500_chrono_70_15_15_v1"
universe_policy: "rolling_top500_market_cap_v1"
data_scope: "daily_stock_only"
input_paths:
  daily_stock: "data/daily_stock/gago9dveytpx6922.csv"
output_dir: "artifacts/phase4/RUN-YYYYMMDD-000001"
code_snapshot_hash: "..."
dirty_flag: false
cost_grid_bps: [0.0, 2.5, 5.0, 10.0]
remote_no_broker_logic: true
```

## CSV Reading Policy

The first implementation should support chunked CSV reading.

Requirements:

- select only needed columns;
- parse dates explicitly;
- do not load the entire warehouse when a stage only needs a sample;
- write intermediate compact panels only when needed;
- report row counts before and after filters.

Pseudo-code pattern:

```python
usecols = ["PERMNO", "DlyCalDt", "DlyRet", "DlyRetx", "DlyPrc", "DlyVol", "DlyPrcVol", "ShrOut", "SICCD", "NAICS", "PrimaryExch"]
for chunk in pd.read_csv(path, usecols=existing_usecols, chunksize=1_000_000):
    chunk["DlyCalDt"] = pd.to_datetime(chunk["DlyCalDt"])
    # filter date range, compute needed fields, append compact output
```

The exact column names must be verified against the sample and EDA summaries before hardcoding.

Before freezing the `daily_stock` contract, schema evidence must include not only column names and dtypes but also compact value diagnostics for universe-critical fields: date range, identifier fields, return fields, price, volume, dollar volume, market cap or shares outstanding, exchange, security type, share type, trading status, conditional type, US-incorporation flag, and industry fields. A bounded sample is enough for this contract preflight, but the report must be explicit about sample size and must not be mistaken for full-file coverage.

`daily_stock_contract_v1` is now frozen from `schema_evidence_v2`; implementation must import the contract from `research/alphaevolve_lite/daily_stock_contract.py` rather than retyping field names.

## Output Bundle

Every remote validation must produce:

```text
run_manifest.yaml
metrics.json
scorecard.csv
diagnostics.csv
evaluator_summary.json
failure_report.md
review.md
cost_sensitivity.csv
subperiod_metrics.csv
liquidity_bucket_metrics.csv
concentration_metrics.csv
universe_summary.csv
split_manifest.yaml
code_snapshot.txt or code_snapshot_hash.txt
```

Optional:

```text
returns_by_split.csv
positions_sample.parquet or positions_sample.csv
turnover_timeseries.csv
null_distribution.csv
join_diagnostics.csv
```

Only compact outputs should sync back to the vault.

All Qwen calls and AlphaEvolve-lite controller execution happen on the remote server. The local Windows machine receives only compact artifacts for review and must not run LLM inference or scan the CSV warehouse.

## Local Artifact Intake

On local sync, the control plane should verify:

- all required files exist;
- `evaluator_summary.json` parses;
- `run_manifest.yaml` matches requested program ID;
- code hash matches the program database record;
- no heavy warehouse data was copied into the artifact bundle;
- decision fields are present;
- failure report exists even for successful runs.

## Resource Discipline

For Stage 0:

```yaml
stage_0_resource_policy:
  data_scope: daily_stock_only
  first_sample_eval:
    date_window: small
    universe_slice: small_or_top500_sample
  full_validation:
    universe: rolling_top500
    splits: 70_15_15
  parallelism: conservative_initially
```

Use explicit logs for wall time and memory where possible.

## Error Handling

A remote job that fails should still produce:

```text
failure_report.md
evaluator_summary.json
stderr_tail.txt
stdout_tail.txt
run_manifest.yaml
```

The evaluator summary should mark:

```json
{
  "decision": "reject",
  "failure_category": "remote_runtime_error",
  "failure_reason": "...",
  "usable_for_prompt_feedback": true
}
```

Failed jobs can be useful inspiration for repair prompts, but only if failure is not leakage, broker logic, or split/cost tampering.
