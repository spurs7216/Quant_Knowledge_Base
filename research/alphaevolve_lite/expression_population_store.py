"""SQLite persistence for expression-population episode artifacts."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any, Mapping, Sequence

from .artifact_io import clean_json
from .expression_eval_records import finite_or_none


SCHEMA_VERSION = "expression_population_sqlite_v1"


def write_expression_population_sqlite(
    db_path: str | Path,
    *,
    population_records: Sequence[Mapping[str, Any]],
    parent_selection_records: Sequence[Mapping[str, Any]],
    run_summary: Mapping[str, Any],
) -> Path:
    """Write a compact SQLite mirror of expression population state."""

    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as conn:
        _create_schema(conn)
        run_id = str(run_summary.get("run_id") or "")
        conn.execute(
            """
            INSERT OR REPLACE INTO expression_population_runs
            (run_id, schema_version, status, summary_json)
            VALUES (?, ?, ?, ?)
            """,
            (
                run_id,
                SCHEMA_VERSION,
                str(run_summary.get("status") or ""),
                _json(run_summary),
            ),
        )
        conn.execute("DELETE FROM expression_population_records WHERE run_id = ?", (run_id,))
        conn.execute("DELETE FROM expression_parent_selection_records WHERE run_id = ?", (run_id,))
        conn.executemany(
            """
            INSERT INTO expression_population_records
            (
                run_id, expression_id, root_expression_id, parent_expression_id,
                record_type, generation, turn, status, selection_score,
                root_turnover_aware_delta, parent_sampling_eligible,
                map_cell_key, historical, source_path, record_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [_population_row(record, run_id) for record in population_records],
        )
        conn.executemany(
            """
            INSERT INTO expression_parent_selection_records
            (
                run_id, root_expression_id, turn, selected_expression_id,
                parent_sampling_mode, selection_reason, eligible_parent_count,
                record_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [_parent_selection_row(record, run_id) for record in parent_selection_records],
        )
    return path


def _create_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS expression_population_runs (
            run_id TEXT PRIMARY KEY,
            schema_version TEXT NOT NULL,
            status TEXT NOT NULL,
            summary_json TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS expression_population_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id TEXT NOT NULL,
            expression_id TEXT,
            root_expression_id TEXT,
            parent_expression_id TEXT,
            record_type TEXT,
            generation INTEGER,
            turn INTEGER,
            status TEXT,
            selection_score REAL,
            root_turnover_aware_delta REAL,
            parent_sampling_eligible INTEGER NOT NULL,
            map_cell_key TEXT,
            historical INTEGER NOT NULL,
            source_path TEXT,
            record_json TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_expr_population_root
            ON expression_population_records(root_expression_id, record_type, status);
        CREATE INDEX IF NOT EXISTS idx_expr_population_parent_sampling
            ON expression_population_records(parent_sampling_eligible, selection_score);
        CREATE INDEX IF NOT EXISTS idx_expr_population_map_cell
            ON expression_population_records(map_cell_key);

        CREATE TABLE IF NOT EXISTS expression_parent_selection_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id TEXT NOT NULL,
            root_expression_id TEXT,
            turn INTEGER,
            selected_expression_id TEXT,
            parent_sampling_mode TEXT,
            selection_reason TEXT,
            eligible_parent_count INTEGER,
            record_json TEXT NOT NULL
        );
        """
    )


def _population_row(record: Mapping[str, Any], fallback_run_id: str) -> tuple[Any, ...]:
    return (
        fallback_run_id,
        _text_or_none(record.get("expression_id")),
        _text_or_none(record.get("root_expression_id")),
        _text_or_none(record.get("parent_expression_id")),
        _text_or_none(record.get("record_type")),
        _int_or_none(record.get("generation")),
        _int_or_none(record.get("turn")),
        _text_or_none(record.get("status")),
        finite_or_none(record.get("selection_score")),
        finite_or_none(record.get("root_turnover_aware_delta")),
        int(bool(record.get("parent_sampling_eligible"))),
        _text_or_none(record.get("map_cell_key")),
        int(bool(record.get("historical"))),
        _text_or_none(record.get("source_path")),
        _json(record),
    )


def _parent_selection_row(record: Mapping[str, Any], fallback_run_id: str) -> tuple[Any, ...]:
    return (
        str(record.get("run_id") or fallback_run_id),
        _text_or_none(record.get("root_expression_id")),
        _int_or_none(record.get("turn")),
        _text_or_none(record.get("selected_expression_id")),
        _text_or_none(record.get("parent_sampling_mode")),
        _text_or_none(record.get("selection_reason")),
        _int_or_none(record.get("eligible_parent_count")),
        _json(record),
    )


def _json(payload: Mapping[str, Any]) -> str:
    return json.dumps(clean_json(dict(payload)), sort_keys=True)


def _text_or_none(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value)
    return text if text else None


def _int_or_none(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


__all__ = ["SCHEMA_VERSION", "write_expression_population_sqlite"]
