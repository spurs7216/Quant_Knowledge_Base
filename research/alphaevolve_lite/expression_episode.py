"""Prompting and bookkeeping for remote daily-stock expression episodes."""

from __future__ import annotations

import json
import math
import re
from dataclasses import asdict, dataclass
from typing import Any, Mapping, Sequence

from .expression_evolution import (
    ExpressionAttemptRecord,
    ExpressionSpec,
    expression_similarity,
)


DEFAULT_EPISODE_PARENT_IDS = (
    "expr_smoothed_rev",
    "expr_size_ind_rev",
    "expr_mom_060_ind",
)


PARENT_OBJECTIVES: Mapping[str, str] = {
    "expr_smoothed_rev": (
        "Keep the smoothed short-horizon reversal mechanism, keep turnover near or below the "
        "parent, and repair the negative 2023-2025 out-of-sample behavior. Prefer causal "
        "smoothing, robust rank/winsor transforms, and regime/quality controls over stronger "
        "daily churn."
    ),
    "expr_size_ind_rev": (
        "Preserve the only seed-zoo pattern with positive IS and OS Sharpe while reducing "
        "turnover and cost drag. Do not trade raw size or ordinal industry codes; use capacity "
        "only as a robustness or implementation-confidence modifier."
    ),
    "expr_mom_060_ind": (
        "Treat the OS-positive momentum behavior as a regime diagnostic. Add causal controls "
        "that improve 2011-2022 in-sample stability without simply reversing the signal or "
        "creating a sparse few-day book."
    ),
    "expr_liquidity_momentum": (
        "Treat the OS-positive liquid momentum behavior as a regime diagnostic. Add causal "
        "controls that improve 2011-2022 in-sample stability while preserving broad coverage "
        "and reasonable turnover."
    ),
}


@dataclass(frozen=True)
class ExpressionProposal:
    """One JSON proposal returned by the remote model."""

    model_expression_id: str
    expression: str
    thesis: str
    mechanism: str
    expected_effect: str

    def to_spec(self, expression_id: str, parent: ExpressionSpec, turn: int) -> ExpressionSpec:
        """Convert the proposal into an evaluable expression spec."""

        title = f"{parent.title} episode turn {turn}"
        return ExpressionSpec(
            expression_id=expression_id,
            title=title,
            thesis=self.thesis,
            expression=self.expression,
            mechanism=self.mechanism,
            expected_effect=self.expected_effect,
            tags=(*parent.tags, "episode_child"),
        )

    def as_record(self) -> dict[str, Any]:
        return asdict(self)


def parent_objective(parent_expression_id: str) -> str:
    """Return the first-episode objective for a parent seed."""

    return PARENT_OBJECTIVES.get(
        parent_expression_id,
        "Improve turnover-aware IS/OS behavior without changing evaluator contracts, "
        "creating sparse books, or adding unsupported data fields.",
    )


def build_expression_episode_prompt(
    *,
    parent: ExpressionSpec,
    root_parent: ExpressionSpec | None = None,
    parent_ranking: Mapping[str, Any],
    population_context: Mapping[str, Any] | None = None,
    prior_feedback: Sequence[Mapping[str, Any]],
    turn: int,
    offspring_per_turn: int,
    interface_markdown: str,
) -> tuple[str, str]:
    """Build the JSON-only prompt for one expression-evolution turn."""

    system_prompt = (
        "You are a quant research expression generator. Return exactly one JSON object and "
        "nothing else. Do not use Markdown, code fences, Python files, SEARCH/REPLACE patches, "
        "EVOLVE markers, imports, loops, attribute access, subscripts, or fields/operators not "
        "listed in the interface. Expressions must be causal daily-stock DSL expressions."
    )
    schema = {
        "children": [
            {
                "expression_id": "short_model_label",
                "expression": "rank(-rolling_sum(excess_ret, 5))",
                "thesis": "why this can improve the parent",
                "mechanism": "specific mechanism being changed",
                "expected_effect": "expected effect on IS/OS, turnover, coverage, or costs",
            }
        ]
    }
    compact_feedback = list(prior_feedback)[-12:]
    root = root_parent or parent
    population_payload = dict(population_context or {})
    user_prompt = (
        "# Task\n"
        f"Generate {offspring_per_turn} child expressions for turn {turn}. The goal is not a "
        "grid search over constants; propose small but meaningful expression-level mechanisms.\n\n"
        "# Root Seed\n"
        f"- root_expression_id: {root.expression_id}\n"
        f"- root_expression: `{root.expression}`\n"
        f"- root_mechanism: {root.mechanism}\n\n"
        "# Parent\n"
        f"- parent_expression_id: {parent.expression_id}\n"
        f"- parent_expression: `{parent.expression}`\n"
        f"- parent_mechanism: {parent.mechanism}\n"
        f"- parent_expected_effect: {parent.expected_effect}\n\n"
        "# Objective\n"
        f"{parent_objective(root.expression_id)}\n\n"
        "# Parent Metrics\n"
        f"{json.dumps(parent_ranking, indent=2, sort_keys=True)}\n\n"
        "# Population Context\n"
        f"{json.dumps(population_payload, indent=2, sort_keys=True)}\n\n"
        "# Prior Episode Feedback\n"
        f"{json.dumps(compact_feedback, indent=2, sort_keys=True)}\n\n"
        "# Hard Rules\n"
        "- Use only listed fields and operators.\n"
        "- Do not use raw `industry` or SIC codes as a tradable numeric field; use "
        "`industry_neutralize(...)` only.\n"
        "- Preserve broad daily coverage; do not rely on sparse event-only trading.\n"
        "- Prefer transformations that plausibly reduce turnover or improve regime stability "
        "without hiding cost, max weight, missing-held weight, or net exposure.\n"
        "- Each expression must be syntactically valid in the DSL and under 1200 characters.\n\n"
        "# Output Schema\n"
        f"{json.dumps(schema, indent=2, sort_keys=True)}\n\n"
        "# Expression Interface\n"
        f"{interface_markdown}"
    )
    return system_prompt, user_prompt


def parse_expression_proposals(content: str) -> list[ExpressionProposal]:
    """Parse the model's JSON response into expression proposals."""

    payload = _load_json_object(content)
    children = payload.get("children")
    if not isinstance(children, list):
        raise ValueError("model response must contain a list field named 'children'")
    proposals: list[ExpressionProposal] = []
    for idx, item in enumerate(children):
        if not isinstance(item, dict):
            raise ValueError(f"child {idx} is not a JSON object")
        expression = _required_text(item, "expression", idx)
        proposals.append(
            ExpressionProposal(
                model_expression_id=str(item.get("expression_id") or f"child_{idx:02d}"),
                expression=expression,
                thesis=_required_text(item, "thesis", idx),
                mechanism=_required_text(item, "mechanism", idx),
                expected_effect=_required_text(item, "expected_effect", idx),
            )
        )
    return proposals


def exact_expression_key(expression: str) -> str:
    """Normalize expression text for exact-duplicate checks."""

    return re.sub(r"\s+", "", expression.strip())


def expression_novelty_diagnostics(
    *,
    expression: str,
    parent_expression: str,
    prior_expressions: Sequence[str],
    near_duplicate_threshold: float,
) -> dict[str, Any]:
    """Return exact and structural similarity diagnostics for one proposal."""

    expression_key = exact_expression_key(expression)
    prior_keys = [exact_expression_key(item) for item in prior_expressions]
    parent_similarity = expression_similarity(expression, parent_expression)
    prior_similarities = [
        expression_similarity(expression, prior) for prior in prior_expressions
    ]
    max_prior = max(prior_similarities) if prior_similarities else None
    exact_duplicate = expression_key == exact_expression_key(parent_expression) or expression_key in prior_keys
    near_duplicate = bool(
        not exact_duplicate
        and (
            parent_similarity >= near_duplicate_threshold
            or (max_prior is not None and max_prior >= near_duplicate_threshold)
        )
    )
    return {
        "exact_duplicate": exact_duplicate,
        "near_duplicate": near_duplicate,
        "similarity_to_parent": float(parent_similarity),
        "max_similarity_to_prior": None if max_prior is None else float(max_prior),
        "near_duplicate_threshold": float(near_duplicate_threshold),
    }


def attempt_record_from_result(result: Mapping[str, Any]) -> ExpressionAttemptRecord:
    """Convert an evaluated or rejected child result into a trajectory record."""

    search = result.get("metrics", {}).get("search_sample", {})
    status = str(result.get("status") or "")
    return ExpressionAttemptRecord(
        turn=int(result.get("turn") or 0),
        expression_id=str(result.get("expression_id") or ""),
        expression=str(result.get("expression") or ""),
        valid=status == "expression_sample_pass",
        score=_finite_or_none(search.get("turnover_aware_score")),
        hard_gate_pass=status == "expression_sample_pass",
        failure_reason=result.get("failure_reason"),
        similarity_to_seed=_finite_or_none(result.get("similarity_to_parent")),
        max_similarity_to_prior=_finite_or_none(result.get("max_similarity_to_prior")),
    )


def _required_text(item: Mapping[str, Any], key: str, idx: int) -> str:
    value = item.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"child {idx} missing non-empty string field {key!r}")
    return value.strip()


def _load_json_object(content: str) -> dict[str, Any]:
    if not isinstance(content, str) or not content.strip():
        raise ValueError("model response content is empty")
    stripped = _strip_code_fence(content.strip())
    try:
        payload = json.loads(stripped)
    except json.JSONDecodeError:
        start = stripped.find("{")
        end = stripped.rfind("}")
        if start < 0 or end <= start:
            raise ValueError("model response does not contain a JSON object") from None
        try:
            payload = json.loads(stripped[start : end + 1])
        except json.JSONDecodeError as exc:
            raise ValueError(f"model response JSON is malformed: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError("model response must be a JSON object")
    return payload


def _strip_code_fence(content: str) -> str:
    if not content.startswith("```"):
        return content
    lines = content.splitlines()
    if len(lines) >= 3 and lines[-1].strip().startswith("```"):
        return "\n".join(lines[1:-1]).strip()
    return content


def _finite_or_none(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


__all__ = [
    "DEFAULT_EPISODE_PARENT_IDS",
    "ExpressionProposal",
    "attempt_record_from_result",
    "build_expression_episode_prompt",
    "exact_expression_key",
    "expression_novelty_diagnostics",
    "parent_objective",
    "parse_expression_proposals",
]
