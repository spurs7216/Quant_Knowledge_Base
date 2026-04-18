# Catalog

This folder is the vault's mirrored data catalog.

Its job is to let you and the agent understand what data exists on the remote Linux server without reopening the full warehouse locally.

## What is here

- `csv_data_catalog.md`
Human-readable inventory of the mirrored datasets.

- `csv_data_inventory.csv`
Machine-readable dataset inventory.

- `samples/`
Small mirrored samples of the original datasets with original header structure preserved.

- `samples/processed/eda/`
Compact EDA summaries and descriptive statistics.

- `samples/processed/research/`
Mirrored processed research outputs, replications, and strategy diagnostics.

## What this folder is for

Use `catalog/` to answer questions like:

- What datasets do we have?
- What are the key columns?
- What identifiers appear in each dataset?
- What date coverage exists?
- What fields are numeric, categorical, or date-like?
- What processed outputs already exist?

This folder is the data observability layer of the vault.

## What this folder is not

This is not the durable wiki.

It is also not the heavy warehouse itself.

Do not treat `catalog/` as the place for:

- final dataset explanations
- project conclusions
- strategy interpretations
- freeform notes

Those belong in `wiki/` or `projects/`.

## Recommended workflow

1. Start with `csv_data_catalog.md` or `csv_data_inventory.csv`.
2. Inspect a relevant sample file under `samples/`.
3. Inspect the EDA summaries under `samples/processed/eda/`.
4. Create or update a durable note in `wiki/` if the understanding is reusable.
5. Link a project note in `projects/` if the question is still active.

## Current mirror profile

The mirror currently covers 706 files and about 43.94 GB of source data on the remote side.

Important mirrored areas include:

- `daily_stock`
- `CCM`
- `comp_na_daily_all_annual`
- `option_forward_price`
- `option_volumne`
- `ownership_13F`
- `Fama–French`
- Treasury and risk-free data
- mirrored processed research outputs

## Naming policy

Preserve the exact mirror names when referring to physical files.

That includes legacy spellings such as:

- `option_volumne`
- `Treasurey_Daily_Time_Series`
- `Treasurey_Term_structure`

If cleaner aliases are needed, create them in `wiki/`, not by renaming the mirror.
