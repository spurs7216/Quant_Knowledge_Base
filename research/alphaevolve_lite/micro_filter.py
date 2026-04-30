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


class PortfolioSemanticError(ValueError):
    """Raised when a child compiles but violates portfolio-shape invariants."""

    def __init__(self, reason: str, metrics: dict[str, float]) -> None:
        super().__init__(reason)
        self.metrics = metrics


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
    vector_smoke_metrics: dict[str, float] | None = None,
) -> MicroFilterResult:
    return MicroFilterResult(
        decision="reject",
        hard_gates=gates,
        failure_category=category,
        failure_reason=reason,
        parsed_block_count=parsed_block_count,
        vector_smoke_metrics=vector_smoke_metrics or {},
    )


def _named_evolve_block_bodies(parent_text: str) -> dict[str, str]:
    lines = parent_text.splitlines(keepends=True)
    bodies: dict[str, str] = {}
    current_name: str | None = None
    current_body: list[str] = []
    unnamed_count = 0
    for line in lines:
        if START_MARKER in line:
            suffix = line.split(START_MARKER, 1)[1].strip()
            if suffix.startswith(":"):
                current_name = suffix[1:].strip() or f"unnamed_{unnamed_count}"
            else:
                current_name = f"unnamed_{unnamed_count}"
            unnamed_count += 1
            current_body = []
            continue
        if END_MARKER in line and current_name is not None:
            bodies[current_name] = "".join(current_body)
            current_name = None
            current_body = []
            continue
        if current_name is not None:
            current_body.append(line)
    return bodies


def _search_blocks_inside_evolve_blocks(
    parent_text: str,
    diff_text: str,
    *,
    target_surface: str | None = None,
) -> tuple[bool, str | None]:
    blocks = parse_search_replace_blocks(diff_text)
    if target_surface:
        named_bodies = _named_evolve_block_bodies(parent_text)
        target_body = named_bodies.get(target_surface)
        if target_body is None:
            allowed = ", ".join(sorted(named_bodies))
            return False, f"target EVOLVE block {target_surface!r} not found; allowed: {allowed}"
        allowed_bodies = [target_body]
    else:
        allowed_bodies = [evolve.text for evolve in find_evolve_blocks(parent_text)]
    for block in blocks:
        if START_MARKER in block.search or END_MARKER in block.search:
            return False, "SEARCH block includes EVOLVE marker"
        if not any(block.search in body for body in allowed_bodies):
            if target_surface:
                return False, f"SEARCH block is not strictly inside target EVOLVE block {target_surface!r}"
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
    configured_max_weight = float(params.get("max_weight", 0.02))
    max_weight_limit = min(0.05, max(configured_max_weight, 0.0) + 1e-12)
    if max_weight > max_weight_limit:
        raise ValueError(f"max smoke-test weight too large: {max_weight} > {max_weight_limit}")

    ranked_numeric = pd.to_numeric(ranked.reindex(panel.index), errors="coerce")
    weight_numeric = pd.to_numeric(weights.reindex(panel.index), errors="coerce").fillna(0.0)
    smoke_frame = pd.DataFrame(
        {
            "date": panel[CONTRACT.date].to_numpy(),
            "ranked_signal": ranked_numeric.to_numpy(dtype=float),
            "weight": weight_numeric.to_numpy(dtype=float),
        },
        index=panel.index,
    )
    eps = 1e-12
    by_date = smoke_frame.groupby("date", sort=True)
    gross_by_date = by_date["weight"].apply(lambda s: float(s.abs().sum()))
    active_dates = gross_by_date[gross_by_date > eps].index
    if len(active_dates) == 0:
        raise ValueError("weights are all zero")

    net_by_date = by_date["weight"].sum().reindex(active_dates)
    long_count_by_date = by_date["weight"].apply(lambda s: int((s > eps).sum())).reindex(active_dates)
    short_count_by_date = by_date["weight"].apply(lambda s: int((s < -eps).sum())).reindex(active_dates)
    long_sum_by_date = by_date["weight"].apply(lambda s: float(s[s > eps].sum())).reindex(active_dates)
    short_sum_by_date = by_date["weight"].apply(lambda s: float(-s[s < -eps].sum())).reindex(active_dates)
    active = smoke_frame["weight"].abs() > eps
    sign_bad = active & (
        ((smoke_frame["weight"] > eps) & (smoke_frame["ranked_signal"] < -eps))
        | ((smoke_frame["weight"] < -eps) & (smoke_frame["ranked_signal"] > eps))
    )

    output = {
        "max_weight": max_weight,
        "nonzero_weight_count": float(finite_weights.ne(0.0).sum()),
        "mean_abs_weight": float(finite_weights.abs().mean()),
        "active_day_count": float(len(active_dates)),
        "mean_gross_exposure": float(gross_by_date.reindex(active_dates).mean()),
        "max_gross_exposure": float(gross_by_date.max()),
        "mean_net_exposure": float(net_by_date.mean()),
        "max_abs_net_exposure": float(net_by_date.abs().max()),
        "min_long_count_active_day": float(long_count_by_date.min()),
        "min_short_count_active_day": float(short_count_by_date.min()),
        "mean_long_exposure": float(long_sum_by_date.mean()),
        "mean_short_exposure": float(short_sum_by_date.mean()),
        "side_sign_bad_count": float(sign_bad.sum()),
        "side_sign_bad_weight": float(smoke_frame.loc[sign_bad, "weight"].abs().sum()),
    }
    for key, value in metrics.items():
        if isinstance(value, (int, float)) and math.isfinite(float(value)):
            output[f"eval_{key}"] = float(value)

    gross_limit = float(params.get("gross_exposure", 1.0)) * 1.05 + 1e-12
    net_limit = max(0.05, 0.10 * output["max_gross_exposure"])
    if output["max_gross_exposure"] > gross_limit:
        raise PortfolioSemanticError(
            f"gross exposure too large: {output['max_gross_exposure']} > {gross_limit}",
            output,
        )
    if output["max_abs_net_exposure"] > net_limit:
        raise PortfolioSemanticError(
            f"net exposure too large: {output['max_abs_net_exposure']} > {net_limit}",
            output,
        )
    if output["min_long_count_active_day"] <= 0 or output["min_short_count_active_day"] <= 0:
        raise PortfolioSemanticError("active days must contain both long and short weights", output)
    if output["side_sign_bad_count"] > 0 and output["side_sign_bad_weight"] > 1e-9:
        raise PortfolioSemanticError(
            f"weights disagree with ranked signal sign for {output['side_sign_bad_count']} rows",
            output,
        )
    return output


def run_micro_filter(
    parent_text: str,
    generated_text: str,
    *,
    target_surface: str | None = None,
) -> MicroFilterResult:
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
        "portfolio_semantic_pass": False,
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
        safe, reason = _search_blocks_inside_evolve_blocks(
            parent_text,
            generated_text,
            target_surface=target_surface,
        )
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
    except PortfolioSemanticError as exc:
        gates["vector_smoke_pass"] = True
        return _fail(
            gates,
            category="portfolio_semantic_failed",
            reason=str(exc),
            parsed_block_count=parsed_count,
            vector_smoke_metrics=exc.metrics,
        )
    except Exception as exc:
        return _fail(gates, category="vector_smoke_failed", reason=str(exc), parsed_block_count=parsed_count)
    gates["vector_smoke_pass"] = True
    gates["portfolio_semantic_pass"] = True

    return MicroFilterResult(
        decision="pass",
        hard_gates=gates,
        parsed_block_count=parsed_count,
        child_text=child_text,
        vector_smoke_metrics=smoke_metrics,
    )


__all__ = ["MicroFilterResult", "run_micro_filter"]
