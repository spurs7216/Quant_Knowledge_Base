---
title: Phase 4 Search Loop
type: project
status: active
updated: 2026-05-14
tags:
  - project
  - phase4
  - search-loop
  - alphaevolve
  - qwen
  - sampling-policy
---
# Phase 4 Search Loop

## Start Here

Use [current_state.md](current_state.md) as the compact entry point before reading dated run reviews. It combines the current decisions, evidence timeline, failure memory, and next remote action.

The dated run reviews remain useful evidence records, but they should not be treated as separate active plans once their lessons have been folded into `current_state.md` and the implementation tasks.

## Purpose

Phase 4 builds a bounded AlphaEvolve-style search loop for quantitative research.

The goal is not to let an agent freely rewrite the research system. The goal is to generate controlled executable child programs, evaluate them through a fixed cascade, store every result in a program database, and promote only candidates that survive strict research-validity gates.

The AlphaEvolve transfer is:

```text
parent_program, inspirations = database.sample()
prompt = prompt_sampler.build(parent_program, inspirations)
diff = llm.generate(prompt)
child_program = apply_diff(parent_program, diff)
results = evaluator.execute(child_program)
database.add(child_program, results)
```

For quant research, this loop is useful only if the evaluator is stronger than the generator. Search must not win by changing splits, hiding turnover, removing costs, creating data leakage, shrinking coverage, or repeatedly overfitting the same validation interval.

## Current Non-Negotiable Decisions

### System boundary

The local vault is the memory and control layer. The remote Linux/GPU/data server is the heavy data and compute layer. IBKR/TWS access is local-only. Remote jobs must not require broker connectivity, TWS, IB Gateway, account state, position state, order submission, or broker credentials.

The local Windows machine cannot run Qwen or other Phase 4 LLM inference because of memory constraints. In Phase 4, all Qwen calls, AlphaEvolve-lite controller execution, program-database updates, static/generated-code filters, toy evaluators, sample evaluators, and warehouse-backed evaluators run on the remote Linux/GPU/data server. The local Windows machine edits code and markdown, uses GitHub for sync, and reviews compact artifacts.

Executable stage names must avoid the ambiguous word `local`. Use `controller_static` for cheap static/micro-filter work run by the remote controller.

### First production loop

The first production loop is daily-stock-only.

```yaml
phase4_first_loop:
  data_scope: daily_stock_only
  split_policy: chronological_70_15_15
  universe_policy: rolling_top500_market_cap
  universe_recompute: monthly_from_prior_month_end
  candidate_unit: executable_seed_strategy_module
  mutation_format: SEARCH_REPLACE_diffs_inside_evolve_blocks
  model_stack: qwen_only
  test_set_use: forbidden_until_branch_freeze
```

The rolling top-500 list is not static. It must be recomputed through time from lagged market capitalization information available at or before the formation date. This avoids survivorship and future-membership leakage.

### Storage and execution

```yaml
storage_decision:
  search_metadata: SQLite
  audit_log: JSONL append-only
  large_metric_panels: Parquet when available; CSV fallback allowed
  analysis_reporting: DuckDB when available; SQLite/pandas fallback allowed

remote_constraints:
  warehouse_format: CSV
  no_external_exe_assumption: true
  heavy_data_stays_remote: true
  local_vault_receives_only_compact_artifacts: true
```

No design should assume that external `.exe` files can be installed on the remote server. Python packages may be used if the environment permits them, but the fallback must work with standard Python, pandas/chunked CSV, and SQLite.

## Current Model Stack

Gemma 4 is retired from the active model stack.

| Role | Model | Status | Use |
| --- | --- | --- | --- |
| `fast_generator` | `Qwen/Qwen3.5-9B` | primary | high-throughput SEARCH/REPLACE proposals |
| `critic_repair` | `Qwen/Qwen3.5-9B` | primary | repair malformed diffs, shrink oversized patches, enforce evolve-block rules |
| `medium_quality_reviewer` | `Qwen/Qwen3.5-27B-FP8` | optional | evaluator-summary review and medium-depth mutation-surface proposals |
| `deep_generator` | `Qwen/Qwen3.6-35B-A3B-FP8` | scheduled only | high-level search-state synthesis and hard strategy-logic proposals |
| `micro_filter` | deterministic code | mandatory | parse, exact-match, evolve-block, AST/name, compile, vector-smoke, schema validation |

Measured policy:

- `Qwen3.5-9B` is the default inner-loop model because it passed strict patching, oversized-patch repair, compile, undeclared-name checks, semantic checks, NumPy/pandas vector smoke, critic JSON, medium-context JSON, and 10/10 batch patch quality.
- `Qwen3.5-27B-FP8` should not be the default patch generator because it produced an oversized SEARCH block in testing. It can still be useful as a reviewer and medium-context idea source.
- `Qwen3.6-35B-A3B-FP8` passed deep-model tests but is slower and uses both GPUs, so it is reserved for scheduled deep batches.
- `Gemma 4 E4B-it` is removed from the active model design.

## Package

Compact entry point:

- [current_state.md](current_state.md): current decisions, evidence timeline, failure memory, and next remote action.

Core design files:

- [../phase4_codex_clarifications.md](../phase4_codex_clarifications.md): implementation clarifications for remote-only Qwen, stage naming, schema verification, split construction, missing-return policy, and dataset unlock authority.
- [alphaevolve_method_translation.md](alphaevolve_method_translation.md): paper-grounded translation of AlphaEvolve into this quant research system.
- [task_001_search_design.md](task_001_search_design.md): source-of-truth search-loop design. Do not bypass it.
- [task_002_kalman_reversal_batch.md](task_002_kalman_reversal_batch.md): pre-evolution evaluator seed for the Kalman innovation reversal family.
- [task_003_alphaevolve_scaffold.md](task_003_alphaevolve_scaffold.md): local scaffold for evolve blocks, diffs, and program database primitives.
- [task_004_seed_strategy_program.md](task_004_seed_strategy_program.md): implementation task that executes Task 001; it does not replace Task 001.

New implementation-policy files:

- [phase4_sampling_policy_v1.md](phase4_sampling_policy_v1.md): data-aware MAP-Elites + island sampling policy.
- [daily_stock_contract_v1.md](daily_stock_contract_v1.md): frozen `daily_stock` field mapping, fixed eligibility filters, and seed evaluator command.
- [program_database_schema.md](program_database_schema.md): SQLite schema, JSONL audit log, and descriptor fields.
- [universe_and_split_policy.md](universe_and_split_policy.md): 70/15/15 split and rolling top-500 universe rules.
- [dataset_admission_policy.md](dataset_admission_policy.md): staged dataset unlock and point-in-time join requirements.
- [processed_outputs_policy.md](processed_outputs_policy.md): how to use processed research CSV outputs and validate source scripts.
- [remote_csv_execution_policy.md](remote_csv_execution_policy.md): remote CSV execution, artifact, and storage rules.
- [prompt_contracts.md](prompt_contracts.md): exact prompt modes, output rules, repair prompts, and model routing.
- [artifact_renderer_contract.md](artifact_renderer_contract.md): compact prompt-card and evaluator-summary artifacts.
- [reasoning_memory_layer_design.md](reasoning_memory_layer_design.md): ReasoningBank-style memory layer for turning batch successes and failures into retrievable prompt lessons.
- [dr_rtl_method_transfer_20260504.md](dr_rtl_method_transfer_20260504.md): Dr. RTL transfer note for group-relative sibling comparison and skill learning.
- [diagnostic_analyzer_and_skill_library_20260504.md](diagnostic_analyzer_and_skill_library_20260504.md): implementation note for the deterministic analyzer role and explicit skill-library layer.
- [alphaevolve_extension_methods_20260509.md](alphaevolve_extension_methods_20260509.md): CodeEvolve, ShinkaEvolve, and ThetaEvolve transfer note for duplicate control, parent sampling, novelty pressure, and deferred RL.
- [attempt017_mechanism_design_20260513.md](attempt017_mechanism_design_20260513.md): concrete daily-stock-only mechanism targets for the attempt017 branch.
- [codex_implementation_tasks.md](codex_implementation_tasks.md): concrete Codex implementation sequence.
- [configs/controller_batch_001_remote_qwen.yaml](configs/controller_batch_001_remote_qwen.yaml): 50-attempt controller-only remote run preset.
- [controller_batch_001_diversity_topup_remote_instructions_20260509.md](controller_batch_001_diversity_topup_remote_instructions_20260509.md): diversity top-up handoff after the 50-attempt duplicate bottleneck.

Existing policy files included for completeness:

- [model_stack_and_vllm_results.md](model_stack_and_vllm_results.md)
- [cost_model_policy.md](cost_model_policy.md)
- [dataset_context.md](dataset_context.md)
- [evaluator_contract.md](evaluator_contract.md)
- [phase4_evaluator_improvement_plan.md](phase4_evaluator_improvement_plan.md)

Dated review records retained as evidence, not active plans:

- [phase4_readthrough.md](phase4_readthrough.md): old-plan comparison and adoption record.
- [remote_evidence_review_20260430.md](remote_evidence_review_20260430.md): remote schema/model/controller evidence review.
- [remote_sample_eval_hardening_20260430.md](remote_sample_eval_hardening_20260430.md): seed sample-evaluator hardening record.
- [controller_child_dry_run_20260430.md](controller_child_dry_run_20260430.md): first child dry-run protocol record.
- [controller_batch_001_small_review_20260430.md](controller_batch_001_small_review_20260430.md): first failed small child batch review.
- [controller_batch_001_small_repair_v1_review_20260430.md](controller_batch_001_small_repair_v1_review_20260430.md): repair-enabled small child batch review.
- [controller_batch_001_small_semantic_v2_review_20260501.md](controller_batch_001_small_semantic_v2_review_20260501.md): semantic-gated small batch review.
- [controller_batch_001_small_semantic_v3_review_20260501.md](controller_batch_001_small_semantic_v3_review_20260501.md): no-thinking and larger-token-budget small batch review.
- [controller_batch_001_small_semantic_v4_review_20260508.md](controller_batch_001_small_semantic_v4_review_20260508.md): duplicate-retry and MAP-cell small batch review.
- [controller_batch_001_remote_instructions_20260508.md](controller_batch_001_remote_instructions_20260508.md): 50-attempt controller-only remote handoff.
- [controller_batch_001_review_20260509.md](controller_batch_001_review_20260509.md): 50-attempt controller run review; mechanics healthy but uniqueness gate failed.
- [controller_attempt017_focused_round_review_20260511.md](controller_attempt017_focused_round_review_20260511.md): focused attempt017 round review; one child improved missing-held weight but failed parent-relative performance and turnover-aware criteria.
- [controller_attempt017_search_control_remote_instructions_20260511.md](controller_attempt017_search_control_remote_instructions_20260511.md): next small controller-only focused run after the search-control patch.
- [controller_attempt017_search_control_rerun_review_20260513.md](controller_attempt017_search_control_rerun_review_20260513.md): search-control rerun review; controller healthy but no sample-eval candidate.
- [controller_attempt017_mechanism_batch_remote_instructions_20260513.md](controller_attempt017_mechanism_batch_remote_instructions_20260513.md): next controller-only mechanism batch handoff.
- [controller_attempt017_mechanism_batch_review_20260514.md](controller_attempt017_mechanism_batch_review_20260514.md): mechanism batch plus attempt007 sample-eval review; one selected child was broad but worse than attempt017, and portfolio/risk mechanism prompts need local data-scope repair.
- [controller_prompt_smoke_repair_20260514.md](controller_prompt_smoke_repair_20260514.md): local prompt/smoke repair for surface-local daily-stock field access and multi-industry/liquidity smoke coverage.
- [controller_attempt017_mechanism_rerun_remote_instructions_20260514.md](controller_attempt017_mechanism_rerun_remote_instructions_20260514.md): remote rerun handoff after the prompt/smoke repair, including Git hygiene preflight.
- [controller_attempt017_mechanism_rerun_review_20260514.md](controller_attempt017_mechanism_rerun_review_20260514.md): rerun plus attempt009 sample-eval review; attempt009 improved implementation shape but weakened parent-relative return and Sharpe.
- [controller_attempt017_27b_mechanism_cards_remote_instructions_20260514.md](controller_attempt017_27b_mechanism_cards_remote_instructions_20260514.md): next remote handoff using Qwen3.5-27B-FP8 for JSON mechanism cards and Qwen3.5-9B for strict patches.

## Search Principle

Search is allowed only inside bounded executable strategy artifacts.

A remote validation batch is only an evaluator artifact. An AlphaEvolve-style loop requires:

- executable programs with `# EVOLVE-BLOCK-START` / `# EVOLVE-BLOCK-END` markers
- generated SEARCH/REPLACE diffs
- deterministic patch application
- `controller_static` preflight and smoke tests on the remote server
- evaluator feedback as scalar metrics and hard-gate diagnostics
- deterministic diagnostic cards that localize evaluator/controller bottlenecks before generation
- explicit skill cards with confidence/status, separate from raw program memory
- a program database that stores every generated program, not just winners
- parent/inspiration sampling that balances exploitation and diversity
- population policies that track duplicate pressure, parent offspring counts, prompt fitness, and MAP-cell occupancy
- deterministic near-duplicate checks over edit signatures before any market evaluator is launched

The candidate registry and program database are different:

- Program database: search-time memory of many programs, including weak, rejected, repaired, and near-valid programs.
- Candidate registry: official research lineage for reviewed candidates worth preserving.

## Initial Search Family

The first family remains daily-stock reversal / Kalman innovation reversal.

Task 002 remains a pre-evolution evaluator seed. It tests the evaluator, null controls, cost sensitivity, concentration metrics, and dataset diagnostics. Task 004 turns that family into the first true evolved seed program.

## Initial Sampling Policy

Use `phase4_sampling_v1` from [phase4_sampling_policy_v1.md](phase4_sampling_policy_v1.md):

```yaml
phase4_sampling_v1:
  active_data_stage: stage_0_daily_stock
  active_islands:
    daily_stock_signal: 0.45
    ranking_transform: 0.15
    portfolio_risk_turnover: 0.20
    neutralization_liquidity: 0.10
    repair_near_miss: 0.05
    negative_control: 0.05
  model_routing:
    child_generation: Qwen3.5-9B
    repair: Qwen3.5-9B
    medium_review: Qwen3.5-27B-FP8 every 30 children
    deep_review: Qwen3.6-35B-A3B-FP8 every 50 children
```

Dataset additions are disabled until the daily-stock loop has stable `controller_static`, `toy_eval`, and `remote_sample_eval` behavior.

## Exit Criteria For Phase 4 Initial Loop

The first loop is complete when:

- seed program exists with at least signal and portfolio evolve blocks
- the rolling top-500-by-market-cap universe is reproducible and point-in-time safe
- the 70/15/15 chronological split is fixed under a named `split_id`
- `Qwen3.5-9B` first produces a small auditable controller dry run, then can generate 50+ children through the remote server's localhost vLLM API
- every child is stored in the program database with lineage and result status
- malformed/oversized patches are repaired once or rejected
- `controller_static` produces valid `evaluator_summary.json`
- at least one child reaches `remote_sample_eval` before any full validation
- no test-set evaluation is used before branch freeze
- parent/inspiration sampling uses score, novelty, MAP-Elites descriptors, and validation-exposure penalties
- a human can trace every promoted candidate back to parent code, prompt, diff, controller_static gates, remote artifacts, and decision reason
