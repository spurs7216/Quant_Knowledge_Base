---
title: Controller Prompt Smoke Repair 2026-05-14
type: project
status: active
updated: 2026-05-14
tags:
  - project
  - phase4
  - alphaevolve
  - controller
  - prompt-contract
  - smoke-test
sources:
  - "controller_attempt017_mechanism_batch_review_20260514.md"
  - "current_state.md"
  - "remote_csv_execution_policy.md"
---
# Controller Prompt Smoke Repair 2026-05-14

## Purpose

Repair the local controller/prompt layer after `controller_attempt017_mechanism_batch_20260513`.

The mechanism batch did not fail because Qwen could not follow SEARCH/REPLACE format. It failed because direct portfolio/risk/ranking mechanisms were underspecified at the surface-local data-access boundary. The prompt told Qwen that daily-stock fields were allowed, but did not tell it which local EVOLVE-block frames actually carried those fields.

## Implemented Repair

### Prompt Builder

`research/alphaevolve_lite/prompt_builder.py` now injects a surface-local data-access contract into child-generation and repair prompts.

Contracts:

```yaml
signal:
  local_frame: "group is a per-security full daily_stock slice"
  valid_extra_field_access:
    - group[CONTRACT.dollar_volume]
    - group[CONTRACT.volume]
    - group[CONTRACT.market_cap]
ranking:
  local_frame: "group contains only date and signal"
  required_extra_field_access:
    - panel.loc[group.index, CONTRACT.industry_primary]
portfolio:
  local_frame: "data/group/valid contain date, security id, and signal only"
  required_extra_field_access:
    - panel.loc[valid.index, CONTRACT.dollar_volume]
    - panel.loc[longs, CONTRACT.dollar_volume]
    - panel.loc[shorts, CONTRACT.dollar_volume]
risk:
  local_frame: "data/group contain date and weight only"
  required_extra_field_access:
    - panel.loc[group.index, CONTRACT.dollar_volume]
    - panel.loc[group.index, CONTRACT.market_cap]
```

The repair prompt also names the failure pattern:

```text
for daily_stock field KeyError failures, replace local-frame field access with panel.loc[...] access aligned to the same index
```

### Negative Sample-Eval Memory

`PARENT_RELATIVE_SEARCH_RULES` now records that `PROG-20260513-A017-MECH-0007` was the best controller sibling but failed parent-relative sample evaluation.

This prevents the prompt from treating signal-side liquidity adjustment as a successful attempt017 repair.

### Smoke Panel

`research/alphaevolve_lite/micro_filter.py` now gives the deterministic controller smoke panel:

- multiple `CONTRACT.industry_primary` values;
- multiple exchanges;
- wider liquidity variation;
- wider market-cap variation.

This makes industry-neutral, liquidity, and cap-shaped mechanisms more observable in controller smoke.

### Reasoning Memory And Skill Library

`research/alphaevolve_lite/reasoning_memory.py` adds active memories for:

- surface-local daily-stock field access;
- failed sample-eval evidence for the controller-best signal liquidity child.

`research/alphaevolve_lite/skill_library.py` adds a high-confidence repair skill:

```text
Use panel.loc for extra daily-stock fields
```

## Remote Git Hygiene

Durable remote-machine hygiene instructions were added to:

- [remote_csv_execution_policy.md](remote_csv_execution_policy.md)
- [../../../agent/operations.md](../../../agent/operations.md)

Policy:

- remote research runs should be reproducible from a GitHub-fetchable commit;
- a clean worktree on an unpushed local commit is not enough for exact reproducibility;
- hygiene-only commits such as ignoring `.codex/` should be pushed before a research run or explicitly recorded as unpushed hygiene-only in the artifact review;
- hygiene commits must not be mixed with research-code edits.

## Verification

Local checks:

```yaml
py_compile:
  - research/alphaevolve_lite/prompt_builder.py
  - research/alphaevolve_lite/micro_filter.py
  - research/alphaevolve_lite/reasoning_memory.py
  - research/alphaevolve_lite/skill_library.py
prompt_checks:
  - child prompt includes surface-local data-access contract
  - portfolio prompt includes panel.loc[valid.index, CONTRACT.dollar_volume]
  - repair prompt includes daily_stock field KeyError guidance
smoke_panel_checks:
  - multiple industries
  - multiple exchanges
  - dollar-volume heterogeneity
  - market-cap heterogeneity
memory_skill_checks:
  - surface-local field-access memory is retrievable
  - panel.loc repair skill is retrievable
micro_filter_check:
  - corrected portfolio liquidity patch no longer fails with DlyPrcVol vector-smoke KeyError
git_diff_check: passed
```

## Next Step

After GitHub sync, run one small controller-only mechanism rerun focused on direct mechanisms:

```yaml
preferred_targets:
  - portfolio/liquidity_weighted_sides
  - portfolio/persistence_trade_gate
  - risk/liquidity_scaled_cap
  - ranking/industry_neutral_rank
sample_eval_limit: 0_or_1
full_validation: false
test_set_used: false
```

Sample-evaluate only a controller-pass child that is target-matched, broad, has final-weight delta, and is a direct portfolio/risk/ranking mechanism rather than another signal-side liquidity adjustment.
