"""Remote-first control primitives for Phase 4 AlphaEvolve-lite."""

from .daily_stock_contract import CONTRACT, DailyStockContract
from .stage_names import CONTROLLER_STATIC, StageNameError, validate_stage_name

__all__ = [
    "CONTRACT",
    "CONTROLLER_STATIC",
    "DailyStockContract",
    "StageNameError",
    "validate_stage_name",
]
