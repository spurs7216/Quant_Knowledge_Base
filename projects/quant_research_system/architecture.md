---
title: Quant Research System Architecture
type: project
status: active
updated: 2026-04-23
tags:
  - project
  - architecture
  - quant
  - research-agent
---
# Quant Research System Architecture

## Operating model

The local vault is the memory and control layer. The remote machine is the heavy data and compute layer. IBKR is the execution realism layer.

Do not collapse these into one tool. Each layer has a different trust role.

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

- IBKR paper account
- TWS API or Client Portal Web API harness
- read-only IBKR MCP where available

Purpose:

- test brokerage-facing implementation
- inspect account and position state
- resolve contracts
- handle orders, fills, cancellations, and reconciliation in paper trading

Rules:

- no live orders without explicit human approval
- paper-trading comes after historical validation gates
- execution checks must not be confused with alpha validity

## Control loop

The intended loop is:

1. retrieve context from the vault
2. define task and artifact type
3. create candidate or patch candidate
4. run cheap local checks
5. submit remote validation job if needed
6. sync compact artifacts back
7. score and decide: reject, revise, promote, or paper-test
8. update project notes and crystallize durable lessons only after evidence

## AlphaEvolve translation

AlphaEvolve component mapping:

| AlphaEvolve component | Quant system counterpart |
| --- | --- |
| Initial program | baseline factor, strategy, or research script |
| EVOLVE block | editable candidate artifact region |
| Prompt sampler | vault-aware context builder |
| LLM ensemble | Codex plus optional smaller/faster proposal models later |
| Evaluator pool | local checks, remote validation, paper-execution checks |
| Program database | candidate registry with lineage and scores |
| Multiple metrics | research score panel and evaluator cascade |

## Design priority

Build the evaluator and remote artifact contract before building large search loops. Without a reliable evaluator, search only accelerates overfitting.
