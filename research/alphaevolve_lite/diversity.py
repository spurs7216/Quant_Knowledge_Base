"""Controller-stage diversity helpers inspired by MAP-Elites.

The first controller batch does not have historical fitness yet, so these
helpers build a lightweight behavior map from patch intent and smoke-test
portfolio-shape metrics. Later remote evaluations can replace the local score
with real selection scores while keeping the same cell vocabulary.
"""

from __future__ import annotations

import hashlib
import re
from collections import Counter
from dataclasses import dataclass
from typing import Any

from .diff_blocks import DiffBlockError, parse_search_replace_blocks


@dataclass(frozen=True)
class DiversityTarget:
    """One intended behavior cell for the prompt sampler to target."""

    cell_label: str
    intent: str
    instruction: str


DIVERSITY_TARGETS: dict[str, tuple[DiversityTarget, ...]] = {
    "signal": (
        DiversityTarget(
            "signal:direction_flip",
            "direction_flip",
            "Test the sign-flipped innovation direction while preserving volatility scaling.",
        ),
        DiversityTarget(
            "signal:bounded_tanh_dampening",
            "bounded_tanh_dampening",
            "Use a bounded nonlinear dampener that reduces extreme innovation magnitudes.",
        ),
        DiversityTarget(
            "signal:clipped_magnitude_dampening",
            "clipped_magnitude_dampening",
            "Clip or winsorize signal magnitudes without changing sign direction.",
        ),
        DiversityTarget(
            "signal:history_confidence_weighting",
            "history_confidence_weighting",
            "Weight signals by causal history length or early-history confidence.",
        ),
        DiversityTarget(
            "signal:volatility_floor_or_scaling",
            "volatility_floor_or_scaling",
            "Change the volatility denominator, floor, or scaling shape causally.",
        ),
        DiversityTarget(
            "signal:time_smoothing",
            "time_smoothing",
            "Smooth the per-security signal causally with rolling or exponentially weighted logic.",
        ),
    ),
    "ranking": (
        DiversityTarget(
            "ranking:direction_flip",
            "direction_flip",
            "Flip the cross-sectional ranked direction without changing portfolio construction.",
        ),
        DiversityTarget(
            "ranking:winsorization_quantile_change",
            "winsorization_quantile_change",
            "Change robust cross-sectional clipping or winsorization quantiles.",
        ),
        DiversityTarget(
            "ranking:robust_center_scale",
            "robust_center_scale",
            "Use robust center and scale such as median/MAD-style logic.",
        ),
        DiversityTarget(
            "ranking:rank_transform",
            "rank_transform",
            "Convert scores to cross-sectional ranks or percentile ranks before scaling.",
        ),
        DiversityTarget(
            "ranking:shrinkage_transform",
            "shrinkage_transform",
            "Shrink weak cross-sectional signals toward zero while preserving order.",
        ),
    ),
    "portfolio": (
        DiversityTarget(
            "portfolio:selection_threshold_change",
            "selection_threshold_change",
            "Change long/short quantile thresholds while preserving both books.",
        ),
        DiversityTarget(
            "portfolio:equal_side_weight_refactor",
            "equal_side_weight_refactor",
            "Refactor equal long/short side weights without changing exposure targets.",
        ),
        DiversityTarget(
            "portfolio:signal_weighted_sides",
            "signal_weighted_sides",
            "Use positive signal magnitudes separately on long and short sides.",
        ),
        DiversityTarget(
            "portfolio:gross_exposure_control",
            "gross_exposure_control",
            "Use conservative gross exposure logic inside the portfolio block.",
        ),
        DiversityTarget(
            "portfolio:no_trade_band_or_sparsity",
            "no_trade_band_or_sparsity",
            "Reduce marginal positions using a band or sparse selection rule.",
        ),
    ),
    "risk": (
        DiversityTarget(
            "risk:max_weight_tightening",
            "max_weight_tightening",
            "Tighten effective max-weight or cap handling conservatively.",
        ),
        DiversityTarget(
            "risk:side_renormalization",
            "side_renormalization",
            "Improve separate long-side and short-side normalization.",
        ),
        DiversityTarget(
            "risk:small_book_guard",
            "small_book_guard",
            "Handle days with too few longs or shorts conservatively.",
        ),
        DiversityTarget(
            "risk:exposure_dampening",
            "exposure_dampening",
            "Dampen exposure after caps while keeping net exposure near zero.",
        ),
        DiversityTarget(
            "risk:cap_shape_change",
            "cap_shape_change",
            "Change clip/cap shape without weakening max-weight safety.",
        ),
    ),
}


def choose_diversity_target(
    surface: str,
    attempt_index: int,
    *,
    occupied_labels: set[str] | None = None,
) -> DiversityTarget:
    """Choose the first unoccupied target cell in a deterministic rotation."""

    targets = DIVERSITY_TARGETS.get(surface)
    if not targets:
        return DiversityTarget(f"{surface}:other", "other", "Make a safe, distinct change on this surface.")

    occupied = occupied_labels or set()
    start = attempt_index % len(targets)
    for offset in range(len(targets)):
        target = targets[(start + offset) % len(targets)]
        if target.cell_label not in occupied:
            return target
    return targets[start]


def format_diversity_target(target: DiversityTarget | None) -> str:
    if target is None:
        return "No explicit target cell supplied."
    lines = [
        f"cell_label: {target.cell_label}",
        f"intended_patch_intent: {target.intent}",
        f"instruction: {target.instruction}",
        "intent_contract:",
        "- Implement this intended_patch_intent, not a different easier intent.",
        "- A controller-safe patch that lands in an already occupied intent is still a failed search step.",
    ]
    if target.intent == "direction_flip":
        lines.append("- Because direction_flip is requested, make the sign or ranking direction change explicit.")
    else:
        lines.append("- Do not use a sign or direction flip as the main change for this target.")
    return "\n".join(lines)


def _replacement_text(diff_text: str) -> str:
    try:
        return "\n".join(block.replace for block in parse_search_replace_blocks(diff_text))
    except DiffBlockError:
        return diff_text


def _normalized_code(text: str) -> str:
    lines: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if line:
            lines.append(re.sub(r"\s+", " ", line))
    return "\n".join(lines)


def _changed_replacement_text(diff_text: str) -> str:
    """Return normalized replacement lines that are not copied from SEARCH."""

    try:
        blocks = parse_search_replace_blocks(diff_text)
    except DiffBlockError:
        return _normalized_code(diff_text)

    changed_lines: list[str] = []
    for block in blocks:
        search_counts = Counter(_normalized_code(block.search).splitlines())
        replacement_lines = _normalized_code(block.replace).splitlines()
        block_changed: list[str] = []
        for line in replacement_lines:
            if search_counts[line] > 0:
                search_counts[line] -= 1
            else:
                block_changed.append(line)
        changed_lines.extend(block_changed)
    return "\n".join(changed_lines)


def patch_fingerprint(diff_text: str) -> str:
    """Hash the normalized replacement code for semantic duplicate detection."""

    normalized = _normalized_code(_replacement_text(diff_text))
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def classify_patch_intent(diff_text: str, target_surface: str) -> str:
    """Classify a patch into a coarse behavior cell descriptor."""

    replace = _changed_replacement_text(diff_text) or _normalized_code(_replacement_text(diff_text))
    lower = replace.lower()
    compact = re.sub(r"\s+", "", lower)

    if target_surface == "signal":
        if "signal=-" in compact or "signal=-signal" in compact:
            return "direction_flip"
        if "rolling(" in lower or "ewm(" in lower or ".shift(" in lower:
            return "time_smoothing"
        if "history" in lower or "min_history" in lower:
            return "history_confidence_weighting"
        if "rolling_vol" in lower or "clip(lower=" in lower:
            return "volatility_floor_or_scaling"
        if "tanh" in lower:
            return "bounded_tanh_dampening"
        if "np.sign" in lower or "sign(" in lower or "minimum(" in lower:
            return "clipped_magnitude_dampening"
        return "signal_other"

    if target_surface == "ranking":
        if "return-" in compact or "return-demeaned" in compact:
            return "direction_flip"
        if "quantile" in lower:
            return "winsorization_quantile_change"
        if "median" in lower or "mad" in lower:
            return "robust_center_scale"
        if ".rank(" in lower or "pct=true" in compact:
            return "rank_transform"
        if "clip" in lower or "where" in lower or "shrink" in lower or "scale+" in compact:
            return "shrinkage_transform"
        return "ranking_other"

    if target_surface == "portfolio":
        if "long_quantile" in lower or "short_quantile" in lower or "quantile" in lower:
            return "selection_threshold_change"
        if "band" in lower or "sparse" in lower or "threshold" in lower or "=0.0" in compact:
            return "no_trade_band_or_sparsity"
        if "abs()" in lower and "weights.loc[shorts]" in lower:
            return "signal_weighted_sides"
        if "damp" in lower or "gross=" in compact:
            return "gross_exposure_control"
        if "long_weight" in lower or "short_weight" in lower or "base_weight" in lower:
            return "equal_side_weight_refactor"
        if "gross" in lower:
            return "gross_exposure_control"
        return "portfolio_other"

    if target_surface == "risk":
        if "max_weight" in lower and ("*" in lower or "min(" in lower or "max(" in lower):
            return "max_weight_tightening"
        if "len(" in lower:
            return "small_book_guard"
        if "damp" in lower or "0.5" in lower:
            return "exposure_dampening"
        if "clip" in lower:
            return "cap_shape_change"
        if "long_sum" in lower or "short_sum" in lower:
            return "side_renormalization"
        return "risk_other"

    return f"{target_surface}_other"


def _bucket(value: float | int | None, cuts: tuple[float, float], labels: tuple[str, str, str]) -> str:
    if value is None:
        return "unknown"
    try:
        x = float(value)
    except (TypeError, ValueError):
        return "unknown"
    if x != x:
        return "unknown"
    if x <= cuts[0]:
        return labels[0]
    if x <= cuts[1]:
        return labels[1]
    return labels[2]


def portfolio_shape_buckets(metrics: dict[str, Any]) -> dict[str, str]:
    return {
        "net_exposure_bucket": _bucket(
            metrics.get("max_abs_net_exposure"),
            (0.02, 0.06),
            ("balanced", "near_balanced", "imbalanced"),
        ),
        "gross_exposure_bucket": _bucket(
            metrics.get("max_gross_exposure"),
            (0.75, 1.05),
            ("low_gross", "normal_gross", "high_gross"),
        ),
        "concentration_bucket": _bucket(
            metrics.get("max_weight"),
            (0.015, 0.025),
            ("low_concentration", "normal_concentration", "high_concentration"),
        ),
        "book_activity_bucket": _bucket(
            min(
                float(metrics.get("min_long_count_active_day", 0.0) or 0.0),
                float(metrics.get("min_short_count_active_day", 0.0) or 0.0),
            ),
            (3.0, 10.0),
            ("thin_book", "medium_book", "broad_book"),
        ),
    }


def behavior_delta_buckets(metrics: dict[str, Any] | None) -> dict[str, str]:
    metrics = metrics or {}
    return {
        "portfolio_delta_bucket": _bucket(
            metrics.get("weight_max_abs_delta"),
            (1e-12, 0.002),
            ("no_portfolio_delta", "small_portfolio_delta", "material_portfolio_delta"),
        ),
        "rank_delta_bucket": _bucket(
            metrics.get("ranked_signal_max_abs_delta"),
            (1e-12, 0.05),
            ("no_rank_delta", "small_rank_delta", "material_rank_delta"),
        ),
        "gross_delta_bucket": _bucket(
            metrics.get("max_abs_gross_exposure_delta"),
            (1e-12, 0.05),
            ("no_gross_delta", "small_gross_delta", "material_gross_delta"),
        ),
    }


def map_cell_key(
    target_surface: str,
    intent: str,
    metrics: dict[str, Any],
    behavior_delta_metrics: dict[str, Any] | None = None,
) -> str:
    buckets = portfolio_shape_buckets(metrics)
    delta_buckets = behavior_delta_buckets(behavior_delta_metrics)
    parts = {
        "surface": target_surface,
        "intent": intent,
        **buckets,
        **delta_buckets,
    }
    return "|".join(f"{key}={parts[key]}" for key in sorted(parts))


def patch_diversity_descriptor(
    diff_text: str,
    target_surface: str,
    metrics: dict[str, Any],
    behavior_delta_metrics: dict[str, Any] | None = None,
) -> dict[str, str]:
    intent = classify_patch_intent(diff_text, target_surface)
    buckets = portfolio_shape_buckets(metrics)
    delta_buckets = behavior_delta_buckets(behavior_delta_metrics)
    return {
        "patch_intent": intent,
        "patch_fingerprint": patch_fingerprint(diff_text),
        "map_cell_key": map_cell_key(target_surface, intent, metrics, behavior_delta_metrics),
        **buckets,
        **delta_buckets,
    }


__all__ = [
    "DIVERSITY_TARGETS",
    "DiversityTarget",
    "behavior_delta_buckets",
    "choose_diversity_target",
    "classify_patch_intent",
    "format_diversity_target",
    "map_cell_key",
    "patch_diversity_descriptor",
    "patch_fingerprint",
    "portfolio_shape_buckets",
]
