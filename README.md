# Quant Knowledge Vault

A source-grounded quantitative research vault and project control layer.

This repository combines an Obsidian knowledge base, active research project notes, compact data catalogs, evidence artifacts, and executable research tooling. The goal is to make quantitative finance research compound across sessions: sources become durable knowledge, project work stays tied to explicit assumptions, and numerical claims remain connected to reproducible evidence.

The vault is not a data warehouse, broker account, or secret store. Heavy market data, GPU inference, and warehouse-scale evaluation run on the remote Linux machine. This repository holds the local control plane: reasoning, manifests, code, compact evidence, and reviewed conclusions.

## What This Vault Is For

- Building durable math, statistics, machine learning, market microstructure, and quantitative finance knowledge.
- Turning papers, books, and implementation experience into reusable notes under `wiki/`.
- Managing active research systems under `projects/`, especially work that needs remote evaluation.
- Keeping compact data contracts and dataset observability in `catalog/`.
- Preserving bounded evidence in `artifacts/` when a result, diagnosis, or remote run needs to be reviewed later.

## Main Project

The flagship active project is the quant research system in [`projects/quant_research_system/`](projects/quant_research_system/).

Its purpose is to move from research ideas to increasingly realistic evidence:

1. define research tasks and contracts locally
2. run heavy data, model, and evaluator jobs on the remote Linux machine
3. import compact artifacts for local review
4. promote durable lessons into `wiki/`
5. keep candidate strategies, implementation constraints, and falsification evidence inspectable

The current active line is the Phase 4 AlphaEvolve-lite search loop: a controller-driven alpha discovery workflow with prompt sampling, open-model generation on the remote machine, evaluator pools, a program database, semantic filters, diversity pressure, and a reasoning-memory layer.

## Repository Map

- [`wiki/`](wiki/): durable compiled knowledge, including source notes, concepts, methods, metrics, strategies, datasets, and maps.
- [`projects/`](projects/): active investigations and systems that are still changing.
- [`research/`](research/): executable support code for validation, candidate registries, implementation translation, and AlphaEvolve-lite experiments.
- [`catalog/`](catalog/): compact data catalogs, schema evidence, sample summaries, and dataset observability.
- [`artifacts/`](artifacts/): bounded evidence outputs from remote runs, diagnostics, charts, tables, and reviews. Most generated artifacts are not tracked by git.
- [`raw/`](raw/): local source library for books, papers, articles, and reference material. Copyrighted or bulky source files are not meant to be pushed.
- [`agent/`](agent/): operating rules for agents and contributors.
- [`AGENTS.md`](AGENTS.md): authoritative agent entry point and vault schema.
- [`.obsidian/`](.obsidian/): Obsidian frontend configuration where portable and safe to track.

## How To Navigate

Start with [`wiki/index.md`](wiki/index.md) for durable entry points.

For the quant research system, read:

- [`projects/quant_research_system/brief.md`](projects/quant_research_system/brief.md)
- [`projects/quant_research_system/build_sequence.md`](projects/quant_research_system/build_sequence.md)
- [`projects/quant_research_system/architecture.md`](projects/quant_research_system/architecture.md)
- [`projects/quant_research_system/phase4_search_loop/current_state.md`](projects/quant_research_system/phase4_search_loop/current_state.md)

For agent or contributor work, start with [`AGENTS.md`](AGENTS.md), then read the relevant files under [`agent/`](agent/).

## Research Standards

The vault is built around a few research constraints:

- Mathematical and statistical claims should be explicit enough to inspect.
- Empirical claims should link to source notes, datasets, artifacts, or reproducible code.
- Strategy results should account for costs, turnover, concentration, exposure, data availability, and implementation limits.
- Remote jobs should return compact evidence, not raw warehouse data.
- IBKR, TWS, account state, and broker execution logic are local-only concerns and must not be pushed to the remote machine.

## Git And Data Boundaries

The git repository is intentionally narrower than the full local vault.

Tracked material should generally include markdown notes, schemas, manifests, portable Obsidian config, and research code. Do not track raw books or PDFs, warehouse data samples, generated artifact bundles, credentials, API keys, broker settings, or machine-specific secrets.

GitHub is used as a synchronization channel when the remote machine needs to pull a specific code or manifest state. It is not the default destination after every local edit.

## Obsidian

Obsidian is the frontend for browsing, linking, reviewing, and editing the vault. Markdown files remain the source of truth. The graph, backlinks, Bases, Dataview, canvases, and local automation are useful interfaces over the same repository structure.

## Status

This is an active research workspace. Some folders contain stable durable knowledge; others contain live design notes, remote-run instructions, and experiment evidence. Prefer the layer READMEs, current project state files, and artifact reviews over stale assumptions from chat history.
