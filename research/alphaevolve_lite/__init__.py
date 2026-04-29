"""Remote-first control primitives for Phase 4 AlphaEvolve-lite."""

from .stage_names import CONTROLLER_STATIC, StageNameError, validate_stage_name

__all__ = [
    "CONTROLLER_STATIC",
    "StageNameError",
    "validate_stage_name",
]
