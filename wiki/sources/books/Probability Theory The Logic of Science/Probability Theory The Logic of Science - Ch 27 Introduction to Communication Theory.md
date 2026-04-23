---
title: Probability Theory The Logic of Science - Ch 27 Introduction to Communication Theory
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - information-theory
  - bayesian
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: chapter-start and selected coding-and-markov-source pages via pymupdf
technical_depth: medium
ingest_stage: selective_deepen
chapter_or_section: Ch 27 Introduction to Communication Theory
parent_source: "[[Probability Theory The Logic of Science]]"
sources:
  - "[[Probability Theory The Logic of Science]]"
  - "[[raw/math_statistics/Probability Theory The Logic of Science.pdf]]"
---
# Probability Theory The Logic of Science - Ch 27 Introduction to Communication Theory

## Ingest Scope and Depth

- Ingest stage: `selective_deepen`
- Pass 1: full chapter scan completed.
- Pass 2: deepened the chapter's main bridges from entropy to coding, Markov structure, and noisy-channel correction.

## Role of the chapter

This chapter reframes communication theory as another application of the same entropy and probability calculus developed earlier. Coding efficiency, source structure, and noise correction are all treated as inference problems.

## Core mathematical objects

- source probabilities `p_i`
- source entropy
  $$H(p)=-\sum_i p_i \log p_i$$
- code lengths
- Markov or digram structure in symbol sequences
- noisy channel and checksum correction

## Key results

The main durable point is that entropy controls coding efficiency only relative to the actual source model. Independent-letter coding leaves information on the table if the source has higher-order dependence such as digram or Markov structure.

Jaynes also treats noisy communication as an inference problem: the receiver should combine channel behavior with source structure rather than treating error correction as a purely mechanical add-on.

## Why this matters later

The chapter is not central to the vault's current math/statistics spine, but it matters because it shows how information theory remains subordinate to the same Bayesian logic rather than becoming a separate foundational doctrine.

## Failure modes and misuse points

- using entropy as if it were independent of the source model
- ignoring dependence structure when designing encoders or decoders
- thinking of noisy-channel correction as unrelated to inference

## Quant research relevance

The main relevance is indirect: compression, message filtering, sequential inference, and state decoding in finance all benefit when dependence structure is modeled instead of discarded.

## What should be promoted out of this source note

- a future bridge note on entropy, coding, and state-sequence models

## Related notes

- [[Probability Theory The Logic of Science]]
- [[Maximum Entropy Principle]]
- [[Hidden Markov Models and Switching Autoregression]]

## Sources

- [[Probability Theory The Logic of Science]]
- [[raw/math_statistics/Probability Theory The Logic of Science.pdf]]
