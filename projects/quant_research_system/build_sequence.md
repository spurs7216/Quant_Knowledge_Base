---
title: Quant Research System Build Sequence
type: project
status: active
updated: 2026-04-23
tags:
  - project
  - roadmap
  - system-design
  - quant
---
# Quant Research System Build Sequence

## Build principle

Do not optimize for smallness.

The target is a robust, useful, reusable, and learnable quant-research system. If the system needs complexity to support real data, real validation, remote compute, execution safety, and long-term learning, then the system should be complex.

The constraint is not "keep it small." The constraint is:

- keep complexity modular
- keep interfaces explicit
- keep evidence inspectable
- keep runs reproducible
- keep failures and rejected ideas visible
- keep the system learnable by future agents and by the human researcher

Build in phases because staged construction controls risk and reveals bad assumptions early, not because minimalism is the goal.

Search without good evaluation accelerates overfitting, so evaluator quality and artifact provenance remain first-class design requirements.

## Phase 0. Freeze design assumptions

Outputs:

- architecture note
- environment contracts
- remote job manifest schema
- artifact bundle schema
- GitHub synchronization policy
- remote environment policy for the Ubuntu machine
- IBKR safety hierarchy

Exit criteria:

- human agrees on the first environment to build
- GitHub sync path and branch policy are clear enough for Phase 1
- remote environment choice is recorded or deliberately deferred
- code snapshot fields are defined
- manual artifact review path is defined

## Phase 1. Remote validation foundation

Goal:

Run one end-to-end remote validation job from local manifest to synced artifact bundle.

Foundation scope:

- use one remote dataset family, likely `daily_stock`
- use one auditable candidate factor or strategy
- run one train / validation / test split
- return metrics and diagnostics to `artifacts/`

Phase package:

- [phase1_remote_validation/README.md](phase1_remote_validation/README.md)
- [phase1_remote_validation/remote_job_manifest.template.yaml](phase1_remote_validation/remote_job_manifest.template.yaml)
- [phase1_remote_validation/artifact_bundle_schema.md](phase1_remote_validation/artifact_bundle_schema.md)
- [phase1_remote_validation/preflight_checklist.md](phase1_remote_validation/preflight_checklist.md)
- [phase1_remote_validation/task_001_daily_stock_short_reversal.md](phase1_remote_validation/task_001_daily_stock_short_reversal.md)

Exit criteria:

- manifest exists
- remote run completes
- artifact bundle syncs back, or local artifact import is explicitly waived by the human
- local project note records proceed / revise / reject
- local or human-reviewed project note records the final phase-close decision

Remote machines and remote agents produce evidence and recommendations. They do not have final authority to close phases.

## Phase 2. Research falsification tasks

Goal:

Make rejection discipline explicit.

Foundation scope:

- create 5 null tasks
- create evaluator checklist
- score false accepts
- store decisions and failure reasons

Exit criteria:

- agent can correctly reject at least some weak ideas
- false accepts are visible in scorecard

## Phase 3. Candidate registry

Goal:

Track candidate lineage.

Foundation scope:

- candidate id
- parent id
- artifact type
- patch or code path
- evaluator result
- status: rejected, active, promoted, paper-test

Exit criteria:

- candidate history is inspectable
- repeated experiments do not disappear into chat history

## Phase 4. Search loop

Goal:

Add AlphaEvolve-style iterative improvement.

Foundation scope:

- patch one bounded artifact region
- evaluate through remote validation cascade
- keep best survivors and diverse alternatives
- do not evolve whole notebooks

Exit criteria:

- search improves at least one validation metric without breaking gates
- failure modes are logged

## Phase 5. IBKR read-only and dry-run layer

Goal:

Test execution implementation without order risk.

Foundation scope:

- read-only account and position checks
- market-data request checks
- contract-resolution tasks
- dry-run order construction

Exit criteria:

- no live orders
- order tickets pass static risk checks
- evidence artifacts are stored

## Phase 6. IBKR paper-trading layer

Goal:

Test paper execution lifecycle.

Foundation scope:

- paper order submission
- order status tracking
- cancellation
- fill reconciliation
- position and cash checks

Exit criteria:

- paper-only safety confirmed
- lifecycle events are captured
- system can flatten or cancel safely

## Phase 7. Prospective paper books

Goal:

Measure frozen strategy behavior through time.

Foundation scope:

- one predeclared strategy
- fixed rebalance cadence
- fixed risk limits
- monthly review

Exit criteria:

- no mid-run rule changes
- forward evidence is recorded honestly

## Immediate next decision

The next concrete choice is which foundation environment to build first:

- recommended: `remote_validation`
- alternative: `implementation_execution` read-only IBKR checks

Independent judgment: build `remote_validation` first. It is the highest-leverage path because it connects the vault, real data, evaluators, and artifacts while avoiding premature trading API risk.
