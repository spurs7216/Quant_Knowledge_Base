---
title: Quant Research System Architecture
type: project
status: active
updated: 2026-04-29
tags:
  - project
  - architecture
  - quant
  - research-agent
---
# Quant Research System Architecture

## Operating model

The local vault is the memory and control layer. The remote machine is the heavy data and compute layer. IBKR/TWS is the local execution realism layer.

Do not collapse these into one tool. Each layer has a different trust role.

Current machine boundary: IBKR TWS access exists only on the local machine, not on the remote Linux/GPU machine. Remote jobs must not require broker connectivity, TWS, IB Gateway, account access, position access, paper order submission, or broker credentials.

Current Phase 4 LLM boundary: the local Windows machine cannot run Qwen or other Phase 4 LLM inference because of memory constraints. All Qwen calls, AlphaEvolve-lite controller execution, static generated-code filters, toy/sample/full evaluator runs, and program-database updates must run on the remote Linux/GPU/data server. Local Windows remains the edit, Git sync, Obsidian, and compact-artifact review machine.

This architecture is not trying to be minimal. It is trying to be durable. Complexity is acceptable when it buys reliability, reuse, auditability, execution safety, or learning value. Complexity is unacceptable when it hides assumptions or makes results harder to reproduce.

## Plane 1. Knowledge plane

Lives primarily in:

- `raw/`
- `wiki/`
- `catalog/`

Purpose:

- source-grounded knowledge
- mathematical and statistical foundations
- dataset observability
- method and failure-mode memory

Rules:

- use `raw/` for original sources
- use `wiki/` for durable compiled knowledge
- use `catalog/` to understand remote data without loading heavy files locally

## Plane 2. Control plane

Lives primarily in:

- `projects/`

Purpose:

- task definitions
- research plans
- job manifests
- retrieval traces
- decisions
- unresolved questions

Rules:

- keep active research uncertain until evidence supports promotion
- every serious task should state what would falsify it
- every remote job should have a manifest before execution

## Plane 3. Research compute plane

Lives primarily on:

- remote Linux data/GPU machine

Purpose:

- full data scans
- expensive backtests
- model training
- feature generation
- validation batteries

Rules:

- local vault does not become the warehouse
- remote jobs must write compact evidence outputs
- only small artifacts and metadata come back to the vault
- heavy datasets stay remote
- remote jobs do not call IBKR, TWS, IB Gateway, or broker APIs

## Plane 4. Evaluation plane

Lives across:

- `projects/quant_research_eval/`
- `artifacts/`
- remote evaluator scripts

Purpose:

- score tasks
- reject weak ideas
- compare blind, wiki-only, and full-vault regimes
- support longitudinal measurement

Rules:

- use multi-metric scoring, not one Sharpe-like target
- include null tasks
- separate in-sample improvement from hidden out-of-sample validation
- record failure categories

## Plane 5. Candidate plane

Lives across:

- project folders
- remote candidate database
- artifact bundles

Purpose:

- store proposed factors, strategy rules, model variants, and search heuristics
- keep parent-child lineage
- keep scores and failure reasons

Candidate artifact types:

- direct artifact: finished factor, strategy, or portfolio rule
- constructor artifact: generator for feature families or parameterized signals
- search artifact: code that searches for candidate rules under constraints

Rules:

- start with direct and constructor artifacts
- avoid whole-codebase evolution until the evaluator is mature
- keep lineage inspectable

## Plane 6. Execution plane

Lives around:

- local IBKR paper account
- local TWS API or Client Portal Web API harness
- local read-only IBKR MCP where available

Purpose:

- test brokerage-facing implementation
- inspect account and position state
- resolve contracts
- handle orders, fills, cancellations, and reconciliation in paper trading

Rules:

- IBKR/TWS tasks are local-only unless a future remote broker environment is explicitly built and approved
- no live orders without explicit human approval
- no-send strategy-to-order translation can be tested early as an implementation-feasibility smoke test
- paper-trading order submission comes after historical validation gates
- execution checks must not be confused with alpha validity
- remote compute may produce feasibility inputs, such as estimated turnover, liquidity, short-side concentration, and candidate target books, but local IBKR checks decide broker-facing readiness

## Control loop

The intended loop is:

1. retrieve context from the vault
2. define task and artifact type
3. create candidate or patch candidate
4. run cheap local checks
5. submit remote validation job if needed
6. sync compact artifacts back
7. score and decide: reject, revise, promote, or paper-test
8. for strategy artifacts, run no-send execution-readiness checks before large search or paper-test promotion
9. update project notes and crystallize durable lessons only after evidence

## AlphaEvolve translation

AlphaEvolve component mapping:

| AlphaEvolve component | Quant system counterpart |
| --- | --- |
| Initial program | executable seed strategy module |
| EVOLVE block | bounded candidate artifact region marked in code |
| SEARCH/REPLACE diff | generated code patch applied to the seed program |
| Prompt sampler | vault-aware context builder using parent code, inspirations, wiki notes, catalog context, and evaluator results |
| LLM ensemble | measured Qwen stack: Qwen3.5-9B generation/repair, Qwen3.5-27B-FP8 review, Qwen3.6-35B-A3B-FP8 scheduled deep review |
| Evaluator pool | remote `controller_static`, `toy_eval`, `remote_sample_eval`, `remote_stage0_eval`, `remote_full_validation`, artifact review, later paper-execution checks |
| Program database | SQLite search-facing store of programs, scores, descriptors, outputs, prompts, evaluations, validation exposure, and lineage |
| Candidate registry | official research lineage and promotion state after review |
| Multiple metrics | scalar score dictionary plus hard-gate diagnostics |

## Design priority

Build the evaluator and remote artifact contract before building large search loops. Without a reliable evaluator, search only accelerates overfitting.

After the AlphaEvolve source re-read and the Phase 4 v2 update, Phase 4 should not treat a one-time batch of variants as the search loop. The loop requires parent/inspiration sampling, code diffs, evaluator execution, program-database updates, validation-exposure accounting, and compact prompt-facing artifacts. The first production loop is daily-stock-only with a rolling point-in-time top-500 universe and locked chronological 70/15/15 split.

## Related Notes

- [Quant Research System Multi-Agent Orchestration](multi_agent_orchestration.md)
