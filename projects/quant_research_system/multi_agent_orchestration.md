---
title: Quant Research System Multi-Agent Orchestration
type: project
status: active
updated: 2026-04-24
tags:
  - project
  - architecture
  - multi-agent
  - orchestration
  - quant
---
# Quant Research System Multi-Agent Orchestration

## Decision Summary

Multi-agent structure can help this project, but only in a narrow, contract-driven form.

Adopted judgment:

- do not copy a large roster of personality agents into the quant system
- do use a small set of role contracts where each role has a bounded mission, tool surface, deliverables, and authority boundary
- do not assume every role is an LLM or subagent
- explicitly treat `data_execution_runner` as the remote machine role, not as a free-form conversational agent

The main value of multi-agent design for this project is:

- parallelism where research branches are genuinely independent
- adversarial separation between proposal and falsification
- explicit authority boundaries between remote execution, local review, and broker-facing implementation
- better observability through role-specific outputs

The main risk is unnecessary complexity. If a task is linear, tightly coupled, or demands one coherent mathematical argument, one strong agent with a good workflow is better than a committee.

## Why The Agency-Style Roster Is The Wrong Default

The `agency-agents` repository is useful as a formatting reference because it makes specialist roles explicit.

It is not the right design to import directly.

Reasons:

- it is broad, personality-heavy, and optimized for many general workflows rather than one quant-research system
- it does not define the evidence hierarchy, evaluator discipline, or phase authority boundaries that our project requires
- it treats roles mainly as prompt-specialists, while our system also needs environment roles and machine roles
- a large roster would increase orchestration cost before our evaluator is mature

What is worth borrowing is the role-card idea:

- role name
- purpose
- when to use
- allowed tools
- forbidden tools
- required outputs
- decision authority
- handoff format
- failure gates

## Core Design Principle

Not every node in a multi-agent system should be an LLM.

For this project, there are three different role classes:

1. reasoning roles
   LLM-based roles that plan, critique, or synthesize
2. execution roles
   script- or environment-driven roles that run manifests and return artifacts
3. control roles
   local review roles that decide whether evidence is accepted, promoted, revised, or rejected

This matters because `data_execution_runner` should not be modeled as "another smart assistant." It should be modeled as:

- the remote Ubuntu/GPU machine
- the remote environment contract
- the manifest runner
- the artifact bundle producer

If a remote LLM is later used to operate that machine, that LLM is still subordinate to the machine role and its contract. The role is defined by environment and deliverables, not by agent personality.

## Adopted Minimal Role Set

### 1. `research_supervisor`

Environment:

- local control plane

Purpose:

- decompose work
- choose whether a task should stay single-agent or become multi-role
- assign bounded role contracts
- integrate outputs into one inspectable project decision

Authority:

- may recommend `reject`, `revise`, `proceed`, or `paper-test`
- does not overrule raw data, artifacts, or local human review

Required outputs:

- task decomposition
- explicit handoffs
- final integrated memo

### 2. `statistical_falsifier`

Environment:

- local reasoning role

Purpose:

- attack leakage, multiple testing, null-model weakness, disguised exposures, and nonstationary narratives

Authority:

- may recommend rejection
- does not close phases

Required outputs:

- falsification memo
- failure categories
- missing-check list

### 3. `artifact_auditor`

Environment:

- local review role

Purpose:

- verify artifact completeness, hashes, manifest fields, git snapshots, diagnostics, and unsupported claims

Authority:

- can block artifact acceptance
- cannot promote a strategy to alpha by itself

Required outputs:

- artifact intake checklist
- audit note
- accepted or blocked status for evidence intake

### 4. `data_execution_runner`

Environment:

- remote Ubuntu/GPU machine

Identity:

- this role is the remote machine plus its manifest-and-artifact protocol
- it is not a generic subagent persona

Purpose:

- load full datasets
- run remote validation jobs
- run falsification suites
- produce compact artifact bundles
- return runtime and reproducibility metadata

Allowed inputs:

- pinned git commit
- manifest
- remote dataset paths
- evaluator scripts

Forbidden actions:

- no phase closure decisions
- no IBKR/TWS access
- no broker credentials
- no local wiki governance decisions
- no silent task redefinition

Required outputs:

- artifact bundle
- run metadata
- warning and failure counts
- non-binding recommendation such as `accept_artifacts`, `revise_and_rerun`, or `blocked`

### 5. `implementation_translator`

Environment:

- local IBKR/TWS-adjacent role

Purpose:

- turn a strategy specification into target books, contract-resolution requests, order intents, and static risk checks

Authority:

- can reject broker-facing readiness
- cannot claim alpha validity

Required outputs:

- `strategy_spec.md`
- `target_portfolio.csv`
- `contract_resolution_requests.csv`
- `order_intents.json`
- `risk_check_report.md`
- `implementation_caveats.md`

### 6. `math_foundation_reviewer`

Environment:

- local reasoning role

Purpose:

- review theorem-level, derivation-level, or object-level understanding when a note or method is mathematically load-bearing

Authority:

- can force a note or method back into `revise`
- does not decide portfolio deployment

Required outputs:

- theorem and assumption audit
- notation corrections
- failure-mode clarifications

## Activation Policy

Do not activate all roles by default.

Use the minimal role set that actually reduces risk for the current phase.

Current phase guidance:

- Phase 2 remote falsification:
  `research_supervisor` + `data_execution_runner` + `artifact_auditor`
- Phase 2 hidden or adversarial falsification expansion:
  add `statistical_falsifier`
- Phase 2B strategy-to-IBKR translation:
  `research_supervisor` + `implementation_translator` + `artifact_auditor`
- Phase 4 search loop:
  likely `research_supervisor` + bounded proposer role + `statistical_falsifier` + `data_execution_runner` + `artifact_auditor`

Independent judgment:

- the system should stay mostly single-agent through the first real Phase 2 run
- the first justified multi-role addition after that is `artifact_auditor` as an explicit review role
- the next justified addition is `statistical_falsifier`
- full search-time proposer/evaluator separation belongs later, after candidate lineage and evaluator stability improve

## Authority And Memory Rules

All role outputs must remain inspectable in the vault or artifacts.

Rules:

- final phase decisions remain local
- remote roles produce evidence and recommendations only
- broker-facing readiness remains local because IBKR/TWS access is local-only
- durable knowledge still belongs in `wiki/`, not in transient role memory
- role memory should be explicit project context, not hidden reliance on model memory

## Rejected Designs

Rejected for now:

- a large general-purpose roster of dozens or hundreds of specialists
- free-form peer chat among many equal agents with no authority hierarchy
- remote broker-facing execution roles
- debate-style multi-agent reasoning as a default for quant research
- adding a multi-agent runtime before Phase 2 evidence discipline is working

Why:

- our main bottleneck is evaluator quality and evidence discipline, not lack of agent variety
- too many roles too early will obscure failures and make reproduction harder
- quant tasks often require one coherent chain of mathematical and statistical reasoning

## Recommended Next Step

Do not build a general multi-agent framework yet.

The next justified step is smaller:

1. finish the first remote Phase 2 falsification run
2. create one reusable role-card template
3. instantiate only two explicit operational roles beyond the default agent:
   `artifact_auditor` and `data_execution_runner`
4. add `statistical_falsifier` only after the first falsification artifacts are reviewed locally

This keeps the system aligned with the current bottleneck instead of solving a later orchestration problem too early.

## Role-Card Template

Recommended fields:

```text
name
role_class
environment
purpose
when_to_use
inputs
allowed_tools
forbidden_tools
required_outputs
handoff_format
decision_authority
failure_gates
success_metrics
```

If this template is later promoted into a reusable vault method, it should move out of this project note.

## Related Notes

- [Quant Research System Architecture](architecture.md)
- [Quant Research System Build Sequence](build_sequence.md)
- [Quant Research System Environments](environments.md)
- [Remote Data and GPU Workflow](remote_workflow.md)
- [Strategy-to-IBKR Translation Smoke Test](execution_translation_smoke_test.md)

## Sources

- https://github.com/msitarzewski/agency-agents
- https://www.anthropic.com/engineering/built-multi-agent-research-system
- https://langchain-ai.github.io/langgraphjs/reference/modules/langgraph-supervisor.html
- https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/index.html
- https://doi.org/10.48550/arXiv.2407.01489
