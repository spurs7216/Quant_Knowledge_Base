---
title: Qwen27B Mechanism Cards Failure Review 2026-05-15
type: project
status: active
updated: 2026-05-15
tags:
  - project
  - phase4
  - alphaevolve
  - qwen
  - mechanism-cards
sources:
  - "artifacts/qwen27b_attempt017_mechanism_cards_20260514.zip"
  - "controller_attempt017_27b_mechanism_cards_remote_instructions_20260514.md"
---
# Qwen27B Mechanism Cards Failure Review 2026-05-15

## Diagnosis

The run did not fail because 27B could not produce useful mechanism cards. The first launch at
`--max-model-len 8192` was too small for the prompt, but the restarted 16384-context server accepted
the request and returned content.

The actual parsing failure was output truncation:

```yaml
served_model: qwen35-27b-fp8
prompt_tokens: 8143
completion_tokens: 1536
total_tokens: 9679
finish_reason: length
builder_max_tokens: 1536
```

The raw output was valid-looking JSON until it was cut off inside the fourth card. Treat this as an
incomplete generation, not as evidence that the mechanism-card schema is unusable.

## Fix

- Launch 27B with `--max-model-len 16384` as the minimum for this workflow.
- Keep `--gpu-memory-utilization 0.90`; the previous remote run already launched successfully with
  that utilization after increasing the context window.
- Build mechanism cards with `--max-tokens 4096`, not `1536`.
- If the remote machine has enough headroom, `--max-model-len 32768` is acceptable, but it is not
  required for the current 8143-token prompt plus a 4096-token completion budget.
- The builder now writes `mechanism_card_error.json` with `status: incomplete_generation` when
  vLLM reports `finish_reason: length`, so future artifact review can distinguish truncation from
  genuine malformed JSON.

## Next Run Rule

Only continue from 27B mechanism-card generation to 9B controller generation when
`mechanism_cards.json` exists and parses. If `mechanism_card_error.json` exists, return the artifact
for local review and do not hand-edit cards on the remote machine.
