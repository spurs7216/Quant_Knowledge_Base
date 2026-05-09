---
title: AlphaEvolve Extension Methods Readthrough
type: project
status: active
updated: 2026-05-09
tags:
  - project
  - phase4
  - alphaevolve
  - codeevolve
  - shinkaevolve
  - thetaevolve
sources:
  - "../../../wiki/sources/papers/CodeEvolve - An Open-Source Evolutionary Framework for Algorithmic Discovery and Optimization.md"
  - "../../../wiki/sources/papers/ShinkaEvolve - Towards Open-Ended and Sample-Efficient Program Evolution.md"
  - "../../../wiki/sources/papers/ThetaEvolve - Test-time Learning on Open Problems.md"
  - "../../../wiki/methods/AlphaEvolve Extension Methods for Quant Search.md"
  - "current_state.md"
  - "controller_batch_001_review_20260509.md"
---
# AlphaEvolve Extension Methods Readthrough

## Purpose

This note records the Phase 4 interpretation of CodeEvolve, ShinkaEvolve, and ThetaEvolve after the first 50-attempt controller run showed healthy mechanics but too many duplicate children.

The readthrough does not change the immediate evidence state: we have still not completed market evaluation or a full iterative evolution round. The current bottleneck remains controller-level uniqueness.

## What Is New Compared With The Previous Plan

The old Phase 4 plan already had the AlphaEvolve modules, reasoning memory, diagnostic cards, a skill library, MAP-style descriptors, and duplicate retry. The extension papers sharpen the next level of design:

- CodeEvolve says diversity should be maintained by island topology, descriptor cells, prompt fitness, and plateau-aware exploration, not by instructions alone.
- ShinkaEvolve says sample efficiency comes from parent sampling, offspring-count penalties, novelty rejection, and meta-scratchpad memory before expensive evaluation.
- ThetaEvolve says duplicate/no-op outputs should receive explicit lazy penalties and that batch throughput or RL only works after the environment and evaluator are stable.

The practical change is that duplicate handling should become an explicit population policy.

## Current Controller Implication

`controller_batch_001` had 35 unique controller-static passes out of 50 attempts. The rejected children were mostly duplicates, concentrated in `ranking/direction_flip`.

The right response is not to weaken duplicate rejection. It is:

1. keep the 20-attempt controller-only diversity top-up as the next remote action;
2. seed prior hashes, accepted summaries, duplicate fingerprints, and occupied MAP cells into that run;
3. treat repeated ranking/direction-flip outputs as evidence of an overused intent pocket;
4. make prompt-card productivity and lazy duplicate/no-op penalties observable before any market evaluation;
5. if the top-up still fails uniqueness, inspect prompt-card fitness and target-intent compliance before adding heavier novelty machinery.

## Adopt Now

Already aligned with the current handoff:

- mandatory target intent in generation prompts;
- prior-summary duplicate and MAP-state seeding;
- exact child-hash duplicate rejection;
- patch-fingerprint duplicate rejection where available;
- reasoning memory and skill-card retrieval;
- remote-only Qwen execution;
- controller-only top-up before `remote_sample_eval`.

## Implemented Next: Controller Population Policy V2

Implemented after this readthrough:

```yaml
slice: controller_population_policy_v2 + prompt_fitness_and_lazy_score_v1
purpose: make duplicate prevention a sampler/database policy
changes:
  - track parent_offspring_count in the prompt-sampling summary
  - track target_intent occupancy by surface
  - downweight saturated surface/intent cells
  - expose near-duplicate patch fingerprints in prompt cards
  - add deterministic edit-signature token-shingle similarity before expensive evaluator calls
  - add prompt_card reliability and duplicate rates
  - assign lazy penalties to empty, malformed, invalid, duplicate, and near-duplicate attempts
  - persist controller_search_score, lazy_penalty_score, prompt_card_fitness, and prompt_card_lazy_penalty_sums
  - use prompt-card fitness as a deterministic selector signal for future attempts in the same run
  - emit `diag_low_prompt_card_fitness` when controller diagnostics detect weak prompt cards
tests:
  - compileall for research/alphaevolve_lite
  - mock duplicate controller batch
  - direct artifact check that summary.md, summary.json, micro_filter_result.json, and population_policy_state.json expose prompt fitness and lazy scores
```

This slice remains deterministic and controller-local. Embedding novelty and LLM novelty judging can wait until exact, fingerprint, and edit-signature policies are proven insufficient.

## Defer

Do not implement these before the controller and sample evaluator are stable:

- full-program rewrites outside narrow evolve blocks;
- model-bandit routing without two stable remote models under the same patch contract;
- batch generation that breaks audit ordering;
- reward shaping from uninspected market score distributions;
- RL fine-tuning against validation Sharpe or any early sample-evaluator metric.

ThetaEvolve is valuable, but its RL result relies on deterministic verifiers and heavy GPU infrastructure. A trading validator is not a theorem checker.

## Token-Budget Note

ShinkaEvolve and ThetaEvolve both report 16,384 maximum response tokens in their experimental configurations. This is useful precedent, but it does not by itself prove that Phase 4 should always use 16,384 completion tokens.

Our prior null-content failure was caused by Qwen reasoning content consuming the response while `message.content` was empty. The fix was top-level no-thinking routing plus empty-content retry. Completion-token budget should be increased only when artifacts show true truncation or insufficient final-content space.

## Working Consensus

The next remote run should remain the controller-only diversity top-up, now with `controller_population_policy_v2` enabled. If it passes the uniqueness gate, select a small diverse set of nontrivial children for `remote_sample_eval`. If it fails, inspect target-intent compliance and near-duplicate decisions before market evaluation.

## Durable Reference

The reusable synthesis lives in [[AlphaEvolve Extension Methods for Quant Search]].
