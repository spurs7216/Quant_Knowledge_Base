---
title: Quant Research System Environments
type: project
status: active
updated: 2026-04-23
tags:
  - project
  - environments
  - evaluator
  - quant
---
# Quant Research System Environments

## Environment contract

Every research environment should define:

- objective
- candidate artifact type
- allowed data
- tool policy
- evaluator cascade
- hidden tests
- output bundle
- pass gates
- human approval points

An environment is not just a folder. It is a bounded game whose scoring rules are known before the candidate is generated.

Current execution-location rule: IBKR TWS access is local-only. Remote environments may evaluate historical data, null models, statistical robustness, and implementation-feasibility proxies, but they must not require TWS, IB Gateway, account state, position state, broker credentials, contract lookup, or order submission.

## Environment 1. `remote_validation`

### Purpose

Test whether a proposed factor, strategy, or model survives disciplined historical validation on the remote warehouse.

### Candidate artifacts

- factor definition
- feature pipeline
- forecast model
- portfolio construction rule
- strategy research script

### Inputs

- dataset paths selected from `catalog/`
- universe definition
- date range
- train / validation / hidden-test split
- cost model
- benchmark model or null model

### Evaluator cascade

1. schema and manifest validation
2. data availability and identifier checks
3. timestamp and leakage checks
4. small-sample smoke run
5. full remote run
6. out-of-sample evaluation
7. robustness battery
8. final memo and decision

### Pass gates

- no obvious leakage
- reproducible job manifest
- explicit universe and date range
- explicit cost assumptions
- evidence bundle synced back
- proceed / revise / reject decision recorded

## Environment 2. `research_falsification`

### Purpose

Test whether the agent can reject weak or non-identifiable ideas.

### Candidate artifacts

- research memo
- diagnostic script
- null-test result
- falsification checklist

### Task examples

- given a noisy signal, decide whether evidence supports further work
- detect that a result comes from look-ahead leakage
- show that a factor is mostly a disguised exposure
- prove that available data cannot answer the proposed question

### Evaluator cascade

1. claim extraction
2. data feasibility check
3. leakage and bias checklist
4. null-model comparison
5. decision scoring

### Pass gates

- the agent must be allowed to answer "reject"
- false accepts are penalized more than false rejects
- memo distinguishes evidence from speculation

## Environment 2B. `implementation_translation_smoke`

### Purpose

Test whether a strategy rule can be translated into broker-facing artifacts before full IBKR paper trading exists.

This environment is earlier and cheaper than `implementation_execution`. It is no-send by design.

This environment is local-control-plane work. It may be run without connecting to IBKR if it only generates reviewable artifacts. If it uses IBKR metadata or account context, it must run on the local machine where TWS access exists, not on the remote warehouse/GPU machine.

### Candidate artifacts

- target portfolio table
- target-delta or rebalance instruction table
- contract-resolution request table
- order-intent JSON
- static risk-check report
- implementation caveat report

### Evaluator cascade

1. strategy rule completeness check
2. target-portfolio schema check
3. contract field completeness check
4. no-send order-intent validation
5. static risk checks
6. implementation caveat scoring

### Pass gates

- no live-order submission
- no credentials in the vault
- explicit account mode and paper-only assumption
- explicit notional and quantity caps
- explicit order type and time-in-force
- ambiguous contracts rejected
- shorting and borrow assumptions identified
- cancel or flattening plan stated

### Role in build order

Run this after Phase 1 and alongside Phase 2 falsification. It should catch implementation-impossible ideas before candidate search scales them.

## Environment 3. `implementation_execution`

### Purpose

Test deployable implementation mechanics, especially IBKR paper-trading workflow.

This environment is local-only under the current infrastructure because only the local machine has IBKR TWS access.

### Candidate artifacts

- contract-resolution script
- order-ticket construction logic
- paper-trading strategy shell
- execution reconciliation script
- risk-limit guard

### Evaluator cascade

1. static safety checks
2. paper-account read-only checks
3. contract resolution
4. market-data request checks
5. dry-run order construction
6. paper order submission when explicitly enabled
7. order status, fill, cancellation, and position reconciliation

### Pass gates

- paper account only
- explicit live-trading lock
- order size limits
- cancellation path exists
- reconciliation output is stored
- no credentials in the vault

### Current limitation

The currently exposed IBKR MCP tools are read-only: historical data, fundamentals, account summary, and positions. They are available only from the local machine's IBKR/TWS setup. A true execution environment requires a local TWS API, IB Gateway, or Client Portal API harness for order placement.

The remote Ubuntu data/GPU machine must not be used for IBKR execution tasks unless a separate broker environment is deliberately installed, isolated, and approved later.

## Environment 4. `foundation_mastery`

### Purpose

Test whether the vault improves theorem-level and method-level understanding.

### Candidate artifacts

- technical memo
- derivation repair
- assumption audit
- method comparison

### Evaluator cascade

1. source-grounded retrieval check
2. theorem or object statement
3. assumption and failure-mode audit
4. quant transfer explanation
5. human review when needed

### Pass gates

- equations use MathJax
- assumptions are explicit
- unsupported claims are penalized

## Environment 5. `prospective_paper`

### Purpose

Test behavior after a strategy is frozen.

### Candidate artifacts

- paper portfolio definition
- rebalance rule
- risk limits
- monitoring report

### Evaluator cascade

1. predeclared rule check
2. paper execution or simulated forward run
3. risk and drawdown monitoring
4. rule adherence check
5. monthly or quarterly review

### Pass gates

- no rule changes inside the same run
- performance interpreted with uncertainty
- failures recorded, not hidden

## Environment order

Build in this order:

1. `remote_validation`
2. `research_falsification`
3. `implementation_translation_smoke` local no-send order-intent checks
4. `implementation_execution` local read-only and dry-run
5. `foundation_mastery` hidden shadow suite
6. `prospective_paper`

This order prioritizes false-positive control and real data access before brokerage-facing automation.
