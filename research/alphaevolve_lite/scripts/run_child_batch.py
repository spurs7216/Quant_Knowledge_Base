"""Run a small remote Qwen child-generation controller dry run."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


DEFAULT_MAX_COMPLETION_TOKENS = 8192


def _ensure_repo_import() -> None:
    repo_root = Path(__file__).resolve().parents[3]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run controller-static child generation attempts.")
    parser.add_argument(
        "--program-path",
        default="research/alphaevolve_lite/seeds/kalman_reversal_seed.py",
    )
    parser.add_argument("--evaluator-summary", default="")
    parser.add_argument("--out-dir", default="artifacts/phase4_alphaevolve/controller_batch_001")
    parser.add_argument("--db-path", default="")
    parser.add_argument("--attempts", type=int, default=5)
    parser.add_argument("--model-role", default="fast_generator")
    parser.add_argument("--temperature-grid", default="0.0,0.2,0.5")
    parser.add_argument(
        "--surface-schedule",
        default="signal,ranking,portfolio,risk",
        help=(
            "Comma-separated target-surface schedule. Use this for diversity top-up "
            "runs without changing seed code or prompt contracts."
        ),
    )
    parser.add_argument(
        "--prior-summary",
        action="append",
        default=[],
        help=(
            "Prior controller summary.json used to seed duplicate hashes, patch "
            "fingerprints, occupied MAP cells, and accepted patch examples. May be repeated."
        ),
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=DEFAULT_MAX_COMPLETION_TOKENS,
        help=(
            "Maximum completion tokens requested from vLLM. The remote server's "
            "max-model-len must exceed prompt tokens plus this value."
        ),
    )
    parser.add_argument("--empty-retry-attempts", type=int, default=1)
    parser.add_argument(
        "--duplicate-retry-attempts",
        type=int,
        default=1,
        help="Retry once when a controller-pass child duplicates an earlier child or patch fingerprint.",
    )
    parser.add_argument(
        "--population-policy-version",
        choices=["v1", "v2"],
        default="v2",
        help=(
            "v2 enables deterministic population-policy context, intent de-saturation, "
            "prompt-card counters, and near-duplicate edit-signature checks."
        ),
    )
    parser.add_argument(
        "--near-duplicate-threshold",
        type=float,
        default=0.88,
        help="Jaccard threshold for deterministic edit-signature near-duplicate rejection under policy v2.",
    )
    parser.add_argument(
        "--disable-near-duplicate-check",
        action="store_true",
        help="Disable policy-v2 near-duplicate edit-signature rejection while keeping policy context.",
    )
    parser.add_argument(
        "--memory-path",
        default="artifacts/phase4_alphaevolve/reasoning_memory/memory_items.jsonl",
        help="JSONL reasoning-memory bank used for prompt cards.",
    )
    parser.add_argument("--memory-card-limit", type=int, default=3)
    parser.add_argument("--disable-reasoning-memory", action="store_true")
    parser.add_argument("--diagnostic-card-limit", type=int, default=4)
    parser.add_argument(
        "--skill-library-path",
        default="artifacts/phase4_alphaevolve/skill_library/skill_items.jsonl",
        help="JSONL explicit skill library used for prompt skill cards.",
    )
    parser.add_argument("--skill-card-limit", type=int, default=3)
    parser.add_argument("--disable-skill-library", action="store_true")
    parser.add_argument("--program-id-prefix", default="PROG-20260430-CHILD")
    parser.add_argument(
        "--mock-patch-mode",
        choices=["none", "sign_flip", "marker_oversize", "portfolio_long_only", "no_valid_patch"],
        default="none",
    )
    parser.add_argument("--no-repair", action="store_true", help="Disable one-shot critic repair.")
    return parser.parse_args()


def main() -> int:
    _ensure_repo_import()
    from research.alphaevolve_lite.controller_batch_artifacts import (
        summarize_attempts,
        write_json,
        write_messages,
        write_summary_markdown,
    )
    from research.alphaevolve_lite.controller_batch_filter import (
        PatchFilterConfig,
        filter_patch_with_optional_repair,
    )
    from research.alphaevolve_lite.controller_batch_mocks import mock_patch
    from research.alphaevolve_lite.controller_batch_state import (
        load_prior_attempts,
        parse_surface_schedule,
        seed_controller_search_state,
    )
    from research.alphaevolve_lite.controller_population_policy import (
        DEFAULT_PARENT_PROGRAM_ID,
        NEAR_DUPLICATE_FAILURE_CATEGORY,
        POPULATION_POLICY_VERSION,
        PROMPT_FITNESS_POLICY_VERSION,
        check_patch_novelty,
        choose_population_diversity_target,
        controller_search_score_for_attempt,
        format_population_policy_context,
        lazy_penalty_for_attempt,
        prompt_card_id_for,
        seed_population_policy_state,
    )
    from research.alphaevolve_lite.controller_prompt_context import build_controller_prompt_context
    from research.alphaevolve_lite.diversity import (
        choose_diversity_target,
        patch_diversity_descriptor,
    )
    from research.alphaevolve_lite.diagnostic_analyzer import (
        build_controller_diagnostic_report,
        build_evaluator_diagnostic_report,
        write_diagnostic_report,
    )
    from research.alphaevolve_lite.model_router import chat_completion
    from research.alphaevolve_lite.program_database import init_db, insert_program_record
    from research.alphaevolve_lite.prompt_builder import (
        build_child_generation_prompt,
        choose_target_surface,
        extract_evolve_block_bodies,
        load_json_if_exists,
        write_prompt_artifact,
    )
    from research.alphaevolve_lite.reasoning_memory import (
        append_memory_update,
        bootstrap_default_memory_bank,
        build_controller_batch_memory_update,
        write_memory_update,
    )
    from research.alphaevolve_lite.skill_library import (
        append_skill_update,
        bootstrap_default_skill_library,
        build_controller_batch_skill_update,
        write_skill_update,
    )

    args = parse_args()
    if args.attempts <= 0:
        print("--attempts must be positive", file=sys.stderr)
        return 2
    if not 0.0 < args.near_duplicate_threshold <= 1.0:
        print("--near-duplicate-threshold must be in (0, 1]", file=sys.stderr)
        return 2

    program_path = Path(args.program_path)
    if not program_path.exists():
        print(f"program path does not exist: {program_path}", file=sys.stderr)
        return 2
    parent_text = program_path.read_text(encoding="utf-8")
    try:
        surface_schedule = parse_surface_schedule(
            args.surface_schedule,
            available_surfaces=extract_evolve_block_bodies(parent_text),
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    evaluator_summary = load_json_if_exists(args.evaluator_summary)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    evaluator_diagnostic_report = build_evaluator_diagnostic_report(
        evaluator_summary,
        source_path=args.evaluator_summary or None,
    )
    evaluator_diagnostic_paths = write_diagnostic_report(
        out_dir,
        "evaluator_diagnostic_report",
        evaluator_diagnostic_report,
    )
    temperatures = [float(item.strip()) for item in args.temperature_grid.split(",") if item.strip()]
    if not temperatures:
        temperatures = [0.2]
    if args.db_path:
        init_db(args.db_path)
    memory_path = None if args.disable_reasoning_memory else Path(args.memory_path)
    reasoning_memory_items: list[dict[str, Any]] = []
    retrieved_memory_ids_seen: set[str] = set()
    if memory_path is not None:
        reasoning_memory_items = bootstrap_default_memory_bank(memory_path)
        write_json(
            out_dir / "reasoning_memory_loaded.json",
            {
                "memory_path": str(memory_path),
                "memory_item_count": len(reasoning_memory_items),
                "active_memory_item_count": sum(
                    1 for item in reasoning_memory_items if item.get("status") == "active"
                ),
                "memory_item_ids": [item.get("memory_item_id") for item in reasoning_memory_items],
            },
        )
    skill_library_path = None if args.disable_skill_library else Path(args.skill_library_path)
    skill_items: list[dict[str, Any]] = []
    retrieved_skill_ids_seen: set[str] = set()
    if skill_library_path is not None:
        skill_items = bootstrap_default_skill_library(skill_library_path)
        write_json(
            out_dir / "skill_library_loaded.json",
            {
                "skill_library_path": str(skill_library_path),
                "skill_item_count": len(skill_items),
                "active_skill_item_count": sum(1 for item in skill_items if item.get("status") == "active"),
                "skill_ids": [item.get("skill_id") for item in skill_items],
            },
        )
    patch_filter_config = PatchFilterConfig(
        parent_text=parent_text,
        no_repair=args.no_repair,
        mock_patch_mode=args.mock_patch_mode,
        max_tokens=args.max_tokens,
    )

    def describe_pass_candidate(
        *,
        result: Any,
        final_diff_text: str,
        target_surface: str,
    ) -> dict[str, Any]:
        child_hash = None
        if result.child_text is not None:
            child_hash = hashlib.sha256(result.child_text.encode("utf-8")).hexdigest()
        if result.decision != "pass":
            return {
                "child_hash": child_hash,
                "diversity_descriptor": {},
                "patch_fingerprint": None,
                "map_cell_key": None,
            }
        diversity_descriptor = patch_diversity_descriptor(
            final_diff_text,
            target_surface,
            result.vector_smoke_metrics,
        )
        return {
            "child_hash": child_hash,
            "diversity_descriptor": diversity_descriptor,
            "patch_fingerprint": diversity_descriptor.get("patch_fingerprint"),
            "map_cell_key": diversity_descriptor.get("map_cell_key"),
        }

    try:
        prior_attempt_records = load_prior_attempts(args.prior_summary)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"failed to load prior summary: {exc}", file=sys.stderr)
        return 2
    search_state = seed_controller_search_state(prior_attempt_records)
    population_policy_enabled = args.population_policy_version == "v2"
    near_duplicate_check_enabled = population_policy_enabled and not args.disable_near_duplicate_check
    population_policy_state = seed_population_policy_state(
        prior_attempt_records,
        default_parent_id=DEFAULT_PARENT_PROGRAM_ID,
    )

    attempt_records: list[dict[str, Any]] = []
    seen_child_hashes = search_state.seen_child_hashes
    seen_patch_fingerprints = search_state.seen_patch_fingerprints
    occupied_map_cells = search_state.occupied_map_cells
    occupied_target_labels_by_surface = search_state.occupied_target_labels_by_surface
    accepted_patches_by_surface = search_state.accepted_patches_by_surface
    prior_seen_child_hash_count = len(seen_child_hashes)
    for attempt in range(args.attempts):
        attempt_dir = out_dir / f"attempt_{attempt:03d}"
        attempt_dir.mkdir(parents=True, exist_ok=True)
        temperature = temperatures[attempt % len(temperatures)]
        parent_id = DEFAULT_PARENT_PROGRAM_ID
        target_surface = choose_target_surface(attempt, surface_schedule=surface_schedule)
        if population_policy_enabled:
            diversity_target = choose_population_diversity_target(
                population_policy_state,
                target_surface,
                attempt,
                occupied_labels=occupied_target_labels_by_surface.get(target_surface, set()),
            )
        else:
            diversity_target = choose_diversity_target(
                target_surface,
                attempt,
                occupied_labels=occupied_target_labels_by_surface.get(target_surface, set()),
            )
        target_intent = diversity_target.intent if diversity_target else "other"
        prompt_card_id = prompt_card_id_for(target_surface, target_intent)
        if population_policy_enabled:
            population_policy_snapshot = population_policy_state.target_snapshot(
                parent_id=parent_id,
                surface=target_surface,
                target=diversity_target,
                prompt_card_id=prompt_card_id,
            )
            population_policy_text = format_population_policy_context(
                population_policy_state,
                parent_id=parent_id,
                surface=target_surface,
                target=diversity_target,
                prompt_card_id=prompt_card_id,
                near_duplicate_threshold=args.near_duplicate_threshold,
            )
        else:
            population_policy_snapshot = {
                "population_policy_version": "v1",
                "parent_id": parent_id,
                "parent_offspring_count": 0,
                "target_surface": target_surface,
                "target_intent": target_intent,
                "target_cell_label": diversity_target.cell_label if diversity_target else None,
                "prompt_card_id": prompt_card_id,
            }
            population_policy_text = "Population policy v2 is disabled; using explicit surface schedule only."
        occupied_same_surface_cells = [
            cell for cell in sorted(occupied_map_cells) if f"surface={target_surface}" in cell
        ]
        prompt_context = build_controller_prompt_context(
            reasoning_memory_items=reasoning_memory_items,
            evaluator_diagnostic_cards=evaluator_diagnostic_report.get("diagnostic_cards", []),
            skill_items=skill_items,
            target_surface=target_surface,
            query_parts=[
                target_surface,
                diversity_target.cell_label if diversity_target else "",
                diversity_target.instruction if diversity_target else "",
            ],
            memory_card_limit=args.memory_card_limit,
            diagnostic_card_limit=args.diagnostic_card_limit,
            skill_card_limit=args.skill_card_limit,
        )
        retrieved_memory_item_ids = prompt_context.reasoning_memory_item_ids
        retrieved_memory_ids_seen.update(retrieved_memory_item_ids)
        diagnostic_card_ids = prompt_context.diagnostic_card_ids
        retrieved_skill_ids = prompt_context.skill_ids
        retrieved_skill_ids_seen.update(retrieved_skill_ids)
        messages = build_child_generation_prompt(
            parent_code=parent_text,
            evaluator_summary=evaluator_summary,
            attempt_index=attempt,
            parent_id=parent_id,
            prompt_card_id=prompt_card_id,
            target_surface=target_surface,
            previous_accepted_patches=accepted_patches_by_surface.get(target_surface, [])[-3:],
            diversity_target=diversity_target,
            occupied_map_cells=occupied_same_surface_cells,
            population_policy_text=population_policy_text,
            reasoning_memory_text=prompt_context.reasoning_memory_text,
            diagnostic_text=prompt_context.diagnostic_text,
            skill_text=prompt_context.skill_text,
        )
        write_prompt_artifact(attempt_dir, messages)

        response_record: dict[str, Any]
        if args.mock_patch_mode == "none":
            response_record = chat_completion(
                role=args.model_role,
                system_prompt=messages["system"],
                user_prompt=messages["user"],
                temperature=temperature,
                max_tokens=args.max_tokens,
                verify=True,
            )
            generated_text = response_record["content"]
        else:
            generated_text = mock_patch(parent_text, args.mock_patch_mode, target_surface=target_surface)
            response_record = {
                "role": "mock",
                "served_model_name": "mock",
                "temperature": temperature,
                "content": generated_text,
            }

        (attempt_dir / "raw_output.txt").write_text(generated_text, encoding="utf-8")
        write_json(attempt_dir / "model_response.json", response_record)
        initial_response_record = dict(response_record)

        empty_retry_count = 0
        empty_retry_succeeded = False
        while (
            args.mock_patch_mode == "none"
            and not generated_text.strip()
            and empty_retry_count < max(0, args.empty_retry_attempts)
        ):
            empty_retry_count += 1
            retry_messages = {
                "system": messages["system"]
                + "\nYou must put the SEARCH/REPLACE patch in message.content. Do not use reasoning output.",
                "user": messages["user"]
                + "\n\nPrevious response had empty final content. Retry once with only the final SEARCH/REPLACE patch in message.content.",
            }
            write_messages(attempt_dir / f"empty_retry_{empty_retry_count}_prompt", "Empty Output Retry Prompt", retry_messages)
            retry_record = chat_completion(
                role=args.model_role,
                system_prompt=retry_messages["system"],
                user_prompt=retry_messages["user"],
                temperature=0.0,
                max_tokens=args.max_tokens,
                verify=True,
            )
            retry_text = retry_record["content"]
            write_json(attempt_dir / f"empty_retry_{empty_retry_count}_response.json", retry_record)
            (attempt_dir / f"empty_retry_{empty_retry_count}_output.txt").write_text(retry_text, encoding="utf-8")
            if retry_text.strip():
                generated_text = retry_text
                response_record = retry_record
                empty_retry_succeeded = True
                (attempt_dir / "raw_output.txt").write_text(generated_text, encoding="utf-8")
                write_json(attempt_dir / "model_response.json", response_record)
                break

        filter_record = filter_patch_with_optional_repair(
            config=patch_filter_config,
            attempt_dir=attempt_dir,
            generated_text=generated_text,
            raw_output_path=attempt_dir / "raw_output.txt",
            target_surface=target_surface,
            attempt=attempt,
        )
        result = filter_record["result"]
        initial_result_record = filter_record["initial_result_record"]
        repair_attempted = bool(filter_record["repair_attempted"])
        repair_succeeded = bool(filter_record["repair_succeeded"])
        repair_response_path = filter_record["repair_response_path"]
        final_diff_text = str(filter_record["final_diff_text"])
        final_diff_path = Path(filter_record["final_diff_path"])

        child_hash = None
        duplicate_of_program_id = None
        duplicate_patch_fingerprint_of_program_id = None
        duplicate_retry_attempted = False
        duplicate_retry_succeeded = False
        duplicate_retry_count = 0
        duplicate_retry_reason = None
        near_duplicate_of_program_id = None
        near_duplicate_similarity = 0.0
        novelty_decision_record: dict[str, Any] = {
            "decision": "not_checked",
            "reason": None,
            "similarity": 0.0,
            "matched_program_id": None,
            "matched_patch_intent": None,
            "signature_token_count": 0,
        }
        diversity_descriptor: dict[str, Any] = {}
        patch_fingerprint = None
        map_cell_key_value = None
        map_cell_already_occupied = False
        map_cell_elite_program_id = None

        identity = describe_pass_candidate(
            result=result,
            final_diff_text=final_diff_text,
            target_surface=target_surface,
        )
        child_hash = identity["child_hash"]
        diversity_descriptor = identity["diversity_descriptor"]
        patch_fingerprint = identity["patch_fingerprint"]
        map_cell_key_value = identity["map_cell_key"]

        if result.decision == "pass":
            result.hard_gates["unique_child"] = True
            if child_hash in seen_child_hashes:
                duplicate_of_program_id = seen_child_hashes[child_hash]
                duplicate_retry_reason = f"duplicate child program hash already seen for {duplicate_of_program_id}"
            elif patch_fingerprint in seen_patch_fingerprints:
                duplicate_patch_fingerprint_of_program_id = seen_patch_fingerprints[str(patch_fingerprint)]
                duplicate_retry_reason = (
                    "duplicate normalized patch fingerprint already seen for "
                    f"{duplicate_patch_fingerprint_of_program_id}"
                )
            elif near_duplicate_check_enabled:
                novelty_decision = check_patch_novelty(
                    population_policy_state,
                    surface=target_surface,
                    diff_text=final_diff_text,
                    threshold=args.near_duplicate_threshold,
                )
                novelty_decision_record = novelty_decision.to_record()
                if novelty_decision.is_near_duplicate:
                    near_duplicate_of_program_id = novelty_decision.matched_program_id
                    near_duplicate_similarity = novelty_decision.similarity
                    duplicate_retry_reason = novelty_decision.reason

            if duplicate_retry_reason and args.duplicate_retry_attempts > 0:
                duplicate_retry_attempted = True
                forbidden_patches = [final_diff_text] + accepted_patches_by_surface.get(target_surface, [])[-2:]
                for retry_index in range(1, max(0, args.duplicate_retry_attempts) + 1):
                    duplicate_retry_count += 1
                    if population_policy_enabled:
                        retry_target = choose_population_diversity_target(
                            population_policy_state,
                            target_surface,
                            attempt + args.attempts + retry_index,
                            occupied_labels=occupied_target_labels_by_surface.get(target_surface, set()),
                        )
                    else:
                        retry_target = choose_diversity_target(
                            target_surface,
                            attempt + args.attempts + retry_index,
                            occupied_labels=occupied_target_labels_by_surface.get(target_surface, set()),
                        )
                    retry_target_intent = retry_target.intent if retry_target else "other"
                    retry_prompt_card_id = prompt_card_id_for(target_surface, retry_target_intent)
                    if population_policy_enabled:
                        retry_population_policy_text = format_population_policy_context(
                            population_policy_state,
                            parent_id=parent_id,
                            surface=target_surface,
                            target=retry_target,
                            prompt_card_id=retry_prompt_card_id,
                            near_duplicate_threshold=args.near_duplicate_threshold,
                        )
                    else:
                        retry_population_policy_text = (
                            "Population policy v2 is disabled; using explicit surface schedule only."
                        )
                    retry_prompt_context = build_controller_prompt_context(
                        reasoning_memory_items=reasoning_memory_items,
                        evaluator_diagnostic_cards=evaluator_diagnostic_report.get("diagnostic_cards", []),
                        skill_items=skill_items,
                        target_surface=target_surface,
                        query_parts=[
                            target_surface,
                            "duplicate retry",
                            duplicate_retry_reason or "",
                            retry_target.cell_label if retry_target else "",
                            retry_target.instruction if retry_target else "",
                        ],
                        memory_card_limit=args.memory_card_limit,
                        diagnostic_card_limit=args.diagnostic_card_limit,
                        skill_card_limit=args.skill_card_limit,
                        include_diagnostic_card_ids_in_skill_query=False,
                    )
                    retry_memory_ids = retry_prompt_context.reasoning_memory_item_ids
                    retrieved_memory_ids_seen.update(retry_memory_ids)
                    retry_skill_ids = retry_prompt_context.skill_ids
                    retrieved_skill_ids_seen.update(retry_skill_ids)
                    retry_messages = build_child_generation_prompt(
                        parent_code=parent_text,
                        evaluator_summary=evaluator_summary,
                        attempt_index=attempt,
                        parent_id=parent_id,
                        prompt_card_id=retry_prompt_card_id,
                        target_surface=target_surface,
                        previous_accepted_patches=accepted_patches_by_surface.get(target_surface, [])[-3:],
                        diversity_target=retry_target,
                        occupied_map_cells=occupied_same_surface_cells,
                        forbidden_patches=forbidden_patches,
                        duplicate_retry_reason=duplicate_retry_reason,
                        population_policy_text=retry_population_policy_text,
                        reasoning_memory_text=retry_prompt_context.reasoning_memory_text,
                        diagnostic_text=retry_prompt_context.diagnostic_text,
                        skill_text=retry_prompt_context.skill_text,
                    )
                    write_messages(
                        attempt_dir / f"duplicate_retry_{retry_index}_prompt",
                        "Duplicate Retry Prompt",
                        retry_messages,
                    )
                    if args.mock_patch_mode == "none":
                        retry_response_record = chat_completion(
                            role=args.model_role,
                            system_prompt=retry_messages["system"],
                            user_prompt=retry_messages["user"],
                            temperature=max(0.5, temperature),
                            max_tokens=args.max_tokens,
                            verify=True,
                        )
                        retry_text = retry_response_record["content"]
                    else:
                        retry_text = mock_patch(parent_text, args.mock_patch_mode, target_surface=target_surface)
                        retry_response_record = {
                            "role": "mock_duplicate_retry",
                            "served_model_name": "mock",
                            "temperature": max(0.5, temperature),
                            "content": retry_text,
                        }
                    retry_output_path = attempt_dir / f"duplicate_retry_{retry_index}_output.txt"
                    retry_output_path.write_text(retry_text, encoding="utf-8")
                    write_json(attempt_dir / f"duplicate_retry_{retry_index}_response.json", retry_response_record)
                    retry_filter_record = filter_patch_with_optional_repair(
                        config=patch_filter_config,
                        attempt_dir=attempt_dir,
                        generated_text=retry_text,
                        raw_output_path=retry_output_path,
                        target_surface=target_surface,
                        attempt=attempt,
                        artifact_prefix=f"duplicate_retry_{retry_index}_",
                    )
                    retry_result = retry_filter_record["result"]
                    retry_identity = describe_pass_candidate(
                        result=retry_result,
                        final_diff_text=str(retry_filter_record["final_diff_text"]),
                        target_surface=target_surface,
                    )
                    retry_child_hash = retry_identity["child_hash"]
                    retry_patch_fingerprint = retry_identity["patch_fingerprint"]
                    retry_duplicate_reason = None
                    retry_near_duplicate_of_program_id = None
                    retry_near_duplicate_similarity = 0.0
                    retry_novelty_decision_record = {
                        "decision": "not_checked",
                        "reason": None,
                        "similarity": 0.0,
                        "matched_program_id": None,
                        "matched_patch_intent": None,
                        "signature_token_count": 0,
                    }
                    if retry_result.decision == "pass" and retry_child_hash in seen_child_hashes:
                        retry_duplicate_reason = (
                            "duplicate child program hash already seen for "
                            f"{seen_child_hashes[retry_child_hash]}"
                        )
                    elif retry_result.decision == "pass" and retry_patch_fingerprint in seen_patch_fingerprints:
                        retry_duplicate_reason = (
                            "duplicate normalized patch fingerprint already seen for "
                            f"{seen_patch_fingerprints[str(retry_patch_fingerprint)]}"
                        )
                    elif retry_result.decision == "pass" and near_duplicate_check_enabled:
                        retry_novelty_decision = check_patch_novelty(
                            population_policy_state,
                            surface=target_surface,
                            diff_text=str(retry_filter_record["final_diff_text"]),
                            threshold=args.near_duplicate_threshold,
                        )
                        retry_novelty_decision_record = retry_novelty_decision.to_record()
                        if retry_novelty_decision.is_near_duplicate:
                            retry_near_duplicate_of_program_id = retry_novelty_decision.matched_program_id
                            retry_near_duplicate_similarity = retry_novelty_decision.similarity
                            retry_duplicate_reason = retry_novelty_decision.reason
                    write_json(
                        attempt_dir / f"duplicate_retry_{retry_index}_duplicate_check.json",
                        {
                            "decision": retry_result.decision,
                            "duplicate_reason": retry_duplicate_reason,
                            "child_sha256": retry_child_hash,
                            "patch_fingerprint": retry_patch_fingerprint,
                            "map_cell_key": retry_identity["map_cell_key"],
                            "near_duplicate_of_program_id": retry_near_duplicate_of_program_id,
                            "near_duplicate_similarity": retry_near_duplicate_similarity,
                            "novelty_decision": retry_novelty_decision_record,
                        },
                    )
                    if retry_result.decision == "pass" and retry_duplicate_reason is None:
                        result = retry_result
                        response_record = retry_response_record
                        final_diff_text = str(retry_filter_record["final_diff_text"])
                        final_diff_path = Path(retry_filter_record["final_diff_path"])
                        repair_attempted = repair_attempted or bool(retry_filter_record["repair_attempted"])
                        repair_succeeded = repair_succeeded or bool(retry_filter_record["repair_succeeded"])
                        repair_response_path = retry_filter_record["repair_response_path"] or repair_response_path
                        child_hash = retry_child_hash
                        diversity_descriptor = retry_identity["diversity_descriptor"]
                        patch_fingerprint = retry_patch_fingerprint
                        map_cell_key_value = retry_identity["map_cell_key"]
                        diversity_target = retry_target
                        target_intent = retry_target_intent
                        prompt_card_id = retry_prompt_card_id
                        if population_policy_enabled:
                            population_policy_snapshot = population_policy_state.target_snapshot(
                                parent_id=parent_id,
                                surface=target_surface,
                                target=diversity_target,
                                prompt_card_id=prompt_card_id,
                            )
                        else:
                            population_policy_snapshot = {
                                "population_policy_version": "v1",
                                "parent_id": parent_id,
                                "parent_offspring_count": 0,
                                "target_surface": target_surface,
                                "target_intent": target_intent,
                                "target_cell_label": diversity_target.cell_label if diversity_target else None,
                                "prompt_card_id": prompt_card_id,
                            }
                        duplicate_of_program_id = None
                        duplicate_patch_fingerprint_of_program_id = None
                        near_duplicate_of_program_id = None
                        near_duplicate_similarity = 0.0
                        novelty_decision_record = retry_novelty_decision_record
                        duplicate_retry_succeeded = True
                        duplicate_retry_reason = None
                        break

            if duplicate_retry_reason:
                if duplicate_of_program_id:
                    result.failure_category = "duplicate_child"
                elif duplicate_patch_fingerprint_of_program_id:
                    result.failure_category = "duplicate_patch_fingerprint"
                else:
                    result.failure_category = NEAR_DUPLICATE_FAILURE_CATEGORY
                result.decision = "reject"
                result.failure_reason = duplicate_retry_reason
                result.hard_gates["unique_child"] = False
                result.hard_gates["novel_patch"] = False
            elif child_hash is not None:
                result.hard_gates["unique_child"] = True
                result.hard_gates["novel_patch"] = True
                program_id_for_seen = f"{args.program_id_prefix}-{attempt:04d}"
                seen_child_hashes[child_hash] = program_id_for_seen
                if patch_fingerprint is not None:
                    seen_patch_fingerprints[str(patch_fingerprint)] = program_id_for_seen
                if map_cell_key_value:
                    map_cell_already_occupied = map_cell_key_value in occupied_map_cells
                    map_cell_elite_program_id = occupied_map_cells.get(map_cell_key_value)
                    occupied_map_cells.setdefault(map_cell_key_value, program_id_for_seen)
                actual_target_label = f"{target_surface}:{diversity_descriptor.get('patch_intent', 'unknown')}"
                occupied_labels = occupied_target_labels_by_surface.setdefault(target_surface, set())
                occupied_labels.add(diversity_target.cell_label)
                occupied_labels.add(actual_target_label)
                accepted_patches_by_surface.setdefault(target_surface, []).append(final_diff_text)
        else:
            result.hard_gates["unique_child"] = False
            result.hard_gates["novel_patch"] = False

        result_record = result.to_record()
        lazy_penalty_score = lazy_penalty_for_attempt(result_record)
        controller_search_score = controller_search_score_for_attempt(result_record)
        program_id = f"{args.program_id_prefix}-{attempt:04d}"
        child_path = None
        if result.decision == "pass" and result.child_text is not None:
            child_path = attempt_dir / "child_program.py"
            child_path.write_text(result.child_text, encoding="utf-8")

        db_inserted = False
        if args.db_path:
            try:
                insert_program_record(
                    args.db_path,
                    {
                        "program_id": program_id,
                        "parent_id": "PROG-20260430-000000",
                        "root_id": "CAND-20260423-001",
                        "branch_id": "BRANCH-CAND-20260423-001-001",
                        "generation": 1,
                        "island": "daily_stock_signal",
                        "mutation_surface": "controller_static_child_dry_run",
                        "data_scope": "daily_stock_only",
                        "status": "controller_static_pass" if result.decision == "pass" else "controller_static_reject",
                        "program_path": str(child_path) if child_path else str(program_path),
                        "diff_path": str(final_diff_path),
                        "prompt_path": str(attempt_dir / "prompt.json"),
                        "evaluator_summary_path": None,
                        "metrics": result.vector_smoke_metrics,
                        "descriptors": {
                            "population_policy_version": (
                                POPULATION_POLICY_VERSION if population_policy_enabled else "v1"
                            ),
                            "prompt_fitness_policy_version": PROMPT_FITNESS_POLICY_VERSION,
                            "lazy_penalty_score": lazy_penalty_score,
                            "controller_search_score": controller_search_score,
                            "model_role": args.model_role,
                            "temperature": temperature,
                            "parent_id": parent_id,
                            "target_surface": target_surface,
                            "target_intent": target_intent,
                            "target_cell_label": diversity_target.cell_label if diversity_target else None,
                            "prompt_card_id": prompt_card_id,
                            **population_policy_snapshot,
                            "child_sha256": child_hash,
                            "duplicate_of_program_id": duplicate_of_program_id,
                            "duplicate_patch_fingerprint_of_program_id": duplicate_patch_fingerprint_of_program_id,
                            "near_duplicate_of_program_id": near_duplicate_of_program_id,
                            "near_duplicate_similarity": near_duplicate_similarity,
                            "novelty_decision": novelty_decision_record,
                            "duplicate_retry_attempted": duplicate_retry_attempted,
                            "duplicate_retry_succeeded": duplicate_retry_succeeded,
                            "duplicate_retry_count": duplicate_retry_count,
                            "map_cell_key": map_cell_key_value,
                            "map_cell_already_occupied": map_cell_already_occupied,
                            "map_cell_elite_program_id": map_cell_elite_program_id,
                            **diversity_descriptor,
                            "repair_attempted": repair_attempted,
                            "repair_succeeded": repair_succeeded,
                            "empty_retry_count": empty_retry_count,
                            "empty_retry_succeeded": empty_retry_succeeded,
                            "diagnostic_card_ids": diagnostic_card_ids,
                            "reasoning_memory_item_ids": retrieved_memory_item_ids,
                            "skill_ids": retrieved_skill_ids,
                            "initial_failure_category": initial_result_record.get("failure_category"),
                            "dry_run_only": True,
                        },
                        "hard_gates": result.hard_gates,
                        "validation_exposure": {
                            "controller_static": True,
                            "remote_sample_eval": False,
                            "remote_full_validation": False,
                            "test_set_used": False,
                        },
                        "failure_reason": result.failure_reason,
                    },
                )
                db_inserted = True
            except Exception as exc:
                result_record["db_insert_error"] = str(exc)

        result_record.update(
            {
                "attempt": attempt,
                "program_id": program_id,
                "parent_id": parent_id,
                "population_policy_version": POPULATION_POLICY_VERSION if population_policy_enabled else "v1",
                "prompt_fitness_policy_version": PROMPT_FITNESS_POLICY_VERSION,
                "lazy_penalty_score": lazy_penalty_score,
                "controller_search_score": controller_search_score,
                "target_surface": target_surface,
                "target_intent": target_intent,
                "target_cell_label": diversity_target.cell_label if diversity_target else None,
                "prompt_card_id": prompt_card_id,
                **population_policy_snapshot,
                "temperature": temperature,
                "db_inserted": db_inserted,
                "child_program_path": str(child_path) if child_path else None,
                "child_sha256": child_hash,
                "duplicate_of_program_id": duplicate_of_program_id,
                "duplicate_patch_fingerprint_of_program_id": duplicate_patch_fingerprint_of_program_id,
                "near_duplicate_of_program_id": near_duplicate_of_program_id,
                "near_duplicate_similarity": near_duplicate_similarity,
                "novelty_decision": novelty_decision_record,
                "duplicate_retry_attempted": duplicate_retry_attempted,
                "duplicate_retry_succeeded": duplicate_retry_succeeded,
                "duplicate_retry_count": duplicate_retry_count,
                "map_cell_key": map_cell_key_value,
                "map_cell_already_occupied": map_cell_already_occupied,
                "map_cell_elite_program_id": map_cell_elite_program_id,
                **diversity_descriptor,
                "initial_response_content_was_null": bool(initial_response_record.get("content_was_null", False)),
                "initial_response_content_length": len(str(initial_response_record.get("content", "") or "")),
                "initial_response_reasoning_length": int(initial_response_record.get("reasoning_length", 0) or 0),
                "final_response_content_was_null": bool(response_record.get("content_was_null", False)),
                "final_response_content_length": len(str(response_record.get("content", "") or "")),
                "final_response_reasoning_length": int(response_record.get("reasoning_length", 0) or 0),
                "initial_decision": initial_result_record.get("decision"),
                "initial_failure_category": initial_result_record.get("failure_category"),
                "initial_failure_reason": initial_result_record.get("failure_reason"),
                "initial_hard_gates": initial_result_record.get("hard_gates", {}),
                "repair_attempted": repair_attempted,
                "repair_succeeded": repair_succeeded,
                "empty_retry_count": empty_retry_count,
                "empty_retry_succeeded": empty_retry_succeeded,
                "repair_response_path": str(repair_response_path) if repair_response_path else None,
                "final_diff_path": str(final_diff_path),
                "diagnostic_card_ids": diagnostic_card_ids,
                "reasoning_memory_item_ids": retrieved_memory_item_ids,
                "reasoning_memory_path": str(memory_path) if memory_path else None,
                "skill_ids": retrieved_skill_ids,
                "skill_library_path": str(skill_library_path) if skill_library_path else None,
            }
        )
        write_json(attempt_dir / "micro_filter_result.json", result_record)
        if population_policy_enabled:
            population_policy_state.record_attempt(result_record, final_diff_text=final_diff_text)
        attempt_records.append(result_record)

    summary = summarize_attempts(attempt_records)
    population_policy_summary = population_policy_state.to_summary()
    population_policy_state_path = write_json(
        out_dir / "population_policy_state.json",
        population_policy_summary,
    )
    summary.update(
        {
            "program_path": str(program_path),
            "evaluator_summary": args.evaluator_summary,
            "model_role": args.model_role,
            "population_policy_version": POPULATION_POLICY_VERSION if population_policy_enabled else "v1",
            "prompt_fitness_policy_version": PROMPT_FITNESS_POLICY_VERSION,
            "population_policy_enabled": population_policy_enabled,
            "population_policy_state_json": str(population_policy_state_path),
            "near_duplicate_check_enabled": near_duplicate_check_enabled,
            "near_duplicate_threshold": args.near_duplicate_threshold,
            "parent_offspring_counts": population_policy_summary["parent_offspring_counts"],
            "surface_attempt_counts": population_policy_summary["surface_attempt_counts"],
            "surface_duplicate_counts": population_policy_summary["surface_duplicate_counts"],
            "intent_attempt_counts": population_policy_summary["intent_attempt_counts"],
            "intent_duplicate_counts": population_policy_summary["intent_duplicate_counts"],
            "prompt_card_attempt_counts": population_policy_summary["prompt_card_attempt_counts"],
            "prompt_card_duplicate_counts": population_policy_summary["prompt_card_duplicate_counts"],
            "prompt_card_score_sums": population_policy_summary["prompt_card_score_sums"],
            "prompt_card_lazy_penalty_sums": population_policy_summary["prompt_card_lazy_penalty_sums"],
            "prompt_card_best_scores": population_policy_summary["prompt_card_best_scores"],
            "prompt_card_fitness": population_policy_summary["prompt_card_fitness"],
            "duplicate_heavy_intents": population_policy_summary["duplicate_heavy_intents"],
            "surface_schedule": list(surface_schedule),
            "prior_summary_paths": [str(path) for path in args.prior_summary],
            "prior_attempt_count": search_state.prior_attempt_count,
            "prior_pass_count": search_state.prior_pass_count,
            "prior_seen_child_hash_count": prior_seen_child_hash_count,
            "mock_patch_mode": args.mock_patch_mode,
            "remote_sample_eval_launched": False,
            "full_validation_launched": False,
            "reasoning_memory_enabled": memory_path is not None,
            "reasoning_memory_path": str(memory_path) if memory_path else None,
            "reasoning_memory_item_count": len(reasoning_memory_items),
            "retrieved_reasoning_memory_ids": sorted(retrieved_memory_ids_seen),
            "skill_library_enabled": skill_library_path is not None,
            "skill_library_path": str(skill_library_path) if skill_library_path else None,
            "skill_library_item_count": len(skill_items),
            "retrieved_skill_ids": sorted(retrieved_skill_ids_seen),
            "evaluator_diagnostic_report_json": evaluator_diagnostic_paths["json"],
            "evaluator_diagnostic_report_markdown": evaluator_diagnostic_paths["markdown"],
            "evaluator_diagnostic_card_ids": [
                card.get("diagnostic_id")
                for card in evaluator_diagnostic_report.get("diagnostic_cards", [])
            ],
        }
    )
    if memory_path is not None:
        memory_update = build_controller_batch_memory_update(
            source_run_id=out_dir.name,
            summary=summary,
            attempts=attempt_records,
            memory_path=memory_path,
            retrieved_memory_ids=sorted(retrieved_memory_ids_seen),
        )
        memory_update_paths = write_memory_update(out_dir, memory_update)
        memory_update_log = append_memory_update(memory_path.parent / "memory_updates.jsonl", memory_update)
        summary["reasoning_memory_update_json"] = memory_update_paths["json"]
        summary["reasoning_memory_update_markdown"] = memory_update_paths["markdown"]
        summary["reasoning_memory_update_log"] = memory_update_log
    controller_diagnostic_report = build_controller_diagnostic_report(
        summary=summary,
        attempts=attempt_records,
        source_path=out_dir / "summary.json",
    )
    controller_diagnostic_paths = write_diagnostic_report(
        out_dir,
        "controller_diagnostic_report",
        controller_diagnostic_report,
    )
    summary["controller_diagnostic_report_json"] = controller_diagnostic_paths["json"]
    summary["controller_diagnostic_report_markdown"] = controller_diagnostic_paths["markdown"]
    summary["controller_diagnostic_card_ids"] = [
        card.get("diagnostic_id") for card in controller_diagnostic_report.get("diagnostic_cards", [])
    ]
    if skill_library_path is not None:
        skill_update = build_controller_batch_skill_update(
            source_run_id=out_dir.name,
            summary=summary,
            attempts=attempt_records,
            skill_library_path=skill_library_path,
            retrieved_skill_ids=sorted(retrieved_skill_ids_seen),
        )
        skill_update_paths = write_skill_update(out_dir, skill_update)
        skill_update_log = append_skill_update(skill_library_path.parent / "skill_updates.jsonl", skill_update)
        summary["skill_update_json"] = skill_update_paths["json"]
        summary["skill_update_markdown"] = skill_update_paths["markdown"]
        summary["skill_update_log"] = skill_update_log
    write_json(out_dir / "summary.json", {"summary": summary, "attempts": attempt_records})
    write_summary_markdown(out_dir / "summary.md", summary)
    print(json.dumps({"status": "ok", "out_dir": str(out_dir), "summary": summary}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
