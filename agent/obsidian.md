# Obsidian Operation

This file expands the Obsidian rules from [../AGENTS.md](../AGENTS.md).

## Obsidian Doctrine

Obsidian is the main interface for:

- graph view
- backlinks
- properties and frontmatter
- Dataview
- Bases
- tasks and periodic notes
- canvases
- git-backed history

The vault should be pleasant and useful inside Obsidian:

- stable titles
- meaningful wikilinks
- readable standalone notes
- folder semantics that still make sense in the file tree

## MCP / CLI Doctrine

Prefer the lowest-cost tool that preserves the needed vault context.

QMD complements Obsidian rather than replacing it.

In this environment:

- Obsidian MCP is the default inside the sandbox
- desktop `obsidian` CLI commands that require IPC may need unsandboxed execution
- direct filesystem reads and `rg` are the cheapest exact-match layer for markdown files
- QMD is available as a broad-discovery layer over indexed markdown collections
- raw PDF tooling is the expensive escalation layer for source verification and ingest

Use direct filesystem reads or `rg` first for:

- a known path, filename, heading, or literal phrase
- broad exact-match sweeps across many markdown files
- read-only inspection that does not need backlinks, properties, tabs, or other vault context

Use Obsidian tooling first for:

- listing or reading known notes when note-local context matters
- searching the vault when the task is note-local or the target area is already known
- patching or appending note-local changes
- checking recent changes or periodic notes
- backlink, unresolved-link, property, or Bases-oriented workflows

Use QMD first when:

- the target note is not yet known
- the question is cross-source, fuzzy, or concept-level
- semantic discovery across many notes is more important than exact note-local operations

Use QMD `get` / `multi_get` when:

- QMD has already surfaced the indexed notes
- the task is read-only retrieval of one or several candidate notes
- indexed fetch is cheaper than repeated direct note opens

Once QMD has surfaced the candidate notes, prefer Obsidian or direct note reads for close inspection, backlink navigation, and edits.

Use `raw/` or PDF tooling when:

- compiled markdown notes do not contain enough support
- theorem statements, page-local wording, or source provenance matter
- source ingest or contradiction resolution requires going back to the original material

Use filesystem reads and `apply_patch` when:

- a multi-file refactor needs precise diff control
- the task is structural rather than note-local
- Obsidian tooling lacks the needed capability

## Links, Bases, and Tags

### Links

Links are the main connective tissue of the vault.

Rules:

- prefer wikilinks when referring to existing durable entities
- prefer meaningful links over link stuffing
- source notes should link forward into promoted durable notes

### Bases

Bases are the main operational dashboard layer, not the source of truth.

Rules:

- markdown plus frontmatter remains the source of truth
- keep frontmatter stable enough for Base views
- use Bases for registries, audits, and maintenance surfaces

### Tags

Tags are a secondary faceting layer.

Rules:

- keep tag vocabulary controlled
- use tags for facets, not for replacing links or titles
- avoid one-off near-duplicate tags

## Plugin-Aware Conventions

### Dataview

Write notes and frontmatter so Dataview queries remain stable and useful.

### Bases

Keep `type`, `status`, `updated`, `domain`, and `sources` consistent enough for table views and audits.

### Tasks

Use Tasks for operational follow-ups, not as the main storage of knowledge.

### Templater

Templates are scaffolding only. Do not let them become the content.

### Excalidraw and Canvas

Use canvases and diagrams as navigation or explanatory surfaces. Keep the main factual content in markdown.

### Obsidian Git

Prefer small readable note changes and avoid noisy churn in tracked config.

### Local REST API

Only use it when a task specifically requires app-native interaction that MCP or normal file editing does not cover.
