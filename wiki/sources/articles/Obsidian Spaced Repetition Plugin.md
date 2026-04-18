---
title: Obsidian Spaced Repetition Plugin
type: source
status: section_ingested
updated: 2026-04-18
tags:
  - source
  - obsidian
  - learning
  - interview-prep
sources:
  - "[[raw/LLM Knowledge Bases/st3v3nmwobsidian-spaced-repetition Fight the forgetting curve by reviewing flashcards & entire notes on Obsidian.md]]"
---
# Obsidian Spaced Repetition Plugin

## Summary

This source documents an Obsidian plugin for flashcard review and note review using spaced repetition. It supports simple question-answer cards, cloze cards, deck organization via tags or folders, and scheduled review of whole notes.

## Section-by-Section Ingest

- `Reviewing flashcards`: the plugin supports single-line, multiline, reversible, and cloze-style cards directly in markdown.
- `Organize decks`: deck structure can follow tags or folder hierarchy, which fits an Obsidian vault without separate study software.
- `Reviewing notes`: the plugin can schedule whole-note review, not only card review, which is useful for conceptual subjects.
- `Usage TLDR`: the workflow is create deck tags, write cards in the note, and run review commands from the command palette.
- `Statistics`: the review process is tracked so the vault can function as a deliberate study loop as well as a knowledge base.

## Key Claims

- Flashcards can be authored directly in markdown using lightweight inline patterns.
- Notes can also be scheduled for full-note review, not only card review.
- Deck structure can follow Obsidian tags or folders.
- Review statistics and due queues turn the vault into a study system as well as a knowledge system.

## Methods and Data

This is plugin documentation rather than a conceptual essay. It gives authoring syntax, deck organization rules, and the command-level review workflow inside Obsidian.

## Why It Matters Here

This plugin is not part of Karpathy's core raw -> wiki -> schema workflow, but it is relevant for a quant researcher candidate. The vault can support both durable knowledge maintenance and deliberate recall for:

- interview questions
- mathematical definitions
- econometrics assumptions
- market microstructure terminology

## Reflection

Used carefully, this plugin can convert stable wiki notes into active memory without splitting the learning system away from the knowledge system. Used badly, it can flood the vault with low-value cards. The right use here is selective reinforcement of high-signal concepts.

## Caveats

- Spaced repetition is a learning overlay, not a replacement for durable wiki synthesis.
- Card creation should stay selective. Turning every note into flashcards would create maintenance noise.

## Related Notes

- [[LLM Knowledge Base Workflow]]
- [[Karpathy LLM Knowledge Bases Thread]]
- `raw/interview_questions/`

## Sources

- [[raw/LLM Knowledge Bases/st3v3nmwobsidian-spaced-repetition Fight the forgetting curve by reviewing flashcards & entire notes on Obsidian.md]]
