---
title: Parent Zoo Cost-Aware Review 20260522
type: project_evidence_review
status: active
updated: 2026-05-22
tags:
  - project
  - phase4
  - parent-zoo
  - controller
  - daily-stock
  - alphaevolve
sources:
  - "parent_zoo_cost_aware_remote_instructions_20260522.md"
  - "seed_zoo_is_os_review_20260522.md"
  - "artifacts/parent_zoo_cost_aware_20260522.zip"
---
# Parent Zoo Cost-Aware Review 20260522

## Artifact

- Local zip: `artifacts/parent_zoo_cost_aware_20260522.zip`
- Remote artifact root: `artifacts/phase4_alphaevolve/parent_zoo_cost_aware_20260522/`
- Stage: controller-only parent-zoo generation
- Model path used: Qwen9B strict patch implementation
- 27B card pass: not present in returned artifact; default parent-zoo cards were used
- Remote hygiene: all three root summaries record clean Git state and `HEAD == origin/main`
- Stop rule respected: no `remote_sample_eval` or full validation was launched in this run

## Mechanical Result

The controller infrastructure is healthy. The run completed three parent-root subprocesses and wrote all expected manifests, summaries, diagnostic cards, reasoning-memory updates, skill updates, prompts, and child programs.

| Root | Attempts | Passes | Sample-eval eligible | Main failures |
| --- | ---: | ---: | ---: | --- |
| `attempt017_isos_repair` | 6 | 1 | 1 | 4 behavioral no-ops, 1 vector-smoke failure |
| `five_day_excess_reversal` | 6 | 4 | 4 | 1 behavioral no-op, 1 vector-smoke failure |
| `vol_norm_five_day_reversal` | 6 | 4 | 3 | 1 behavioral no-op, 1 vector-smoke failure, 1 pass with no final-weight delta |

The important positive result is that the two deterministic seed roots produced more execution-effective children than the already-optimized attempt017 branch. That supports the seed-zoo decision: we should not replace attempt017, but we should use simpler roots to explore cost-aware transformations.

## Candidate Read

Controller pass is not market evidence. The candidates differ sharply in information value.

| Program | Root | Target | Read |
| --- | --- | --- | --- |
| `PROG-20260522-PZOO-00-0005` | `attempt017_isos_repair` | `signal/time_smoothing` | Adds another causal EWM smoothing layer to attempt017. Final book changed, but only modestly. Useful as an incumbent-branch control, not a breakthrough. |
| `PROG-20260522-PZOO-01-0000` | `five_day_excess_reversal` | `portfolio/no_trade_band_or_sparsity` | Adds a fixed 0.02 signal-margin band. It passed but is a `thin_book` candidate with very small portfolio change. Do not prioritize. |
| `PROG-20260522-PZOO-01-0002` | `five_day_excess_reversal` | `signal/time_smoothing` | Replaces fixed rolling five-day excess reversal with an EWM-summed reversal. It has the largest final book effect among eligible children: about 9.17% changed weights, material rank movement, and active-position Jaccard about 0.495. Highest information value for sample eval. |
| `PROG-20260522-PZOO-01-0003` | `five_day_excess_reversal` | `risk/liquidity_scaled_cap` | Liquidity-scaled cap with side renormalization. Names are unchanged and the final-weight change is small. Useful capacity diagnostic, not first sample-eval priority. |
| `PROG-20260522-PZOO-01-0004` | `five_day_excess_reversal` | `signal/regime_aware_reversal` | Causal volatility-state dampener. It is not a true HMM and it used per-name excess-return volatility despite a benchmark-volatility comment, but it is the closest returned regime-style child. Worth sample eval as a regime-proxy diagnostic. |
| `PROG-20260522-PZOO-02-0000` | `vol_norm_five_day_reversal` | `portfolio/no_trade_band_or_sparsity` | Same fixed-margin no-trade-band idea as the five-day root and marked `thin_book`. Do not prioritize. |
| `PROG-20260522-PZOO-02-0002` | `vol_norm_five_day_reversal` | `portfolio/persistence_trade_gate` | Semantically weak: it computes `prior_signal` inside a per-date group, so prior signal is mostly unavailable and the patch degenerates toward a margin band. Do not sample-evaluate as persistence evidence. |
| `PROG-20260522-PZOO-02-0003` | `vol_norm_five_day_reversal` | `risk/liquidity_scaled_cap` | Same liquidity-cap shape as the five-day root, with small final effect. Not first priority. |
| `PROG-20260522-PZOO-02-0004` | `vol_norm_five_day_reversal` | `ranking/rank_transform` | Changed ranked signal but not final weights, so it is correctly ineligible for sample eval. |

Vector-smoke failures are also informative:

- `attempt017` no-trade-band failed on missing `prior_signal`;
- `five_day` robust-centering failed because `Series.mad` is unavailable;
- `vol_norm` time-smoothing failed because `ExponentialMovingWindow.where` is invalid.

These are normal strict-controller rejections, not infrastructure failures.

## Direct Next-Step Read

A direct artifact read says: there are eligible controller children, so run a small data-backed sample evaluation before generating more children.

The best direct candidate is `PROG-20260522-PZOO-01-0002` because it has the largest execution-effective change while staying within the simple five-day reversal family. The second useful direct candidate is `PROG-20260522-PZOO-00-0005`, because it tests whether the incumbent branch can still be improved by smoother signal persistence.

Direct conclusion: run curated `remote_sample_eval` on a small subset, not all eligible children.

## Zoom-Out Diagnosis

At the system level, this run changes the problem statement again.

The earlier stall was not only "Qwen9B cannot invent better ideas." Qwen9B can still produce target-matched, controller-safe children when the root is simple enough. The weak point is mechanism fidelity:

- regime-aware became a per-name volatility dampener, not a market-state or HMM-like regime model;
- persistence gating computed prior signal inside the same date group, so the intended temporal memory was not implemented correctly;
- no-trade-band patches tended to thin the book rather than preserve broad coverage;
- liquidity cap patches changed weights only weakly after side renormalization.

This is an AlphaEvolve design issue: the prompt sampler and evaluator pool need enough semantic pressure that children implement the intended mechanism, not just any syntactically valid patch matching the target label.

Zoom-out conclusion: evaluate the best high-information children now, but before the next generation batch, harden mechanism-specific prompts and smoke checks for persistence and regime logic.

## Final Decision

Do not run another broad controller batch yet.

Run a curated sample-evaluation milestone with exactly these high-information children:

1. `PROG-20260522-PZOO-00-0005`
   - incumbent branch control;
   - tests whether additional causal smoothing helps attempt017 after the IS/OS forward-return repair.
2. `PROG-20260522-PZOO-01-0002`
   - primary candidate;
   - highest controller information value because it materially changes final books while preserving five-day reversal structure.
3. `PROG-20260522-PZOO-01-0004`
   - regime-proxy diagnostic;
   - not a true HMM, but useful evidence on whether volatility-state dampening helps the five-day root.

Do not sample-evaluate the thin-book no-trade-band children, the semantically broken persistence child, the small liquidity-cap children, or the no-final-weight rank transform.

## Promotion Rule For The Curated Sample Eval

No child should be promoted from this sample-eval alone.

A child can become a next controller parent only if it:

- passes the repaired IS/OS sample hard gates;
- improves parent-relative search-sample turnover-aware score at 2.5 bps;
- does not achieve the result by sparse active days or collapsed coverage;
- has tolerable IS behavior, not only OS improvement;
- is metric-distinct from both its direct parent and the attempt017 incumbent;
- has max weight and missing-held weight within current contracts.

If none pass, the next implementation move is not another random batch. It is mechanism-fidelity hardening:

- persistence gate checks must require `prior_signal` to be computed before date-group portfolio construction;
- regime-aware prompts must distinguish market-level causal state variables from per-name volatility dampening;
- no-trade-band cards must include broad-book fallback and active-day coverage constraints;
- larger-model review should produce mechanism pseudocode or cards for regime/persistence before Qwen9B writes patches.

## Sources

- `artifacts/parent_zoo_cost_aware_20260522.zip`
- `parent_zoo_run_manifest.json`
- `parent_zoo_manifest.json`
- `parent_zoo_mechanism_cards.json`
- `controller/<root>/summary.json`
- `controller/<root>/controller_diagnostic_report.json`
- `controller/<root>/attempt_*/micro_filter_result.json`
- `controller/<root>/attempt_*/child_program.py`
