---
title: Quant Research Eval Suite Scorecard
type: project
status: active
updated: 2026-04-23
tags:
  - project
  - benchmark
  - scorecard
  - quant
  - evaluation
---
# Quant Research Eval Suite Scorecard

## Score panel

Do not reduce the vault to one number by default. Track a score panel first.

### 1. Foundation score

Measures theorem-level, derivation-level, and object-level correctness on hidden technical tasks.

Suggested components:

- mathematical correctness
- explicit assumptions
- notation quality
- transfer into quant use

### 2. Implementation score

Measures whether the agent can deliver correct runnable code under framework constraints.

Suggested components:

- compile rate
- runtime success
- framework compliance
- implementation clarity

### 3. Research score

Measures the quality of research design and reasoning.

Suggested components:

- hypothesis quality
- economic or statistical rationale
- identification and test design
- diagnostics
- reproducibility
- final decision quality

### 4. Null-discipline score

Measures whether the agent correctly rejects bad ideas and weak evidence.

This should be treated as a first-class score, not a side note.

### 5. Robustness score

Measures whether surviving ideas remain credible after realistic validation.

Suggested components:

- out-of-sample behavior
- cost realism
- turnover and capacity awareness
- regime sensitivity
- multiple-testing awareness

### 6. Prospective score

Measures behavior after the research memo is frozen.

Suggested components:

- paper-trading stability
- adherence to declared rules
- drawdown behavior
- forecast versus realization discipline

### 7. Efficiency diagnostics

Track these, but keep them out of the main composite unless there is a strong reason:

- wall-clock runtime
- tool usage
- retrieval depth
- token or compute cost

## Suggested formulas

Let each score be normalized to the interval $[0, 100]$.

For rubric-based scores, use weighted averages rather than all-or-nothing pass rates:

$$
S_{\text{research}} = \sum_{i=1}^{k} w_i s_i,
$$

where $\sum_i w_i = 1$ and each $s_i \in [0, 100]$.

For null-task discipline, the simplest version is:

$$
S_{\text{null}} = 100 \left(1 - \frac{N_{\text{false accept}}}{N_{\text{null tasks}}}\right).
$$

This makes false positives expensive, which is desirable.

For domain-local lift after an ingest milestone, track:

$$
\Delta_{d,m} = S_{d,m}^{\text{after}} - S_{d,m}^{\text{before}},
$$

where $d$ is a domain tag and $m$ is a metric such as foundation, research, or robustness.

## Optional composite score

If a single dashboard number is needed, use it as a summary view only:

$$
S_{\text{vault}} =
0.15 S_{\text{foundation}} +
0.15 S_{\text{implementation}} +
0.25 S_{\text{research}} +
0.20 S_{\text{null}} +
0.15 S_{\text{robustness}} +
0.10 S_{\text{prospective}}.
$$

Independent judgment: do not optimize directly for this composite. It is too easy to Goodhart. The panel and the raw artifacts matter more.

## Pass gates

Before any task is counted as a serious success, require basic gates:

### Alpha or validation tasks

- reproducible code or explicit reproducible procedure
- no obvious leakage or timestamp violation
- realistic cost handling
- explicit go or no-go decision

### Foundation tasks

- mathematical statement is materially correct
- assumptions are not silently dropped
- notation is inspectable

### Research tasks

- the memo states what would falsify the idea
- the memo distinguishes evidence from speculation

## What to store each run

For each benchmark run, keep:

- benchmark regime
- vault snapshot identifier
- task list version
- per-task scores
- reviewer notes
- key failure categories
- aggregated panel scores
- domain-tag lift summary

That is the minimum needed to make longitudinal comparison honest.
