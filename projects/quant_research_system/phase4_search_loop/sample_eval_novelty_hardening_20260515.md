# Sample-Eval Novelty Hardening

Date: 2026-05-15

## Purpose

Prevent the Phase 4 loop from spending expensive remote sample evaluations on controller-safe children that are already represented by an occupied MAP cell or by a prior sample-evaluated sibling.

## Design

The hardening is split across four modules:

- `controller_sample_eval_policy.py` owns the controller-to-sample-eval candidate policy.
- `controller_batch_state.py` seeds occupied MAP-cell elite records from prior controller summaries.
- `sample_eval_metrics.py` owns metric-equivalence comparison against one or more prior sample summaries.
- `mechanism_cards.py` owns the exact mechanism-card vocabulary for surfaces, intents, and daily-stock field handles.

This keeps orchestration scripts thin: `run_child_batch.py`, `remote_sample_eval.py`, and `build_mechanism_cards.py` call these contracts instead of duplicating policy strings.

## Candidate Eligibility V2

A controller pass is not sample-eval eligible when:

- it is not target-intent matched,
- it has no final-weight delta,
- it is too sparse or has thin long/short books in controller smoke,
- it uses forward-return evaluator fields,
- or it lands in an occupied MAP cell without beating and materially differing from the cell elite.

The occupied-cell comparison uses controller search score and behavior-delta distance. It is not an alpha claim; it is only a budget gate.

Known-bad attempt017 families remain prompt memory and review context. They are not a hard sample-eval eligibility rule for the next controller-only novelty smoke.

## Prior-Sample Equivalence

`remote_sample_eval.py` now accepts repeated `--prior-sample-summary` arguments. When supplied, the evaluator adds:

- `prior_sample_comparison`
- `not_metric_equivalent_to_prior_sample`
- equivalent prior program ids in the review and evaluator summary

This catches sibling replay even when the child is not equivalent to the seed or parent.

## Mechanism-Card Contract

Mechanism cards must use exact:

- surfaces from `DIVERSITY_TARGETS`
- intents from the selected surface's target vocabulary
- data fields from `CONTRACT.*` handles or local strategy artifacts such as `signal`

Loose fields such as `industry_code`, `avg_daily_volume`, `returns_1d`, and `signal_raw` are invalid.

## Negative Memory

The attempt017 `industry_neutral_rank` repeat is now active negative memory and an avoid skill. This is not a permanent ban on industry neutralization. It is a guard against repeating the same attempt017 mechanism after two sample-evaluated siblings showed no parent-relative promotion evidence.

## Verification

Local verification:

```powershell
python -m unittest research.alphaevolve_lite.tests.test_phase4_hardening
python -m py_compile research/alphaevolve_lite/controller_sample_eval_policy.py research/alphaevolve_lite/scripts/run_child_batch.py research/alphaevolve_lite/sample_eval_metrics.py research/alphaevolve_lite/scripts/remote_sample_eval.py research/alphaevolve_lite/mechanism_cards.py research/alphaevolve_lite/scripts/build_mechanism_cards.py
```

Both checks passed locally on 2026-05-15.
