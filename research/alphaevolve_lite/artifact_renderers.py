"""Deterministic artifact renderers for controller smoke outputs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .paths import write_text


def _write_json(path: Path, payload: dict[str, Any]) -> Path:
    text = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    return write_text(path, text)


def render_prompt_card(
    out_dir: str | Path,
    *,
    program_id: str,
    parent_id: str | None,
    generation: int,
    island: str,
    mutation_surface: str,
    data_scope: str,
    allowed_surfaces: list[str],
    forbidden_changes: list[str],
    evaluator_feedback_summary: str,
    inspiration_programs: list[dict[str, Any]],
    strict_output_contract: str,
) -> dict[str, Path]:
    """Write a prompt card as JSON and Markdown."""

    out = Path(out_dir)
    payload = {
        "program_id": program_id,
        "parent_id": parent_id,
        "generation": generation,
        "island": island,
        "mutation_surface": mutation_surface,
        "data_scope": data_scope,
        "allowed_surfaces": allowed_surfaces,
        "forbidden_changes": forbidden_changes,
        "evaluator_feedback_summary": evaluator_feedback_summary,
        "inspiration_programs": inspiration_programs,
        "strict_output_contract": strict_output_contract,
    }
    json_path = _write_json(out / "prompt_card.json", payload)
    md = [
        f"# Program Card: {program_id}",
        "",
        f"- parent: {parent_id}",
        f"- generation: {generation}",
        f"- island: {island}",
        f"- mutation surface: {mutation_surface}",
        f"- data scope: {data_scope}",
        "",
        "## Allowed Surfaces",
        "",
        *[f"- {item}" for item in allowed_surfaces],
        "",
        "## Forbidden Changes",
        "",
        *[f"- {item}" for item in forbidden_changes],
        "",
        "## Evaluator Feedback Summary",
        "",
        evaluator_feedback_summary,
        "",
        "## Inspiration Programs",
        "",
        *[f"- {item.get('program_id', 'unknown')}: {item.get('summary', '')}" for item in inspiration_programs],
        "",
        "## Strict Output Contract",
        "",
        strict_output_contract,
        "",
    ]
    md_path = write_text(out / "prompt_card.md", "\n".join(md))
    return {"json": json_path, "markdown": md_path}


def render_evaluator_summary(
    out_dir: str | Path,
    *,
    program_id: str,
    stage: str,
    hard_gates: dict[str, Any],
    metrics: dict[str, Any],
    descriptors: dict[str, Any],
    decision: str,
    failure_reason: str | None,
    next_prompt_hint: str,
    artifact_paths: dict[str, str],
) -> dict[str, Path]:
    """Write an evaluator summary as JSON and Markdown."""

    out = Path(out_dir)
    payload = {
        "schema_version": "phase4_evaluator_summary_v1",
        "program_id": program_id,
        "stage": stage,
        "hard_gates": hard_gates,
        "metrics": metrics,
        "descriptors": descriptors,
        "decision": decision,
        "failure_reason": failure_reason,
        "next_prompt_hint": next_prompt_hint,
        "artifact_paths": artifact_paths,
    }
    json_path = _write_json(out / "evaluator_summary.json", payload)
    md = [
        f"# Evaluator Summary: {program_id}",
        "",
        f"- stage: {stage}",
        f"- decision: {decision}",
        f"- failure reason: {failure_reason}",
        "",
        "## Hard Gates",
        "",
        *[f"- {key}: {value}" for key, value in sorted(hard_gates.items())],
        "",
        "## Metrics",
        "",
        *[f"- {key}: {value}" for key, value in sorted(metrics.items())],
        "",
        "## Next Prompt Hint",
        "",
        next_prompt_hint,
        "",
    ]
    md_path = write_text(out / "evaluator_summary.md", "\n".join(md))
    return {"json": json_path, "markdown": md_path}


def render_failure_report(
    out_dir: str | Path,
    *,
    failure_category: str,
    exact_gate: str,
    minimal_reproduction: str,
    repair_allowed: bool,
    next_prompt_hint: str,
    usable_as_inspiration: bool,
) -> Path:
    """Write a standard failure report."""

    md = f"""# Failure Report

## Failure Category

{failure_category}

## Exact Gate That Failed

{exact_gate}

## Minimal Reproduction

{minimal_reproduction}

## Whether Repair Is Allowed

{repair_allowed}

## Next Prompt Hint

{next_prompt_hint}

## Whether This Failure Can Be Used As Inspiration

{usable_as_inspiration}
"""
    return write_text(Path(out_dir) / "failure_report.md", md)


def render_controller_static_report(
    out_dir: str | Path,
    *,
    run_id: str,
    config_path: str,
    db_path: str,
    audit_log_path: str,
    checks: dict[str, bool],
) -> Path:
    """Write the controller_static smoke report."""

    md = [
        f"# Controller Static Report: {run_id}",
        "",
        f"- config: {config_path}",
        f"- database: {db_path}",
        f"- audit log: {audit_log_path}",
        "",
        "## Checks",
        "",
        *[f"- {key}: {value}" for key, value in sorted(checks.items())],
        "",
        "## Execution Boundary",
        "",
        "No LLM endpoint was called. No heavy CSV data was loaded.",
        "",
    ]
    return write_text(Path(out_dir) / "controller_static_report.md", "\n".join(md))
