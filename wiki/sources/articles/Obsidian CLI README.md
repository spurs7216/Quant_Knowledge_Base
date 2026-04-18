---
title: Obsidian CLI README
type: source
status: section_ingested
updated: 2026-04-18
tags:
  - source
  - obsidian
  - cli
  - workflow
  - bases
sources:
  - "[[raw/Obsidian/Obsidian_README.md]]"
---
# Obsidian CLI README

## Summary

This README documents the official Obsidian CLI introduced in v1.12. It covers prerequisites, platform behavior, command groups, common agent patterns, and operational caveats. For this vault, the most important message is not just that the CLI exists, but that it makes Obsidian-native operations auditable and scriptable.

## Section-by-Section Ingest

- `Skill metadata and triggers`: frames Obsidian operations as an action surface rather than a purely explanatory topic.
- `Prerequisites`: requires Obsidian Desktop v1.12+, CLI enabled in settings, and a running desktop instance.
- `Platform notes`: highlights Windows-specific constraints around `Obsidian.com`, normal-user terminals, and Git Bash / MSYS2 wrapper issues.
- `Syntax and multi-vault targeting`: explains `key=value` arguments and vault targeting conventions.
- `Command overview`: organizes the CLI into file, daily, search, properties, tags, tasks, links, bookmarks, templates, plugins, sync, themes, snippets, commands, bases, history, workspace, diff, developer, and vault commands.
- `Quick reference`: gives note CRUD, daily-note, search, property, tag, task, and developer examples.
- `Common agent patterns`: shows practical automation patterns for journaling, templated note creation, vault analytics, search-and-extract, sync management, and command execution.
- `Tips`: documents important operational caveats, especially around vault-relative paths, frontmatter lists, JSON output, and `eval` behavior.
- `Troubleshooting`: captures the main failure modes and their platform-specific fixes.

## Key Claims

- Obsidian can be used as an operational surface for vault maintenance rather than only a GUI.
- Links, tags, properties, and Bases are queryable and scriptable enough to support serious agent workflows.
- CLI usage must respect platform constraints, especially on Windows.

## Methods and Data

- vault-relative note CRUD
- search and search-context workflows
- frontmatter and property management
- tag inspection and filtering
- backlink, orphan, unresolved-link, and dead-end analysis
- Bases queries and view operations
- developer access through `eval`

## Why It Matters Here

This source sharpens how the vault should be maintained. The most useful operational pattern is: use links as the main knowledge structure, Bases as the main dashboard surface, and tags as a controlled faceting layer.

## Reflection

The README is most valuable as an operating manual, not as a conceptual essay. It makes clear that Obsidian-native structure can be queried and maintained directly, which is exactly what a long-term knowledge vault needs.

## Caveats

- The CLI depends on a running Obsidian desktop instance.
- On Windows, CLI behavior depends on `Obsidian.com` and normal-user privilege level.
- `property:set` writes list-like values as strings, so YAML arrays still require more careful handling.
- Multi-vault targeting and colon subcommands may behave differently across environments.

## Related Notes

- [[LLM Knowledge Base Workflow]]
- [[Obsidian Spaced Repetition Plugin]]
- [[Reading Map]]

## Sources

- [[raw/Obsidian/Obsidian_README.md]]
