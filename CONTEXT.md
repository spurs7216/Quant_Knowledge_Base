# Quant Research System Context

This context defines project-specific language for the AlphaEvolve-style quant research system. It is a glossary for shared domain terms, not an implementation spec.

## Language

**Controller-Only Novelty Smoke**:
A remote controller run that tests whether novelty gates prevent occupied or equivalent children from becoming sample-evaluation candidates.
_Avoid_: automatic sample eval, broad validation, alpha validation

**Negative-Control Cell**:
A known occupied or failed behavior cell deliberately included to verify that search-control gates reject or de-prioritize repeats.
_Avoid_: target opportunity, preferred mechanism

**Underfilled Mechanism Cell**:
A behavior cell with plausible research value and insufficient nonduplicate controller evidence.
_Avoid_: duplicate pocket, occupied elite cell

**Sample-Evaluation Bar**:
The minimum controller and reproducibility evidence required before spending one remote sample evaluation.
_Avoid_: promotion rule, alpha proof

**Proof Run**:
A deliberately small run that verifies search-control wiring and artifact fields before generating a larger candidate batch.
_Avoid_: production batch, broad search

## Relationships

- A **Controller-Only Novelty Smoke** may produce zero or more sample-evaluation candidates.
- A **Controller-Only Novelty Smoke** does not itself run sample evaluation.
- A **Negative-Control Cell** may appear in a **Controller-Only Novelty Smoke** only to test guard behavior.
- An **Underfilled Mechanism Cell** is the preferred target for new child generation.
- The **Sample-Evaluation Bar** is stricter than controller pass/fail but weaker than promotion.
- A **Proof Run** should be inspected before a larger controller-only batch is launched.

## Example Dialogue

> **Dev:** "The smoke found one sample-evaluation candidate. Should the remote machine evaluate it now?"
> **Domain expert:** "No. A **Controller-Only Novelty Smoke** stops at the controller artifact; Codex reviews the artifact before any sample evaluation is launched."

## Flagged Ambiguities

- "novelty smoke" could mean controller-only or controller-plus-sample-eval; resolved: **Controller-Only Novelty Smoke** means no automatic sample evaluation.
- `ranking/industry_neutral_rank` could mean a preferred target or a guard probe; resolved: for the next smoke it should be used only as a **Negative-Control Cell** if guard verification is needed, otherwise avoided in favor of **Underfilled Mechanism Cells**.
- "known-bad attempt017 family" could mean a hard filter or a prompt/review warning; resolved: for the next smoke it is prompt memory and review context, not part of the hard **Sample-Evaluation Bar**.
- "ranking surface" could mean an underfilled target or a duplicate/replay-heavy area; resolved: exclude the whole ranking surface from the next **Controller-Only Novelty Smoke** unless a later run explicitly asks for a **Negative-Control Cell**.
- "next smoke" could mean a useful candidate batch or a wiring check; resolved: make the next smoke a six-attempt **Proof Run** before any larger controller-only batch.
