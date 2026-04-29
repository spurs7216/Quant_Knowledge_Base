"""CLI for the Phase 4 AlphaEvolve-lite controller."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _ensure_repo_import() -> None:
    repo_root = Path(__file__).resolve().parents[3]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run AlphaEvolve-lite controller stages.")
    parser.add_argument("--config", required=True, help="Path to Phase 4 YAML config.")
    parser.add_argument("--stage", required=True, help="Stage to run. Use controller_static for this milestone.")
    parser.add_argument("--run-id", help="Optional deterministic run id.")
    return parser.parse_args()


def main() -> int:
    _ensure_repo_import()
    from research.alphaevolve_lite.controller import run_controller

    args = parse_args()
    try:
        result = run_controller(args.config, args.stage, args.run_id)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
