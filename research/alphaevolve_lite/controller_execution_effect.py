"""Controller-local execution-effect checks.

Controller-static pass/fail proves that a generated child is syntactically safe
and respects basic portfolio invariants. It does not by itself prove that the
edit affects the tradable book. This module owns the narrower contract used to
detect edits that are absorbed before ranked signals, final weights, or exposure
shape change.
"""

from __future__ import annotations

import math
from typing import Any


EXECUTION_EFFECT_VERSION = "controller_execution_effect_v1"
EXECUTION_EFFECT_EPS = 1e-12


def execution_effect_from_attempt(attempt: dict[str, Any]) -> dict[str, Any]:
    """Return execution-effect diagnostics for one controller attempt."""

    return execution_effect_from_metrics(
        attempt.get("behavior_delta_metrics", {}) or {},
        target_surface=attempt.get("target_surface"),
    )


def execution_effect_from_metrics(
    metrics: dict[str, Any],
    *,
    target_surface: str | None = None,
) -> dict[str, Any]:
    """Classify whether a behavior delta survives to the relevant layer."""

    surface = str(target_surface or "").strip().lower()
    signal_delta = _positive(metrics.get("signal_max_abs_delta")) or _positive(
        metrics.get("signal_changed_fraction")
    )
    ranked_signal_delta = _positive(metrics.get("ranked_signal_max_abs_delta")) or _positive(
        metrics.get("ranked_signal_changed_fraction")
    )
    final_weight_delta = has_final_weight_effect(metrics)
    exposure_shape_delta = final_weight_delta or _positive(
        metrics.get("max_abs_gross_exposure_delta")
    ) or _positive(metrics.get("max_abs_net_exposure_delta"))

    reasons: list[str] = []
    if surface in {"signal", "ranking"} and not (ranked_signal_delta or final_weight_delta):
        reasons.append("ranked_signal_and_final_weights_unchanged")
    if surface in {"portfolio", "risk"} and not exposure_shape_delta:
        reasons.append("final_weights_and_exposure_shape_unchanged")

    return {
        "execution_effect_version": EXECUTION_EFFECT_VERSION,
        "target_surface": surface or None,
        "signal_delta": bool(signal_delta),
        "ranked_signal_delta": bool(ranked_signal_delta),
        "final_weight_delta": bool(final_weight_delta),
        "exposure_shape_delta": bool(exposure_shape_delta),
        "controller_execution_effective": not reasons,
        "execution_effect_reasons": reasons,
    }


def has_final_weight_effect(metrics: dict[str, Any]) -> bool:
    """Return true when final smoke-test weights or active names changed."""

    return (
        _positive(metrics.get("weight_max_abs_delta"))
        or _positive(metrics.get("weight_changed_fraction"))
        or _positive(metrics.get("active_position_symmetric_diff_count"))
    )


def _positive(value: Any) -> bool:
    number = _as_float(value)
    return number is not None and number > EXECUTION_EFFECT_EPS


def _as_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    return result if math.isfinite(result) else None


__all__ = [
    "EXECUTION_EFFECT_EPS",
    "EXECUTION_EFFECT_VERSION",
    "execution_effect_from_attempt",
    "execution_effect_from_metrics",
    "has_final_weight_effect",
]
