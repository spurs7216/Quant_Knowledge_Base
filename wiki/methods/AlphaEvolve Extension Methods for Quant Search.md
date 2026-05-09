---
title: AlphaEvolve Extension Methods for Quant Search
type: method
status: active
updated: 2026-05-09
tags:
  - method
  - alphaevolve
  - quant-research
  - program-search
  - novelty-search
  - quality-diversity
sources:
  - "../sources/papers/AlphaEvolve - A coding agent for scientific and algorithmic discovery.md"
  - "../sources/papers/CodeEvolve - An Open-Source Evolutionary Framework for Algorithmic Discovery and Optimization.md"
  - "../sources/papers/ShinkaEvolve - Towards Open-Ended and Sample-Efficient Program Evolution.md"
  - "../sources/papers/ThetaEvolve - Test-time Learning on Open Problems.md"
  - "../../projects/quant_research_system/phase4_search_loop/alphaevolve_extension_methods_20260509.md"
  - "../../projects/quant_research_system/phase4_search_loop/current_state.md"
---
# AlphaEvolve Extension Methods for Quant Search

## Summary

The base AlphaEvolve loop gives four necessary modules: prompt sampler, LLM ensemble, evaluator pools, and program database. CodeEvolve, ShinkaEvolve, and ThetaEvolve show that these modules need sharper internal policies when search moves beyond a toy run.

The durable lesson for quant research is:

```text
evolution quality = evaluator validity
                  + database diversity
                  + novelty pressure
                  + parent/prompt selection
                  + bounded generation contracts
```

For equity alpha search, these extension methods should strengthen controller discipline before broad market evaluation. They should not be used to justify looser gates or early RL on noisy validation results.

## Extension Map

| Source | Main extension | Quant translation |
| --- | --- | --- |
| CodeEvolve | Operator portfolio, island search, plateau scheduling, MAP-Elites/CVT-MAP-Elites, prompt fitness | Track prompt/surface/memory-card productivity, use descriptor cells, shift exploration when a surface repeats duplicates |
| ShinkaEvolve | Weighted parent sampling, offspring-count penalty, embedding/LLM novelty rejection, bandit model selection, meta-scratchpad | Penalize overused parents and intents, reject exact and near duplicates before data evaluation, write compact run memory |
| ThetaEvolve | Single-model simplification, large database, batch sampling, lazy duplicate penalties, reward shaping, optional test-time RL | Keep Qwen-only inner loop simple, treat duplicates/no-ops as negative evidence, defer reward shaping and RL until evaluator distributions are stable |

## Database Is Not Just Storage

All three extensions make the program database more active than a log.

It should answer:

- which parents have been overused;
- which prompt cards produce valid nonduplicate children;
- which target surfaces and intents are saturated;
- which MAP cells are empty or underfilled;
- which failure categories are increasing;
- which patches are exact or near duplicates;
- which children are useful inspirations despite not being current winners.

For Phase 4, the database should therefore store both proof-of-attempt facts and search-control descriptors.

## Duplicate Control Stack

The current Phase 4 bottleneck is duplicate generation, especially ranking/direction-flip attempts. The extension papers imply a layered response.

Minimum deterministic layer:

```text
child_code_hash
patch_fingerprint
target_surface
target_intent
parent_id
parent_offspring_count
map_cell
duplicate_retry_count
```

Next novelty layer:

```text
mutable_block_embedding or token shingles
max_similarity_with_island
near_duplicate_reason
semantic_descriptor_delta
```

Prompt layer:

```text
prior accepted same-surface summaries
prior duplicate fingerprints
occupied MAP cells
mandatory target intent
do-not-repeat cards
```

Evaluator layer:

```text
exact duplicate -> stored failure, not unique pass
no-op child -> lazy penalty
near duplicate in diversity top-up -> retry or reject
novel but invalid -> failure memory, not promotion
```

## Parent And Prompt Sampling

A Phase 4 parent should not be sampled only by best score. Before market evaluation exists, controller-static quality and novelty should guide sampling.

A practical first parent weight can be:

```text
validity_score = 1 if controller_static passed else 0
novelty_score = 1 / (1 + duplicate_count_in_cell)
offspring_penalty = 1 / (1 + parent_offspring_count)
surface_bonus = underfilled_surface_weight

parent_weight = validity_score
              * novelty_score
              * offspring_penalty
              * surface_bonus
```

After sample/full evaluator results exist, add a separate scalar performance term, but keep hard gates outside the scalar objective.

Prompt sampling should use prompt fitness:

```text
prompt_fitness = best useful child produced by prompt_card
prompt_reliability = nonduplicate_controller_passes / attempts
prompt_risk = hard_gate_failures / attempts
lazy_penalty = negative evidence for empty, malformed, invalid, duplicate, or near-duplicate outputs
```

The active Phase 4 implementation is `prompt_fitness_and_lazy_score_v1`. It gives a controller-static pass a positive search score, assigns deterministic negative scores to lazy or invalid output categories, rolls those scores up by prompt card, emits low-fitness prompt-card diagnostics, and exposes the result in both prompt context and artifacts. This is controller search quality only; it is not a market-alpha score.

## Quality-Diversity Descriptors For Quant Search

Good descriptors are not arbitrary code metrics. They should correspond to research behavior.

Useful Phase 4 descriptors:

- evolve surface: `signal`, `ranking`, `portfolio`, `risk`;
- target intent: `direction_flip`, `vol_scaling`, `sector_neutral`, `turnover_control`, `tail_clip`, `liquidity_filter`, `ranking_smooth`, `side_balance`;
- signal family: reversal, trend, innovation, residual, volatility, liquidity, sector/industry;
- holding-period tendency: short, medium, slow;
- exposure behavior: gross, net, max weight, long/short balance;
- turnover behavior: low, medium, high;
- data scope: daily-stock-only, approved joined dataset, rejected dataset attempt;
- evaluator state: controller-pass, semantic-fail, vector-fail, duplicate, data-eval-pass.

The MAP archive should be used to preserve diverse valid behavior, not just diverse syntax.

## Reward Shaping Rule

ThetaEvolve's reward shaping is useful only after observing score distributions. In quant research:

1. Run controller-only batches until generated children are unique and semantically valid.
2. Run sample evaluators on a small diverse subset.
3. Inspect distributions of Sharpe, net return, turnover, cost drag, concentration, coverage, and null-relative performance.
4. Only then define a shaped scalar for parent/prompt selection.

Do not train or fine-tune a model against validation Sharpe during Phase 4. The reward is too noisy and too vulnerable to overfit until the evaluator stack is much more mature.

## LLM Stack Implications

The extension papers do not require local LLM inference. In this project:

- local Windows remains edit/review/sync only;
- Qwen calls run on the remote Linux/GPU machine;
- Gemma is not in the active Phase 4 model stack unless a future remote evidence run justifies reactivation;
- a model bandit should wait until at least two remote models are stable under the same patch contract;
- a 16,384 completion-token budget appears in ShinkaEvolve and ThetaEvolve experiments, but Phase 4 should tune completion tokens from observed failure modes rather than copying a paper value mechanically.

## Adoption Matrix

Use now:

- prior-summary duplicate seeding;
- mandatory target intent;
- exact code-hash and patch-fingerprint duplicate rejection;
- deterministic edit-signature near-duplicate checks;
- parent offspring counts, surface/intent saturation counters, prompt-card duplicate counters, prompt-card fitness, and lazy penalties;
- MAP-cell reporting;
- reasoning memory and skill cards;
- remote-only Qwen execution.

Use in the next implementation slice if duplicate pockets persist:

- plateau-triggered exploration schedule.
- stronger surface-level rerouting when a scheduled surface is saturated.

Use later, after sample/full evaluator stability:

- evaluator-informed scalar reward shaping;
- inspiration crossover among diverse accepted children;
- model-bandit routing across stable remote models;
- batched generation with careful database audit ordering.

Defer:

- full rewrites outside narrow evolve blocks;
- RL fine-tuning against quant validation results;
- automatic dataset expansion by generated children;
- static-environment RL from only the initial seed.

## Related Notes

- [[AlphaEvolve Lite Quant Search Workflow]]
- [[Reasoning Memory for AlphaEvolve Search]]
- [[Group-Relative Skill Learning for Alpha Search]]
- [[CodeEvolve - An Open-Source Evolutionary Framework for Algorithmic Discovery and Optimization]]
- [[ShinkaEvolve - Towards Open-Ended and Sample-Efficient Program Evolution]]
- [[ThetaEvolve - Test-time Learning on Open Problems]]
