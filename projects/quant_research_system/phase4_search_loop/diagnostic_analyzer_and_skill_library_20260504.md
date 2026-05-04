---
title: Phase 4 Diagnostic Analyzer And Skill Library
type: project
status: active
updated: 2026-05-04
tags:
  - project
  - phase4
  - alphaevolve
  - diagnostics
  - skill-library
sources:
  - "dr_rtl_method_transfer_20260504.md"
  - "reasoning_memory_layer_design.md"
  - "../../../wiki/methods/Group-Relative Skill Learning for Alpha Search.md"
---
# Phase 4 Diagnostic Analyzer And Skill Library

## Decision

Dr. RTL's four main contributions should map into Phase 4 as:

1. realistic benchmark setting;
2. multi-agent closed-loop optimizer;
3. group-relative skill learning;
4. explicit skill library.

Before the next remote run, Phase 4 now implements the missing controller-side pieces for points 2 and 4:

- `diagnostic_analyzer.py` is the deterministic analyzer role;
- `skill_library.py` is the explicit pattern -> strategy skill layer;
- `run_child_batch.py` writes diagnostic and skill-update artifacts for every batch;
- `prompt_builder.py` injects relevant diagnostic cards and skill cards into child-generation prompts.

## Diagnostic Analyzer

The diagnostic analyzer is the quant analogue of Dr. RTL's timing-analysis agent. It does not propose patches. It localizes bottlenecks from artifacts:

```text
evaluator_summary.json -> evaluator_diagnostic_report.json/.md
controller summary + attempts -> controller_diagnostic_report.json/.md
```

The first implementation is deterministic. It detects conditions such as:

- missing evaluator context;
- negative net Sharpe;
- cost and turnover fragility;
- high turnover;
- max-weight concentration;
- missing held weight;
- sign-flip baseline beating the parent;
- weak matched-random null delta;
- no controller-pass children;
- patch-format fragility;
- duplicate generation;
- portfolio semantic failures;
- reasoning-only empty Qwen output.

These cards are bottleneck localization, not market-alpha proof.

## Explicit Skill Library

The skill library is separate from both the program database and the ReasoningBank memory layer.

```text
program database: every generated child and result
reasoning memory: compact evidence-linked lessons
skill library: explicit pattern -> strategy rules with confidence and status
```

Skill item schema:

```yaml
skill_id: "skill_..."
skill_name: short label
skill_type: success_strategy | failure_guardrail | repair_pattern | avoid_strategy | diagnostic_rule | model_routing
confidence: high | medium | low | avoid
status: candidate | active | superseded | rejected
pattern: diagnostic or failure pattern
strategy: reusable transformation principle
prompt_rule: compact instruction inserted into prompts
applicability:
  source_stage: controller_static
  data_stage: stage_0_daily_stock
  target_surface: []
evidence:
  support_count:
  failure_count:
  artifact_paths: []
```

Default active skills are conservative controller skills already supported by prior artifacts:

- strict evolve-block SEARCH/REPLACE;
- preserve balanced long and short books;
- avoid one-sided signal-proportional short weights;
- no-thinking Qwen routing for patch calls;
- duplicate retry should change semantic intent.

## Promotion Rule

New `skill_update.json` entries from the next controller batch are candidates only.

Do not automatically promote a skill to active from one controller-static batch. Promotion should require deterministic support, preferably:

- repeated controller-static support across sibling batches; or
- sibling-relative remote sample-evaluator evidence; and
- no conflict with frozen data, cost, split, universe, or portfolio semantic gates.

## Remote Run Artifacts

The next remote controller run should now produce:

```text
evaluator_diagnostic_report.json
evaluator_diagnostic_report.md
controller_diagnostic_report.json
controller_diagnostic_report.md
skill_library_loaded.json
skill_update.json
skill_update.md
reasoning_memory_update.json
reasoning_memory_update.md
```

Review these together:

- `evaluator_diagnostic_report.md`: did the analyzer give the generator the right bottleneck?
- `controller_diagnostic_report.md`: what failed after generation?
- `skill_update.md`: what new skills were proposed, and are they only candidate-level?
- `reasoning_memory_update.md`: what group-relative sibling evidence was recorded?

## Implementation Files

```text
research/alphaevolve_lite/diagnostic_analyzer.py
research/alphaevolve_lite/skill_library.py
research/alphaevolve_lite/prompt_builder.py
research/alphaevolve_lite/scripts/run_child_batch.py
```
