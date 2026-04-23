# Agent Core

This file expands the mission-level rules from [../AGENTS.md](../AGENTS.md).

## Mission

The vault exists to support quantitative research that could eventually matter in real trading.

That means the research this vault supports must be:

- mathematically sound
- statistically defensible
- logically coherent
- computationally implementable
- financially realistic
- robust under out-of-sample and implementation pressure

Profitability matters, but the vault must not confuse attractive stories with deployable edges.

## Vault Map

- `raw/`: original books, papers, captures, and source material
- `catalog/`: mirrored dataset descriptions, samples, and EDA
- `wiki/`: durable knowledge
- `projects/`: active questions, replications, and evolving synthesis
- `artifacts/`: bounded evidence outputs
- `.obsidian/`: frontend and automation surface

## Source-of-Truth Hierarchy

Use this trust order:

1. `raw/`
2. `catalog/`
3. `artifacts/`
4. `wiki/`
5. `projects/`

If a durable note conflicts with the raw source, the data mirror, or verified evidence, fix the note.

## Model-Memory Policy

Internal model knowledge may be used to:

- recognize relevant structure
- understand the question
- form candidate explanations, derivations, and research directions

But it must not be treated as the vault's memory or as the main criterion for note inclusion.

Why:

- it is not inspectable by the human user
- it is not stable across models or sessions
- it is often directionally right but too vague for serious quant work

So the right standard is:

- store what the research system must know explicitly

## Quant Doctrine

There are two different kinds of truth in the vault:

- conceptual truth: definitions, assumptions, methods, semantics, interpretations
- numerical truth: measured outputs, diagnostics, replication results, and empirical evidence

Do not blur them.

Examples:

- a wiki note can explain what a field means
- a claim that a signal is robust or profitable requires evidence from `artifacts/` or verified processed outputs

## Inclusion Test for Durable Knowledge

A note belongs in `wiki/` when at least one of these is true:

- it carries assumptions, theorem conditions, proof ideas, derivation structure, or implementation caveats that matter later
- it is repeatedly needed across projects or future ingests
- it is easy to misuse if left implicit
- it anchors later econometrics, ML, finance, or trading work
- it captures vault-specific synthesis or cross-source interpretation

Novelty to the model is not enough. Foundational material often belongs because it is high-leverage and failure-prone.

## Human-in-the-Loop

The agent should work autonomously on structure, ingest, and promotion, but should not pretend certainty where the understanding is shallow.

If understanding is partial:

- mark it honestly
- keep scanning or deepening until the relevant mathematical and statistical structure is understood

## Success Criteria

The vault is healthy when:

- source coverage is honest
- load-bearing chapters are deepened at the right level
- reusable knowledge is promoted out of the source shelf
- notes are linked and inspectable
- claims are tied to sources or evidence
- the system becomes more useful for future research questions

## Immediate Priorities

- deepen the math and statistics shelf before broadening too aggressively
- keep the ingest workflow disciplined
- promote source knowledge into durable concepts and methods
- maintain evidence and provenance standards that can support future trading-facing research
