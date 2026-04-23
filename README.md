# Quant Knowledge Vault

This repository is an Obsidian vault for building and maintaining a quantitative finance knowledge base in the style of Andrej Karpathy's April 2026 `LLM Knowledge Bases` workflow.

In this vault:

- `raw/` is the source library
- `catalog/` is the mirrored data catalog and sample layer
- `wiki/` is the compiled knowledge base
- `projects/` is the active working area for research and synthesis
- `artifacts/` is the evidence layer for outputs from data work, diagnostics, charts, and reports
- `AGENTS.md` is the schema that tells the agent how to maintain the vault
- `.obsidian/` is the vault frontend and plugin configuration

Inside `wiki/`, the knowledge base is now organized into:

- root control notes: `index.md`, `log.md`, `glossary.md`, `inbox.md`
- `maps/` for domain entry points and reading order
- `sources/books/` for book overview notes plus `sources/books/<Book Title>/` for chapter digests of deeply ingested books
- `sources/papers/` and `sources/articles/` for source-tied notes that do not need a book-style chapter shelf
- `concepts/` for durable conceptual synthesis
- `methods/` for workflows and procedures
- `metrics/` for evaluation quantities and research measures
- `strategies/` for alpha, portfolio, and execution notes
- `datasets/` and `identifiers/` for the data spine

## Karpathy-style mapping

The vault follows the same basic pattern:

1. Collect curated sources into `raw/`
2. Keep data mirrors and sample evidence in `catalog/`
3. Let the agent compile durable markdown into `wiki/`
4. Use `projects/` for live investigations and question-driven work
5. Save bounded outputs into `artifacts/`
6. Browse, search, link, and review everything in Obsidian

This is not a local warehouse clone. The heavy data still lives on the remote Linux server. The vault is the local memory and control layer.

## Memory lifecycle

The vault now treats its layers as a memory lifecycle, not only a folder tree:

- `raw/` stores source memory
- `projects/` stores working or episodic memory while a thread is still live
- `wiki/` stores semantic and procedural memory that should compound over time
- `catalog/` and `artifacts/` store evidence and observability memory for numerical or operational claims

This matters because not every observation deserves durable promotion, and durable notes should not be silently "forgotten" when they age. They should be verified, superseded, or archived honestly.

## Git policy

The git repository is intentionally narrower than the full local vault:

- track markdown notes, maps, canvases, schemas, and portable Obsidian config
- do not track `raw/` source books and PDFs
- do not track `catalog/samples/` mirrored data extracts
- do not track generated `artifacts/`
- do not track local plugin installs or plugin `data.json` files under `.obsidian/plugins/`

This keeps the repo portable and avoids pushing copyrighted source materials, proprietary data samples, and local secrets.

## Vault layers

### `raw/`

Use for books, papers, clipped web articles, interview notes, and other original sources.

### `catalog/`

Use for:

- `csv_data_catalog.md`
- `csv_data_inventory.csv`
- mirrored dataset samples
- mirrored EDA summaries
- mirrored processed research outputs

This is the vault's compact substitute for opening huge remote files.

### `wiki/`

Use for durable notes the agent maintains over time:

- maps
- source notes
- concept notes
- method notes
- metric notes
- strategy notes
- dataset and identifier notes

### `projects/`

Use for active research work:

- current questions
- plans
- replications
- validation notes
- decisions

### `artifacts/`

Use for bounded outputs that support claims:

- query exports
- charts
- tables
- backtest summaries
- replication results

## Obsidian as the frontend

This vault already has an active Obsidian setup. Core capabilities enabled include:

- graph view
- backlinks
- search
- properties
- daily notes
- templates
- bases
- web viewer

Installed community plugins include:

- Dataview
- Tasks
- Templater
- Excalidraw
- Obsidian Git
- Obsidian Local REST API
- Table Editor

Math authoring rule:

- Extended MathJax is installed through `obsidian-latex`
- shared macros now live in `preamble.sty` at the vault root
- mathematically important notes should use MathJax equations instead of code-style pseudo-math

That means the vault is already ready to serve as:

- the browser for the knowledge graph
- the note editor for human review
- the dashboard surface for Dataview tables
- the canvas surface for spatial knowledge maps
- the project board for tasks and open questions

## Automation note

In this Codex environment there are two Obsidian execution paths:

- Obsidian MCP works well for note-local reads, appends, searches, and vault maintenance
- shell-side `obsidian` CLI commands that need the running desktop app must be executed unsandboxed, because the sandboxed shell runs under a different Windows identity than the interactive Obsidian session

Use the lowest-cost tool that preserves the needed context. Direct reads or exact search are cheaper when the target is already known, Obsidian MCP is the default for note-local maintenance, QMD is for broad discovery, and the shell CLI should be used intentionally when the task needs desktop-native commands such as tab control, command execution, Bases, backlink audits, or opening canvas views.

## Operating principle

The human curates and asks questions.

The agent reads sources, compiles notes, maintains links, finds contradictions, and updates the vault.

The goal is to make knowledge compound instead of disappear into chat history.

Start with [AGENTS.md](AGENTS.md), then read:

- [raw/README.md](raw/README.md)
- [catalog/README.md](catalog/README.md)
- [wiki/README.md](wiki/README.md)
- [projects/README.md](projects/README.md)
- [artifacts/README.md](artifacts/README.md)
