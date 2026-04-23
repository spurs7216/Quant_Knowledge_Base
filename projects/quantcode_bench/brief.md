---
title: QuantCode-Bench Brief
type: project
status: active
updated: 2026-04-23
tags:
  - project
  - benchmark
  - quant
  - llm
  - backtrader
---
# QuantCode-Bench Brief

## Goal

Use QuantCode-Bench to measure whether this vault actually improves strategy-generation performance over time, rather than only making the notes feel richer.

The intended use is longitudinal:

- record a baseline with the current vault
- rerun after meaningful ingest or query-driven learning
- compare results under a stable protocol

## What the benchmark is

[QuantCode-Bench](https://github.com/LimexAILab/QuantCode-Bench) is a benchmark for generating executable algorithmic trading strategies for Backtrader from natural-language task descriptions.

The official README defines a four-stage evaluation pipeline:

1. compilation
2. backtest execution
3. trade generation
4. judge alignment

The benchmark supports two modes:

- single-shot: one attempt only
- agentic: iterative refinement with structured feedback, up to a configured turn limit

## Dataset shape

The repo README and dataset file define a 400-task benchmark.

Current dataset composition:

- sources: Reddit 183, TradingView 100, StackExchange 90, GitHub 19, Synthetic 8
- difficulties: easy 197, medium 116, hard 87
- timeframes: `1d` 211, `5m` 83, `15m` 36, `1h` 35, `1m` 32, `30m` 3

The tasks are not evenly distributed across assets. The dataset is heavily dominated by `AAPL`, with smaller coverage for `SPY`, `BTC-USD`, `GC=F`, `QQQ`, `TSLA`, `EURUSD=X`, and a longer tail of single-name or FX cases.

This matters for interpretation: strong performance on the headline score does not imply equally broad market coverage.

## What the official runner actually tests

The README gives the broad pipeline, but the repo code is more specific than the README suggests.

### Hard prompt contract

`quantcode_bench/generator.py` imposes benchmark-specific rules that are not part of Backtrader itself:

- only `import backtrader as bt`
- no `pandas`, `numpy`, `scipy`, `yfinance`, or other imports in generated code
- class name must be `TradingStrategy(bt.Strategy)`
- required methods: `__init__`, `next`, `notify_order`
- use `self.order`
- use `self.data`, not `self.data0` or multiple feeds
- use only a restricted indicator list:
  - `SMA`
  - `EMA`
  - `RSI`
  - `MACD`
  - `BollingerBands`
  - `Stochastic`
  - `ATR`
  - `CrossOver`

So the benchmark measures at least three things at once:

- quant and trading-logic understanding
- Backtrader API competence
- compliance with the benchmark's own prompt discipline

### Execution wrapper

`quantcode_bench/reward.py` evaluates generated code by:

- cleaning markdown and extra text
- validating basic structure
- wrapping the strategy in a minimal Backtrader script
- loading cached market data via pickle
- feeding data through `bt.feeds.PandasData`
- setting broker cash to `10000`
- setting commission to `0.001`
- adding `TradeAnalyzer`
- running `cerebro.run()`

The backtest counts as successful only if it runs without runtime errors. The trade criterion requires at least one trade:

$$\text{has\_trades} \equiv \text{total\_trades} > 0.$$

The reward is binary per task:

- `1.0` only if compilation, backtest, trade generation, and judge alignment all pass
- `0.0` otherwise

The runner still reports richer summary metrics such as compilation rate, backtest rate, trade rate, and judge pass rate.

### Judge behavior

`quantcode_bench/judge.py` uses an LLM judge and is intentionally lenient. It explicitly allows simplifications when the original task is hard to implement exactly inside the benchmark's restricted Backtrader setting.

That means the judge score is useful, but it is not a mathematically precise correctness proof.

## What Backtrader knowledge matters most here

The benchmark uses Backtrader as the execution substrate, so several framework concepts are load-bearing.

### 1. Lines and index-0 semantics

Backtrader's quickstart explains that data feeds, indicators, and strategies expose lines, and the current value is read at index `0`, with prior values at `-1`, `-2`, and so on.

This is a common source of errors for models that think in pandas terms instead of event-driven bar logic.

### 2. Strategy lifecycle

The official strategy docs define the main lifecycle:

- `__init__` for indicator construction
- `prenext` before minimum period is met
- `nextstart` at transition
- `next` for mature execution
- `stop` at the end

The benchmark specifically requires code that behaves correctly inside `next`, while `notify_order` is needed to manage pending orders cleanly.

### 3. Cerebro orchestration

Backtrader's `Cerebro` object is the engine that gathers data feeds, strategies, analyzers, and broker state, then executes the backtest.

The benchmark wrapper uses the standard pattern:

- create `bt.Cerebro()`
- add the strategy class
- add a `PandasData` feed
- set cash and commission
- run the engine

### 4. Data-feed access

The data-feed docs explain that feeds become available in `self.datas`, with `self.data` and `self.data0` as aliases to the first feed.

The benchmark deliberately narrows this to `self.data` only. So multi-data or multi-timeframe strategy logic from the task text usually has to be simplified into a single-feed implementation.

### 5. Order execution semantics

The strategy docs note that `buy` and `sell` create orders, and in backtesting a market order executes at the next available bar open.

That means task instructions that sound like "buy at close" or "trade intrabar breakout" may not map exactly to the benchmark harness.

## Implication for the knowledge-base study

The benchmark is useful, but the official runner alone does **not** measure the effect of this vault.

Why:

- the stock repo calls an OpenAI-compatible model directly
- the stock generator prompt does not query this vault
- the stock runner has no QMD, no wiki reads, no project memory, and no raw-source lookup

So an unmodified repo run is a **model-and-prompt baseline**, not a **vault-aware Codex baseline**.

For the actual question "does the knowledge base help Codex learn quant knowledge?", the right experiment is:

- keep the repo's execution and scoring logic
- replace the code-generation side with a vault-aware harness
- allow local vault retrieval
- forbid unrelated web lookup during evaluation

That will let future score changes mean something about the knowledge base rather than about external retrieval.

## Sources

- https://github.com/LimexAILab/QuantCode-Bench
- https://raw.githubusercontent.com/LimexAILab/QuantCode-Bench/main/run_single_shot.py
- https://raw.githubusercontent.com/LimexAILab/QuantCode-Bench/main/run_agentic.py
- https://raw.githubusercontent.com/LimexAILab/QuantCode-Bench/main/quantcode_bench/generator.py
- https://raw.githubusercontent.com/LimexAILab/QuantCode-Bench/main/quantcode_bench/reward.py
- https://raw.githubusercontent.com/LimexAILab/QuantCode-Bench/main/quantcode_bench/judge.py
- https://raw.githubusercontent.com/LimexAILab/QuantCode-Bench/main/data/benchmark_tasks_multiframe.json
- https://www.backtrader.com/docu/quickstart/quickstart/
- https://www.backtrader.com/docu/strategy/
- https://www.backtrader.com/docu/datafeed/
- https://www.backtrader.com/docu/cerebro/
