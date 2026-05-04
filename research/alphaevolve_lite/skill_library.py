"""Explicit skill library for Phase 4 AlphaEvolve-lite.

Reasoning memory stores compact lessons. The skill library is narrower: it
stores pattern -> strategy rules with confidence, status, and evidence. New
controller batches can propose skill candidates, but promotion stays explicit.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from pathlib import Path
from typing import Any, Iterable

from .paths import utc_now_iso


SKILL_SCHEMA_VERSION = "phase4_skill_item_v1"
SKILL_UPDATE_SCHEMA_VERSION = "phase4_skill_update_v1"

VALID_CONFIDENCE = {"high", "medium", "low", "avoid"}
VALID_STATUS = {"candidate", "active", "superseded", "rejected"}
VALID_SKILL_TYPES = {
    "success_strategy",
    "failure_guardrail",
    "repair_pattern",
    "avoid_strategy",
    "diagnostic_rule",
    "model_routing",
}

CONFIDENCE_SORT = {"avoid": 0, "high": 1, "medium": 2, "low": 3}


DEFAULT_SKILL_ITEMS: list[dict[str, Any]] = [
    {
        "skill_name": "Strict evolve-block SEARCH/REPLACE",
        "skill_type": "failure_guardrail",
        "confidence": "high",
        "status": "active",
        "pattern": "Qwen patching fails by copying marker lines or code outside the target evolve block.",
        "strategy": "Expose only one editable evolve-block body and require SEARCH text from that body only.",
        "prompt_rule": "Copy SEARCH text only from the supplied editable body; never include EVOLVE markers.",
        "applicability": {
            "source_stage": "controller_static",
            "data_stage": "stage_0_daily_stock",
            "target_surface": ["signal", "ranking", "portfolio", "risk"],
        },
        "evidence": {
            "support_count": 2,
            "failure_count": 0,
            "artifact_paths": [
                "projects/quant_research_system/phase4_search_loop/controller_batch_001_small_review_20260430.md",
                "projects/quant_research_system/phase4_search_loop/controller_batch_001_small_semantic_v3_review_20260501.md",
            ],
        },
        "created_at": "2026-05-04T00:00:00+00:00",
    },
    {
        "skill_name": "Preserve balanced long and short books",
        "skill_type": "failure_guardrail",
        "confidence": "high",
        "status": "active",
        "pattern": "Portfolio or risk patch passes syntax but creates no effective short side or high net exposure.",
        "strategy": "Compute positive long and short magnitudes separately, then assign negative weights to shorts.",
        "prompt_rule": "Keep long weights positive, short weights negative, and net exposure near zero.",
        "applicability": {
            "source_stage": "controller_static",
            "data_stage": "stage_0_daily_stock",
            "target_surface": ["signal", "ranking", "portfolio", "risk"],
        },
        "evidence": {
            "support_count": 2,
            "failure_count": 0,
            "artifact_paths": [
                "projects/quant_research_system/phase4_search_loop/controller_batch_001_small_semantic_v2_review_20260501.md",
                "projects/quant_research_system/phase4_search_loop/current_state.md",
            ],
        },
        "created_at": "2026-05-04T00:00:00+00:00",
    },
    {
        "skill_name": "Avoid one-sided signal-proportional short weights",
        "skill_type": "avoid_strategy",
        "confidence": "avoid",
        "status": "active",
        "pattern": "Short-side weighting formula uses negative signal values directly as magnitudes.",
        "strategy": "Avoid this formulation; use absolute or sign-corrected short magnitudes before assigning negative weights.",
        "prompt_rule": "Do not normalize short weights by raw negative signal sums in a way that removes short exposure.",
        "applicability": {
            "source_stage": "controller_static",
            "data_stage": "stage_0_daily_stock",
            "target_surface": ["portfolio", "risk"],
        },
        "evidence": {
            "support_count": 1,
            "failure_count": 1,
            "artifact_paths": [
                "projects/quant_research_system/phase4_search_loop/controller_batch_001_small_semantic_v2_review_20260501.md"
            ],
        },
        "created_at": "2026-05-04T00:00:00+00:00",
    },
    {
        "skill_name": "No-thinking Qwen routing for patch calls",
        "skill_type": "model_routing",
        "confidence": "high",
        "status": "active",
        "pattern": "Qwen spends completion budget in reasoning and returns null final content.",
        "strategy": "Disable thinking in the raw vLLM payload and retry empty final content once.",
        "prompt_rule": "The patch must be in message.content; do not rely on reasoning output.",
        "applicability": {
            "source_stage": "controller_static",
            "data_stage": "stage_0_daily_stock",
            "target_surface": ["signal", "ranking", "portfolio", "risk"],
        },
        "evidence": {
            "support_count": 1,
            "failure_count": 1,
            "artifact_paths": [
                "projects/quant_research_system/phase4_search_loop/controller_batch_001_small_semantic_v3_review_20260501.md"
            ],
        },
        "created_at": "2026-05-04T00:00:00+00:00",
    },
    {
        "skill_name": "Duplicate retry should change semantic intent",
        "skill_type": "repair_pattern",
        "confidence": "medium",
        "status": "active",
        "pattern": "A safe child duplicates an existing child hash or normalized patch fingerprint.",
        "strategy": "Retry with occupied MAP cells and forbidden patches, targeting a different behavior descriptor.",
        "prompt_rule": "A duplicate retry must make a distinct semantic change, not a cosmetic diff.",
        "applicability": {
            "source_stage": "controller_static",
            "data_stage": "stage_0_daily_stock",
            "target_surface": ["signal", "ranking", "portfolio", "risk"],
        },
        "evidence": {
            "support_count": 1,
            "failure_count": 1,
            "artifact_paths": [
                "projects/quant_research_system/phase4_search_loop/controller_batch_001_small_semantic_v3_review_20260501.md"
            ],
        },
        "created_at": "2026-05-04T00:00:00+00:00",
    },
]


def _stable_skill_id(item: dict[str, Any]) -> str:
    payload = "|".join(
        _compact_text(item.get(key, "")) for key in ("skill_type", "skill_name", "pattern", "strategy")
    )
    return "skill_" + hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def _compact_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip()).lower()


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return [value]


def validate_skill_item(item: dict[str, Any]) -> dict[str, Any]:
    """Normalize and validate one skill-library item."""

    record = dict(item)
    record.setdefault("schema_version", SKILL_SCHEMA_VERSION)
    record.setdefault("skill_id", _stable_skill_id(record))
    record.setdefault("skill_type", "failure_guardrail")
    record.setdefault("confidence", "low")
    record.setdefault("status", "candidate")
    record.setdefault("created_at", utc_now_iso())
    record.setdefault("applicability", {})
    record.setdefault("evidence", {})
    required = ["skill_id", "skill_name", "skill_type", "confidence", "status", "pattern", "strategy", "prompt_rule"]
    missing = [key for key in required if not record.get(key)]
    if missing:
        raise ValueError(f"skill item missing required fields: {missing}")
    if record["skill_type"] not in VALID_SKILL_TYPES:
        raise ValueError(f"invalid skill_type: {record['skill_type']}")
    if record["confidence"] not in VALID_CONFIDENCE:
        raise ValueError(f"invalid skill confidence: {record['confidence']}")
    if record["status"] not in VALID_STATUS:
        raise ValueError(f"invalid skill status: {record['status']}")
    if not isinstance(record["applicability"], dict):
        raise ValueError("skill applicability must be a dict")
    if not isinstance(record["evidence"], dict):
        raise ValueError("skill evidence must be a dict")
    return record


def read_skill_items(path: str | Path) -> list[dict[str, Any]]:
    skill_path = Path(path)
    if not skill_path.exists():
        return []
    items = []
    for line_number, line in enumerate(skill_path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid JSONL skill item at {skill_path}:{line_number}") from exc
        items.append(validate_skill_item(payload))
    return items


def append_skill_items(path: str | Path, items: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    skill_path = Path(path)
    skill_path.parent.mkdir(parents=True, exist_ok=True)
    existing = read_skill_items(skill_path)
    existing_ids = {item["skill_id"] for item in existing}
    appended = []
    with skill_path.open("a", encoding="utf-8") as handle:
        for item in items:
            record = validate_skill_item(item)
            if record["skill_id"] in existing_ids:
                continue
            handle.write(json.dumps(record, sort_keys=True) + "\n")
            existing_ids.add(record["skill_id"])
            appended.append(record)
    return appended


def bootstrap_default_skill_library(path: str | Path) -> list[dict[str, Any]]:
    append_skill_items(path, DEFAULT_SKILL_ITEMS)
    return read_skill_items(path)


def retrieve_skill_items(
    items: Iterable[dict[str, Any]],
    *,
    source_stage: str,
    target_surface: str,
    data_stage: str,
    query: str = "",
    limit: int = 3,
) -> list[dict[str, Any]]:
    """Retrieve active skill items by applicability and lexical overlap."""

    query_terms = set(_compact_text(query).split())
    scored: list[tuple[float, dict[str, Any]]] = []
    for item in items:
        record = validate_skill_item(item)
        if record.get("status") != "active":
            continue
        applicability = record.get("applicability", {})
        stages = {str(value) for value in _as_list(applicability.get("source_stage")) if value}
        data_stages = {str(value) for value in _as_list(applicability.get("data_stage")) if value}
        surfaces = {str(value) for value in _as_list(applicability.get("target_surface")) if value}
        if stages and source_stage not in stages and "any" not in stages:
            continue
        if data_stages and data_stage not in data_stages and "any" not in data_stages:
            continue
        if surfaces and target_surface not in surfaces and "any" not in surfaces:
            continue
        text = " ".join(
            _compact_text(record.get(key)) for key in ("skill_name", "pattern", "strategy", "prompt_rule")
        )
        terms = set(text.split())
        overlap = len(query_terms & terms)
        evidence = record.get("evidence", {})
        support = _as_float(evidence.get("support_count")) or 0.0
        confidence_bonus = 4.0 - CONFIDENCE_SORT.get(record.get("confidence"), 3)
        score = confidence_bonus + min(support, 5.0) * 0.25 + overlap * 0.1
        scored.append((score, record))
    scored.sort(
        key=lambda item: (
            -item[0],
            CONFIDENCE_SORT.get(item[1].get("confidence"), 99),
            item[1].get("skill_name", ""),
        )
    )
    return [record for _, record in scored[: max(0, limit)]]


def _as_float(value: Any) -> float | None:
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    return result if math.isfinite(result) else None


def render_skill_cards(items: Iterable[dict[str, Any]]) -> str:
    """Render compact prompt-facing skill cards."""

    lines: list[str] = []
    for item in items:
        record = validate_skill_item(item)
        evidence = record.get("evidence", {})
        lines.append(
            f"- [{record['confidence']} | {record['skill_type']}] {record['skill_name']}: {record['prompt_rule']}"
        )
        lines.append(f"  pattern: {record['pattern']}")
        lines.append(
            "  evidence: "
            f"support_count={evidence.get('support_count')}, failure_count={evidence.get('failure_count')}"
        )
    return "\n".join(lines) if lines else "None."


def build_controller_batch_skill_update(
    *,
    source_run_id: str,
    summary: dict[str, Any],
    attempts: list[dict[str, Any]],
    skill_library_path: str | Path | None,
    retrieved_skill_ids: list[str],
) -> dict[str, Any]:
    """Build a deterministic skill update proposal from one controller batch."""

    candidate_items: list[dict[str, Any]] = []
    pass_attempts = [item for item in attempts if item.get("decision") == "pass"]
    for item in pass_attempts[:5]:
        surface = str(item.get("target_surface") or "unknown")
        intent = str(item.get("patch_intent") or "unknown")
        candidate_items.append(
            validate_skill_item(
                {
                    "skill_name": f"Controller-safe {surface}/{intent} patch",
                    "skill_type": "success_strategy",
                    "confidence": "low",
                    "status": "candidate",
                    "pattern": (
                        f"A {surface} patch with intent {intent} passed controller-static gates in a sibling batch."
                    ),
                    "strategy": (
                        "Keep the transformation focused and evaluate it against sibling children before promotion."
                    ),
                    "prompt_rule": (
                        f"{surface}/{intent} is controller-safe evidence only; do not treat it as market-alpha proof."
                    ),
                    "applicability": {
                        "source_stage": "controller_static",
                        "data_stage": "stage_0_daily_stock",
                        "target_surface": [surface],
                    },
                    "evidence": {
                        "support_count": 1,
                        "failure_count": 0,
                        "source_run_id": source_run_id,
                        "program_id": item.get("program_id"),
                        "map_cell_key": item.get("map_cell_key"),
                    },
                }
            )
        )
    failure_categories = summary.get("failure_categories", {}) or {}
    for category, count in sorted(failure_categories.items())[:5]:
        candidate_items.append(
            validate_skill_item(
                {
                    "skill_name": f"Guard against {category}",
                    "skill_type": "failure_guardrail",
                    "confidence": "low",
                    "status": "candidate",
                    "pattern": f"Controller batch produced {count} `{category}` failures.",
                    "strategy": "Use the concrete failure reason and artifacts before changing generator policy.",
                    "prompt_rule": f"Do not repeat patches that trigger `{category}`.",
                    "applicability": {
                        "source_stage": "controller_static",
                        "data_stage": "stage_0_daily_stock",
                        "target_surface": ["signal", "ranking", "portfolio", "risk"],
                    },
                    "evidence": {
                        "support_count": 0,
                        "failure_count": int(count),
                        "source_run_id": source_run_id,
                    },
                }
            )
        )
    return {
        "schema_version": SKILL_UPDATE_SCHEMA_VERSION,
        "source_run_id": source_run_id,
        "created_at": utc_now_iso(),
        "skill_library_path": str(skill_library_path) if skill_library_path else None,
        "retrieved_skill_ids": sorted(set(retrieved_skill_ids)),
        "summary": {
            "attempt_count": summary.get("attempt_count"),
            "pass_count": summary.get("pass_count"),
            "failure_categories": failure_categories,
            "duplicate_child_count": summary.get("duplicate_child_count"),
            "duplicate_patch_fingerprint_count": summary.get("duplicate_patch_fingerprint_count"),
        },
        "candidate_skill_items": candidate_items,
        "promotion_policy": (
            "Candidate skills are not auto-promoted from one controller batch. Promote to active only after "
            "deterministic support checks, preferably including sibling-relative evaluator evidence."
        ),
    }


def write_skill_update(out_dir: str | Path, update: dict[str, Any]) -> dict[str, str]:
    path = Path(out_dir)
    path.mkdir(parents=True, exist_ok=True)
    json_path = path / "skill_update.json"
    md_path = path / "skill_update.md"
    json_path.write_text(json.dumps(update, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(_render_skill_update_markdown(update), encoding="utf-8")
    return {"json": str(json_path), "markdown": str(md_path)}


def append_skill_update(path: str | Path, update: dict[str, Any]) -> str:
    update_path = Path(path)
    update_path.parent.mkdir(parents=True, exist_ok=True)
    with update_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(update, sort_keys=True) + "\n")
    return str(update_path)


def _render_skill_update_markdown(update: dict[str, Any]) -> str:
    lines = [
        "# Skill Update",
        "",
        f"- schema_version: `{update.get('schema_version')}`",
        f"- source_run_id: `{update.get('source_run_id')}`",
        f"- skill_library_path: `{update.get('skill_library_path')}`",
        f"- retrieved_skill_ids: `{update.get('retrieved_skill_ids')}`",
        "",
        "## Promotion Policy",
        "",
        str(update.get("promotion_policy", "")),
        "",
        "## Candidate Skill Items",
        "",
    ]
    for item in update.get("candidate_skill_items", []) or []:
        lines.extend(
            [
                f"### {item.get('skill_name')}",
                "",
                f"- skill_id: `{item.get('skill_id')}`",
                f"- skill_type: `{item.get('skill_type')}`",
                f"- confidence: `{item.get('confidence')}`",
                f"- status: `{item.get('status')}`",
                f"- prompt_rule: {item.get('prompt_rule')}",
                f"- evidence: `{item.get('evidence')}`",
                "",
            ]
        )
    if not update.get("candidate_skill_items"):
        lines.append("- none")
    return "\n".join(lines)


__all__ = [
    "DEFAULT_SKILL_ITEMS",
    "SKILL_SCHEMA_VERSION",
    "SKILL_UPDATE_SCHEMA_VERSION",
    "append_skill_items",
    "append_skill_update",
    "bootstrap_default_skill_library",
    "build_controller_batch_skill_update",
    "read_skill_items",
    "render_skill_cards",
    "retrieve_skill_items",
    "validate_skill_item",
    "write_skill_update",
]
