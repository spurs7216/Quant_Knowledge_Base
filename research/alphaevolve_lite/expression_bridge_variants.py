"""Evaluator-side bridge variants for daily-stock expression portfolios."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Sequence

import pandas as pd

from .daily_stock_contract import CONTRACT, DailyStockContract
from .expression_evolution import ExpressionEvaluationConfig


@dataclass(frozen=True)
class BridgeVariantSpec:
    """One deterministic portfolio bridge variant used for diagnostics."""

    name: str
    kind: str
    parameter: float | int | None = None
    phase_offset: int = 0


def parse_bridge_variant_grid(value: str) -> list[BridgeVariantSpec]:
    """Parse a comma-separated bridge-variant grid."""

    items = [item.strip() for item in value.split(",") if item.strip()]
    if not items:
        raise ValueError("--bridge-variant-grid must include at least one variant")
    return [parse_bridge_variant(item) for item in items]


def parse_bridge_variant(value: str) -> BridgeVariantSpec:
    """Parse one bridge variant name."""

    if value == "daily":
        return BridgeVariantSpec(name=value, kind="daily")
    match = re.fullmatch(r"rebalance_([0-9]+)(?:_(?:offset|o)_?([0-9]+))?", value)
    if match:
        period = int(match.group(1))
        if period < 1:
            raise ValueError("rebalance period must be positive")
        phase_offset = int(match.group(2) or 0)
        if phase_offset < 0 or phase_offset >= period:
            raise ValueError("rebalance phase offset must satisfy 0 <= offset < period")
        return BridgeVariantSpec(
            name=value,
            kind="rebalance",
            parameter=period,
            phase_offset=phase_offset,
        )
    match = re.fullmatch(r"signal_decay_([0-9]+)", value)
    if match:
        period = int(match.group(1))
        if period < 1:
            raise ValueError("signal decay period must be positive")
        return BridgeVariantSpec(name=value, kind="signal_decay", parameter=period)
    match = re.fullmatch(r"no_trade_band_([0-9]+(?:\.[0-9]+)?)", value)
    if match:
        band = float(match.group(1))
        if band < 0:
            raise ValueError("no-trade band must be non-negative")
        return BridgeVariantSpec(name=value, kind="no_trade_band", parameter=band)
    raise ValueError(
        "unsupported bridge variant "
        f"{value!r}; expected daily, rebalance_N, rebalance_N_offset_M, "
        "signal_decay_N, or no_trade_band_X"
    )


def apply_bridge_variant(
    target_weights: pd.Series,
    panel: pd.DataFrame,
    *,
    variant: BridgeVariantSpec,
    config: ExpressionEvaluationConfig,
    contract: DailyStockContract = CONTRACT,
) -> pd.Series:
    """Apply a deterministic evaluator-side holding/turnover bridge variant."""

    if variant.kind == "daily":
        return target_weights.copy()

    output = pd.Series(0.0, index=target_weights.index, name=target_weights.name)
    previous_by_security = pd.Series(dtype=float)
    grouped_dates = panel[contract.date].groupby(panel[contract.date], sort=False).groups

    for date_index, idx in enumerate(grouped_dates.values()):
        securities = panel.loc[idx, contract.security_id]
        target_by_security = pd.Series(target_weights.loc[idx].to_numpy(), index=securities.to_numpy())
        previous = previous_by_security.reindex(target_by_security.index).fillna(0.0)
        if variant.kind == "rebalance":
            period = int(variant.parameter or 1)
            should_rebalance = date_index % period == variant.phase_offset
            raw = target_by_security if should_rebalance else previous
        elif variant.kind == "signal_decay":
            period = int(variant.parameter or 1)
            alpha = 1.0 / period
            raw = target_by_security if previous_by_security.empty else alpha * target_by_security + (1.0 - alpha) * previous
        elif variant.kind == "no_trade_band":
            band = float(variant.parameter or 0.0) * config.max_weight
            if previous_by_security.empty:
                raw = target_by_security
            else:
                rebalance = (target_by_security - previous).abs() >= band
                raw = target_by_security.where(rebalance, previous)
        else:  # pragma: no cover - parse_bridge_variant prevents this path.
            raise ValueError(f"unsupported bridge variant kind {variant.kind!r}")

        normalized = _normalize_daily_bridge_weights(raw, config=config)
        output.loc[idx] = normalized.reindex(target_by_security.index).fillna(0.0).to_numpy()
        previous_by_security = normalized[normalized != 0.0]

    return output


def bridge_variant_names(variants: Sequence[BridgeVariantSpec]) -> list[str]:
    return [variant.name for variant in variants]


def _normalize_daily_bridge_weights(
    weights_by_security: pd.Series,
    *,
    config: ExpressionEvaluationConfig,
) -> pd.Series:
    positive = weights_by_security[weights_by_security > 0.0]
    negative = weights_by_security[weights_by_security < 0.0]
    normalized = pd.Series(0.0, index=weights_by_security.index, dtype=float)
    if positive.empty or negative.empty:
        return normalized
    side_gross = min(
        config.gross_exposure / 2.0,
        len(positive) * config.max_weight,
        len(negative) * config.max_weight,
    )
    if side_gross <= 0.0:
        return normalized
    long_scaled = _scale_side(positive, side_gross, config.max_weight)
    short_scaled = _scale_side(negative.abs(), side_gross, config.max_weight)
    common_gross = min(float(long_scaled.sum()), float(short_scaled.sum()))
    if common_gross <= 0.0:
        return normalized
    normalized.loc[positive.index] = long_scaled / float(long_scaled.sum()) * common_gross
    normalized.loc[negative.index] = -short_scaled / float(short_scaled.sum()) * common_gross
    return normalized


def _scale_side(abs_weights: pd.Series, side_gross: float, max_weight: float) -> pd.Series:
    total = float(abs_weights.sum())
    if total <= 0.0:
        return pd.Series(0.0, index=abs_weights.index, dtype=float)
    scaled = abs_weights / total * side_gross
    return scaled.clip(upper=max_weight)


__all__ = [
    "BridgeVariantSpec",
    "apply_bridge_variant",
    "bridge_variant_names",
    "parse_bridge_variant",
    "parse_bridge_variant_grid",
]
