"""Export the daily-stock expression interface for remote agents.

The generated files are prompt-facing artifacts.  They let a remote LLM inspect
the exact fields, operators, and starter seeds without importing project code.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _ensure_repo_import() -> None:
    repo_root = Path(__file__).resolve().parents[3]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))


_ensure_repo_import()

from research.alphaevolve_lite.expression_evolution import (  # noqa: E402
    expression_interface_markdown,
    expression_seed_library_rows,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Directory where expression_interface.md and expression_seed_library.json are written.",
    )
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "expression_interface.md").write_text(
        expression_interface_markdown(),
        encoding="utf-8",
    )
    (args.output_dir / "expression_seed_library.json").write_text(
        json.dumps(expression_seed_library_rows(), indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
