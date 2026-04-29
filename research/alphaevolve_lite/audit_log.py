"""Append-only JSONL audit log for AlphaEvolve-lite controller events."""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any

from .paths import ensure_dir, utc_now_iso


SUPPORTED_EVENT_TYPES = frozenset(
    {
        "controller_started",
        "controller_finished",
        "config_loaded",
        "database_initialized",
        "artifact_written",
        "schema_inspection_recorded",
        "model_test_recorded",
        "error",
    }
)


class AuditLogError(ValueError):
    """Raised when an audit event is invalid."""


def append_audit_event(
    audit_log_path: str | Path,
    event_type: str,
    run_id: str | None,
    payload: dict[str, Any] | None = None,
    event_id: str | None = None,
) -> dict[str, Any]:
    """Append an event to the JSONL audit log and return the event."""

    if event_type not in SUPPORTED_EVENT_TYPES:
        raise AuditLogError(f"unsupported audit event type: {event_type}")

    event = {
        "event_id": event_id or f"EVT-{uuid.uuid4().hex[:16]}",
        "timestamp": utc_now_iso(),
        "event_type": event_type,
        "run_id": run_id,
        "payload": payload or {},
    }
    path = Path(audit_log_path)
    ensure_dir(path.parent)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, sort_keys=True, ensure_ascii=False) + "\n")
    return event
