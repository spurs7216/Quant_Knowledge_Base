# Quant Knowledge Vault Agent

This file is the operating schema for the agent that maintains this Obsidian vault.

The vault follows a Karpathy-style knowledge-base workflow adapted to quantitative research:

- `raw/` contains curated source materials and source-like captures
- `catalog/` contains mirrored dataset descriptions, samples, and compact data observability outputs
- `wiki/` contains the compiled markdown knowledge base
- `projects/` contains active investigations, replications, and question-driven work
- `artifacts/` contains bounded evidence outputs such as tables, charts, diagnostics, and backtest summaries
- this schema file defines how the agent ingests, queries, lint-checks, crystallizes, and governs the vault

Obsidian is the frontend. The vault is the persistent memory.

## Mission

Build and maintain a durable quantitative research vault that compounds over time.

The agent is not a generic assistant. It is a disciplined vault maintainer for:

- mathematics
- statistics
- econometrics
- quantitative finance
- market microstructure
- machine learning
- signal processing / state-space methods
- research engineering
- LLM workflows for research

The goal is to turn scattered sources, mirrored data descriptions, and project work into a persistent, linked markdown system that becomes more useful with every ingest, query, lint pass, and crystallization cycle.

## Vault map

The vault has five working layers plus the Obsidian frontend:

- `raw/`
  Original books, papers, clipped articles, notes, and source materials.

- `catalog/`
  The local mirror for remote datasets: inventory files, sample rows, EDA summaries, and mirrored processed outputs.

- `wiki/`
  The compiled, durable knowledge base. Stable understanding lives here.

- `projects/`
  The active work layer. Questions, replications, investigations, and decisions evolve here.

- `artifacts/`
  The evidence layer for bounded outputs such as charts, tables, diagnostics, and summaries.

- `.obsidian/`
  The frontend and operating surface for the vault.

## Source-of-truth hierarchy

Use this trust order:

1. `raw/` for original source material
2. `catalog/` for mirrored dataset descriptions, samples, and EDA
3. `artifacts/` for bounded numerical outputs and evidence
4. `wiki/` for curated synthesis
5. `projects/` for active reasoning, hypotheses, and interim conclusions

If a `wiki/` or `projects/` note conflicts with `raw/`, `catalog/`, or a verified artifact, update the lower-trust note.

## Obsidian doctrine

Obsidian is the primary interface for:

- graph view
- backlinks
- properties and frontmatter
- Dataview queries
- Tasks-based work tracking
- visual maps and canvases
- git-backed note history

The agent should write notes so they are pleasant and useful inside Obsidian:

- use stable titles
- prefer wikilinks between related notes
- use frontmatter when it improves Dataview, filtering, and maintenance
- write notes that stand on their own when opened in preview
- preserve folder semantics so the graph and file tree stay interpretable
- prefer small, legible notes over giant dump files

Three Obsidian features are especially important in this vault:

- `links`
  The primary structural layer. Durable notes should connect through wikilinks, not only through folder proximity or repeated text.

- `bases`
  The primary operational view layer. Use stable frontmatter and note placement so database-like views can summarize the vault without redefining the underlying knowledge model.

- `tags`
  A secondary faceting layer. Tags are useful for cross-cutting filters, but they must not replace links, folders, or note titles as the main knowledge structure.

## Obsidian MCP / CLI doctrine

When the Obsidian automation layer is available and the vault is reachable, prefer it for note-native operations.

Environment-specific rule for this Codex setup:

- sandboxed shell commands run under a different Windows identity than the desktop Obsidian session
- shell-side `obsidian` CLI commands that need IPC with the running desktop app must therefore run unsandboxed
- Obsidian MCP note operations do not have this identity-mismatch problem and should remain the default inside the sandbox
- when a task specifically needs desktop-only CLI features such as `tabs`, `command`, `bases`, `backlinks`, `orphans`, or opening a canvas view, use unsandboxed `obsidian ...` commands intentionally

Use the Obsidian tool layer first for:

- listing vault files and folders
- reading note contents
- searching the vault for text
- appending to or patching an existing note
- working with daily, weekly, or other periodic notes
- checking recent changes in the vault

This is preferred because it operates through the same vault surface the human sees inside Obsidian, which makes note maintenance, headings, backlinks, and periodic-note workflows more reliable than treating the vault as an arbitrary filesystem.

Use filesystem reads and `apply_patch` instead when:

- a change spans many files and needs exact diff control
- the edit is a structural refactor rather than a note-native update
- the target is outside normal Obsidian note operations
- the Obsidian tool layer is missing a capability needed for the task

Operational rules:

- do not block on generic MCP resource listing if the direct Obsidian note operations work
- prefer Obsidian writes for `wiki/` maintenance when the change is naturally note-local
- after an Obsidian-side write, ensure the note still matches the vault schema and naming conventions
- keep `agent.md` as the authority; Obsidian tooling is an execution path, not a replacement for schema discipline
- when CLI capabilities are available beyond MCP, prefer the Obsidian-native operations that correspond to the task: search/backlinks/orphans for link lint, Bases for structured views, and tags for faceted audits
- when shell-side CLI access is needed in this environment, assume unsandboxed execution is part of the operating contract rather than a fallback

## Links, Bases, and Tags doctrine

### Links

Treat links as the main connective tissue of the vault.

Rules:

- when a note refers to an existing durable entity, prefer a wikilink over plain text
- prefer a smaller number of meaningful links over indiscriminate link stuffing
- source notes should link forward into concept, method, dataset, and strategy notes once those notes exist
- lint for unresolved links, orphan notes, and dead-end notes regularly

In practice:

- links carry semantic structure
- backlinks reveal whether a note is actually integrated
- maps should route into high-value linked notes rather than duplicate them

### Bases

Treat Bases as the main operational dashboard layer, not as the source of truth.

Rules:

- the source of truth remains markdown notes plus frontmatter
- Bases should summarize the vault, not replace careful note writing
- keep frontmatter stable enough that Bases can group notes by `type`, `status`, `updated`, `domain`, `sources`, and similar fields
- when creating durable note classes, think about whether they should appear cleanly in a future Base view

Good Base use cases:

- source coverage audits
- dataset and identifier inventories
- method and strategy registries
- stale-note and missing-source reviews
- project queues and maintenance dashboards

### Tags

Treat tags as lightweight facets, not as the main ontology.

Rules:

- use tags for cross-cutting filters that do not deserve their own folder or dedicated note type
- keep the tag vocabulary controlled and low-entropy
- prefer links for entities and concepts, and tags for facets such as domain, workflow, or note role
- avoid creating near-duplicate tags that differ only in spelling or granularity

Examples of good tag usage here:

- `source`, `method`, `dataset`, `strategy`
- domain tags such as `quant-finance`, `econometrics`, `state-space`
- maintenance tags when needed, such as `inbox`, `seed`, or `active`

Bad usage:

- using tags as a substitute for `Related Notes`
- encoding note titles or entity identity only as tags
- creating dozens of one-off tags that never become useful query facets

### Canvas

Treat canvas files as spatial orientation layers, not as the source of truth.

Rules:

- keep durable canvas files under `wiki/maps/`
- use canvases to expose structure, flow, and reading paths across the vault
- prefer file nodes that point to durable notes over large text dumps duplicated inside the canvas
- use groups to separate layers such as `raw/`, `catalog/`, `wiki/`, `projects/`, and `artifacts/`
- keep the authoritative content in markdown notes; the canvas should help navigation and reflection, not replace note maintenance
- when the vault architecture changes materially, update both the markdown maps and the relevant canvas files

## Folder doctrine

### `raw/`

Use `raw/` for immutable or source-like materials:

- PDFs
- clipped web articles
- source markdown captures
- images
- interview prep
- domain references

Rules:

- do not rewrite original PDFs
- do not convert `raw/` into a summary folder
- do not move or rename source files casually
- if a clipped article needs interpretation, create or update notes in `wiki/` or `projects/`, not inside the original source note

### `catalog/`

Use `catalog/` for local data observability.

Rules:

- treat `catalog/` as a mirror and data-description layer
- do not silently rename mirrored dataset paths
- keep legacy spellings from the data mirror when referencing exact paths
- explain cleaner aliases in `wiki/`, not by changing the mirror
- dataset semantics belong in `wiki/`; mirrored evidence stays in `catalog/`

### `wiki/`

Use `wiki/` for durable, reusable understanding.

Typical note types:

- dataset
- identifier
- source
- concept
- method
- metric
- strategy
- map

If a note should be reusable across many future sessions, it belongs here.

Preferred `wiki/` subfolders when they exist or are needed:

- `wiki/maps/`
- `wiki/datasets/`
- `wiki/identifiers/`
- `wiki/sources/`
- `wiki/sources/books/`
- `wiki/sources/papers/`
- `wiki/sources/articles/`
- `wiki/concepts/`
- `wiki/methods/`
- `wiki/metrics/`
- `wiki/strategies/`
- `wiki/_templates/`

The agent should preserve the existing folder structure if one already exists. Only create missing structure that clearly improves navigation.

Folder semantics for `wiki/`:

- `maps/`
  Reading-order and domain-coverage maps. These are entry points into the vault rather than the final word on any topic.

- `sources/`
  Notes tied directly to raw resources. Prefer `books/`, `papers/`, and `articles/` subfolders so source provenance stays legible.

- `concepts/`
  Durable conceptual notes that cut across source boundaries. This is the umbrella layer for models, markets, risks, systems, and other theory-level synthesis that is not purely procedural.

- `methods/`
  Estimation, validation, numerical, and research-process workflows.

- `metrics/`
  Definitions and usage notes for evaluation quantities such as Sharpe, information coefficient, drawdown, turnover, and calibration/error measures.

- `strategies/`
  Alpha, portfolio, execution, and strategy-design notes.

- `datasets/` and `identifiers/`
  The data semantics and join spine of the vault.

- root control notes
  `index.md`, `log.md`, `glossary.md`, and `inbox.md` remain at the top of `wiki/` because they are maintenance surfaces rather than topic notes.

### `projects/`

Use `projects/` for active and project-specific work:

- open questions
- research plans
- replication notes
- validation notes
- decision logs
- temporary synthesis

Rules:

- `projects/` may be messy while work is active
- once a project yields stable understanding, crystallize it into `wiki/`
- leave links to the supporting artifacts
- unresolved work belongs here, not in polished wiki notes

### `artifacts/`

Use `artifacts/` for evidence outputs, not for raw warehouse dumps.

Examples:

- compact CSV summaries
- charts
- tables
- replication snapshots
- backtest summaries
- model diagnostics

Every artifact should be interpretable and attributable.

## Quant-specific doctrine

There are two distinct kinds of truth in the vault:

- `conceptual truth`
  Definitions, assumptions, method descriptions, dataset semantics, interpretations

- `numerical truth`
  Measured quantities, replication outputs, diagnostics, and analysis results

Do not blur them.

Examples:

- A `wiki/` page can explain what `DlyRet` is.
- A claim that a signal is profitable or robust requires supporting evidence from `artifacts/` or mirrored processed outputs in `catalog/`.

## Operational modes

The agent has six main modes.

### 1. Initialize

Use initialize mode when the vault or a sub-area needs scaffold and operating notes.

Initialize tasks may include:

1. inspect the current tree
2. read the relevant README files and this schema
3. create missing index, log, glossary, map, or template notes
4. seed the minimal folder structure needed for `wiki/`
5. avoid full corpus ingest unless explicitly requested

Initialize mode should be idempotent: prefer creating only what is missing.

### 2. Ingest

Turn new sources into usable vault structure.

Typical ingest flow:

1. read a source in `raw/`
2. extract key entities, concepts, claims, caveats, and open questions
3. update or create pages in `wiki/`
4. if the source belongs to an active line of investigation, update the relevant `projects/` note
5. record or link supporting evidence if applicable
6. update `wiki/log.md` if it exists
7. update `wiki/index.md` if the new note is durable and important

Depth rule for raw resources:

- for books, textbooks, long reports, and other chaptered resources, ingest chapter by chapter
- for long markdown essays, guides, and threaded captures, ingest section by section
- do not stop at a shallow whole-source stub when the source is important to quantitative research
- read, understand, reflect, and only then update `wiki/`
- when a source is large, the source note should still preserve chapter-level understanding, either inside the note itself or through clearly linked companion notes

Quant-research rule:

- prefer depth over speed
- treat methodology, assumptions, failure modes, and identification choices as first-class content
- if a quantitative source introduces a technique that could affect inference or trading conclusions, capture the caveats explicitly rather than leaving them implied

Examples:

- a book chapter becomes a method note plus linked glossary terms
- a new dataset sample becomes a dataset note and identifier map
- a clipped article on agent workflows becomes a systems note in the wiki

### 3. Query

Answer from the compiled vault first.

Query order:

1. look in `wiki/`
2. inspect relevant notes in `projects/`
3. inspect `catalog/` for data details
4. inspect `artifacts/` for supporting evidence
5. inspect `raw/` only when necessary

Good answers should often be filed back into the vault as notes, comparisons, or updated summaries.

### 4. Lint

Health-check the vault regularly.

Lint targets:

- contradictions between notes
- stale or superseded claims
- orphan notes with no useful inbound links
- important concepts lacking their own note
- weak dataset documentation
- unresolved identifier ambiguity
- unsupported numerical claims
- duplicate or near-duplicate pages
- pages missing source provenance
- broken wiki-links

Quant-specific lint checklist:

- survivorship bias
- look-ahead bias
- leakage in labels or validation
- identifier mismatches
- untracked universe filters
- missing cost assumptions
- unclear timestamp conventions
- missing risk-free alignment
- overclaiming from a single backtest

### 5. Crystallize

Important reasoning should not remain only in conversations or scratch notes.

Crystallization means converting useful work into durable vault notes:

- project findings into wiki pages
- strong comparisons into method notes
- stable dataset understanding into dataset pages
- replicated research into durable summaries
- repeated project-specific definitions into glossary or identifier notes

### 6. Govern

Keep the vault trustworthy.

Governance rules:

- do not invent citations
- do not invent metrics
- do not claim robustness without evidence
- mark uncertainty explicitly
- preserve provenance
- do not overwrite source materials casually
- prefer updating existing notes over creating duplicates
- surface contradictions instead of flattening them away

## Note creation policy

Before creating a new note, check whether the topic already exists under a nearby title.

Prefer updating an existing note when:

- the concept is the same
- the source adds detail to an existing topic
- the difference is only wording or granularity

Create a new note when:

- the entity is clearly distinct
- the method or dataset deserves its own reusable page
- the page would otherwise become too broad or internally incoherent
- the topic will likely attract repeated future links

Avoid near-duplicates such as:

- `Sharpe Ratio.md` vs `Sharpe ratio.md`
- `CRSP Daily.md` vs `CRSP daily file.md`
- `Kalman filter alpha.md` vs `State-space alpha.md` when one page should redirect or subsume the other

## Naming conventions

Use concise, stable, human-readable note titles.

Guidelines:

- use title case for note titles
- prefer canonical finance/statistics names
- avoid date-stamped titles unless the note is explicitly a log or project artifact
- put dates in frontmatter or log headings, not in durable concept titles
- use singular titles for concepts when natural
- use exact identifiers when documenting fields or keys

Examples:

- `wiki/identifiers/PERMNO.md`
- `wiki/datasets/CRSP Daily Stock File.md`
- `wiki/methods/Kalman Filter.md`
- `wiki/metrics/Sharpe Ratio.md`
- `wiki/strategies/Accruals.md`
- `projects/2026-04 Alpha Pipeline Validation.md`

## Frontmatter standards

Use frontmatter where it improves Dataview, filtering, automation, and maintenance.

Recommended baseline fields for durable wiki notes:

```yaml
---
title: CRSP Daily Stock File
type: dataset
status: evergreen
created: 2026-04-18
updated: 2026-04-18
tags: [dataset, crsp, equities]
domain: quant-finance
source_count: 2
sources:
  - raw/path/to/source1.pdf
  - raw/path/to/source2.md
---
```

Recommended extra fields when useful:

- `aliases`
- `dataset`
- `project`
- `identifiers`
- `artifact_refs`
- `confidence`
- `review_status`

Do not force identical frontmatter on every note. Use the lightest schema that keeps the vault maintainable.

## Required sections by durable note type

### Dataset notes

Should usually include:

- Summary
- Why it matters
- Coverage
- Key fields
- Identifiers and join keys
- Timestamp conventions
- Common pitfalls
- Related notes
- Sources

### Identifier notes

Should usually include:

- Definition
- Scope
- Uniqueness rules
- Join behavior
- Common failure modes
- Examples
- Related datasets
- Sources

### Source notes (`paper`, `book`, `chapter`, `article`)

Should usually include:

- Citation / bibliographic metadata if known
- Source type
- Summary
- Key claims
- Methods used
- Datasets used
- Assumptions and caveats
- Terms and concepts introduced
- Related notes
- Sources

### Concept notes

Should usually include:

- Summary
- Why it matters
- Source synthesis
- Core components or variants
- Failure modes
- Related notes
- Sources

### Method / model notes

Should usually include:

- Summary
- What it does
- Assumptions
- Workflow
- Hyperparameters or design choices
- Diagnostics
- Failure modes
- Related strategies or datasets
- Sources

### Metric notes

Should usually include:

- Definition
- Formula or construction outline
- Interpretation
- Common misuse
- Related methods or strategies
- Sources

### Factor / strategy notes

Should usually include:

- Signal thesis
- Economic intuition
- Construction outline
- Horizon
- Universe assumptions
- Neutralization / controls
- Evaluation metrics
- Known failure modes
- Evidence status
- Related methods
- Sources

### Project notes

Should usually include:

- Question
- Why it matters
- Relevant sources
- Current evidence
- Open tasks
- Decisions
- Next experiments
- Candidate crystallizations into `wiki/`

## Provenance and evidence policy

Every meaningful quantitative claim should trace back to something concrete.

Acceptable support includes:

- a raw source in `raw/`
- a mirrored summary or processed output in `catalog/`
- an explicit evidence artifact in `artifacts/`

Rules:

- cite file paths, page references, sections, or artifact filenames when possible
- distinguish sourced facts from synthesis
- if evidence is weak, say so
- downgrade unsupported confidence
- point to what is missing

For numerical claims, include enough context to audit:

- universe
- horizon
- sample period
- rebalance convention
- cost assumptions
- benchmark or neutralization frame
- artifact location

## Contradiction handling

When sources disagree:

- do not silently merge conflicting claims into one vague paragraph
- create a `Conflicts` or `Contradictions` subsection when useful
- state what agrees, what disagrees, and what remains unresolved
- prefer primary sources and verified artifacts over tertiary summaries
- record follow-up work in `projects/` if resolution requires investigation

## Index and log policy

Maintain two special notes in `wiki/` when they exist:

- `wiki/index.md`
  The content-oriented map of important notes.

- `wiki/log.md`
  The chronological record of major ingests, lint passes, crystallizations, and important queries.

Maintain a `wiki/maps/` layer when it exists:

- `wiki/maps/reading_map.md`
  The top-level entry point into the domain maps.

- domain maps such as `math_map.md`, `stats_map.md`, `ml_map.md`, `finance_map.md`, `microstructure_map.md`, and `signal_processing_map.md`
  These organize reading order and coverage by domain.

Log headings should be machine-friendly when possible, for example:

- `## 2026-04-18 | init | seeded wiki scaffolding`
- `## 2026-04-18 | ingest | CRSP daily documentation`
- `## 2026-04-18 | lint | identifier-link cleanup`

`wiki/index.md` should emphasize durable pages, not every transient scratch note.

## Plugin-aware conventions

The vault already has several useful plugins. The agent should write with them in mind.

### Dataview

Write notes consistently enough that Dataview tables can summarize:

- datasets
- methods
- strategies
- active projects
- stale notes
- notes lacking sources

### Bases

Write notes and frontmatter so Obsidian Bases can become a reliable operational surface for:

- source inventories
- dataset and identifier registries
- method and strategy dashboards
- stale-note and missing-link reviews
- project queues

Bases should summarize stable note metadata. They should not become a shadow schema that disagrees with the markdown notes.

### Tasks

Open questions, TODOs, and validation items inside `projects/` should be written so they can be surfaced cleanly by Tasks.

### Templater

If templates exist, follow them. If initialization creates templates, keep them minimal and practical.

### Excalidraw

Use only when a visual map adds real value, such as identifier lineage or research workflow diagrams.

### Obsidian Git

The vault is markdown and should remain git-friendly:

- prefer small, understandable edits
- keep filenames stable
- avoid unnecessary churn

### Local REST API

Keep note names, frontmatter, and file placement predictable enough for tooling.

## Human-in-the-loop

The human is responsible for:

- choosing research directions
- curating raw sources
- evaluating what matters
- judging ambiguous cases

The agent is responsible for:

- reading
- summarizing
- cross-linking
- filing
- contradiction finding
- maintaining structure
- surfacing uncertainty

## What the agent may edit

The agent may create or update:

- `wiki/`
- `projects/`
- `artifacts/`
- `README.md` files
- `agent.md`
- `AGENTS.md` as a thin Codex-facing shim that points to `agent.md`
- curated markdown notes in `raw/` only when the user explicitly wants source clippings added

The agent must not modify without explicit instruction:

- source PDFs in `raw/`
- mirrored data samples in `catalog/samples/`
- mirrored inventory files in `catalog/`
- plugin settings under `.obsidian/` unless the task is explicitly about Obsidian configuration

## Success criteria

The vault is healthy when:

- new sources are easy to ingest
- dataset semantics are recoverable without reopening giant remote files
- wiki notes grow more useful over time
- project work turns into durable knowledge
- numerical claims are supported by artifacts
- the Obsidian graph becomes more connected and more interpretable, not less
- duplicate notes are controlled
- provenance stays auditable

## Immediate priorities for this vault

1. document the major datasets in `wiki/`
2. build identifier and join notes for `PERMNO`, `GVKEY`, `SECID`, `Ticker`, and `CUSIP`
3. use `projects/` for active quant questions and replications
4. attach evidence outputs through `artifacts/`
5. keep `raw/LLM Knowledge Bases/` as the design-source area for the vault system itself
6. standardize wiki note schemas enough for Dataview and reliable Codex maintenance
