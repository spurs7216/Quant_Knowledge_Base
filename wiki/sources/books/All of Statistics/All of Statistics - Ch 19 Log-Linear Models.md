---
title: All of Statistics - Ch 19 Log-Linear Models
type: source
status: chapter_ingested
updated: 2026-04-19
tags:
  - source
  - statistics
  - discrete-models
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: full_source
extraction_basis: full_text
technical_depth: moderate
ingest_stage: scan
chapter_or_section: Ch 19 Log-Linear Models
parent_source: "[[All of Statistics]]"
sources:
  - "[[All of Statistics]]"
  - "[[raw/math_statistics/2004 - wasserman - all of statistics.pdf]]"
---
# All of Statistics - Ch 19 Log-Linear Models

## Ingest Scope and Depth

- Ingest stage: `scan`
- Pass 1: full chapter scan completed against the raw source.
- Pass 2: rescan completed to identify the pieces that justify later deepening.

## Deepening Targets

- Deepen Theorem 19.1 if the vault later needs a more explicit map from multinomial tables to log-linear coordinates.
- Deepen Theorem 19.4 if conditional-independence restrictions in discrete systems become operationally important.
- Deepen the distinction between graphical and hierarchical models, since that is the chapter's main modeling subtlety.
- Deepen deviance-based fitting and model search if discrete regime or event-state models become a live research tool.

## Deepened Subparts

- No subpart has been rewritten at full deep-note depth yet.

## Worth Attending From The Rescan

- Theorem 19.1 is the structural spine: any discrete joint law can be written in a log-linear expansion, so dependence becomes a question about which interaction terms are present.
- Theorem 19.4 is the key bridge from coefficients to independence: conditional independence is equivalent to the vanishing of all interaction terms that touch both blocks being separated.
- Definition 19.6 versus Definition 19.8 is the chapter's main conceptual distinction. Graphical models impose only conditional-independence restrictions; hierarchical models are broader and can encode extra structural restrictions that no graph alone captures.
- Definition 19.13 and Theorem 19.14 matter because deviance is just a likelihood-ratio test against the saturated model. That turns discrete model selection into a formally testable comparison rather than a purely descriptive exercise.

## Role of the chapter

This chapter develops a structured model family for discrete multivariate laws.

The central idea is to model the log of the joint probability through additive interaction terms. This makes independence and interaction structure explicit and connects naturally to graphical models.

## Core mathematical objects

- log-linear expansion of a joint pmf
- interaction terms
- hierarchical models
- graphical log-linear models
- deviance

## Log-linear representation

### Theorem 19.1

The chapter shows that a discrete joint law can be expressed in log-linear form.

This is important because it turns discrete dependence into a coefficient-structure problem rather than a raw table-of-probabilities problem.

## Conditional independence and interaction structure

### Theorem 19.4 and Lemma 19.5

Conditional independence constraints correspond to specific zero-structure restrictions in the log-linear representation.

This is the main conceptual bridge between discrete dependence and graphical structure.

## Hierarchical and graphical models

### Definition 19.8 and related examples

Hierarchical models preserve lower-order terms whenever higher-order interactions are present.

Graphical log-linear models are a particularly structured subclass.

The practical point is that sparsity and interpretability come from restricting which interaction terms are allowed.

## Deviance and fitting

### Definition 19.13 and Theorem 19.14

The deviance acts as a likelihood-ratio test statistic for comparing a fitted submodel to a richer reference.

This turns model selection and goodness-of-fit for discrete interaction structures into a testing problem.

## What the chapter is really teaching

This chapter teaches that discrete dependence can be decomposed into interaction order and graphical structure.

That is useful because it separates:

- main effects
- pairwise interactions
- higher-order interactions

instead of treating the full joint table as unanalyzable.

## Failure modes the chapter is trying to prevent

- treating discrete dependence tables as if they have no structure to exploit
- forgetting that higher-order interaction terms change the meaning of lower-order interpretations
- fitting rich interaction models without checking model complexity and deviance

## Quant research relevance

This chapter is most relevant when quant problems are discretized:

- categorical regimes
- contingency-style event systems
- discretized state variables

It is also useful as a bridge between graphical reasoning and likelihood-based model comparison for discrete systems.

## What should be promoted out of this source note

- a durable note on log-linear models
- a durable note on hierarchical interaction structure
- a durable note on deviance

## Related notes

- [[All of Statistics]]
- [[All of Statistics - Ch 18 Undirected Graphs]]
- [[All of Statistics - Ch 22 Classification]]

## Sources

- [[All of Statistics]]
- [[raw/math_statistics/2004 - wasserman - all of statistics.pdf]]
