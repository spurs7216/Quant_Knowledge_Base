"""Mechanism-card helpers for medium-model search-state review."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import fields
from pathlib import Path
from typing import Any, Iterable

from .daily_stock_contract import DailyStockContract
from .diversity import DIVERSITY_TARGETS


MECHANISM_CARD_SCHEMA_VERSION = "phase4_mechanism_cards_v1"

VALID_MECHANISM_SURFACES = frozenset({"any", *DIVERSITY_TARGETS.keys()})
VALID_MECHANISM_INTENTS_BY_SURFACE = {
    surface: frozenset({"any", *(target.intent for target in targets)})
    for surface, targets in DIVERSITY_TARGETS.items()
}
VALID_MECHANISM_INTENTS_BY_SURFACE["any"] = frozenset(
    {"any", *(target.intent for targets in DIVERSITY_TARGETS.values() for target in targets)}
)
LOCAL_MECHANISM_DATA_FIELDS = frozenset(
    {
        "signal",
        "ranked_signal",
        "weight",
        "weights",
        "final_weight",
    }
)
CONTRACT_MECHANISM_DATA_FIELDS = frozenset(
    f"CONTRACT.{field.name}"
    for field in fields(DailyStockContract)
    if field.name not in {"contract_id", "evidence_path"}
)
ALLOWED_MECHANISM_DATA_FIELDS = frozenset(
    LOCAL_MECHANISM_DATA_FIELDS | CONTRACT_MECHANISM_DATA_FIELDS
)


def extract_json_object(text: str) -> dict[str, Any]:
    """Extract one JSON object from plain text or a fenced JSON response."""

    stripped = text.strip()
    fence = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", stripped, flags=re.DOTALL)
    if fence:
        stripped = fence.group(1).strip()
    try:
        payload = json.loads(stripped)
    except json.JSONDecodeError:
        start = stripped.find("{")
        end = stripped.rfind("}")
        if start < 0 or end <= start:
            raise
        payload = json.loads(stripped[start : end + 1])
    if not isinstance(payload, dict):
        raise ValueError("mechanism-card response must be a JSON object")
    return payload


def normalize_mechanism_card(card: dict[str, Any]) -> dict[str, Any]:
    """Return a stable mechanism-card record with required fields present."""

    surface = str(card.get("surface") or "").strip().lower()
    intent = str(card.get("intent") or "").strip().lower()
    thesis = _compact_text(card.get("thesis") or card.get("rationale") or "")
    if not surface or not intent or not thesis:
        raise ValueError("mechanism card requires surface, intent, and thesis")
    _validate_surface_intent(surface, intent)
    required_data_fields = _as_string_list(card.get("required_data_fields"))
    invalid_data_fields = sorted(set(required_data_fields) - ALLOWED_MECHANISM_DATA_FIELDS)
    if invalid_data_fields:
        allowed = ", ".join(sorted(ALLOWED_MECHANISM_DATA_FIELDS))
        bad = ", ".join(invalid_data_fields)
        raise ValueError(f"mechanism card uses unknown data fields: {bad}; allowed: {allowed}")
    record = {
        "card_id": str(card.get("card_id") or _stable_card_id(surface, intent, thesis)),
        "surface": surface,
        "intent": intent,
        "priority": _as_float(card.get("priority"), default=0.0),
        "status": str(card.get("status") or "active").strip().lower(),
        "thesis": thesis,
        "expected_effect": _compact_text(card.get("expected_effect")),
        "implementation_hints": _as_string_list(card.get("implementation_hints")),
        "required_data_fields": required_data_fields,
        "avoid": _as_string_list(card.get("avoid")),
        "sample_eval_hypothesis": _compact_text(card.get("sample_eval_hypothesis")),
        "evidence": card.get("evidence", {}) if isinstance(card.get("evidence", {}), dict) else {},
    }
    return record


def normalize_mechanism_cards(payload: dict[str, Any]) -> dict[str, Any]:
    """Normalize a mechanism-card JSON payload."""

    raw_cards = payload.get("cards", [])
    if not isinstance(raw_cards, list):
        raise ValueError("mechanism-card payload must contain a cards list")
    cards = [normalize_mechanism_card(item) for item in raw_cards if isinstance(item, dict)]
    return {
        "schema_version": MECHANISM_CARD_SCHEMA_VERSION,
        "cards": cards,
        "source_model": payload.get("source_model"),
        "review_summary": _compact_text(payload.get("review_summary")),
    }


def mechanism_card_contract_context() -> dict[str, Any]:
    """Return the exact surface, intent, and field vocabulary for card prompts."""

    return {
        "schema_version": MECHANISM_CARD_SCHEMA_VERSION,
        "allowed_surfaces": sorted(VALID_MECHANISM_SURFACES),
        "allowed_intents_by_surface": {
            surface: sorted(intents)
            for surface, intents in sorted(VALID_MECHANISM_INTENTS_BY_SURFACE.items())
        },
        "allowed_required_data_fields": sorted(ALLOWED_MECHANISM_DATA_FIELDS),
        "field_handle_rule": (
            "Use exact handles like CONTRACT.industry_primary and CONTRACT.dollar_volume, "
            "not loose names like industry_code, avg_daily_volume, returns_1d, or signal_raw."
        ),
    }


def read_mechanism_cards(path: str | Path) -> list[dict[str, Any]]:
    """Read normalized mechanism cards from a JSON artifact."""

    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(payload, list):
        payload = {"cards": payload}
    return normalize_mechanism_cards(payload)["cards"]


def select_mechanism_cards(
    cards: Iterable[dict[str, Any]],
    *,
    target_surface: str,
    target_intent: str,
    limit: int,
) -> list[dict[str, Any]]:
    """Select prompt cards relevant to the sampled surface and intent."""

    if limit <= 0:
        return []
    target_surface = target_surface.lower()
    target_intent = target_intent.lower()
    scored: list[tuple[float, str, dict[str, Any]]] = []
    for card in cards:
        record = normalize_mechanism_card(card)
        if record["status"] not in {"active", "candidate"}:
            continue
        score = record["priority"]
        if record["surface"] == target_surface:
            score += 3.0
        elif record["surface"] != "any":
            continue
        if record["intent"] == target_intent:
            score += 5.0
        elif record["intent"] != "any":
            score -= 0.5
        scored.append((score, record["card_id"], record))
    scored.sort(key=lambda item: (-item[0], item[1]))
    return [item for _, _, item in scored[:limit]]


def render_mechanism_cards(cards: Iterable[dict[str, Any]]) -> str:
    """Render mechanism cards as compact prompt text."""

    lines: list[str] = []
    for card in cards:
        record = normalize_mechanism_card(card)
        lines.append(
            f"- [{record['card_id']} | {record['surface']}/{record['intent']}] {record['thesis']}"
        )
        if record["expected_effect"]:
            lines.append(f"  expected_effect: {record['expected_effect']}")
        if record["required_data_fields"]:
            lines.append(f"  data_fields: {', '.join(record['required_data_fields'])}")
        if record["implementation_hints"]:
            lines.append(f"  hints: {'; '.join(record['implementation_hints'])}")
        if record["avoid"]:
            lines.append(f"  avoid: {'; '.join(record['avoid'])}")
        if record["sample_eval_hypothesis"]:
            lines.append(f"  sample_eval_hypothesis: {record['sample_eval_hypothesis']}")
    return "\n".join(lines) if lines else "None."


def mechanism_card_ids(cards: Iterable[dict[str, Any]]) -> list[str]:
    """Return stable card ids for selected cards."""

    return [normalize_mechanism_card(card)["card_id"] for card in cards]


def _stable_card_id(surface: str, intent: str, thesis: str) -> str:
    payload = f"{surface}|{intent}|{thesis}"
    return "mech_" + hashlib.sha256(payload.encode("utf-8")).hexdigest()[:12]


def _validate_surface_intent(surface: str, intent: str) -> None:
    if surface not in VALID_MECHANISM_SURFACES:
        allowed = ", ".join(sorted(VALID_MECHANISM_SURFACES))
        raise ValueError(f"mechanism card surface must be one of {allowed}; got {surface}")
    allowed_intents = VALID_MECHANISM_INTENTS_BY_SURFACE[surface]
    if intent not in allowed_intents:
        allowed = ", ".join(sorted(allowed_intents))
        raise ValueError(
            f"mechanism card intent for surface {surface} must be one of {allowed}; got {intent}"
        )


def _compact_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip())


def _as_string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [_compact_text(item) for item in value if _compact_text(item)]
    text = _compact_text(value)
    return [text] if text else []


def _as_float(value: Any, *, default: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


__all__ = [
    "ALLOWED_MECHANISM_DATA_FIELDS",
    "CONTRACT_MECHANISM_DATA_FIELDS",
    "LOCAL_MECHANISM_DATA_FIELDS",
    "MECHANISM_CARD_SCHEMA_VERSION",
    "VALID_MECHANISM_INTENTS_BY_SURFACE",
    "VALID_MECHANISM_SURFACES",
    "extract_json_object",
    "mechanism_card_contract_context",
    "mechanism_card_ids",
    "normalize_mechanism_cards",
    "read_mechanism_cards",
    "render_mechanism_cards",
    "select_mechanism_cards",
]
