"""Profile rolling top-N coverage and forward-return availability."""

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

from research.alphaevolve_lite.splits import (  # noqa: E402
    DEFAULT_ANALYSIS_END_DATE,
    DEFAULT_ANALYSIS_START_DATE,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run a chunked rolling top-N coverage and forward-return availability diagnostic. "
            "This writes data-understanding artifacts only; it does not evaluate alpha."
        )
    )
    parser.add_argument("--csv-path", required=True, help="Path to daily_stock CSV.")
    parser.add_argument("--out-dir", required=True, help="Directory for diagnostic artifacts.")
    parser.add_argument("--chunksize", type=int, default=1_000_000, help="CSV chunk size.")
    parser.add_argument("--top-n", type=int, default=500, help="Rolling monthly top-N universe size.")
    parser.add_argument(
        "--coverage-start-date",
        default=None,
        help=(
            "Optional start date for the whole-timeline top-N coverage scan. Leave unset for "
            "the full available timeline."
        ),
    )
    parser.add_argument(
        "--coverage-end-date",
        default=None,
        help=(
            "Optional end date for the whole-timeline top-N coverage scan. Leave unset for "
            "the full available timeline."
        ),
    )
    parser.add_argument(
        "--forward-start-date",
        default=DEFAULT_ANALYSIS_START_DATE,
        help="Start date for evaluator-style next-day return availability diagnostics.",
    )
    parser.add_argument(
        "--forward-end-date",
        default=DEFAULT_ANALYSIS_END_DATE,
        help="End date for evaluator-style next-day return availability diagnostics.",
    )
    parser.add_argument(
        "--max-input-rows",
        type=int,
        default=None,
        help="Raw row cap for smoke tests only. Leave unset for the remote full timeline.",
    )
    return parser.parse_args()


def _validate_args(args: argparse.Namespace) -> None:
    if args.chunksize <= 0:
        raise ValueError("--chunksize must be positive")
    if args.top_n <= 0:
        raise ValueError("--top-n must be positive")
    if args.max_input_rows is not None and args.max_input_rows <= 0:
        raise ValueError("--max-input-rows must be positive when provided")


def main() -> int:
    _ensure_repo_import()
    from research.alphaevolve_lite.daily_stock_forward_coverage import (
        profile_daily_stock_forward_coverage,
    )

    args = parse_args()
    try:
        _validate_args(args)
        result = profile_daily_stock_forward_coverage(
            csv_path=args.csv_path,
            out_dir=args.out_dir,
            chunksize=args.chunksize,
            top_n=args.top_n,
            coverage_start_date=args.coverage_start_date,
            coverage_end_date=args.coverage_end_date,
            forward_start_date=args.forward_start_date,
            forward_end_date=args.forward_end_date,
            max_input_rows=args.max_input_rows,
        )
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({"status": "ok", **result}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
