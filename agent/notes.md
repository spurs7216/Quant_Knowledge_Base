# Note and Folder Standards

This file expands the note-structure rules from [../AGENTS.md](../AGENTS.md).

## Folder Doctrine

### `raw/`

Use for immutable or source-like materials:

- PDFs
- clipped articles
- source markdown captures
- images
- interview prep

Do not turn `raw/` into a summary layer.

### `catalog/`

Use for mirrored dataset description, samples, and observability.

Do not silently rename mirror paths. Cleaner aliases belong in `wiki/`, not in the mirror itself.

### `wiki/`

Use for durable reusable understanding.

Main subfolders:

- `maps/`
- `datasets/`
- `identifiers/`
- `sources/`
- `concepts/`
- `methods/`
- `metrics/`
- `strategies/`
- `_templates/`

Keep root control notes at the top level:

- `index.md`
- `log.md`
- `glossary.md`
- `inbox.md`

### `projects/`

Use for active work, uncertain reasoning, replication, and evolving synthesis.

### `artifacts/`

Use for bounded evidence outputs:

- charts
- tables
- diagnostics
- backtest summaries
- compact exports

## Note Creation Policy

Create a durable note when the knowledge should be reusable across future sessions or projects.

If the material is still uncertain or project-specific, keep it in `projects/` until it crystallizes.

Treat the folders as different memory tiers, not only different locations:

- `projects/` holds working or episodic material
- `wiki/` holds semantic or procedural material
- `artifacts/` and `catalog/` hold supporting evidence and observability

## Naming Conventions

- prefer stable descriptive titles
- keep source note titles source-linked
- avoid one-off abbreviations unless they are standard in the field
- prefer predictable chapter titles for book shelves

## Frontmatter Standards

Use frontmatter when it improves maintenance, filtering, or Bases.

Common fields:

- `title`
- `type`
- `status`
- `updated`
- `tags`
- `sources`
- `last_verified`
- `verification_status`
- `supersedes`
- `superseded_by`

Useful source-note fields:

- `source_type`
- `source_class`
- `read_scope`
- `extraction_basis`
- `technical_depth`
- `ingest_stage`
- `chapter_or_section`
- `parent_source`

Useful optional relation fields for high-value notes:

- `depends_on`
- `used_by`
- `contradicts`

Do not force these onto every note. Use them when the relationship is load-bearing and worth making machine-visible.

## Required Sections by Note Type

### Dataset notes

Should usually include:

- what the dataset is
- key fields or structure
- coverage
- identifier semantics
- caveats
- related notes
- sources

### Identifier notes

Should usually include:

- definition
- where it appears
- join semantics
- instability or ambiguity caveats
- related notes
- sources

### Source overview notes

For `overview_source` notes with `read_scope: full_source`, the parent note is a shelf controller, not a second long digest.

Use exactly these top-level sections, in order:

- Citation / metadata
- Why this book matters
- Reading logic from the source
- Stage map
- Chapter shelf
- Core objects and modeling vocabulary
- Main themes
- Promoted durable notes
- Next promotion targets
- Caveats
- Related notes
- Sources

Do not add extra top-level sections such as scope / purpose, structural map, chapter-by-chapter technical digest, ingest status, or reflection. Put theorem-level detail in chapter digests and durable notes.

For shorter source notes, compress this structure rather than faking a chapter shelf.

### Technical chapter or section digests

Should usually include:

- ingest scope and depth
- role of the chapter or section
- core objects
- deepened subparts when applicable
- theorem / derivation content when selected for deep treatment
- quant relevance when applicable
- promoted or next promotion targets
- related notes
- sources

### Concept notes

Should usually include:

- summary
- core objects or definitions
- why it matters
- failure modes or caveats when needed
- related notes
- sources

For system or governance notes, it is often useful to state clearly which suggestions were adopted, which were rejected, and why.

### Method notes

Should usually include:

- summary
- workflow or main logic
- assumptions
- diagnostics or failure modes
- quant relevance when applicable
- related notes
- sources

### Metric notes

Should usually include:

- definition
- interpretation
- common misuse
- related notes
- sources

### Strategy notes

Should usually include:

- idea
- mechanism
- assumptions
- implementation caveats
- evaluation considerations
- related notes
- sources

## Writing Standard

For technical content, do not replace formulas, notation, algorithm steps, or theorem-level summaries with vague prose.

Prefer:

- explicit objects
- assumptions
- derivation skeletons
- algorithm logic
- failure modes

For mathematical writing in this vault:

- write real equations in MathJax form, not inline code
- use inline math for local symbols and short identities
- use block math for theorem statements, optimization problems, long derivations, and algorithm updates
- prefer shared macros from `preamble.sty` for stable notation such as `\R`, `\E`, `\Var`, `\argmin`, and `\norm{}` when they match the source cleanly
- do not flatten important equations into prose if the mathematical form is part of the meaning

## What the Agent May Edit

The agent may edit:

- `wiki/`
- `projects/`
- vault-level schema and control notes
- small supporting notes in `raw/` such as shelf trackers

The agent should not casually rewrite or rename original source files in `raw/` or physical mirror files in `catalog/`.

## Staleness and Supersession

Do not simulate memory management inside `wiki/` by deleting durable notes just because they are old.

Prefer:

- verifying and updating the note
- marking it stale, conflicted, or superseded when that is the honest state
- linking forward to the stronger replacement note

Use archival or de-prioritization logic mainly for scratch or project material, not for durable knowledge that may still matter historically.
