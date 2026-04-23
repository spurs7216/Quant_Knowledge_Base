# Operations

This file expands the workflow rules from [../AGENTS.md](../AGENTS.md).

## Operational Modes

The main modes are:

1. initialize
2. ingest
3. query
4. lint
5. crystallize
6. govern

## Knowledge Lifecycle Rule

Do not treat all vault content as one flat memory layer.

Use this lifecycle:

- `raw/` for immutable source memory
- `projects/` for working or episodic memory such as active reasoning, temporary synthesis, and session-level findings
- `wiki/` for semantic and procedural memory that should stay reusable across sessions
- `catalog/` and `artifacts/` for evidence and observability memory that supports numerical or operational claims

Operational implication:

- do not promote fresh observations directly into durable notes just because they look useful once
- let repeated, verified, or high-leverage material crystallize upward
- do not solve "memory rot" in `wiki/` by silent forgetting; use explicit stale, conflicted, or superseded handling instead

## Initialize

Use initialize mode when a shelf, folder, or sub-area needs basic control notes or structure.

Typical tasks:

1. inspect the current tree
2. read the relevant README files and schema
3. create missing index, log, map, glossary, or template notes
4. avoid full corpus ingest unless explicitly requested

### Raw shelf controller rule

For shelf-control notes such as `raw/<shelf>/README.md`:

- order all source-like items currently in the folder, not only formal books
- use one unified ordered shelf table instead of splitting "main books" and "bridge resources" into separate sequences when they belong to the same working shelf
- if the shelf mixes books, tutorials, notes, or compact references, make the source role explicit in the table
- `NEXT` means the next active ingest target, not necessarily the next unfinished formal book
- bridge or tutorial sources can remain queued while still holding an explicit place in the ordered shelf

## Ingest

### Standard ingest flow

1. read the source in `raw/`
2. classify the source
3. create or update scan notes
4. choose what deserves deep treatment
5. deepen the selected material
6. promote the strongest reusable material into durable notes
7. update `projects/` if the source belongs to active work
8. update `wiki/log.md` and `wiki/index.md` when needed

### Trigger rules

Treat these as event-like maintenance triggers even when the workflow is still manual:

- on new source added to a managed shelf: update the shelf controller if the ordering or active queue changes
- on meaningful ingest completion: update `wiki/log.md`, and update `wiki/index.md` if a durable entry point changed
- on contradiction or major correction: resolve against the trust hierarchy and mark supersession or conflict explicitly rather than only rewriting prose quietly
- on durable outcome from a project or query chain: crystallize it into `wiki/` or file bounded evidence into `artifacts/`
- on periodic maintenance work: run lint for stale notes, orphan notes, unsupported claims, and broken or outdated cross-references

### Source classes

- `overview_source`: whole-source note for a book, long report, survey, or large article
- `chapter_digest`: chapter-level or section-level note for large sources
- `article_source`: bounded article, paper, essay, or shorter source
- `metadata_stub`: provisional note created from metadata or weak extraction only

Do not let `metadata_stub` notes masquerade as deep knowledge.

### 3-step rule for long sources

For books, long papers, long reports, and long markdown sources:

1. `scan pass`
   Build honest coverage chapter by chapter or section by section.
2. `selection and deepen pass`
   Decide which chapters, sections, proofs, appendices, examples, or exercises are load-bearing. Deepen the selected chapters to theorem-level detail. Rescan the non-selected parts and deepen any local theorem, derivation, caveat, or concept that still matters.
3. `promotion pass`
   Promote the strongest reusable material into `wiki/concepts/`, `wiki/methods/`, `wiki/metrics/`, or `wiki/strategies/`.

### Theorem-level standard

When a chapter or section is selected for deep treatment, the target is not a better summary. The target is theorem-level or derivation-level understanding.

At minimum, capture:

- the main objects
- theorem or proposition statements when they matter
- assumptions
- proof idea or derivation skeleton
- why the result matters later
- relevant failure modes or misuse points

For mathematically heavy material, also preserve:

- the load-bearing equations in MathJax form, not only prose paraphrase
- theorem hypotheses and conclusions in notation that can be inspected directly
- optimization problems, update equations, and residual definitions as explicit display math when they are central

For foundational math and statistics, theorem-oriented notes are the default for selected deep chapters.

### Math writing and verification rule

For math, statistics, optimization, and theorem-heavy source work:

- write equations in Obsidian MathJax syntax using `$...$` or `$$...$$`, not backticks
- use the shared vault macros in `preamble.sty` for recurring notation when they fit the source cleanly
- use display math for load-bearing theorem statements, optimization problems, derivations, algorithm updates, and residual definitions
- if PDF extraction mangles notation, use formula OCR on a cropped equation before writing the durable note
- if a central equation is still uncertain, normalize or parse it with the local LaTeX parser and check it with SymPy before promoting the result outward

### PDF ingest and render rule

For PDF-heavy ingest, prefer a staged evidence workflow instead of treating the whole PDF as images:

1. use text extraction or markdown conversion first for broad coverage
2. render the table of contents and front-matter pages first when the chapter map or source structure is still unclear
3. render only load-bearing pages when visual layout matters

Load-bearing pages usually include:

- theorem, proposition, lemma, corollary, or definition pages
- derivation pages with dense displayed math
- pages where equations, indices, or line breaks are corrupted by extraction
- figures or tables that carry modeling assumptions or algorithm structure
- adjacent continuation pages when a theorem, proof, derivation, or example spans page boundaries

Do not render routine exposition pages just because they belong to a deep chapter. If text extraction is already clean and the page is not load-bearing, keep the cheaper text path.

For theorem-heavy math and finance books, do not claim theorem-level understanding from text extraction alone when notation, alignment, or page structure is ambiguous. Escalate to rendered-page reading before writing the durable note.

### PDF render cache hygiene rule

Rendered page images and temporary PDF conversions under `.codex/memories` are scratch evidence, not part of the vault.

- keep renders in a book-specific folder or clearly named file group
- keep the rendered set sparse and evidence-driven rather than rendering full chapters by habit
- prefer a small reusable set of TOC pages, structure pages, and load-bearing theorem or derivation pages
- after the ingest is verified, keep only the minimal render set that still helps near-term continuation or verification
- if the cached images no longer support an active ingest, follow-up verification, or imminent reingest, remove the book-specific scratch cache instead of letting memories become a shadow archive
- never treat `.codex/memories` as a durable citation layer; the durable output belongs in `wiki/`, and the source of truth remains `raw/`

### Selection rule

Prefer deep treatment for material that is:

- foundational for later math, statistics, econometrics, finance, or ML
- easy to misuse if left vague
- central to inference quality, robustness, or research validity
- repeatedly reusable across future projects

Not every chapter needs equal depth:

- some chapters remain scan notes
- some become deep notes
- some routine chapters only need one deep subpart

### Sensitive-source rule

Do not copy secrets, tokens, passwords, private credentials, or unnecessary PII from `raw/` into `wiki/`, `projects/`, `artifacts/`, `index.md`, or `log.md`.

If a sensitive source matters structurally:

- abstract the pattern
- redact the sensitive values
- keep the durable lesson without turning the vault into a secret spill layer

### Storage rule

- keep one stable overview note at `wiki/sources/books/<Book Title>.md`
- store chapter digests under `wiki/sources/books/<Book Title>/`
- keep chapter titles predictable and source-linked
- use the same parent-note plus child-folder pattern only when the source truly needs many subordinate notes

### Full-source overview note rule

For `overview_source` notes with `read_scope: full_source`, the parent note is the stable shelf controller.

Use exactly this top-level section order:

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

Do not duplicate a chapter-by-chapter technical digest in the parent overview. Put deep technical detail in child chapter notes and promote reusable material outward into durable notes.

### Promotion rule

Important source content must not remain trapped in source notes.

Promote reusable material into:

- `wiki/concepts/`
- `wiki/methods/`
- `wiki/metrics/`
- `wiki/strategies/`

Promotion should favor:

- ideas that recur across chapters or future projects
- concepts that are easy to misuse if left buried
- methods whose assumptions and diagnostics need to remain explicit

## Query

Answer from the vault first.

Use internal knowledge to frame the search, but ground the durable answer in explicit material.

### Retrieval routing rule

- choose the evidence layer first, then use the lowest-cost tool that can answer reliably within that layer
- treat tool choice as a means, not a law; the goal is reliable grounded answers from the vault
- do not pay semantic-search cost when exact matching or a known path is enough
- do not pay raw-source cost when compiled notes already support the claim
- if a cheaper tool or cheaper layer is insufficient, escalate deliberately rather than mixing tools by habit

### Lowest-cost capable tool ladder

Within the current target layer, prefer:

1. direct path reads or exact text search such as `rg` when the file, shelf, heading, or literal phrase is already known
2. Obsidian-native operations when the work is note-local and benefits from vault context such as backlinks, properties, appends, tabs, or Bases
3. QMD `query` when the target note is not yet known and the retrieval problem is broad, fuzzy, cross-source, or semantic
4. QMD `get` / `multi_get` after QMD has already surfaced indexed notes and fast read-only retrieval of one or many candidate notes is needed
5. `raw/` access, including PDF tooling, when the compiled vault is insufficient, ingest is underway, contradiction resolution reaches the source layer, or source-level wording matters

Operational implications:

- use QMD to discover, not to replace verification
- once a note is known, switch back to direct reads or Obsidian unless QMD `get` / `multi_get` is clearly cheaper
- use filesystem reads plus `apply_patch` for structural edits or multi-file refactors rather than forcing retrieval tools into write workflows
- if QMD is unavailable, cold, or low-signal for the question, fall back immediately to exact search, direct note reads, or the normal vault query order rather than forcing semantic search

Query order:

1. `wiki/`
2. `projects/`
3. `catalog/`
4. `artifacts/`
5. `raw/` when needed

### Index and log role rule

Treat the control notes differently:

- `wiki/index.md` is a curated human gateway to durable entry points, not the primary machine retrieval substrate once the vault grows
- `wiki/log.md` is the chronological audit trail, not a second content index
- keep `index.md` useful for browsing, orientation, and major entry points, but do not let it turn into the only place where stage maps, shelf state, or discovery logic live
- if retrieval would require scanning a bloated `index.md`, switch to exact search, Obsidian, or QMD instead of expanding the index further

## Lint

Regularly check for:

- contradictions
- stale claims
- weak or missing provenance
- broken links
- duplicate pages
- source notes that overclaim depth
- unsupported numerical claims

Quant-specific lint checklist:

- survivorship bias
- look-ahead bias
- leakage
- identifier mismatches
- missing cost assumptions
- unclear timestamp conventions
- overclaiming from a single backtest

## Crystallize

Use crystallize mode when active work in `projects/` becomes stable enough to turn into durable knowledge.

Typical outputs:

- concept notes
- method notes
- dataset or identifier notes
- strategy or metric notes

## Govern

Use govern mode when the schema, folder structure, naming rules, or maintenance policy needs revision.

Typical tasks:

- adjust the ingest workflow
- improve note classes
- revise templates
- tighten provenance or evidence rules

## Provenance and Evidence

Every meaningful durable note should say where it comes from.

At minimum, preserve:

- source note links
- dataset or artifact references when relevant
- date or update fields when timing matters

If a claim is numerical or empirical, link evidence rather than leaving the claim unsupported.

### Verification and supersession rule

When freshness or contradiction matters, prefer explicit lifecycle metadata over silent drift.

Useful optional fields include:

- `last_verified`
- `verification_status`
- `supersedes`
- `superseded_by`

Use them when:

- a note's claims were recently checked against source or evidence
- a note has been materially weakened by newer information
- one note replaces another as the current durable view

Do not invent fake numeric confidence scores for claims just to look precise. Prefer inspectable provenance, explicit caveats, and honest verification state.

## Contradiction Handling

When two notes conflict:

1. check `raw/`, `catalog/`, or verified `artifacts/`
2. determine which note is weaker or stale
3. update the weaker note
4. leave an explicit caveat if the conflict is not fully resolved

If the newer note materially replaces the older view:

5. link the replacement with `supersedes` / `superseded_by` when useful
6. avoid leaving the older note looking current by omission

## Index and Log

- update `wiki/index.md` when a note becomes a durable entry point
- update `wiki/log.md` for meaningful schema, ingest, or promotion work
