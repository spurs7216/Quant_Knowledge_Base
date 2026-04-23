---
title: Quant Research System Brief
type: project
status: active
updated: 2026-04-23
tags:
  - project
  - system-design
  - quant
  - research-agent
  - alphaevolve
---
# Quant Research System Brief

## Goal

Design a system that can help Codex become a useful independent quant-research agent:

- reads and internalizes durable mathematical and financial knowledge
- proposes research hypotheses
- writes executable research code
- runs disciplined validation on the full remote data warehouse
- rejects weak ideas
- produces compact evidence artifacts
- eventually handles paper-trading implementation through IBKR safely

The system is not only a vault and not only a benchmark. It is a research operating system.

## Core design claim

The next bottleneck is not model fine-tuning. The next bottleneck is environment design:

- clear candidate artifact types
- evaluator cascades
- remote data access discipline
- artifact provenance
- execution safety
- longitudinal scoring

This follows the strongest lesson from AlphaEvolve: the human defines the task, initial scaffold, and evaluation criteria; the agent searches over executable artifacts and is disciplined by machine feedback.

## System quality principle

Smallness is not a goal.

The system should be as complex as necessary to be robust, useful, reusable, and learnable. The real danger is not complexity by itself. The real danger is unstructured complexity: hidden assumptions, untracked data movement, undocumented evaluator choices, unreviewed artifacts, and research results that cannot be reproduced.

So the design standard is modular complexity:

- each subsystem should have a clear contract
- each run should leave inspectable evidence
- each candidate should have lineage and status
- each result should be reproducible or explicitly marked provisional
- each layer should teach the next agent how to use it

## What we adopt from AlphaEvolve

- candidate artifacts should be executable when possible
- search should happen through patches, not only one-shot generation
- the system should keep a candidate database with scores and failure reasons
- evaluators should be multi-metric
- evaluation should use cascades: cheap filters first, expensive tests later
- rich context from the knowledge base should be available, but not treated as a substitute for evaluation
- different problems need different abstraction levels: final strategy, constructor, or search heuristic

## What we reject for now

- no general RL training as the first project
- no live trading automation
- no single headline score as the system target
- no unrestricted search over huge notebooks or entire codebases in the first phase
- no treating Backtrader as the main implementation exam

## System planes

The system has six planes:

1. `knowledge plane`
   The local vault: `raw/`, `wiki/`, `projects/`, `catalog/`, and `artifacts/`.
2. `control plane`
   Local project specs, task manifests, retrieval traces, decisions, and review notes.
3. `research compute plane`
   Remote warehouse and GPU machine for heavy data work, model training, and full validation.
4. `evaluation plane`
   Evaluator cascades, hidden tests, null tasks, scorecards, and robustness checks.
5. `candidate plane`
   Versioned factors, strategies, research scripts, search heuristics, and result histories.
6. `execution plane`
   IBKR paper-trading and eventually deployment-facing implementation checks.

## First system milestone

The first milestone should be a working `remote_validation` environment:

- candidate artifact: factor or strategy research script
- data: remote warehouse, selected from local `catalog/`
- evaluator: staged validation cascade
- output: compact artifact bundle synced back to `artifacts/`
- decision: proceed, revise, or reject

This is more important than running QuantCode-Bench first because it tests the real research loop.

## Sources

- [[raw/Quantitative Research Agent.md]]
- [[raw/AlphaEvolve - A coding agent for scientific and algorithmic discovery.pdf]]
- [Quant Research Eval Suite Brief](../quant_research_eval/brief.md)
- [Catalog README](../../catalog/README.md)
- https://interactivebrokers.github.io/tws-api/order_submission.html
- https://interactivebrokers.github.io/tws-api/historical_limitations.html
- https://ibkrcampus.com/campus/ibkr-api-page/webapi-doc/
