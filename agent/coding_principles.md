# Coding Principles

This file is mandatory reading before implementation, refactoring, controller/evaluator changes, prompt-contract code, dataset-contract code, or tooling changes in this vault.

Durable reference: [[Coding Principles for Quant Research Systems]].

Source notes:

- [[A Philosophy of Software Design]]
- [[A Philosophy of Software Design Selected Excerpts]]
- [[The Pragmatic Programmer]]

## Operating Rule

Do not optimize for code that merely looks tidy. Optimize for code whose important research semantics are explicit, whose module boundaries hide the right decisions, and whose behavior can be verified by focused tests or artifacts.

## Before Editing Code

Answer these questions briefly in your own reasoning before touching files:

1. What design decision does this change own?
2. Which module should own that decision?
3. What interface should callers see?
4. What important assumptions must be named, documented, or tested?
5. Is there duplicated knowledge that should become one contract?
6. What failure mode should be impossible after this change?
7. What focused verification proves the boundary works?

## Design Rules

- Prefer deep modules: small public interface, meaningful hidden implementation.
- Avoid shallow pass-through wrappers unless they isolate a real boundary.
- Hide each important decision in one place.
- Keep different layers at different abstractions.
- Pull mechanical complexity downward into the module that has the context to handle it.
- Generalize only under real pressure from likely uses.
- Define errors and special cases out of existence where a better representation can remove them.
- For nontrivial design changes, consider at least two boundary designs before implementing.

## Quant Research Rules

- Treat data grain, timestamp semantics, lagging, exposure, cost, split policy, universe construction, and evaluator metrics as first-class contracts.
- Never leave schema fields, cost assumptions, or promotion rules as duplicated informal strings.
- Strategy code must make weight timing, gross/net exposure, max weight, and cost treatment inspectable.
- Controller code must make patch format, rejection categories, uniqueness, diagnostics, and database writes inspectable.
- Prompt-building code must keep immutable output rules, retrieved memory, diagnostics, and skill cards separated.

## Comments And Names

- Write comments for intent, invariants, constraints, interface behavior, and non-obvious failure modes.
- Do not write comments that merely repeat nearby code.
- Use precise names that expose semantics such as lag, unit, data grain, before/after cost, gross/net exposure, and validation/test split.
- Treat a hard-to-name object as a design warning.

## Testing And Evidence

- Use deterministic unit tests for pure logic.
- Use semantic smoke tests for portfolio and evaluator behavior.
- Use artifacts for numerical or remote-run claims.
- Measure before optimizing performance.
- A passing test does not prove alpha validity; it proves only the contract it checks.

## Refactoring Discipline

Do not refactor simply because a file is imperfect. Refactor when the current task exposes a concrete boundary problem, duplication, hidden assumption, or failure mode. Keep the scope close to the requested work and preserve unrelated user changes.

## Red Flags During Review

- Shallow module.
- Information leakage.
- Temporal decomposition.
- Pass-through method or variable.
- Repetition of nontrivial knowledge.
- Special-purpose and general-purpose code mixed together.
- Conjoined functions that must be read together.
- Vague or misleading names.
- Non-obvious code behavior.
- Tests that execute code but do not check the research contract.
