"""Reasoning memory utilities for Phase 4 AlphaEvolve-lite.

This module is deliberately lightweight. It provides the local scaffold for a
ReasoningBank-style memory layer without requiring local LLM or embedding
inference.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Iterable

from .paths import utc_now_iso


MEMORY_SCHEMA_VERSION = "phase4_reasoning_memory_item_v1"
MEMORY_UPDATE_SCHEMA_VERSION = "phase4_reasoning_memory_update_v1"

ACTIVE_STATUSES = {"active"}
VALID_STATUSES = {"candidate", "active", "superseded", "rejected"}
VALID_MEMORY_TYPES = {
    "success_strategy",
    "failure_guardrail",
    "repair_pattern",
    "evaluator_caveat",
    "data_contract",
    "model_routing",
}

DEFAULT_MEMORY_ITEMS: list[dict[str, Any]] = [
    {
        "source_run_id": "phase4_current_state_20260504",
        "source_stage": "controller_static",
        "source_outcome": "failure",
        "memory_type": "failure_guardrail",
        "title": "Expose one editable evolve-block body",
        "description": "Use for controller-static child generation on any target surface.",
        "content": (
            "Full-program prompts invite marker copying and helper edits. Give the model only one "
            "target evolve-block body, and require SEARCH text to come from that body only."
        ),
        "applicability": {
            "data_stage": "stage_0_daily_stock",
            "target_surface": "any",
            "island": "any",
        },
        "evidence": {
            "artifact_paths": [
                "projects/quant_research_system/phase4_search_loop/current_state.md",
                "projects/quant_research_system/phase4_search_loop/controller_batch_001_small_review_20260430.md",
            ],
            "failure_categories": ["outside_evolve_block", "evolve_marker_error", "exact_search_not_found"],
        },
        "status": "active",
        "created_at": "2026-05-04T00:00:00+00:00",
    },
    {
        "source_run_id": "phase4_current_state_20260504",
        "source_stage": "controller_static",
        "source_outcome": "failure",
        "memory_type": "failure_guardrail",
        "title": "Portfolio smoke must check long and short books",
        "description": "Use for portfolio and risk evolve surfaces.",
        "content": (
            "Compile and vector smoke are not enough for long/short strategies. Preserve both positive "
            "and negative weights, keep short weights negative, keep long weights positive, and keep "
            "net exposure near zero."
        ),
        "applicability": {
            "data_stage": "stage_0_daily_stock",
            "target_surface": ["portfolio", "risk"],
            "island": ["portfolio_risk_turnover", "repair_near_miss"],
        },
        "evidence": {
            "artifact_paths": [
                "projects/quant_research_system/phase4_search_loop/current_state.md",
                "projects/quant_research_system/phase4_search_loop/controller_batch_001_small_repair_v1_review_20260430.md",
            ],
            "failure_categories": ["portfolio_semantic_failed"],
        },
        "status": "active",
        "created_at": "2026-05-04T00:00:00+00:00",
    },
    {
        "source_run_id": "phase4_current_state_20260504",
        "source_stage": "controller_static",
        "source_outcome": "failure",
        "memory_type": "failure_guardrail",
        "title": "Use positive side magnitudes before signed weights",
        "description": "Use when signal-proportional portfolio weights are proposed.",
        "content": (
            "When weighting by signal strength, compute positive magnitudes separately for longs and "
            "shorts, normalize each side, then assign negative weights to shorts. Do not multiply a "
            "negative short-side signal by a negative sign and accidentally remove short exposure."
        ),
        "applicability": {
            "data_stage": "stage_0_daily_stock",
            "target_surface": ["portfolio", "risk"],
            "island": ["portfolio_risk_turnover", "repair_near_miss"],
        },
        "evidence": {
            "artifact_paths": [
                "projects/quant_research_system/phase4_search_loop/current_state.md",
                "projects/quant_research_system/phase4_search_loop/controller_batch_001_small_semantic_v2_review_20260501.md",
            ],
            "failure_categories": ["portfolio_semantic_failed"],
        },
        "status": "active",
        "created_at": "2026-05-04T00:00:00+00:00",
    },
    {
        "source_run_id": "phase4_current_state_20260504",
        "source_stage": "controller_static",
        "source_outcome": "failure",
        "memory_type": "model_routing",
        "title": "Treat Qwen reasoning-only output as empty content",
        "description": "Use for remote Qwen child generation and repair calls.",
        "content": (
            "Qwen can spend the completion budget in reasoning while returning null final content. "
            "Disable thinking mode in the HTTP payload, require the patch in message.content, and retry "
            "empty final content once."
        ),
        "applicability": {
            "data_stage": "stage_0_daily_stock",
            "target_surface": "any",
            "island": "any",
        },
        "evidence": {
            "artifact_paths": [
                "projects/quant_research_system/phase4_search_loop/current_state.md",
                "projects/quant_research_system/phase4_search_loop/controller_batch_001_small_semantic_v3_review_20260501.md",
            ],
            "failure_categories": ["empty_output"],
        },
        "status": "active",
        "created_at": "2026-05-04T00:00:00+00:00",
    },
    {
        "source_run_id": "phase4_current_state_20260504",
        "source_stage": "controller_static",
        "source_outcome": "failure",
        "memory_type": "failure_guardrail",
        "title": "Duplicates are evidence but not unique passes",
        "description": "Use when a child passes controller gates but repeats a prior child or patch intent.",
        "content": (
            "Store duplicate children and duplicate patch fingerprints as evidence, but do not count them "
            "as unique controller passes. On retry, ask for a different behavior cell and forbid the "
            "duplicate patch text."
        ),
        "applicability": {
            "data_stage": "stage_0_daily_stock",
            "target_surface": "any",
            "island": "any",
        },
        "evidence": {
            "artifact_paths": [
                "projects/quant_research_system/phase4_search_loop/current_state.md",
                "projects/quant_research_system/phase4_search_loop/controller_batch_001_small_semantic_v3_review_20260501.md",
            ],
            "failure_categories": ["duplicate_child", "duplicate_patch_fingerprint"],
        },
        "status": "active",
        "created_at": "2026-05-04T00:00:00+00:00",
    },
    {
        "source_run_id": "phase4_current_state_20260504",
        "source_stage": "controller_static",
        "source_outcome": "failure",
        "memory_type": "repair_pattern",
        "title": "Use pandas clip upper and lower keywords",
        "description": "Use for vector-smoke repair on pandas expressions.",
        "content": (
            "Pandas Series.clip uses lower and upper keyword arguments. A patch with .clip(max=...) is a "
            "repairable API mistake; replace max with upper when the intended cap is an upper bound."
        ),
        "applicability": {
            "data_stage": "stage_0_daily_stock",
            "target_surface": ["signal", "ranking", "portfolio", "risk"],
            "island": "repair_near_miss",
        },
        "evidence": {
            "artifact_paths": [
                "projects/quant_research_system/phase4_search_loop/current_state.md",
                "projects/quant_research_system/phase4_search_loop/controller_batch_001_small_semantic_v2_review_20260501.md",
            ],
            "failure_categories": ["vector_smoke_failed"],
        },
        "status": "active",
        "created_at": "2026-05-04T00:00:00+00:00",
    },
]


def _compact_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return " ".join(value.split())
    return " ".join(json.dumps(value, sort_keys=True, default=str).split())


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value if str(item)]
    if isinstance(value, tuple):
        return [str(item) for item in value if str(item)]
    return [str(value)]


def _stable_memory_id(item: dict[str, Any]) -> str:
    fields = [
        item.get("memory_type", ""),
        item.get("title", ""),
        item.get("description", ""),
        item.get("content", ""),
        item.get("source_run_id", ""),
    ]
    digest = hashlib.sha256("\n".join(_compact_text(field) for field in fields).encode("utf-8")).hexdigest()
    return f"mem_{digest[:16]}"


def validate_memory_item(item: dict[str, Any]) -> dict[str, Any]:
    """Normalize and validate one reasoning-memory item."""

    record = dict(item)
    record.setdefault("schema_version", MEMORY_SCHEMA_VERSION)
    record.setdefault("memory_item_id", _stable_memory_id(record))
    record.setdefault("source_program_ids", [])
    record.setdefault("source_attempt_ids", [])
    record.setdefault("source_stage", "")
    record.setdefault("source_outcome", "")
    record.setdefault("memory_type", "failure_guardrail")
    record.setdefault("applicability", {})
    record.setdefault("evidence", {})
    record.setdefault("status", "candidate")
    record.setdefault("created_at", utc_now_iso())
    record.setdefault("retrieval_text", "")

    missing = [key for key in ("title", "description", "content") if not _compact_text(record.get(key))]
    if missing:
        raise ValueError(f"memory item missing required fields: {missing}")
    if record["memory_type"] not in VALID_MEMORY_TYPES:
        raise ValueError(f"invalid memory_type: {record['memory_type']}")
    if record["status"] not in VALID_STATUSES:
        raise ValueError(f"invalid memory status: {record['status']}")
    if not isinstance(record["applicability"], dict):
        raise ValueError("memory applicability must be a dict")
    if not isinstance(record["evidence"], dict):
        raise ValueError("memory evidence must be a dict")
    if not record["retrieval_text"]:
        record["retrieval_text"] = " ".join(
            _compact_text(record.get(key)) for key in ("title", "description", "content")
        )
    return record


def read_memory_items(path: str | Path) -> list[dict[str, Any]]:
    """Read JSONL memory items. Missing files return an empty list."""

    memory_path = Path(path)
    if not memory_path.exists():
        return []
    items: list[dict[str, Any]] = []
    for line_number, line in enumerate(memory_path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid JSONL memory item at {memory_path}:{line_number}") from exc
        items.append(validate_memory_item(payload))
    return items


def append_memory_items(path: str | Path, items: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """Append memory items to JSONL, skipping existing ids and exact content duplicates."""

    memory_path = Path(path)
    memory_path.parent.mkdir(parents=True, exist_ok=True)
    existing = read_memory_items(memory_path)
    existing_ids = {item["memory_item_id"] for item in existing}
    existing_fingerprints = {_memory_fingerprint(item) for item in existing}
    appended: list[dict[str, Any]] = []
    with memory_path.open("a", encoding="utf-8") as handle:
        for item in items:
            record = validate_memory_item(item)
            fingerprint = _memory_fingerprint(record)
            if record["memory_item_id"] in existing_ids or fingerprint in existing_fingerprints:
                continue
            handle.write(json.dumps(record, sort_keys=True) + "\n")
            appended.append(record)
            existing_ids.add(record["memory_item_id"])
            existing_fingerprints.add(fingerprint)
    return appended


def bootstrap_default_memory_bank(path: str | Path) -> list[dict[str, Any]]:
    """Ensure the default Phase 4 seed lessons exist and return the full bank."""

    append_memory_items(path, DEFAULT_MEMORY_ITEMS)
    return read_memory_items(path)


def _memory_fingerprint(item: dict[str, Any]) -> str:
    text = "\n".join(
        _compact_text(item.get(key)) for key in ("memory_type", "title", "description", "content")
    )
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _tokenize(text: str) -> set[str]:
    return {token for token in re.findall(r"[a-zA-Z0-9_]+", text.lower()) if len(token) > 2}


def _value_matches(stored: Any, requested: str | None) -> bool:
    if not requested:
        return True
    values = {item.lower() for item in _as_list(stored)}
    if not values or "any" in values:
        return True
    return requested.lower() in values


def _applicability_matches(
    item: dict[str, Any],
    *,
    source_stage: str | None,
    target_surface: str | None,
    island: str | None,
    data_stage: str | None,
    map_cell: str | None,
) -> bool:
    applicability = item.get("applicability", {})
    return (
        _value_matches(item.get("source_stage"), source_stage)
        and _value_matches(applicability.get("target_surface"), target_surface)
        and _value_matches(applicability.get("island"), island)
        and _value_matches(applicability.get("data_stage"), data_stage)
        and _value_matches(applicability.get("map_cell"), map_cell)
    )


def retrieve_memory_items(
    items: Iterable[dict[str, Any]],
    *,
    source_stage: str | None = None,
    target_surface: str | None = None,
    island: str | None = None,
    data_stage: str | None = None,
    map_cell: str | None = None,
    query: str = "",
    limit: int = 3,
    statuses: set[str] | None = None,
) -> list[dict[str, Any]]:
    """Retrieve memory items by hard context first, then lexical overlap."""

    if limit <= 0:
        return []
    allowed_statuses = statuses or ACTIVE_STATUSES
    query_tokens = _tokenize(query)
    scored: list[tuple[float, str, dict[str, Any]]] = []
    for item in items:
        record = validate_memory_item(item)
        if record["status"] not in allowed_statuses:
            continue
        if not _applicability_matches(
            record,
            source_stage=source_stage,
            target_surface=target_surface,
            island=island,
            data_stage=data_stage,
            map_cell=map_cell,
        ):
            continue
        text_tokens = _tokenize(record.get("retrieval_text", ""))
        overlap = len(query_tokens & text_tokens)
        applicability = record.get("applicability", {})
        context_score = 0.0
        if source_stage and _value_matches(record.get("source_stage"), source_stage):
            context_score += 1.0
        if target_surface and target_surface in {
            value.lower() for value in _as_list(applicability.get("target_surface"))
        }:
            context_score += 3.0
        if island and island in {value.lower() for value in _as_list(applicability.get("island"))}:
            context_score += 1.0
        if data_stage and data_stage in {value.lower() for value in _as_list(applicability.get("data_stage"))}:
            context_score += 1.0
        score = context_score + float(overlap)
        ranked = dict(record)
        ranked["_retrieval_score"] = score
        scored.append((score, ranked["title"], ranked))
    scored.sort(key=lambda item: (-item[0], item[1]))
    return [item for _, _, item in scored[:limit]]


def render_memory_cards(items: Iterable[dict[str, Any]]) -> str:
    """Render prompt-facing memory cards."""

    lines: list[str] = []
    for item in items:
        record = validate_memory_item(item)
        applicability = record.get("applicability", {})
        surface = ",".join(_as_list(applicability.get("target_surface"))) or "any"
        lines.append(f"- [{record['memory_type']} | {surface}] {record['title']}:")
        lines.append(f"  {record['content']}")
        evidence_text = _render_evidence(record.get("evidence", {}))
        if evidence_text:
            lines.append(f"  Evidence: {evidence_text}")
    return "\n".join(lines) if lines else "None."


def _render_evidence(evidence: dict[str, Any]) -> str:
    parts: list[str] = []
    failure_categories = _as_list(evidence.get("failure_categories"))
    if failure_categories:
        parts.append("failure_categories=" + ",".join(failure_categories[:4]))
    artifact_paths = _as_list(evidence.get("artifact_paths"))
    if artifact_paths:
        parts.append("artifacts=" + ",".join(artifact_paths[:2]))
    return "; ".join(parts)


def build_controller_batch_memory_update(
    *,
    source_run_id: str,
    summary: dict[str, Any],
    attempts: list[dict[str, Any]],
    memory_path: str | Path | None,
    retrieved_memory_ids: list[str],
) -> dict[str, Any]:
    """Build a deterministic memory update for one controller batch."""

    failure_categories = summary.get("failure_categories", {})
    success_lessons: list[str] = []
    failure_lessons: list[str] = []
    candidate_memory_topics: list[dict[str, Any]] = []

    pass_count = int(summary.get("pass_count", 0) or 0)
    if pass_count:
        success_lessons.append(
            "Controller-static generated "
            f"{pass_count} pass children across {summary.get('map_cell_count', 0)} MAP cells."
        )
    if summary.get("reasoning_only_empty_count", 0):
        failure_lessons.append(
            "Reasoning-only empty responses still appeared; keep no-thinking routing and empty-content retry active."
        )
        candidate_memory_topics.append(
            {
                "memory_type": "model_routing",
                "title": "Reasoning-only empty output",
                "support": {"count": summary.get("reasoning_only_empty_count", 0)},
            }
        )
    for category, count in failure_categories.items():
        lesson = _failure_category_lesson(category, count)
        if lesson:
            failure_lessons.append(lesson)
            candidate_memory_topics.append(
                {
                    "memory_type": _memory_type_for_failure_category(category),
                    "title": category,
                    "support": {"count": count},
                }
            )

    surfaces = sorted({str(item.get("target_surface")) for item in attempts if item.get("target_surface")})
    map_cells = sorted({str(item.get("map_cell_key")) for item in attempts if item.get("map_cell_key")})

    return {
        "schema_version": MEMORY_UPDATE_SCHEMA_VERSION,
        "source_run_id": source_run_id,
        "created_at": utc_now_iso(),
        "memory_path": str(memory_path) if memory_path else None,
        "retrieved_memory_ids": sorted(set(retrieved_memory_ids)),
        "summary_metrics": {
            "attempt_count": summary.get("attempt_count"),
            "pass_count": summary.get("pass_count"),
            "unique_child_pass_rate": summary.get("unique_child_pass_rate"),
            "duplicate_child_count": summary.get("duplicate_child_count"),
            "duplicate_patch_fingerprint_count": summary.get("duplicate_patch_fingerprint_count"),
            "map_cell_count": summary.get("map_cell_count"),
            "failure_categories": failure_categories,
        },
        "surfaces_seen": surfaces,
        "map_cells_seen": map_cells,
        "success_lessons": success_lessons,
        "failure_lessons": failure_lessons,
        "candidate_memory_topics": candidate_memory_topics,
        "extraction_status": "deterministic_summary_only",
        "next_extraction_step": (
            "Run remote Qwen self-contrast extraction on this update plus attempt artifacts before "
            "promoting new non-seed active memories."
        ),
    }


def write_memory_update(out_dir: str | Path, update: dict[str, Any]) -> dict[str, str]:
    """Write a deterministic memory update as JSON and Markdown."""

    path = Path(out_dir)
    path.mkdir(parents=True, exist_ok=True)
    json_path = path / "reasoning_memory_update.json"
    md_path = path / "reasoning_memory_update.md"
    json_path.write_text(json.dumps(update, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(_render_memory_update_markdown(update), encoding="utf-8")
    return {"json": str(json_path), "markdown": str(md_path)}


def append_memory_update(path: str | Path, update: dict[str, Any]) -> str:
    """Append a controller/evaluator memory update to a central JSONL log."""

    update_path = Path(path)
    update_path.parent.mkdir(parents=True, exist_ok=True)
    with update_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(update, sort_keys=True) + "\n")
    return str(update_path)


def _failure_category_lesson(category: str, count: Any) -> str:
    prefix = f"{category} occurred {count} time(s). "
    lessons = {
        "portfolio_semantic_failed": (
            "Keep portfolio semantic memory active and inspect whether the patch removed one side, "
            "broke signs, or exceeded net/gross/max-weight limits."
        ),
        "duplicate_child": "Duplicate child hashes remain a diversity bottleneck; use retry and distinct MAP cells.",
        "duplicate_patch_fingerprint": (
            "Duplicate normalized patch fingerprints remain a diversity bottleneck; forbid the repeated patch text."
        ),
        "vector_smoke_failed": "Vector-smoke failures should become repair-pattern candidates if the API mistake is local.",
        "exact_search_not_found": "Exact SEARCH mismatch means the prompt or repair must copy from the editable body only.",
        "outside_evolve_block": "Outside-block failures mean the model tried to edit helper or marker code.",
        "evolve_marker_error": "Marker failures mean the output copied EVOLVE-BLOCK lines and should be rejected or repaired.",
        "empty_output": "Empty final content is a model-routing failure, not a strategy failure.",
    }
    detail = lessons.get(category)
    return prefix + detail if detail else ""


def _memory_type_for_failure_category(category: str) -> str:
    if category in {"empty_output"}:
        return "model_routing"
    if category in {"vector_smoke_failed"}:
        return "repair_pattern"
    return "failure_guardrail"


def _render_memory_update_markdown(update: dict[str, Any]) -> str:
    lines = [
        "# Reasoning Memory Update",
        "",
        f"- source_run_id: `{update.get('source_run_id')}`",
        f"- extraction_status: `{update.get('extraction_status')}`",
        f"- memory_path: `{update.get('memory_path')}`",
        "",
        "## Summary Metrics",
        "",
    ]
    for key, value in update.get("summary_metrics", {}).items():
        lines.append(f"- {key}: `{value}`")
    lines.extend(["", "## Success Lessons", ""])
    for lesson in update.get("success_lessons", []) or ["none"]:
        lines.append(f"- {lesson}")
    lines.extend(["", "## Failure Lessons", ""])
    for lesson in update.get("failure_lessons", []) or ["none"]:
        lines.append(f"- {lesson}")
    lines.extend(["", "## Candidate Memory Topics", ""])
    for topic in update.get("candidate_memory_topics", []) or ["none"]:
        if isinstance(topic, dict):
            lines.append(f"- {topic.get('memory_type')}: {topic.get('title')} `{topic.get('support')}`")
        else:
            lines.append(f"- {topic}")
    lines.extend(["", "## Next Extraction Step", "", str(update.get("next_extraction_step", "")), ""])
    return "\n".join(lines)


__all__ = [
    "DEFAULT_MEMORY_ITEMS",
    "MEMORY_SCHEMA_VERSION",
    "MEMORY_UPDATE_SCHEMA_VERSION",
    "append_memory_items",
    "append_memory_update",
    "bootstrap_default_memory_bank",
    "build_controller_batch_memory_update",
    "read_memory_items",
    "render_memory_cards",
    "retrieve_memory_items",
    "validate_memory_item",
    "write_memory_update",
]
