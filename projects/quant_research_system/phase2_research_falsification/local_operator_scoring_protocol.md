---
title: Phase 2 Local Operator And Scoring Protocol
type: project
status: active
updated: 2026-04-24
tags:
  - project
  - phase2
  - protocol
  - scoring
---
# Phase 2 Local Operator And Scoring Protocol

## Purpose

This protocol defines the exact role split for a scored Phase 2 run.

The goal is to keep the answering agent, the scorer, and the reviewer from leaking into each other.

## Role Split

### 1. Local operator

Responsible for:

- preparing the run folder
- controlling packet handoff
- keeping the answer key away from the answering agent
- recording the independence attestation

### 2. Answering agent

Responsible for:

- reading only the packet and cited evidence
- filling `responses.csv`
- writing optional memos if needed

### 3. Local scoring role

Responsible for:

- running the scoring script against `responses.csv`
- producing `scored_scorecard.csv`, `metrics.json`, and `score_report.md`
- not changing the answering agent's decisions

### 4. Local reviewer

Responsible for:

- deciding whether the run is accepted
- deciding what the run means for Phase 2
- recording the project-level review note

## Exact Sequence

1. Prepare a dedicated artifact run folder.
2. Copy a run-local packet and blank `responses.csv` into that folder.
3. Keep the answer key outside the answering agent's working set.
4. Record the exact handoff prompt and intended answering-agent session label in the run-local operator log before or at handoff time.
5. Send only the run-local packet and cited evidence to the answering agent.
6. Receive a filled `responses.csv` in the artifact run folder.
7. Complete the operator log with return time and any deviations.
8. Record the independence attestation.
9. Run the scoring script locally.
10. Review the scored outputs locally.

## Preparation Rule

Use the run-prep script before the answering-agent handoff.

The run-prep script should create:

- `packet.md`
- `responses.csv`
- `task_manifest.yaml`
- `independence_attestation.md`
- `operator_handoff_record.md`
- `handoff_prompt.txt`
- `run_instructions.md`

Do not hand the answering agent the reusable project template as the live response file.

## Handoff Logging Rule

The local operator must preserve a minimal machine-readable or markdown trail for the handoff.

At minimum record:

- the exact prompt used to brief the answering agent
- the answering-agent session label if available
- handoff time
- return time
- any deviation from packet-only evidence access

If the handoff is relayed through a human instead of directly by the local operator, say that explicitly in the operator log and later review note rather than overstating independence.

## Scoring Rule

The scoring script must be run only after the answering agent has finished.

The scoring role must not:

- edit the agent's decisions
- fill blank decisions on the agent's behalf
- relax the answer key after seeing weak responses

## Review Rule

A run is not complete just because `metrics.json` exists.

The local reviewer must still decide:

- whether the independence controls were adequate
- whether the task bank is strong enough
- whether the phase should remain open or close

## Related Notes

- [Phase 2 Answering Agent Protocol](answering_agent_protocol.md)
- [Phase 2 Independence Attestation Template](independence_attestation_template.md)
