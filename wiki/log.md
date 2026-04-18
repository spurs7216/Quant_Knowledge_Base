---
title: Wiki Log
type: log
status: active
updated: 2026-04-19
tags:
  - log
  - wiki
---
# Wiki Log

## 2026-04-18 | init | wiki scaffolding

- Added `glossary.md`, the original research-map note now evolved into `maps/reading_map.md`, and `inbox.md` as the baseline navigation notes.
- Created lightweight note templates under `wiki/_templates/`.
- Added empty topical folders for future source, method, factor, model, strategy, market, risk, and system notes.
- Added `AGENTS.md` at the vault root so Codex reads `agent.md` as the primary schema.

## 2026-04-18 | ingest | llm knowledge base sources

- Added source notes for the Karpathy thread, the `llm-wiki` gist, the Atlan enterprise guide, and the Obsidian spaced-repetition plugin documentation.
- Added [[LLM Knowledge Base Workflow]] as the first system-level synthesis note for how this vault should operate.

## 2026-04-18 | ingest | econometrics and derivatives sources

- Added source notes for Hull, Hansen, Brooks, and Wooldridge.
- Added [[Panel Data]] as the first reusable econometrics method note.
- Added [[Derivatives Markets]] as the first reusable market note tied to the options and Treasury datasets.

## 2026-04-18 | ingest | dataset expansion

- Added dataset notes for `ownership_13F`, `option_volumne`, `Treasurey_Daily_Time_Series`, and `Treasurey_Term_structure`.
- Recorded important mirror caveats, including sample-versus-full coverage mismatches and legacy path spellings that should be preserved.

## 2026-04-18 | schema | deep ingest rule

- Updated `agent.md` and `AGENTS.md` to require chapter-by-chapter ingest for chaptered raw resources and section-by-section ingest for long markdown resources.
- Updated the source-note template so future source notes preserve ingest depth explicitly.

## 2026-04-18 | ingest | chapter-by-chapter source re-ingest

- Reworked the LLM knowledge-base sources into section-by-section notes instead of top-level stubs.
- Reworked the Hull, Hansen, Brooks, and Wooldridge notes into chapter-by-chapter source digests.
- Updated [[LLM Knowledge Base Workflow]] so the ingest-depth rule is part of the vault's operating doctrine.
- Expanded [[Panel Data]] and [[Derivatives Markets]] so the deeper source pass also changed the reusable concept layer.

## 2026-04-18 | init | vault contract rewritten

- Rewrote the vault documentation around the new Obsidian structure: `raw/`, `catalog/`, `wiki/`, `projects/`, and `artifacts/`.
- Reframed `agent.md` as a vault-maintenance schema instead of a generic repo note.
- Aligned the README files with the active Obsidian plugin stack and Karpathy-style workflow.

## 2026-04-18 | seed | first wiki spine

- Created the first dataset notes for `daily_stock`, `CCM`, `comp_na_daily_all_annual`, `option_forward_price`, and `risk_free_rate`.
- Created the first identifier notes for `permno`, `gvkey`, `secid`, `ticker`, and `cusip`.
- Added `index.md` and this `log.md` so the vault now has both a content map and a chronological maintenance record.

## 2026-04-18 | note | current emphasis

- The current wiki seed focuses on the core join spine between market data, fundamentals, options, and excess-return construction.
- The next high-value expansion should document additional datasets and then connect them to active project notes in `projects/`.

## 2026-04-18 | ingest | machine learning and quantitative finance source shelf

- Added deep source notes for the core `raw/machine_learning/` books, including ISL, Bishop, Murphy, Bayesian reasoning, financial signal processing, Lopez de Prado, and reinforcement learning.
- Added deep source notes for the core `raw/quantitative_finance/` books, including HFT, algorithmic trading, portfolio optimization, risk management, quantitative trading, computational finance, Monte Carlo, and alpha research.
- Ingested `Causality and Factor Investing A Primer` section by section to anchor causal caution in the factor-research layer.

## 2026-04-18 | crystallize | cross-source quant synthesis

- Added [[Probabilistic Machine Learning]], [[Reinforcement Learning]], [[Financial Machine Learning Workflow]], and [[Monte Carlo Methods]].
- Added [[Portfolio Construction]], [[High-Frequency Trading]], [[Alpha Research]], and [[Backtest Overfitting]].
- Updated `index.md`, the reading-map layer, and `inbox.md` so the vault map reflects the new source shelf and synthesis layer.

## 2026-04-18 | restructure | wiki taxonomy tightened

- Added `maps/` and split the vault map into a top-level reading map plus domain maps.
- Reorganized `sources/` into `books/`, `papers/`, and `articles/` so provenance is easier to read.
- Collapsed the old `models/`, `markets/`, `risks/`, and `systems/` folders into a broader `concepts/` layer.
- Kept `glossary.md`, `inbox.md`, and `_templates/` at the root because they are maintenance surfaces rather than topic buckets.

## 2026-04-18 | audit | raw shelf coverage expanded

- Audited the full `raw/` tree against the current wiki source layer instead of relying on memory or the earlier backlog.
- Added the missing `raw/math_statistics/` source notes, including [[All of Statistics]], [[Applied Probability]], [[Arbitrage Theory in Continuous Time]], [[Convex Optimization]], [[Time Series Analysis and Its Applications]], [[Bayesian Filtering and Smoothing]], [[Stochastic Calculus for Finance II]], and [[Kalman Filter Tutorial]].
- Added the remaining ML, finance, and interview notes, including [[Ensemble Methods in Data Mining]], [[GraphSAGE with Deep Reinforcement Learning for Financial Portfolio Optimization]], [[Financial Risk Manager Handbook]], [[Heard on the Street]], [[A Practical Guide to Quantitative Finance Interviews]], and [[Quant Job Interview Questions and Answers]].
- Folded the Chinese editions of Aldridge, Chan, and Tulchinsky into their existing English source notes as alternate editions, and added [[Quantitative Strategies for Achieving Alpha]] for the distinct Chinese-only alpha book.
- Logged the image capture `[[Target from Quant Firm]]` so the source inventory is complete even though manual visual review is still pending.

## 2026-04-18 | crystallize | methods from the new source shelf

- Added [[Kalman Filtering]] as the first durable state-estimation method note built from the Kalman tutorial, Bayesian filtering, time-series, and signal-processing sources.
- Added [[Time-Series Forecasting]] to turn the new time-series shelf into a reusable forecasting workflow note instead of leaving it source-bound.
- Added [[Stochastic Calculus]] as the continuous-time bridge between probability, pricing, hedging, and dynamic portfolio problems.
- Added [[Convex Optimization Methods]] to connect the new optimization shelf with portfolio construction and regularized estimation.
- Updated the index and map layer so the new methods are visible as top-level entry points rather than only as source byproducts.

## 2026-04-18 | tooling | obsidian mcp verified

- Verified that the Obsidian tool layer can list the vault and read wiki notes directly.
- Verified that wiki maintenance can be written through the Obsidian layer by appending this log entry.
- Updated `agent.md` so future vault work prefers Obsidian operations for note-local tasks while keeping `apply_patch` for large or diff-sensitive refactors.

## 2026-04-18 | ingest | obsidian cli operating note

- Ingested `raw/Obsidian/Obsidian_README.md` into [[Obsidian CLI README]].
- Updated [[LLM Knowledge Base Workflow]] so links, Bases, and tags are treated as the most important Obsidian operating surfaces for this vault.
- Tightened `agent.md` so future vault maintenance prefers Obsidian-native operations for note-local work and treats Bases as an operational dashboard layer rather than a second source of truth.

## 2026-04-18 | tooling | obsidian cli partial verification

- Confirmed that `Obsidian.com` exists at the standard Windows install path, so the CLI binary is installed.
- Confirmed that the bare `obsidian` command is not on `PATH` in this shell.
- Confirmed that invoking `Obsidian.com` directly reaches the CLI, but IPC still reports that it cannot find Obsidian from this session, so the shell-side CLI is not fully usable yet even though the Obsidian MCP layer works.

## 2026-04-19 | tooling | obsidian cli fixed for desktop ipc

- Identified the real failure mode: sandboxed shell commands run under a different Windows identity than the interactive Obsidian desktop session, so the shell could see the CLI binary but could not attach to the named pipe.
- Confirmed that `obsidian` works when executed unsandboxed against the running desktop app.
- Updated `agent.md`, `README.md`, and `wiki/README.md` so future sessions treat Obsidian MCP as the default sandbox-safe path and use unsandboxed shell CLI commands only for app-native operations.

## 2026-04-19 | maps | knowledge base canvas added

- Added `wiki/maps/knowledge_base.canvas` as the first spatial overview of the vault.
- Structured the canvas around the five working layers: governance, inputs, compiled wiki, active research, and evidence outputs.
- Anchored the canvas to real vault files instead of free-floating text so it remains a navigation surface rather than a second knowledge store.
