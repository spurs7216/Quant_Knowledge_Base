"""Profile daily_stock data into compact Phase 4 EDA artifacts."""

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
    parser = argparse.ArgumentParser(
        description=(
            "Run a chunked daily_stock empirical profile. This writes data-understanding "
            "artifacts only; it does not evaluate alpha."
        )
    )
    parser.add_argument("--csv-path", required=True, help="Path to daily_stock CSV.")
    parser.add_argument("--out-dir", required=True, help="Directory for compact EDA artifacts.")
    parser.add_argument("--chunksize", type=int, default=1_000_000, help="CSV chunk size.")
    parser.add_argument("--start-date", default=None, help="Optional full-scan start date.")
    parser.add_argument("--end-date", default=None, help="Optional full-scan end date.")
    parser.add_argument(
        "--max-input-rows",
        type=int,
        default=None,
        help="Raw row cap for smoke tests only. Leave unset for the remote full map.",
    )
    parser.add_argument(
        "--sample-modulus",
        type=int,
        default=200,
        help="Keep every Nth raw row for approximate quantiles and prompt cards.",
    )
    parser.add_argument(
        "--max-sample-rows",
        type=int,
        default=300_000,
        help="Maximum deterministic sample rows retained in memory.",
    )
    parser.add_argument(
        "--deep-start-date",
        default=None,
        help="Date-window start for rolling top-N and cross-sectional deep profile.",
    )
    parser.add_argument(
        "--deep-end-date",
        default=None,
        help="Date-window end for rolling top-N and cross-sectional deep profile.",
    )
    parser.add_argument("--deep-top-n", type=int, default=500, help="Rolling top-N universe size.")
    return parser.parse_args()


def _validate_args(args: argparse.Namespace) -> None:
    if args.chunksize <= 0:
        raise ValueError("--chunksize must be positive")
    if args.max_input_rows is not None and args.max_input_rows <= 0:
        raise ValueError("--max-input-rows must be positive when provided")
    if args.sample_modulus < 0:
        raise ValueError("--sample-modulus must be nonnegative")
    if args.max_sample_rows <= 0:
        raise ValueError("--max-sample-rows must be positive")
    if args.deep_top_n <= 0:
        raise ValueError("--deep-top-n must be positive")


def main() -> int:
    _ensure_repo_import()
    from research.alphaevolve_lite.daily_stock_eda import profile_daily_stock_data

    args = parse_args()
    try:
        _validate_args(args)
        result = profile_daily_stock_data(
            csv_path=args.csv_path,
            out_dir=args.out_dir,
            chunksize=args.chunksize,
            start_date=args.start_date,
            end_date=args.end_date,
            max_input_rows=args.max_input_rows,
            sample_modulus=args.sample_modulus,
            max_sample_rows=args.max_sample_rows,
            deep_start_date=args.deep_start_date,
            deep_end_date=args.deep_end_date,
            deep_top_n=args.deep_top_n,
        )
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({"status": "ok", **result}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
