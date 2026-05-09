"""Deterministic diagnostic cards for Phase 4 AlphaEvolve-lite.

The Dr. RTL transfer needs an analyzer role that localizes bottlenecks before
the generator proposes edits. This module keeps that role tool-grounded: it
turns evaluator/controller artifacts into compact cards and never invents
market validity labels.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any, Iterable

from .artifact_io import write_json
from .paths import utc_now_iso


DIAGNOSTIC_REPORT_SCHEMA_VERSION = "phase4_diagnostic_report_v1"

SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2, "info": 3}


def _as_float(value: Any) -> float | None:
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(result):
        return None
    return result


def _dig(mapping: dict[str, Any], *keys: str) -> Any:
    current: Any = mapping
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def _card(
    *,
    diagnostic_id: str,
    bottleneck: str,
    severity: str,
    evidence: dict[str, Any],
    likely_causes: list[str],
    target_surfaces: list[str],
    prompt_instruction: str,
    avoid_actions: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "diagnostic_id": diagnostic_id,
        "bottleneck": bottleneck,
        "severity": severity,
        "evidence": evidence,
        "likely_causes": likely_causes,
        "target_surfaces": target_surfaces,
        "prompt_instruction": prompt_instruction,
        "avoid_actions": avoid_actions or [],
    }


def build_evaluator_diagnostic_report(
    evaluator_summary: dict[str, Any] | None,
    *,
    source_path: str | Path | None = None,
) -> dict[str, Any]:
    """Convert an evaluator summary into prompt-facing bottleneck cards."""

    summary = evaluator_summary or {}
    cards: list[dict[str, Any]] = []
    if not summary:
        cards.append(
            _card(
                diagnostic_id="diag_no_evaluator_summary",
                bottleneck="missing_evaluator_context",
                severity="medium",
                evidence={"source_path": str(source_path) if source_path else None},
                likely_causes=["controller dry run without data-backed parent summary"],
                target_surfaces=["signal", "ranking", "portfolio", "risk"],
                prompt_instruction=(
                    "Use only controller-static constraints and known seed lessons; do not infer market quality."
                ),
            )
        )
    search = _dig(summary, "metrics", "search_sample") or {}
    baseline = summary.get("baseline_summary", {}) if isinstance(summary.get("baseline_summary"), dict) else {}
    decision = summary.get("decision")
    sharpe = _as_float(search.get("sharpe"))
    ann_return = _as_float(search.get("annualized_return"))
    turnover = _as_float(search.get("turnover"))
    turnover_score = _as_float(search.get("turnover_aware_score"))
    max_weight = _as_float(search.get("max_weight"))
    max_missing = _as_float(search.get("max_missing_held_weight"))
    if decision and str(decision) not in {"sample_pass", "survive_for_mutation", "record_only"}:
        cards.append(
            _card(
                diagnostic_id="diag_parent_not_promoted",
                bottleneck="parent_evaluator_decision_not_promoted",
                severity="medium",
                evidence={"decision": decision},
                likely_causes=["parent is evaluator-ready context, not a tradable alpha"],
                target_surfaces=["signal", "ranking", "portfolio", "risk"],
                prompt_instruction=(
                    "Treat the parent as a mutation scaffold. Improve one mechanism without weakening evaluator gates."
                ),
            )
        )
    if sharpe is not None and sharpe < 0.0:
        cards.append(
            _card(
                diagnostic_id="diag_negative_net_sharpe",
                bottleneck="negative_net_performance",
                severity="high",
                evidence={"search_sample_sharpe": sharpe, "annualized_return": ann_return},
                likely_causes=["signal direction may be wrong", "signal may be too noisy after scaling"],
                target_surfaces=["signal", "ranking"],
                prompt_instruction=(
                    "Prefer a focused signal-direction, ranking-direction, or smoothing change over portfolio leverage."
                ),
                avoid_actions=["do not compensate by increasing gross exposure", "do not edit cost or split logic"],
            )
        )
    if turnover_score is not None and turnover_score < 0.0:
        cards.append(
            _card(
                diagnostic_id="diag_cost_turnover_fragility",
                bottleneck="cost_and_turnover_fragility",
                severity="high",
                evidence={"turnover_aware_score": turnover_score, "turnover": turnover},
                likely_causes=["too much day-to-day rank churn", "signal is not sufficiently persistent"],
                target_surfaces=["signal", "ranking", "portfolio", "risk"],
                prompt_instruction=(
                    "Prefer turnover damping, robust ranking, or conservative risk controls that preserve both books."
                ),
                avoid_actions=["do not remove transaction costs", "do not hide turnover by changing rebalance timing"],
            )
        )
    elif turnover is not None and turnover >= 0.35:
        cards.append(
            _card(
                diagnostic_id="diag_high_turnover",
                bottleneck="high_turnover",
                severity="medium",
                evidence={"turnover": turnover},
                likely_causes=["unstable cross-sectional ordering", "overreactive signal transform"],
                target_surfaces=["signal", "ranking", "portfolio"],
                prompt_instruction="Make one bounded change that lowers churn without collapsing long/short balance.",
                avoid_actions=["do not reduce turnover by dropping one side of the book"],
            )
        )
    if max_weight is not None and max_weight > 0.025:
        cards.append(
            _card(
                diagnostic_id="diag_concentration",
                bottleneck="position_concentration",
                severity="high",
                evidence={"max_weight": max_weight},
                likely_causes=["too few selected names", "weight normalization may be too concentrated"],
                target_surfaces=["portfolio", "risk"],
                prompt_instruction="Preserve max-weight discipline and avoid changes that put most gross exposure in one name.",
                avoid_actions=["do not raise max_weight", "do not create one-stock or one-side portfolios"],
            )
        )
    if max_missing is not None and max_missing > 0.01:
        cards.append(
            _card(
                diagnostic_id="diag_missing_held_weight",
                bottleneck="missing_held_weight",
                severity="medium",
                evidence={"max_missing_held_weight": max_missing},
                likely_causes=["held names may lose forward-return coverage", "coverage can distort reported returns"],
                target_surfaces=["portfolio", "risk"],
                prompt_instruction="Avoid narrowing the book in a way that increases missing held-weight exposure.",
                avoid_actions=["do not treat missing returns as alpha"],
            )
        )
    sign_flip = baseline.get("sign_flip_search_sample", {})
    sign_flip_sharpe = _as_float(sign_flip.get("sharpe")) if isinstance(sign_flip, dict) else None
    if sign_flip_sharpe is not None and sharpe is not None and sign_flip_sharpe > sharpe:
        cards.append(
            _card(
                diagnostic_id="diag_sign_flip_better",
                bottleneck="signal_direction_suspect",
                severity="high",
                evidence={"parent_sharpe": sharpe, "sign_flip_sharpe": sign_flip_sharpe},
                likely_causes=["current innovation sign may be backward for the sample"],
                target_surfaces=["signal", "ranking"],
                prompt_instruction="Consider direction changes or monotone ranking changes before complex parameter tweaks.",
                avoid_actions=["do not grid-search Kalman constants as the main contribution"],
            )
        )
    random_score = baseline.get("random_search_sample_turnover_aware_score", {})
    if isinstance(random_score, dict):
        seed_value = _as_float(random_score.get("seed_value"))
        random_median = _as_float(random_score.get("median"))
        if seed_value is not None and random_median is not None and seed_value <= random_median:
            cards.append(
                _card(
                    diagnostic_id="diag_weak_null_delta",
                    bottleneck="weak_null_delta",
                    severity="high",
                    evidence={"seed_turnover_aware_score": seed_value, "random_median": random_median},
                    likely_causes=["signal may not beat matched random long/short selection"],
                    target_surfaces=["signal", "ranking"],
                    prompt_instruction="Make the signal economically more selective; do not tune portfolio mechanics only.",
                    avoid_actions=["do not promote without null improvement"],
                )
            )
    if not cards:
        cards.append(
            _card(
                diagnostic_id="diag_no_major_evaluator_bottleneck",
                bottleneck="no_major_evaluator_bottleneck_detected",
                severity="info",
                evidence={"decision": decision},
                likely_causes=["available evaluator card did not trigger deterministic diagnostics"],
                target_surfaces=["signal", "ranking", "portfolio", "risk"],
                prompt_instruction="Keep changes small and preserve existing evaluator-safe behavior.",
            )
        )
    return _report("evaluator_diagnostics", cards, source_path=source_path)


def build_controller_diagnostic_report(
    *,
    summary: dict[str, Any],
    attempts: list[dict[str, Any]],
    source_path: str | Path | None = None,
) -> dict[str, Any]:
    """Convert controller batch outcomes into Dr. RTL-style bottleneck cards."""

    cards: list[dict[str, Any]] = []
    pass_count = int(summary.get("pass_count", 0) or 0)
    attempt_count = int(summary.get("attempt_count", 0) or 0)
    failure_categories = summary.get("failure_categories", {}) or {}
    if attempt_count and pass_count == 0:
        cards.append(
            _card(
                diagnostic_id="diag_no_controller_pass_children",
                bottleneck="no_controller_pass_children",
                severity="high",
                evidence={"attempt_count": attempt_count, "failure_categories": failure_categories},
                likely_causes=["prompt/repair contract too loose", "model changed code outside safe surface"],
                target_surfaces=["signal", "ranking", "portfolio", "risk"],
                prompt_instruction="Before scaling, fix the dominant controller failure category and rerun a small batch.",
            )
        )
    if int(failure_categories.get("no_valid_patch", 0) or 0):
        cards.append(
            _card(
                diagnostic_id="diag_model_declined_patch",
                bottleneck="model_declined_or_failed_to_propose_patch",
                severity="medium",
                evidence={"no_valid_patch": failure_categories.get("no_valid_patch")},
                likely_causes=["prompt may be too constrained", "model may not see a safe focused edit"],
                target_surfaces=["signal", "ranking", "portfolio", "risk"],
                prompt_instruction="Inspect prompt salience before loosening gates; NO_VALID_PATCH is preferable to unsafe edits.",
            )
        )
    if int(failure_categories.get("malformed_search_replace", 0) or 0):
        cards.append(
            _card(
                diagnostic_id="diag_patch_format_fragility",
                bottleneck="patch_format_fragility",
                severity="high",
                evidence={
                    "malformed_search_replace": failure_categories.get("malformed_search_replace"),
                    "raw_parse_pass_rate": summary.get("raw_parse_pass_rate"),
                },
                likely_causes=["model output violated SEARCH/REPLACE contract"],
                target_surfaces=["signal", "ranking", "portfolio", "risk"],
                prompt_instruction="Keep output-format instructions strict and use repair only for bounded malformed patches.",
                avoid_actions=["do not accept markdown or explanatory output as a patch"],
            )
        )
    block_contract_failures = {
        key: failure_categories.get(key)
        for key in ("exact_search_not_found", "outside_evolve_block", "evolve_marker_error")
        if int(failure_categories.get(key, 0) or 0)
    }
    if block_contract_failures:
        cards.append(
            _card(
                diagnostic_id="diag_evolve_block_contract_failure",
                bottleneck="evolve_block_contract_failure",
                severity="high",
                evidence=block_contract_failures,
                likely_causes=["SEARCH text came from the wrong body", "patch included marker or helper code"],
                target_surfaces=["signal", "ranking", "portfolio", "risk"],
                prompt_instruction="Keep the editable body slice strict and reject cross-surface SEARCH text.",
                avoid_actions=["do not repair by broadening the editable region"],
            )
        )
    if int(summary.get("duplicate_child_count", 0) or 0) or int(
        summary.get("duplicate_patch_fingerprint_count", 0) or 0
    ):
        cards.append(
            _card(
                diagnostic_id="diag_duplicate_generation",
                bottleneck="duplicate_generation",
                severity="medium",
                evidence={
                    "duplicate_child_count": summary.get("duplicate_child_count"),
                    "duplicate_patch_fingerprint_count": summary.get("duplicate_patch_fingerprint_count"),
                    "duplicate_retry_success_rate": summary.get("duplicate_retry_success_rate"),
                },
                likely_causes=["prompt lacks enough behavior-cell pressure", "model repeats a known easy patch"],
                target_surfaces=["signal", "ranking", "portfolio", "risk"],
                prompt_instruction="Use occupied MAP cells and forbidden-patch examples to force a distinct semantic change.",
                avoid_actions=["do not count duplicate children as search progress"],
            )
        )
    if int(summary.get("target_intent_mismatch_pass_count", 0) or 0):
        cards.append(
            _card(
                diagnostic_id="diag_target_intent_mismatch",
                bottleneck="target_intent_mismatch",
                severity="medium",
                evidence={
                    "target_intent_mismatch_pass_count": summary.get("target_intent_mismatch_pass_count"),
                    "target_intent_match_rate": summary.get("target_intent_match_rate"),
                },
                likely_causes=[
                    "model substituted an easier patch intent for the sampled MAP target",
                    "generic evaluator guidance overpowered target-cell instructions",
                ],
                target_surfaces=["signal", "ranking", "portfolio", "risk"],
                prompt_instruction=(
                    "Treat the intended_patch_intent as binding; a safe off-target child may still enter "
                    "the database, but it should lower prompt-card fitness."
                ),
                avoid_actions=["do not reward off-target patches as full target-cell successes"],
            )
        )
    weak_prompt_cards = _weak_prompt_card_rows(summary, limit=3)
    if weak_prompt_cards:
        cards.append(
            _card(
                diagnostic_id="diag_low_prompt_card_fitness",
                bottleneck="low_prompt_card_fitness",
                severity="medium",
                evidence={"weak_prompt_cards": weak_prompt_cards},
                likely_causes=[
                    "prompt card is associated with duplicate or invalid outputs",
                    "target intent may be too easy to satisfy with a repeated patch",
                ],
                target_surfaces=_target_surfaces_from_prompt_cards(weak_prompt_cards),
                prompt_instruction=(
                    "Treat low-fitness prompt cards as negative evidence and require a more specific "
                    "nonduplicate edit for the requested target intent."
                ),
                avoid_actions=["do not keep sampling a prompt card only because one prior child passed"],
            )
        )
    if int(failure_categories.get("portfolio_semantic_failed", 0) or 0):
        cards.append(
            _card(
                diagnostic_id="diag_portfolio_semantic_failures",
                bottleneck="portfolio_semantic_failures",
                severity="high",
                evidence={
                    "portfolio_semantic_failed": failure_categories.get("portfolio_semantic_failed"),
                    "portfolio_semantic_pass_rate": summary.get("portfolio_semantic_pass_rate"),
                },
                likely_causes=["patch may remove short book", "net exposure may be imbalanced"],
                target_surfaces=["portfolio", "risk", "signal", "ranking"],
                prompt_instruction="Preserve positive long weights, negative short weights, and near-zero net exposure.",
                avoid_actions=["do not use negative signal values as positive short-side denominators"],
            )
        )
    if int(summary.get("reasoning_only_empty_count", 0) or 0):
        cards.append(
            _card(
                diagnostic_id="diag_reasoning_only_empty_output",
                bottleneck="reasoning_only_empty_output",
                severity="high",
                evidence={
                    "reasoning_only_empty_count": summary.get("reasoning_only_empty_count"),
                    "max_initial_response_reasoning_length": summary.get("max_initial_response_reasoning_length"),
                },
                likely_causes=["Qwen thinking mode consumed completion budget without final content"],
                target_surfaces=["signal", "ranking", "portfolio", "risk"],
                prompt_instruction="Keep no-thinking routing and empty-content retry enabled.",
                avoid_actions=["do not solve this by increasing completion tokens alone"],
            )
        )
    if pass_count and _as_float(summary.get("unique_child_pass_rate")) not in {None, 1.0}:
        cards.append(
            _card(
                diagnostic_id="diag_unique_child_rate_below_one",
                bottleneck="unique_child_rate_below_one",
                severity="medium",
                evidence={"unique_child_pass_rate": summary.get("unique_child_pass_rate")},
                likely_causes=["valid patch duplicated an existing child or patch fingerprint"],
                target_surfaces=["signal", "ranking", "portfolio", "risk"],
                prompt_instruction="Sample underfilled MAP cells and include recent accepted patches as negative examples.",
            )
        )
    if not cards:
        cards.append(
            _card(
                diagnostic_id="diag_controller_no_major_bottleneck",
                bottleneck="no_major_controller_bottleneck_detected",
                severity="info",
                evidence={"attempt_count": attempt_count, "pass_count": pass_count},
                likely_causes=["controller-static gates passed on the observed batch"],
                target_surfaces=["signal", "ranking", "portfolio", "risk"],
                prompt_instruction="Review group-relative report before scaling or launching data-backed child evaluation.",
            )
        )
    return _report("controller_diagnostics", cards, source_path=source_path, attempts=attempts)


def _weak_prompt_card_rows(summary: dict[str, Any], *, limit: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    prompt_card_fitness = summary.get("prompt_card_fitness", {})
    if not isinstance(prompt_card_fitness, dict):
        return rows
    attempt_counts = summary.get("prompt_card_attempt_counts", {})
    duplicate_counts = summary.get("prompt_card_duplicate_counts", {})
    for prompt_card_id, fitness in prompt_card_fitness.items():
        if not isinstance(fitness, dict):
            continue
        attempt_count_value = attempt_counts.get(str(prompt_card_id)) if isinstance(attempt_counts, dict) else None
        attempts = int(_as_float(attempt_count_value) or 0)
        if attempts <= 0:
            continue
        fitness_score = _as_float(fitness.get("prompt_card_fitness_score"))
        duplicate_rate = _as_float(fitness.get("prompt_card_duplicate_rate"))
        lazy_penalty_sum = _as_float(fitness.get("prompt_card_lazy_penalty_sum"))
        hard_gate_risk = _as_float(fitness.get("prompt_card_hard_gate_risk"))
        duplicate_count_value = (
            duplicate_counts.get(str(prompt_card_id)) if isinstance(duplicate_counts, dict) else None
        )
        duplicate_count = int(_as_float(duplicate_count_value) or 0)
        if (
            (fitness_score is not None and fitness_score < 0.0)
            or (duplicate_rate is not None and duplicate_rate >= 0.5)
            or (lazy_penalty_sum is not None and lazy_penalty_sum < 0.0)
        ):
            rows.append(
                {
                    "prompt_card_id": str(prompt_card_id),
                    "attempt_count": attempts,
                    "duplicate_count": duplicate_count,
                    "fitness_score": fitness_score,
                    "duplicate_rate": duplicate_rate,
                    "lazy_penalty_sum": lazy_penalty_sum,
                    "hard_gate_risk": hard_gate_risk,
                }
            )
    rows.sort(
        key=lambda item: (
            item["fitness_score"] if item["fitness_score"] is not None else 0.0,
            -item["duplicate_count"],
            item["prompt_card_id"],
        )
    )
    return rows[: max(0, limit)]


def _target_surfaces_from_prompt_cards(rows: list[dict[str, Any]]) -> list[str]:
    surfaces: set[str] = set()
    for row in rows:
        parts = str(row.get("prompt_card_id") or "").split(":")
        if len(parts) >= 3 and parts[1]:
            surfaces.add(parts[1])
    return sorted(surfaces) or ["signal", "ranking", "portfolio", "risk"]


def _report(
    report_type: str,
    cards: list[dict[str, Any]],
    *,
    source_path: str | Path | None = None,
    attempts: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    ordered = sorted(cards, key=lambda item: (SEVERITY_ORDER.get(item["severity"], 99), item["diagnostic_id"]))
    return {
        "schema_version": DIAGNOSTIC_REPORT_SCHEMA_VERSION,
        "report_type": report_type,
        "created_at": utc_now_iso(),
        "source_path": str(source_path) if source_path else None,
        "diagnostic_cards": ordered,
        "diagnostic_card_count": len(ordered),
        "attempt_count": len(attempts or []),
    }


def retrieve_diagnostic_cards(
    cards: Iterable[dict[str, Any]],
    *,
    target_surface: str,
    limit: int = 4,
) -> list[dict[str, Any]]:
    """Return the most relevant diagnostic cards for a target evolve surface."""

    relevant = []
    for card in cards:
        surfaces = card.get("target_surfaces", [])
        if target_surface in surfaces or "any" in surfaces:
            relevant.append(card)
    relevant.sort(key=lambda item: (SEVERITY_ORDER.get(item.get("severity"), 99), item.get("diagnostic_id", "")))
    return relevant[: max(0, limit)]


def render_diagnostic_cards(cards: Iterable[dict[str, Any]]) -> str:
    """Render compact prompt cards for the diagnostic analyzer output."""

    lines: list[str] = []
    for card in cards:
        evidence = ", ".join(f"{key}={value}" for key, value in sorted(card.get("evidence", {}).items()))
        avoid = "; ".join(card.get("avoid_actions", [])[:3])
        lines.append(
            f"- [{card.get('severity')} | {card.get('bottleneck')}] {card.get('prompt_instruction')}"
        )
        if evidence:
            lines.append(f"  evidence: {evidence}")
        if avoid:
            lines.append(f"  avoid: {avoid}")
    return "\n".join(lines) if lines else "None."


def write_diagnostic_report(out_dir: str | Path, stem: str, report: dict[str, Any]) -> dict[str, str]:
    """Write diagnostic report JSON and Markdown artifacts."""

    path = Path(out_dir)
    path.mkdir(parents=True, exist_ok=True)
    json_path = path / f"{stem}.json"
    md_path = path / f"{stem}.md"
    write_json(json_path, report)
    md_path.write_text(_render_diagnostic_report_markdown(report), encoding="utf-8")
    return {"json": str(json_path), "markdown": str(md_path)}


def _render_diagnostic_report_markdown(report: dict[str, Any]) -> str:
    lines = [
        f"# {report.get('report_type', 'Diagnostic Report')}",
        "",
        f"- schema_version: `{report.get('schema_version')}`",
        f"- created_at: `{report.get('created_at')}`",
        f"- source_path: `{report.get('source_path')}`",
        f"- diagnostic_card_count: `{report.get('diagnostic_card_count')}`",
        "",
        "## Cards",
        "",
    ]
    for card in report.get("diagnostic_cards", []) or []:
        lines.extend(
            [
                f"### {card.get('diagnostic_id')}",
                "",
                f"- bottleneck: `{card.get('bottleneck')}`",
                f"- severity: `{card.get('severity')}`",
                f"- target_surfaces: `{card.get('target_surfaces')}`",
                f"- prompt_instruction: {card.get('prompt_instruction')}",
                f"- likely_causes: `{card.get('likely_causes')}`",
                f"- avoid_actions: `{card.get('avoid_actions')}`",
                f"- evidence: `{card.get('evidence')}`",
                "",
            ]
        )
    if not report.get("diagnostic_cards"):
        lines.append("- none")
    return "\n".join(lines)


__all__ = [
    "DIAGNOSTIC_REPORT_SCHEMA_VERSION",
    "build_controller_diagnostic_report",
    "build_evaluator_diagnostic_report",
    "render_diagnostic_cards",
    "retrieve_diagnostic_cards",
    "write_diagnostic_report",
]
