"""Parser and applier for AlphaEvolve-style SEARCH/REPLACE diffs."""

from __future__ import annotations

from dataclasses import dataclass


SEARCH_MARKER = "<<<<<<< SEARCH"
SEPARATOR_MARKER = "======="
REPLACE_MARKER = ">>>>>>> REPLACE"


@dataclass(frozen=True)
class SearchReplaceBlock:
    """One exact code replacement proposed by a generator."""

    search: str
    replace: str


class DiffBlockError(ValueError):
    """Raised when a generated diff block cannot be parsed or applied."""


def parse_search_replace_blocks(diff_text: str) -> list[SearchReplaceBlock]:
    """Parse SEARCH/REPLACE blocks from generated text."""

    lines = diff_text.splitlines(keepends=True)
    blocks: list[SearchReplaceBlock] = []
    pos = 0

    while pos < len(lines):
        if not lines[pos].lstrip().startswith(SEARCH_MARKER):
            pos += 1
            continue

        pos += 1
        search_lines: list[str] = []
        while pos < len(lines) and not lines[pos].lstrip().startswith(SEPARATOR_MARKER):
            search_lines.append(lines[pos])
            pos += 1
        if pos >= len(lines):
            raise DiffBlockError("SEARCH block missing separator")

        pos += 1
        replace_lines: list[str] = []
        while pos < len(lines) and not lines[pos].lstrip().startswith(REPLACE_MARKER):
            replace_lines.append(lines[pos])
            pos += 1
        if pos >= len(lines):
            raise DiffBlockError("SEARCH block missing REPLACE terminator")

        blocks.append(SearchReplaceBlock(search="".join(search_lines), replace="".join(replace_lines)))
        pos += 1

    if not blocks:
        raise DiffBlockError("no SEARCH/REPLACE blocks found")
    return blocks


def apply_search_replace(program_text: str, diff_text: str) -> str:
    """Apply generated SEARCH/REPLACE blocks to a program.

    Each search segment must occur exactly once in the current program. This keeps
    generated patches auditable and prevents accidental broad replacements.
    """

    child = program_text
    for block in parse_search_replace_blocks(diff_text):
        count = child.count(block.search)
        if count == 0:
            raise DiffBlockError("search segment was not found in program")
        if count > 1:
            raise DiffBlockError("search segment matched multiple locations")
        child = child.replace(block.search, block.replace, 1)
    return child
