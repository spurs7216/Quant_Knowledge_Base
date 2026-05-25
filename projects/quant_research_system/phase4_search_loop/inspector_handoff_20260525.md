---
title: Inspector Handoff 20260525
type: handoff
status: active
updated: 2026-05-25
tags:
  - project
  - phase4
  - handoff
  - inspection
  - alphaevolve
sources:
  - "current_state.md"
  - "alphaagentevo_transfer_20260525.md"
  - "daily_stock_expression_evolution_v1.md"
  - "../../../wiki/methods/AlphaAgentEvo-Style Alpha Evolution for Quant Search.md"
---
# Inspector Handoff 20260525

## Mission For The Inspector

Audit whether the Phase 4 research system still aligns with the stated goal:

> a bounded AlphaEvolve-style daily-stock quant search loop whose generator cannot win by changing data, universe, splits, costs, accounting, or promotion gates.

Please inspect for plan drift, bugs, brittle assumptions, hidden leakage, unsafe generated-code surfaces, weak validation, and documentation/code inconsistencies. Prefer findings with file paths, line references, concrete failure modes, and suggested tests.

Do not start by implementing fixes. First produce an inspection report.

## Read First

Read these in order:

1. `AGENTS.md`
2. `agent/coding_principles.md`
3. `projects/quant_research_system/phase4_search_loop/current_state.md`
4. `projects/quant_research_system/phase4_search_loop/README.md`
5. `projects/quant_research_system/phase4_search_loop/alphaagentevo_transfer_20260525.md`
6. `projects/quant_research_system/phase4_search_loop/daily_stock_expression_evolution_v1.md`
7. `wiki/methods/AlphaAgentEvo-Style Alpha Evolution for Quant Search.md`

Suggested skills for the next agent:

- `zoom-out`: compare implementation against the whole Phase 4 objective.
- `grill-with-docs`: stress-test terminology and plan alignment against project docs.
- `improve-codebase-architecture`: inspect module boundaries and hidden coupling.
- `diagnose`: use only after identifying a concrete bug or failure mode.
- `tdd`: use only if the user asks the inspector to implement fixes.

## Current Phase 4 State

The active loop is daily-stock only:

```yaml
data_scope: daily_stock_only
analysis_window: 2011-01-01_to_2025-12-31
in_sample: 2011-01-01_to_2022-12-31
out_sample: 2023-01-01_to_latest_2025_date
universe: rolling_top500_by_lagged_market_cap
cost_feedback: 2.5_bps default plus cost grid
local_machine: edits, docs, artifact review only
remote_machine: Qwen, controller runs, sample evaluation, CSV warehouse access
```

The prior parent-zoo sample evaluation is reviewed in `remote_sample_eval_pzoo_0_review_20260525.md`. No child was promoted. The main conclusion was that infrastructure is no longer the main blocker; the blocker is semantic alpha construction and cost conversion.

AlphaAgentEvo was then ingested because it is close to our problem. The transfer decision is to add expression-level alpha evolution and trajectory scoring before another broad Python-patch controller batch.

## New Local Implementation To Inspect

New or recently changed implementation files:

- `research/alphaevolve_lite/expression_evolution.py`
- `research/alphaevolve_lite/scripts/export_expression_interface.py`
- `research/alphaevolve_lite/scripts/run_expression_seed_zoo.py`
- `research/alphaevolve_lite/tests/test_expression_evolution.py`
- `research/alphaevolve_lite/README.md`

New or recently changed project/wiki notes:

- `projects/quant_research_system/phase4_search_loop/alphaagentevo_transfer_20260525.md`
- `projects/quant_research_system/phase4_search_loop/daily_stock_expression_evolution_v1.md`
- `projects/quant_research_system/phase4_search_loop/current_state.md`
- `projects/quant_research_system/phase4_search_loop/README.md`
- `wiki/methods/AlphaAgentEvo-Style Alpha Evolution for Quant Search.md`
- `wiki/log.md`

The expression layer currently provides:

- safe daily-stock field aliases over `daily_stock_contract_v1`;
- AST validation rejecting imports, attribute access, subscripts, undefined names, comprehensions, loops, chained comparisons, and non-positive rolling windows;
- causal operators such as rank, zscore, winsorize, industry neutralize, delay, rolling sum/std/rank/beta, safe divide, transforms, and `where`;
- fixed long/short top-bottom quantile portfolio bridge with max-weight and neutral side-gross constraints;
- 24 starter expression seeds;
- expression similarity;
- deterministic trajectory scoring with valid ratio, pass@T, best turn, improvement streak, consistency, and exploration;
- deterministic remote expression seed-zoo evaluator that does not call Qwen.

## Verification Already Run

These passed locally:

```bash
python -m unittest research.alphaevolve_lite.tests.test_expression_evolution
python -m unittest research.alphaevolve_lite.tests.test_seed_zoo
python -B -c "import research.alphaevolve_lite.expression_evolution; import research.alphaevolve_lite.scripts.export_expression_interface; import research.alphaevolve_lite.scripts.run_expression_seed_zoo"
```

Additional smoke checks:

- `export_expression_interface.py` wrote `expression_interface.md` and `expression_seed_library.json` to a temp directory; seed count was 24.
- `run_expression_seed_zoo.py` ran on a synthetic daily-stock CSV through the real loader, static eligibility, rolling universe, IS/OS split, forward-return builder, expression evaluator, and portfolio accounting. A two-seed smoke passed when configured with small synthetic-universe side counts.

Known local caveat: `python -m compileall` hit Windows permission errors writing `.pyc` files under existing `__pycache__` directories. Imports and unit tests passed with `python -B`, so this looks like local bytecode-write hygiene, not a syntax failure.

## Inspection Priorities

### 1. Alignment With AlphaEvolve / AlphaAgentEvo Plan

Check whether the system still has clear equivalents for:

- prompt sampler;
- LLM ensemble;
- evaluator pools;
- program database;
- trajectory records and pass@T diagnostics;
- seed library;
- fixed evaluator contracts.

Confirm that expression evolution is a smaller proposal object, not a bypass around the hardened Python strategy evaluator.

### 2. Data And Leakage Safety

Inspect whether expression operators are truly causal:

- positive `delay` and rolling windows only;
- rolling operations sort by security and date correctly;
- cross-sectional rank/zscore/winsorize use same-date data only;
- `industry_neutralize` does not leak future sector composition;
- `rolling_beta(ret, benchmark_return, window)` uses only past/current rows, not shifted future returns;
- no expression can edit universe, split, cost, path, or forward-return accounting.

### 3. Portfolio And Evaluator Contract

Check that `construct_expression_portfolio`:

- stays dollar-neutral when both sides are active;
- enforces max weight even when quantile side counts are small;
- avoids sparse few-day artifacts;
- aligns signal index to panel index safely;
- handles missing values without silently creating one-sided exposure.

Check that `run_expression_seed_zoo.py` reuses the repaired evaluator path rather than duplicating old broken logic:

- static eligibility before universe;
- lagged rolling top-500 universe;
- forward returns sourced from eligible raw panel, not next-month top-500 membership;
- fixed 2011-2025 IS/OS split;
- cost sensitivity and max-weight reporting.

### 4. Bugs Or Fragile Details Worth Checking

Potential issues noticed during handoff:

- The 24-seed catalog may contain at least one near-duplicate or exact duplicate expression under different labels. Inspect `DEFAULT_EXPRESSION_SEEDS`.
- `run_expression_seed_zoo.py` writes `run_result.json` with an `error` field that is a count, not a failure status. This may confuse artifact readers.
- The seed catalog is intentionally only 24 expressions, below the 50-100 long-run target.
- Trajectory scoring is implemented but not yet connected to the program database, prompt sampler, reasoning memory, or Qwen episode runner.
- No real remote daily-stock run has been completed for the expression seed-zoo evaluator yet.
- The synthetic smoke needed smaller side-count/max-weight settings than production because the synthetic top-N was tiny; production defaults should be judged on rolling top-500.
- The worktree is dirty and contains many unrelated pre-existing files. Do not assume every modified or untracked file belongs to this implementation slice.
- The latest expression-evolution implementation has not been pushed to GitHub unless the user does that after this handoff.

### 5. Security / Robustness

Inspect the expression AST validator for escape paths:

- attribute access;
- imports;
- dunder names;
- function calls through non-name objects;
- keyword argument misuse;
- list/dict/set/comprehension objects;
- string constants;
- boolean `and`/`or` versus vectorized `&`/`|`;
- pathological windows or denominator behavior.

Also inspect remote scripts for path and artifact assumptions. Remote machines should never require local Qwen, broker/TWS state, or hidden credentials.

## Non-Goals For The Inspector

Do not evaluate strategy performance by full validation or final test use.

Do not add new datasets. Dataset additions remain locked by `dataset_admission_policy.md`.

Do not run Qwen locally. The local Windows machine cannot run Qwen due to memory constraints. Any Qwen run belongs on the remote Linux/GPU machine after vLLM is launched and verified.

Do not treat positive OS Sharpe alone as promotion. Phase 4 requires cost, turnover, max weight, coverage, null-relative, and parent-relative interpretation.

## Expected Output From Inspector

Please produce a concise inspection report with:

- high-severity bugs or vulnerabilities first;
- file and line references;
- whether the implementation aligns with the Phase 4 plan;
- whether the next remote action should still be `remote_expression_seed_zoo_eval_v1`;
- any tests or artifacts that should be added before a remote run;
- whether any docs contradict code or current project state.

If no blocking issues are found, say so explicitly and list residual risks.
