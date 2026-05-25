# AlphaEvolve-Lite Scaffold

This module holds the local control primitives for the Phase 4 search loop.

It is not a full AlphaEvolve implementation. It gives the project the pieces that must exist before strategy-generation prompts are useful:

- detect bounded `# EVOLVE-BLOCK-START` / `# EVOLVE-BLOCK-END` regions
- parse and apply AlphaEvolve-style SEARCH/REPLACE diffs
- store early smoke-test program records with lineage, metrics, descriptors, and status
- sample prior records for prompt construction
- store and retrieve compact reasoning-memory cards for prompt construction
- build deterministic diagnostic cards from evaluator/controller artifacts
- store and retrieve explicit skill-library cards with confidence and status
- evaluate safe daily-stock expression seeds before promoting them into full seed programs

Phase 4 v2 supersedes the initial JSONL-only database design. `program_database.py` remains a small smoke-test primitive; production search should implement the SQLite schema and JSONL audit log described in `projects/quant_research_system/phase4_search_loop/program_database_schema.md`.

The first production use should keep data loading, split dates, duplicate policy, cost accounting, and artifact writing outside evolve blocks.

`reasoning_memory.py` is the local ReasoningBank-style scaffold. It bootstraps evidence-linked Phase 4 seed lessons, retrieves active cards by controller stage and target surface, and writes deterministic batch memory updates. It does not call local Qwen or local embedding inference.

`diagnostic_analyzer.py` and `skill_library.py` are the Dr. RTL transfer scaffold. The analyzer localizes bottlenecks without proposing patches; the skill library stores explicit pattern -> strategy rules and writes candidate skill updates after controller batches. Candidate skills are not automatically promoted to active.

Controller batch refactor notes:

- `artifact_io.py` owns shared JSON normalization and deterministic JSON artifact writes.
- `controller_batch_artifacts.py` owns prompt-message artifacts and controller summary rendering.
- `controller_batch_filter.py` owns controller-static micro-filter execution plus the bounded one-shot repair path.
- `controller_batch_mocks.py` owns deterministic mock patches used by local smoke tests.
- `controller_batch_state.py` owns prior-summary seeding, duplicate state, MAP-cell state, explicit surface schedules, and exact target-cell schedules for controller top-up runs.
- `controller_execution_effect.py` owns the controller-local distinction between safe code changes and execution-effective changes that survive to ranked signals, final weights, or exposure shape.
- `controller_sample_eval_policy.py` owns deterministic controller-to-sample-eval eligibility, including occupied-MAP-cell elite comparison before expensive remote sample evaluation.
- `controller_population_policy.py` owns controller population-policy v2: parent offspring counts, surface/intent saturation counters, prompt-card productivity/fitness counters, deterministic lazy penalties for invalid or duplicate outputs, prompt-facing population context, and deterministic edit-signature near-duplicate checks.
- `micro_filter.py` owns deterministic child safety plus parent-child smoke behavior-delta diagnostics. Exact smoke no-ops are controller rejects; weaker deltas remain diagnostics.
- `diversity.py` owns MAP descriptors, including patch intent, portfolio-shape buckets, and behavior-delta buckets.
- `controller_prompt_context.py` owns prompt-side retrieval and rendering of reasoning-memory cards, diagnostic cards, and skill cards.
- `mechanism_cards.py` owns mechanism-card parsing and exact contract validation for surface, intent, and `CONTRACT.*` daily-stock field handles.
- `expression_evolution.py` owns the AlphaAgentEvo-style daily-stock expression layer: safe field/operator DSL, causal signal evaluation, constrained dollar-neutral portfolio construction, seed-expression catalog, expression similarity, and multi-turn trajectory scoring. It does not own data loading, sample-evaluation accounting, cost sensitivity, or promotion gates.
- `expression_eval_records.py` owns shared expression sample-pass gates and artifact row rendering so seed-zoo and episode outputs use the same status semantics.
- `expression_population.py` owns expression-episode population policy: deterministic child-survivor parent selection, MAP-style descriptors, parent-sampling eligibility, selection scores, novelty scoring, and branch stop-loss diagnostics. It does not evaluate market performance or promote children.
- `expression_episode.py` owns the Qwen expression-episode prompt, JSON parser, duplicate/similarity diagnostics, and trajectory-record conversion.
- `daily_stock_eda.py` owns the chunked daily-stock empirical map used to convert the frozen field contract into prompt-facing data guidance. It writes data-understanding artifacts only; it is not an alpha evaluator.
- `daily_stock_forward_coverage.py` owns the chunked rolling top-N coverage and evaluator-style forward-return availability diagnostic. It answers data-coverage and missing-held-cause questions only; it must not become an alpha evaluator. Its default forward-availability window now matches the active 2011-2025 IS/OS evaluator window.
- `splits.py` owns the active Phase 4 split contract: fixed IS/OS with 2011-2022 in-sample and 2023-2025 out-of-sample. The old 70/15/15 builder is retained only for legacy diagnostics.
- `scripts/run_child_batch.py` should remain the orchestration entry point; avoid adding new artifact, repair, mock-patch, or prompt-context policy directly into the script when a module can own it.
- `scripts/profile_daily_stock_data.py` is the remote CLI for the daily-stock EDA milestone. It should run on the remote data machine, not local Windows, for full-file profiling.
- `scripts/profile_daily_stock_forward_coverage.py` is the remote CLI for whole-timeline rolling top-500 coverage plus active-window forward-return availability diagnostics. It should run on the remote data machine and does not require Qwen or vLLM.
- `scripts/export_expression_interface.py` writes prompt-facing expression-interface markdown and seed-library JSON for remote expression-generation runs. It does not evaluate alphas.
- `scripts/run_expression_seed_zoo.py` is the remote CLI for deterministic daily-stock expression seed evaluation under the repaired rolling top-500, forward-return, IS/OS, cost, max-weight, and coverage contracts. It does not call Qwen.
- `scripts/run_expression_episode.py` is the remote CLI for Qwen-backed JSON expression episodes. It calls remote vLLM through `model_router.py`, validates generated DSL expressions, evaluates them under the same seed-zoo contracts, records duplicate/similarity diagnostics, samples later-turn parents from eligible child survivors by default, and writes trajectory plus population-ledger artifacts. Child IDs include a run token, and `--prior-population-ledger` can reload previous ledger artifacts for duplicate checks and historical parent sampling. It supports `--mock-response-json` for local tests without running Qwen.

Remote sample-evaluator refactor notes:

- `sample_eval_metrics.py` owns one-day-forward return construction, portfolio accounting, split metrics, scorecards, and cost sensitivity.
- `sample_eval_metrics.py` separates signal-date universe rows from next-day return source rows for remote sample evaluation. The active contract is `signal_universe_t_return_source_eligible_t_plus_1_v1`: strategies trade rolling top-500 names at date t, while evaluator accounting sources date-(t+1) returns from the statically eligible raw panel.
- `sample_eval_metrics.py` also owns active portfolio-day coverage diagnostics so sparse few-day sample artifacts cannot pass as broad daily-stock evidence.
- `sample_eval_metrics.py` reports gross/net/long/short exposure diagnostics so de-grossing artifacts are visible in parent-relative comparisons.
- `sample_eval_metrics.py` owns search-sample equivalence checks against seed/parent references and prior sample-evaluated siblings.
- `sample_eval_baselines.py` owns sign-flip and matched-random null baseline construction.
- `scripts/remote_sample_eval.py` should remain the remote CLI orchestration entry point; keep loading, hard gates, artifact routing, lineage validation, and database writes there unless a new reusable contract appears. Its default analysis window is 2011-2025 with fixed IS/OS metrics. Child sample evaluations must use explicit child `--program-id`, should provide `--parent-program-id`, and should pass prior sibling summaries with `--prior-sample-summary` when checking a follow-up branch.
