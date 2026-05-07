"""Prompt-side evidence retrieval for controller child batches."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from .diagnostic_analyzer import render_diagnostic_cards, retrieve_diagnostic_cards
from .reasoning_memory import render_memory_cards, retrieve_memory_items
from .skill_library import render_skill_cards, retrieve_skill_items


CONTROLLER_STATIC_STAGE = "controller_static"
STAGE_0_DAILY_STOCK = "stage_0_daily_stock"


@dataclass(frozen=True)
class PromptContext:
    """Retrieved prompt cards and rendered text for one target surface."""

    memory_query: str
    reasoning_memory_items: list[dict[str, Any]]
    reasoning_memory_item_ids: list[str]
    reasoning_memory_text: str
    diagnostic_cards: list[dict[str, Any]]
    diagnostic_card_ids: list[str]
    diagnostic_text: str
    skill_query: str
    skill_items: list[dict[str, Any]]
    skill_ids: list[str]
    skill_text: str


def build_controller_prompt_context(
    *,
    reasoning_memory_items: Iterable[dict[str, Any]],
    evaluator_diagnostic_cards: Iterable[dict[str, Any]],
    skill_items: Iterable[dict[str, Any]],
    target_surface: str,
    query_parts: Iterable[Any],
    memory_card_limit: int,
    diagnostic_card_limit: int,
    skill_card_limit: int,
    source_stage: str = CONTROLLER_STATIC_STAGE,
    data_stage: str = STAGE_0_DAILY_STOCK,
    include_diagnostic_card_ids_in_skill_query: bool = True,
) -> PromptContext:
    """Retrieve and render memory, diagnostic, and skill cards for a prompt."""

    memory_query = _join_query_parts(query_parts)
    retrieved_memory_items = retrieve_memory_items(
        reasoning_memory_items,
        source_stage=source_stage,
        target_surface=target_surface,
        data_stage=data_stage,
        query=memory_query,
        limit=max(0, memory_card_limit),
    )
    reasoning_memory_item_ids = _ids(retrieved_memory_items, "memory_item_id")
    reasoning_memory_text = render_memory_cards(retrieved_memory_items)

    diagnostic_cards = retrieve_diagnostic_cards(
        evaluator_diagnostic_cards,
        target_surface=target_surface,
        limit=max(0, diagnostic_card_limit),
    )
    diagnostic_card_ids = _ids(diagnostic_cards, "diagnostic_id")
    diagnostic_text = render_diagnostic_cards(diagnostic_cards)

    skill_query_parts: list[Any] = [memory_query, diagnostic_text]
    if include_diagnostic_card_ids_in_skill_query:
        skill_query_parts.append(" ".join(diagnostic_card_ids))
    skill_query = _join_query_parts(skill_query_parts)
    retrieved_skill_items = retrieve_skill_items(
        skill_items,
        source_stage=source_stage,
        target_surface=target_surface,
        data_stage=data_stage,
        query=skill_query,
        limit=max(0, skill_card_limit),
    )
    skill_ids = _ids(retrieved_skill_items, "skill_id")
    skill_text = render_skill_cards(retrieved_skill_items)

    return PromptContext(
        memory_query=memory_query,
        reasoning_memory_items=retrieved_memory_items,
        reasoning_memory_item_ids=reasoning_memory_item_ids,
        reasoning_memory_text=reasoning_memory_text,
        diagnostic_cards=diagnostic_cards,
        diagnostic_card_ids=diagnostic_card_ids,
        diagnostic_text=diagnostic_text,
        skill_query=skill_query,
        skill_items=retrieved_skill_items,
        skill_ids=skill_ids,
        skill_text=skill_text,
    )


def _join_query_parts(parts: Iterable[Any]) -> str:
    return " ".join(str(part) for part in parts if part is not None and str(part))


def _ids(items: Iterable[dict[str, Any]], key: str) -> list[str]:
    return [str(item.get(key)) for item in items if item.get(key)]


__all__ = [
    "CONTROLLER_STATIC_STAGE",
    "PromptContext",
    "STAGE_0_DAILY_STOCK",
    "build_controller_prompt_context",
]
