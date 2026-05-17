---
title: Forced Target-Cell Schedule Patch 2026-05-17
type: project
status: active
updated: 2026-05-17
tags:
  - project
  - phase4
  - alphaevolve
  - controller
  - search-control
sources:
  - "controller_attempt017_novelty_smoke_review_20260517.md"
  - "current_state.md"
  - "../../../wiki/methods/AlphaEvolve Lite Quant Search Workflow.md"
---
# Forced Target-Cell Schedule Patch 2026-05-17

## Purpose

The `controller_attempt017_novelty_smoke_20260516` run proved the controller infrastructure but exposed a routing problem: the remote command could force surfaces, not exact behavior cells. The sampler therefore chose absorbed portfolio/risk cells instead of the intended underfilled mechanism cells.

This patch makes exact target cells a first-class controller runner contract.

## Implemented Contract

`run_child_batch.py` now accepts:

```bash
--target-cell-schedule portfolio/liquidity_weighted_sides,risk/liquidity_scaled_cap
```

When supplied, this schedule overrides `--surface-schedule` for target selection. Each item must be an exact `surface/intent` pair from the controller diversity vocabulary. Invalid surfaces or intents fail before model generation.

The batch summary now records:

```yaml
target_cell_schedule_enabled: true
target_cell_schedule:
  - portfolio/liquidity_weighted_sides
  - risk/liquidity_scaled_cap
surface_schedule:
  - portfolio
  - risk
```

Each attempt record now includes:

```yaml
forced_target_cell: portfolio/liquidity_weighted_sides
target_surface: portfolio
target_intent: liquidity_weighted_sides
target_cell_label: portfolio:liquidity_weighted_sides
```

Duplicate retry stays inside the forced cell instead of rerouting to a different intent. Retry artifacts now also surface:

```yaml
duplicate_retry_terminal_decision
duplicate_retry_terminal_failure_category
duplicate_retry_terminal_reason
duplicate_retry_terminal_novelty_decision
```

This preserves the final attempt's original rejection while making the terminal retry diagnosis visible in `summary.json`.

## Files Changed

```yaml
code:
  - research/alphaevolve_lite/controller_batch_state.py
  - research/alphaevolve_lite/scripts/run_child_batch.py
  - research/alphaevolve_lite/controller_batch_artifacts.py
tests:
  - research/alphaevolve_lite/tests/test_phase4_hardening.py
docs:
  - research/alphaevolve_lite/README.md
  - wiki/methods/AlphaEvolve Lite Quant Search Workflow.md
  - projects/quant_research_system/phase4_search_loop/current_state.md
```

## Verification

Local tests:

```powershell
python -m unittest research.alphaevolve_lite.tests.test_phase4_hardening
python -m unittest discover research/alphaevolve_lite/tests
python -m py_compile research/alphaevolve_lite/controller_batch_state.py research/alphaevolve_lite/controller_batch_artifacts.py research/alphaevolve_lite/scripts/run_child_batch.py research/alphaevolve_lite/tests/test_phase4_hardening.py
```

All passed on 2026-05-17.

Local mock runner smoke:

```powershell
python research/alphaevolve_lite/scripts/run_child_batch.py `
  --out-dir C:\Users\g3055\.codex\memories\forced_cell_mock_smoke_20260517 `
  --attempts 3 `
  --surface-schedule signal `
  --target-cell-schedule portfolio/liquidity_weighted_sides,risk/liquidity_scaled_cap `
  --mock-patch-mode no_valid_patch `
  --disable-reasoning-memory `
  --disable-skill-library `
  --no-repair
```

The mock summary confirmed exact forced cells:

| Attempt | Target surface | Target intent | Forced target cell |
| --- | --- | --- | --- |
| `0` | `portfolio` | `liquidity_weighted_sides` | `portfolio/liquidity_weighted_sides` |
| `1` | `risk` | `liquidity_scaled_cap` | `risk/liquidity_scaled_cap` |
| `2` | `portfolio` | `liquidity_weighted_sides` | `portfolio/liquidity_weighted_sides` |

## Next Remote Run After Sync

Run a controller-only forced-cell proof. Do not launch sample evaluation automatically. The formal remote handoff is [controller_attempt017_forced_cell_smoke_remote_instructions_20260517.md](controller_attempt017_forced_cell_smoke_remote_instructions_20260517.md).

```bash
python research/alphaevolve_lite/scripts/run_child_batch.py \
  --program-path artifacts/phase4_alphaevolve/controller_batch_001_diversity_topup/attempt_017/child_program.py \
  --parent-program-id PROG-20260430-CHILD-0017 \
  --evaluator-summary artifacts/phase4_alphaevolve/remote_sample_eval_controller_batch_001_topup_attempt_017_20260509/evaluator_summary.json \
  --out-dir artifacts/phase4_alphaevolve/controller_attempt017_forced_cell_smoke_20260517 \
  --db-path artifacts/phase4_alphaevolve/program_database.sqlite \
  --attempts 6 \
  --target-cell-schedule portfolio/liquidity_weighted_sides,portfolio/persistence_trade_gate,risk/liquidity_scaled_cap,risk/liquidity_scaled_cap,signal/liquidity_adjusted_reversal,signal/liquidity_adjusted_reversal \
  --prior-summary artifacts/phase4_alphaevolve/controller_batch_001/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_batch_001_diversity_topup/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_batch_001_attempt017_repair_20260509/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_evaluator_hardening_smoke_20260510/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_attempt017_focused_round_20260511/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_attempt017_search_control_rerun_20260511/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_attempt017_mechanism_batch_20260513/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_attempt017_mechanism_rerun_20260514/summary.json \
  --prior-summary artifacts/phase4_alphaevolve/controller_attempt017_27b_card_batch_20260514/summary.json \
  --program-id-prefix PROG-20260517-A017-FORCEDCELL \
  --max-tokens 8192
```

Expected artifact checks:

```yaml
target_cell_schedule_enabled: true
target_cell_schedule_matches_command: true
ranking_attempt_count: 0
sample_eval_candidate_count: inspect_after_local_review
remote_sample_eval_launched: false
full_validation_launched: false
test_set_used: false
```
