---
title: Controller Batch 001 Curated Remote Sample Eval Review 2026-05-09
type: project
status: active
updated: 2026-05-09
tags:
  - phase4
  - alphaevolve
  - remote-sample-eval
  - evaluator
sources:
  - "../../../artifacts/remote_sample_eval_controller_batch_001.zip"
  - "controller_batch_001_curated_sample_eval_remote_instructions_20260509.md"
  - "current_state.md"
---

# Controller Batch 001 Curated Remote Sample Eval Review 2026-05-09

## Decision

The first curated data-backed child evaluation did not produce a promote-ready child. It did produce useful evaluator and generator lessons.

Treat `attempt_017` as the only useful structural lead, not as a passed strategy. It improves broad-sample Sharpe versus the seed, but it failed the missing-held-weight sample tolerance and has mixed train/validation behavior.

Do not promote `attempt_000`, `attempt_004`, `attempt_010`, or `attempt_011`.

## Evidence Summary

| Program | Decision | Portfolio days | Search Sharpe | Turnover-aware score | Main read |
| --- | ---: | ---: | ---: | ---: | --- |
| seed reference | `sample_pass` | 581 | -1.2615 | -1.9591 | Infrastructure baseline only; not alpha evidence. |
| attempt_000 | `sample_pass` under old gates | 3 | 17.9110 | 17.4160 | Sparse coverage artifact. The evaluator should not let this remain `sample_pass`. |
| attempt_004 | `sample_pass` | 581 | -1.2615 | -1.9591 | Metric-identical to seed. |
| attempt_010 | `sample_pass` | 581 | -1.2615 | -1.9591 | Metric-identical to seed within numerical tolerance. |
| attempt_011 | `sample_pass` | 581 | -1.2615 | -1.9591 | Metric-identical to seed. |
| attempt_017 | `sample_review` | 581 | 0.4426 | -0.2737 | Broad-coverage causal smoothing lead; failed missing-held-weight gate at 0.12. |

`attempt_017` also reduced turnover materially versus the seed, from about `1.79` to `0.47`, and improved the 2.5 bps net Sharpe from about `-1.26` to `0.44`. Its cost sensitivity is still fragile: at 10 bps its Sharpe falls below zero. Its train split is negative while validation is positive, so this is not robust market evidence.

## Lessons

- A high Sharpe over only a few active days is a coverage artifact. `remote_sample_eval` needs an active portfolio-day coverage gate, not just `portfolio_nonempty`.
- Metric-equivalent children are not useful improvements. A code change can be monotone-invariant or absorbed by selection/risk controls and still produce identical reported metrics.
- Causal signal smoothing is the first useful direction from this curated sample, but it must be repaired with missing-held-weight control and checked for train/validation stability.
- The curated subset was the right size for a first data-backed probe. Evaluating all 48 controller-static children would have wasted remote cycles before the evaluator encoded the two new lessons above.

## Local Follow-Up Patch

The local scaffold now adds:

- `remote_sample_eval.py` hard gates for minimum active portfolio days and minimum active portfolio-day coverage;
- optional reference-summary comparison so metric-equivalent children become `sample_review`;
- controller-static rejection for generated replacements that use evaluator-only forward-return availability fields;
- evaluator diagnostic cards for sparse coverage and metric equivalence;
- prompt, reasoning-memory, and skill-library lessons that discourage sparse few-day and functionally neutral children.

## Next Step

After syncing the patch, rerun only a small focused remote loop. The next generation should use `attempt_017` as a structural lead or prompt inspiration, with the target objective:

```yaml
goal: "retain broad-coverage causal smoothing improvement while fixing missing-held-weight exposure"
blocked_actions:
  - promote attempt_017 directly
  - evaluate all controller-static children blindly
  - use test split
required_evidence:
  - sample_coverage portfolio_day_coverage passes
  - not_metric_equivalent_to_reference passes
  - max_missing_held_weight returns inside sample tolerance
  - turnover-aware score improves versus seed
  - train and validation splits are both inspected
```

If that focused loop yields one or two broad-coverage, non-equivalent children with acceptable missing-held weight, then run a slightly wider sample-eval comparison against seed, attempt_017, sign-flip, and matched random baselines.
