---
title: Phase 4 daily_stock Contract v1
type: project
status: active
updated: 2026-04-30
tags: [phase4, alphaevolve, daily-stock, contract, schema]
sources:
  - "remote_evidence_review_20260430.md"
  - "remote_csv_execution_policy.md"
  - "universe_and_split_policy.md"
---

# Phase 4 daily_stock Contract v1

## Evidence

This contract is frozen from the remote `schema_evidence_v2` bundle:

```text
artifacts/schema_evidence_v2/daily_stock_schema_report.json
artifacts/schema_evidence_v2/daily_stock_field_mapping.yaml
```

The evidence sampled 50,000 rows from:

```text
/home/b08303004/Desktop/WRDS/data/daily_stock/gago9dveytpx6922.csv
```

The sample confirmed 94 columns, no schema warnings, and date coverage from `2000-01-03` through `2025-11-28`.

Important limitation: the 50,000-row sample had only 16 unique `PERMNO`s, so the CSV appears sorted by security then date. This evidence freezes field names and basic diagnostics, not full cross-sectional universe distribution. Remote sample evaluation must use chunked date-window loading, not first-N-row sampling, when cross-sectional coverage matters.

## Frozen Field Mapping

```yaml
contract_id: daily_stock_contract_v1
date: DlyCalDt
security_id: PERMNO
issuer_id: PERMCO
total_return: DlyRet
ex_dividend_return: DlyRetx
price: DlyPrc
volume: DlyVol
dollar_volume: DlyPrcVol
market_cap: DlyCap
shares_outstanding: ShrOut
exchange: PrimaryExch
security_type: SecurityType
share_type: ShareType
trading_status: TradingStatusFlg
conditional_type: ConditionalType
us_incorporated: USIncFlg
industry_primary: SICCD
benchmark_return_primary: vwretd
benchmark_return_secondary: sprtrn
```

## Fixed Eligibility Filter

The non-evolvable loader/universe layer applies:

```yaml
USIncFlg: Y
SecurityType: EQTY
ShareType: NS
TradingStatusFlg: A
ConditionalType: RW
PrimaryExch: [A, N, Q]
abs(DlyPrc): > 0
DlyCap: > 0
DlyVol: > 0 for tradability
DlyRetx: nonmissing for PnL
```

Candidate programs may consume the filtered panel and universe membership, but may not change these filters.

## Universe Variable

Use verified `DlyCap` as the primary market-cap field for rolling top-500 formation. `ShrOut` remains available as an audit/fallback field, but a fallback from `abs(DlyPrc) * ShrOut` requires a manifest change and must not be introduced by generated children.

## Return Timing

For signal date `t`:

- compute signals using information available at or before `t`;
- form positions after signal date `t`;
- earn `DlyRetx` on the next global trading date only;
- report missing held weight if a held name lacks a valid next-date return;
- do not forward-fill returns;
- do not silently renormalize surviving names.

## Implementation

Code contract:

```text
research/alphaevolve_lite/daily_stock_contract.py
research/alphaevolve_lite/daily_stock_loader.py
research/alphaevolve_lite/splits.py
research/alphaevolve_lite/universe.py
```

First seed program:

```text
research/alphaevolve_lite/seeds/kalman_reversal_seed.py
```

Remote sample evaluator:

```text
research/alphaevolve_lite/scripts/remote_sample_eval.py
```

Run on the remote machine, not local Windows:

```bash
python research/alphaevolve_lite/scripts/remote_sample_eval.py \
  --csv-path /home/b08303004/Desktop/WRDS/data/daily_stock/gago9dveytpx6922.csv \
  --out-dir artifacts/phase4_alphaevolve/remote_sample_eval_seed_v1 \
  --db-path artifacts/phase4_alphaevolve/program_database.sqlite \
  --start-date 2018-01-01 \
  --end-date 2020-12-31
```

Do not start Qwen child generation until this remote sample-eval artifact is reviewed.
