"""
Phase 3 Task 004: duplicate-policy revision for daily-stock reversal.

Run on the remote Ubuntu machine that has the full WRDS mirror.

Example:
    python research/remote_validation/task004_duplicate_policy_reversal.py \
        --data-root /home/b08303004/Desktop/WRDS/data \
        --output-dir artifacts/remote_runs/20260425_cand_20260425_002_duplicate_policy_reversal

This candidate keeps the Phase 1 signal and portfolio construction fixed.
The only intended research-code change is deterministic duplicate resolution at
the raw PERMNO x DlyCalDt grain before universe filtering and signal formation.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from research.remote_validation import task001_daily_stock_short_reversal as base


JOB_ID = "20260425_cand_20260425_002_duplicate_policy_reversal"
CANDIDATE_ID = "CAND-20260425-002"
PARENT_CANDIDATE_ID = "CAND-20260425-001"
ROOT_CANDIDATE_ID = "CAND-20260423-001"
DUPLICATE_POLICY = (
    "resolve_raw_permno_date_duplicates_by_quality_then_dollar_volume_before_filters"
)
POLICY_REQUIRED_FIELDS = [
    "DlyRet",
    "DlyRetx",
    "DlyPrc",
    "DlyVol",
    "vwretd",
    "sprtrn",
    "PrimaryExch",
    "SecurityType",
    "ShareType",
    "TradingStatusFlg",
]
ORIGINAL_PREPARE_PANEL = base.prepare_panel
ORIGINAL_WRITE_MANIFEST = base.write_manifest
ORIGINAL_MAKE_FAILURE_REPORT = base.make_failure_report


def duplicate_policy_metadata() -> dict[str, Any]:
    return {
        "candidate_id": CANDIDATE_ID,
        "parent_candidate_id": PARENT_CANDIDATE_ID,
        "root_candidate_id": ROOT_CANDIDATE_ID,
        "duplicate_policy": DUPLICATE_POLICY,
        "policy_required_fields": POLICY_REQUIRED_FIELDS,
        "tie_breakers": [
            "highest nonmissing count across policy_required_fields",
            "highest absolute price times volume",
            "lowest original row order",
        ],
        "signal_change": "none",
        "portfolio_change": "none",
    }


def resolve_raw_permno_date_duplicates(df: pd.DataFrame) -> tuple[pd.DataFrame, list[dict[str, Any]]]:
    diagnostics: list[dict[str, Any]] = []
    key = ["PERMNO", "DlyCalDt"]
    duplicate_mask = df.duplicated(key, keep=False)
    duplicate_rows = int(duplicate_mask.sum())
    diagnostics.append(
        {
            "check": "raw_duplicate_permno_date_rows_before_policy",
            "status": "info",
            "value": duplicate_rows,
            "threshold": "",
            "notes": "Rows belonging to duplicate PERMNO-date groups before deterministic policy resolution.",
        }
    )
    if duplicate_rows == 0:
        diagnostics.extend(
            [
                {
                    "check": "raw_duplicate_permno_date_groups_before_policy",
                    "status": "info",
                    "value": 0,
                    "threshold": "",
                    "notes": "",
                },
                {
                    "check": "duplicate_policy_rows_removed",
                    "status": "pass",
                    "value": 0,
                    "threshold": "",
                    "notes": "No duplicate rows existed at the raw PERMNO-date grain.",
                },
                {
                    "check": "duplicate_policy_applied",
                    "status": "pass",
                    "value": DUPLICATE_POLICY,
                    "threshold": "deterministic raw-grain policy",
                    "notes": "No-op because no raw duplicates existed.",
                },
            ]
        )
        return df.copy(), diagnostics

    duplicate_part = df.loc[duplicate_mask].copy()
    duplicate_groups = int(duplicate_part.groupby(key, sort=False).ngroups)
    duplicate_part["_original_order"] = duplicate_part.index.to_numpy()
    duplicate_part["_policy_quality_score"] = duplicate_part[POLICY_REQUIRED_FIELDS].notna().sum(axis=1)
    duplicate_part["_policy_dollar_volume"] = (
        pd.to_numeric(duplicate_part["DlyPrc"], errors="coerce").abs()
        * pd.to_numeric(duplicate_part["DlyVol"], errors="coerce")
    ).replace([np.inf, -np.inf], np.nan).fillna(-1.0)
    duplicate_part.sort_values(
        key + ["_policy_quality_score", "_policy_dollar_volume", "_original_order"],
        ascending=[True, True, False, False, True],
        inplace=True,
    )
    chosen = duplicate_part.drop_duplicates(key, keep="first").drop(
        columns=["_original_order", "_policy_quality_score", "_policy_dollar_volume"]
    )
    deduped = pd.concat([df.loc[~duplicate_mask], chosen], axis=0).sort_index(kind="stable")
    rows_removed = int(len(df) - len(deduped))
    remaining_duplicates = int(deduped.duplicated(key).sum())
    diagnostics.extend(
        [
            {
                "check": "raw_duplicate_permno_date_groups_before_policy",
                "status": "info",
                "value": duplicate_groups,
                "threshold": "",
                "notes": "",
            },
            {
                "check": "duplicate_policy_rows_removed",
                "status": "pass" if rows_removed == duplicate_rows - duplicate_groups else "fail",
                "value": rows_removed,
                "threshold": duplicate_rows - duplicate_groups,
                "notes": "Exactly one row should remain from each duplicate PERMNO-date group.",
            },
            {
                "check": "duplicate_policy_remaining_raw_duplicates",
                "status": "pass" if remaining_duplicates == 0 else "fail",
                "value": remaining_duplicates,
                "threshold": 0,
                "notes": "Raw PERMNO-date duplicates must be removed before universe filters.",
            },
            {
                "check": "duplicate_policy_applied",
                "status": "pass",
                "value": DUPLICATE_POLICY,
                "threshold": "deterministic raw-grain policy",
                "notes": "Policy ranks rows by nonmissing field count, dollar volume, then original row order.",
            },
        ]
    )
    return deduped, diagnostics


def prepare_panel(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    deduped, duplicate_diagnostics = resolve_raw_permno_date_duplicates(df)
    panel, diagnostics = ORIGINAL_PREPARE_PANEL(deduped)
    diagnostics = pd.concat([pd.DataFrame(duplicate_diagnostics), diagnostics], ignore_index=True)

    after_filter_mask = diagnostics["check"].eq("duplicate_permno_date_after_universe_filters")
    if after_filter_mask.any():
        diagnostics.loc[after_filter_mask, "notes"] = (
            "Duplicates are expected to be zero because raw PERMNO-date duplicate resolution "
            "runs before universe filters."
        )
    return panel, diagnostics


def write_manifest(path: Path, args: Any, row_count: int) -> None:
    ORIGINAL_WRITE_MANIFEST(path, args, row_count)
    manifest = json.loads(path.read_text(encoding="utf-8"))
    manifest.update(duplicate_policy_metadata())
    manifest["candidate_artifact"] = {
        "type": "strategy_script",
        "candidate_id": CANDIDATE_ID,
        "parent_candidate_id": PARENT_CANDIDATE_ID,
        "root_candidate_id": ROOT_CANDIDATE_ID,
        "source_files": ["research/remote_validation/task004_duplicate_policy_reversal.py"],
        "changed_surface": "raw PERMNO-date duplicate resolution only",
    }
    manifest["duplicate_policy"] = duplicate_policy_metadata()
    manifest["expected_outputs"].append("duplicate_policy_diagnostics_in_diagnostics_csv")
    path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def make_failure_report(path: Path, diagnostics: pd.DataFrame, metrics: dict[str, Any]) -> None:
    ORIGINAL_MAKE_FAILURE_REPORT(path, diagnostics, metrics)
    with path.open("a", encoding="utf-8") as handle:
        handle.write("\n## Candidate Lineage\n\n")
        handle.write(f"- candidate_id: `{CANDIDATE_ID}`\n")
        handle.write(f"- parent_candidate_id: `{PARENT_CANDIDATE_ID}`\n")
        handle.write(f"- root_candidate_id: `{ROOT_CANDIDATE_ID}`\n")
        handle.write(f"- duplicate_policy: `{DUPLICATE_POLICY}`\n")


def main() -> None:
    base.JOB_ID = JOB_ID
    base.prepare_panel = prepare_panel
    base.write_manifest = write_manifest
    base.make_failure_report = make_failure_report
    base.main()


if __name__ == "__main__":
    main()
