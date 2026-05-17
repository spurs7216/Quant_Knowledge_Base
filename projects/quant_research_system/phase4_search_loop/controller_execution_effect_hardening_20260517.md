---
title: Controller Execution-Effect Hardening 2026-05-17
type: project
status: active
updated: 2026-05-17
tags:
  - project
  - phase4
  - alphaevolve
  - controller
  - hardening
sources:
  - "controller_attempt017_forced_cell_smoke_review_20260517.md"
  - "../../../wiki/methods/AlphaEvolve Lite Quant Search Workflow.md"
---
# Controller Execution-Effect Hardening 2026-05-17

## Purpose

The forced-cell smoke proved exact `surface/intent` routing but exposed a weaker controller contract: a child could pass controller-static gates while changing only raw signal magnitude, with ranked signal and final weights unchanged.

This patch makes execution effect explicit.

## Implemented Contract

```yaml
contract: controller_execution_effect_v1
signal_or_ranking_child_required_effect:
  - ranked_signal changes
  - or final weights change
portfolio_or_risk_child_required_effect:
  - final weights change
  - or exposure shape changes after risk controls
failure_category: execution_effect_failed
repairable: true
```

This is still not market-alpha evidence. It is a controller-local budget rule: do not spend sample-eval or success-memory attention on patches that are absorbed before execution-relevant outputs change.

## Files Changed

```yaml
code:
  - research/alphaevolve_lite/controller_execution_effect.py
  - research/alphaevolve_lite/micro_filter.py
  - research/alphaevolve_lite/controller_batch_filter.py
  - research/alphaevolve_lite/controller_batch_artifacts.py
  - research/alphaevolve_lite/controller_sample_eval_policy.py
  - research/alphaevolve_lite/controller_population_policy.py
  - research/alphaevolve_lite/diagnostic_analyzer.py
  - research/alphaevolve_lite/prompt_builder.py
  - research/alphaevolve_lite/reasoning_memory.py
  - research/alphaevolve_lite/skill_library.py
tests:
  - research/alphaevolve_lite/tests/test_phase4_hardening.py
docs:
  - research/alphaevolve_lite/README.md
  - wiki/methods/AlphaEvolve Lite Quant Search Workflow.md
  - projects/quant_research_system/phase4_search_loop/current_state.md
```

## Prompt Repairs

The prompt now carries the following concrete repairs:

- `liquidity_adjusted_reversal`: avoid inverse raw dollar volume clipped into a uniform scale; use bounded relative liquidity, log liquidity, percentile, market-cap, or rolling confidence logic that can affect ranks or selected weights.
- `persistence_trade_gate`: `signal` is local data, not a panel field; create prior signal from `data.groupby(CONTRACT.security_id)["signal"].shift(1)`.
- `liquidity_scaled_cap`: per-name caps must be no larger than `max_weight`; clip, side-renormalize, and clip again.
- `liquidity_weighted_sides`: avoid side-weight formulas that max-weight clipping turns back into equal weights.

## Verification

Local checks on 2026-05-17:

```powershell
python -m py_compile research/alphaevolve_lite/controller_execution_effect.py research/alphaevolve_lite/micro_filter.py research/alphaevolve_lite/controller_batch_filter.py research/alphaevolve_lite/controller_batch_artifacts.py research/alphaevolve_lite/controller_sample_eval_policy.py research/alphaevolve_lite/prompt_builder.py research/alphaevolve_lite/skill_library.py research/alphaevolve_lite/reasoning_memory.py research/alphaevolve_lite/diagnostic_analyzer.py research/alphaevolve_lite/controller_population_policy.py research/alphaevolve_lite/tests/test_phase4_hardening.py
python -m unittest research.alphaevolve_lite.tests.test_phase4_hardening
python -m unittest discover research/alphaevolve_lite/tests
```

All passed.

Artifact-derived replay of `controller_attempt017_forced_cell_smoke_20260517/attempt_004`:

```yaml
decision: reject
failure_category: execution_effect_failed
failure_reason: ranked_signal_and_final_weights_unchanged
behavior_delta_pass: true
execution_effect_pass: false
```

## Next Remote Run

Run one controller-only smoke after GitHub sync. The formal handoff is [controller_attempt017_execution_effect_smoke_remote_instructions_20260517.md](controller_attempt017_execution_effect_smoke_remote_instructions_20260517.md).
