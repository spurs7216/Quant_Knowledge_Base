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

## Navigation notes

The main control notes in this folder are:

- `index.md` for the durable map of important notes
- `log.md` for chronological maintenance history
- `glossary.md` for recurring terms
- `maps/reading_map.md` for major domain coverage and reading order
- `inbox.md` for candidate sources and note targets

## Current folder map

- root control notes: `index.md`, `log.md`, `glossary.md`, `inbox.md`
- `maps/` for domain entry points such as reading, math, statistics, ML, finance, microstructure, signal-processing maps, and `.canvas` overviews
- `datasets/` for durable dataset pages
- `identifiers/` for keys, join semantics, and identifier caveats
- `sources/books/`, `sources/papers/`, and `sources/articles/` for source notes
- `concepts/` for models, markets, risks, systems, and other cross-source conceptual syntheses
- `methods/` for statistics, econometrics, validation, and technical workflows
- `metrics/` for evaluation and research measures
- `strategies/` for alpha, portfolio, and execution theses
- `_templates/` for lightweight note templates

Create durable notes here. Keep active or uncertain work in `projects/` until it is ready to crystallize.

Canvas guidance:

- use `.canvas` files in `wiki/maps/` for vault-level structure and navigation
- keep the factual content in markdown notes and use the canvas to point at those notes
- prefer a small number of maintained canvases over many abandoned boards
