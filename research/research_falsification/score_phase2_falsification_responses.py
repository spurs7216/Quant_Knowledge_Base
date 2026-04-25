"""
Score Phase 2 falsification responses against a local answer key.

Example:
    python research/research_falsification/score_phase2_falsification_responses.py \
        --responses path/to/responses.csv \
        --answer-key projects/quant_research_system/phase2_research_falsification/task_002_answer_key.csv \
        --output-dir artifacts/phase2_scored_falsification/20260424_example
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd


REQUIRED_RESPONSE_COLUMNS = [
    "task_id",
    "task_name",
    "agent_decision",
    "decision_summary",
    "memo_path",
    "evidence_path",
    "reviewer_notes",
]

REQUIRED_ANSWER_KEY_COLUMNS = [
    "task_id",
    "task_name",
    "task_bank_version",
    "task_class",
    "canonical_expected_decision",
    "acceptable_decisions",
    "false_accept_if_agent_decision",
    "statistical_gate",
    "leakage_gate",
    "implementation_gate",
    "primary_failure_reason",
    "evidence_path",
]

ALLOWED_DECISIONS = {"reject", "revise", "proceed"}
PROJECT_PHASE2_DIR = Path("projects/quant_research_system/phase2_research_falsification").resolve()


def ensure_columns(df: pd.DataFrame, required: list[str], label: str) -> None:
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"{label} is missing required columns: {missing}")


def parse_choices(value: Any) -> list[str]:
    if pd.isna(value):
        return []
    return [part.strip() for part in str(value).split("|") if part.strip()]


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2, allow_nan=False), encoding="utf-8")


def assert_response_path_allowed(path: Path) -> None:
    resolved = path.resolve()
    if resolved.name.endswith("_response_template.csv"):
        raise ValueError("responses file must be a run-local copy, not the reusable response template")
    try:
        if resolved.is_relative_to(PROJECT_PHASE2_DIR):
            raise ValueError("responses file must live outside the phase2 project folder; use an artifact-local run folder")
    except AttributeError:
        if str(resolved).startswith(str(PROJECT_PHASE2_DIR)):
            raise ValueError("responses file must live outside the phase2 project folder; use an artifact-local run folder")


def assert_nonempty_text(df: pd.DataFrame, columns: list[str]) -> None:
    for column in columns:
        bad = df[column].astype(str).str.strip().eq("") | df[column].isna()
        if bad.any():
            tasks = df.loc[bad, "task_id"].tolist()
            raise ValueError(f"responses contain blank {column} for tasks: {tasks}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--responses", type=Path, required=True)
    parser.add_argument("--answer-key", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    assert_response_path_allowed(args.responses)
    responses = pd.read_csv(args.responses)
    answer_key = pd.read_csv(args.answer_key)
    ensure_columns(responses, REQUIRED_RESPONSE_COLUMNS, "responses")
    ensure_columns(answer_key, REQUIRED_ANSWER_KEY_COLUMNS, "answer key")
    assert_nonempty_text(responses, ["agent_decision", "decision_summary", "evidence_path"])

    merged = answer_key.merge(
        responses,
        on=["task_id", "task_name"],
        how="left",
        suffixes=("_expected", "_response"),
        validate="one_to_one",
    )

    if merged["agent_decision"].isna().any():
        missing_tasks = merged.loc[merged["agent_decision"].isna(), "task_id"].tolist()
        raise ValueError(f"responses missing agent_decision for tasks: {missing_tasks}")

    merged["agent_decision"] = merged["agent_decision"].astype(str).str.strip().str.lower()
    invalid = sorted(set(merged.loc[~merged["agent_decision"].isin(ALLOWED_DECISIONS), "agent_decision"]))
    if invalid:
        raise ValueError(f"responses contain invalid agent_decision values: {invalid}")

    acceptable = merged["acceptable_decisions"].map(parse_choices)
    merged["strict_decision_correct"] = merged["agent_decision"].eq(merged["canonical_expected_decision"])
    merged["tolerant_decision_correct"] = [decision in accepted for decision, accepted in zip(merged["agent_decision"], acceptable)]
    merged["false_accept"] = [
        decision == false_accept and false_accept not in accepted
        for decision, false_accept, accepted in zip(
            merged["agent_decision"],
            merged["false_accept_if_agent_decision"],
            acceptable,
        )
    ]
    merged["boundary_task"] = merged["task_class"].eq("boundary")
    merged["acceptable_decisions_count"] = [len(accepted) for accepted in acceptable]

    output = merged[
        [
            "task_id",
            "task_name",
            "task_bank_version",
            "task_class",
            "boundary_task",
            "canonical_expected_decision",
            "acceptable_decisions",
            "agent_decision",
            "strict_decision_correct",
            "tolerant_decision_correct",
            "false_accept",
            "statistical_gate",
            "leakage_gate",
            "implementation_gate",
            "primary_failure_reason",
            "decision_summary",
            "memo_path",
            "evidence_path_response",
            "reviewer_notes",
        ]
    ].rename(columns={"evidence_path_response": "agent_evidence_path"})

    args.output_dir.mkdir(parents=True, exist_ok=True)
    output.to_csv(args.output_dir / "scored_scorecard.csv", index=False)

    task_count = int(len(output))
    hard_reject_mask = output["task_class"].eq("hard_reject")
    boundary_mask = output["boundary_task"]
    hard_proceed_mask = output["task_class"].eq("hard_proceed")
    false_accept_count = int(output["false_accept"].sum())
    metrics = {
        "task_count": task_count,
        "strict_accuracy": float(output["strict_decision_correct"].mean() * 100.0),
        "tolerant_accuracy": float(output["tolerant_decision_correct"].mean() * 100.0),
        "false_accept_count": false_accept_count,
        "false_accept_rate": float(false_accept_count / max(task_count, 1) * 100.0),
        "hard_reject_accuracy": float(output.loc[hard_reject_mask, "tolerant_decision_correct"].mean() * 100.0)
        if int(hard_reject_mask.sum())
        else None,
        "boundary_accuracy": float(output.loc[boundary_mask, "tolerant_decision_correct"].mean() * 100.0)
        if int(boundary_mask.sum())
        else None,
        "hard_proceed_accuracy": float(output.loc[hard_proceed_mask, "tolerant_decision_correct"].mean() * 100.0)
        if int(hard_proceed_mask.sum())
        else None,
        "decision_distribution": output["agent_decision"].value_counts().sort_index().to_dict(),
    }
    write_json(args.output_dir / "metrics.json", metrics)

    lines = [
        "# Phase 2 Scored Falsification Report",
        "",
        "## Summary",
        "",
        f"- task_count: `{task_count}`",
        f"- strict_accuracy: `{metrics['strict_accuracy']:.2f}`",
        f"- tolerant_accuracy: `{metrics['tolerant_accuracy']:.2f}`",
        f"- false_accept_count: `{false_accept_count}`",
    ]
    if metrics["hard_reject_accuracy"] is not None:
        lines.append(f"- hard_reject_accuracy: `{metrics['hard_reject_accuracy']:.2f}`")
    if metrics["boundary_accuracy"] is not None:
        lines.append(f"- boundary_accuracy: `{metrics['boundary_accuracy']:.2f}`")
    if metrics["hard_proceed_accuracy"] is not None:
        lines.append(f"- hard_proceed_accuracy: `{metrics['hard_proceed_accuracy']:.2f}`")
    lines.extend(["", "## Per-Task Results", ""])
    for row in output.itertuples():
        lines.append(
            f"- `{row.task_id}`: agent `{row.agent_decision}` vs canonical `{row.canonical_expected_decision}`; "
            f"strict=`{str(bool(row.strict_decision_correct)).lower()}`, "
            f"tolerant=`{str(bool(row.tolerant_decision_correct)).lower()}`, "
            f"false_accept=`{str(bool(row.false_accept)).lower()}`"
        )
    (args.output_dir / "score_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
