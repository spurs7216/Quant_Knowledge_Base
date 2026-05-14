---
title: Attempt017 Mechanism Design 2026-05-13
type: project
status: active
updated: 2026-05-13
tags:
  - project
  - phase4
  - alphaevolve
  - mechanism-design
  - daily-stock
sources:
  - "daily_stock_contract_v1.md"
  - "dataset_context.md"
  - "controller_attempt017_search_control_rerun_review_20260513.md"
  - "../../artifacts/remote_sample_eval_controller_batch_001.zip"
  - "../../artifacts/controller_batch_001_diversity_topup.zip"
---
# Attempt017 Mechanism Design 2026-05-13

## Purpose

This note turns the attempt017 evidence into concrete daily-stock-only mechanisms before the next remote generation batch.

The goal is not to sample more shallow dampeners. The goal is to give the controller prompt sampler mechanisms that can plausibly affect final weights and parent-relative economics while staying inside the frozen daily-stock contract.

## Evidence Boundary

Attempt017 is the causal EWM smoothing child:

```python
signal = signal / rolling_vol.clip(lower=1e-4)
signal = signal.where(history >= min_history)
signal = signal.ewm(span=max(5, min_history * 2), adjust=False).mean()
```

Its sample evaluation is `sample_review`, not promotion:

```yaml
search_sample_sharpe: 0.44259876228477274
search_sample_annualized_return: 0.05974649689082866
search_sample_turnover: 0.46502555411148977
search_sample_turnover_aware_score: -0.2736576262430996
max_missing_held_weight: 0.11999999999999998
max_weight: 0.010416666666666668
train_sharpe: -0.2089158034905555
validation_sharpe: 1.2750153636421429
```

The parent has a real lead against random long/short baselines, but it is fragile:

- high enough turnover to make the turnover-aware score negative;
- missing-held-weight gate failure at the sample tolerance;
- mixed train/validation behavior;
- subsequent repairs mostly produced generic signal dampening or no final-weight delta.

## Allowed Data

Stage 0 children may use only fields already inside `daily_stock_contract_v1` or verified adjacent daily-stock columns:

```yaml
returns: DlyRet, DlyRetx, vwretd, vwretx, ewretd, ewretx, sprtrn
liquidity: DlyVol, DlyPrcVol, DlyNumTrd, DlyMMCnt
price: DlyPrc, DlyClose, DlyLow, DlyHigh, DlyBid, DlyAsk, DlyOpen
size: DlyCap, ShrOut
groups: SICCD, NAICS, ICBIndustry, PrimaryExch
status_flags: TradingStatusFlg, DlyRetMissFlg, DlyDelFlg
```

Forward-return evaluator fields remain forbidden:

```yaml
forbidden: [fwd_ret, fwd_date, fwd_vwretd, next_market_date, one_day_forward]
```

## Mechanism Candidates

### 1. Liquidity-weighted side weights

Mechanism:

Within each long and short selected tail, replace equal side weights with positive magnitudes based on a bounded combination of signal strength and current-day liquidity or market cap. Normalize each side separately and preserve negative short weights.

Why it is plausible:

- Current attempt017 equal-weights about 100 names, with max weight around 1.04%.
- Missing-held spikes likely concentrate in names whose next-day return coverage is fragile; current-day liquidity, dollar volume, price, and market cap are ex-ante proxies for continuity.
- This changes final weights directly, so it will not be absorbed by ranking.

Controller target:

```yaml
surface: portfolio
intent: liquidity_weighted_sides
required_effect: material final-weight delta
sample_eval_eligibility: target_match_required
```

Caveats:

- Liquidity weighting can reduce breadth and increase concentration.
- Risk controls may cap or partially absorb the edit, so the patch must keep both side-normalization and max-weight discipline explicit.

### 2. Signal-persistence trade gate

Mechanism:

Select long and short tails only when the current ranked signal is supported by prior-day same-sign signal or a large current margin. Fall back to the original tail selection if a side becomes too thin.

Why it is plausible:

- Attempt017 improved by adding causal time smoothing, so persistence appears relevant.
- A same-sign or margin gate can reduce day-to-day churn without using future returns.
- This should change selected names and turnover, not merely raw magnitudes.

Controller target:

```yaml
surface: portfolio
intent: persistence_trade_gate
required_effect: final-weight delta and broad book
sample_eval_eligibility: target_match_required
```

Caveats:

- Too strict a gate can create sparse books or miss fresh reversals.
- The controller should reject patches that collapse active days or one side of the book.

### 3. Industry-neutral ranking

Mechanism:

Cross-sectionally standardize within native industry groups such as `SICCD` with fallback to full-date ranking when a group is too small. Use broad SIC buckets if needed.

Why it is plausible:

- Reversal effects can be partly industry or sector shocks; within-industry ranking reduces unintended sector bets.
- The first-loop dataset already verifies `SICCD`, and schema evidence also lists `NAICS` and `ICBIndustry`.
- This can change selected names while keeping daily-stock-only discipline.

Controller target:

```yaml
surface: ranking
intent: industry_neutral_rank
required_effect: rank delta and preferably final-weight delta
sample_eval_eligibility: target_match_required
```

Caveats:

- Small groups need fallback.
- Industry neutralization may reduce a true cross-industry reversal edge.

### 4. Liquidity-scaled risk cap

Mechanism:

Within the risk block, lower the effective single-name cap for names with low current-day dollar volume or low market cap, then side-renormalize.

Why it is plausible:

- It directly attacks missing-held and implementation fragility through an ex-ante tradability proxy.
- It changes final weights while preserving the existing long/short selection.

Controller target:

```yaml
surface: risk
intent: liquidity_scaled_cap
required_effect: final-weight delta
sample_eval_eligibility: target_match_required
```

Caveats:

- The current parent max weight is already below the default cap. A cap-only edit may be a no-op unless the cap formula bites below current weights.
- This target should be sampled less often than portfolio liquidity weighting unless controller smoke confirms nonzero final-weight delta.

## Rejected Mechanisms For Now

Generic magnitude dampening stays rejected for the attempt017 branch:

```yaml
rejected:
  - bounded_tanh_dampening
  - clipped_magnitude_dampening
  - raw signal shrinkage without final-weight mechanism
```

These have already produced controller-visible deltas without alpha evidence and can harm parent-relative economics.

Forward-return availability filters are also rejected. Missing held weight must be improved through ex-ante daily-stock proxies, not evaluator accounting fields.

## Controller Translation

The local controller vocabulary now includes explicit mechanism targets:

```yaml
new_targets:
  signal:
    - liquidity_adjusted_reversal
  ranking:
    - industry_neutral_rank
  portfolio:
    - liquidity_weighted_sides
    - persistence_trade_gate
  risk:
    - liquidity_scaled_cap
```

The most important next remote candidates are not all equal:

```yaml
priority:
  first:
    - portfolio/liquidity_weighted_sides
    - portfolio/persistence_trade_gate
  second:
    - ranking/industry_neutral_rank
  cautious:
    - risk/liquidity_scaled_cap
  avoid:
    - signal/bounded_tanh_dampening
    - signal/clipped_magnitude_dampening
```

Sample-eval eligibility reporting now requires:

```yaml
required:
  target_intent_match: true
  final_weight_delta: true
  broad_active_book: true
  no_forward_return_fields: true
  not_known_bad_avoid_family: true
```

## Next Step

Run a small remote controller-only mechanism batch after GitHub sync. Do not sample-evaluate automatically; use the new sample-eval eligibility summary first. If no child is target-matched, changes final weights, and avoids known bad dampening families, return only the controller artifact.
