---
title: daily_stock Forward Coverage Review 2026-05-19
type: project
status: reviewed
updated: 2026-05-19
tags:
  - project
  - phase4
  - daily-stock
  - data-exploration
  - forward-coverage
sources:
  - "../../../artifacts/daily_stock_forward_coverage_20260518.zip"
  - "daily_stock_forward_coverage_remote_instructions_20260518.md"
  - "daily_stock_data_understanding_plan_20260518.md"
  - "notebooks/daily_stock_forward_coverage_20260518_report_executed.ipynb"
---
# daily_stock Forward Coverage Review 2026-05-19

## Purpose

Review the remote `daily_stock` forward-coverage diagnostic before resuming Phase 4 child generation.

The two questions were:

1. What is rolling top-500 stock coverage over the whole available timeline?
2. Why can evaluator-held weights miss next-day returns in the 2018-2020 smoke/debug window?

This artifact is data-understanding evidence. It is not alpha evidence and does not promote any child.

Split-policy caveat: after this review, Phase 4 moved alpha-evolution evidence to the fixed 2011-2025 IS/OS window. The whole-timeline top-500 coverage facts remain active. The 2018-2020 forward-availability figures remain a diagnostic explanation of the evaluator construction issue, but the forward-availability diagnostic should be rerun on the active IS/OS window before the next data-backed child evaluation.

## Artifact Integrity

Artifact:

```text
artifacts/daily_stock_forward_coverage_20260518.zip
```

Main files inspected:

- `forward_coverage_summary.json`
- `top500_daily_coverage.csv`
- `top500_monthly_coverage.csv`
- `top500_membership_churn.csv`
- `top500_permno_coverage.csv`
- `forward_availability_by_date.csv`
- `forward_availability_by_bucket.csv`
- `forward_availability_by_industry.csv`
- `forward_availability_by_exchange.csv`
- `held_availability_prompt_cards.md`

The run scanned the full file:

- rows scanned: 49,651,441
- `max_input_rows`: null
- raw trading dates: 6,517
- eligible trading dates: 6,517
- schema version: `daily_stock_forward_coverage_v1`

## Whole-Timeline Top-500 Coverage

The rolling top-500 universe is very well covered over the full available timeline.

Summary:

- monthly top-500 universes: 310
- top-500 membership rows: 155,000
- distinct top-500 `PERMNO`: 1,675
- daily coverage rows: 6,497
- median daily observed selected names: 500
- median daily coverage rate: 1.000
- mean daily coverage rate: 0.99842
- 1st percentile daily coverage rate: 0.992
- minimum daily coverage rate: 0.986, or 493 observed names out of 500

The 6,497 daily coverage rows are fewer than the 6,517 eligible trading dates because the first calendar month has no prior-month formation date. This is a method implication of the lagged monthly universe rule, not a raw data failure.

Worst daily coverage dates are still mild. The minimum observed count is 493 names, appearing in late June 2000 and late October 2007. The worst month is July 2000, with 9,914 observed rows out of 10,000 expected rows, for monthly coverage 0.9914.

Interpretation: broad top-500 coverage is strong enough for daily long/short evaluation. Sparse few-day portfolios remain strategy/evaluator artifacts, not a top-500 data-coverage limitation.

## Membership Churn

Rolling top-500 membership churn is material but normally moderate.

Summary:

- median month-to-month Jaccard: 0.953125
- median monthly entries: 12
- maximum monthly entries: 49
- minimum month-to-month Jaccard: 0.821494

Worst churn months:

- March 2000: 49 entries, 49 exits, Jaccard 0.821494
- April 2000: 43 entries, 43 exits, Jaccard 0.841621
- November 2008: 37 entries, 37 exits, Jaccard 0.862197
- May 2009: 34 entries, 34 exits, Jaccard 0.872659
- April 2020: 27 entries, 27 exits, Jaccard 0.897533

Interpretation: turnover metrics must separate strategy turnover from exogenous monthly universe turnover. Crisis and early-sample months can have large membership changes.

## Forward-Return Availability

The raw forward-availability rate in the 2018-2020 smoke window is high:

- forward rows: 377,592
- available rows: 376,668
- unavailable rows: 924
- raw availability rate: 0.997553
- date count: 756
- distinct `PERMNO`: 689

Unavailable causes:

| Cause | Count | Interpretation |
| --- | ---: | --- |
| `final_visible_market_date` | 500 | mechanical end-of-window boundary |
| `security_not_observed_next_market_date` | 235 | next row for the security skips the next visible market date |
| `no_next_security_row` | 189 | no later row exists for the security in the filtered panel |
| `missing_forward_return` | 0 | no direct missing-return rows survive the fixed eligibility filter |

After excluding the mechanical final visible date, the non-final availability rate is:

```text
376,668 / 377,092 = 0.998876
```

There are 424 non-final unavailable rows. Of these, 392 occur on month-end dates inside the evaluator panel. Only 32 occur away from month-end.

Interpretation: the missing-held issue is not primarily broad raw missingness. It is concentrated at monthly universe transitions.

## Concentration Diagnostics

The strongest concentration is next-month membership exit.

Adjusted for the final visible date:

- names that do not continue into next-month membership: 419 non-final unavailable rows out of 8,778 rows, adjusted availability 0.952267
- names that continue into next-month membership: 5 non-final unavailable rows out of 368,314 rows, adjusted availability about 0.999986

The bottom market-cap quintile is also concentrated:

- bottom market-cap quintile: 396 non-final unavailable rows, adjusted availability 0.994736
- bottom dollar-volume quintile: 227 non-final unavailable rows, adjusted availability 0.996983
- bottom price quintile: 186 non-final unavailable rows, adjusted availability 0.997527

Exchange differences are small after excluding the final boundary:

- NASDAQ (`Q`): adjusted availability 0.998687
- NYSE (`N`): adjusted availability 0.998951
- AMEX (`A`): adjusted availability 1.000000, but only 756 rows

The worst SIC2 availability rates are in tiny groups, such as SIC2 82 and 83 with only 21 and 42 rows. Larger SIC2 groups generally have adjusted availability above 0.995. This is not strong evidence for an industry-specific raw data problem.

## Main Diagnosis

The evidence points to an evaluator construction issue:

1. The signal-date universe is rolling monthly top-500.
2. The evaluator currently builds forward returns on the already-filtered `universe_panel`.
3. If a security is in the top-500 on the last day of month \(m\), but exits the top-500 in month \(m+1\), its next-day row is absent from `universe_panel`.
4. `build_forward_returns` then treats the held name as missing, even though the raw eligible data may have its next-day return.

This is not a strategy feature the child should learn from. It is a timing and universe-membership contract in the evaluator.

The correct research contract should be:

- membership at date \(t\) determines which names can receive signal-date weights;
- next-day return availability should be attached from the eligible raw panel for those date-\(t\) holdings, even if the name leaves the top-500 at \(t+1\);
- generated child strategies must still not use evaluator-only fields such as `fwd_ret`, `fwd_date`, `next_market_date`, or `one_day_forward`.

## Implications For Phase 4

Do not resume child generation yet.

The next step should be an evaluator-forward-return repair, then a seed/attempt017 re-evaluation:

1. compute one-day-forward returns before or alongside monthly-universe filtering, using the eligible raw panel;
2. keep the signal-date panel restricted to rolling top-500 membership;
3. preserve next-day returns for current holdings even if the name exits next month;
4. handle the final visible date by either loading one extra forward trading day or dropping the final signal date from return evaluation;
5. rerun the seed and attempt017-family sample evaluations to measure how much missing-held weight was evaluator-induced.

Only after this repair should prompt cards about missing-held risk be promoted into child-generation context.

## What To Promote Now

Promote as durable data facts:

- whole-timeline rolling top-500 coverage is very high, with median daily count 500 and minimum observed count 493;
- rolling universe membership churn is real and should be separated from strategy turnover;
- historical 2018-2020 smoke-window forward-return unavailability is mostly a boundary or month-end universe-transition effect;
- `missing_forward_return` is not observed after fixed eligibility filtering in this diagnostic;
- low market-cap / low liquidity names are the main cross-sectional concentration for non-final unavailability, but the mechanism is largely membership exit.

Do not promote as alpha guidance:

- do not tell child strategies to predict or use next-month membership directly;
- do not use `fwd_ret`, `fwd_date`, `next_market_date`, or `one_day_forward` in child strategies;
- do not treat missing-held reduction alone as alpha evidence until the evaluator contract is repaired.

## Further Exploration Needed

After evaluator repair:

- compare old versus repaired missing-held diagnostics for the seed, attempt017, attempt009, and recent execution-effect candidates;
- report how much `max_missing_held_weight` drops when next-day returns are sourced from the eligible panel;
- check whether month-end returns introduce any unintended lookahead or survivorship problem;
- verify that final-date handling is consistent across in-sample, out-sample, and search-sample metrics;
- only then decide whether child prompts should include liquidity/size rules for residual raw missingness.

## Related Outputs

- [notebooks/daily_stock_forward_coverage_20260518_report.ipynb](notebooks/daily_stock_forward_coverage_20260518_report.ipynb)
- [notebooks/daily_stock_forward_coverage_20260518_report_executed.ipynb](notebooks/daily_stock_forward_coverage_20260518_report_executed.ipynb)
- [notebooks/daily_stock_forward_coverage_20260518_report.html](notebooks/daily_stock_forward_coverage_20260518_report.html)
