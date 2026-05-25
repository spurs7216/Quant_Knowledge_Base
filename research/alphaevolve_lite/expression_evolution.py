"""Safe daily-stock expression evolution primitives.

This module is the first AlphaAgentEvo-style layer for the project.  It gives
the controller a compact object to evolve: a causal daily-stock expression that
can be evaluated into a signal and then converted into a dollar-neutral
portfolio with explicit exposure limits.

The module intentionally owns only expression semantics.  Data loading,
sample-evaluation accounting, cost sensitivity, and promotion gates remain in
the existing evaluator modules.
"""

from __future__ import annotations

import ast
import math
import re
from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
import pandas as pd

from .daily_stock_contract import CONTRACT, DailyStockContract, validate_columns


class ExpressionError(ValueError):
    """Raised when an expression is unsafe, invalid, or not evaluable."""


@dataclass(frozen=True)
class ExpressionEvaluationConfig:
    """Portfolio and operator constraints for expression evaluation."""

    long_quantile: float = 0.9
    short_quantile: float = 0.1
    gross_exposure: float = 1.0
    max_weight: float = 0.02
    min_names_per_side: int = 5
    min_group_count: int = 5
    min_rolling_periods: int = 3
    max_window: int = 252


@dataclass(frozen=True)
class ExpressionSpec:
    """A durable seed expression with the research thesis kept near the code."""

    expression_id: str
    title: str
    thesis: str
    expression: str
    mechanism: str
    expected_effect: str
    tags: tuple[str, ...] = ()


FIELD_DESCRIPTIONS: Mapping[str, str] = {
    "ret": "daily ex-dividend return",
    "total_ret": "daily total return including distributions when available",
    "benchmark_return": "CRSP value-weighted benchmark return",
    "excess_ret": "ret minus benchmark_return",
    "price": "absolute daily closing price",
    "volume": "daily share volume",
    "dollar_volume": "daily dollar volume",
    "market_cap": "daily market capitalization",
    "shares_outstanding": "shares outstanding",
}


OPERATOR_DESCRIPTIONS: Mapping[str, str] = {
    "rank": "cross-sectional percentile rank by date",
    "zscore": "cross-sectional z-score by date",
    "winsorize": "cross-sectional date-wise quantile clipping",
    "industry_neutralize": "within-date industry z-score with broad-date fallback",
    "delay": "security-wise lag; positive windows only",
    "delta": "security-wise current value minus positive lag",
    "rolling_mean": "security-wise causal rolling mean",
    "rolling_sum": "security-wise causal rolling sum",
    "rolling_std": "security-wise causal rolling standard deviation",
    "rolling_rank": "security-wise percentile rank of the latest value in a window",
    "rolling_beta": "security-wise rolling beta of x to y",
    "safe_divide": "division that returns NaN near zero denominators",
    "log1p_abs": "log(1 + abs(x))",
    "signed_sqrt": "sign(x) * sqrt(abs(x))",
    "clip": "numeric clipping",
    "where": "element-wise conditional selection",
}


_FIELD_NAMES = frozenset(FIELD_DESCRIPTIONS)
_OPERATOR_NAMES = frozenset(OPERATOR_DESCRIPTIONS)
_CONSTANT_NAMES = frozenset({"nan", "inf"})
MAX_EXPRESSION_CHARS = 1200
MAX_AST_NODES = 180
MAX_AST_DEPTH = 28
MAX_OPERATOR_CALLS = 56


DEFAULT_EXPRESSION_SEEDS: tuple[ExpressionSpec, ...] = (
    ExpressionSpec(
        expression_id="expr_rev_001",
        title="One-day excess reversal",
        thesis="Short-horizon overreaction can revert after benchmark removal.",
        expression="rank(-excess_ret)",
        mechanism="single-day reversal",
        expected_effect="low turnover baseline for mean-reversion search",
        tags=("reversal", "benchmark_adjusted"),
    ),
    ExpressionSpec(
        expression_id="expr_rev_005",
        title="Five-day excess reversal",
        thesis="A short cumulative residual move can revert more reliably than one noisy day.",
        expression="rank(-rolling_sum(excess_ret, 5))",
        mechanism="multi-day reversal",
        expected_effect="smoother reversal signal with moderate turnover",
        tags=("reversal", "smoothing"),
    ),
    ExpressionSpec(
        expression_id="expr_rev_vol_005_020",
        title="Volatility-normalized reversal",
        thesis="A reversal event should be judged relative to the stock's recent noise scale.",
        expression="rank(-safe_divide(rolling_sum(excess_ret, 5), rolling_std(excess_ret, 20)))",
        mechanism="risk-scaled reversal",
        expected_effect="avoid treating naturally volatile names as stronger signals",
        tags=("reversal", "volatility"),
    ),
    ExpressionSpec(
        expression_id="expr_rev_ind_005",
        title="Industry-neutral reversal",
        thesis="Residual moves within an industry are less likely to be sector beta.",
        expression="industry_neutralize(-rolling_sum(excess_ret, 5))",
        mechanism="industry residualization",
        expected_effect="reduce sector crowding and macro contamination",
        tags=("reversal", "industry_neutral"),
    ),
    ExpressionSpec(
        expression_id="expr_rev_liq_005",
        title="Liquidity-confidence reversal",
        thesis="Short-horizon reversal is more reliable when the move occurs in tradable names.",
        expression="rank(-rolling_sum(excess_ret, 5)) * rank(log1p_abs(dollar_volume))",
        mechanism="reversal gated by liquidity confidence",
        expected_effect="lower implementation risk than pure illiquidity effects",
        tags=("reversal", "liquidity"),
    ),
    ExpressionSpec(
        expression_id="expr_rev_size_005",
        title="Large-cap reversal control",
        thesis="Large-cap names can express reversal with lower missing-weight and cost risk.",
        expression="rank(-rolling_sum(excess_ret, 5)) * rank(log1p_abs(market_cap))",
        mechanism="reversal tilted toward capacity",
        expected_effect="trade off raw edge for coverage and cost robustness",
        tags=("reversal", "capacity"),
    ),
    ExpressionSpec(
        expression_id="expr_mom_020",
        title="Twenty-day residual momentum",
        thesis="Some intermediate-horizon residual moves persist instead of reverting.",
        expression="rank(rolling_sum(excess_ret, 20))",
        mechanism="short momentum",
        expected_effect="test whether parent zoo is missing a continuation family",
        tags=("momentum", "benchmark_adjusted"),
    ),
    ExpressionSpec(
        expression_id="expr_mom_060_ind",
        title="Industry-neutral sixty-day momentum",
        thesis="Intermediate momentum should survive sector demeaning if it is stock-specific.",
        expression="industry_neutralize(rolling_sum(excess_ret, 60))",
        mechanism="industry-neutral continuation",
        expected_effect="reduce sector trend contamination",
        tags=("momentum", "industry_neutral"),
    ),
    ExpressionSpec(
        expression_id="expr_rev_minus_mom",
        title="Reversal against stale momentum",
        thesis="A short reversal is cleaner when it is not just fighting a strong medium trend.",
        expression="rank(-rolling_sum(excess_ret, 5) - 0.25 * rolling_sum(excess_ret, 60))",
        mechanism="horizon interaction",
        expected_effect="avoid buying falling medium-horizon losers solely on bounce logic",
        tags=("reversal", "momentum_interaction"),
    ),
    ExpressionSpec(
        expression_id="expr_price_volume_shock",
        title="Price-volume shock reversal",
        thesis="A large negative residual move on unusually high volume may reflect temporary pressure.",
        expression="rank(where(rolling_sum(excess_ret, 3) < 0, -rolling_sum(excess_ret, 3) * zscore(log1p_abs(volume)), nan))",
        mechanism="signed pressure event",
        expected_effect="focus on sell-pressure candidates instead of all losers",
        tags=("reversal", "volume", "event"),
    ),
    ExpressionSpec(
        expression_id="expr_turnover_proxy",
        title="Dollar-volume adjusted residual move",
        thesis="The same residual return is easier to monetize in high dollar-volume names.",
        expression="rank(safe_divide(-rolling_sum(excess_ret, 5), 1 + zscore(log1p_abs(dollar_volume))))",
        mechanism="liquidity-normalized move",
        expected_effect="penalize fragile low-liquidity names",
        tags=("reversal", "liquidity"),
    ),
    ExpressionSpec(
        expression_id="expr_low_vol_reversal",
        title="Low-volatility reversal",
        thesis="Short-term reversal in calm names is less likely to be a jump-risk artifact.",
        expression="rank(-rolling_sum(excess_ret, 5)) * rank(-rolling_std(excess_ret, 20))",
        mechanism="risk filter",
        expected_effect="lower turnover-aware drawdown from volatile tails",
        tags=("reversal", "volatility"),
    ),
    ExpressionSpec(
        expression_id="expr_high_vol_pressure",
        title="High-volatility pressure control",
        thesis="If reversal edge comes from liquidity pressure, high recent volatility may carry information.",
        expression="rank(-rolling_sum(excess_ret, 5)) * rank(rolling_std(excess_ret, 20))",
        mechanism="pressure risk interaction",
        expected_effect="separate risk-scaled reversal from pressure-event reversal",
        tags=("reversal", "volatility", "event"),
    ),
    ExpressionSpec(
        expression_id="expr_beta_neutral_rev",
        title="Benchmark-beta residual reversal",
        thesis="Market-sensitive stocks need beta adjustment beyond subtracting benchmark return.",
        expression="rank(-(rolling_sum(ret, 5) - rolling_beta(ret, benchmark_return, 60) * rolling_sum(benchmark_return, 5)))",
        mechanism="rolling benchmark residual",
        expected_effect="reduce market-beta leakage in reversal selection",
        tags=("reversal", "beta_adjusted"),
    ),
    ExpressionSpec(
        expression_id="expr_gap_continuation_proxy",
        title="Residual acceleration",
        thesis="Acceleration can distinguish fresh information from stale reversal candidates.",
        expression="rank(delta(rolling_sum(excess_ret, 5), 5))",
        mechanism="return acceleration",
        expected_effect="candidate momentum/event feature for mechanism search",
        tags=("momentum", "event"),
    ),
    ExpressionSpec(
        expression_id="expr_smoothed_rev",
        title="Smoothed reversal",
        thesis="Averaging overlapping short-window reversal estimates can reduce day noise.",
        expression="rank(-rolling_mean(rolling_sum(excess_ret, 5), 3))",
        mechanism="time-smoothed reversal",
        expected_effect="lower turnover while preserving the reversal mechanism",
        tags=("reversal", "smoothing"),
    ),
    ExpressionSpec(
        expression_id="expr_ranked_rev_vol",
        title="Ranked volatility-scaled reversal",
        thesis="Rank-normalizing both legs can avoid unstable magnitudes from noisy denominators.",
        expression="rank(-rolling_sum(excess_ret, 5)) + rank(-rolling_std(excess_ret, 20))",
        mechanism="rank interaction",
        expected_effect="more robust than raw ratio scaling",
        tags=("reversal", "rank_transform"),
    ),
    ExpressionSpec(
        expression_id="expr_ind_mom_minus_rev",
        title="Industry momentum minus short reversal",
        thesis="Medium stock-specific trend and short reversal can coexist at different horizons.",
        expression="industry_neutralize(rolling_sum(excess_ret, 40) - 0.5 * rolling_sum(excess_ret, 5))",
        mechanism="multi-horizon residual blend",
        expected_effect="search across continuation and mean-reversion balance",
        tags=("momentum", "reversal", "industry_neutral"),
    ),
    ExpressionSpec(
        expression_id="expr_volume_fade",
        title="Volume spike fade",
        thesis="Short residual moves on abnormal volume can fade after pressure dissipates.",
        expression="rank(-rolling_sum(excess_ret, 5) * zscore(log1p_abs(volume) - rolling_mean(log1p_abs(volume), 20)))",
        mechanism="abnormal-volume fade",
        expected_effect="test a pressure-release mechanism without new datasets",
        tags=("reversal", "volume"),
    ),
    ExpressionSpec(
        expression_id="expr_size_ind_rev",
        title="Industry-neutral capacity reversal",
        thesis="Industry-neutral reversal should be more tradable when capacity is explicit.",
        expression="industry_neutralize(-rolling_sum(excess_ret, 5)) * rank(log1p_abs(market_cap))",
        mechanism="neutral residual with capacity tilt",
        expected_effect="reduce sector and microcap concentration",
        tags=("reversal", "industry_neutral", "capacity"),
    ),
    ExpressionSpec(
        expression_id="expr_liquidity_momentum",
        title="Liquid residual momentum",
        thesis="Continuation signals may be more reliable and implementable in liquid names.",
        expression="rank(rolling_sum(excess_ret, 20)) * rank(log1p_abs(dollar_volume))",
        mechanism="momentum with capacity confidence",
        expected_effect="cost-aware alternative to reversal-only search",
        tags=("momentum", "liquidity"),
    ),
    ExpressionSpec(
        expression_id="expr_vol_breakout_fade",
        title="Volatility breakout fade",
        thesis="A residual selloff during a volatility breakout can mean forced selling.",
        expression="rank(where(rolling_std(excess_ret, 10) > rolling_std(excess_ret, 60), -rolling_sum(excess_ret, 5), nan))",
        mechanism="conditional pressure fade",
        expected_effect="event-aware reversal without unbounded leverage",
        tags=("reversal", "volatility", "event"),
    ),
    ExpressionSpec(
        expression_id="expr_stable_liq_rev",
        title="Stable-liquidity reversal",
        thesis="Signals are cleaner when liquidity itself is not undergoing a regime shock.",
        expression="rank(-rolling_sum(excess_ret, 5)) * rank(-rolling_std(log1p_abs(dollar_volume), 20))",
        mechanism="liquidity-stability filter",
        expected_effect="avoid temporary data/implementation artifacts from volume shocks",
        tags=("reversal", "liquidity", "stability"),
    ),
    ExpressionSpec(
        expression_id="expr_return_quality",
        title="Return quality reversal",
        thesis="A cumulative residual move supported by many same-sign days may be different from one jump.",
        expression="rank(-rolling_sum(excess_ret, 5) * (1 + rolling_mean(where(excess_ret < 0, 1, 0), 5)))",
        mechanism="path-shape filter",
        expected_effect="separate gradual pressure from single-day noise",
        tags=("reversal", "path_shape"),
    ),
)


@dataclass(frozen=True)
class ExpressionAttemptRecord:
    """One attempt in an expression-evolution episode."""

    turn: int
    expression_id: str
    expression: str
    valid: bool
    score: float | None = None
    hard_gate_pass: bool = True
    failure_reason: str | None = None
    similarity_to_seed: float | None = None
    max_similarity_to_prior: float | None = None


class _ExpressionSafetyValidator(ast.NodeVisitor):
    """Validate that expression AST contains only the supported DSL."""

    _ALLOWED_BINOPS = (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.BitAnd, ast.BitOr)
    _ALLOWED_UNARYOPS = (ast.UAdd, ast.USub, ast.Invert)
    _ALLOWED_CMPOPS = (ast.Gt, ast.GtE, ast.Lt, ast.LtE, ast.Eq, ast.NotEq)

    def __init__(self, allowed_names: set[str]) -> None:
        self._allowed_names = allowed_names

    def generic_visit(self, node: ast.AST) -> None:
        disallowed = (
            ast.Attribute,
            ast.Subscript,
            ast.Lambda,
            ast.Dict,
            ast.List,
            ast.Tuple,
            ast.Set,
            ast.ListComp,
            ast.DictComp,
            ast.SetComp,
            ast.GeneratorExp,
            ast.Await,
            ast.Yield,
            ast.YieldFrom,
            ast.NamedExpr,
            ast.IfExp,
        )
        if isinstance(node, disallowed):
            raise ExpressionError(f"Unsupported expression syntax: {type(node).__name__}")
        super().generic_visit(node)

    def visit_Expression(self, node: ast.Expression) -> None:
        self.visit(node.body)

    def visit_Name(self, node: ast.Name) -> None:
        if node.id not in self._allowed_names:
            raise ExpressionError(f"Unknown expression name: {node.id}")

    def visit_Call(self, node: ast.Call) -> None:
        if not isinstance(node.func, ast.Name):
            raise ExpressionError("Only direct function calls are allowed")
        if node.func.id not in _OPERATOR_NAMES:
            raise ExpressionError(f"Unsupported operator: {node.func.id}")
        if node.keywords:
            raise ExpressionError("Keyword arguments are not allowed in expressions")
        for arg in node.args:
            self.visit(arg)

    def visit_Constant(self, node: ast.Constant) -> None:
        if node.value is None:
            return
        if isinstance(node.value, (bool, int, float)):
            return
        raise ExpressionError("Only numeric, boolean, and None constants are allowed")

    def visit_BinOp(self, node: ast.BinOp) -> None:
        if not isinstance(node.op, self._ALLOWED_BINOPS):
            raise ExpressionError(f"Unsupported binary operator: {type(node.op).__name__}")
        self.visit(node.left)
        self.visit(node.right)

    def visit_UnaryOp(self, node: ast.UnaryOp) -> None:
        if not isinstance(node.op, self._ALLOWED_UNARYOPS):
            raise ExpressionError(f"Unsupported unary operator: {type(node.op).__name__}")
        self.visit(node.operand)

    def visit_Compare(self, node: ast.Compare) -> None:
        if len(node.ops) != 1 or len(node.comparators) != 1:
            raise ExpressionError("Chained comparisons are not allowed")
        if not isinstance(node.ops[0], self._ALLOWED_CMPOPS):
            raise ExpressionError(f"Unsupported comparison: {type(node.ops[0]).__name__}")
        self.visit(node.left)
        self.visit(node.comparators[0])

    def visit_BoolOp(self, node: ast.BoolOp) -> None:
        raise ExpressionError("Use '&' and '|' for element-wise boolean logic")


def evaluate_expression_signal(
    expression_or_spec: str | ExpressionSpec,
    panel: pd.DataFrame,
    *,
    config: ExpressionEvaluationConfig | None = None,
    contract: DailyStockContract = CONTRACT,
) -> pd.Series:
    """Evaluate a safe daily-stock expression into an aligned signal series."""

    config = config or ExpressionEvaluationConfig()
    expression = (
        expression_or_spec.expression
        if isinstance(expression_or_spec, ExpressionSpec)
        else expression_or_spec
    )
    validate_columns(panel, contract)
    tree = _parse_and_validate_expression(expression)
    env = _build_expression_environment(panel, config=config, contract=contract)
    try:
        result = eval(  # noqa: S307 - validated DSL with empty builtins.
            compile(tree, filename="<daily_stock_expression>", mode="eval"),
            {"__builtins__": {}},
            env,
        )
    except Exception as exc:  # pragma: no cover - message path matters more than type.
        raise ExpressionError(f"Expression evaluation failed: {exc}") from exc
    signal = _coerce_series(result, panel.index, name="signal")
    return signal.replace([np.inf, -np.inf], np.nan).astype(float)


def construct_expression_portfolio(
    signal: pd.Series,
    panel: pd.DataFrame,
    *,
    config: ExpressionEvaluationConfig | None = None,
    contract: DailyStockContract = CONTRACT,
) -> pd.Series:
    """Convert an expression signal into constrained dollar-neutral weights."""

    config = config or ExpressionEvaluationConfig()
    if len(signal) != len(panel):
        raise ExpressionError("Signal and panel lengths do not match")
    if not 0.0 < config.short_quantile < config.long_quantile < 1.0:
        raise ExpressionError("Quantiles must satisfy 0 < short < long < 1")
    if config.gross_exposure <= 0:
        raise ExpressionError("gross_exposure must be positive")
    if config.max_weight <= 0:
        raise ExpressionError("max_weight must be positive")

    dates = panel[contract.date]
    weights = pd.Series(0.0, index=panel.index, name="weight")
    side_target = config.gross_exposure / 2.0

    for _, idx in dates.groupby(dates, sort=False).groups.items():
        day_signal = signal.loc[idx].replace([np.inf, -np.inf], np.nan).dropna()
        if day_signal.empty:
            continue
        ordered = day_signal.sort_values(kind="mergesort")
        short_count = max(
            config.min_names_per_side,
            int(math.ceil(config.short_quantile * len(ordered))),
        )
        long_count = max(
            config.min_names_per_side,
            int(math.ceil((1.0 - config.long_quantile) * len(ordered))),
        )
        if short_count + long_count > len(ordered):
            continue
        if _has_lower_boundary_tie(ordered, short_count):
            continue
        if _has_upper_boundary_tie(ordered, long_count):
            continue
        short_idx = ordered.head(short_count).index
        long_idx = ordered.tail(long_count).index
        side_gross = min(
            side_target,
            len(long_idx) * config.max_weight,
            len(short_idx) * config.max_weight,
        )
        if side_gross <= 0:
            continue
        weights.loc[long_idx] = side_gross / len(long_idx)
        weights.loc[short_idx] = -side_gross / len(short_idx)

    return weights


def evaluate_expression_to_weights(
    expression_or_spec: str | ExpressionSpec,
    panel: pd.DataFrame,
    *,
    config: ExpressionEvaluationConfig | None = None,
    contract: DailyStockContract = CONTRACT,
) -> pd.Series:
    """Evaluate an expression and construct its constrained portfolio weights."""

    signal = evaluate_expression_signal(
        expression_or_spec,
        panel,
        config=config,
        contract=contract,
    )
    return construct_expression_portfolio(
        signal,
        panel,
        config=config,
        contract=contract,
    )


def expression_seed_library_rows(
    seeds: Sequence[ExpressionSpec] = DEFAULT_EXPRESSION_SEEDS,
) -> list[dict[str, Any]]:
    """Return JSON-serializable seed expression metadata."""

    return [
        {
            "expression_id": seed.expression_id,
            "title": seed.title,
            "thesis": seed.thesis,
            "expression": seed.expression,
            "mechanism": seed.mechanism,
            "expected_effect": seed.expected_effect,
            "tags": list(seed.tags),
        }
        for seed in seeds
    ]


def expression_similarity(left: str, right: str) -> float:
    """Compute a lightweight operator/field-token similarity for expressions."""

    left_tokens = _expression_tokens(left)
    right_tokens = _expression_tokens(right)
    if not left_tokens and not right_tokens:
        return 1.0
    if not left_tokens or not right_tokens:
        return 0.0
    return len(left_tokens & right_tokens) / len(left_tokens | right_tokens)


def score_expression_trajectory(
    records: Sequence[ExpressionAttemptRecord | Mapping[str, Any]],
    *,
    seed_expression: str | None = None,
    parent_score: float = 0.0,
    pass_margin: float = 0.0,
) -> dict[str, Any]:
    """Score a multi-turn expression-evolution trajectory.

    This is not a promotion gate.  It is an episode-level diagnostic inspired by
    AlphaAgentEvo's emphasis on valid ratio, pass@T, consistency, exploration,
    and improvement streaks.
    """

    normalized = [_normalize_record(record) for record in records]
    total = len(normalized)
    if total == 0:
        return {
            "attempt_count": 0,
            "valid_ratio": 0.0,
            "pass_at_final": False,
            "pass_at_by_turn": {},
            "best_score": None,
            "best_turn": None,
            "best_expression_id": None,
            "improvement_streak": 0,
            "consistency": None,
            "exploration": None,
            "trajectory_score": 0.0,
        }

    threshold = parent_score + pass_margin
    valid_records = [
        record
        for record in normalized
        if record.valid and record.hard_gate_pass and _finite_or_none(record.score) is not None
    ]
    valid_ratio = len(valid_records) / total
    best_record = max(valid_records, key=lambda item: item.score) if valid_records else None

    pass_at_by_turn: dict[int, bool] = {}
    running_pass = False
    for turn in sorted({record.turn for record in normalized}):
        turn_scores = [
            record.score
            for record in normalized
            if record.turn <= turn
            and record.valid
            and record.hard_gate_pass
            and _finite_or_none(record.score) is not None
        ]
        running_pass = running_pass or any(score > threshold for score in turn_scores)
        pass_at_by_turn[turn] = running_pass

    per_turn_best = _best_valid_score_by_turn(normalized)
    improvement_streak = _longest_improvement_streak(per_turn_best, parent_score)
    consistency = _trajectory_consistency(valid_records, seed_expression)
    exploration = _trajectory_exploration(valid_records)
    performance_gain = (
        max(0.0, float(best_record.score) - parent_score) if best_record is not None else 0.0
    )
    valid_component = min(1.0, valid_ratio)
    performance_component = min(1.0, performance_gain)
    streak_component = min(0.5, 0.1 * improvement_streak)
    exploration_component = 0.0 if exploration is None else min(0.3, 0.3 * exploration)
    consistency_component = 0.0 if consistency is None else min(0.2, 0.2 * consistency)
    trajectory_score = (
        valid_component
        + performance_component
        + streak_component
        + exploration_component
        + consistency_component
    )

    return {
        "attempt_count": total,
        "valid_count": len(valid_records),
        "valid_ratio": valid_ratio,
        "pass_at_final": bool(pass_at_by_turn and list(pass_at_by_turn.values())[-1]),
        "pass_at_by_turn": pass_at_by_turn,
        "best_score": None if best_record is None else float(best_record.score),
        "best_turn": None if best_record is None else int(best_record.turn),
        "best_expression_id": None if best_record is None else best_record.expression_id,
        "improvement_streak": improvement_streak,
        "consistency": consistency,
        "exploration": exploration,
        "trajectory_score": trajectory_score,
    }


def expression_interface_markdown() -> str:
    """Render a compact prompt appendix for remote expression-generation agents."""

    field_lines = "\n".join(
        f"- `{name}`: {description}" for name, description in FIELD_DESCRIPTIONS.items()
    )
    operator_lines = "\n".join(
        f"- `{name}`: {description}" for name, description in OPERATOR_DESCRIPTIONS.items()
    )
    seed_lines = "\n".join(
        f"- `{seed.expression_id}`: `{seed.expression}` ({seed.mechanism})"
        for seed in DEFAULT_EXPRESSION_SEEDS
    )
    return (
        "# Daily-Stock Expression Interface\n\n"
        "Expressions must be causal, vectorized over the daily stock panel, and limited "
        "to the fields and operators below. Positive delays and rolling windows look "
        "backward within each security. Do not use attribute access, imports, file IO, "
        "subscripts, Python loops, or undefined names.\n\n"
        "## Fields\n"
        f"{field_lines}\n\n"
        "## Operators\n"
        f"{operator_lines}\n\n"
        "## Starter Seeds\n"
        f"{seed_lines}\n"
    )


def _parse_and_validate_expression(expression: str) -> ast.Expression:
    if not isinstance(expression, str) or not expression.strip():
        raise ExpressionError("Expression must be a non-empty string")
    if len(expression) > MAX_EXPRESSION_CHARS:
        raise ExpressionError(
            f"Expression length {len(expression)} exceeds max {MAX_EXPRESSION_CHARS}"
        )
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise ExpressionError(f"Expression syntax error: {exc.msg}") from exc
    resource_usage = _expression_resource_usage(tree)
    if resource_usage["node_count"] > MAX_AST_NODES:
        raise ExpressionError(
            f"Expression AST node count {resource_usage['node_count']} exceeds max {MAX_AST_NODES}"
        )
    if resource_usage["max_depth"] > MAX_AST_DEPTH:
        raise ExpressionError(
            f"Expression AST depth {resource_usage['max_depth']} exceeds max {MAX_AST_DEPTH}"
        )
    if resource_usage["operator_calls"] > MAX_OPERATOR_CALLS:
        raise ExpressionError(
            f"Expression operator-call count {resource_usage['operator_calls']} exceeds max {MAX_OPERATOR_CALLS}"
        )
    allowed_names = set(_FIELD_NAMES | _OPERATOR_NAMES | _CONSTANT_NAMES)
    _ExpressionSafetyValidator(allowed_names).visit(tree)
    return tree


def _build_expression_environment(
    panel: pd.DataFrame,
    *,
    config: ExpressionEvaluationConfig,
    contract: DailyStockContract,
) -> dict[str, Any]:
    fields = _field_environment(panel, contract)

    def rank(value: Any) -> pd.Series:
        series = _coerce_series(value, panel.index)
        return series.groupby(panel[contract.date], sort=False).rank(pct=True)

    def zscore(value: Any) -> pd.Series:
        series = _coerce_series(value, panel.index)
        return _date_zscore(series, panel, contract)

    def winsorize(value: Any, lower: float = 0.01, upper: float = 0.99) -> pd.Series:
        if not 0.0 <= lower < upper <= 1.0:
            raise ExpressionError("winsorize bounds must satisfy 0 <= lower < upper <= 1")
        series = _coerce_series(value, panel.index)
        grouped = series.groupby(panel[contract.date], sort=False)
        low = grouped.transform(lambda item: item.quantile(lower))
        high = grouped.transform(lambda item: item.quantile(upper))
        return series.clip(lower=low, upper=high)

    def industry_neutralize(value: Any) -> pd.Series:
        series = _coerce_series(value, panel.index)
        industry = panel[contract.industry_primary]
        group_keys = [panel[contract.date], industry]
        counts = series.groupby(group_keys, sort=False).transform("count")
        mean = series.groupby(group_keys, sort=False).transform("mean")
        std = series.groupby(group_keys, sort=False).transform("std").replace(0.0, np.nan)
        group_z = (series - mean) / std
        broad_z = _date_zscore(series, panel, contract)
        return group_z.where(counts >= config.min_group_count, broad_z)

    def delay(value: Any, window: int) -> pd.Series:
        return _security_shift(
            _coerce_series(value, panel.index),
            panel,
            contract,
            _validate_window(window, config),
        )

    def delta(value: Any, window: int) -> pd.Series:
        series = _coerce_series(value, panel.index)
        return series - _security_shift(series, panel, contract, _validate_window(window, config))

    def rolling_mean(value: Any, window: int) -> pd.Series:
        return _security_rolling(
            _coerce_series(value, panel.index),
            panel,
            contract,
            _validate_window(window, config),
            "mean",
            config.min_rolling_periods,
        )

    def rolling_sum(value: Any, window: int) -> pd.Series:
        return _security_rolling(
            _coerce_series(value, panel.index),
            panel,
            contract,
            _validate_window(window, config),
            "sum",
            config.min_rolling_periods,
        )

    def rolling_std(value: Any, window: int) -> pd.Series:
        return _security_rolling(
            _coerce_series(value, panel.index),
            panel,
            contract,
            _validate_window(window, config),
            "std",
            config.min_rolling_periods,
        )

    def rolling_rank(value: Any, window: int) -> pd.Series:
        return _security_rolling_rank(
            _coerce_series(value, panel.index),
            panel,
            contract,
            _validate_window(window, config),
            config.min_rolling_periods,
        )

    def rolling_beta(x_value: Any, y_value: Any, window: int) -> pd.Series:
        return _security_rolling_beta(
            _coerce_series(x_value, panel.index),
            _coerce_series(y_value, panel.index),
            panel,
            contract,
            _validate_window(window, config),
            config.min_rolling_periods,
        )

    def safe_divide(numerator: Any, denominator: Any) -> pd.Series:
        numerator_series = _coerce_series(numerator, panel.index)
        denominator_series = _coerce_series(denominator, panel.index).replace(0.0, np.nan)
        denominator_series = denominator_series.mask(denominator_series.abs() < 1.0e-12)
        return numerator_series / denominator_series

    def log1p_abs(value: Any) -> pd.Series:
        series = _coerce_series(value, panel.index)
        return np.log1p(series.abs())

    def signed_sqrt(value: Any) -> pd.Series:
        series = _coerce_series(value, panel.index)
        return np.sign(series) * np.sqrt(series.abs())

    def clip(value: Any, lower: float, upper: float) -> pd.Series:
        if lower >= upper:
            raise ExpressionError("clip lower bound must be below upper bound")
        return _coerce_series(value, panel.index).clip(lower=lower, upper=upper)

    def where(condition: Any, if_true: Any, if_false: Any) -> pd.Series:
        condition_series = _coerce_series(condition, panel.index).fillna(False).astype(bool)
        true_series = _coerce_series(if_true, panel.index)
        false_series = _coerce_series(if_false, panel.index)
        return pd.Series(
            np.where(condition_series, true_series, false_series),
            index=panel.index,
        )

    operators: dict[str, Any] = {
        "rank": rank,
        "zscore": zscore,
        "winsorize": winsorize,
        "industry_neutralize": industry_neutralize,
        "delay": delay,
        "delta": delta,
        "rolling_mean": rolling_mean,
        "rolling_sum": rolling_sum,
        "rolling_std": rolling_std,
        "rolling_rank": rolling_rank,
        "rolling_beta": rolling_beta,
        "safe_divide": safe_divide,
        "log1p_abs": log1p_abs,
        "signed_sqrt": signed_sqrt,
        "clip": clip,
        "where": where,
        "nan": np.nan,
        "inf": np.inf,
    }
    return {**fields, **operators}


def _field_environment(panel: pd.DataFrame, contract: DailyStockContract) -> dict[str, pd.Series]:
    ret = pd.to_numeric(panel[contract.ex_dividend_return], errors="coerce")
    total_ret = pd.to_numeric(panel[contract.total_return], errors="coerce")
    benchmark_return = pd.to_numeric(panel[contract.benchmark_return_primary], errors="coerce")
    price = pd.to_numeric(panel[contract.price], errors="coerce").abs()
    volume = pd.to_numeric(panel[contract.volume], errors="coerce")
    dollar_volume = pd.to_numeric(panel[contract.dollar_volume], errors="coerce")
    market_cap = pd.to_numeric(panel[contract.market_cap], errors="coerce")
    shares_outstanding = pd.to_numeric(panel[contract.shares_outstanding], errors="coerce")
    return {
        "ret": ret,
        "total_ret": total_ret,
        "benchmark_return": benchmark_return,
        "excess_ret": ret - benchmark_return,
        "price": price,
        "volume": volume,
        "dollar_volume": dollar_volume,
        "market_cap": market_cap,
        "shares_outstanding": shares_outstanding,
    }


def _has_lower_boundary_tie(ordered: pd.Series, count: int) -> bool:
    if count <= 0 or count >= len(ordered):
        return False
    return bool(ordered.iloc[count - 1] == ordered.iloc[count])


def _has_upper_boundary_tie(ordered: pd.Series, count: int) -> bool:
    if count <= 0 or count >= len(ordered):
        return False
    start = len(ordered) - count
    return bool(ordered.iloc[start - 1] == ordered.iloc[start])


def _expression_resource_usage(tree: ast.AST) -> dict[str, int]:
    node_count = 0
    operator_calls = 0
    max_depth = 0
    stack: list[tuple[ast.AST, int]] = [(tree, 1)]
    while stack:
        node, depth = stack.pop()
        node_count += 1
        max_depth = max(max_depth, depth)
        if isinstance(node, ast.Call):
            operator_calls += 1
        for child in ast.iter_child_nodes(node):
            stack.append((child, depth + 1))
    return {
        "node_count": node_count,
        "max_depth": max_depth,
        "operator_calls": operator_calls,
    }


def _coerce_series(value: Any, index: pd.Index, name: str | None = None) -> pd.Series:
    if isinstance(value, pd.Series):
        if not value.index.equals(index):
            value = value.reindex(index)
        return value.rename(name) if name is not None else value
    if np.isscalar(value) or value is None:
        scalar = np.nan if value is None else value
        return pd.Series(scalar, index=index, name=name)
    array = np.asarray(value)
    if array.shape != (len(index),):
        raise ExpressionError("Expression result cannot be aligned to panel index")
    return pd.Series(array, index=index, name=name)


def _validate_window(window: int | float, config: ExpressionEvaluationConfig) -> int:
    if not isinstance(window, (int, float)) or not float(window).is_integer():
        raise ExpressionError("Window arguments must be positive integers")
    window_int = int(window)
    if window_int < 1:
        raise ExpressionError("Window arguments must be positive; negative delays imply lookahead")
    if window_int > config.max_window:
        raise ExpressionError(f"Window {window_int} exceeds max_window={config.max_window}")
    return window_int


def _ordered_frame(
    series: pd.Series,
    panel: pd.DataFrame,
    contract: DailyStockContract,
    column: str = "x",
) -> pd.DataFrame:
    frame = pd.DataFrame(
        {
            column: series,
            "_security": panel[contract.security_id],
            "_date": panel[contract.date],
        },
        index=series.index,
    )
    return frame.sort_values(["_security", "_date"], kind="mergesort")


def _security_shift(
    series: pd.Series,
    panel: pd.DataFrame,
    contract: DailyStockContract,
    window: int,
) -> pd.Series:
    ordered = _ordered_frame(series, panel, contract)
    shifted = ordered.groupby("_security", sort=False)["x"].shift(window)
    return shifted.reindex(series.index)


def _security_rolling(
    series: pd.Series,
    panel: pd.DataFrame,
    contract: DailyStockContract,
    window: int,
    method: str,
    min_periods: int,
) -> pd.Series:
    ordered = _ordered_frame(series, panel, contract)
    grouped = ordered.groupby("_security", sort=False)["x"]
    roller = grouped.rolling(window=window, min_periods=min(min_periods, window))
    if method == "mean":
        rolled = roller.mean()
    elif method == "sum":
        rolled = roller.sum()
    elif method == "std":
        rolled = roller.std()
    else:  # pragma: no cover - private caller controls method.
        raise ExpressionError(f"Unsupported rolling method: {method}")
    return rolled.reset_index(level=0, drop=True).reindex(series.index)


def _security_rolling_rank(
    series: pd.Series,
    panel: pd.DataFrame,
    contract: DailyStockContract,
    window: int,
    min_periods: int,
) -> pd.Series:
    ordered = _ordered_frame(series, panel, contract)

    def latest_percentile(values: np.ndarray) -> float:
        latest = values[-1]
        if math.isnan(latest):
            return np.nan
        valid = values[~np.isnan(values)]
        if len(valid) == 0:
            return np.nan
        return float(np.sum(valid <= latest) / len(valid))

    rolled = (
        ordered.groupby("_security", sort=False)["x"]
        .rolling(window=window, min_periods=min(min_periods, window))
        .apply(latest_percentile, raw=True)
    )
    return rolled.reset_index(level=0, drop=True).reindex(series.index)


def _security_rolling_beta(
    x_series: pd.Series,
    y_series: pd.Series,
    panel: pd.DataFrame,
    contract: DailyStockContract,
    window: int,
    min_periods: int,
) -> pd.Series:
    ordered = pd.DataFrame(
        {
            "x": x_series,
            "y": y_series,
            "_security": panel[contract.security_id],
            "_date": panel[contract.date],
        },
        index=x_series.index,
    ).sort_values(["_security", "_date"], kind="mergesort")
    beta = pd.Series(np.nan, index=ordered.index)
    effective_min = min(min_periods, window)
    for _, group in ordered.groupby("_security", sort=False):
        covariance = group["x"].rolling(window=window, min_periods=effective_min).cov(group["y"])
        variance = group["y"].rolling(window=window, min_periods=effective_min).var()
        beta.loc[group.index] = covariance / variance.replace(0.0, np.nan)
    return beta.reindex(x_series.index)


def _date_zscore(
    series: pd.Series,
    panel: pd.DataFrame,
    contract: DailyStockContract,
) -> pd.Series:
    grouped = series.groupby(panel[contract.date], sort=False)
    mean = grouped.transform("mean")
    std = grouped.transform("std").replace(0.0, np.nan)
    return (series - mean) / std


def _expression_tokens(expression: str) -> set[str]:
    try:
        tree = _parse_and_validate_expression(expression)
    except ExpressionError:
        return set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", expression))
    tokens: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            tokens.add(f"name:{node.id}")
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            tokens.add(f"call:{node.func.id}")
        elif isinstance(node, ast.BinOp):
            tokens.add(f"op:{type(node.op).__name__}")
        elif isinstance(node, ast.UnaryOp):
            tokens.add(f"op:{type(node.op).__name__}")
        elif isinstance(node, ast.Compare):
            tokens.add(f"cmp:{type(node.ops[0]).__name__}")
        elif isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            tokens.add("const:number")
    return tokens


def _normalize_record(record: ExpressionAttemptRecord | Mapping[str, Any]) -> ExpressionAttemptRecord:
    if isinstance(record, ExpressionAttemptRecord):
        return record
    return ExpressionAttemptRecord(
        turn=int(record.get("turn", 0)),
        expression_id=str(record.get("expression_id", "")),
        expression=str(record.get("expression", "")),
        valid=bool(record.get("valid", False)),
        score=_finite_or_none(record.get("score")),
        hard_gate_pass=bool(record.get("hard_gate_pass", True)),
        failure_reason=record.get("failure_reason"),
        similarity_to_seed=_finite_or_none(record.get("similarity_to_seed")),
        max_similarity_to_prior=_finite_or_none(record.get("max_similarity_to_prior")),
    )


def _finite_or_none(value: Any) -> float | None:
    if value is None:
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def _best_valid_score_by_turn(records: Sequence[ExpressionAttemptRecord]) -> dict[int, float]:
    scores_by_turn: dict[int, list[float]] = {}
    for record in records:
        score = _finite_or_none(record.score)
        if record.valid and record.hard_gate_pass and score is not None:
            scores_by_turn.setdefault(record.turn, []).append(score)
    return {turn: max(scores) for turn, scores in scores_by_turn.items()}


def _longest_improvement_streak(scores_by_turn: Mapping[int, float], parent_score: float) -> int:
    best_so_far = parent_score
    current = 0
    longest = 0
    previous_turn: int | None = None
    for turn, score in sorted(scores_by_turn.items()):
        if previous_turn is not None and turn != previous_turn + 1:
            current = 0
        if score > best_so_far:
            current += 1
            best_so_far = score
        else:
            current = 0
        longest = max(longest, current)
        previous_turn = turn
    return longest


def _trajectory_consistency(
    records: Sequence[ExpressionAttemptRecord],
    seed_expression: str | None,
) -> float | None:
    similarities: list[float] = []
    for record in records:
        explicit = _finite_or_none(record.similarity_to_seed)
        if explicit is not None:
            similarities.append(explicit)
        elif seed_expression:
            similarities.append(expression_similarity(seed_expression, record.expression))
    if not similarities:
        return None
    return float(np.mean(similarities))


def _trajectory_exploration(records: Sequence[ExpressionAttemptRecord]) -> float | None:
    novelty_scores: list[float] = []
    prior_expressions: list[str] = []
    for record in records:
        explicit = _finite_or_none(record.max_similarity_to_prior)
        if explicit is not None:
            novelty_scores.append(max(0.0, 1.0 - explicit))
        elif prior_expressions:
            max_similarity = max(
                expression_similarity(record.expression, prior)
                for prior in prior_expressions
            )
            novelty_scores.append(max(0.0, 1.0 - max_similarity))
        prior_expressions.append(record.expression)
    if not novelty_scores:
        return None
    return float(np.mean(novelty_scores))
