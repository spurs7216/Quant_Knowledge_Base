"""
Register a Phase 3 candidate from a simple YAML manifest.

The parser intentionally supports only the manifest subset used by this vault:
top-level scalar keys and one-level nested scalar maps. That keeps the
registration path dependency-free and inspectable.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

import pandas as pd

from validate_candidate_registry import (
    EVENT_COLUMNS,
    REGISTRY_COLUMNS,
    validate_registry_tables,
)


DEFAULT_REGISTRY = Path("projects/quant_research_system/phase3_candidate_registry/candidate_registry.csv")
DEFAULT_EVENTS = Path("projects/quant_research_system/phase3_candidate_registry/candidate_event_log.csv")
CANDIDATE_ID_RE = re.compile(r"^CAND-\d{8}-\d{3}$")
EVENT_ID_RE = re.compile(r"^EVT-\d{8}-\d{3}$")


def parse_scalar(raw: str) -> str:
    value = raw.strip()
    if not value:
        return ""
    if value.startswith("#"):
        return ""
    if "#" in value and not (value.startswith('"') or value.startswith("'")):
        value = value.split("#", 1)[0].strip()
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]
    return value.strip()


def parse_simple_yaml(path: Path) -> dict[str, Any]:
    data: dict[str, Any] = {}
    section: str | None = None
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()
        if ":" not in line:
            raise ValueError(f"unsupported manifest line without key-value separator: {raw_line}")
        key, raw_value = line.split(":", 1)
        key = key.strip()
        raw_value_stripped = raw_value.strip()
        value = parse_scalar(raw_value)
        if indent == 0:
            if raw_value_stripped == "":
                section = key
                data.setdefault(section, {})
            else:
                section = None
                data[key] = value
        elif indent == 2 and section:
            if not isinstance(data.get(section), dict):
                raise ValueError(f"manifest section {section} is not a mapping")
            data[section][key] = value
        else:
            raise ValueError(f"unsupported indentation in manifest line: {raw_line}")
    return data


def require_nonempty(data: dict[str, Any], keys: list[str]) -> None:
    missing = [key for key in keys if not str(data.get(key, "")).strip()]
    if missing:
        raise ValueError(f"manifest is missing required values: {missing}")


def candidate_row_from_manifest(data: dict[str, Any]) -> dict[str, str]:
    require_nonempty(
        data,
        [
            "candidate_id",
            "root_candidate_id",
            "candidate_name",
            "created",
            "artifact_type",
            "environment",
            "artifact_path",
            "evaluator_result",
            "local_decision",
            "status",
            "score_summary",
            "evidence_path",
            "source_phase",
            "notes",
        ],
    )
    candidate_id = str(data["candidate_id"]).strip()
    if not CANDIDATE_ID_RE.match(candidate_id):
        raise ValueError(f"candidate_id must match CAND-YYYYMMDD-NNN: {candidate_id}")
    row = {column: str(data.get(column, "")).strip() for column in REGISTRY_COLUMNS}
    return row


def event_row_from_manifest(data: dict[str, Any], candidate_row: dict[str, str]) -> dict[str, str]:
    event = data.get("event", {})
    if not isinstance(event, dict):
        raise ValueError("manifest event field must be a mapping")
    required = ["event_id", "event_type", "actor_role", "summary"]
    missing = [key for key in required if not str(event.get(key, "")).strip()]
    if missing:
        raise ValueError(f"manifest event is missing required values: {missing}")
    event_id = str(event["event_id"]).strip()
    if not EVENT_ID_RE.match(event_id):
        raise ValueError(f"event_id must match EVT-YYYYMMDD-NNN: {event_id}")
    return {
        "event_id": event_id,
        "event_date": str(event.get("event_date") or candidate_row["created"]).strip(),
        "candidate_id": candidate_row["candidate_id"],
        "event_type": str(event["event_type"]).strip(),
        "from_status": str(event.get("from_status", "")).strip(),
        "to_status": str(event.get("to_status") or candidate_row["status"]).strip(),
        "actor_role": str(event["actor_role"]).strip(),
        "evidence_path": str(event.get("evidence_path") or candidate_row["evidence_path"]).strip(),
        "summary": str(event["summary"]).strip(),
    }


def read_csv(path: Path, columns: list[str]) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=columns)
    return pd.read_csv(path, keep_default_na=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--events", type=Path, default=DEFAULT_EVENTS)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    data = parse_simple_yaml(args.manifest)
    candidate_row = candidate_row_from_manifest(data)
    event_row = event_row_from_manifest(data, candidate_row)

    registry = read_csv(args.registry, REGISTRY_COLUMNS)
    events = read_csv(args.events, EVENT_COLUMNS)
    next_registry = pd.concat([registry, pd.DataFrame([candidate_row])], ignore_index=True)
    next_events = pd.concat([events, pd.DataFrame([event_row])], ignore_index=True)

    validate_registry_tables(next_registry, next_events)

    if args.dry_run:
        print(f"dry_run_candidate_id: {candidate_row['candidate_id']}")
        print(f"dry_run_event_id: {event_row['event_id']}")
        return

    args.registry.parent.mkdir(parents=True, exist_ok=True)
    args.events.parent.mkdir(parents=True, exist_ok=True)
    next_registry.to_csv(args.registry, index=False)
    next_events.to_csv(args.events, index=False)
    print(f"registered_candidate_id: {candidate_row['candidate_id']}")
    print(f"registered_event_id: {event_row['event_id']}")


if __name__ == "__main__":
    main()
