# Raw

This folder is the source library of the vault.

It contains the materials the agent reads from but does not treat as the compiled knowledge base.

## What is here

Current source areas include:

- `books_cn/`
- `econometrics/`
- `finance_microstructure/`
- `interview_questions/`
- `LLM Knowledge Bases/`
- `machine_learning/`
- `math_statistics/`
- `quantitative_finance/`

These are domain-oriented shelves inside the vault's source library.

Shelf notes:

- `math_statistics/README.md` tracks the ordered source inventory and active ingest status for the math/statistics shelf, including books, bridge tutorials, and compact references rather than only formal books.

## What this folder is for

Use `raw/` for:

- books
- papers
- textbooks
- clipped articles
- reference notes
- images and source attachments

This is the input layer for the vault.

## What this folder is not

This is not the final wiki.

Do not use `raw/` as the place for:

- durable synthesis
- project conclusions
- cleaned dataset explanations
- final strategy notes

Those belong in `wiki/` or `projects/`.

## Special note: `LLM Knowledge Bases/`

This subfolder is important for the vault itself.

It contains source material about the Karpathy workflow and related knowledge-base ideas, including:

- the original Karpathy thread
- the `llm-wiki.md` gist
- supporting or adjacent notes about LLM knowledge bases and Obsidian

Treat it as the design-source shelf for the vault system.

## Handling rule

Prefer to preserve source materials as they are.

If a source needs interpretation:

1. keep the original in `raw/`
2. create or update the understanding in `wiki/`
3. use `projects/` if the interpretation is still evolving
