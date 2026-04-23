---
title: Task 001 Daily Stock Short-Horizon Reversal
type: project
status: draft
updated: 2026-04-23
tags:
  - project
  - task
  - remote-validation
  - daily-stock
  - equity
  - baseline
---
# Task 001 Daily Stock Short-Horizon Reversal

## Objective

Validate the first end-to-end `remote_validation` workflow on the full `daily_stock` warehouse file.

The research target is not to prove a new alpha. The target is to verify that the system can:

- select a real remote dataset from the local catalog
- define an auditable signal without look-ahead
- form a daily equity universe
- run chronological train / validation / test splits
- apply transaction costs
- return a compact artifact bundle
- record a proceed / revise / reject decision

## Dataset

Primary dataset:

```text
/home/b08303004/Desktop/WRDS/data/daily_stock/gago9dveytpx6922.csv
```

Local observability sources:

- [daily_stock dataset note](../../../wiki/datasets/daily_stock.md)
- [catalog inventory](../../../catalog/csv_data_inventory.csv)
- [catalog sample](../../../catalog/samples/daily_stock/gago9dveytpx6922.csv)

Catalog facts:

- rows: `49,651,441`
- columns: `94`
- date coverage: `DlyCalDt = 2000-01-03` to `2025-11-28`
- working grain: `PERMNO` by `DlyCalDt`

Catalog-relative path:

```text
data/daily_stock/gago9dveytpx6922.csv
```

## Required Fields

Required fields:

- `PERMNO`
- `DlyCalDt`
- `DlyRet`
- `DlyRetx`
- `DlyPrc`
- `DlyVol`
- `PrimaryExch`
- `SecurityType`
- `ShareType`
- `TradingStatusFlg`
- `vwretd`
- `sprtrn`

## Baseline Signal

Use a short-horizon reversal signal based on lagged five-day excess return.

For security $i$ and date $t$, define:

$$
r^{x}_{i,t} = r_{i,t} - r^{m}_{t},
$$

where $r_{i,t}$ is `DlyRetx` and $r^{m}_{t}$ is `vwretd`.

The raw signal for decision date $t$ is:

$$
s_{i,t} = - \sum_{k=1}^{5} r^{x}_{i,t-k}.
$$

The minus sign means the strategy buys recent relative losers and shorts recent relative winners.

No value from date $t$ or later may enter $s_{i,t}$.

## Universe

Initial recommended universe:

- `SecurityType == EQTY`
- `ShareType == NS`
- `TradingStatusFlg == A`
- `abs(DlyPrc) > 5`
- `DlyVol > 0`
- non-missing `DlyRetx`
- non-missing `vwretd`
- minimum 60 prior valid return observations for the security before ranking

If any field is not stable enough on the remote file, the remote run should report the issue in `failure_report.md` rather than silently changing the rule.

## Portfolio Construction

Recommended baseline:

- rebalance daily
- rank eligible securities cross-sectionally by $s_{i,t}$
- long top decile
- short bottom decile
- equal weight within long and short books
- target gross exposure: `1.0`
- target net exposure: `0.0`
- one-day holding period

Timing convention:

- compute $s_{i,t}$ after the close of date $t$
- form positions for the next trading day
- earn portfolio return from `DlyRetx` on date $t+1`

If the remote implementation uses a different convention, it must state that convention in `run_manifest.yaml` and explain why it is still non-leaking.

The first implementation may also report a long-only top-decile diagnostic, but the long-short result is the primary baseline.

## Date Splits

Recommended chronological split:

- train: `2000-01-03` to `2012-12-31`
- validation: `2013-01-01` to `2018-12-31`
- test: `2019-01-01` to `2025-11-28`

The signal has no tuned hyperparameters in the first pass. Train exists mainly to verify that the system handles chronological splits consistently.

## Cost Model

Baseline costs:

- commission: `0.5` bps per traded notional
- slippage: `2.0` bps per traded notional
- borrow: `0.0` bps annualized for first pass
- turnover cost applied on both long and short rebalance trades

Also run cost sensitivity:

- `0` bps total cost
- `2.5` bps total cost
- `5.0` bps total cost
- `10.0` bps total cost

## Evaluation Metrics

Required split-level metrics:

- annualized return
- annualized volatility
- Sharpe ratio
- max drawdown
- daily turnover
- mean number of long names
- mean number of short names
- gross exposure
- net exposure
- beta to `vwretd` or `sprtrn`

Required diagnostics:

- date coverage after filters
- monthly universe count
- missing return rate
- duplicate `PERMNO` by `DlyCalDt` count
- performance by subperiod
- performance by `PrimaryExch`
- performance by liquidity bucket
- cost sensitivity table

## Failure Gates

The task fails if:

- the signal uses date $t$ or future returns
- the realized return timing is not explicit
- the universe is empty for material periods
- duplicate `PERMNO` by `DlyCalDt` rows are not handled or reported
- returns contain nonfinite values after portfolio construction
- turnover cost is missing from the cost-adjusted result
- artifact bundle is incomplete
- code snapshot fields are absent from `run_manifest.yaml`

## Decision Rule

This task can produce three acceptable decisions:

- `proceed`: workflow is valid and baseline is worth extending
- `revise`: workflow runs but data, cost, or construction issues require changes
- `reject`: baseline is not useful or the implementation is not trustworthy

The decision is not based on Sharpe alone. Implementation trust and evidence quality matter more in Task 001.

## Expected Artifact Bundle

Required local target after manual review:

```text
artifacts/remote_runs/20260423_task001_daily_stock_short_reversal/
```

Required files:

- `run_manifest.yaml`
- `metrics.json`
- `scorecard.csv`
- `diagnostics.csv`
- `failure_report.md`
- `review.md`

Recommended optional files:

- `subperiod_metrics.csv`
- `cost_sensitivity.csv`
- `universe_counts_by_month.csv`
- `turnover_by_day.csv`
- `plots/equity_curve.png`
- `plots/drawdown.png`

## Sources

- [remote_workflow.md](../remote_workflow.md)
- [environments.md](../environments.md)
- [daily_stock](../../../wiki/datasets/daily_stock.md)
- [catalog/csv_data_inventory.csv](../../../catalog/csv_data_inventory.csv)
- [catalog/samples/daily_stock/gago9dveytpx6922.csv](../../../catalog/samples/daily_stock/gago9dveytpx6922.csv)
