"""Utilities for finding bounded AlphaEvolve-style code regions."""

from __future__ import annotations

from dataclasses import dataclass


START_MARKER = "# EVOLVE-BLOCK-START"
END_MARKER = "# EVOLVE-BLOCK-END"


@dataclass(frozen=True)
class EvolveBlock:
    """A marked code region that may be changed by the search loop."""

    index: int
    start_line: int
    end_line: int
    text: str


class EvolveBlockError(ValueError):
    """Raised when evolve-block markers are malformed."""


def find_evolve_blocks(program_text: str) -> list[EvolveBlock]:
    """Return all evolve blocks in a program.

    Line numbers are one-based and include the marker lines. The returned text is
    the code between the markers, excluding the marker lines themselves.
    """

    lines = program_text.splitlines(keepends=True)
    blocks: list[EvolveBlock] = []
    open_start: int | None = None
    open_body_start: int | None = None

    for pos, line in enumerate(lines):
        line_number = pos + 1
        if START_MARKER in line:
            if open_start is not None:
                raise EvolveBlockError(f"nested evolve block starts at line {line_number}")
            open_start = line_number
            open_body_start = pos + 1
            continue
        if END_MARKER in line:
            if open_start is None or open_body_start is None:
                raise EvolveBlockError(f"end marker without start at line {line_number}")
            body = "".join(lines[open_body_start:pos])
            blocks.append(
                EvolveBlock(
                    index=len(blocks),
                    start_line=open_start,
                    end_line=line_number,
                    text=body,
                )
            )
            open_start = None
            open_body_start = None

    if open_start is not None:
        raise EvolveBlockError(f"unterminated evolve block starting at line {open_start}")
    return blocks


def require_evolve_blocks(program_text: str) -> list[EvolveBlock]:
    """Return evolve blocks, raising if none are present."""

    blocks = find_evolve_blocks(program_text)
    if not blocks:
        raise EvolveBlockError("program has no evolve blocks")
    return blocks
