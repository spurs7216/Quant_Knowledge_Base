---
title: Coding Principles for Quant Research Systems
type: method
status: active
updated: 2026-05-05
tags:
  - method
  - coding-principles
  - software-design
  - quant-research-system
sources:
  - wiki/sources/books/A Philosophy of Software Design
  - wiki/sources/books/A Philosophy of Software Design Selected Excerpts
  - wiki/sources/books/The Pragmatic Programmer
used_by:
  - projects/quant_research_system
---
# Coding Principles for Quant Research Systems

## Summary

Code in this vault should be designed for repeated quant research, not only for a single run. Clean code here means:

- the important research semantics are explicit;
- each module owns a clear design decision;
- interfaces are smaller than the implementation they hide;
- invalid states and informal assumptions are converted into contracts, checks, or data structures;
- tests and artifacts verify behavior at the right boundary;
- implementation stays compatible with the existing codebase style.

This note synthesizes [[A Philosophy of Software Design]], [[A Philosophy of Software Design Selected Excerpts]], and [[The Pragmatic Programmer]] for the active quant research system.

## Core Standard

The main design question is: what matters here, and where should it live?

For quant code, what matters usually includes dataset grain, timestamp semantics, universe construction, split policy, exposure constraints, transaction costs, evaluator pass/fail logic, model-router behavior, prompt contracts, and evidence provenance. These should be named, centralized, tested, and documented. Incidental mechanics such as file layout, default paths, JSON formatting, retries, and CLI glue should be hidden inside their owning modules.

## Module Design Rules

### Prefer deep modules

A module should expose a simple interface that hides meaningful complexity. Avoid adding a class, function, or wrapper if its interface is almost as complex as what it wraps.

Good quant examples:

- an evaluator API that accepts a strategy program and returns a typed summary;
- a dataset contract module that owns daily-stock field names and timestamp rules;
- a model router that hides provider-specific response shape and timeout behavior.

Weak examples:

- pass-through helpers that only rename arguments;
- one-off wrappers that force callers to know every internal file path;
- strategy helpers whose names hide whether weights are lagged, normalized, gross-scaled, or cost-adjusted.

### Hide information once

Every important design decision should have one owner. Duplicating knowledge creates synchronization risk.

Common knowledge that must not be duplicated casually:

- cost assumptions;
- train/validation/test split dates;
- daily-stock schema and field aliases;
- portfolio exposure limits;
- EVOLVE-BLOCK patch rules;
- model response parsing rules;
- program-database promotion rules.

### Keep different layers at different abstractions

Controller code should talk about attempts, patch validation, child uniqueness, diagnostics, and database records. Evaluator code should talk about universe, signal, portfolio, costs, and metrics. Prompt-building code should talk about task context, memory, diagnostic cards, skill cards, and immutable output rules.

If two adjacent layers use nearly identical signatures and vocabulary, the upper layer may not be adding a real abstraction.

### Pull complexity downward

Place unavoidable complexity inside the module with the most context to handle it. A caller should not repeatedly provide obscure defaults, remember file naming conventions, catch expected edge cases, or rebuild common JSON structures.

Downward complexity is not hiding evidence. It is hiding mechanics while keeping the important output inspectable.

### Be somewhat general, not speculative

Generalize when it makes the interface simpler for likely future uses. Do not build broad frameworks without current pressure.

In Phase 4, this means a reusable diagnostic-card writer is justified because each controller batch needs it. A generic trading-platform abstraction is not justified while the current loop is daily-stock-only and still freezing contracts.

### Define errors out of existence

Prefer representations where impossible or invalid states cannot flow downstream.

Examples:

- parse model responses into a structured patch object before filtering;
- reject ambiguous portfolio outputs before expensive evaluation;
- represent pass/fail reasons with stable categories rather than free-form strings only;
- make missing schema fields a contract failure, not a late KeyError.

## Workflow For New Code

1. Identify the owner: state which module owns the design decision.
2. Write the interface contract first: expected inputs, outputs, invariants, and failure modes.
3. Consider two designs for nontrivial changes: compare boundary placement, testability, and future coupling.
4. Implement the smallest coherent deep module: avoid shallow wrappers and broad abstractions.
5. Add focused tests or smoke checks at the boundary where failure would be costly.
6. Update the relevant wiki or project note when the code creates a durable contract.
7. Leave generated artifacts out of git unless they are bounded evidence explicitly requested for tracking.

## Comments, Names, And Documentation

Comments are design tools when they capture information that code cannot make obvious:

- why a constraint exists;
- what invariant downstream code relies on;
- what timestamp convention prevents leakage;
- what evaluator failure mode a guard is preventing;
- what a prompt rule must preserve for remote runs.

Avoid comments that merely restate code. If a name is hard to choose, treat that as a design signal: the concept may be mixed, vague, or in the wrong module.

Names in quant code should carry the semantic load needed for correctness:

- `lagged_weight` is better than `weight` when timing matters;
- `gross_exposure` and `net_exposure` should not be collapsed into `exposure`;
- `validation_sharpe_after_cost` is more honest than `score`;
- `daily_stock_contract` is clearer than `schema` if the object freezes required field semantics.

## Testing And Evidence

Testing should match the risk:

- pure transformation logic gets deterministic unit tests;
- portfolio construction gets semantic smoke tests for signs, gross exposure, net exposure, max weight, and missing data behavior;
- evaluator changes get sample-run artifacts;
- LLM-controller changes get static filter, duplicate, and diagnostic-card evidence before expensive full evaluation;
- performance changes get measurement before and after.

For research code, numerical claims still require `artifacts/` evidence. A clean implementation does not imply a valid alpha.

## Quant-Specific Red Flags

- A function mixes data loading, signal logic, portfolio construction, cost accounting, and reporting.
- The same field alias, split date, or cost assumption appears in several unrelated files.
- A prompt rule, evaluator metric, or database promotion condition exists only in prose.
- A module's public parameters expose rare internal options needed only by one caller.
- Error handling is a chain of special cases rather than a cleaner representation.
- A child strategy passes syntax checks but leaves exposure, lag, cost, or max-weight semantics implicit.
- A name hides whether a quantity is before-cost, after-cost, lagged, cross-sectional, sector-neutral, gross-scaled, or dollar-neutral.
- A comment explains what the line does but not why the system needs it.
- Tests prove a toy branch executes but not that the research contract is preserved.

## What This Rejects

- Refactoring for tidiness without a concrete owner, boundary, or failure mode.
- Splitting functions purely to make them shorter when the split creates conjoined shallow functions.
- Treating comments as failures by default.
- Treating tests, patterns, or framework style as substitutes for design judgment.
- Pushing code that relies on assumed field names, informal model logs, or unverified cost semantics.

## Related notes

- [[A Philosophy of Software Design]]
- [[A Philosophy of Software Design Selected Excerpts]]
- [[The Pragmatic Programmer]]
- [[AlphaEvolve Lite Quant Search Workflow]]
- [[Reasoning Memory for AlphaEvolve Search]]
- [[Group-Relative Skill Learning for Alpha Search]]

## Sources

- [[A Philosophy of Software Design]]
- [[A Philosophy of Software Design Selected Excerpts]]
- [[The Pragmatic Programmer]]
