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

from .artifact_io import write_json
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
    {
        "skill_name": "Target intent must match actual patch intent",
        "skill_type": "diagnostic_rule",
        "confidence": "high",
        "status": "active",
        "pattern": "A generated child passes controller gates but implements a different intent from the sampled MAP target.",
        "strategy": "Store the child by its actual descriptor, but lower prompt-card fitness and retry future prompts toward the requested intent.",
        "prompt_rule": "Implement the intended_patch_intent directly; do not substitute an easier or more familiar edit.",
        "applicability": {
            "source_stage": "controller_static",
            "data_stage": "stage_0_daily_stock",
            "target_surface": ["signal", "ranking", "portfolio", "risk"],
        },
        "evidence": {
            "support_count": 1,
            "failure_count": 1,
            "artifact_paths": [
                "projects/quant_research_system/phase4_search_loop/controller_batch_001_diversity_topup_review_20260509.md"
            ],
        },
        "created_at": "2026-05-09T00:00:00+00:00",
    },
    {
        "skill_name": "Align pandas mask indexes before weight assignment",
        "skill_type": "repair_pattern",
        "confidence": "high",
        "status": "active",
        "pattern": "A sparse portfolio patch uses a boolean Series indexed by valid rows directly against weights.loc.",
        "strategy": "Convert masks to labels on the same index before assignment, for example valid.index[mask] or side_index[side_mask].",
        "prompt_rule": "For boolean filtering, assign weights with aligned index labels, not a boolean Series from another object.",
        "applicability": {
            "source_stage": "controller_static",
            "data_stage": "stage_0_daily_stock",
            "target_surface": ["portfolio", "risk"],
        },
        "evidence": {
            "support_count": 1,
            "failure_count": 1,
            "artifact_paths": [
                "projects/quant_research_system/phase4_search_loop/controller_batch_001_diversity_topup_review_20260509.md"
            ],
        },
        "created_at": "2026-05-09T00:00:00+00:00",
    },
    {
        "skill_name": "Time smoothing means causal smoothing",
        "skill_type": "failure_guardrail",
        "confidence": "medium",
        "status": "active",
        "pattern": "A signal/time_smoothing prompt produces a nonlinear magnitude dampener instead of rolling or EWM smoothing.",
        "strategy": "For time smoothing, use causal rolling, EWM, or lagged smoothing on the signal and keep the sign contract intact.",
        "prompt_rule": "Do not replace a time_smoothing target with magnitude dampening.",
        "applicability": {
            "source_stage": "controller_static",
            "data_stage": "stage_0_daily_stock",
            "target_surface": ["signal"],
        },
        "evidence": {
            "support_count": 1,
            "failure_count": 3,
            "artifact_paths": [
                "projects/quant_research_system/phase4_search_loop/controller_batch_001_diversity_topup_review_20260509.md"
            ],
        },
        "created_at": "2026-05-09T00:00:00+00:00",
    },
    {
        "skill_name": "Do not win by shrinking active days",
        "skill_type": "diagnostic_rule",
        "confidence": "high",
        "status": "active",
        "pattern": "A sample-evaluated child reports strong Sharpe but is active on only a few portfolio days.",
        "strategy": "Classify the result as a coverage artifact and require broad active-day coverage for sample_pass.",
        "prompt_rule": "Do not create sparse few-day books to improve metrics; keep the strategy active on most eligible sample dates.",
        "applicability": {
            "source_stage": ["controller_static", "remote_sample_eval"],
            "data_stage": "stage_0_daily_stock",
            "target_surface": ["signal", "ranking", "portfolio", "risk"],
        },
        "evidence": {
            "support_count": 1,
            "failure_count": 1,
            "artifact_paths": [
                "projects/quant_research_system/phase4_search_loop/remote_sample_eval_controller_batch_001_review_20260509.md"
            ],
        },
        "created_at": "2026-05-09T00:00:00+00:00",
    },
    {
        "skill_name": "Avoid metric-equivalent no-op children",
        "skill_type": "diagnostic_rule",
        "confidence": "high",
        "status": "active",
        "pattern": "A child changes code but the sample metrics are indistinguishable from the seed or parent.",
        "strategy": "Flag the child as functionally neutral and steer future prompts toward behavior changes that survive downstream controls.",
        "prompt_rule": "Do not propose cosmetic, monotone-invariant, or threshold-absorbed edits; make the intended behavior observable after ranking and risk controls.",
        "applicability": {
            "source_stage": ["controller_static", "remote_sample_eval"],
            "data_stage": "stage_0_daily_stock",
            "target_surface": ["signal", "ranking", "portfolio", "risk"],
        },
        "evidence": {
            "support_count": 1,
            "failure_count": 3,
            "artifact_paths": [
                "projects/quant_research_system/phase4_search_loop/remote_sample_eval_controller_batch_001_review_20260509.md"
            ],
        },
        "created_at": "2026-05-09T00:00:00+00:00",
    },
    {
        "skill_name": "No forward-return availability filters",
        "skill_type": "failure_guardrail",
        "confidence": "high",
        "status": "active",
        "pattern": "A repair for missing-held-weight is tempted to select names with known next-day returns.",
        "strategy": "Reject generated edits that use evaluator-only forward-return fields and repair missingness through ex-ante signal, ranking, portfolio, or risk logic.",
        "prompt_rule": "Do not use fwd_ret, fwd_date, fwd_vwretd, next_market_date, or one_day_forward in generated strategy edits.",
        "applicability": {
            "source_stage": ["controller_static", "remote_sample_eval"],
            "data_stage": "stage_0_daily_stock",
            "target_surface": ["signal", "ranking", "portfolio", "risk"],
        },
        "evidence": {
            "support_count": 1,
            "failure_count": 0,
            "artifact_paths": [
                "projects/quant_research_system/phase4_search_loop/remote_sample_eval_controller_batch_001_review_20260509.md"
            ],
        },
        "created_at": "2026-05-09T00:00:00+00:00",
    },
    {
        "skill_name": "Avoid single-diagnostic missing-held repairs",
        "skill_type": "avoid_strategy",
        "confidence": "avoid",
        "status": "active",
        "pattern": (
            "A sample_review repair improves max_missing_held_weight but worsens parent-relative performance "
            "or turnover-aware criteria."
        ),
        "strategy": (
            "Reject the idea as a narrow caveat fix unless it also preserves or improves parent-relative Sharpe, "
            "annualized return, turnover-aware score, coverage, and max-weight discipline."
        ),
        "prompt_rule": (
            "Do not optimize missing-held weight alone; the child must preserve parent-relative economics and "
            "turnover-aware quality."
        ),
        "applicability": {
            "source_stage": ["controller_static", "remote_sample_eval"],
            "data_stage": "stage_0_daily_stock",
            "target_surface": ["signal", "ranking", "portfolio", "risk"],
        },
        "evidence": {
            "support_count": 1,
            "failure_count": 1,
            "artifact_paths": [
                "projects/quant_research_system/phase4_search_loop/controller_attempt017_focused_round_review_20260511.md"
            ],
        },
        "created_at": "2026-05-11T00:00:00+00:00",
    },
    {
        "skill_name": "Avoid attempt017 generic signal dampening",
        "skill_type": "avoid_strategy",
        "confidence": "avoid",
        "status": "active",
        "pattern": (
            "A signal patch uses bounded_tanh_dampening, clipped_magnitude_dampening, or generic magnitude "
            "compression to repair missing-held weight."
        ),
        "strategy": (
            "Avoid generic signal compression for attempt017-style repair unless there is a specific mechanism "
            "that should preserve ranking economics after costs and turnover."
        ),
        "prompt_rule": (
            "Do not use bounded tanh, clipped magnitude, or simple signal shrinkage as a missing-held repair "
            "unless it should preserve parent-relative return and turnover-aware score."
        ),
        "applicability": {
            "source_stage": ["controller_static", "remote_sample_eval"],
            "data_stage": "stage_0_daily_stock",
            "target_surface": ["signal"],
        },
        "evidence": {
            "support_count": 1,
            "failure_count": 2,
            "artifact_paths": [
                "projects/quant_research_system/phase4_search_loop/controller_attempt017_focused_round_review_20260511.md"
            ],
        },
        "created_at": "2026-05-11T00:00:00+00:00",
    },
    {
        "skill_name": "Portfolio and risk edits must change final weights",
        "skill_type": "failure_guardrail",
        "confidence": "high",
        "status": "active",
        "pattern": (
            "Portfolio or risk patches pass syntax but are absorbed by selection, side normalization, or risk "
            "logic, producing behavioral_noop rejects."
        ),
        "strategy": (
            "Before emitting a patch, reason about whether the change survives downstream controls into final "
            "weights or portfolio-shape metrics."
        ),
        "prompt_rule": (
            "If a portfolio or risk edit is likely to leave final weights unchanged, output NO_VALID_PATCH."
        ),
        "applicability": {
            "source_stage": "controller_static",
            "data_stage": "stage_0_daily_stock",
            "target_surface": ["portfolio", "risk"],
        },
        "evidence": {
            "support_count": 1,
            "failure_count": 7,
            "artifact_paths": [
                "projects/quant_research_system/phase4_search_loop/controller_attempt017_focused_round_review_20260511.md"
            ],
        },
        "created_at": "2026-05-11T00:00:00+00:00",
    },
    {
        "skill_name": "Use panel.loc for extra daily-stock fields",
        "skill_type": "repair_pattern",
        "confidence": "high",
        "status": "active",
        "pattern": (
            "A ranking, portfolio, or risk mechanism patch reads CONTRACT fields from a local frame that "
            "does not contain those columns."
        ),
        "strategy": (
            "Use panel.loc[index, CONTRACT.field] aligned to the active group, valid set, long side, "
            "short side, or risk-control weight index."
        ),
        "prompt_rule": (
            "When the editable body's local data/group/valid frame lacks a daily_stock field, read it from "
            "panel.loc[...] with aligned index labels; never use CONTRACT.field[group.index]."
        ),
        "applicability": {
            "source_stage": "controller_static",
            "data_stage": "stage_0_daily_stock",
            "target_surface": ["ranking", "portfolio", "risk"],
        },
        "evidence": {
            "support_count": 1,
            "failure_count": 5,
            "artifact_paths": [
                "projects/quant_research_system/phase4_search_loop/controller_attempt017_mechanism_batch_review_20260514.md"
            ],
        },
        "created_at": "2026-05-14T00:00:00+00:00",
    },
    {
        "skill_name": "Avoid repeated attempt017 industry-neutral rank",
        "skill_type": "avoid_strategy",
        "confidence": "avoid",
        "status": "active",
        "pattern": (
            "Attempt017 ranking/industry_neutral_rank children repeat the attempt009 mechanism or "
            "sample metrics while weakening parent-relative return and Sharpe."
        ),
        "strategy": (
            "Prefer an underfilled non-industry-neutral mechanism cell. If industry_neutral_rank is "
            "proposed again, require occupied-MAP-cell elite improvement, material behavior difference, "
            "and prior-sample equivalence checks before sample evaluation."
        ),
        "prompt_rule": (
            "Do not use industry_neutral_rank as the main attempt017 mechanism after attempt009/attempt011; "
            "choose an underfilled non-industry-neutral cell unless the patch is explicitly different and "
            "prior sample equivalence is checked."
        ),
        "applicability": {
            "source_stage": ["controller_static", "remote_sample_eval"],
            "data_stage": "stage_0_daily_stock",
            "target_surface": ["ranking"],
        },
        "evidence": {
            "support_count": 1,
            "failure_count": 2,
            "artifact_paths": [
                "projects/quant_research_system/phase4_search_loop/remote_sample_eval_controller_attempt017_27b_card_batch_review_20260515.md"
            ],
        },
        "created_at": "2026-05-15T00:00:00+00:00",
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
    write_json(json_path, update)
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
