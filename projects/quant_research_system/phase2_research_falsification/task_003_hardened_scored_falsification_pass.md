---
title: Phase 2 Task 003 Hardened Scored Falsification Pass
type: project
status: active
updated: 2026-04-24
tags:
  - project
  - phase2
  - falsification
  - scored
  - hardening
---
# Phase 2 Task 003 Hardened Scored Falsification Pass

## Objective

Run the next scored falsification pass under stricter workflow controls and stronger task-bank design.

This task exists because Task 002 was informative but not sufficient for clean Phase 2 closure.

## Required Improvements Over Task 002

- use a prepared artifact-local packet and response file
- record an operator attestation for answer-key independence
- include less-visible task presentation or stronger answer-key separation
- include at least one real `proceed` task

## Task Package

- [task_bank_v2_hardened.md](task_bank_v2_hardened.md)
- [task_003_agent_packet.md](task_003_agent_packet.md)
- [task_003_answer_key.csv](task_003_answer_key.csv)
- [task_003_response_template.csv](task_003_response_template.csv)
- [task_003_manifest.yaml](task_003_manifest.yaml)
- [../../../research/research_falsification/prepare_phase2_scored_run.py](../../../research/research_falsification/prepare_phase2_scored_run.py)
- [../../../research/research_falsification/score_phase2_falsification_responses.py](../../../research/research_falsification/score_phase2_falsification_responses.py)

## Required Protocol

- [Phase 2 Answering Agent Protocol](answering_agent_protocol.md)
- [Phase 2 Local Operator And Scoring Protocol](local_operator_scoring_protocol.md)
- [Phase 2 Independence Attestation Template](independence_attestation_template.md)
- [Phase 2 Task Bank V2 Requirements](task_bank_v2_requirements.md)

## Acceptance Standard

Task 003 is useful only if:

- the workflow controls are actually followed
- the task bank is no longer only visible hard rejects and revise boundaries
- the scoring artifacts are complete
- local review addresses the independence record and the richer decision-class coverage

## Current Judgment

Task 003 is now the gating task for Phase 2 closure.

Phase 2 should remain open until Task 003 or an equivalent hardened pass is reviewed locally.
