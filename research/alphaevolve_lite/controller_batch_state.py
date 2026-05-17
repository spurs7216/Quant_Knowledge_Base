"""Controller batch search-state helpers."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

from .controller_sample_eval_policy import controller_quality_score
from .diversity import DIVERSITY_TARGETS, DiversityTarget


@dataclass(frozen=True)
class ControllerTargetCell:
    """One exact surface/intent target requested by a controller batch caller."""

    surface: str
    target: DiversityTarget

    @property
    def cell_label(self) -> str:
        return self.target.cell_label

    @property
    def intent(self) -> str:
        return self.target.intent

    def to_cli_value(self) -> str:
        return f"{self.surface}/{self.intent}"


@dataclass
class ControllerSearchState:
    """Duplicate and MAP-cell state carried into a controller batch."""

    seen_child_hashes: dict[str, str] = field(default_factory=dict)
    seen_patch_fingerprints: dict[str, str] = field(default_factory=dict)
    occupied_map_cells: dict[str, str] = field(default_factory=dict)
    map_cell_elite_records: dict[str, dict[str, Any]] = field(default_factory=dict)
    occupied_target_labels_by_surface: dict[str, set[str]] = field(default_factory=dict)
    accepted_patches_by_surface: dict[str, list[str]] = field(default_factory=dict)
    prior_attempt_count: int = 0
    prior_pass_count: int = 0


def parse_surface_schedule(raw_schedule: str, *, available_surfaces: Iterable[str]) -> tuple[str, ...]:
    """Parse and validate a comma-separated target-surface schedule."""

    schedule = tuple(part.strip() for part in raw_schedule.split(",") if part.strip())
    if not schedule:
        raise ValueError("surface schedule must include at least one surface")
    available = set(available_surfaces)
    invalid = sorted(set(schedule) - available)
    if invalid:
        allowed = ", ".join(sorted(available))
        bad = ", ".join(invalid)
        raise ValueError(f"surface schedule contains unknown surfaces: {bad}; allowed: {allowed}")
    return schedule


def parse_target_cell_schedule(
    raw_schedule: str,
    *,
    available_surfaces: Iterable[str],
) -> tuple[ControllerTargetCell, ...]:
    """Parse exact ``surface/intent`` cells for deterministic controller targeting."""

    if not raw_schedule.strip():
        return ()

    available = set(available_surfaces)
    cells: list[ControllerTargetCell] = []
    for raw_part in raw_schedule.split(","):
        part = raw_part.strip()
        if not part:
            continue
        surface, intent = _split_target_cell(part)
        if surface not in available:
            allowed = ", ".join(sorted(available))
            raise ValueError(
                f"target-cell schedule contains unknown surface {surface!r}; allowed surfaces: {allowed}"
            )
        targets = DIVERSITY_TARGETS.get(surface)
        if not targets:
            raise ValueError(f"target-cell schedule cannot force intents for surface {surface!r}")
        target_by_intent = {target.intent: target for target in targets}
        try:
            target = target_by_intent[intent]
        except KeyError as exc:
            allowed = ", ".join(sorted(target_by_intent))
            raise ValueError(
                f"target-cell schedule contains unknown intent {intent!r} for surface {surface!r}; "
                f"allowed intents: {allowed}"
            ) from exc
        cells.append(ControllerTargetCell(surface=surface, target=target))
    if not cells:
        raise ValueError("target-cell schedule must include at least one surface/intent cell")
    return tuple(cells)


def target_cell_for_attempt(
    attempt_index: int,
    target_cell_schedule: tuple[ControllerTargetCell, ...],
) -> ControllerTargetCell:
    """Return the exact forced target cell for an attempt, cycling the schedule."""

    if not target_cell_schedule:
        raise ValueError("target-cell schedule must include at least one cell")
    return target_cell_schedule[attempt_index % len(target_cell_schedule)]


def _split_target_cell(raw_cell: str) -> tuple[str, str]:
    if "/" in raw_cell:
        surface, intent = raw_cell.split("/", 1)
    elif ":" in raw_cell:
        surface, intent = raw_cell.split(":", 1)
    else:
        raise ValueError(
            f"target-cell schedule item {raw_cell!r} must use surface/intent or surface:intent"
        )
    surface = surface.strip()
    intent = intent.strip()
    if not surface or not intent:
        raise ValueError(f"target-cell schedule item {raw_cell!r} has an empty surface or intent")
    return surface, intent


def load_prior_attempts(summary_paths: Iterable[str | Path]) -> list[dict[str, Any]]:
    """Load attempt records from prior controller summary files."""

    attempts: list[dict[str, Any]] = []
    for raw_path in summary_paths:
        if not raw_path:
            continue
        path = Path(raw_path)
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload, dict):
            records = payload.get("attempts", [])
        elif isinstance(payload, list):
            records = payload
        else:
            raise ValueError(f"unsupported prior summary payload in {path}")
        if not isinstance(records, list):
            raise ValueError(f"prior summary attempts must be a list in {path}")
        attempts.extend(item for item in records if isinstance(item, dict))
    return attempts


def seed_controller_search_state(prior_attempts: Iterable[dict[str, Any]]) -> ControllerSearchState:
    """Seed duplicate, MAP-cell, and negative-example state from prior attempts."""

    state = ControllerSearchState()
    for idx, attempt in enumerate(prior_attempts):
        state.prior_attempt_count += 1
        if attempt.get("decision") != "pass":
            continue
        state.prior_pass_count += 1
        program_id = str(attempt.get("program_id") or f"prior_pass_{idx:04d}")
        child_hash = attempt.get("child_sha256")
        if child_hash:
            state.seen_child_hashes.setdefault(str(child_hash), program_id)
        patch_fingerprint = attempt.get("patch_fingerprint")
        if patch_fingerprint:
            state.seen_patch_fingerprints.setdefault(str(patch_fingerprint), program_id)
        map_cell_key = attempt.get("map_cell_key")
        if map_cell_key:
            key = str(map_cell_key)
            current_elite = state.map_cell_elite_records.get(key)
            if current_elite is None or controller_quality_score(attempt) > controller_quality_score(current_elite):
                state.occupied_map_cells[key] = program_id
                state.map_cell_elite_records[key] = dict(attempt)

        surface = attempt.get("target_surface")
        patch_intent = attempt.get("patch_intent")
        if surface and patch_intent:
            state.occupied_target_labels_by_surface.setdefault(str(surface), set()).add(
                f"{surface}:{patch_intent}"
            )

        patch_text = _read_patch_text(attempt.get("final_diff_path"))
        if patch_text and surface:
            state.accepted_patches_by_surface.setdefault(str(surface), []).append(patch_text)
    return state


def _read_patch_text(raw_path: Any) -> str | None:
    if not raw_path:
        return None
    path = Path(str(raw_path))
    if not path.exists() or not path.is_file():
        return None
    return path.read_text(encoding="utf-8")


__all__ = [
    "ControllerSearchState",
    "ControllerTargetCell",
    "load_prior_attempts",
    "parse_surface_schedule",
    "parse_target_cell_schedule",
    "seed_controller_search_state",
    "target_cell_for_attempt",
]
