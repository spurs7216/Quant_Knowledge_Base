---
title: Phase 4 Current State
type: project
status: active
updated: 2026-05-14
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

The controller-static population gate is satisfied, and the first curated data-backed sample evaluation has been reviewed. The latest reviewed artifact is:

```text
artifacts/remote_sample_eval_controller_batch_001.zip
```

`controller_batch_001` produced 35/50 unique controller-static pass children but missed the uniqueness gate because 15 attempts were duplicate rejects, mostly in `ranking/direction_flip`. The follow-up `controller_batch_001_diversity_topup` used prior-summary duplicate seeding and added 13/20 unique controller-static pass children, bringing the aggregate unique controller-static population to 48. The top-up met the aggregate controller population gate and reduced duplicate concentration, but exposed localized signal/portfolio repair lessons and a MAP-intent accounting bug now patched locally.

`remote_sample_eval_controller_batch_001` evaluated the seed and five curated children. It found no promote-ready child. `attempt_000` was a sparse 3-portfolio-day artifact; `attempt_004`, `attempt_010`, and `attempt_011` were effectively metric-identical to the seed; `attempt_017` was the only broad-coverage child with better Sharpe, but it failed the missing-held-weight sample tolerance and has mixed train/validation behavior.

This is now a partial data-backed evolution probe, not a completed AlphaEvolve improvement round. The attempt017 repair run confirmed that Qwen/controller mechanics are healthy but also showed off-target children, gross-exposure dampeners, and exact smoke no-ops. The follow-up hardening smoke confirmed the new behavior-delta gate and parent-offspring accounting, then sample-evaluated one nontrivial signal child. That child underperformed attempt017 and did not fix missing-held-weight risk.

The focused attempt017 round generated one target-matched child worth sample evaluation, `PROG-20260511-A017-FOCUS-0000`. Remote review rejected promotion: the child improved missing-held-weight behavior, but failed parent-relative performance and turnover-aware criteria badly. This is negative sample-eval evidence against treating generic signal dampening as an attempt017 improvement.

The local search-control patch was tested in `controller_attempt017_search_control_rerun_20260511`. The controller path is healthy, but the batch did not produce a sample-eval candidate. Four children passed controller-static gates; two were off-target, and the two target-matched passes did not change final portfolio weights. The only material portfolio-delta signal child was another generic magnitude dampener, which remains negative evidence for the attempt017 branch.

The better next research move is documented in [attempt017_mechanism_design_20260513.md](attempt017_mechanism_design_20260513.md) and wired into the controller vocabulary. The new target families are daily-stock-only mechanisms with plausible final-weight effects: liquidity-weighted side weights, signal-persistence trade gates, industry-neutral ranking, liquidity-adjusted reversal confidence, and liquidity-scaled risk caps. Controller summaries now also report deterministic sample-eval eligibility so off-target, no-final-weight-delta, and known-bad dampening children are not accidentally treated as evaluation candidates.

The first mechanism batch, reviewed in [controller_attempt017_mechanism_batch_review_20260514.md](controller_attempt017_mechanism_batch_review_20260514.md), produced exactly one sample-eval-eligible child, `PROG-20260513-A017-MECH-0007`, and the remote operator evaluated only that child. The controller selection rule worked, but the child was not promotable: it was worse than attempt017 on Sharpe, annualized return, turnover-aware score, drawdown, and missing-held exposure. The batch also exposed a controller prompt/smoke problem: portfolio, ranking, and risk mechanism patches often tried to read daily-stock fields from local frames that do not carry those columns.

The local repair is now implemented in [controller_prompt_smoke_repair_20260514.md](controller_prompt_smoke_repair_20260514.md). Prompt generation and repair now include surface-local data-access contracts; the smoke panel has multiple industries, exchanges, liquidity levels, and market-cap levels; reasoning memory and the skill library carry the field-access repair rule; and remote Git hygiene is documented in [remote_csv_execution_policy.md](remote_csv_execution_policy.md) plus [agent/operations.md](../../../agent/operations.md).

The mechanism rerun, reviewed in [controller_attempt017_mechanism_rerun_review_20260514.md](controller_attempt017_mechanism_rerun_review_20260514.md), produced one sample-eval-eligible child, `PROG-20260514-A017-MECHFIX-0009`. The child was an industry-neutral ranking mechanism that correctly used `panel.loc[group.index, CONTRACT.industry_primary]` and materially changed the book. It improved turnover, drawdown, breadth, and missing-held behavior versus attempt017, but weakened parent-relative annualized return and Sharpe and had a negative train Sharpe. It is useful evidence, not a promotion.

The next search move is 27B-assisted but not 27B-direct-code. `Qwen/Qwen3.5-27B-FP8` should synthesize attempt017, attempt007, attempt009, and controller diagnostics into JSON mechanism cards. `Qwen/Qwen3.5-9B` should then generate strict SEARCH/REPLACE children conditioned on those cards. The code now supports this through `build_mechanism_cards.py`, `--mechanism-card-path`, and prompt-side medium-model mechanism-card injection.

The CodeEvolve, ShinkaEvolve, and ThetaEvolve readthrough confirms that duplicate and lazy-output issues should be treated as population/database policy problems, not only prompt wording problems. `controller_population_policy_v2` is the active controller policy: it tracks parent offspring counts, surface/intent saturation, prompt-card duplicate rates, prompt-card fitness, deterministic lazy penalties for invalid/duplicate/off-target outputs, and edit-signature near duplicates before market evaluation.

Current evolution status:

```yaml
child_generation_done: controller_population_ready
controller_static_small_batch_passed: true
controller_static_50_batch_passed: true_after_diversity_topup
child_market_evaluation_done: first_curated_sample_eval_reviewed
iterative_evolution_round_done: false
next_stage: remote_27b_mechanism_cards_then_9b_controller_batch_after_sync
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
| `controller_attempt017_search_control_rerun_20260511` | 4/12 controller pass, no empty Qwen output, no duplicate child rejects, DB insert 1.0, but 6 behavioral no-op rejects, 1 exact-search failure, 1 near-duplicate patch, and 2 target-intent mismatch passes. The target-matched passes had no final-weight delta. | Do not sample-evaluate this batch. Prompt memory alone is not enough; add deterministic sample-eval eligibility gates for target-intent match and final-weight effect, and harden avoid-skill handling for known-bad focused repair families. |
| `attempt017_mechanism_design_20260513` | Attempt017 evidence was translated into concrete daily-stock-only mechanisms: portfolio liquidity weighting, signal persistence gating, industry-neutral ranking, liquidity-adjusted reversal confidence, and liquidity-scaled caps. The target vocabulary, intent classifier, prompt guidance, and sample-eval eligibility summary are patched locally. | Stop asking Qwen for generic dampeners. Give it mechanism targets that use ex-ante price, volume, dollar-volume, market-cap, status, exchange, or industry fields and should affect final weights. |
| `controller_attempt017_mechanism_batch_20260513` plus attempt007 sample eval | 5/12 controller pass, target-intent match 1.0, no duplicate pressure, but vector smoke and portfolio semantic pass rates were only 0.5. The only sample-eval candidate, `PROG-20260513-A017-MECH-0007`, was broad and non-equivalent but worse than attempt017 on parent-relative Sharpe, return, turnover-aware score, drawdown, and missing-held exposure. | The controller eligibility rule worked, but the mechanism prompt did not specify local data-scope contracts for each EVOLVE block. Repair prompt/smoke fixtures before another remote generation batch. |
| `controller_prompt_smoke_repair_20260514` | Local prompt/smoke repair implemented surface-local data-access guidance, panel.loc repair prompts, multi-industry and wider-liquidity smoke fixtures, active reasoning memory, high-confidence skill rule, and remote Git hygiene policy. Local checks passed. | After GitHub sync, run one small controller-only rerun focused on direct portfolio/risk/ranking mechanisms. Sample-evaluate at most one eligible direct-mechanism child. |
| `controller_attempt017_mechanism_rerun_20260514` plus attempt009 sample eval | 2/12 controller pass, 7 behavioral no-op rejects, 1 duplicate child reject, 2 vector-smoke rejects, and exactly one sample-eval candidate. Attempt009 was a target-matched industry-neutral ranking child with material final-weight delta. Sample eval narrowly failed missing-held tolerance at 0.0512, improved turnover/drawdown/breadth versus attempt017, but reduced annualized return and Sharpe and showed negative train Sharpe. | Do not promote. Use 27B as a medium reviewer to propose mechanism cards that preserve attempt009 implementation-shape gains without giving up attempt017 parent-relative alpha metrics. Add program snapshots and `HEAD == origin/main` reproducibility capture. |

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
- Avoid skills are currently prompt guidance, not hard filters. The search-control rerun still generated clipped magnitude dampening despite retrieving the avoid skill, so focused repair mode needs deterministic eligibility or rejection rules for known-bad patch families.
- Target-matched controller passes can still be useless if final weights are unchanged. For sample-eval eligibility, require target-intent match plus final-weight delta or an explicit pre-declared reason why raw-signal/ranking changes should matter in full data.
- Mechanism prompts must name the surface-local data-access contract. Portfolio and risk blocks may have `panel` available but local `data`, `group`, or `valid` frames may not include `CONTRACT.dollar_volume`, `CONTRACT.volume`, `CONTRACT.market_cap`, or industry fields. Use `panel.loc[index, CONTRACT.field]` with aligned indices when the local frame lacks the field.
- Controller smoke fixtures must exercise the mechanism being targeted. A one-industry smoke panel cannot prove that industry neutralization affects final weights, and a smoke panel that only checks generic pass/fail can miss data-scope prompt defects.
- Controller-relative success memory should not be promoted to active strategy skill until sample-eval evidence is checked. `PROG-20260513-A017-MECH-0007` was the best controller sibling but failed parent-relative market evaluation.
- `PROG-20260514-A017-MECHFIX-0009` shows the opposite tradeoff: a direct industry-neutral mechanism can improve implementation shape, turnover, drawdown, breadth, and missing-held weight while weakening parent-relative return and Sharpe. Do not confuse cleaner portfolio construction with stronger alpha.
- A clean remote worktree is insufficient if `HEAD` is an unpushed commit. Remote controller and sample-eval artifacts must record `git_origin_main_commit`, `git_head_matches_origin_main`, and code snapshots/hashes.
- 27B should be used as a mechanism reviewer before direct generation. Prior evidence showed 27B can be useful for medium-depth review but is not the default strict patch generator.

## Reasoning Memory Layer

Phase 4 now treats these lessons as a formal ReasoningBank-style layer rather than only prose inside this current-state file.

[reasoning_memory_layer_design.md](reasoning_memory_layer_design.md) defines the new memory item schema, extraction workflow, prompt-injection rule, and implementation milestones. The design follows [[ReasoningBank - Scaling Agent Self-Evolving with Reasoning Memory]] but adapts it for quant research by using deterministic controller/evaluator outcomes as the source of success/failure labels.

The memory bank is distinct from the program database:

- program database: exhaustive evidence for every generated child;
- reasoning memory bank: compact, evidence-linked lessons retrieved into future prompts.

The explicit skill library is a third layer. It is narrower than reasoning memory and stores operational pattern -> strategy rules with `high`, `medium`, `low`, or `avoid` confidence. New `skill_update.json` entries from a small controller batch are candidate-level only until deterministic evidence supports promotion.

## Current Next Step

The next step is not broad validation and not test evaluation. After GitHub sync, run the 27B-assisted mechanism-card workflow in [controller_attempt017_27b_mechanism_cards_remote_instructions_20260514.md](controller_attempt017_27b_mechanism_cards_remote_instructions_20260514.md).

```yaml
next_remote_run:
  type: qwen27b_mechanism_cards_then_qwen9b_controller_batch
  parent: PROG-20260430-CHILD-0017
  reviewer_model: Qwen3.5-27B-FP8
  generator_model: Qwen3.5-9B
  medium_model_output: JSON mechanism cards only
  preferred_surfaces:
    - ranking/industry_neutral_rank
    - portfolio/liquidity_weighted_sides
    - portfolio/persistence_trade_gate
    - risk/liquidity_scaled_cap
  sample_eval_limit_after_review: 0_or_1
  broad_validation: false
  full_validation: false
starting_evidence:
  - controller_attempt017_mechanism_batch_20260513
  - controller_attempt017_mechanism_rerun_20260514
  - remote_sample_eval_controller_attempt017_mechanism_rerun_20260514_attempt_009
structural_lead: "attempt_017 causal signal smoothing"
main_defect_to_check: "mechanism cards propose ways to keep attempt009 implementation-shape gains without sacrificing attempt017 parent-relative return and Sharpe"
checks_to_inspect:
  - mechanism_cards.json is valid JSON and contains no code patches
  - 9B prompts include mechanism_card_ids
  - controller artifact records git_head_matches_origin_main
  - sample eval artifacts include program_snapshot.py and program_sha256
  - no-final-weight-delta passes stay sample-eval ineligible
test_set_used: false
```

Required evaluator behavior before that run:

```yaml
remote_sample_eval_hardening:
  active_portfolio_day_coverage_gate: true
  optional_reference_metric_equivalence_gate: true
  exposure_diagnostics_reported: true
  report_sample_coverage: true
  report_reference_comparison: true
```

After the hardening smoke passes, the focused loop should generate only a small number of children. It should either mutate the `attempt_017` child directly or use it as prompt evidence, but it must treat `attempt_017` as `sample_review`, not as a promoted parent.

Controller smoke-test Sharpe must not be used as alpha evidence. It is only an invariant smoke metric.

## Main Links

- Active design: [README.md](README.md), [task_001_search_design.md](task_001_search_design.md), [task_004_seed_strategy_program.md](task_004_seed_strategy_program.md)
- Contracts: [daily_stock_contract_v1.md](daily_stock_contract_v1.md), [prompt_contracts.md](prompt_contracts.md), [evaluator_contract.md](evaluator_contract.md), [program_database_schema.md](program_database_schema.md)
- Memory and skills: [reasoning_memory_layer_design.md](reasoning_memory_layer_design.md), [dr_rtl_method_transfer_20260504.md](dr_rtl_method_transfer_20260504.md), [diagnostic_analyzer_and_skill_library_20260504.md](diagnostic_analyzer_and_skill_library_20260504.md), [alphaevolve_extension_methods_20260509.md](alphaevolve_extension_methods_20260509.md), [Reasoning Memory for AlphaEvolve Search](../../../wiki/methods/Reasoning%20Memory%20for%20AlphaEvolve%20Search.md), [Group-Relative Skill Learning for Alpha Search](../../../wiki/methods/Group-Relative%20Skill%20Learning%20for%20Alpha%20Search.md), [AlphaEvolve Extension Methods for Quant Search](../../../wiki/methods/AlphaEvolve%20Extension%20Methods%20for%20Quant%20Search.md)
- Data and costs: [dataset_context.md](dataset_context.md), [dataset_admission_policy.md](dataset_admission_policy.md), [universe_and_split_policy.md](universe_and_split_policy.md), [cost_model_policy.md](cost_model_policy.md)
- Remote/runtime: [remote_qwen_vllm_config.md](remote_qwen_vllm_config.md), [remote_csv_execution_policy.md](remote_csv_execution_policy.md), [model_stack_and_vllm_results.md](model_stack_and_vllm_results.md)
- Dated evidence records: [remote_evidence_review_20260430.md](remote_evidence_review_20260430.md), [controller_batch_001_small_review_20260430.md](controller_batch_001_small_review_20260430.md), [controller_batch_001_small_repair_v1_review_20260430.md](controller_batch_001_small_repair_v1_review_20260430.md), [controller_batch_001_small_semantic_v2_review_20260501.md](controller_batch_001_small_semantic_v2_review_20260501.md), [controller_batch_001_small_semantic_v3_review_20260501.md](controller_batch_001_small_semantic_v3_review_20260501.md), [controller_batch_001_small_semantic_v4_review_20260508.md](controller_batch_001_small_semantic_v4_review_20260508.md), [controller_batch_001_review_20260509.md](controller_batch_001_review_20260509.md), [controller_batch_001_diversity_topup_review_20260509.md](controller_batch_001_diversity_topup_review_20260509.md), [remote_sample_eval_controller_batch_001_review_20260509.md](remote_sample_eval_controller_batch_001_review_20260509.md), [controller_batch_001_attempt017_repair_hardening_20260510.md](controller_batch_001_attempt017_repair_hardening_20260510.md), [controller_evaluator_hardening_smoke_review_20260511.md](controller_evaluator_hardening_smoke_review_20260511.md)
- Remote handoff: [controller_batch_001_remote_instructions_20260508.md](controller_batch_001_remote_instructions_20260508.md), [controller_batch_001_diversity_topup_remote_instructions_20260509.md](controller_batch_001_diversity_topup_remote_instructions_20260509.md), [controller_batch_001_curated_sample_eval_remote_instructions_20260509.md](controller_batch_001_curated_sample_eval_remote_instructions_20260509.md), [controller_batch_001_attempt017_repair_remote_instructions_20260509.md](controller_batch_001_attempt017_repair_remote_instructions_20260509.md), [controller_evaluator_hardening_remote_instructions_20260510.md](controller_evaluator_hardening_remote_instructions_20260510.md), [controller_attempt017_search_control_remote_instructions_20260511.md](controller_attempt017_search_control_remote_instructions_20260511.md), [controller_attempt017_mechanism_batch_remote_instructions_20260513.md](controller_attempt017_mechanism_batch_remote_instructions_20260513.md), [configs/controller_batch_001_remote_qwen.yaml](configs/controller_batch_001_remote_qwen.yaml)
- Durable method memory: [AlphaEvolve Lite Quant Search Workflow](../../../wiki/methods/AlphaEvolve%20Lite%20Quant%20Search%20Workflow.md), [AlphaEvolve Extension Methods for Quant Search](../../../wiki/methods/AlphaEvolve%20Extension%20Methods%20for%20Quant%20Search.md)
