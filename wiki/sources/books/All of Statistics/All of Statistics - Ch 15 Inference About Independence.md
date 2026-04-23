---
title: All of Statistics - Ch 15 Inference About Independence
type: source
status: chapter_ingested
updated: 2026-04-19
tags:
  - source
  - statistics
  - dependence
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: full_source
extraction_basis: full_text
technical_depth: moderate
ingest_stage: scan
chapter_or_section: Ch 15 Inference About Independence
parent_source: "[[All of Statistics]]"
sources:
  - "[[All of Statistics]]"
  - "[[raw/math_statistics/2004 - wasserman - all of statistics.pdf]]"
---
# All of Statistics - Ch 15 Inference About Independence

## Ingest Scope and Depth

- Ingest stage: `scan`
- Pass 1: full chapter scan completed against the raw source.
- Pass 2: rescan completed to identify which inferential pieces deserve later deepening.

## Deepening Targets

- Deepen the odds-ratio parameterization in the `2 x 2` case if binary-event dependence becomes a recurring quant object.
- Deepen the likelihood-ratio and Pearson chi-square logic for contingency tables if categorical dependence testing becomes operationally important.
- Deepen the mixed discrete-continuous case, especially Theorems 15.11 and 15.12, if the vault needs a stronger bridge from independence to distribution-equality testing.
- Deepen the appendix discussion of case-control sampling and rare-disease approximation if event studies or rare-event classification notes start to rely on odds ratios.

## Deepened Subparts

- No subpart has been rewritten at full deep-note depth yet.

## Worth Attending From The Rescan

- Theorem 15.2 is the load-bearing equivalence in the binary case: independence, `psi = 1`, `gamma = 0`, and factorization of the joint table all say the same thing. This turns an abstract independence claim into a scalar estimand.
- Theorems 15.3 and 15.4 are worth attending together because the likelihood-ratio and Pearson statistics are both asymptotic `chi^2` tests, but they arise from different approximations to the same null restriction.
- Theorems 15.6 and 15.7 matter because the log-odds ratio has a cleaner asymptotic standard error than the raw odds ratio. This is why interval construction is usually done on the log scale and exponentiated afterward.
- Theorem 15.11 is the mixed-type bridge: when one variable is discrete and the other continuous, independence is equivalent to equality of conditional cdfs. That is the conceptual step that justifies the two-sample Kolmogorov-Smirnov route.
- Theorem 15.13 in the appendix is easy to skip but practically important: under rare disease, relative risk and odds ratio are approximately the same, which explains why case-control sampling can still support meaningful effect-size estimation.

## Role of the chapter

This chapter moves from defining independence to testing and estimating it from data.

It treats several cases:

- two binary variables
- two discrete variables
- two continuous variables
- mixed discrete-continuous settings

The chapter is important because dependence is usually not an all-or-nothing conceptual issue in applied work. It is an inferential question.

## Core mathematical objects

- odds ratio
- contingency tables
- likelihood-ratio and Pearson tests for independence
- mle under independence constraints

## Binary case and odds ratio

### Definition 15.1 and Theorem 15.2

For two binary variables, the chapter shows the equivalence between independence and an odds ratio of one.

This is a very useful result because it turns an abstract factorization property into a scalar quantity that can be estimated and tested.

### Theorems 15.3 and 15.4

The chapter then gives likelihood-ratio and Pearson chi-square tests for independence in the binary table.

## General discrete case

### Theorem 15.9

The logic extends to larger contingency tables.

The main lesson is that independence can be encoded as structured restrictions on cell probabilities, and those restrictions can be tested by comparing fitted and observed counts.

## Continuous and mixed cases

The later sections and appendix widen the framework beyond pure discrete tables.

The point is that dependence testing is not only about cross-tabulation. It is about determining whether the joint law factorizes after accounting for the variable types involved.

## What the chapter is really teaching

Inference about independence is not merely checking whether a sample correlation is near zero.

Depending on variable type, one needs:

- the correct parameterization of dependence
- the correct null restriction
- the correct sampling distribution for the test statistic

## Failure modes the chapter is trying to prevent

- equating independence with zero correlation in general settings
- forgetting that the right statistic depends on the variable types
- treating sparse contingency tables as if asymptotic chi-square approximations are automatically reliable

## Quant research relevance

This chapter matters for quant research because dependence questions appear constantly:

- are two signals redundant?
- is a label independent of a feature?
- do discrete event categories depend on treatment or regime?
- does a binary market event co-move with another binary condition?

The odds-ratio perspective is especially useful when binary event dependence is the real object of interest.

## What should be promoted out of this source note

- a durable note on odds ratios
- a durable note on testing independence in contingency tables
- a durable note on why zero correlation does not imply independence

## Related notes

- [[All of Statistics]]
- [[All of Statistics - Ch 16 Causal Inference]]
- [[All of Statistics - Ch 17 Directed Graphs and Conditional Independence]]
- [[Stats Map]]

## Sources

- [[All of Statistics]]
- [[raw/math_statistics/2004 - wasserman - all of statistics.pdf]]
