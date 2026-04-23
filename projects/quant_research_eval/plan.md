---
title: Quant Research Eval Suite Plan
type: project
status: active
updated: 2026-04-23
tags:
  - project
  - benchmark
  - plan
  - quant
  - evaluation
---
# Quant Research Eval Suite Plan

## Objective

Build a longitudinal evaluation protocol for the vault that can answer:

1. does the vault improve mathematical and statistical understanding?
2. does the vault improve actual quant research quality?
3. does the vault improve alpha validation discipline rather than only idea generation?
4. does any observed improvement survive hidden and prospective checks?

## Main experimental regimes

Use three regimes, not one.

### 1. Blind control

Same model, same local execution environment, same task, no vault access, no web.

Purpose:

- measure raw model capability
- stop us from attributing generic model improvement to the vault

### 2. Wiki-only regime

Allow access to `wiki/` and its retrieval surfaces, but not `projects/`, `raw/`, `catalog/`, or `artifacts/`.

Purpose:

- isolate the value of durable curated knowledge
- test whether promoted notes are actually doing useful work

### 3. Full-vault regime

Allow normal local vault access under the tool ladder:

- `wiki/`
- `projects/`
- `catalog/`
- `artifacts/`
- `raw/` when the task genuinely requires source-level evidence

Purpose:

- measure the value of the full research system, not only the durable wiki

Independent judgment: this is a better main comparison than splitting QMD and Obsidian into separate primary benchmark arms. QMD and Obsidian are tool surfaces, while the real object of evaluation is the vault as a knowledge system.

## Evaluation layers

### Layer A. Foundation mastery

Use hidden technical tasks drawn from the domains we ingest heavily:

- probability and statistics
- time series
- state space methods
- optimization
- stochastic calculus
- extreme value theory

Task types:

- explain a theorem with assumptions and consequences
- repair a flawed derivation
- identify the hidden condition missing from a proof sketch
- translate a formal result into quant-research use
- answer a source-grounded concept question with explicit notation

Deliverables:

- short technical memo
- equations in MathJax
- explicit assumptions and caveats

Why it matters:

This is the cleanest way to test whether book ingest is improving real understanding rather than only broad familiarity.

### Layer B. Implementation competence

Use executable tasks where real implementation details matter.

Primary implementation slices:

- remote research jobs against the full data warehouse
- reproducible validation scripts with manifest and artifact output
- IBKR read-only, dry-run, and paper-trading tasks

[QuantCode-Bench](../quantcode_bench/brief.md) remains a useful cheap Backtrader subtest, but it is not the main implementation exam.

Possible later extensions:

- vectorbt
- PyPortfolioOpt
- custom research notebooks
- small factor-pipeline coding tasks

Deliverables:

- runnable code
- short explanation of tradeoffs and limits

Why it matters:

A quant researcher who cannot implement correctly is not operationally useful.

### Layer C. Research design and falsification

Use tasks where the agent must decide what to test, how to test it, and whether the idea should be rejected.

Subfamilies:

- factor replication
- event-study design
- signal sanity checking
- model-diagnostic research
- risk-model or portfolio-research questions
- execution or market-microstructure research questions

Include explicit null tasks where the correct answer is:

- no robust edge
- evidence insufficient
- implementation impossible under the stated constraints

Deliverables:

- research memo
- test design
- code or pseudocode
- rejection or proceed decision

Why it matters:

False-positive control is one of the most important traits of a real quant researcher.

### Layer D. Alpha validation

Use tasks where a candidate factor or strategy already exists, and the agent must validate it properly.

Required checks should include, when relevant:

- timestamp alignment
- leakage and survivorship checks
- cost and turnover realism
- hidden out-of-sample testing
- regime robustness
- multiple-testing awareness

Independent judgment: this layer should score validation quality more heavily than headline return.

### Layer E. Prospective discipline

Use frozen paper portfolios or shadow-live research books.

Rules:

- predeclare the strategy definition
- predeclare rebalance cadence and risk limits
- do not revise the rule set midstream without starting a new run

Why it matters:

This is the closest cheap approximation to "can the system survive contact with the future?"

## Domain tagging and local-lift tracking

Every task should carry one or more domain tags, for example:

- `time_series`
- `state_space`
- `bayesian_filtering`
- `convex_optimization`
- `stochastic_calculus`
- `extreme_value_theory`
- `portfolio`
- `execution`
- `factor_modeling`

After a major ingest milestone, rerun the aligned shadow slice first.

Example:

- after ingesting an EVT book, rerun the `extreme_value_theory` slice
- after ingesting a state-space book, rerun `state_space` and `bayesian_filtering`

This gives a more believable causal signal than only watching one global score drift.

## Fixed controls

Hold these fixed inside a regime series:

- model name
- reasoning setting
- vault snapshot or git commit
- task set version
- data snapshot
- judge configuration
- time budget
- tool policy
- cost model
- transaction-cost assumptions

If one of these changes materially, record a new regime instead of pretending the score series is continuous.

## Standard task output package

Each evaluated task should produce:

- the task brief
- regime metadata
- retrieval trace or explicit no-retrieval statement
- final memo
- code
- key artifacts such as plots or diagnostics
- machine-readable score output
- reviewer notes when manual scoring is involved

Store bounded outputs in `artifacts/`, and keep planning or discussion notes in `projects/`.

## Rerun cadence

### Shadow suite

Run a fixed small subset:

- after each major source-shelf milestone
- after major tool or harness changes

Purpose:

- cheap regression tracking
- domain-local lift checks

### Full suite

Run the full suite:

- at the first serious baseline
- after major vault milestones
- after major model or harness regime changes

### Prospective review

Review frozen paper books on a slower cadence:

- monthly for health checks
- quarterly for serious comparison

## Immediate build order

1. freeze the three benchmark regimes
2. define the first shadow suite for each layer
3. define the first `remote_validation` task against the remote data warehouse
4. keep QuantCode-Bench as a cheap implementation subtest, not the primary exam
5. design the first hidden foundation task bank from ingested math and finance sources
6. design the first null-task bank for research falsification
7. define the artifact schema for storing results
8. run the first baseline across all three regimes

## Open risks

- manual review may still be needed for some foundation and research tasks
- a composite score can be gamed if it becomes the only target
- too much benchmark-specific prompting can turn the exercise into prompt engineering
- prospective evaluation is slower and noisier than offline evaluation

## Sources

- [QuantCode-Bench Brief](../quantcode_bench/brief.md)
- https://arxiv.org/abs/2602.18481
- https://arxiv.org/abs/2508.00828
- https://metr.org/blog/2024-11-22-evaluating-r-d-capabilities-of-llms/
- https://metr.org/blog/2025-08-12-research-update-towards-reconciling-slowdown-with-time-horizons/
- https://ssrn.com/abstract=2326253
- https://ssrn.com/abstract=2460551
- https://ssrn.com/abstract=2513152
- https://ssrn.com/abstract=4778909
