"""Deterministic controller-static micro-filter for generated child patches."""

from __future__ import annotations

import ast
import math
from dataclasses import asdict, dataclass, field
from typing import Any

import numpy as np
import pandas as pd

from .daily_stock_contract import CONTRACT
from .diff_blocks import DiffBlockError, apply_search_replace, parse_search_replace_blocks
from .evolve_blocks import END_MARKER, START_MARKER, EvolveBlockError, find_evolve_blocks


FORBIDDEN_TEXT_PATTERNS = [
    "ib_insync",
    "IBKR",
    "TWS",
    "IB Gateway",
    "placeOrder",
    "reqPositions",
    "accountSummary",
    "order_submission",
    "broker_credentials",
    "yfinance",
    "pandas_datareader",
    "requests.get",
    "urllib.request.urlopen",
    "read_csv(",
    "to_csv(",
]


@dataclass
class MicroFilterResult:
    """Serializable result for one generated patch."""

    decision: str
    hard_gates: dict[str, bool] = field(default_factory=dict)
    failure_category: str | None = None
    failure_reason: str | None = None
    parsed_block_count: int = 0
    child_text: str | None = None
    vector_smoke_metrics: dict[str, float] = field(default_factory=dict)

    def to_record(self) -> dict[str, Any]:
        payload = asdict(self)
        if self.child_text is not None:
            payload["child_text_length"] = len(self.child_text)
            payload.pop("child_text", None)
        return payload


def _fail(
    gates: dict[str, bool],
    *,
    category: str,
    reason: str,
    parsed_block_count: int = 0,
) -> MicroFilterResult:
    return MicroFilterResult(
        decision="reject",
        hard_gates=gates,
        failure_category=category,
        failure_reason=reason,
        parsed_block_count=parsed_block_count,
    )


def _search_blocks_inside_evolve_blocks(parent_text: str, diff_text: str) -> tuple[bool, str | None]:
    blocks = parse_search_replace_blocks(diff_text)
    evolve_blocks = find_evolve_blocks(parent_text)
    for block in blocks:
        if START_MARKER in block.search or END_MARKER in block.search:
            return False, "SEARCH block includes EVOLVE marker"
        if not any(block.search in evolve.text for evolve in evolve_blocks):
            return False, "SEARCH block is not strictly inside an EVOLVE block"
    return True, None


def _import_nodes(program_text: str) -> set[str]:
    tree = ast.parse(program_text)
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            imports.add(module)
    return imports


def _new_imports(parent_text: str, child_text: str) -> set[str]:
    return _import_nodes(child_text) - _import_nodes(parent_text)


def _contains_forbidden_pattern(child_text: str) -> str | None:
    lowered = child_text.lower()
    for pattern in FORBIDDEN_TEXT_PATTERNS:
        if pattern.lower() in lowered:
            return pattern
    return None


def _make_smoke_panel() -> pd.DataFrame:
    rng = np.random.default_rng(123)
    dates = pd.bdate_range("2020-01-01", periods=90)
    rows: list[dict[str, Any]] = []
    for idx, permno in enumerate(range(10001, 10041)):
        cap = 1_000_000.0 + idx * 20_000.0
        price = 20.0 + idx * 0.5
        for pos, date in enumerate(dates):
            ret = float(rng.normal(0.0001, 0.01))
            price = max(1.0, price * (1.0 + ret))
            volume = float(50_000 + (idx + pos) * 100)
            rows.append(
                {
                    CONTRACT.security_id: permno,
                    CONTRACT.issuer_id: permno + 1000,
                    CONTRACT.date: date,
                    CONTRACT.total_return: ret,
                    CONTRACT.ex_dividend_return: ret,
                    CONTRACT.price: price,
                    CONTRACT.volume: volume,
                    CONTRACT.dollar_volume: price * volume,
                    CONTRACT.market_cap: cap * (1.0 + pos * 0.0001),
                    CONTRACT.shares_outstanding: cap / price,
                    CONTRACT.exchange: "N",
                    CONTRACT.security_type: "EQTY",
                    CONTRACT.share_type: "NS",
                    CONTRACT.trading_status: "A",
                    CONTRACT.conditional_type: "RW",
                    CONTRACT.us_incorporated: "Y",
                    CONTRACT.industry_primary: 3500,
                    CONTRACT.benchmark_return_primary: float(rng.normal(0.0001, 0.008)),
                    CONTRACT.benchmark_return_secondary: float(rng.normal(0.0001, 0.008)),
                    "fwd_ret": float(rng.normal(0.0001, 0.01)),
                }
            )
    return pd.DataFrame(rows)


def _vector_smoke(child_text: str) -> dict[str, float]:
    namespace: dict[str, Any] = {"__name__": "_alphaevolve_child_smoke", "__file__": "<child>"}
    exec(compile(child_text, "<child>", "exec"), namespace)
    panel = _make_smoke_panel()
    params = dict(namespace["DEFAULT_PARAMS"])
    signal = namespace["compute_signal"](panel, params)
    ranked = namespace["rank_or_transform_signal"](signal, panel, params)
    weights = namespace["construct_portfolio"](ranked, panel, params)
    weights = namespace["apply_risk_controls"](weights, panel, params)
    metrics = namespace["evaluate"]({"panel": panel, "params": params})

    for name, series in {"signal": signal, "ranked": ranked, "weights": weights}.items():
        if len(series) != len(panel):
            raise ValueError(f"{name} length mismatch: {len(series)} != {len(panel)}")
    finite_weights = pd.to_numeric(weights, errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
    if finite_weights.empty:
        raise ValueError("weights are all nonfinite")
    max_weight = float(finite_weights.abs().max())
    if max_weight > 1.0:
        raise ValueError(f"max smoke-test weight too large: {max_weight}")

    output = {
        "max_weight": max_weight,
        "nonzero_weight_count": float(finite_weights.ne(0.0).sum()),
        "mean_abs_weight": float(finite_weights.abs().mean()),
    }
    for key, value in metrics.items():
        if isinstance(value, (int, float)) and math.isfinite(float(value)):
            output[f"eval_{key}"] = float(value)
    return output


def run_micro_filter(parent_text: str, generated_text: str) -> MicroFilterResult:
    """Apply deterministic controller-static checks to one generated patch."""

    gates = {
        "nonempty_output": False,
        "not_no_valid_patch": False,
        "parse_search_replace": False,
        "exact_search_match": False,
        "evolve_block_safe": False,
        "apply_patch": False,
        "evolve_markers_preserved": False,
        "forbidden_pattern_pass": False,
        "no_new_imports": False,
        "compile_pass": False,
        "vector_smoke_pass": False,
    }
    text = generated_text.strip()
    if not text:
        return _fail(gates, category="empty_output", reason="model returned empty output")
    gates["nonempty_output"] = True
    if text == "NO_VALID_PATCH":
        return _fail(gates, category="no_valid_patch", reason="model declined to provide a patch")
    gates["not_no_valid_patch"] = True

    try:
        blocks = parse_search_replace_blocks(generated_text)
    except DiffBlockError as exc:
        return _fail(gates, category="malformed_search_replace", reason=str(exc))
    parsed_count = len(blocks)
    gates["parse_search_replace"] = True

    exact_counts = [parent_text.count(block.search) for block in blocks]
    if any(count != 1 for count in exact_counts):
        return _fail(
            gates,
            category="exact_search_not_found",
            reason=f"SEARCH match counts were {exact_counts}",
            parsed_block_count=parsed_count,
        )
    gates["exact_search_match"] = True

    try:
        safe, reason = _search_blocks_inside_evolve_blocks(parent_text, generated_text)
    except (DiffBlockError, EvolveBlockError) as exc:
        return _fail(gates, category="outside_evolve_block", reason=str(exc), parsed_block_count=parsed_count)
    if not safe:
        return _fail(gates, category="outside_evolve_block", reason=reason or "", parsed_block_count=parsed_count)
    gates["evolve_block_safe"] = True

    try:
        child_text = apply_search_replace(parent_text, generated_text)
    except DiffBlockError as exc:
        return _fail(gates, category="apply_failed", reason=str(exc), parsed_block_count=parsed_count)
    gates["apply_patch"] = True

    try:
        parent_blocks = find_evolve_blocks(parent_text)
        child_blocks = find_evolve_blocks(child_text)
    except EvolveBlockError as exc:
        return _fail(gates, category="evolve_marker_error", reason=str(exc), parsed_block_count=parsed_count)
    if len(parent_blocks) != len(child_blocks):
        return _fail(
            gates,
            category="evolve_marker_error",
            reason=f"evolve block count changed: {len(parent_blocks)} -> {len(child_blocks)}",
            parsed_block_count=parsed_count,
        )
    gates["evolve_markers_preserved"] = True

    forbidden = _contains_forbidden_pattern(child_text)
    if forbidden:
        return _fail(
            gates,
            category="forbidden_policy_edit",
            reason=f"forbidden pattern introduced or present: {forbidden}",
            parsed_block_count=parsed_count,
        )
    gates["forbidden_pattern_pass"] = True

    try:
        imports = _new_imports(parent_text, child_text)
    except SyntaxError as exc:
        return _fail(gates, category="compile_failed", reason=str(exc), parsed_block_count=parsed_count)
    if imports:
        return _fail(
            gates,
            category="introduced_new_import",
            reason=f"new imports are not allowed: {sorted(imports)}",
            parsed_block_count=parsed_count,
        )
    gates["no_new_imports"] = True

    try:
        compile(child_text, "<child>", "exec")
    except SyntaxError as exc:
        return _fail(gates, category="compile_failed", reason=str(exc), parsed_block_count=parsed_count)
    gates["compile_pass"] = True

    try:
        smoke_metrics = _vector_smoke(child_text)
    except Exception as exc:
        return _fail(gates, category="vector_smoke_failed", reason=str(exc), parsed_block_count=parsed_count)
    gates["vector_smoke_pass"] = True

    return MicroFilterResult(
        decision="pass",
        hard_gates=gates,
        parsed_block_count=parsed_count,
        child_text=child_text,
        vector_smoke_metrics=smoke_metrics,
    )


__all__ = ["MicroFilterResult", "run_micro_filter"]
