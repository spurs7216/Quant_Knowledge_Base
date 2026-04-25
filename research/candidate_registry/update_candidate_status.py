"""
Update an existing Phase 3 candidate from a status-update manifest.

The update path is intentionally narrow: it may change only evaluator/result
fields on an existing candidate row and must append one event-log row.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import pandas as pd

from register_candidate import DEFAULT_EVENTS, DEFAULT_REGISTRY, EVENT_ID_RE, parse_simple_yaml
from validate_candidate_registry import (
    ALLOWED_STATUSES,
    EVENT_COLUMNS,
    REGISTRY_COLUMNS,
    validate_registry_tables,
)


MUTABLE_FIELDS = [
    "evaluator_result",
    "local_decision",
    "status",
    "score_summary",
    "evidence_path",
    "notes",
]

ALLOWED_TRANSITIONS = {
    ("active", "active"),
    ("active", "rejected"),
    ("active", "promoted"),
    ("active", "paper-test"),
    ("active", "superseded"),
    ("promoted", "promoted"),
    ("promoted", "paper-test"),
    ("promoted", "superseded"),
    ("rejected", "active"),
    ("superseded", "active"),
}


def clean(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()


def read_csv(path: Path, columns: list[str]) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=columns)
    return pd.read_csv(path, keep_default_na=False)


def require_nonempty(data: dict[str, Any], keys: list[str]) -> None:
    missing = [key for key in keys if not str(data.get(key, "")).strip()]
    if missing:
        raise ValueError(f"status manifest is missing required values: {missing}")


def event_row_from_update_manifest(data: dict[str, Any], evidence_path: str) -> dict[str, str]:
    event = data.get("event", {})
    if not isinstance(event, dict):
        raise ValueError("status manifest event field must be a mapping")
    required = ["event_id", "event_date", "event_type", "from_status", "to_status", "actor_role", "summary"]
    missing = [key for key in required if not str(event.get(key, "")).strip()]
    if missing:
        raise ValueError(f"status manifest event is missing required values: {missing}")
    event_id = clean(event["event_id"])
    if not EVENT_ID_RE.match(event_id):
        raise ValueError(f"event_id must match EVT-YYYYMMDD-NNN: {event_id}")
    return {
        "event_id": event_id,
        "event_date": clean(event["event_date"]),
        "candidate_id": clean(data["candidate_id"]),
        "event_type": clean(event["event_type"]),
        "from_status": clean(event["from_status"]),
        "to_status": clean(event["to_status"]),
        "actor_role": clean(event["actor_role"]),
        "evidence_path": clean(event.get("evidence_path") or evidence_path),
        "summary": clean(event["summary"]),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--events", type=Path, default=DEFAULT_EVENTS)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    data = parse_simple_yaml(args.manifest)
    require_nonempty(
        data,
        [
            "candidate_id",
            "expected_current_status",
            "new_status",
            "evaluator_result",
            "local_decision",
            "score_summary",
            "evidence_path",
            "notes",
        ],
    )

    candidate_id = clean(data["candidate_id"])
    expected_current_status = clean(data["expected_current_status"])
    new_status = clean(data["new_status"])
    if expected_current_status not in ALLOWED_STATUSES:
        raise ValueError(f"expected_current_status is invalid: {expected_current_status}")
    if new_status not in ALLOWED_STATUSES:
        raise ValueError(f"new_status is invalid: {new_status}")
    if (expected_current_status, new_status) not in ALLOWED_TRANSITIONS:
        raise ValueError(f"status transition is not allowed: {expected_current_status} -> {new_status}")

    registry = read_csv(args.registry, REGISTRY_COLUMNS)
    events = read_csv(args.events, EVENT_COLUMNS)
    match = registry["candidate_id"].map(clean).eq(candidate_id)
    if not match.any():
        raise ValueError(f"candidate_id not found in registry: {candidate_id}")
    if int(match.sum()) != 1:
        raise ValueError(f"candidate_id matched multiple rows: {candidate_id}")

    row_index = registry.index[match][0]
    actual_status = clean(registry.at[row_index, "status"])
    if actual_status != expected_current_status:
        raise ValueError(
            f"candidate {candidate_id} status mismatch: "
            f"expected {expected_current_status}, found {actual_status}"
        )

    event_row = event_row_from_update_manifest(data, clean(data["evidence_path"]))
    if event_row["from_status"] != expected_current_status or event_row["to_status"] != new_status:
        raise ValueError("event from_status/to_status must match the requested status transition")

    next_registry = registry.copy()
    for field in MUTABLE_FIELDS:
        source_key = "new_status" if field == "status" else field
        next_registry.at[row_index, field] = clean(data[source_key])

    next_events = pd.concat([events, pd.DataFrame([event_row])], ignore_index=True)
    validate_registry_tables(next_registry, next_events)

    if args.dry_run:
        print(f"dry_run_candidate_id: {candidate_id}")
        print(f"dry_run_event_id: {event_row['event_id']}")
        print(f"dry_run_transition: {expected_current_status} -> {new_status}")
        return

    next_registry.to_csv(args.registry, index=False)
    next_events.to_csv(args.events, index=False)
    print(f"updated_candidate_id: {candidate_id}")
    print(f"appended_event_id: {event_row['event_id']}")
    print(f"transition: {expected_current_status} -> {new_status}")


if __name__ == "__main__":
    main()
