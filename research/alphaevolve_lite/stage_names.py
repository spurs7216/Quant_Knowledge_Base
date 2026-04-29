"""Canonical stage names for the Phase 4 AlphaEvolve-lite controller."""

from __future__ import annotations

from enum import StrEnum


class StageNameError(ValueError):
    """Raised when a controller stage name is ambiguous or unsupported."""


class StageName(StrEnum):
    """Supported controller stages for the preparation milestone."""

    CONTROLLER_STATIC = "controller_static"
    TOY_EVAL = "toy_eval"
    SAMPLE_EVAL = "sample_eval"
    FAST_HISTORICAL_EVAL = "fast_historical_eval"
    REMOTE_VALIDATION = "remote_validation"
    REVIEW = "review"


CONTROLLER_STATIC = StageName.CONTROLLER_STATIC.value
DEPRECATED_LOCAL_STATIC = "local_static"

ALLOWED_STAGE_NAMES = frozenset(stage.value for stage in StageName)


def validate_stage_name(stage: str) -> str:
    """Return a canonical stage name or raise a precise error."""

    normalized = stage.strip()
    if normalized == DEPRECATED_LOCAL_STATIC:
        raise StageNameError(
            "`local_static` is ambiguous. Use `controller_static` for controller-local static checks."
        )
    if normalized not in ALLOWED_STAGE_NAMES:
        allowed = ", ".join(sorted(ALLOWED_STAGE_NAMES))
        raise StageNameError(f"unsupported stage {stage!r}; allowed stages: {allowed}")
    return normalized
