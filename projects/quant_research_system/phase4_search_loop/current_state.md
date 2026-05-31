---
title: Phase 4 Current State
type: project
status: active
updated: 2026-05-31
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
  - "controller_batch_001_diversity_topup_review_20260509.md"
  - "remote_sample_eval_controller_batch_001_review_20260509.md"
  - "reasoning_memory_layer_design.md"
  - "diagnostic_analyzer_and_skill_library_20260504.md"
  - "alphaevolve_extension_methods_20260509.md"
  - "controller_batch_001_remote_instructions_20260508.md"
  - "controller_batch_001_diversity_topup_remote_instructions_20260509.md"
  - "controller_batch_001_curated_sample_eval_remote_instructions_20260509.md"
  - "controller_batch_001_attempt017_repair_remote_instructions_20260509.md"
  - "controller_batch_001_attempt017_repair_hardening_20260510.md"
  - "controller_evaluator_hardening_remote_instructions_20260510.md"
  - "controller_evaluator_hardening_smoke_review_20260511.md"
  - "controller_attempt017_focused_round_review_20260511.md"
  - "controller_attempt017_search_control_remote_instructions_20260511.md"
  - "controller_attempt017_search_control_rerun_review_20260513.md"
  - "attempt017_mechanism_design_20260513.md"
  - "controller_attempt017_mechanism_batch_remote_instructions_20260513.md"
  - "controller_attempt017_mechanism_batch_review_20260514.md"
  - "controller_prompt_smoke_repair_20260514.md"
  - "controller_attempt017_mechanism_rerun_remote_instructions_20260514.md"
  - "controller_attempt017_mechanism_rerun_review_20260514.md"
  - "controller_attempt017_27b_mechanism_cards_remote_instructions_20260514.md"
  - "remote_sample_eval_controller_attempt017_27b_card_batch_review_20260515.md"
  - "sample_eval_novelty_hardening_20260515.md"
  - "controller_attempt017_novelty_smoke_remote_instructions_20260516.md"
  - "controller_attempt017_novelty_smoke_review_20260517.md"
  - "forced_target_cell_schedule_patch_20260517.md"
  - "controller_attempt017_forced_cell_smoke_remote_instructions_20260517.md"
  - "controller_attempt017_forced_cell_smoke_review_20260517.md"
  - "controller_execution_effect_hardening_20260517.md"
  - "controller_attempt017_execution_effect_smoke_remote_instructions_20260517.md"
  - "controller_attempt017_execution_effect_smoke_review_20260518.md"
  - "daily_stock_data_understanding_plan_20260518.md"
  - "daily_stock_eda_remote_instructions_20260518.md"
  - "daily_stock_eda_full_review_20260518.md"
  - "daily_stock_forward_coverage_remote_instructions_20260518.md"
  - "daily_stock_forward_coverage_review_20260519.md"
  - "is_os_evaluation_policy_20260519.md"
  - "evaluator_forward_return_contract_repair_20260519.md"
  - "remote_sample_eval_is_os_forward_repair_rerun_20260519.md"
  - "remote_sample_eval_is_os_forward_repair_review_20260520.md"
  - "controller_attempt017_is_os_cost_robustness_remote_instructions_20260520.md"
  - "seed_zoo_parent_discovery_20260521.md"
  - "seed_zoo_remote_instructions_20260521.md"
  - "seed_zoo_is_os_review_20260522.md"
  - "parent_zoo_cost_aware_remote_instructions_20260522.md"
  - "parent_zoo_cost_aware_review_20260522.md"
  - "parent_zoo_curated_sample_eval_remote_instructions_20260522.md"
  - "remote_sample_eval_pzoo_0_review_20260525.md"
  - "alphaagentevo_transfer_20260525.md"
  - "daily_stock_expression_evolution_v1.md"
  - "phase4_caveat_repair_ledger.md"
  - "expression_seed_zoo_remote_instructions_20260525.md"
  - "expression_seed_zoo_review_20260525.md"
  - "expression_episode_remote_instructions_20260526.md"
  - "expression_episode_20260526_review.md"
  - "expression_bridge_followup_review_20260526.md"
  - "expression_bridge_robustness_review_20260526.md"
  - "expression_episode_v2_memory_20260531.md"
  - "expression_episode_v2_remote_instructions_20260531.md"
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
split: fixed IS/OS, 2011-2022 IS and 2023-2025 OS
generator: Qwen3.5-9B on remote Linux/GPU server
mutation_format: SEARCH/REPLACE inside named evolve-block bodies
controller_gate: controller_static before any data-backed child evaluation
test_set_use: forbidden until branch freeze
```

The controller-static population gate is satisfied, the seed-zoo parent-discovery sample evaluation has been reviewed, the first controller-only parent-zoo cost-aware run has been reviewed, its curated sample-eval follow-up has been reviewed, the first expression seed-zoo baseline has been reviewed, and the first expression bridge robustness run has been reviewed. The latest reviewed artifact is:

```text
artifacts/expression_bridge_robustness_20260526.zip
```

The similarly named older `artifacts/remote_sample_eval_.zip` is a zero-byte corrupt placeholder and should be ignored.

`controller_batch_001` produced 35/50 unique controller-static pass children but missed the uniqueness gate because 15 attempts were duplicate rejects, mostly in `ranking/direction_flip`. The follow-up `controller_batch_001_diversity_topup` used prior-summary duplicate seeding and added 13/20 unique controller-static pass children, bringing the aggregate unique controller-static population to 48. The top-up met the aggregate controller population gate and reduced duplicate concentration, but exposed localized signal/portfolio repair lessons and a MAP-intent accounting bug now patched locally.

`remote_sample_eval_controller_batch_001` evaluated the seed and five curated children under the old split/window. It found no promote-ready child. `attempt_000` was a sparse 3-portfolio-day artifact; `attempt_004`, `attempt_010`, and `attempt_011` were effectively metric-identical to the seed; `attempt_017` was the only broad-coverage child with better Sharpe, but it failed the missing-held-weight sample tolerance and had mixed old train/validation behavior.

This is now a partial data-backed evolution probe, not a completed AlphaEvolve improvement round. The attempt017 repair run confirmed that Qwen/controller mechanics are healthy but also showed off-target children, gross-exposure dampeners, and exact smoke no-ops. The follow-up hardening smoke confirmed the new behavior-delta gate and parent-offspring accounting, then sample-evaluated one nontrivial signal child. That child underperformed attempt017 and did not fix missing-held-weight risk.

The focused attempt017 round generated one target-matched child worth sample evaluation, `PROG-20260511-A017-FOCUS-0000`. Remote review rejected promotion: the child improved missing-held-weight behavior, but failed parent-relative performance and turnover-aware criteria badly. This is negative sample-eval evidence against treating generic signal dampening as an attempt017 improvement.

The local search-control patch was tested in `controller_attempt017_search_control_rerun_20260511`. The controller path is healthy, but the batch did not produce a sample-eval candidate. Four children passed controller-static gates; two were off-target, and the two target-matched passes did not change final portfolio weights. The only material portfolio-delta signal child was another generic magnitude dampener, which remains negative evidence for the attempt017 branch.

The better next research move is documented in [attempt017_mechanism_design_20260513.md](attempt017_mechanism_design_20260513.md) and wired into the controller vocabulary. The new target families are daily-stock-only mechanisms with plausible final-weight effects: liquidity-weighted side weights, signal-persistence trade gates, industry-neutral ranking, liquidity-adjusted reversal confidence, and liquidity-scaled risk caps. Controller summaries now also report deterministic sample-eval eligibility so off-target and no-final-weight-delta children are not accidentally treated as evaluation candidates.

The first mechanism batch, reviewed in [controller_attempt017_mechanism_batch_review_20260514.md](controller_attempt017_mechanism_batch_review_20260514.md), produced exactly one sample-eval-eligible child, `PROG-20260513-A017-MECH-0007`, and the remote operator evaluated only that child. The controller selection rule worked, but the child was not promotable: it was worse than attempt017 on Sharpe, annualized return, turnover-aware score, drawdown, and missing-held exposure. The batch also exposed a controller prompt/smoke problem: portfolio, ranking, and risk mechanism patches often tried to read daily-stock fields from local frames that do not carry those columns.

The local repair is now implemented in [controller_prompt_smoke_repair_20260514.md](controller_prompt_smoke_repair_20260514.md). Prompt generation and repair now include surface-local data-access contracts; the smoke panel has multiple industries, exchanges, liquidity levels, and market-cap levels; reasoning memory and the skill library carry the field-access repair rule; and remote Git hygiene is documented in [remote_csv_execution_policy.md](remote_csv_execution_policy.md) plus [agent/operations.md](../../../agent/operations.md).

The mechanism rerun, reviewed in [controller_attempt017_mechanism_rerun_review_20260514.md](controller_attempt017_mechanism_rerun_review_20260514.md), produced one sample-eval-eligible child, `PROG-20260514-A017-MECHFIX-0009`. The child was an industry-neutral ranking mechanism that correctly used `panel.loc[group.index, CONTRACT.industry_primary]` and materially changed the book. It improved turnover, drawdown, breadth, and missing-held behavior versus attempt017, but weakened parent-relative annualized return and Sharpe and had a negative train Sharpe. It is useful evidence, not a promotion.

The 27B-card batch follow-up is reviewed in [remote_sample_eval_controller_attempt017_27b_card_batch_review_20260515.md](remote_sample_eval_controller_attempt017_27b_card_batch_review_20260515.md). Its sample-evaluated child repeated the prior attempt009 industry-neutral ranking mechanism closely enough that it should be treated as occupied-cell replay, not new alpha evidence. The follow-up hardening is documented in [sample_eval_novelty_hardening_20260515.md](sample_eval_novelty_hardening_20260515.md): controller sample-eval eligibility now requires occupied-MAP-cell elite comparison, remote sample eval can compare against prior sibling summaries, mechanism cards must use exact surfaces/intents/data-field handles, and reasoning memory now carries the negative repeat lesson.

The CodeEvolve, ShinkaEvolve, and ThetaEvolve readthrough confirms that duplicate and lazy-output issues should be treated as population/database policy problems, not only prompt wording problems. `controller_population_policy_v2` is the active controller policy: it tracks parent offspring counts, surface/intent saturation, prompt-card duplicate rates, prompt-card fitness, deterministic lazy penalties for invalid/duplicate/off-target outputs, and edit-signature near duplicates before market evaluation.

The controller-only novelty smoke, reviewed in [controller_attempt017_novelty_smoke_review_20260517.md](controller_attempt017_novelty_smoke_review_20260517.md), passed as an infrastructure proof but produced zero sample-eval candidates. It confirmed clean Git reproducibility, eligibility-v2 fields, no ranking attempts, no automatic sample eval, no empty Qwen outputs, no-final-weight no-op rejection, and occupied-MAP-cell elite comparison. It also exposed a target-routing gap: the remote command forced surfaces only, so the sampler selected `portfolio/signal_weighted_sides`, `risk/max_weight_tightening`, and `risk/cap_shape_change` instead of the preferred underfilled cells.

The local forced-cell patch is now implemented in [forced_target_cell_schedule_patch_20260517.md](forced_target_cell_schedule_patch_20260517.md). `run_child_batch.py` accepts `--target-cell-schedule`, validates exact `surface/intent` pairs before generation, keeps duplicate retry inside the forced cell, and records target-cell schedule fields plus duplicate-retry terminal diagnostics in artifacts. Local unit tests and a mock runner smoke passed.

The forced-cell smoke is reviewed in [controller_attempt017_forced_cell_smoke_review_20260517.md](controller_attempt017_forced_cell_smoke_review_20260517.md). It proved exact target-cell routing and clean Git reproducibility, but produced zero sample-eval candidates. The two controller passes were `signal/liquidity_adjusted_reversal` children that changed raw signal only; ranked signals and final weights were unchanged, and the occupied MAP-cell elite was not beaten. The local hardening in [controller_execution_effect_hardening_20260517.md](controller_execution_effect_hardening_20260517.md) adds an execution-effect gate, so signal/ranking edits must affect ranked signals or final weights and portfolio/risk edits must affect final weights or exposure shape.

The execution-effect smoke is reviewed in [controller_attempt017_execution_effect_smoke_review_20260518.md](controller_attempt017_execution_effect_smoke_review_20260518.md). It produced two sample-eval-eligible controller passes, but both are caveated: one is mostly liquidity-conditioned gross/exposure dampening and one is a confounded signal patch that removed multiple parent mechanisms while changing liquidity weighting. The decision is to pause child generation and build a full `daily_stock` empirical map before another attempt017 round.

The full `daily_stock` EDA is reviewed in [daily_stock_eda_full_review_20260518.md](daily_stock_eda_full_review_20260518.md), with a meeting-style notebook under [notebooks/daily_stock_eda_full_20260518_report_executed.ipynb](notebooks/daily_stock_eda_full_20260518_report_executed.ipynb). The full file has 49.65M rows, 25,139 unique PERMNOs, and 28.30M fixed-contract eligible rows. The 2018-2020 rolling top-500 deep window is much cleaner than the broad eligible universe: median 500 tradable names per day, median 53 SIC2 groups, median 15 SIC2 groups with at least 10 names, and median month-to-month membership Jaccard about 0.957. The accepted prompt lesson is to use robust date-level ranks/log/winsorized transforms and group-size-aware industry logic rather than raw-scale liquidity or market-cap dampening.

The forward-coverage diagnostic is reviewed in [daily_stock_forward_coverage_review_20260519.md](daily_stock_forward_coverage_review_20260519.md), with an executed report notebook under [notebooks/daily_stock_forward_coverage_20260518_report_executed.ipynb](notebooks/daily_stock_forward_coverage_20260518_report_executed.ipynb). Whole-timeline rolling top-500 coverage is excellent: median daily observed selected names are 500 and the minimum daily coverage is 493/500. The important finding is not broad raw missingness. In the historical 2018-2020 smoke window, forward availability is 99.755% raw and about 99.888% after excluding the final visible date; 392 of 424 non-final unavailable rows occur at month-end. Names that do not continue into next-month membership account for 419 non-final unavailable rows. This points to an evaluator forward-return construction issue: next-day returns are being built after monthly-universe filtering, so a date-\(t\) holding that exits next month's top-500 can look missing even when raw eligible data may have its next-day return.

The active evaluation split is now fixed IS/OS rather than chronological 70/15/15. EDA and coverage work should use the full available 2000-2025 timeline, but AlphaEvolve performance feedback should use the 2011-2025 development window: in-sample is 2011-01-01 through 2022-12-31, and out-of-sample starts on 2023-01-01 and runs through the latest available 2025 date. The 2018-2020 window is retained only as a historical smoke/debug window.

The evaluator forward-return source repair is implemented in [evaluator_forward_return_contract_repair_20260519.md](evaluator_forward_return_contract_repair_20260519.md). Signal-date weights still use rolling top-500 membership at date t, but one-day-forward returns are now sourced from the duplicate-resolved statically eligible raw panel. This should remove the month-end universe-exit missing-held artifact before any more attempt017-family market evidence is interpreted.

The repaired IS/OS rerun is reviewed in [remote_sample_eval_is_os_forward_repair_review_20260520.md](remote_sample_eval_is_os_forward_repair_review_20260520.md). All six runs were clean and reproducible from GitHub at commit `82a524fd6b0903588367b6d3b1b656adb4cbadc8`, with `HEAD == origin/main`, `git_dirty == false`, the repaired forward-return source, and the fixed 2011-2025 IS/OS split. Attempt017 is now the active parent lead: `PROG-20260430-CHILD-0017-ISOSREPAIR` passed sample hard gates with IS Sharpe 0.1589, OS Sharpe 0.5061, search-sample Sharpe 0.2244, turnover 0.5602, turnover-aware score 0.0322, max missing-held weight 0.0104, and max weight 0.0104. This is not promotion. It means missing-held repair is no longer the main objective; the next objective is cost robustness and IS stability while preserving the attempt017 OS lead.

Before running the next attempt017 controller batch, Phase 4 will run deterministic parent discovery through the seed zoo implemented in [seed_zoo_parent_discovery_20260521.md](seed_zoo_parent_discovery_20260521.md). This creates 10 concrete daily-stock parent programs and evaluates them through the repaired IS/OS sample evaluator. The goal is to avoid overfitting the search process to one modest local parent and to identify whether a simpler, neutralized, liquidity-aware, or blended deterministic parent should become the next AlphaEvolve branch root.

The parent-zoo cost-aware controller run is reviewed in [parent_zoo_cost_aware_review_20260522.md](parent_zoo_cost_aware_review_20260522.md). It produced controller-safe children from attempt017, five-day reversal, and volatility-normalized reversal roots, but no market evidence yet. The seed roots generated more execution-effective candidates than the already-optimized attempt017 branch. The next stage is a narrow evaluator-only run for three high-information children: `PROG-20260522-PZOO-00-0005`, `PROG-20260522-PZOO-01-0002`, and `PROG-20260522-PZOO-01-0004`. Do not sample-evaluate the thin-book no-trade-band children, the semantically broken persistence child, or small liquidity-cap variants before stronger evidence appears.

The curated parent-zoo sample eval is reviewed in [remote_sample_eval_pzoo_0_review_20260525.md](remote_sample_eval_pzoo_0_review_20260525.md). All three runs were mechanically clean and `sample_pass`, but no child is promotable. `PROG-20260522-PZOO-00-0005` improved attempt017's turnover-aware score by cutting turnover, but its OS Sharpe was negative. `PROG-20260522-PZOO-01-0002` and `PROG-20260522-PZOO-01-0004` showed positive gross signal but high turnover and negative net turnover-aware scores at 2.5 bps. The conclusion is that the bottleneck is now semantic alpha construction and cost conversion, not controller infrastructure.

AlphaAgentEvo has now been ingested as a directly relevant source. The durable source note is [AlphaAgentEvo - Evolution-Oriented Alpha Mining via Self-Evolving Agentic Reinforcement Learning](../../../wiki/sources/papers/AlphaAgentEvo%20-%20Evolution-Oriented%20Alpha%20Mining%20via%20Self-Evolving%20Agentic%20Reinforcement%20Learning.md), and the Phase 4 transfer note is [alphaagentevo_transfer_20260525.md](alphaagentevo_transfer_20260525.md). The accepted design implication is to use a daily-stock expression-evolution layer with multi-turn trajectory scoring before another broad Python-patch controller batch. The first local slice is implemented in `research/alphaevolve_lite/expression_evolution.py`: safe expression grammar, admitted daily-stock fields/operators, constrained dollar-neutral portfolio bridge, 24 starter seeds, expression similarity, and trajectory scoring with valid ratio, pass@T, consistency, exploration, performance, and streak diagnostics. `scripts/run_expression_seed_zoo.py` now provides a deterministic remote evaluation path for those expression seeds under the repaired IS/OS evaluator contract.

The expression seed-zoo baseline is reviewed in [expression_seed_zoo_review_20260525.md](expression_seed_zoo_review_20260525.md). The evaluator worked cleanly at commit `981b1d31e2104820dc8c2fa381b4a03dd21a7da4`: 24 seeds evaluated, 23 expression sample passes, 1 sample review, no errors. Research-wise, no seed is promotable. Only `expr_smoothed_rev` has positive full-window turnover-aware score after 2.5 bps, and it has negative OS behavior. `expr_size_ind_rev` is the only seed with positive IS and OS Sharpe, but it remains negative after cost. OS-positive momentum expressions are likely regime diagnostics because IS is strongly negative. The next objective is expression-level cost conversion and regime stability, not seed promotion. RL fine-tuning remains deferred until we have enough clean trajectories.

The first Qwen-backed expression episode runner is now implemented in `research/alphaevolve_lite/scripts/run_expression_episode.py`. It asks remote Qwen for JSON-only expression proposals, parses and records malformed outputs, rejects exact duplicate expressions, records structural similarity, evaluates valid children through the same rolling top-500 / forward-return / IS-OS / cost / coverage contracts as the seed-zoo run, and writes trajectory summaries per parent. Local verification uses a mock JSON response so the Windows machine does not run Qwen.

Current evolution status:

```yaml
child_generation_done: controller_population_ready
controller_static_small_batch_passed: true
controller_static_50_batch_passed: true_after_diversity_topup
child_market_evaluation_done: parent_zoo_curated_sample_eval_reviewed
iterative_evolution_round_done: false
expression_evolution_v1_local_scaffold: implemented
expression_seed_zoo_remote_eval_reviewed: true
remote_expression_episode_runner_v1: implemented_locally
remote_expression_episode_run_v1_reviewed: true
expression_bridge_followup_reviewed: true
expression_bridge_robustness_reviewed: true
expression_episode_v2_research_memory: implemented_locally
expression_episode_v2_remote_instruction: ready_for_remote
next_stage: remote_expression_episode_v2
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
| `controller_batch_001_diversity_topup` | 13/20 pass with prior 35 pass children seeded, aggregate unique controller-static children 48, duplicate-style rejects reduced to 3, no empty/reasoning-only output, DB insert 1.0. Failures concentrated in `signal/time_smoothing` portfolio semantic rejects and one pandas boolean-index vector-smoke reject. | Controller population gate is satisfied. Patch intent classification/accounting, then run curated `remote_sample_eval` on a small diverse subset rather than evaluating all children. |
| `remote_sample_eval_controller_batch_001` | Seed plus five curated children were sample-evaluated. `attempt_000` had huge Sharpe but only 3 portfolio days; `attempt_004`, `attempt_010`, and `attempt_011` were metric-equivalent to the seed; `attempt_017` improved broad-sample Sharpe and turnover but failed missing-held-weight tolerance. | Add active portfolio-day coverage and optional reference-equivalence gates. Use `attempt_017` only as a structural lead, not as a promoted child. |
| `controller_batch_001_attempt017_repair` | 8/12 controller-static pass, no parse/apply/compile/vector/semantic failures, no duplicate child rejects, but target-intent match was low and several pass children were gross-only or behaviorally weak. Prior missing `parent_id` values were incorrectly attributed to attempt017 during policy seeding. | Harden population accounting, reject exact smoke no-ops, add behavior-delta MAP buckets, expose sample-eval exposure diagnostics, and reroute low-fitness prompt cards before another remote run. |
| `controller_evaluator_hardening_smoke_20260510` | 2/6 controller pass, 4/6 exact smoke no-op rejects, no duplicate rejects, parent-offspring accounting correct, MAP delta buckets reported. The only nontrivial child, attempt004, sample-reviewed worse than attempt017 and still failed max missing-held-weight at 0.12. | The no-op gate is useful. Do not promote or further evaluate this batch. Fix child sample-eval lineage and signal intent classification before the next remote run. |
| `controller_attempt017_focused_round_20260511` | 3/12 controller pass, 7 behavioral no-op rejects, one exact-search failure, one near-duplicate reject, no empty Qwen output, DB insert 1.0. The only target-matched child, `PROG-20260511-A017-FOCUS-0000`, improved missing-held weight but failed parent-relative performance and turnover-aware criteria badly in sample eval. | Missing-held-weight improvement alone is not alpha evidence. Treat generic signal dampening as controller-safe but market-unproven/negative for the attempt017 branch. Patch prompt/memory to require preservation of parent-relative return and turnover-aware score before another focused run. |
| `attempt017_search_control_patch_20260511` | Local prompt, reasoning-memory, and skill-library defaults now carry the negative attempt017 repair lesson. Retrieval checks confirm signal prompts retrieve the generic-dampening avoid rule and portfolio/risk prompts retrieve final-weight no-op guardrails. | The next remote action can be a small focused controller-only rerun after GitHub sync. Sample-evaluate at most one target-matched, behaviorally nontrivial child with plausible parent-relative economics. |
| `controller_attempt017_search_control_rerun_20260511` | 4/12 controller pass, no empty Qwen output, no duplicate child rejects, DB insert 1.0, but 6 behavioral no-op rejects, 1 exact-search failure, 1 near-duplicate patch, and 2 target-intent mismatch passes. The target-matched passes had no final-weight delta. | Do not sample-evaluate this batch. Prompt memory alone is not enough; add deterministic sample-eval eligibility gates for target-intent match and final-weight effect. Treat known-bad focused repair families as prompt/review warnings, not hard sample-eval filters for the next novelty smoke. |
| `attempt017_mechanism_design_20260513` | Attempt017 evidence was translated into concrete daily-stock-only mechanisms: portfolio liquidity weighting, signal persistence gating, industry-neutral ranking, liquidity-adjusted reversal confidence, and liquidity-scaled caps. The target vocabulary, intent classifier, prompt guidance, and sample-eval eligibility summary are patched locally. | Stop asking Qwen for generic dampeners. Give it mechanism targets that use ex-ante price, volume, dollar-volume, market-cap, status, exchange, or industry fields and should affect final weights. |
| `controller_attempt017_mechanism_batch_20260513` plus attempt007 sample eval | 5/12 controller pass, target-intent match 1.0, no duplicate pressure, but vector smoke and portfolio semantic pass rates were only 0.5. The only sample-eval candidate, `PROG-20260513-A017-MECH-0007`, was broad and non-equivalent but worse than attempt017 on parent-relative Sharpe, return, turnover-aware score, drawdown, and missing-held exposure. | The controller eligibility rule worked, but the mechanism prompt did not specify local data-scope contracts for each EVOLVE block. Repair prompt/smoke fixtures before another remote generation batch. |
| `controller_prompt_smoke_repair_20260514` | Local prompt/smoke repair implemented surface-local data-access guidance, panel.loc repair prompts, multi-industry and wider-liquidity smoke fixtures, active reasoning memory, high-confidence skill rule, and remote Git hygiene policy. Local checks passed. | After GitHub sync, run one small controller-only rerun focused on direct portfolio/risk/ranking mechanisms. Sample-evaluate at most one eligible direct-mechanism child. |
| `controller_attempt017_mechanism_rerun_20260514` plus attempt009 sample eval | 2/12 controller pass, 7 behavioral no-op rejects, 1 duplicate child reject, 2 vector-smoke rejects, and exactly one sample-eval candidate. Attempt009 was a target-matched industry-neutral ranking child with material final-weight delta. Sample eval narrowly failed missing-held tolerance at 0.0512, improved turnover/drawdown/breadth versus attempt017, but reduced annualized return and Sharpe and showed negative train Sharpe. | Do not promote. Use 27B as a medium reviewer to propose mechanism cards that preserve attempt009 implementation-shape gains without giving up attempt017 parent-relative alpha metrics. Add program snapshots and `HEAD == origin/main` reproducibility capture. |
| `controller_attempt017_novelty_smoke_20260516` | 1/6 controller pass, 4 behavioral no-op rejects, 1 duplicate child reject, 0 sample-eval candidates, all core mechanics pass, clean `HEAD == origin/main`, no ranking attempts, no automatic sample eval. The only pass, `PROG-20260516-A017-NOVELTY-0004`, was `signal/liquidity_adjusted_reversal` and was rejected for sample eval because it landed in an occupied MAP cell without beating the elite. | Eligibility-v2 and Git reproducibility wiring are healthy. Do not sample-evaluate this run. Patch the runner so remote instructions can force exact target cells instead of only surface schedules. |
| `forced_target_cell_schedule_patch_20260517` | Local runner patch added `--target-cell-schedule`, exact `surface/intent` validation, forced-cell duplicate retry, summary schedule fields, and duplicate-retry terminal diagnostics. Unit tests and a local mock runner smoke passed. | The next remote run can be a controller-only forced-cell smoke. Do not use 27B or sample evaluation until the forced-cell controller artifact is reviewed locally. |
| `controller_attempt017_forced_cell_smoke_20260517` | 2/6 controller pass, exact forced target-cell routing, clean `HEAD == origin/main`, no ranking attempts, no sample eval, but zero sample-eval candidates. The two passes changed raw signal only; ranked signal and final weights were unchanged. Portfolio/risk failures exposed persistence local-data misuse, one-sided short-book risk, and max-weight breaches. | Forced-cell routing is solved. Add a controller execution-effect contract and do not treat raw-signal-only passes as success memory. |
| `controller_execution_effect_hardening_20260517` | Local patch added `controller_execution_effect_v1`, `execution_effect_failed`, repairable execution-effect failures, summary `execution_effect_pass_rate`, prompt repairs for failed cells, and skill/reasoning-memory filtering so execution-neutral passes are guardrails, not success strategies. Tests and artifact-derived replay passed. | After GitHub sync, run one controller-only execution-effect forced-cell smoke. Still no sample eval or 27B until a child is target-matched, novel, and final-book-effective. |
| `remote_sample_eval_is_os_forward_repair_20260519` | Seed, attempt017, and four attempt017-family children were rerun under the repaired forward-return source and fixed 2011-2025 IS/OS split. All runs were clean from `origin/main`. Attempt017 passed sample gates and remains the active parent lead; missing-held weight fell to about 0.0104. | Do not promote. Stop optimizing missing-held weight for this branch. Run a targeted controller-only cost-robustness batch from attempt017 and sample-evaluate only after local review of target match, execution effect, novelty, broad book, and sibling equivalence. |
| `seed_zoo_parent_discovery_20260521` | Local implementation added 10 deterministic daily-stock parent candidates, a renderer that writes concrete EVOLVE-block strategy programs, a remote runner that evaluates each through repaired `remote_sample_eval.py`, seed-candidate recording via `--program-kind seed`, aggregate ranking artifacts, and synthetic-data tests. | Run seed-zoo sample evaluation before more LLM child generation. Use the result to choose better parent branches rather than continuing to over-repair attempt017 by default. |
| `seed_zoo_is_os_20260521` | All 10 deterministic seed-zoo programs completed `remote_sample_eval` with clean `HEAD == origin/main` and high portfolio coverage. None beat repaired attempt017 at 2.5 bps cost. The best seed was `five_day_excess_reversal` with search Sharpe `0.0463` and turnover-aware score `-0.2511`; most seeds had positive zero-cost gross Sharpe but lost the edge after costs. `kalman_ewm_reversal` had high OS Sharpe but negative IS Sharpe and high turnover. | Do not promote any seed. Use the result as parent-zoo evidence: keep attempt017 as incumbent benchmark/root, add five-day reversal and volatility-normalized five-day reversal as active deterministic roots, and run a small cost-aware controller batch focused on preserving reversal signal while reducing turnover. |
| `parent_zoo_cost_aware_patch_20260522` | Local patch added `signal/regime_aware_reversal`, parent-root metadata in controller summaries, hand-authored parent-zoo mechanism cards, and `run_parent_zoo_batch.py` to render seed roots and run one controller batch per root. The 27B/35B role is mechanism-card review only; Qwen9B remains the strict SEARCH/REPLACE patch implementer. | Push before the next remote run. Remote should run controller-only parent-zoo search and return artifacts before any sample evaluation. |

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
- MAP descriptor classification must use changed replacement lines, not the whole replacement block. Unchanged context can otherwise mislabel EWM smoothing as `history_confidence_weighting`, risk dampening as `side_renormalization`, or scale-shrinkage as `ranking_other`.
- A controller-safe off-target patch can enter the database under its actual behavior descriptor, but it should not count as a full prompt-card success for the sampled target intent.
- For portfolio sparsity/no-trade-band patches, convert boolean masks to aligned index labels before assigning into `weights`; a boolean Series from a filtered frame can trigger an unalignable-index vector-smoke failure.
- For `signal/time_smoothing`, require causal rolling, EWM, or lagged smoothing. Do not substitute nonlinear magnitude dampeners; they can reorder ranked signals enough to violate portfolio sign semantics.
- A sparse child can produce extreme Sharpe by trading only a few dates. `remote_sample_eval` should require broad active portfolio-day coverage for `sample_pass`.
- Code-different children can be metric-equivalent after ranking, selection, and risk controls. When a seed or parent reference summary is available, sample evaluation should flag those as review-only.
- Controller-static children can also be exact smoke no-ops before data-backed evaluation. Reject exact parent-child no-ops and treat them as lazy search evidence; keep weaker behavior deltas as diagnostics rather than over-filtering.
- Gross-exposure dampening can improve cost and missing-held-weight metrics without improving alpha. Sample evaluation must report gross/net/long/short exposure so parent-relative gains are interpretable.
- Child sample evaluation must use explicit child `program_id` and parent lineage. Refuse child sample eval under the seed default id, otherwise database records can overwrite or misrepresent lineage.
- Missing-held-weight repairs must not use evaluator-only forward-return availability fields such as `fwd_ret`, `fwd_date`, `fwd_vwretd`, `next_market_date`, or `one_day_forward`.
- Improving missing-held weight alone is not promotion evidence. `PROG-20260511-A017-FOCUS-0000` improved that diagnostic but failed parent-relative performance and turnover-aware criteria badly.
- Generic signal dampening (`bounded_tanh_dampening`, `clipped_magnitude_dampening`) can create controller-visible portfolio deltas without improving alpha. Treat it as market-unproven and now negative evidence for the attempt017 branch unless it also improves parent-relative economics.
- Avoid skills are currently prompt guidance, not hard filters. The search-control rerun still generated clipped magnitude dampening despite retrieving the avoid skill, so focused repair mode should surface that as review context rather than silently treating the family as alpha evidence.
- Target-matched controller passes can still be useless if final weights are unchanged. For sample-eval eligibility, require target-intent match plus final-weight delta or an explicit pre-declared reason why raw-signal/ranking changes should matter in full data.
- Mechanism prompts must name the surface-local data-access contract. Portfolio and risk blocks may have `panel` available but local `data`, `group`, or `valid` frames may not include `CONTRACT.dollar_volume`, `CONTRACT.volume`, `CONTRACT.market_cap`, or industry fields. Use `panel.loc[index, CONTRACT.field]` with aligned indices when the local frame lacks the field.
- Controller smoke fixtures must exercise the mechanism being targeted. A one-industry smoke panel cannot prove that industry neutralization affects final weights, and a smoke panel that only checks generic pass/fail can miss data-scope prompt defects.
- Controller-relative success memory should not be promoted to active strategy skill until sample-eval evidence is checked. `PROG-20260513-A017-MECH-0007` was the best controller sibling but failed parent-relative market evaluation.
- `PROG-20260514-A017-MECHFIX-0009` shows the opposite tradeoff: a direct industry-neutral mechanism can improve implementation shape, turnover, drawdown, breadth, and missing-held weight while weakening parent-relative return and Sharpe. Do not confuse cleaner portfolio construction with stronger alpha.
- A clean remote worktree is insufficient if `HEAD` is an unpushed commit. Remote controller and sample-eval artifacts must record `git_origin_main_commit`, `git_head_matches_origin_main`, and code snapshots/hashes.
- 27B should be used as a mechanism reviewer before direct generation. Prior evidence showed 27B can be useful for medium-depth review but is not the default strict patch generator.
- Surface schedules are not enough when the research instruction names exact underfilled mechanism cells. `controller_attempt017_novelty_smoke_20260516` asked for preferred cells but the runner only forced surfaces, so it sampled absorbed portfolio/risk cells and produced no sample-eval candidates.
- Portfolio signal-weighted-side edits can be no-ops after downstream max-weight clipping and side renormalization. Risk cap-shape edits can also be no-ops if they re-clip at the same cap boundary after normalization. Treat these as search-control routing failures unless a prompt declares how final weights will actually change.
- Controller-safe is not controller-useful. A signal or ranking edit must change ranked signal or final weights; a portfolio or risk edit must change final weights or exposure shape after risk controls. Raw-signal-only liquidity scaling is `execution_effect_failed`, not success evidence.
- For `portfolio/persistence_trade_gate`, `signal` is local data, not a panel field. Use `data.groupby(CONTRACT.security_id)["signal"].shift(1)` or `data.loc[valid.index, "prior_signal"]`; do not use `panel.loc[..., "signal"]`.
- For `signal/liquidity_adjusted_reversal`, avoid inverse raw dollar volume clipped into a uniform scale. Use bounded relative liquidity, log liquidity, market-cap percentile, or rolling confidence logic that can affect ranks or selected weights.
- For `risk/liquidity_scaled_cap`, cap values must stay no larger than `max_weight`; clip, side-renormalize, and clip again to preserve max-weight and balanced long/short exposure.
- `sample_pass` is not promotion. The repaired attempt017 parent lead passed hard sample gates, but remains a development candidate whose main weakness is cost sensitivity and IS robustness.
- The seed zoo confirms that simple daily-stock reversal has gross structure before costs, but daily churn consumes it. Future mutations should target holding stability, no-trade bands, causal smoothing, regime-aware state conditioning, and liquidity-aware execution rather than generic signal dampening or entirely new reversal definitions.
- `five_day_excess_reversal` is the best deterministic seed root under the 2.5 bps search score, but it is not promoted because it trails attempt017 and has weak OS behavior. Treat it as a root for controlled evolution only.
- `kalman_ewm_reversal` is not a lead despite high OS Sharpe; its negative IS Sharpe and high turnover make it a diagnostic/regime branch, not an optimization target.
- `PROG-20260514-A017-MECHFIX-0009` and `PROG-20260514-A017-27BCARD-0011` produced identical repaired-sample metrics despite different program hashes. Future sample evaluations must pass all relevant prior sibling summaries through `--prior-sample-summary`, not only the seed or current parent.
- Missing-held repair is retired as the main attempt017 objective after the forward-return source fix. The next child generation target is turnover/cost robustness without sparse few-day books or one-sided exposure.

## Reasoning Memory Layer

Phase 4 now treats these lessons as a formal ReasoningBank-style layer rather than only prose inside this current-state file.

[reasoning_memory_layer_design.md](reasoning_memory_layer_design.md) defines the new memory item schema, extraction workflow, prompt-injection rule, and implementation milestones. The design follows [[ReasoningBank - Scaling Agent Self-Evolving with Reasoning Memory]] but adapts it for quant research by using deterministic controller/evaluator outcomes as the source of success/failure labels.

The memory bank is distinct from the program database:

- program database: exhaustive evidence for every generated child;
- reasoning memory bank: compact, evidence-linked lessons retrieved into future prompts.

The explicit skill library is a third layer. It is narrower than reasoning memory and stores operational pattern -> strategy rules with `high`, `medium`, `low`, or `avoid` confidence. New `skill_update.json` entries from a small controller batch are candidate-level only until deterministic evidence supports promotion.

## Current Next Step

The bridge robustness run is reviewed in [expression_bridge_robustness_review_20260526.md](expression_bridge_robustness_review_20260526.md). The run was clean at commit `55d25a97178ee7740d593dc2ec0f55b12a8408fa`: no Qwen, no dirty Git state, 44/44 parent/child bridge records reached `expression_sample_pass`, and no final-test evidence was used.

The important result is negative for parent conversion. The liquidity-gated smoothed-reversal child remains bad under the primary daily bridge, and no bridge family satisfies the robustness rule. `rebalance_5` has only one follow-up pass across five phases, with child positive search/IS/OS counts of 3/5 each. `rebalance_10` has one strong phase, `rebalance_10_offset_5`, but only one follow-up pass across ten phases. Signal-decay variants are OS-positive but IS-negative. At 5 bps, the apparent gains mostly disappear.

This closes the bridge detour for this child. The result is bridge-policy failure memory, not promotion evidence.

The local prep for this next run is now implemented. `run_expression_episode.py` accepts `--research-memory-file`, writes `expression_prompt_memory.json`, and injects reviewed memory into a dedicated prompt section separated from population context and prior episode feedback.

```yaml
next_task:
  type: remote_expression_episode_v2
  remote_instruction: expression_episode_v2_remote_instructions_20260531.md
  research_memory: expression_episode_v2_memory_20260531.md
  basis:
    - expression_episode_20260526
    - expression_bridge_followup_20260526
    - expression_bridge_robustness_20260526
  reason:
    - bridge robustness rejected the liquidity-gated child as phase-sensitive
    - no bridge-aware parent conversion is justified
    - expression infrastructure, prior-population ledger, bridge diagnostics, and hard gates are now working
  local_work_completed:
    - bridge-robustness failure memory is a first-class prompt input
    - remote instruction requires the prior expression_population_ledger from expression_episode_20260526
    - remote instruction keeps multi-root population search rather than focusing on the failed bridge child
    - remote instruction keeps primary daily bridge improvement as the first objective; bridge variants remain diagnostics
  recommended_roots:
    - expr_smoothed_rev
    - expr_mom_060_ind
    - expr_size_ind_rev with mechanism-specific pressure only
  avoid_memory:
    - do not repeat rank(-rolling_mean(rolling_sum(excess_ret, 5), 3)) * rank(log1p_abs(dollar_volume)) as a parent
    - do not select a child because one rebalance phase is strong
    - do not treat OS-only bridge gains as alpha evidence
  forbidden:
    - no promotion
    - no full validation
    - no bridge-aware conversion of expr_smoothed_rev_liq_bridge_20260526
  test_set_used: false
```

Previous expression-episode finding retained for context:

```yaml
prior_expression_episode:
  basis: expression_episode_20260526
  candidate_expression_id: expr_smoothed_rev_000_82524e85_ep_t02_c01
  candidate_bridges:
    - rebalance_5
    - signal_decay_5
  bridge_followup_completed: true
  bridge_robustness_completed: true
  bridge_robustness_decision: rejected_phase_sensitive
```

## Main Links

- Active design: [README.md](README.md), [task_001_search_design.md](task_001_search_design.md), [task_004_seed_strategy_program.md](task_004_seed_strategy_program.md)
- Contracts: [daily_stock_contract_v1.md](daily_stock_contract_v1.md), [prompt_contracts.md](prompt_contracts.md), [evaluator_contract.md](evaluator_contract.md), [program_database_schema.md](program_database_schema.md)
- Memory and skills: [reasoning_memory_layer_design.md](reasoning_memory_layer_design.md), [dr_rtl_method_transfer_20260504.md](dr_rtl_method_transfer_20260504.md), [diagnostic_analyzer_and_skill_library_20260504.md](diagnostic_analyzer_and_skill_library_20260504.md), [alphaevolve_extension_methods_20260509.md](alphaevolve_extension_methods_20260509.md), [Reasoning Memory for AlphaEvolve Search](../../../wiki/methods/Reasoning%20Memory%20for%20AlphaEvolve%20Search.md), [Group-Relative Skill Learning for Alpha Search](../../../wiki/methods/Group-Relative%20Skill%20Learning%20for%20Alpha%20Search.md), [AlphaEvolve Extension Methods for Quant Search](../../../wiki/methods/AlphaEvolve%20Extension%20Methods%20for%20Quant%20Search.md)
- Data and costs: [dataset_context.md](dataset_context.md), [dataset_admission_policy.md](dataset_admission_policy.md), [universe_and_split_policy.md](universe_and_split_policy.md), [is_os_evaluation_policy_20260519.md](is_os_evaluation_policy_20260519.md), [cost_model_policy.md](cost_model_policy.md)
- Remote/runtime: [remote_qwen_vllm_config.md](remote_qwen_vllm_config.md), [remote_csv_execution_policy.md](remote_csv_execution_policy.md), [model_stack_and_vllm_results.md](model_stack_and_vllm_results.md)
- Dated evidence records: [remote_evidence_review_20260430.md](remote_evidence_review_20260430.md), [controller_batch_001_small_review_20260430.md](controller_batch_001_small_review_20260430.md), [controller_batch_001_small_repair_v1_review_20260430.md](controller_batch_001_small_repair_v1_review_20260430.md), [controller_batch_001_small_semantic_v2_review_20260501.md](controller_batch_001_small_semantic_v2_review_20260501.md), [controller_batch_001_small_semantic_v3_review_20260501.md](controller_batch_001_small_semantic_v3_review_20260501.md), [controller_batch_001_small_semantic_v4_review_20260508.md](controller_batch_001_small_semantic_v4_review_20260508.md), [controller_batch_001_review_20260509.md](controller_batch_001_review_20260509.md), [controller_batch_001_diversity_topup_review_20260509.md](controller_batch_001_diversity_topup_review_20260509.md), [remote_sample_eval_controller_batch_001_review_20260509.md](remote_sample_eval_controller_batch_001_review_20260509.md), [controller_batch_001_attempt017_repair_hardening_20260510.md](controller_batch_001_attempt017_repair_hardening_20260510.md), [controller_evaluator_hardening_smoke_review_20260511.md](controller_evaluator_hardening_smoke_review_20260511.md), [remote_sample_eval_controller_attempt017_27b_card_batch_review_20260515.md](remote_sample_eval_controller_attempt017_27b_card_batch_review_20260515.md), [sample_eval_novelty_hardening_20260515.md](sample_eval_novelty_hardening_20260515.md), [controller_attempt017_novelty_smoke_review_20260517.md](controller_attempt017_novelty_smoke_review_20260517.md), [controller_attempt017_forced_cell_smoke_review_20260517.md](controller_attempt017_forced_cell_smoke_review_20260517.md), [controller_execution_effect_hardening_20260517.md](controller_execution_effect_hardening_20260517.md), [remote_sample_eval_is_os_forward_repair_review_20260520.md](remote_sample_eval_is_os_forward_repair_review_20260520.md), [seed_zoo_is_os_review_20260522.md](seed_zoo_is_os_review_20260522.md)
- Remote handoff: [expression_bridge_followup_remote_instructions_20260526.md](expression_bridge_followup_remote_instructions_20260526.md), [expression_episode_remote_instructions_20260526.md](expression_episode_remote_instructions_20260526.md), [daily_stock_forward_coverage_remote_instructions_20260518.md](daily_stock_forward_coverage_remote_instructions_20260518.md), [controller_batch_001_remote_instructions_20260508.md](controller_batch_001_remote_instructions_20260508.md), [controller_batch_001_diversity_topup_remote_instructions_20260509.md](controller_batch_001_diversity_topup_remote_instructions_20260509.md), [controller_batch_001_curated_sample_eval_remote_instructions_20260509.md](controller_batch_001_curated_sample_eval_remote_instructions_20260509.md), [controller_batch_001_attempt017_repair_remote_instructions_20260509.md](controller_batch_001_attempt017_repair_remote_instructions_20260509.md), [controller_evaluator_hardening_remote_instructions_20260510.md](controller_evaluator_hardening_remote_instructions_20260510.md), [controller_attempt017_search_control_remote_instructions_20260511.md](controller_attempt017_search_control_remote_instructions_20260511.md), [controller_attempt017_mechanism_batch_remote_instructions_20260513.md](controller_attempt017_mechanism_batch_remote_instructions_20260513.md), [controller_attempt017_novelty_smoke_remote_instructions_20260516.md](controller_attempt017_novelty_smoke_remote_instructions_20260516.md), [controller_attempt017_forced_cell_smoke_remote_instructions_20260517.md](controller_attempt017_forced_cell_smoke_remote_instructions_20260517.md), [controller_attempt017_execution_effect_smoke_remote_instructions_20260517.md](controller_attempt017_execution_effect_smoke_remote_instructions_20260517.md), [controller_attempt017_is_os_cost_robustness_remote_instructions_20260520.md](controller_attempt017_is_os_cost_robustness_remote_instructions_20260520.md), [parent_zoo_cost_aware_remote_instructions_20260522.md](parent_zoo_cost_aware_remote_instructions_20260522.md), [configs/controller_batch_001_remote_qwen.yaml](configs/controller_batch_001_remote_qwen.yaml)
- Durable method memory: [AlphaEvolve Lite Quant Search Workflow](../../../wiki/methods/AlphaEvolve%20Lite%20Quant%20Search%20Workflow.md), [AlphaEvolve Extension Methods for Quant Search](../../../wiki/methods/AlphaEvolve%20Extension%20Methods%20for%20Quant%20Search.md)
