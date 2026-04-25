---
title: Phase 2 Task 002 Scored Falsification Pass
type: project
status: active
updated: 2026-04-24
tags:
  - project
  - phase2
  - falsification
  - scored
  - local-review
---
# Phase 2 Task 002 Scored Falsification Pass

## Objective

Run the first genuine agent-scored falsification pass using already reviewed Phase 1 and Phase 2 evidence.

This task exists because Task 001 proved only that the scaffold and remote artifact path work. It did not prove that the agent can independently decide `reject`, `revise`, or `proceed`.

## Task Package

- [task_bank_v1_scored.md](task_bank_v1_scored.md)
- [task_002_agent_packet.md](task_002_agent_packet.md)
- [task_002_answer_key.csv](task_002_answer_key.csv)
- [task_002_response_template.csv](task_002_response_template.csv)
- [task_002_manifest.yaml](task_002_manifest.yaml)
- [../../../research/research_falsification/score_phase2_falsification_responses.py](../../../research/research_falsification/score_phase2_falsification_responses.py)

## Workflow

1. give the answering agent only the agent packet and referenced evidence
2. do not give the answering agent the answer key
3. collect one response row per task in the response template
4. score the response file against the answer key with the local scoring script
5. review the strict and tolerant results locally before any Phase 2 closure discussion

## Required Outputs

Minimum outputs for a scored pass:

- `responses.csv`
- `scored_scorecard.csv`
- `metrics.json`
- `score_report.md`

Recommended artifact root:

```text
artifacts/phase2_scored_falsification/<YYYYMMDD>_<run_id>/
```

## Acceptance Standard

This task is useful only if:

- the answering agent did not use the answer key
- every task has an explicit decision
- every task has a short rationale tied to evidence
- false accepts are visible
- boundary-task handling is visible

## Current Judgment

This should be the next Phase 2 task before Phase 3.

The strongest reason is that the project still lacks an inspectable agent-decision score on falsification work. Until that exists, the evaluator is not mature enough for candidate-registry or search-loop work.

## Related Notes

- [Task 001 Local Review](task_001_local_review.md)
- [Build Sequence](../build_sequence.md)
- [Quant Research Eval Suite Scorecard](../../quant_research_eval/scorecard.md)
