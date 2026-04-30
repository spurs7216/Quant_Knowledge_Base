"""Register the generation-zero Kalman reversal seed in SQLite."""

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
    parser = argparse.ArgumentParser(description="Register the Phase 4 generation-zero seed program.")
    parser.add_argument("--db-path", required=True)
    parser.add_argument(
        "--program-path",
        default="research/alphaevolve_lite/seeds/kalman_reversal_seed.py",
    )
    parser.add_argument("--program-id", default="PROG-20260430-000000")
    parser.add_argument("--root-id", default="CAND-20260423-001")
    parser.add_argument("--branch-id", default="BRANCH-CAND-20260423-001-001")
    return parser.parse_args()


def main() -> int:
    _ensure_repo_import()
    from research.alphaevolve_lite.program_database import init_db, insert_program_record

    args = parse_args()
    program_path = Path(args.program_path)
    if not program_path.exists():
        print(f"ERROR: seed program path does not exist: {program_path}", file=sys.stderr)
        return 1

    record = {
        "program_id": args.program_id,
        "parent_id": None,
        "root_id": args.root_id,
        "branch_id": args.branch_id,
        "generation": 0,
        "island": "daily_stock_signal",
        "mutation_surface": "seed",
        "data_scope": "daily_stock_only",
        "status": "seed",
        "program_path": str(program_path),
        "diff_path": None,
        "prompt_path": None,
        "evaluator_summary_path": None,
        "metrics": {},
        "descriptors": {
            "model_role": "human_seed",
            "strategy_family": "kalman_innovation_reversal",
            "daily_stock_contract": "daily_stock_contract_v1",
        },
        "hard_gates": {
            "seed_program_exists": True,
            "child_generation_started": False,
        },
        "validation_exposure": {
            "controller_static": False,
            "remote_sample_eval": False,
            "remote_full_validation": False,
            "test_set_used": False,
        },
        "failure_reason": None,
    }
    init_db(args.db_path)
    insert_program_record(args.db_path, record)
    print(json.dumps({"status": "ok", "program_id": args.program_id}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
