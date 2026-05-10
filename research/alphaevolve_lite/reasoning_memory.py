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

from .artifact_io import write_json
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
    {
        "source_run_id": "controller_batch_001_diversity_topup_review_20260509",
        "source_stage": "controller_static",
        "source_outcome": "mixed",
        "memory_type": "failure_guardrail",
        "title": "Target intent is binding evidence",
        "description": "Use when a MAP target cell is supplied to child generation.",
        "content": (
            "A controller-safe off-target child can still be stored under its actual behavior descriptor, "
            "but it should not count as full success for the sampled prompt card. Penalize target-intent "
            "mismatches so generic evaluator guidance does not overpower MAP-cell coverage."
        ),
        "applicability": {
            "data_stage": "stage_0_daily_stock",
            "target_surface": ["signal", "ranking", "portfolio", "risk"],
            "island": "any",
        },
        "evidence": {
            "artifact_paths": [
                "projects/quant_research_system/phase4_search_loop/controller_batch_001_diversity_topup_review_20260509.md"
            ],
            "failure_categories": ["target_intent_mismatch"],
        },
        "status": "active",
        "created_at": "2026-05-09T00:00:00+00:00",
    },
    {
        "source_run_id": "controller_batch_001_diversity_topup_review_20260509",
        "source_stage": "controller_static",
        "source_outcome": "failure",
        "memory_type": "repair_pattern",
        "title": "Align pandas boolean masks before assignment",
        "description": "Use for portfolio sparse or no-trade-band patches.",
        "content": (
            "Boolean Series indexers must align with the object being indexed. For portfolio weights, "
            "derive index labels such as valid.index[mask], longs[mask], or shorts[mask] before assigning "
            "into weights; do not pass a boolean Series indexed by a filtered frame directly to weights.loc."
        ),
        "applicability": {
            "data_stage": "stage_0_daily_stock",
            "target_surface": ["portfolio", "risk"],
            "island": "repair_near_miss",
        },
        "evidence": {
            "artifact_paths": [
                "projects/quant_research_system/phase4_search_loop/controller_batch_001_diversity_topup_review_20260509.md"
            ],
            "failure_categories": ["vector_smoke_failed"],
        },
        "status": "active",
        "created_at": "2026-05-09T00:00:00+00:00",
    },
    {
        "source_run_id": "controller_batch_001_diversity_topup_review_20260509",
        "source_stage": "controller_static",
        "source_outcome": "failure",
        "memory_type": "failure_guardrail",
        "title": "Do not substitute dampening for time smoothing",
        "description": "Use for signal time_smoothing target cells.",
        "content": (
            "For a time_smoothing target, make a causal rolling, EWM, or lagged smoothing change. "
            "Nonlinear magnitude dampeners such as signal * exp(-abs(signal) / c) are different intents "
            "and can reorder signals enough to violate portfolio sign semantics."
        ),
        "applicability": {
            "data_stage": "stage_0_daily_stock",
            "target_surface": ["signal"],
            "island": "repair_near_miss",
        },
        "evidence": {
            "artifact_paths": [
                "projects/quant_research_system/phase4_search_loop/controller_batch_001_diversity_topup_review_20260509.md"
            ],
            "failure_categories": ["portfolio_semantic_failed"],
        },
        "status": "active",
        "created_at": "2026-05-09T00:00:00+00:00",
    },
    {
        "source_run_id": "remote_sample_eval_controller_batch_001_review_20260509",
        "source_stage": ["controller_static", "remote_sample_eval"],
        "source_outcome": "failure",
        "memory_type": "evaluator_caveat",
        "title": "Sparse few-day portfolios are review artifacts",
        "description": "Use before portfolio, risk, signal, or ranking changes that may reduce active dates.",
        "content": (
            "A child can show very high sample Sharpe by trading only a few dates. Treat that as a "
            "coverage artifact, not alpha. Preserve broad active portfolio-day coverage unless a separate "
            "human-approved sparse strategy contract is introduced."
        ),
        "applicability": {
            "data_stage": "stage_0_daily_stock",
            "target_surface": ["signal", "ranking", "portfolio", "risk"],
            "island": ["portfolio_risk_turnover", "signal_transform", "repair_near_miss", "any"],
        },
        "evidence": {
            "artifact_paths": [
                "projects/quant_research_system/phase4_search_loop/remote_sample_eval_controller_batch_001_review_20260509.md"
            ],
            "failure_categories": ["sparse_portfolio_coverage", "sample_review_artifact"],
            "attempt_ids": ["attempt_000"],
        },
        "status": "active",
        "created_at": "2026-05-09T00:00:00+00:00",
    },
    {
        "source_run_id": "remote_sample_eval_controller_batch_001_review_20260509",
        "source_stage": ["controller_static", "remote_sample_eval"],
        "source_outcome": "failure",
        "memory_type": "evaluator_caveat",
        "title": "Metric-equivalent children are not useful improvements",
        "description": "Use when a patch changes code but not search-sample behavior versus the seed or parent.",
        "content": (
            "A monotone, threshold-absorbed, or cosmetic patch can produce metrics indistinguishable from "
            "the reference program. Store it as evidence, but do not treat it as a useful child; ask for "
            "a behaviorally meaningful change that survives ranking, selection, and risk controls."
        ),
        "applicability": {
            "data_stage": "stage_0_daily_stock",
            "target_surface": ["signal", "ranking", "portfolio", "risk"],
            "island": ["signal_transform", "portfolio_risk_turnover", "any"],
        },
        "evidence": {
            "artifact_paths": [
                "projects/quant_research_system/phase4_search_loop/remote_sample_eval_controller_batch_001_review_20260509.md"
            ],
            "failure_categories": ["metric_equivalent_to_reference"],
            "attempt_ids": ["attempt_004", "attempt_010", "attempt_011"],
        },
        "status": "active",
        "created_at": "2026-05-09T00:00:00+00:00",
    },
    {
        "source_run_id": "remote_sample_eval_controller_batch_001_review_20260509",
        "source_stage": ["controller_static", "remote_sample_eval"],
        "source_outcome": "failure",
        "memory_type": "data_contract",
        "title": "Do not use forward-return availability inside child code",
        "description": "Use when repairing missing-held-weight or sparse-coverage problems.",
        "content": (
            "Missing held weight must be reduced without lookahead. Generated strategy code must not use "
            "fwd_ret, fwd_date, fwd_vwretd, next_market_date, or one_day_forward to select or weight names; "
            "those fields are evaluator accounting fields."
        ),
        "applicability": {
            "data_stage": "stage_0_daily_stock",
            "target_surface": ["signal", "ranking", "portfolio", "risk"],
            "island": "any",
        },
        "evidence": {
            "artifact_paths": [
                "projects/quant_research_system/phase4_search_loop/remote_sample_eval_controller_batch_001_review_20260509.md"
            ],
            "failure_categories": ["lookahead_guardrail"],
        },
        "status": "active",
        "created_at": "2026-05-09T00:00:00+00:00",
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
    group_relative = build_group_relative_controller_report(attempts)

    pass_count = int(summary.get("pass_count", 0) or 0)
    if pass_count:
        success_lessons.append(
            "Controller-static generated "
            f"{pass_count} pass children across {summary.get('map_cell_count', 0)} MAP cells."
        )
    top_siblings = group_relative.get("top_siblings", [])
    if top_siblings:
        best = top_siblings[0]
        best_message = (
            "Best controller sibling by group-relative score: "
            f"attempt {best.get('attempt')} on {best.get('target_surface')} with "
            f"intent {best.get('patch_intent')} and decision {best.get('decision')}."
        )
        if best.get("decision") == "pass":
            success_lessons.append(best_message)
            candidate_memory_topics.append(
                {
                    "memory_type": "success_strategy",
                    "title": "best_group_relative_controller_sibling",
                    "support": {
                        "attempt": best.get("attempt"),
                        "target_surface": best.get("target_surface"),
                        "patch_intent": best.get("patch_intent"),
                        "relative_advantage": best.get("relative_advantage"),
                    },
                }
            )
        else:
            failure_lessons.append(
                best_message + " No sibling passed, so this is contrast evidence only, not a promotable skill."
            )
            candidate_memory_topics.append(
                {
                    "memory_type": "failure_guardrail",
                    "title": "no_passing_group_relative_controller_sibling",
                    "support": {
                        "attempt": best.get("attempt"),
                        "target_surface": best.get("target_surface"),
                        "patch_intent": best.get("patch_intent"),
                        "failure_category": best.get("failure_category"),
                        "relative_advantage": best.get("relative_advantage"),
                    },
                }
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
    weak_strategy_rows = [
        item
        for item in group_relative.get("strategy_stats", [])
        if item.get("attempt_count", 0) >= 1 and item.get("pass_rate", 0.0) == 0.0
    ]
    for weak in weak_strategy_rows[:3]:
        candidate_memory_topics.append(
            {
                "memory_type": "failure_guardrail",
                "title": "weak_group_relative_controller_strategy",
                "support": {
                    "target_surface": weak.get("target_surface"),
                    "patch_intent": weak.get("patch_intent"),
                    "attempt_count": weak.get("attempt_count"),
                    "mean_relative_advantage": weak.get("mean_relative_advantage"),
                },
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
            "behavior_delta_pass_rate": summary.get("behavior_delta_pass_rate"),
            "duplicate_child_count": summary.get("duplicate_child_count"),
            "duplicate_patch_fingerprint_count": summary.get("duplicate_patch_fingerprint_count"),
            "behavioral_noop_count": summary.get("behavioral_noop_count"),
            "map_cell_count": summary.get("map_cell_count"),
            "failure_categories": failure_categories,
        },
        "group_relative_controller_report": group_relative,
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


def build_group_relative_controller_report(attempts: list[dict[str, Any]]) -> dict[str, Any]:
    """Compare sibling controller attempts generated from the same parent.

    This is the controller-static analogue of Dr. RTL's group-relative skill
    signal. It is not a market-alpha score. It ranks siblings by validity,
    uniqueness, repair burden, and diversity so later skill extraction can
    compare matched attempts instead of isolated logs.
    """

    scored = [_controller_attempt_relative_record(item) for item in attempts]
    if not scored:
        return {
            "score_definition": "controller_static_quality_score_higher_is_better",
            "attempt_count": 0,
            "mean_score": None,
            "std_score": None,
            "top_siblings": [],
            "bottom_siblings": [],
            "strategy_stats": [],
        }
    scores = [float(item["controller_quality_score"]) for item in scored]
    mean_score = sum(scores) / len(scores)
    variance = sum((score - mean_score) ** 2 for score in scores) / len(scores)
    std_score = variance**0.5
    for item in scored:
        if std_score > 1e-12:
            item["relative_advantage"] = round((item["controller_quality_score"] - mean_score) / std_score, 6)
        else:
            item["relative_advantage"] = 0.0
    ranked = sorted(scored, key=lambda item: (-item["relative_advantage"], _attempt_sort_value(item)))
    return {
        "score_definition": (
            "controller_static_quality_score_higher_is_better; combines decision, hard-gate pass rate, "
            "uniqueness, repair/empty-output burden, and MAP-cell occupancy. It is for sibling comparison "
            "only, not market validation."
        ),
        "attempt_count": len(scored),
        "mean_score": round(mean_score, 6),
        "std_score": round(std_score, 6),
        "top_siblings": ranked[:5],
        "bottom_siblings": list(reversed(ranked[-5:])),
        "strategy_stats": _group_strategy_stats(scored),
    }


def _attempt_sort_value(item: dict[str, Any]) -> int:
    attempt = item.get("attempt")
    return attempt if isinstance(attempt, int) else 10**9


def _controller_attempt_relative_record(item: dict[str, Any]) -> dict[str, Any]:
    score = _controller_quality_score(item)
    return {
        "attempt": item.get("attempt"),
        "program_id": item.get("program_id"),
        "target_surface": item.get("target_surface"),
        "patch_intent": item.get("patch_intent") or "unknown",
        "map_cell_key": item.get("map_cell_key"),
        "decision": item.get("decision"),
        "failure_category": item.get("failure_category"),
        "repair_attempted": bool(item.get("repair_attempted")),
        "repair_succeeded": bool(item.get("repair_succeeded")),
        "duplicate_retry_attempted": bool(item.get("duplicate_retry_attempted")),
        "duplicate_retry_succeeded": bool(item.get("duplicate_retry_succeeded")),
        "map_cell_already_occupied": bool(item.get("map_cell_already_occupied")),
        "controller_quality_score": round(score, 6),
    }


def _controller_quality_score(item: dict[str, Any]) -> float:
    hard_gates = item.get("hard_gates", {}) or {}
    gate_values = [1.0 if value else 0.0 for value in hard_gates.values()]
    gate_rate = sum(gate_values) / len(gate_values) if gate_values else 0.0
    score = gate_rate
    if item.get("decision") == "pass":
        score += 1.0
    if item.get("hard_gates", {}).get("unique_child"):
        score += 0.25
    if item.get("map_cell_key"):
        score += 0.10
    if item.get("map_cell_already_occupied"):
        score -= 0.10
    if item.get("repair_attempted"):
        score -= 0.10
        if item.get("repair_succeeded"):
            score += 0.05
    empty_retry_count = int(item.get("empty_retry_count", 0) or 0)
    if empty_retry_count:
        score -= 0.20 * empty_retry_count
        if item.get("empty_retry_succeeded"):
            score += 0.05
    if item.get("duplicate_retry_attempted"):
        score -= 0.05
        if item.get("duplicate_retry_succeeded"):
            score += 0.20
    failure_penalties = {
        "empty_output": 0.70,
        "portfolio_semantic_failed": 0.55,
        "vector_smoke_failed": 0.35,
        "duplicate_child": 0.30,
        "duplicate_patch_fingerprint": 0.30,
        "behavioral_noop": 0.30,
        "exact_search_not_found": 0.30,
        "outside_evolve_block": 0.45,
        "evolve_marker_error": 0.45,
    }
    failure_category = item.get("failure_category")
    if failure_category:
        score -= failure_penalties.get(str(failure_category), 0.25)
    return score


def _group_strategy_stats(scored_attempts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for item in scored_attempts:
        key = (str(item.get("target_surface")), str(item.get("patch_intent") or "unknown"))
        groups.setdefault(key, []).append(item)
    rows: list[dict[str, Any]] = []
    for (target_surface, patch_intent), group in groups.items():
        pass_count = sum(1 for item in group if item.get("decision") == "pass")
        mean_score = sum(float(item["controller_quality_score"]) for item in group) / len(group)
        mean_advantage = sum(float(item.get("relative_advantage", 0.0)) for item in group) / len(group)
        rows.append(
            {
                "target_surface": target_surface,
                "patch_intent": patch_intent,
                "attempt_count": len(group),
                "pass_count": pass_count,
                "pass_rate": round(pass_count / len(group), 6),
                "mean_controller_quality_score": round(mean_score, 6),
                "mean_relative_advantage": round(mean_advantage, 6),
                "failure_categories": sorted(
                    {
                        str(item.get("failure_category"))
                        for item in group
                        if item.get("failure_category")
                    }
                ),
            }
        )
    rows.sort(key=lambda item: (-item["mean_relative_advantage"], item["target_surface"], item["patch_intent"]))
    return rows


def write_memory_update(out_dir: str | Path, update: dict[str, Any]) -> dict[str, str]:
    """Write a deterministic memory update as JSON and Markdown."""

    path = Path(out_dir)
    path.mkdir(parents=True, exist_ok=True)
    json_path = path / "reasoning_memory_update.json"
    md_path = path / "reasoning_memory_update.md"
    write_json(json_path, update)
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
        "behavioral_noop": (
            "A controller-safe code edit produced the same smoke-panel signal, ranking, and weights as its parent; "
            "treat it as lazy search evidence and ask for a behavior change that survives downstream controls."
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
    group_relative = update.get("group_relative_controller_report", {})
    lines.extend(["", "## Group-Relative Controller Report", ""])
    lines.append(f"- score_definition: `{group_relative.get('score_definition')}`")
    lines.append(f"- attempt_count: `{group_relative.get('attempt_count')}`")
    lines.append(f"- mean_score: `{group_relative.get('mean_score')}`")
    lines.append(f"- std_score: `{group_relative.get('std_score')}`")
    lines.extend(["", "### Top Siblings", ""])
    for item in group_relative.get("top_siblings", []) or ["none"]:
        if isinstance(item, dict):
            lines.append(
                f"- attempt `{item.get('attempt')}` `{item.get('target_surface')}`/"
                f"`{item.get('patch_intent')}` decision `{item.get('decision')}` "
                f"relative_advantage `{item.get('relative_advantage')}`"
            )
        else:
            lines.append(f"- {item}")
    lines.extend(["", "### Strategy Stats", ""])
    for item in group_relative.get("strategy_stats", []) or ["none"]:
        if isinstance(item, dict):
            lines.append(
                f"- `{item.get('target_surface')}`/`{item.get('patch_intent')}`: "
                f"attempts `{item.get('attempt_count')}`, pass_rate `{item.get('pass_rate')}`, "
                f"mean_relative_advantage `{item.get('mean_relative_advantage')}`"
            )
        else:
            lines.append(f"- {item}")
    lines.extend(["", "## Next Extraction Step", "", str(update.get("next_extraction_step", "")), ""])
    return "\n".join(lines)


__all__ = [
    "DEFAULT_MEMORY_ITEMS",
    "MEMORY_SCHEMA_VERSION",
    "MEMORY_UPDATE_SCHEMA_VERSION",
    "append_memory_items",
    "append_memory_update",
    "bootstrap_default_memory_bank",
    "build_group_relative_controller_report",
    "build_controller_batch_memory_update",
    "read_memory_items",
    "render_memory_cards",
    "retrieve_memory_items",
    "validate_memory_item",
    "write_memory_update",
]
