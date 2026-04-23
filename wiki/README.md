# Wiki

This folder is the compiled knowledge base of the vault.

If `raw/` is the source library and `catalog/` is the mirrored data catalog, then `wiki/` is the durable layer of understanding that the agent maintains over time.

## What belongs here

Use `wiki/` for notes that should remain valuable across many sessions:

- map notes
- canvas maps
- source notes
- concept notes
- dataset notes
- field and identifier notes
- method notes
- metric notes
- strategy notes
- glossary notes

This folder should contain explanations, structure, and synthesis.

## What should not live here

Do not use `wiki/` for:

- raw PDFs
- clipped source dumps
- untouched sample CSVs
- temporary scratch work
- project-only reasoning that is not yet stable

Those belong in `raw/`, `catalog/`, or `projects/`.

## Writing conventions

Because this is an Obsidian vault, notes here should be:

- linkable
- readable on their own
- stable in title
- explicit about sources
- useful in graph view and backlinks

For mathematical notes:

- write equations with MathJax delimiters, not backticks
- use the shared root `preamble.sty` macros when they help notation stay stable across notes
- keep load-bearing formulas explicit instead of paraphrasing them away

Recommended note properties when helpful:

- `type`
- `status`
- `tags`
- `source`
- `source_count`
- `updated`
- `dataset`
- `project`

## Note types to prioritize

The first useful note classes for this vault are:

- map
- source
- concept
- dataset
- identifier
- method
- metric
- strategy
- glossary

For this quant vault, the most important early notes will likely cover:

- `daily_stock`
- `CCM`
- `comp_na_daily_all_annual`
- `option_forward_price`
- `permno`
- `gvkey`
- `secid`
- `cusip`

## Relationship to `projects/`

Use `projects/` for active investigation.

Use `wiki/` for durable understanding that should persist after the investigation ends.

If a project produces a stable insight, the agent should crystallize it into `wiki/`.

## Relationship to Obsidian

Obsidian is the main way to inspect this folder:

- browse the graph
- follow backlinks
- use Dataview to summarize notes
- use search to discover relevant pages
- review linked structures visually

The better the agent maintains this folder, the more useful Obsidian becomes as the vault frontend.

Query and discovery rule:

- use direct reads or exact search when the target note, filename, heading, or phrase is already known
- use Obsidian for note-local browsing, backlink work, and edits
- use QMD for broad or fuzzy discovery across the compiled wiki when the target note is not yet known
- use `raw/` sources or PDFs only when ingest or source verification requires it
- do not treat retrieval quality as a substitute for verification; open the actual notes before making durable claims or edits

## Navigation notes

The main control notes in this folder are:

- `index.md` for the curated durable map of important notes
- `log.md` for chronological maintenance history
- `glossary.md` for recurring terms
- `maps/reading_map.md` for major domain coverage and reading order
- `inbox.md` for candidate sources and note targets

Role split:

- `index.md` is a human-facing gateway, not the primary search engine for the agent at large scale
- `log.md` is the audit trail of changes, not a second navigation tree
- broad discovery should move to exact search or QMD once the target note is not already obvious

## Current folder map

- root control notes: `index.md`, `log.md`, `glossary.md`, `inbox.md`
- `maps/` for domain entry points such as reading, math, statistics, ML, finance, microstructure, signal-processing maps, and `.canvas` overviews
- `datasets/` for durable dataset pages
- `identifiers/` for keys, join semantics, and identifier caveats
- `sources/books/` for stable book overview notes and `sources/books/<Book Title>/` for chapter digests of deeply ingested books
- `sources/papers/` and `sources/articles/` for source notes that do not need a book-style chapter shelf
- `concepts/` for models, markets, risks, systems, and other cross-source conceptual syntheses
- `methods/` for statistics, econometrics, validation, and technical workflows
- `metrics/` for evaluation and research measures
- `strategies/` for alpha, portfolio, and execution theses
- `_templates/` for lightweight note templates

Storage rule for large books:

- keep the canonical book note at `sources/books/<Book Title>.md`
- store chapter or theorem-level digests under `sources/books/<Book Title>/`
- use predictable source-linked chapter titles so search, backlinks, and Bases remain stable
- for `overview_source` book notes with `read_scope: full_source`, keep the parent note thin and use this fixed section order: Citation / metadata, Why this book matters, Reading logic from the source, Stage map, Chapter shelf, Core objects and modeling vocabulary, Main themes, Promoted durable notes, Next promotion targets, Caveats, Related notes, Sources
- do not turn the parent overview into a second chapter-by-chapter digest; deep technical content belongs in the child shelf and the promoted durable notes

Ingest rule for long sources:

- first do a full scan pass chapter by chapter or section by section so the vault has honest coverage of the whole source
- then deepen only the load-bearing chapters or sections, rather than forcing uniform depth everywhere, and rescan the non-selected parts for any local theorem, idea, or caveat that still deserves partial deepening
- then promote the strongest reusable material from the source shelf into durable notes under `concepts/`, `methods/`, `metrics/`, or `strategies/`
- if one chapter is mostly routine but contains one critical idea, theorem, or caveat, deepen that part explicitly without rewriting the whole chapter at maximal depth

Create durable notes here. Keep active or uncertain work in `projects/` until it is ready to crystallize.

Canvas guidance:

- use `.canvas` files in `wiki/maps/` for vault-level structure and navigation
- keep the factual content in markdown notes and use the canvas to point at those notes
- prefer a small number of maintained canvases over many abandoned boards
