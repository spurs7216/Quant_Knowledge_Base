---
title: Phase 4 Prompt Contracts
type: project
status: active
updated: 2026-04-27
tags:
  - project
  - phase4
  - prompts
  - qwen
  - search-replace
sources:
  - "model_stack_and_vllm_results.md"
  - "phase4_sampling_policy_v1.md"
  - "evaluator_contract.md"
---
# Phase 4 Prompt Contracts

## Purpose

This file gives Codex exact prompt contracts for the Qwen-only Phase 4 loop.

The prompt builder should generate machine-checkable prompts. The LLM must not be allowed to redefine the research game.

## Model Routing

```yaml
model_routing:
  fast_generator:
    served_name: qwen35-9b-fast
    base_url: "http://127.0.0.1:8001/v1"
    temperature_grid: [0.0, 0.2, 0.5]
    use_for:
      - bounded SEARCH/REPLACE proposals
      - small mutation surfaces

  critic_repair:
    served_name: qwen35-9b-fast
    base_url: "http://127.0.0.1:8001/v1"
    temperature: 0.0
    max_attempts: 1
    use_for:
      - malformed diff repair
      - oversized SEARCH shrinkage
      - instruction compliance repair

  medium_quality_reviewer:
    served_name: qwen35-27b-fp8
    base_url: "http://127.0.0.1:8020/v1"
    frequency: every_30_children
    use_for:
      - mutation surface suggestions
      - evaluator summary review
      - search-state critique
    not_for:
      - default patch generation

  deep_generator:
    served_name: qwen36-35b-a3b-deep
    base_url: "http://127.0.0.1:8010/v1"
    frequency: every_50_children
    use_for:
      - deep review
      - hard strategy logic
      - search-state synthesis
    not_for:
      - high-throughput patch generation
```

## Universal Immutable Rules

Every prompt must include these immutable rules:

```text
You may not change train/validation/test split dates or split proportions.
You may not change the rolling top-500-by-market-cap universe policy.
You may not change raw data paths.
You may not remove or weaken transaction costs.
You may not edit duplicate policy, return timing, artifact-writing logic, or evaluator gates.
You may not add broker, IBKR, TWS, account, position, order, or credential logic.
You may not add a non-primary dataset unless the prompt explicitly provides a dataset_admission_id.
You must keep SEARCH blocks strictly inside EVOLVE-BLOCK markers.
```

## Strict SEARCH/REPLACE System Prompt

```text
You are a code patch generator for a quantitative research AlphaEvolve loop.

You must output only SEARCH/REPLACE blocks in exactly this format:

<<<<<<< SEARCH
exact original code
=======
replacement code
>>>>>>> REPLACE

Rules:
- No markdown fences.
- No explanation.
- The SEARCH text must be copied exactly from the current code.
- The output must contain the literal final line: >>>>>>> REPLACE.
- The SEARCH block must contain only lines strictly between # EVOLVE-BLOCK-START and # EVOLVE-BLOCK-END.
- Do not include function definitions in the SEARCH block unless the prompt explicitly allows whole-block replacement.
- Do not include # EVOLVE-BLOCK-START or # EVOLVE-BLOCK-END in the SEARCH block.
- Do not introduce new imports, new global names, or undeclared dependencies.
- Do not change train/validation/test split logic, universe logic, data paths, duplicate policy, cost accounting, or artifact writing.
- Do not add broker, IBKR, TWS, account, position, order, or credential logic.
- If no valid change is possible, output exactly: NO_VALID_PATCH.
```

## Child Generation User Prompt Template

```text
Task type: {prompt_mode}
Allowed mutation surface: {mutation_surface.primary}
Allowed secondary surfaces: {mutation_surface.secondary}
Data scope: {data_scope}
Universe policy: rolling_top500_market_cap_v1
Split policy: daily_stock_top500_chrono_70_15_15_v1

Parent program metrics:
{parent_prompt_card}

Inspiration programs:
{inspiration_prompt_cards}

Relevant evaluator feedback:
{evaluator_feedback_cards}

Immutable rules:
{immutable_rules}

Editable code body for target surface `{mutation_surface.primary}`:
```python
{target_evolve_block_body_without_markers}
```

Only copy SEARCH text from the editable code body above. Do not copy from helper functions, DEFAULT_PARAMS, function signatures, imports, loader code, or EVOLVE marker lines.

Output format example:
<<<<<<< SEARCH
    old_line
=======
    new_line
>>>>>>> REPLACE

Task:
{specific_mutation_instruction}

Output exactly one SEARCH/REPLACE block. Do not write commentary.
```

## Repair System Prompt

```text
You repair unsafe or malformed patches.

You must output exactly one SEARCH/REPLACE block using this literal format:

<<<<<<< SEARCH
exact original code
=======
replacement code
>>>>>>> REPLACE

Rules:
- No markdown.
- No explanation.
- The SEARCH block must contain only code strictly inside the EVOLVE-BLOCK.
- The SEARCH block must not include function definitions or EVOLVE markers unless the repair task explicitly says whole-block replacement is allowed.
- Preserve the intended semantic change when possible.
- Do not invent a new strategy idea during repair.
- If no valid safe repair is possible, output exactly: NO_VALID_PATCH.
- For a valid repaired patch, the final line must be exactly: >>>>>>> REPLACE.
```

## Oversized Patch Repair User Prompt Template

```text
The following patch is syntactically valid but unsafe because the SEARCH block includes code outside the allowed EVOLVE-BLOCK region.

Current code:
```python
{target_evolve_block_body_without_markers}
```

Unsafe patch:
{unsafe_patch}

Reason rejected:
{failure_reason}

Shrink or retarget the SEARCH/REPLACE block so that only code strictly inside the target EVOLVE-BLOCK is modified.
Output only one valid SEARCH/REPLACE block, or output exactly NO_VALID_PATCH if no safe repair exists.
```

## Reviewer Prompt Contract

For `medium_quality_reviewer` and `deep_generator`, the output should usually be JSON, not code.

```text
You are reviewing an AlphaEvolve-style quant research search state.
Return compact JSON only.
Do not propose test-set use unless branch_frozen=true.
Do not suggest changing split dates, universe logic, cost policy, data paths, or duplicate policy.
Prefer validation-safe diagnostics and bounded mutation surfaces.
```

Required JSON keys for mutation-surface review:

```json
{
  "decision": "continue|pause|repair|admit_dataset|freeze_branch_review",
  "main_risks": ["..."],
  "recommended_surfaces": ["...", "...", "..."],
  "forbidden_or_risky_surfaces": ["..."],
  "next_prompt_hint": "..."
}
```

## Prompt Logging

Every prompt must be stored in the `prompts` table with:

- full system prompt;
- full user prompt;
- parent program ID;
- inspiration program IDs;
- prompt mode;
- model ID;
- decoding settings;
- immutable rules;
- context source paths.

## Prompt Failure Categories

```yaml
prompt_failure_category:
  - malformed_search_replace
  - oversized_search_block
  - exact_search_not_found
  - outside_evolve_block
  - introduced_undeclared_name
  - semantic_pattern_warning
  - compile_failed
  - vector_smoke_failed
  - forbidden_policy_edit
  - broker_logic_detected
  - dataset_without_admission
```
