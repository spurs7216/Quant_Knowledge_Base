"""SQLite program database for Phase 4 AlphaEvolve-lite."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .paths import utc_now_iso


SCHEMA_STATEMENTS = [
    """
    CREATE TABLE IF NOT EXISTS program_records (
        program_id TEXT PRIMARY KEY,
        parent_id TEXT,
        root_id TEXT,
        branch_id TEXT,
        generation INTEGER NOT NULL,
        island TEXT,
        mutation_surface TEXT,
        data_scope TEXT,
        status TEXT NOT NULL,
        program_path TEXT,
        diff_path TEXT,
        prompt_path TEXT,
        evaluator_summary_path TEXT,
        metrics_json TEXT NOT NULL,
        descriptors_json TEXT NOT NULL,
        hard_gates_json TEXT NOT NULL,
        validation_exposure_json TEXT NOT NULL,
        failure_reason TEXT,
        created_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS model_test_records (
        test_id TEXT PRIMARY KEY,
        model_role TEXT NOT NULL,
        model_id TEXT NOT NULL,
        served_model_name TEXT,
        port INTEGER,
        max_model_len INTEGER,
        gpu_config_json TEXT NOT NULL,
        command_summary TEXT,
        result_log_path TEXT,
        parsed_metrics_json TEXT NOT NULL,
        decision TEXT,
        created_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS controller_runs (
        run_id TEXT PRIMARY KEY,
        stage TEXT NOT NULL,
        config_path TEXT NOT NULL,
        artifact_root TEXT NOT NULL,
        git_commit TEXT,
        status TEXT NOT NULL,
        started_at TEXT NOT NULL,
        finished_at TEXT,
        error_message TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS artifact_index (
        artifact_id TEXT PRIMARY KEY,
        run_id TEXT,
        program_id TEXT,
        artifact_type TEXT NOT NULL,
        path TEXT NOT NULL,
        sha256 TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """,
]


def json_dumps(payload: Any) -> str:
    """Serialize JSON fields deterministically."""

    return json.dumps(payload if payload is not None else {}, sort_keys=True, ensure_ascii=False)


def connect(db_path: str | Path) -> sqlite3.Connection:
    """Open a SQLite connection with row dictionaries enabled."""

    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str | Path) -> None:
    """Create required SQLite tables if they do not exist."""

    with connect(db_path) as conn:
        for statement in SCHEMA_STATEMENTS:
            conn.execute(statement)
        conn.commit()


def insert_program_record(db_path: str | Path, record: dict[str, Any]) -> None:
    """Insert or replace one program record."""

    created_at = record.get("created_at") or utc_now_iso()
    payload = {
        "program_id": record["program_id"],
        "parent_id": record.get("parent_id"),
        "root_id": record.get("root_id"),
        "branch_id": record.get("branch_id"),
        "generation": int(record.get("generation", 0)),
        "island": record.get("island"),
        "mutation_surface": record.get("mutation_surface"),
        "data_scope": record.get("data_scope"),
        "status": record.get("status", "recorded"),
        "program_path": record.get("program_path"),
        "diff_path": record.get("diff_path"),
        "prompt_path": record.get("prompt_path"),
        "evaluator_summary_path": record.get("evaluator_summary_path"),
        "metrics_json": json_dumps(record.get("metrics")),
        "descriptors_json": json_dumps(record.get("descriptors")),
        "hard_gates_json": json_dumps(record.get("hard_gates")),
        "validation_exposure_json": json_dumps(record.get("validation_exposure")),
        "failure_reason": record.get("failure_reason"),
        "created_at": created_at,
    }
    columns = ", ".join(payload)
    placeholders = ", ".join(f":{key}" for key in payload)
    with connect(db_path) as conn:
        conn.execute(
            f"INSERT OR REPLACE INTO program_records ({columns}) VALUES ({placeholders})",
            payload,
        )
        conn.commit()


def insert_model_test_record(db_path: str | Path, record: dict[str, Any]) -> None:
    """Insert or replace one model-test evidence record."""

    payload = {
        "test_id": record["test_id"],
        "model_role": record["model_role"],
        "model_id": record["model_id"],
        "served_model_name": record.get("served_model_name"),
        "port": record.get("port"),
        "max_model_len": record.get("max_model_len"),
        "gpu_config_json": json_dumps(record.get("gpu_config")),
        "command_summary": record.get("command_summary"),
        "result_log_path": record.get("result_log_path"),
        "parsed_metrics_json": json_dumps(record.get("parsed_metrics")),
        "decision": record.get("decision"),
        "created_at": record.get("created_at") or utc_now_iso(),
    }
    columns = ", ".join(payload)
    placeholders = ", ".join(f":{key}" for key in payload)
    with connect(db_path) as conn:
        conn.execute(
            f"INSERT OR REPLACE INTO model_test_records ({columns}) VALUES ({placeholders})",
            payload,
        )
        conn.commit()


def insert_controller_run(db_path: str | Path, record: dict[str, Any]) -> None:
    """Insert or replace a controller run record."""

    payload = {
        "run_id": record["run_id"],
        "stage": record["stage"],
        "config_path": str(record["config_path"]),
        "artifact_root": str(record["artifact_root"]),
        "git_commit": record.get("git_commit"),
        "status": record.get("status", "started"),
        "started_at": record.get("started_at") or utc_now_iso(),
        "finished_at": record.get("finished_at"),
        "error_message": record.get("error_message"),
    }
    columns = ", ".join(payload)
    placeholders = ", ".join(f":{key}" for key in payload)
    with connect(db_path) as conn:
        conn.execute(
            f"INSERT OR REPLACE INTO controller_runs ({columns}) VALUES ({placeholders})",
            payload,
        )
        conn.commit()


def finish_controller_run(
    db_path: str | Path,
    run_id: str,
    status: str,
    error_message: str | None = None,
) -> None:
    """Mark a controller run finished."""

    with connect(db_path) as conn:
        conn.execute(
            """
            UPDATE controller_runs
            SET status = ?, finished_at = ?, error_message = ?
            WHERE run_id = ?
            """,
            (status, utc_now_iso(), error_message, run_id),
        )
        conn.commit()


def insert_artifact_record(db_path: str | Path, record: dict[str, Any]) -> None:
    """Insert one artifact index row."""

    payload = {
        "artifact_id": record["artifact_id"],
        "run_id": record.get("run_id"),
        "program_id": record.get("program_id"),
        "artifact_type": record["artifact_type"],
        "path": str(record["path"]),
        "sha256": record["sha256"],
        "created_at": record.get("created_at") or utc_now_iso(),
    }
    columns = ", ".join(payload)
    placeholders = ", ".join(f":{key}" for key in payload)
    with connect(db_path) as conn:
        conn.execute(
            f"INSERT OR REPLACE INTO artifact_index ({columns}) VALUES ({placeholders})",
            payload,
        )
        conn.commit()


def list_tables(db_path: str | Path) -> list[str]:
    """Return SQLite table names, primarily for smoke checks."""

    with connect(db_path) as conn:
        rows = conn.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name"
        ).fetchall()
    return [str(row["name"]) for row in rows]


# Legacy JSONL helpers kept for earlier local smoke snippets.
@dataclass(frozen=True)
class ProgramRecord:
    """A small scored program record used by the initial smoke scaffold."""

    program_id: str
    parent_id: str | None
    generation: int
    program_text: str
    metrics: dict[str, float]
    descriptors: dict[str, str] = field(default_factory=dict)
    diff_text: str | None = None
    status: str = "evaluated"
    notes: str = ""
    created_at: str = field(default_factory=utc_now_iso)

    def to_json(self) -> str:
        return json.dumps(asdict(self), sort_keys=True, ensure_ascii=False)


def append_record(database_path: Path, record: ProgramRecord) -> None:
    """Append a legacy JSONL smoke-test record."""

    database_path.parent.mkdir(parents=True, exist_ok=True)
    with database_path.open("a", encoding="utf-8") as handle:
        handle.write(record.to_json() + "\n")


def load_records(database_path: Path) -> list[ProgramRecord]:
    """Load legacy JSONL smoke-test records."""

    if not database_path.exists():
        return []
    records: list[ProgramRecord] = []
    with database_path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            payload = json.loads(line)
            try:
                records.append(ProgramRecord(**payload))
            except TypeError as exc:
                raise ValueError(f"invalid program database row {line_number}: {exc}") from exc
    return records


def sample_records(
    records: list[ProgramRecord],
    primary_metric: str,
    limit: int = 4,
) -> list[ProgramRecord]:
    """Sample high-scoring and descriptor-diverse legacy records."""

    if limit <= 0 or not records:
        return []

    scored = [r for r in records if primary_metric in r.metrics]
    scored.sort(key=lambda r: r.metrics[primary_metric], reverse=True)
    selected: list[ProgramRecord] = []
    seen_descriptor_keys: set[tuple[tuple[str, str], ...]] = set()

    for record in scored:
        descriptor_key = tuple(sorted(record.descriptors.items()))
        if descriptor_key in seen_descriptor_keys and len(selected) >= max(1, limit // 2):
            continue
        selected.append(record)
        seen_descriptor_keys.add(descriptor_key)
        if len(selected) >= limit:
            break

    if len(selected) < limit:
        selected_ids = {r.program_id for r in selected}
        for record in scored:
            if record.program_id not in selected_ids:
                selected.append(record)
                if len(selected) >= limit:
                    break

    return selected
