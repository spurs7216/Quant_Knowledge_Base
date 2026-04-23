# Quant Knowledge Vault Agent

This file is the authoritative entry point for the vault schema.

The detailed operating rules are split into smaller files under [`agent/`](agent/):

- [agent/core.md](agent/core.md): mission, trust hierarchy, model-memory policy, quant standards, and success criteria
- [agent/operations.md](agent/operations.md): ingest, query, lint, crystallize, govern, provenance, and contradiction handling
- [agent/notes.md](agent/notes.md): folder doctrine, note standards, frontmatter, and edit scope
- [agent/obsidian.md](agent/obsidian.md): Obsidian usage, links, Bases, tags, MCP / CLI, and plugin-aware conventions

Read this file first. Then read the relevant subfile for the task.

## Mission

Build and maintain a durable quantitative research vault that compounds over time and supports research that could matter in real trading.

The standard is not broad note coverage. The standard is research support that is:

- mathematically sound
- statistically defensible
- logically coherent
- computationally implementable
- financially realistic
- robust to noise, costs, constraints, and regime change

## Non-negotiable Rules

### 1. The vault stores what the research system must know explicitly

Model memory can help reasoning, but it is not inspectable or stable enough to be the vault's memory.

### 2. Trust order

Use this hierarchy:

1. `raw/`
2. `catalog/`
3. `artifacts/`
4. `wiki/`
5. `projects/`

If a higher-level note conflicts with a lower-level source, fix the higher-level note.

### 3. Long-source ingest is a 3-step workflow

1. scan the full source chapter by chapter or section by section
2. select what matters and deepen the selected chapters to theorem-level detail, while rescanning non-selected parts for any local theorem, concept, caveat, or derivation that still deserves deeper treatment
3. promote the strongest reusable material into durable notes outside the source shelf

Do not stop at shallow source stubs for quant materials.

### 4. Math and statistics come first

Weak foundations contaminate later econometrics, machine learning, finance, and trading research. When a source is mathematically or statistically heavy, prefer theorem-level, derivation-level, and object-level understanding over surface summary.

### 5. Durable knowledge and active work must stay separate

- use `wiki/` for durable reusable understanding
- use `projects/` for active uncertain work
- use `artifacts/` for bounded evidence

### 6. Obsidian is the frontend, not the source of truth

Use links, Bases, tags, canvases, and MCP / CLI operations to maintain the vault well, but keep markdown notes and provenance as the underlying source of truth.

## Vault Map

- `raw/`: source library
- `catalog/`: mirrored data catalog and observability layer
- `wiki/`: durable compiled knowledge base
- `projects/`: active investigations and synthesis-in-progress
- `artifacts/`: bounded evidence outputs
- `.obsidian/`: frontend and automation surface

## Read Order

Always read this file first, then:

- read [agent/operations.md](agent/operations.md) for source work, query work, or lint work
- read [agent/notes.md](agent/notes.md) before creating or restructuring notes
- read [agent/obsidian.md](agent/obsidian.md) when the task is Obsidian-native
- read [agent/core.md](agent/core.md) when the task affects mission, standards, or governance

Also read the relevant layer README files before editing:

- [README.md](README.md)
- [raw/README.md](raw/README.md)
- [catalog/README.md](catalog/README.md)
- [wiki/README.md](wiki/README.md)
- [projects/README.md](projects/README.md)
- [artifacts/README.md](artifacts/README.md)

## Immediate Priorities

- continue building the math / statistics shelf carefully
- keep ingest honest: full scan, theorem-level deepen where selected, then promotion
- connect source notes forward into durable concepts and methods
- support future quant research that can survive real implementation standards
