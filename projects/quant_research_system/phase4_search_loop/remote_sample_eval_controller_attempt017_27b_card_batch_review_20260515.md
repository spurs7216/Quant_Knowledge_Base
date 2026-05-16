# Attempt017 27B-Card Batch Sample-Eval Review

Date: 2026-05-15

## Summary

The 27B mechanism-card workflow produced a 9B controller child, `attempt_011`, that was sample-evaluated. The result should not be promoted.

The child is useful as negative search evidence: it preserved some implementation-shape benefits seen in the prior industry-neutral ranking child, but it repeated the same effective mechanism and did not improve parent-relative alpha evidence.

## Main Finding

`attempt_011` was effectively a replay of the prior industry-neutral ranking child:

- prior comparable child: `PROG-20260514-A017-MECHFIX-0009`
- repeated child: `PROG-20260514-A017-27BCARD-0011`
- surface / intent: `ranking/industry_neutral_rank`
- sample behavior: improved turnover, drawdown, breadth, and missing-held diagnostics, but weakened parent-relative return and Sharpe
- critical caveat: sample metrics were equivalent to the prior child under the current sample-eval comparison

This means the controller and evaluator were healthy enough to produce artifacts, but the selection policy spent a sample evaluation on an occupied MAP cell.

## Root Cause

Two contract gaps allowed the repeat:

- Controller sample-eval eligibility knew `map_cell_already_occupied`, but did not require a child to beat and materially differ from the occupied cell's elite before remaining sample-eval eligible.
- Remote sample evaluation compared against the seed/parent reference, but not against prior sample-evaluated sibling summaries.

There was also a prompt-contract gap: 27B mechanism cards could use loose intent or data-field names. That increases the chance that the 9B generator receives a plausible-sounding but underspecified card.

## Implemented Hardening

- Added `controller_sample_eval_policy.py` to own sample-eval candidate eligibility.
- Added occupied-MAP-cell elite comparison before a controller pass can remain sample-eval eligible.
- Added multi-prior sample equivalence checks through `--prior-sample-summary`.
- Added exact mechanism-card validation against allowed surfaces, target intents, and `CONTRACT.*` daily-stock field handles.
- Added a durable negative memory and avoid skill for repeated attempt017 `industry_neutral_rank`.

## Next Remote Rule

Do not sample-evaluate another attempt017 `ranking/industry_neutral_rank` child unless it:

- beats the current occupied MAP-cell elite on controller quality,
- has material behavior-delta distance from that elite,
- is not sample-metric equivalent to prior sibling sample summaries,
- and has a concrete mechanism beyond repeating industry-neutral rank.

The next remote run should be controller-only first. Full validation remains too early.
