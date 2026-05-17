---
title: AlphaEvolve Lite Quant Search Workflow
type: method
status: active
updated: 2026-05-17
tags:
  - method
  - alphaevolve
  - quant-research
  - search-loop
  - program-database
sources:
  - "../sources/papers/AlphaEvolve - A coding agent for scientific and algorithmic discovery.md"
  - "../sources/papers/CodeEvolve - An Open-Source Evolutionary Framework for Algorithmic Discovery and Optimization.md"
  - "../sources/papers/ShinkaEvolve - Towards Open-Ended and Sample-Efficient Program Evolution.md"
  - "../sources/papers/ThetaEvolve - Test-time Learning on Open Problems.md"
  - "AlphaEvolve Extension Methods for Quant Search.md"
  - "../../projects/quant_research_system/phase4_search_loop/current_state.md"
  - "../../projects/quant_research_system/phase4_search_loop/task_001_search_design.md"
  - "../../projects/quant_research_system/phase4_search_loop/alphaevolve_method_translation.md"
---
# AlphaEvolve Lite Quant Search Workflow

## Summary

AlphaEvolve-lite for quant research is an executable program-search loop disciplined by a stronger evaluator. It is not a parameter grid, not a benchmark batch, and not a free-form strategy generator.

The reusable loop is:

```text
parent_program, inspirations = program_database.sample()
prompt = prompt_sampler.build(parent_program, inspirations, evidence_context)
diff = llm_ensemble.generate(prompt)
child_program = deterministic_patch_apply(parent_program, diff)
results = evaluator_pool.execute(child_program)
program_database.add(child_program, results)
```

For trading research, the evaluator must be stricter than the generator because historical alpha discovery is vulnerable to leakage, overfitting, cost underestimation, concentration, and fragile universe choices.

## Reasoning Memory Layer

The program database is exhaustive search memory, but it is too raw for direct prompt use. A ReasoningBank-style layer should sit between the database and prompt sampler.

```text
program_database / artifacts
  -> evidence packet
  -> distilled reasoning memory
  -> stage-aware prompt cards
  -> next child proposal
```

Reasoning memory stores compact lessons from successes and failures: patch-contract guardrails, portfolio semantic pitfalls, model-routing issues, data-contract reminders, and evaluator caveats. It should be retrieved by stage, target evolve surface, search island, and similarity before being injected into prompts.

For quant research, deterministic controller and evaluator outcomes should label success or failure. The LLM may synthesize candidate memories, but it should not be the authority on whether a child was valid.

## Diagnostic And Skill Layers

Dr. RTL adds two layers that are useful on top of ordinary AlphaEvolve program storage.

The diagnostic analyzer localizes bottlenecks before generation:

```text
evaluator/controller artifact -> bottleneck card -> bounded mutation prompt
```

The explicit skill library stores confidence-tagged pattern -> strategy rules:

```text
pattern: recurring bottleneck
strategy: reusable transformation principle
confidence: high | medium | low | avoid
status: candidate | active | superseded | rejected
```

In quant search, these layers must stay subordinate to deterministic gates. A diagnostic card is not proof of alpha, and a skill should not become active from one noisy backtest.

## Extension Methods

CodeEvolve, ShinkaEvolve, and ThetaEvolve sharpen the base loop in ways that matter for Phase 4.

The shared message is that the program database is an active search-control object, not only a result archive. It should track prompt productivity, parent offspring counts, occupied MAP cells, duplicate fingerprints, surface/intent saturation, and failure categories.

Practical additions:

- CodeEvolve supports island search, prompt fitness, inspiration crossover, plateau-triggered exploration, and MAP-Elites/CVT-MAP-Elites diversity pressure.
- ShinkaEvolve supports weighted parent sampling, offspring-count penalties, novelty rejection, adaptive model selection, and periodic meta-scratchpad summaries.
- ThetaEvolve supports single-model simplification, large program databases, batch sampling on remote inference engines, explicit lazy penalties for no-op or duplicate outputs, and reward shaping only after score distributions are known.

For the current quant loop, these ideas should first strengthen duplicate and novelty control. They should not be used to launch RL, full-program rewrites, or automatic dataset expansion before the controller and sample evaluator are stable.

The active controller translation is `controller_population_policy_v2` plus `prompt_fitness_and_lazy_score_v1`: deterministic parent offspring counts, surface/intent saturation counters, prompt-card duplicate counters, prompt-card fitness, lazy invalid-output penalties, and edit-signature near-duplicate checks. This is still controller-local; it does not use embeddings, LLM novelty judges, market reward shaping, or model fine-tuning.

## Module Translation

| AlphaEvolve module | Quant implementation role |
| --- | --- |
| Prompt sampler | Builds compact prompts from parent code, target evolve surface, evaluator summaries, diagnostic cards, skill cards, prior accepted/rejected patches, `wiki/` method knowledge, `catalog/` dataset context, and immutable rules. |
| LLM ensemble | Uses a fast remote model for many bounded patches, a repair role for malformed diffs, and optional larger reviewers for search-state synthesis. |
| Evaluator pools | Runs a cascade: static parsing and semantic checks, toy arrays, remote sample data, validation subsets, full validation, and final human review. |
| Program database | Stores every child, including failures, with lineage, prompt, diff, code hash, scores, descriptors, hard gates, validation exposure, and artifact paths. |

The program database is search memory. A candidate registry is reviewed lineage. They should not be collapsed into one object.

## Quant-Specific Gates

Hard gates should be separate from scalar scores.

Typical hard gates:

- no train/validation/test split edits;
- no universe-construction edits by generated children;
- no raw data-path edits;
- no cost removal;
- no broker, account, position, order, TWS, or IBKR logic;
- point-in-time dataset joins only;
- finite weights and returns;
- bounded gross, net, turnover, and max weight;
- both long and short books present when the strategy is long/short;
- compact artifacts produced with enough provenance.

Typical scalar scores:

- validation net Sharpe;
- validation net return;
- negative turnover;
- negative cost drag;
- negative concentration;
- parent-relative improvement;
- matched-null-relative improvement;
- subperiod stability;
- liquidity robustness;
- novelty or descriptor diversity.

## Semantic Checks

In this workflow, `semantic` means program and trading-logic semantics, not proof of market alpha.

Controller semantic checks ask whether a generated program still has the intended shape:

- long weights are positive and short weights are negative;
- both books are active when the strategy is meant to be long/short;
- net exposure is near zero when the evaluator expects a dollar-neutral book;
- gross exposure and max weight stay within contract limits;
- signal/ranking/portfolio changes do not silently change split, universe, costs, or data access.

Market validity is a later question handled by data-backed evaluators, costs, null baselines, robustness slices, and held-out validation.

## Failure Memory From Phase 4

The first Phase 4 controller batches produced reusable operating lessons:

- exposing the full seed program caused marker copying and helper edits, so prompts now expose only one target evolve-block body;
- syntax, exact SEARCH matching, compile, and vector smoke did not catch one-sided portfolios, so portfolio semantic gates are mandatory;
- duplicate simple sign flips can look like multiple successes unless child program hashes are tracked;
- prompt cards that repeatedly produce invalid, lazy, duplicate, or near-duplicate patches should receive negative controller evidence before expensive market evaluation;
- sample `sample_pass` must require broad active portfolio-day coverage, because a child can generate extreme Sharpe by trading only a few dates;
- child sample evaluation should compare against the seed or parent summary when available, because code-different children can be metric-equivalent after ranking and risk controls;
- child sample evaluation should also compare against prior sample-evaluated siblings, because a child can differ from the parent yet replay a prior occupied MAP-cell elite;
- a controller-static pass in an occupied MAP cell should not receive another sample evaluation unless it beats and materially differs from the current cell elite;
- when a research plan names exact underfilled mechanism cells, the controller runner should force `surface/intent` cells directly; surface-only schedules can drift into absorbed or already-saturated prompt cards;
- medium-model mechanism cards must use exact search vocabulary: allowed surfaces, allowed target intents, and frozen `CONTRACT.*` daily-stock field handles;
- missing-held-weight repairs must not use evaluator-only forward-return fields; reducing missingness by knowing next-day availability is lookahead;
- signal-proportional portfolio weighting must use positive magnitudes for each side and assign negative weights to shorts explicitly;
- hard signal saturation can preserve signs but still imbalance exposure;
- Qwen-style reasoning modes can return `message.content = null`, so serving/routing must disable thinking in the actual HTTP payload and record reasoning-only failures;
- failed children are still useful if their failure category becomes prompt or repair memory.

## Use In Future Projects

Use this workflow when the research object can be represented as executable code and automatically evaluated. Avoid it when the evaluator is vague, the data contract is unfrozen, or success depends on unverified discretionary interpretation.

Minimum setup before search:

1. Freeze the dataset fields and timing convention.
2. Define non-evolvable skeleton code for data loading, splits, universe, costs, and artifacts.
3. Mark narrow evolve blocks.
4. Implement deterministic patch parsing and static gates.
5. Add semantic checks for the strategy family.
6. Store every attempt in a searchable program database.
7. Use test data only after branch freeze.

## Related Notes

- [AlphaEvolve source note](../sources/papers/AlphaEvolve%20-%20A%20coding%20agent%20for%20scientific%20and%20algorithmic%20discovery.md)
- [ReasoningBank source note](../sources/papers/ReasoningBank%20-%20Scaling%20Agent%20Self-Evolving%20with%20Reasoning%20Memory.md)
- [CodeEvolve source note](../sources/papers/CodeEvolve%20-%20An%20Open-Source%20Evolutionary%20Framework%20for%20Algorithmic%20Discovery%20and%20Optimization.md)
- [ShinkaEvolve source note](../sources/papers/ShinkaEvolve%20-%20Towards%20Open-Ended%20and%20Sample-Efficient%20Program%20Evolution.md)
- [ThetaEvolve source note](../sources/papers/ThetaEvolve%20-%20Test-time%20Learning%20on%20Open%20Problems.md)
- [AlphaEvolve Extension Methods for Quant Search](AlphaEvolve%20Extension%20Methods%20for%20Quant%20Search.md)
- [Reasoning Memory for AlphaEvolve Search](Reasoning%20Memory%20for%20AlphaEvolve%20Search.md)
- [Phase 4 Current State](../../projects/quant_research_system/phase4_search_loop/current_state.md)
- [Backtest Overfitting](../concepts/Backtest%20Overfitting.md)
- [Financial Machine Learning Workflow](Financial%20Machine%20Learning%20Workflow.md)
- [Kalman Filtering](Kalman%20Filtering.md)
- [Portfolio Construction](../strategies/Portfolio%20Construction.md)
