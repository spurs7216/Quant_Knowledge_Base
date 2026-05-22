"""Use a medium Qwen reviewer to propose mechanism cards, not code patches."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def _ensure_repo_import() -> None:
    repo_root = Path(__file__).resolve().parents[3]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build 27B-reviewed mechanism cards for child generation.")
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--controller-summary", action="append", default=[])
    parser.add_argument("--sample-eval-summary", action="append", default=[])
    parser.add_argument("--project-note", action="append", default=[])
    parser.add_argument("--model-role", default="medium_quality_reviewer")
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=8192,
        help=(
            "Completion-token budget for JSON mechanism cards. "
            "vLLM max-model-len must cover prompt tokens plus this value."
        ),
    )
    parser.add_argument("--card-limit", type=int, default=6)
    parser.add_argument(
        "--mock-response-path",
        default="",
        help="Local test hook: parse this response instead of calling vLLM.",
    )
    return parser.parse_args()


def load_json(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def compact_controller_summary(path: str) -> dict[str, Any]:
    payload = load_json(path)
    summary = payload.get("summary", payload)
    attempts = payload.get("attempts", [])
    return {
        "path": path,
        "attempt_count": summary.get("attempt_count"),
        "pass_count": summary.get("pass_count"),
        "failure_categories": summary.get("failure_categories"),
        "behavioral_noop_count": summary.get("behavioral_noop_count"),
        "sample_eval_candidate_program_ids": summary.get("sample_eval_candidate_program_ids"),
        "target_intent_match_rate": summary.get("target_intent_match_rate"),
        "unique_child_pass_rate": summary.get("unique_child_pass_rate"),
        "prompt_card_reroute_policy": _compact_reroute(summary.get("prompt_card_reroute_policy", {})),
        "pass_attempts": [
            {
                "attempt": item.get("attempt"),
                "program_id": item.get("program_id"),
                "surface": item.get("target_surface"),
                "target_intent": item.get("target_intent"),
                "patch_intent": item.get("patch_intent"),
                "target_intent_match": item.get("target_intent_match"),
                "sample_eval_eligible": item.get("sample_eval_eligible"),
                "sample_eval_eligibility_reasons": item.get("sample_eval_eligibility_reasons"),
                "weight_max_abs_delta": (item.get("behavior_delta_metrics") or {}).get("weight_max_abs_delta"),
                "active_position_jaccard": (item.get("behavior_delta_metrics") or {}).get(
                    "active_position_jaccard"
                ),
            }
            for item in attempts
            if item.get("decision") == "pass"
        ],
    }


def compact_sample_eval_summary(path: str) -> dict[str, Any]:
    payload = load_json(path)
    metrics = payload.get("metrics", {})
    comparison = payload.get("reference_comparison", {})
    return {
        "path": path,
        "decision": payload.get("decision"),
        "program_id": payload.get("program_id"),
        "parent_program_id": payload.get("parent_program_id"),
        "hard_gates": payload.get("hard_gates"),
        "search_sample": _metric_subset(metrics.get("search_sample", {})),
        "in_sample": _metric_subset(metrics.get("in_sample", metrics.get("train", {}))),
        "out_sample": _metric_subset(metrics.get("out_sample", metrics.get("validation", {}))),
        "is_os_degradation": _metric_subset(metrics.get("is_os_degradation", {})),
        "reference_metrics": {
            key: value
            for key, value in (comparison.get("metrics") or {}).items()
            if key
            in {
                "annualized_return",
                "sharpe",
                "turnover",
                "turnover_aware_score",
                "max_drawdown",
                "max_missing_held_weight",
                "mean_daily_n_names",
            }
        },
    }


def build_prompt(args: argparse.Namespace) -> dict[str, str]:
    from research.alphaevolve_lite.mechanism_cards import mechanism_card_contract_context

    controller_summaries = [compact_controller_summary(path) for path in args.controller_summary]
    sample_eval_summaries = [compact_sample_eval_summary(path) for path in args.sample_eval_summary]
    contract_context = mechanism_card_contract_context()
    notes = []
    for path in args.project_note:
        note_path = Path(path)
        text = note_path.read_text(encoding="utf-8")
        notes.append({"path": path, "text": text[:6000]})

    schema = {
        "schema_version": "phase4_mechanism_cards_v1",
        "review_summary": "brief parent-relative diagnosis",
        "cards": [
            {
                "card_id": "short_stable_id",
                "surface": "exact allowed surface from contract_context",
                "intent": "exact allowed intent for that surface from contract_context",
                "priority": 0.0,
                "status": "active",
                "thesis": "why this mechanism is worth one 9B controller attempt",
                "expected_effect": "observable final-weight or rank effect",
                "required_data_fields": ["exact handles from contract_context.allowed_required_data_fields"],
                "implementation_hints": ["plain-language hints only, no code"],
                "avoid": ["known bad or leakage-prone actions"],
                "sample_eval_hypothesis": "what should improve parent-relative metrics",
                "evidence": {"supporting_artifacts": ["path or program id"]},
            }
        ],
    }
    system = (
        "You are a quant research search-state reviewer. Output JSON only. "
        "Do not output code, diffs, SEARCH/REPLACE blocks, markdown, or prose outside JSON."
    )
    user = (
        "Review the Phase 4 AlphaEvolve-lite evidence and propose mechanism cards for a later 9B "
        "controller-only child-generation run. The cards are mechanism hypotheses, not direct code.\n\n"
        "Rules:\n"
        "- Use only daily_stock_contract_v1 fields and ex-ante information.\n"
        "- Do not use forward-return availability fields or future-return filters.\n"
        "- Use exact surface and intent names from the contract context; do not invent loose intents.\n"
        "- Use exact required_data_fields handles such as CONTRACT.industry_primary, CONTRACT.dollar_volume, and signal.\n"
        "- Do not use loose field names such as industry_code, avg_daily_volume, returns_1d, or signal_raw.\n"
        "- Do not promote attempt009; it improved turnover and missing-held behavior but weakened parent-relative Sharpe/return.\n"
        "- Prefer mechanisms that can improve parent-relative economics while preserving the missing-held and turnover gains.\n"
        "- Avoid no-op portfolio/risk edits and generic signal dampening.\n"
        "- Parent-zoo update: seed-zoo evidence shows gross reversal structure before costs, but daily turnover consumes it. Prefer cost-aware preservation over completely new raw reversal definitions.\n"
        "- Include regime-aware or HMM-style ideas only as causal lightweight state mechanisms that can fit inside one EVOLVE block; do not ask the 9B patcher to add unrestricted full-sample HMM fitting.\n"
        "- Return at most "
        f"{args.card_limit} cards.\n\n"
        "Mechanism-card contract context:\n"
        f"{json.dumps(contract_context, indent=2, sort_keys=True)}\n\n"
        "Required JSON schema:\n"
        f"{json.dumps(schema, indent=2, sort_keys=True)}\n\n"
        "Controller summaries:\n"
        f"{json.dumps(controller_summaries, indent=2, sort_keys=True)}\n\n"
        "Sample-eval summaries:\n"
        f"{json.dumps(sample_eval_summaries, indent=2, sort_keys=True)}\n\n"
        "Project notes:\n"
        f"{json.dumps(notes, indent=2, sort_keys=True)}\n"
    )
    return {"system": system, "user": user}


def main() -> int:
    _ensure_repo_import()
    from research.alphaevolve_lite.artifact_io import write_json
    from research.alphaevolve_lite.controller_batch_artifacts import write_messages
    from research.alphaevolve_lite.mechanism_cards import (
        extract_json_object,
        normalize_mechanism_cards,
        render_mechanism_cards,
    )
    from research.alphaevolve_lite.model_router import chat_completion
    from research.alphaevolve_lite.reproducibility import capture_git_reproducibility

    args = parse_args()
    if args.card_limit <= 0:
        print("--card-limit must be positive", file=sys.stderr)
        return 2
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    git_status = capture_git_reproducibility(out_dir)
    messages = build_prompt(args)
    write_messages(out_dir / "prompt", "27B Mechanism Card Prompt", messages)

    if args.mock_response_path:
        raw_output = Path(args.mock_response_path).read_text(encoding="utf-8")
        response_record = {
            "role": "mock_medium_review",
            "served_model_name": "mock",
            "content": raw_output,
        }
    else:
        response_record = chat_completion(
            role=args.model_role,
            system_prompt=messages["system"],
            user_prompt=messages["user"],
            temperature=args.temperature,
            max_tokens=args.max_tokens,
            verify=True,
        )
        raw_output = str(response_record.get("content") or "")

    (out_dir / "raw_output.txt").write_text(raw_output, encoding="utf-8")
    write_json(out_dir / "model_response.json", response_record)
    truncation_error = _length_truncation_error(response_record, args.max_tokens)
    if truncation_error:
        write_json(out_dir / "mechanism_card_error.json", truncation_error)
        print(json.dumps(truncation_error, sort_keys=True), file=sys.stderr)
        return 1
    try:
        payload = extract_json_object(raw_output)
        normalized = normalize_mechanism_cards(payload)
    except Exception as exc:
        parse_error = {
            "status": "invalid_mechanism_cards",
            "error_type": exc.__class__.__name__,
            "message": str(exc),
            "max_tokens": args.max_tokens,
            "remediation": (
                "Inspect raw_output.txt. If model_response.json finish_reason is length, "
                "rerun with higher --max-tokens and a vLLM --max-model-len large enough "
                "for prompt tokens plus completion tokens. Otherwise tighten the JSON-only prompt."
            ),
        }
        write_json(out_dir / "mechanism_card_error.json", parse_error)
        print(json.dumps(parse_error, sort_keys=True), file=sys.stderr)
        return 1
    normalized.update(
        {
            "source_model_role": args.model_role,
            "controller_summary_paths": args.controller_summary,
            "sample_eval_summary_paths": args.sample_eval_summary,
            "project_note_paths": args.project_note,
            **git_status,
        }
    )
    cards = normalized["cards"][: args.card_limit]
    normalized["cards"] = cards
    write_json(out_dir / "mechanism_cards.json", normalized)
    (out_dir / "mechanism_cards.md").write_text(
        "# 27B Mechanism Cards\n\n" + render_mechanism_cards(cards) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"status": "ok", "out_dir": str(out_dir), "card_count": len(cards)}, sort_keys=True))
    return 0


def _compact_reroute(policy: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value
        for key, value in policy.items()
        if isinstance(value, dict) and value.get("prompt_card_reroute_reasons")
    }


def _length_truncation_error(response_record: dict[str, Any], max_tokens: int) -> dict[str, Any] | None:
    raw_response = response_record.get("raw_response")
    if not isinstance(raw_response, dict):
        return None
    choices = raw_response.get("choices") or []
    if not choices or not isinstance(choices[0], dict):
        return None
    finish_reason = choices[0].get("finish_reason")
    if finish_reason != "length":
        return None
    usage = raw_response.get("usage", {}) if isinstance(raw_response.get("usage"), dict) else {}
    return {
        "status": "incomplete_generation",
        "error_type": "finish_reason_length",
        "message": "The 27B response hit the completion-token limit and may be truncated.",
        "finish_reason": finish_reason,
        "max_tokens": max_tokens,
        "prompt_tokens": usage.get("prompt_tokens"),
        "completion_tokens": usage.get("completion_tokens"),
        "total_tokens": usage.get("total_tokens"),
        "remediation": (
            "Increase build_mechanism_cards.py --max-tokens and launch vLLM with "
            "--max-model-len at least prompt_tokens plus the requested completion budget."
        ),
    }


def _metric_subset(metrics: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "annualized_return",
        "sharpe",
        "turnover",
        "turnover_aware_score",
        "max_drawdown",
        "max_missing_held_weight",
        "mean_missing_held_weight",
        "max_weight",
        "mean_daily_n_names",
        "mean_daily_long_count",
        "mean_daily_short_count",
        "os_minus_is_annualized_return",
        "os_minus_is_sharpe",
        "os_minus_is_turnover",
        "os_minus_is_turnover_aware_score",
        "is_to_os_sharpe_degradation",
    ]
    return {key: metrics.get(key) for key in keys if key in metrics}


if __name__ == "__main__":
    raise SystemExit(main())
