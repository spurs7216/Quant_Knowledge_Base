"""
Validate the Phase 3 candidate registry tables.

This script checks schema and lineage integrity only. It does not judge whether
a candidate is a good alpha.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import pandas as pd


REGISTRY_COLUMNS = [
    "candidate_id",
    "parent_id",
    "root_candidate_id",
    "candidate_name",
    "created",
    "artifact_type",
    "environment",
    "artifact_path",
    "code_path",
    "patch_path",
    "evaluator_result",
    "local_decision",
    "status",
    "score_summary",
    "evidence_path",
    "source_phase",
    "notes",
]

EVENT_COLUMNS = [
    "event_id",
    "event_date",
    "candidate_id",
    "event_type",
    "from_status",
    "to_status",
    "actor_role",
    "evidence_path",
    "summary",
]

ALLOWED_ARTIFACT_TYPES = {
    "strategy_rule",
    "factor_definition",
    "research_script",
    "constructor",
    "search_artifact",
    "implementation_translation",
    "evaluation_workflow",
}

ALLOWED_ENVIRONMENTS = {
    "remote_validation",
    "research_falsification",
    "implementation_translation_smoke",
    "implementation_execution",
    "prospective_paper",
    "manual_control_plane",
}

ALLOWED_DECISIONS = {"pending", "reject", "revise", "proceed", "paper-test", "record-only"}
ALLOWED_STATUSES = {"active", "rejected", "promoted", "paper-test", "superseded"}
CANDIDATE_ID_RE = re.compile(r"^CAND-\d{8}-\d{3}$")
EVENT_ID_RE = re.compile(r"^EVT-\d{8}-\d{3}$")


def require_columns(df: pd.DataFrame, required: list[str], label: str) -> None:
    columns = list(df.columns)
    if columns != required:
        missing = [col for col in required if col not in columns]
        extra = [col for col in columns if col not in required]
        wrong_order = not missing and not extra
        raise ValueError(
            f"{label} columns do not match schema; "
            f"missing={missing}, extra={extra}, wrong_order={wrong_order}"
        )


def require_unique(df: pd.DataFrame, column: str, label: str) -> None:
    duplicated = df.loc[df[column].duplicated(), column].tolist()
    if duplicated:
        raise ValueError(f"{label} has duplicate {column} values: {duplicated}")


def clean_cell(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()


def validate_allowed_values(df: pd.DataFrame) -> None:
    checks = [
        ("artifact_type", ALLOWED_ARTIFACT_TYPES),
        ("environment", ALLOWED_ENVIRONMENTS),
        ("local_decision", ALLOWED_DECISIONS),
        ("status", ALLOWED_STATUSES),
    ]
    for column, allowed in checks:
        values = {clean_cell(value) for value in df[column]}
        invalid = sorted(values - allowed)
        if invalid:
            raise ValueError(f"registry has invalid {column} values: {invalid}")


def validate_identifier_formats(registry: pd.DataFrame, events: pd.DataFrame) -> None:
    bad_candidates = [value for value in registry["candidate_id"].map(clean_cell) if not CANDIDATE_ID_RE.match(value)]
    bad_roots = [value for value in registry["root_candidate_id"].map(clean_cell) if not CANDIDATE_ID_RE.match(value)]
    bad_parents = [
        value
        for value in registry["parent_id"].map(clean_cell)
        if value and not CANDIDATE_ID_RE.match(value)
    ]
    bad_events = [value for value in events["event_id"].map(clean_cell) if not EVENT_ID_RE.match(value)]
    if bad_candidates:
        raise ValueError(f"registry has malformed candidate_id values: {bad_candidates}")
    if bad_roots:
        raise ValueError(f"registry has malformed root_candidate_id values: {bad_roots}")
    if bad_parents:
        raise ValueError(f"registry has malformed parent_id values: {bad_parents}")
    if bad_events:
        raise ValueError(f"event log has malformed event_id values: {bad_events}")


def validate_lineage(registry: pd.DataFrame) -> None:
    by_id = {row.candidate_id: row for row in registry.itertuples(index=False)}
    for row in registry.itertuples(index=False):
        candidate_id = clean_cell(row.candidate_id)
        parent_id = clean_cell(row.parent_id)
        root_id = clean_cell(row.root_candidate_id)
        if not parent_id:
            if root_id != candidate_id:
                raise ValueError(f"root candidate {candidate_id} must have itself as root_candidate_id")
            continue
        if parent_id not in by_id:
            raise ValueError(f"candidate {candidate_id} references missing parent_id {parent_id}")
        parent = by_id[parent_id]
        if clean_cell(parent.root_candidate_id) != root_id:
            raise ValueError(
                f"candidate {candidate_id} root_candidate_id {root_id} "
                f"does not match parent root {clean_cell(parent.root_candidate_id)}"
            )


def validate_event_log(registry: pd.DataFrame, events: pd.DataFrame) -> None:
    candidate_ids = set(registry["candidate_id"].map(clean_cell))
    event_candidate_ids = set(events["candidate_id"].map(clean_cell))
    unknown = sorted(event_candidate_ids - candidate_ids)
    if unknown:
        raise ValueError(f"event log references unknown candidate ids: {unknown}")
    missing = sorted(candidate_ids - event_candidate_ids)
    if missing:
        raise ValueError(f"candidates without event-log rows: {missing}")
    invalid_from = sorted(
        {
            value
            for value in events["from_status"].map(clean_cell)
            if value and value not in ALLOWED_STATUSES
        }
    )
    invalid_to = sorted(
        {
            value
            for value in events["to_status"].map(clean_cell)
            if value and value not in ALLOWED_STATUSES
        }
    )
    if invalid_from:
        raise ValueError(f"event log has invalid from_status values: {invalid_from}")
    if invalid_to:
        raise ValueError(f"event log has invalid to_status values: {invalid_to}")


def validate_registry_tables(registry: pd.DataFrame, events: pd.DataFrame) -> None:
    require_columns(registry, REGISTRY_COLUMNS, "registry")
    require_columns(events, EVENT_COLUMNS, "event log")
    require_unique(registry, "candidate_id", "registry")
    require_unique(events, "event_id", "event log")
    validate_identifier_formats(registry, events)
    validate_allowed_values(registry)
    validate_lineage(registry)
    validate_event_log(registry, events)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--registry",
        type=Path,
        default=Path("projects/quant_research_system/phase3_candidate_registry/candidate_registry.csv"),
    )
    parser.add_argument(
        "--events",
        type=Path,
        default=Path("projects/quant_research_system/phase3_candidate_registry/candidate_event_log.csv"),
    )
    args = parser.parse_args()

    registry = pd.read_csv(args.registry, keep_default_na=False)
    events = pd.read_csv(args.events, keep_default_na=False)

    validate_registry_tables(registry, events)

    print(f"validated_candidates: {len(registry)}")
    print(f"validated_events: {len(events)}")


if __name__ == "__main__":
    main()
