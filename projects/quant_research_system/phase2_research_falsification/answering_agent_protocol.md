---
title: Phase 2 Answering Agent Protocol
type: project
status: active
updated: 2026-04-24
tags:
  - project
  - phase2
  - protocol
  - evaluation
---
# Phase 2 Answering Agent Protocol

## Purpose

This protocol exists to prevent the answering agent from accidentally contaminating a scored falsification run.

The answering agent is not the scorer, not the phase reviewer, and not the owner of the answer key.

## Allowed Inputs

The answering agent may read only:

- the run-local packet copied into the assigned artifact folder
- the evidence files cited by that packet
- the run-local `handoff_prompt.txt` if the operator created one
- optional run-local memo templates if the operator created them

The answering agent must not be pointed at the reusable project templates as the working files for the run.

## Forbidden Files

The answering agent must not read or open:

- any `*answer_key*` file
- any scoring script such as `score_phase2_falsification_responses.py`
- any existing `scored_scorecard.csv`
- any existing `score_report.md`
- any phase-close or local-review note for the task being answered
- any file that directly states expected or canonical decisions

## Allowed Writes

The answering agent may write only inside the assigned artifact run folder.

Allowed outputs:

- `responses.csv`
- optional per-task markdown memos under `memos/`

Forbidden writes:

- do not edit files under `projects/quant_research_system/phase2_research_falsification/`
- do not edit reusable templates in place
- do not edit manifests, answer keys, score reports, or review notes

## Required Response Standard

For every task:

- choose exactly one of `reject`, `revise`, or `proceed`
- fill one row in `responses.csv`
- write a non-empty `decision_summary`
- write a non-empty `evidence_path`
- use `memo_path` only if a longer memo is actually created

The answering agent must not leave any task blank.

## Reasoning Standard

The answering agent should:

- tie the decision to cited evidence
- separate statistical defects, leakage or timing defects, and implementation defects when relevant
- resist promoting a task because one attractive split looks good
- avoid "always reject" behavior when the evidence really supports `revise`

## Forbidden Behaviors

- do not compute or guess the final score
- do not compare against an answer key
- do not rewrite the task bank
- do not make a phase-close recommendation
- do not move the run to a different folder structure

## Operator Handoff Rule

If the packet is incomplete, the evidence paths are broken, or the operator gave the answering agent only the reusable template instead of a run-local `responses.csv`, stop and return the issue rather than improvising around it.

If the operator created a run-local `handoff_prompt.txt`, follow it rather than asking for broader project context.

## Related Notes

- [Phase 2 Local Operator and Scoring Protocol](local_operator_scoring_protocol.md)
- [Phase 2 Independence Attestation Template](independence_attestation_template.md)
