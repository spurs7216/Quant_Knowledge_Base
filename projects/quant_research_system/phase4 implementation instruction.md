You are implementing the next Phase 4 AlphaEvolve-lite milestone.

Important context:
- Local Windows machine is for editing, Git, and review only.
- Remote Linux/GPU server is where all LLM calls, vLLM calls, data inspection, and evaluator runs happen.
- When a remote task calls Qwen, first open a dedicated terminal or tmux pane, launch the required Qwen/vLLM server there, keep it running, and verify `/health` plus `/v1/models` from a separate terminal.
- Do not run Qwen generation yet.
- Do not run a full historical backtest yet.
- Do not assume daily_stock field names until schema/EDA inspection has been run remotely.
- Do not add Gemma.
- Do not add non-daily-stock datasets.
- Do not add IBKR/TWS/broker/account/order logic.
- Do not commit secrets, HF_TOKEN, API keys, or machine-specific credentials.
- Use stage name `controller_static`, not `local_static`.

Goal:
Implement a remote-first preparation milestone that makes the Phase 4 controller and evidence infrastructure real enough for the remote server to run:
1. daily_stock schema inspection,
2. Qwen model evidence formalization,
3. compile/static smoke tests,
before any seed-program generation-zero insertion or child generation.

Implement the following files.

1. Controller scaffold

Create or update:

research/alphaevolve_lite/
  __init__.py
  config.py
  controller.py
  program_database.py
  audit_log.py
  artifact_renderers.py
  stage_names.py
  paths.py

Requirements:
- Implement config parsing from YAML.
- Validate stage names.
- Supported stages for now:
  - controller_static
  - toy_eval
  - sample_eval
  - fast_historical_eval
  - remote_validation
  - review
- Only `controller_static` needs actual behavior now.
- `controller_static` should verify:
  - config file exists and parses;
  - artifact root can be created;
  - SQLite database can be initialized;
  - JSONL audit log can be appended;
  - prompt-card renderer can write an example prompt card;
  - evaluator-summary renderer can write an example evaluator summary;
  - no LLM endpoint is called;
  - no heavy CSV data is loaded.

2. SQLite program database

Implement in:

research/alphaevolve_lite/program_database.py

Use SQLite, not only JSONL.

Minimum tables:
- program_records
- model_test_records
- controller_runs
- artifact_index

`program_records` minimum fields:
- program_id
- parent_id
- root_id
- branch_id
- generation
- island
- mutation_surface
- data_scope
- status
- program_path
- diff_path
- prompt_path
- evaluator_summary_path
- metrics_json
- descriptors_json
- hard_gates_json
- validation_exposure_json
- failure_reason
- created_at

`model_test_records` minimum fields:
- test_id
- model_role
- model_id
- served_model_name
- port
- max_model_len
- gpu_config_json
- command_summary
- result_log_path
- parsed_metrics_json
- decision
- created_at

`controller_runs` minimum fields:
- run_id
- stage
- config_path
- artifact_root
- git_commit
- status
- started_at
- finished_at
- error_message

`artifact_index` minimum fields:
- artifact_id
- run_id
- program_id
- artifact_type
- path
- sha256
- created_at

3. JSONL audit log

Implement:

research/alphaevolve_lite/audit_log.py

Requirements:
- Append-only JSONL.
- Each event has:
  - event_id
  - timestamp
  - event_type
  - run_id
  - payload
- Must support events:
  - controller_started
  - controller_finished
  - config_loaded
  - database_initialized
  - artifact_written
  - schema_inspection_recorded
  - model_test_recorded
  - error

4. Artifact renderers

Implement:

research/alphaevolve_lite/artifact_renderers.py

Add functions:
- render_prompt_card(...)
- render_evaluator_summary(...)
- render_failure_report(...)
- render_controller_static_report(...)

For now these can write deterministic Markdown/JSON example artifacts, but they must use the final artifact shape.

Prompt card fields:
- program_id
- parent_id
- generation
- island
- mutation_surface
- data_scope
- allowed_surfaces
- forbidden_changes
- evaluator_feedback_summary
- inspiration_programs
- strict_output_contract

Evaluator summary fields:
- program_id
- stage
- hard_gates
- metrics
- descriptors
- decision
- failure_reason
- next_prompt_hint
- artifact_paths

5. Stage-name validation

Implement:

research/alphaevolve_lite/stage_names.py

Use explicit enum/constants.

Reject `local_static`.
Use `controller_static`.

If a user passes `local_static`, raise an error saying:
"`local_static` is ambiguous. Use `controller_static` for controller-local static checks."

6. Remote support script: inspect_daily_stock_schema.py

Create:

research/alphaevolve_lite/scripts/inspect_daily_stock_schema.py

Purpose:
Inspect the remote daily_stock CSV schema before implementation assumes field names.

Requirements:
- Input:
  --csv-path
  --out-dir
  --sample-rows default 50000
- Do not load the full 26GB file.
- Read only header and a bounded sample.
- Output:
  daily_stock_schema_report.json
  daily_stock_schema_report.md
- Report:
  - exact column names
  - dtypes inferred from sample
  - missingness by column in sample
  - candidate date columns
  - candidate identifier columns
  - candidate return columns
  - candidate price columns
  - candidate volume columns
  - candidate shares / market-cap-related columns
  - candidate exchange columns
  - candidate security-type/common-equity filter columns
  - min/max sample date if detectable
  - warning if required fields cannot be identified
- Do not implement final exchange/common-equity filters yet.
- Do not implement rolling top-500 universe yet.
- This script only inspects and reports.

7. Remote support script: ae_record_model_test.py

Create:

research/alphaevolve_lite/scripts/ae_record_model_test.py

Purpose:
Formalize measured Qwen test logs as artifacts so model-stack claims link to exact logs.

Requirements:
- Input:
  --model-role
  --model-id
  --served-model-name
  --port
  --log-path
  --db-path
  --out-dir
- Parse or at least store:
  - health pass/fail if visible
  - model-list pass/fail if visible
  - latency mean/median/min/max if visible
  - parse_pass count if visible
  - apply_pass count if visible
  - compile_pass count if visible
  - vector_smoke_pass count if visible
  - critic_json pass/fail if visible
  - medium_context_json pass/fail if visible
- Write:
  model_test_record.json
  model_test_record.md
- Insert one row into `model_test_records`.
- Copy or reference the raw log under the artifact directory.
- If parsing is incomplete, still store the raw log and mark unknown fields as null.
- Do not call vLLM or Qwen from this script.

8. Config file

Create or update:

projects/phase4_search_loop/configs/phase4_stage0_remote_qwen.yaml

Include explicit settings:

stage_names:
  default: controller_static
  allowed:
    - controller_static
    - toy_eval
    - sample_eval
    - fast_historical_eval
    - remote_validation
    - review

runtime:
  execution_location: remote
  local_windows_allowed_actions:
    - edit_code
    - git_commit
    - review_artifacts
  remote_required_actions:
    - qwen_calls
    - data_inspection
    - evaluator_runs
    - program_database_writes

model_stack:
  fast_generator:
    model_id: Qwen/Qwen3.5-9B
    served_model_name: qwen35-9b-fast
    base_url: http://127.0.0.1:8001/v1
    api_key_env: AE_VLLM_API_KEY
    role: primary_generation_and_repair
  medium_reviewer:
    model_id: Qwen/Qwen3.5-27B-FP8
    served_model_name: qwen35-27b-fp8
    base_url: http://127.0.0.1:8020/v1
    api_key_env: AE_VLLM_API_KEY
    role: optional_medium_review
  deep_reviewer:
    model_id: Qwen/Qwen3.6-35B-A3B-FP8
    served_model_name: qwen36-35b-a3b-deep
    base_url: http://127.0.0.1:8010/v1
    api_key_env: AE_VLLM_API_KEY
    role: scheduled_deep_review

data_policy:
  first_loop_scope: daily_stock_only
  split_policy:
    type: chronological
    train_fraction: 0.70
    validation_fraction: 0.15
    test_fraction: 0.15
    construction_order:
      - clean_daily_stock_trading_dates
      - build_chronological_splits
      - compute_universe_membership_inside_each_split
  universe_policy:
    type: rolling_top_n_by_market_cap
    n: 500
    ranking_frequency: monthly
    static_full_period_top_n_forbidden: true
    implementation_status: pending_schema_inspection
  missing_return_policy:
    implementation_status: pending
    rule: explicit_evaluator_logic_required_before_backtest

storage:
  sqlite_db_name: program_database.sqlite
  audit_log_name: audit_log.jsonl
  large_metric_format: parquet
  analysis_engine: duckdb

artifact_policy:
  root: artifacts/phase4_alphaevolve
  compact_outputs_only: true
  heavy_csv_sync_to_local_forbidden: true

dataset_unlock_policy:
  executable_multi_dataset_generation_requires_human_approval: true
  codex_may_write_unlock_review: true
  codex_may_not_unlock_by_itself: true

9. Controller script

Create:

research/alphaevolve_lite/scripts/ae_controller.py

Requirements:
- CLI:
  --config
  --stage
  --run-id optional
- For now implement only `controller_static`.
- It should:
  - load config;
  - validate stage;
  - create artifact run directory;
  - initialize SQLite DB;
  - initialize audit log;
  - write controller_static_report.md;
  - write example prompt_card.json/md;
  - write example evaluator_summary.json/md;
  - record artifacts in artifact_index;
  - write audit events;
  - exit with nonzero status on validation errors.

10. Tests / compile checks

Add simple tests if the repo has a test framework. Otherwise add a smoke script.

At minimum, the following should work locally and remotely without data or Qwen:

python -m compileall research/alphaevolve_lite

python research/alphaevolve_lite/scripts/ae_controller.py \
  --config projects/phase4_search_loop/configs/phase4_stage0_remote_qwen.yaml \
  --stage controller_static

11. Do not implement yet

Do not implement these in this milestone:
- Qwen child generation.
- seed generation-zero DB insert.
- full daily_stock evaluator.
- rolling top-500 construction.
- exchange/common-equity filters.
- missing-return PnL logic.
- multi-dataset feature generation.
- Compustat/options/ownership/IBES joins.
- IBKR/TWS/broker code.

12. Acceptance criteria

This milestone is complete when:

- compileall passes;
- `ae_controller.py --stage controller_static` creates a run directory;
- SQLite DB exists and has required tables;
- JSONL audit log exists and contains controller events;
- prompt-card and evaluator-summary example artifacts exist;
- `inspect_daily_stock_schema.py --help` works;
- `ae_record_model_test.py --help` works;
- no Qwen endpoint is called;
- no large CSV is loaded by controller_static;
- no secrets are committed;
- no references to Gemma remain in active config.
