# Artifacts

This folder is the evidence layer of the vault.

Use it for bounded outputs that support research claims and wiki notes.

## What belongs here

Examples include:

- query result tables
- summary CSVs
- figures and charts
- backtest summaries
- replication snapshots
- diagnostic tables
- slide outputs

The key idea is that artifacts are small, interpretable, and linkable. They are not raw warehouse dumps.

## Provenance rule

Every meaningful artifact should preserve enough context to be trusted later.

At minimum, track:

- source dataset or table names
- execution or export date
- relevant date range
- join path if important
- row count if applicable
- filters or sample rule if applicable
- generating script, query, or workflow

If a result matters to a note in `wiki/` or `projects/`, it should be possible to trace the path back to how it was produced.

## Relationship to the rest of the vault

- `raw/` holds original sources
- `catalog/` describes mirrored data
- `projects/` reasons about active questions
- `wiki/` holds durable conclusions
- `artifacts/` holds the concrete outputs that support those conclusions

## Obsidian usage

Artifacts should be easy to browse in Obsidian:

- charts should render cleanly
- tables should be named clearly
- notes should link to their supporting files
- related wiki and project pages should reference the artifact

If an artifact is important enough to cite repeatedly, give it a short markdown wrapper note so it can participate in links, backlinks, and graph view.
