---
title: Quant Research System Build Sequence
type: project
status: active
updated: 2026-04-25
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

Execution realism should be tested earlier than full paper trading.

There are two different questions:

- Can the agent turn a strategy rule into safe broker-facing target positions, contract-resolution requests, order intents, and risk checks?
- Should the strategy actually be submitted to an IBKR paper account?

The first question should be examined early in no-send mode because it catches non-implementable research logic before large-scale search compounds it. The second question stays later because even paper order lifecycle work needs stronger safety, reconciliation, and account-control infrastructure.

IBKR/TWS access is currently local-only. Remote machines can run historical falsification and validation jobs, but they must not be assigned broker-facing TWS, account, position, contract lookup, paper order, or live order tasks.

Multi-agent structure is not a separate early phase by itself. It is an orchestration pattern that should be introduced only where it lowers error rate or coordination cost. See [Quant Research System Multi-Agent Orchestration](multi_agent_orchestration.md).

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

Status: `closed` on 2026-04-23.

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

Status: `closed` on 2026-04-24 after Task 004 local review.

Goal:

Make rejection discipline explicit before search.

Foundation scope:

- create 5 null tasks
- create evaluator checklist
- score false accepts
- store decisions and failure reasons
- include implementation-feasibility flags when a strategy is obviously not tradable, not borrowable, not contract-resolvable, or not orderable under the intended broker constraints

Exit criteria:

- agent can correctly reject at least some weak ideas
- false accepts are visible in scorecard
- rejected ideas include both statistical failures and implementation-feasibility failures when applicable
- a scored run records an independence-control trail
- the scored bank is not only a plainly visible set of canonical answers
- the scored bank includes at least one serious `proceed` task

Phase package:

- [phase2_research_falsification/README.md](phase2_research_falsification/README.md)
- [phase2_research_falsification/task_bank_v0.md](phase2_research_falsification/task_bank_v0.md)
- [phase2_research_falsification/task_bank_v1_scored.md](phase2_research_falsification/task_bank_v1_scored.md)
- [phase2_research_falsification/task_bank_v2_requirements.md](phase2_research_falsification/task_bank_v2_requirements.md)
- [phase2_research_falsification/evaluator_checklist.md](phase2_research_falsification/evaluator_checklist.md)
- [phase2_research_falsification/task_001_daily_stock_falsification_suite.md](phase2_research_falsification/task_001_daily_stock_falsification_suite.md)
- [phase2_research_falsification/task_001_manifest.yaml](phase2_research_falsification/task_001_manifest.yaml)
- [phase2_research_falsification/task_002_scored_falsification_pass.md](phase2_research_falsification/task_002_scored_falsification_pass.md)
- [phase2_research_falsification/task_003_hardened_scored_falsification_pass.md](phase2_research_falsification/task_003_hardened_scored_falsification_pass.md)
- [phase2_research_falsification/task_004_operator_controlled_scored_pass.md](phase2_research_falsification/task_004_operator_controlled_scored_pass.md)
- [phase2_research_falsification/answering_agent_protocol.md](phase2_research_falsification/answering_agent_protocol.md)
- [phase2_research_falsification/local_operator_scoring_protocol.md](phase2_research_falsification/local_operator_scoring_protocol.md)

## Phase 2B. Strategy-to-IBKR translation smoke test

Status: `closed` on 2026-04-24 after Task 001 local review.

Goal:

Test whether the agent can translate a strategy specification into broker-safe implementation artifacts without sending orders.

Foundation scope:

- take one validated-or-revised strategy spec, initially Task 001 or a deliberately toy target book
- express the intended target portfolio and rebalance logic
- map symbols or identifiers into explicit IBKR contract-resolution requests
- generate order-intent objects with `transmit=false` or equivalent no-send semantics
- run static risk checks: account mode, notional cap, order size, short-sale caveats, cancel path, no credentials
- save a compact implementation-readiness report

Phase package:

- [execution_translation_smoke_test.md](execution_translation_smoke_test.md)
- [phase2b_implementation_translation/README.md](phase2b_implementation_translation/README.md)
- [phase2b_implementation_translation/task_001_representative_book_translation.md](phase2b_implementation_translation/task_001_representative_book_translation.md)
- [phase2b_implementation_translation/task_001_local_review.md](phase2b_implementation_translation/task_001_local_review.md)

Non-goal:

- do not run this through the remote Linux/GPU machine as if it had TWS access
- do not submit paper orders in Phase 2B
- do not treat successful order-intent generation as alpha evidence

Exit criteria:

- one strategy-to-order translation task passes static safety checks
- failure modes are visible when contract, borrow, sizing, or rebalance assumptions are underspecified
- generated artifacts can be reviewed without connecting to a live or paper order-submission endpoint

## Phase 3. Candidate registry

Status: `active` as of 2026-04-25. Task 001 seeded the registry from Phase 1 and Phase 2B artifacts; Task 002 added manifest-driven candidate registration; Task 003 added status-update and event intake; Task 004 created an executable remote-validation handoff; Task 005 prepared the remote execution packet.

Goal:

Track candidate lineage.

Foundation scope:

- candidate id
- parent id
- artifact type
- patch or code path
- evaluator result
- status: rejected, active, promoted, paper-test, superseded

Phase package:

- [phase3_candidate_registry/README.md](phase3_candidate_registry/README.md)
- [phase3_candidate_registry/candidate_registry_schema.md](phase3_candidate_registry/candidate_registry_schema.md)
- [phase3_candidate_registry/candidate_registry.csv](phase3_candidate_registry/candidate_registry.csv)
- [phase3_candidate_registry/candidate_event_log.csv](phase3_candidate_registry/candidate_event_log.csv)
- [phase3_candidate_registry/candidate_manifest.template.yaml](phase3_candidate_registry/candidate_manifest.template.yaml)
- [phase3_candidate_registry/candidate_status_update.template.yaml](phase3_candidate_registry/candidate_status_update.template.yaml)
- [phase3_candidate_registry/task_001_seed_registry.md](phase3_candidate_registry/task_001_seed_registry.md)
- [phase3_candidate_registry/task_002_manifest_registration.md](phase3_candidate_registry/task_002_manifest_registration.md)
- [phase3_candidate_registry/task_003_evaluation_intake.md](phase3_candidate_registry/task_003_evaluation_intake.md)
- [phase3_candidate_registry/task_004_remote_validation_handoff.md](phase3_candidate_registry/task_004_remote_validation_handoff.md)
- [phase3_candidate_registry/task_005_remote_execution_packet.md](phase3_candidate_registry/task_005_remote_execution_packet.md)

Exit criteria:

- candidate history is inspectable
- repeated experiments do not disappear into chat history
- a new candidate can be added from a manifest without changing the schema
- an existing candidate can receive review or evaluator updates through a status-update manifest
- one registered candidate can be handed to remote validation with an executable script and draft job manifest
- a remote execution packet and artifact-intake checklist exist before the run is claimed
- registry validation passes before Phase 4 search creates child candidates

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

Test local brokerage integration without order risk, building on the earlier Phase 2B strategy-to-order smoke test.

Foundation scope:

- local read-only account and position checks
- market-data request checks
- contract-resolution tasks
- dry-run order construction

Exit criteria:

- no live orders
- order tickets pass static risk checks
- evidence artifacts are stored

## Phase 6. IBKR paper-trading layer

Goal:

Test local paper execution lifecycle.

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

## Current next decision

Phase 2B is closed within its scoped objective, and Phase 3 has started.

What is established:

- the remote falsification scaffold works end to end on the full `daily_stock` file
- explicit agent-side falsification decisions can be scored against a separate answer key
- later scored runs include `reject`, `revise`, and `proceed`
- the operator-controlled run preserved the main anti-leak boundary and recorded the exact handoff prompt
- the current evaluator stack shows zero false accepts in the hardened and operator-controlled passes
- one revised strategy can now be translated into explicit no-send broker-facing artifacts with paper-only safety locks

Why the system should still not jump directly to search:

- the benchmark bank is still small and internal
- candidate registry should come before search so candidate lineage does not disappear into chat history
- later IBKR read-only and dry-run stages still need live local broker metadata and order-construction verification

The next concrete choice is:

- recommended next: commit and sync the exact Phase 3 packet for `CAND-20260425-002` when the remote machine is ready, then run the remote job and ingest returned evidence through the status-update path
- defer: search loop and paper-order submission until candidate lineage and later IBKR stages exist

Independent judgment: Phase 2 falsification and Phase 2B translation are strong enough to leave cleanly. Phase 3 should close only after a registered candidate can be handed to remote validation and the result can be ingested back into the registry without provenance loss.
