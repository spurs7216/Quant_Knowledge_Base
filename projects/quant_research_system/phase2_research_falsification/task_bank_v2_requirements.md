---
title: Phase 2 Task Bank V2 Requirements
type: project
status: active
updated: 2026-04-24
tags:
  - project
  - phase2
  - task-bank
  - hardening
---
# Phase 2 Task Bank V2 Requirements

## Purpose

These requirements define what must change before Phase 2 can close cleanly.

The current scored pass was useful, but it still leaves three meaningful caveats:

- weak independence controls
- visible-bank exposure
- no serious `proceed` task

## Required Fixes

### 1. Independence controls

The next scored pass must include:

- run-local packet handoff
- run-local `responses.csv`
- independence attestation recorded by the operator
- no editing of reusable templates

### 2. Less-visible evaluation

The next scored pass must not rely only on a bank whose canonical answers are obvious from the project files.

At minimum, the next pass should include either:

- a task packet that does not expose the canonical decision structure directly, or
- a human-held or operator-controlled answer-key layer that the answering agent never sees

### 3. Mixed decision classes

The next scored bank must include at least one task whose canonical answer is `proceed`.

Reason:

- a system can score well on `reject` and `revise` tasks while still failing to recognize when evidence is actually good enough to move forward
- a serious evaluator must separate "stop", "repair", and "advance"

## Minimum V2 Shape

The next bank should include:

- at least one hard `reject`
- at least one boundary `revise`
- at least one real `proceed`
- at least one implementation-feasibility task
- at least one task where the attractive metric is a trap

## Evidence Quality Rule

Do not fabricate a `proceed` task just to satisfy class coverage.

The `proceed` task must be backed by actual evidence that survives:

- timing sanity
- explicit cost assumptions
- nontrivial diagnostics
- local review

## Implication

Phase 2 should remain open until these requirements are satisfied by a new scored pass and reviewed locally.
