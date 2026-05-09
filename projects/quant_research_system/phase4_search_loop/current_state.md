---
title: Phase 4 Current State
type: project
status: active
updated: 2026-05-09
tags:
  - project
  - phase4
  - alphaevolve
  - current-state
  - memory
sources:
  - "README.md"
  - "task_001_search_design.md"
  - "task_004_seed_strategy_program.md"
  - "daily_stock_contract_v1.md"
  - "model_stack_and_vllm_results.md"
  - "controller_batch_001_small_review_20260430.md"
  - "controller_batch_001_small_repair_v1_review_20260430.md"
  - "controller_batch_001_small_semantic_v2_review_20260501.md"
  - "controller_batch_001_small_semantic_v3_review_20260501.md"
  - "controller_batch_001_small_semantic_v4_review_20260508.md"
  - "controller_batch_001_review_20260509.md"
  - "reasoning_memory_layer_design.md"
  - "diagnostic_analyzer_and_skill_library_20260504.md"
  - "alphaevolve_extension_methods_20260509.md"
  - "controller_batch_001_remote_instructions_20260508.md"
  - "controller_batch_001_diversity_topup_remote_instructions_20260509.md"
---
# Phase 4 Current State

This is the compact working-memory entry point for Phase 4. Use it before reading dated run reviews.

## One-Screen State

Phase 4 is building a bounded AlphaEvolve-style search loop for daily-stock equity strategies.

The first production loop is:

```yaml
data_scope: daily_stock_only
seed_family: Kalman innovation / reversal
universe: rolling top-500 by lagged DlyCap
split: chronological 70/15/15
generator: Qwen3.5-9B on remote Linux/GPU server
mutation_format: SEARCH/REPLACE inside named evolve-block bodies
controller_gate: controller_static before any data-backed child evaluation
test_set_use: forbidden until branch freeze
```

The current remote milestone is still controller-static child generation, not child historical evaluation. The latest reviewed artifact is:

```text
artifacts/controller_batch_001.zip
```

`controller_batch_001` proved the controller mechanics at 50 attempts but did not meet the uniqueness gate: 35/50 controller-static passes, 15 duplicate-child rejects, all parse/apply/compile/vector/semantic gates at 1.0, no empty/reasoning-only outputs, database insertion at 1.0, and 12 MAP cells occupied. Duplicates were concentrated in `ranking/direction_flip`. This is still not market evaluation and not a completed AlphaEvolve evolution round. Do not run child `remote_sample_eval` yet. The next action is a 20-attempt controller-only diversity top-up using prior-summary duplicate seeding.

The CodeEvolve, ShinkaEvolve, and ThetaEvolve readthrough confirms that this duplicate issue should be treated as a population/database policy problem, not only a prompt wording problem. `controller_population_policy_v2` is now implemented for the next top-up: it tracks parent offspring counts, surface/intent saturation, prompt-card duplicate rates, prompt-card fitness, deterministic lazy penalties for invalid/duplicate outputs, and edit-signature near duplicates before market evaluation.

Current evolution status:

```yaml
child_generation_done: partial
controller_static_small_batch_passed: true
controller_static_50_batch_passed: false_due_to_duplicate_generation
child_market_evaluation_done: false
iterative_evolution_round_done: false
next_stage: controller_batch_001_diversity_topup
```

## AlphaEvolve Modules In This Project

| AlphaEvolve module | Phase 4 design |
| --- | --- |
| Prompt sampler | `prompt_builder.py` samples parent code slices, target surfaces, prior accepted same-surface patches, evaluator summaries, diagnostic cards, skill cards, dataset/cost context, and wiki/catalog reminders. |
| LLM ensemble | Qwen-only remote stack: Qwen3.5-9B for child generation and repair, Qwen3.5-27B-FP8 for optional medium review, Qwen3.6-35B-A3B-FP8 for scheduled deep review. |
| Evaluator pools | `controller_static` first; later `toy_eval`, `remote_sample_eval`, stage-0 validation, full validation, artifact review, and branch-freeze/test unlock. |
| Program database | SQLite plus JSONL audit log under `artifacts/phase4_alphaevolve/`, storing every generated child, failure, prompt, diff, descriptors, metrics, and validation exposure. |

The program database is different from the Phase 3 candidate registry. The database is search memory; the registry is reviewed research lineage.

Dr. RTL adds two additional controller-side roles now implemented in the local scaffold:

- diagnostic analyzer: deterministic bottleneck cards from evaluator/controller artifacts;
- explicit skill library: confidence/status-tagged pattern -> strategy rules retrieved into prompts.

## Frozen Contracts

Stable decisions:

- Local Windows edits, reviews, and syncs through GitHub. It must not run Qwen or heavy warehouse evaluation.
- Remote Linux/GPU server runs Qwen, controller child batches, database writes, toy/sample/full evaluators, and CSV warehouse access.
- Before any remote Qwen call, the remote operator must open a persistent terminal or `tmux` pane, launch vLLM, keep it running, and verify `/health` plus `/v1/models` from a separate terminal.
- The active data contract is [daily_stock_contract_v1.md](daily_stock_contract_v1.md), frozen from `schema_evidence_v2`.
- The active cost policy is [cost_model_policy.md](cost_model_policy.md), with costs as evaluator stress tests and prompt-facing diagnostics, not evolvable constants.
- The active model decision is [model_stack_and_vllm_results.md](model_stack_and_vllm_results.md). Gemma is not active.
- Dataset additions are locked by [dataset_admission_policy.md](dataset_admission_policy.md). The prompt sampler may mention available datasets, but generated children may not add non-daily-stock inputs without human approval.

## Current daily_stock Memory

The verified first-loop fields are:

```yaml
date: DlyCalDt
security_id: PERMNO
issuer_id: PERMCO
total_return: DlyRet
ex_dividend_return: DlyRetx
price: DlyPrc
volume: DlyVol
dollar_volume: DlyPrcVol
market_cap: DlyCap
shares_outstanding: ShrOut
exchange: PrimaryExch
security_type: SecurityType
share_type: ShareType
trading_status: TradingStatusFlg
conditional_type: ConditionalType
us_incorporated: USIncFlg
industry_primary: SICCD
benchmark_return_primary: vwretd
benchmark_return_secondary: sprtrn
```

Important caveat: schema evidence froze field names, not the full cross-sectional distribution. The CSV appears sorted by security then date, so first-N-row samples are not representative cross-section samples. Data-backed evaluators must use bounded date-window or chunked loading when cross-sectional coverage matters.

## Controller Evidence Timeline

| Evidence | Result | Lesson now retained |
| --- | --- | --- |
| `phase4_alphaevolve` remote evidence | `controller_static`, SQLite, audit log, model record, and schema inspection worked. First Qwen probe failed because vLLM was not running. | Treat missing vLLM as operator preflight failure. Remote Qwen tasks must explicitly start and verify the server. |
| `schema_evidence_v2` | 50,000-row schema run froze `daily_stock_contract_v1`. | Stop relying on assumed field names; use the verified daily-stock contract. |
| `remote_sample_eval_seed_v2` | Hardened sample evaluator became usable as prompt/evaluator context. | The seed is an evaluator-readiness parent, not evidence of a tradable strategy. |
| `controller_batch_001_small` | 0/5 pass, but parse, exact match, and DB insertion worked. All failures were evolve-block boundary failures. | Prompt exposed too much code. Slice to one editable block body and keep the micro-filter strict. |
| `controller_batch_001_small_repair_v1` | 5/5 pass, but duplicates and one semantically invalid portfolio appeared. | Syntax, compile, and vector smoke are not enough. Add portfolio semantic gates and duplicate child hashes. |
| `controller_batch_001_small_semantic_v2` | Two 10-attempt runs each produced 6 unique semantic-pass children. Failures were empty/reasoning-only output, portfolio semantic errors, and vector/API mistakes. | Add top-level no-thinking routing, final-content retry, semantic/vector repair, and stronger surface-specific guidance. |
| `controller_batch_001_small_semantic_v3` | 7/10 pass, parse/apply/compile/vector/semantic all 1.0, no empty output, no reasoning-only output, DB insert 1.0, three duplicate-child rejects. | No-thinking routing worked. Duplicate generation is now the controller bottleneck. |
| `controller_batch_001_small_semantic_v4` | 10/10 pass, all controller-static gates 1.0, no empty output, no reasoning-only output, DB insert 1.0, duplicate child count 0, duplicate retry success 1.0, 8 MAP cells occupied. | Duplicate-retry hardening and MAP-style targeting are sufficient to scale to a 50-attempt controller-only batch. Controller pass is not market alpha. |
| `controller_batch_001` | 35/50 pass, all controller mechanics healthy, no empty/reasoning-only outputs, no semantic failures, DB insert 1.0, 12 MAP cells occupied, but 15 duplicate-child rejects. Ranking produced only 3/13 pass because 10 attempts fell into duplicate-heavy ranking changes, mostly `direction_flip`. | Do not launch market evaluation yet. Patch prompt intent specificity, seed prior duplicate/MAP state into top-up runs, and run a 20-attempt controller-only diversity top-up. |

## Failure Memory

Keep these lessons in future prompt and controller design:

- Full-program prompts invite marker copying and helper edits. Give the model only one target evolve-block body.
- One SEARCH/REPLACE block is safer than many blocks in the first controller loop.
- `semantic` means program/trading-logic invariants, not market alpha. It checks both-side exposure, sign direction, gross/net exposure, max weight, and basic portfolio shape.
- Market validity comes later through sample/full evaluators with costs, nulls, turnover, liquidity, concentration, subperiod checks, and held-out validation discipline.
- Signal-proportional portfolio weights can accidentally remove the short book if negative short-side signals are used as magnitudes.
- Hard saturation such as naive `tanh` can preserve sign but still produce tied or dense books with bad net exposure.
- Qwen can spend the whole completion budget in reasoning with `message.content = null`; the raw HTTP payload must pass `chat_template_kwargs.enable_thinking=false` at top level and retry empty final content once.
- `max_tokens` is a completion-token budget, not the full context window. The active child-generation and repair budget is `8192`; `semantic_v3` showed the null-content failure was fixed by disabling Qwen thinking mode, not by needing a 16k completion budget. Launch the remote 9B vLLM server with `--max-model-len 32768` if memory allows, or fall back to `16384` while keeping completion tokens at `8192`.
- Duplicate children should be stored but not counted as unique controller passes.
- Generic surface guidance can conflict with MAP target cells. After `controller_batch_001`, the ranking prompt must make target intent mandatory and must not present direction flipping as a generic ranking option.
- A diversity top-up must seed prior child hashes, patch fingerprints, accepted patches, and occupied MAP cells from the prior `summary.json`; otherwise a new process can regenerate already accepted children.
- Extension-method memory: CodeEvolve points to prompt fitness, plateau-triggered exploration, island topology, and MAP-Elites as search-control mechanisms; ShinkaEvolve points to parent offspring-count penalties and novelty rejection; ThetaEvolve points to lazy penalties for no-op or duplicate outputs.
- Controller population policy v2 plus `prompt_fitness_and_lazy_score_v1` is the active deterministic translation of those lessons. It does not use embeddings, LLM novelty judges, reward shaping, or RL; it only changes controller-local selection, prompt context, duplicate/near-duplicate accounting, prompt-card fitness, lazy penalties, and artifacts.
- A 16,384 completion-token budget appears in ShinkaEvolve and ThetaEvolve experiments, but Phase 4 should change token budgets based on artifacts. The prior null-content issue was solved by no-thinking routing, not by token budget alone.
- API mistakes such as pandas `.clip(max=...)` instead of `.clip(upper=...)` belong in repairable vector-smoke failure memory.

## Reasoning Memory Layer

Phase 4 now treats these lessons as a formal ReasoningBank-style layer rather than only prose inside this current-state file.

[reasoning_memory_layer_design.md](reasoning_memory_layer_design.md) defines the new memory item schema, extraction workflow, prompt-injection rule, and implementation milestones. The design follows [[ReasoningBank - Scaling Agent Self-Evolving with Reasoning Memory]] but adapts it for quant research by using deterministic controller/evaluator outcomes as the source of success/failure labels.

The memory bank is distinct from the program database:

- program database: exhaustive evidence for every generated child;
- reasoning memory bank: compact, evidence-linked lessons retrieved into future prompts.

The explicit skill library is a third layer. It is narrower than reasoning memory and stores operational pattern -> strategy rules with `high`, `medium`, `low`, or `avoid` confidence. New `skill_update.json` entries from a small controller batch are candidate-level only until deterministic evidence supports promotion.

## Current Next Step

After `controller_batch_001`, controller mechanics are healthy but the uniqueness gate is not met. The next action is a 20-attempt controller-only diversity top-up after pulling the local prompt/scheduler/prior-summary patch.

Expected remote command:

```bash
python research/alphaevolve_lite/scripts/run_child_batch.py \
  --program-path research/alphaevolve_lite/seeds/kalman_reversal_seed.py \
  --evaluator-summary artifacts/phase4_alphaevolve/remote_sample_eval_refactor_smoke_20260507/evaluator_summary.json \
  --out-dir artifacts/phase4_alphaevolve/controller_batch_001_diversity_topup \
  --db-path artifacts/phase4_alphaevolve/program_database.sqlite \
  --attempts 20 \
  --model-role fast_generator \
  --max-tokens 8192 \
  --memory-card-limit 3 \
  --diagnostic-card-limit 4 \
  --skill-card-limit 3 \
  --duplicate-retry-attempts 2 \
  --population-policy-version v2 \
  --near-duplicate-threshold 0.88 \
  --surface-schedule ranking,signal,portfolio,risk \
  --prior-summary artifacts/phase4_alphaevolve/controller_batch_001/summary.json
```

Review gates:

```yaml
target_controller_batch_001_diversity_topup:
  attempt_count: 20
  prior_summary_loaded: true
  prior_pass_count: 35
  unique_semantic_pass_children: "at least 12 of 20"
  aggregate_unique_controller_pass_children: "at least 45 across controller_batch_001 plus top-up"
  empty_output_rate: 0
  reasoning_only_empty_count: 0
  duplicate_child_count: "target <= 5 of 20"
  ranking_direction_flip_duplicate_pocket: "reduced"
  duplicate_retry_success_rate: "reported"
  map_cell_count: "reported"
  population_policy_version: "controller_population_policy_v2"
  near_duplicate_patch_count: "reported"
  prompt_card_duplicate_counts: "reported"
  prompt_fitness_policy_version: "prompt_fitness_and_lazy_score_v1"
  prompt_card_fitness: "reported"
  prompt_card_lazy_penalty_sums: "reported"
  controller_search_score_mean: "reported"
  lazy_penalty_attempt_count: "reported"
  low_prompt_card_fitness_diagnostic: "reported if triggered"
  reasoning_memory_enabled: true
  reasoning_memory_update_written: true
  group_relative_controller_report_written: true
  evaluator_diagnostic_report_written: true
  controller_diagnostic_report_written: true
  skill_library_enabled: true
  skill_update_written: true
  db_insert_pass_rate: "near 1.0"
  remote_sample_eval_launched: false
  full_validation_launched: false
```

If the top-up fails, inspect target-intent compliance in the ranking prompts before changing evaluator gates. If it passes, do not evaluate all generated children on market data. First select a smaller diverse set of nontrivial children for `remote_sample_eval`.

## Main Links

- Active design: [README.md](README.md), [task_001_search_design.md](task_001_search_design.md), [task_004_seed_strategy_program.md](task_004_seed_strategy_program.md)
- Contracts: [daily_stock_contract_v1.md](daily_stock_contract_v1.md), [prompt_contracts.md](prompt_contracts.md), [evaluator_contract.md](evaluator_contract.md), [program_database_schema.md](program_database_schema.md)
- Memory and skills: [reasoning_memory_layer_design.md](reasoning_memory_layer_design.md), [dr_rtl_method_transfer_20260504.md](dr_rtl_method_transfer_20260504.md), [diagnostic_analyzer_and_skill_library_20260504.md](diagnostic_analyzer_and_skill_library_20260504.md), [alphaevolve_extension_methods_20260509.md](alphaevolve_extension_methods_20260509.md), [Reasoning Memory for AlphaEvolve Search](../../../wiki/methods/Reasoning%20Memory%20for%20AlphaEvolve%20Search.md), [Group-Relative Skill Learning for Alpha Search](../../../wiki/methods/Group-Relative%20Skill%20Learning%20for%20Alpha%20Search.md), [AlphaEvolve Extension Methods for Quant Search](../../../wiki/methods/AlphaEvolve%20Extension%20Methods%20for%20Quant%20Search.md)
- Data and costs: [dataset_context.md](dataset_context.md), [dataset_admission_policy.md](dataset_admission_policy.md), [universe_and_split_policy.md](universe_and_split_policy.md), [cost_model_policy.md](cost_model_policy.md)
- Remote/runtime: [remote_qwen_vllm_config.md](remote_qwen_vllm_config.md), [remote_csv_execution_policy.md](remote_csv_execution_policy.md), [model_stack_and_vllm_results.md](model_stack_and_vllm_results.md)
- Dated evidence records: [remote_evidence_review_20260430.md](remote_evidence_review_20260430.md), [controller_batch_001_small_review_20260430.md](controller_batch_001_small_review_20260430.md), [controller_batch_001_small_repair_v1_review_20260430.md](controller_batch_001_small_repair_v1_review_20260430.md), [controller_batch_001_small_semantic_v2_review_20260501.md](controller_batch_001_small_semantic_v2_review_20260501.md), [controller_batch_001_small_semantic_v3_review_20260501.md](controller_batch_001_small_semantic_v3_review_20260501.md), [controller_batch_001_small_semantic_v4_review_20260508.md](controller_batch_001_small_semantic_v4_review_20260508.md), [controller_batch_001_review_20260509.md](controller_batch_001_review_20260509.md)
- Remote handoff: [controller_batch_001_remote_instructions_20260508.md](controller_batch_001_remote_instructions_20260508.md), [controller_batch_001_diversity_topup_remote_instructions_20260509.md](controller_batch_001_diversity_topup_remote_instructions_20260509.md), [configs/controller_batch_001_remote_qwen.yaml](configs/controller_batch_001_remote_qwen.yaml)
- Durable method memory: [AlphaEvolve Lite Quant Search Workflow](../../../wiki/methods/AlphaEvolve%20Lite%20Quant%20Search%20Workflow.md), [AlphaEvolve Extension Methods for Quant Search](../../../wiki/methods/AlphaEvolve%20Extension%20Methods%20for%20Quant%20Search.md)
