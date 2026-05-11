"""Population policy for controller-static child generation.

This module owns search-control decisions that depend on prior controller
population state: saturated intents, parent reuse, prompt-card productivity,
and deterministic near-duplicate checks. The runner should orchestrate calls
to this module, but it should not own these policy rules.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
import re
from typing import Any, Iterable

from .diff_blocks import DiffBlockError, parse_search_replace_blocks
from .diversity import DIVERSITY_TARGETS, DiversityTarget, choose_diversity_target


POPULATION_POLICY_VERSION = "controller_population_policy_v2"
PROMPT_FITNESS_POLICY_VERSION = "prompt_fitness_and_lazy_score_v1"
DEFAULT_PARENT_PROGRAM_ID = "PROG-20260430-000000"
NEAR_DUPLICATE_FAILURE_CATEGORY = "near_duplicate_patch"
BEHAVIORAL_NOOP_FAILURE_CATEGORY = "behavioral_noop"
PASS_CONTROLLER_SEARCH_SCORE = 1.0
TARGET_INTENT_MISMATCH_CONTROLLER_SCORE = 0.35
TARGET_INTENT_MISMATCH_LAZY_PENALTY = -0.15
DEFAULT_REJECT_LAZY_PENALTY = -0.20
PROMPT_CARD_REROUTE_MIN_ATTEMPTS = 2
PROMPT_CARD_REROUTE_DUPLICATE_RATE = 0.50
PROMPT_CARD_REROUTE_LOW_FITNESS = -0.15
PROMPT_CARD_REROUTE_LOW_PASS_RATE = 0.25
LAZY_PENALTY_BY_FAILURE_CATEGORY = {
    "empty_output": -0.40,
    "malformed_search_replace": -0.40,
    "no_valid_patch": -0.30,
    BEHAVIORAL_NOOP_FAILURE_CATEGORY: -0.30,
    "duplicate_child": -0.30,
    "duplicate_patch_fingerprint": -0.30,
    NEAR_DUPLICATE_FAILURE_CATEGORY: -0.30,
    "exact_search_not_found": -0.25,
    "outside_evolve_block": -0.25,
    "evolve_marker_error": -0.25,
    "apply_failed": -0.25,
    "compile_failed": -0.20,
    "vector_smoke_failed": -0.20,
    "behavior_delta_failed": -0.20,
    "portfolio_semantic_failed": -0.10,
    "forbidden_policy_edit": -0.50,
    "introduced_new_import": -0.50,
}


@dataclass(frozen=True)
class PatchSignatureRecord:
    """Compact deterministic signature for one accepted patch."""

    program_id: str
    surface: str
    patch_intent: str
    signature_text: str
    shingles: frozenset[str]


@dataclass(frozen=True)
class NoveltyDecision:
    """Deterministic patch-novelty decision before expensive evaluation."""

    decision: str
    reason: str | None
    similarity: float
    matched_program_id: str | None
    matched_patch_intent: str | None
    signature_token_count: int

    @property
    def is_near_duplicate(self) -> bool:
        return self.decision == NEAR_DUPLICATE_FAILURE_CATEGORY

    def to_record(self) -> dict[str, Any]:
        return {
            "decision": self.decision,
            "reason": self.reason,
            "similarity": self.similarity,
            "matched_program_id": self.matched_program_id,
            "matched_patch_intent": self.matched_patch_intent,
            "signature_token_count": self.signature_token_count,
        }


@dataclass
class PopulationPolicyState:
    """Mutable controller population state for one batch."""

    version: str = POPULATION_POLICY_VERSION
    default_parent_id: str = DEFAULT_PARENT_PROGRAM_ID
    parent_offspring_counts: Counter[str] = field(default_factory=Counter)
    surface_attempt_counts: Counter[str] = field(default_factory=Counter)
    surface_pass_counts: Counter[str] = field(default_factory=Counter)
    surface_duplicate_counts: Counter[str] = field(default_factory=Counter)
    intent_attempt_counts: Counter[str] = field(default_factory=Counter)
    intent_pass_counts: Counter[str] = field(default_factory=Counter)
    intent_duplicate_counts: Counter[str] = field(default_factory=Counter)
    prompt_card_attempt_counts: Counter[str] = field(default_factory=Counter)
    prompt_card_pass_counts: Counter[str] = field(default_factory=Counter)
    prompt_card_duplicate_counts: Counter[str] = field(default_factory=Counter)
    prompt_card_score_sums: Counter[str] = field(default_factory=Counter)
    prompt_card_lazy_penalty_sums: Counter[str] = field(default_factory=Counter)
    prompt_card_best_scores: dict[str, float] = field(default_factory=dict)
    patch_signatures_by_surface: dict[str, list[PatchSignatureRecord]] = field(default_factory=dict)

    def parent_offspring_count(self, parent_id: str | None = None) -> int:
        return int(self.parent_offspring_counts[parent_id or self.default_parent_id])

    def target_snapshot(
        self,
        *,
        parent_id: str,
        surface: str,
        target: DiversityTarget,
        prompt_card_id: str,
    ) -> dict[str, Any]:
        intent_key = target_intent_key(surface, target.intent)
        return {
            "population_policy_version": self.version,
            "parent_id": parent_id,
            "parent_offspring_count": self.parent_offspring_count(parent_id),
            "target_surface": surface,
            "target_intent": target.intent,
            "target_cell_label": target.cell_label,
            "surface_attempt_count": int(self.surface_attempt_counts[surface]),
            "surface_pass_count": int(self.surface_pass_counts[surface]),
            "surface_duplicate_count": int(self.surface_duplicate_counts[surface]),
            "target_intent_attempt_count": int(self.intent_attempt_counts[intent_key]),
            "target_intent_pass_count": int(self.intent_pass_counts[intent_key]),
            "target_intent_duplicate_count": int(self.intent_duplicate_counts[intent_key]),
            "prompt_card_id": prompt_card_id,
            "prompt_card_attempt_count": int(self.prompt_card_attempt_counts[prompt_card_id]),
            "prompt_card_pass_count": int(self.prompt_card_pass_counts[prompt_card_id]),
            "prompt_card_duplicate_count": int(self.prompt_card_duplicate_counts[prompt_card_id]),
            **self.prompt_card_fitness(prompt_card_id),
            **self.prompt_card_reroute_policy(prompt_card_id),
        }

    def record_attempt(self, attempt_record: dict[str, Any], *, final_diff_text: str | None = None) -> None:
        """Update policy counters after an attempt has a final decision."""

        parent_id = str(attempt_record.get("parent_id") or self.default_parent_id)
        surface = str(attempt_record.get("target_surface") or "unknown")
        target_intent = str(attempt_record.get("target_intent") or "unknown")
        patch_intent = str(attempt_record.get("patch_intent") or target_intent)
        prompt_card_id = str(
            attempt_record.get("prompt_card_id") or prompt_card_id_for(surface, target_intent)
        )
        intent_key = target_intent_key(surface, patch_intent)
        failure_category = attempt_record.get("failure_category")
        lazy_penalty = lazy_penalty_for_attempt(attempt_record)
        search_score = controller_search_score_for_attempt(attempt_record)

        self.surface_attempt_counts[surface] += 1
        self.intent_attempt_counts[intent_key] += 1
        self.prompt_card_attempt_counts[prompt_card_id] += 1
        self.prompt_card_score_sums[prompt_card_id] += search_score
        self.prompt_card_lazy_penalty_sums[prompt_card_id] += lazy_penalty
        self.prompt_card_best_scores[prompt_card_id] = max(
            self.prompt_card_best_scores.get(prompt_card_id, float("-inf")),
            search_score,
        )

        if is_duplicate_failure(failure_category):
            self.surface_duplicate_counts[surface] += 1
            self.intent_duplicate_counts[intent_key] += 1
            self.prompt_card_duplicate_counts[prompt_card_id] += 1

        if attempt_record.get("decision") == "pass":
            target_intent_match = attempt_record.get("target_intent_match") is not False
            self.parent_offspring_counts[parent_id] += 1
            self.surface_pass_counts[surface] += 1
            self.intent_pass_counts[intent_key] += 1
            if target_intent_match:
                self.prompt_card_pass_counts[prompt_card_id] += 1
            if final_diff_text:
                self.add_patch_signature(
                    program_id=str(attempt_record.get("program_id") or "unknown_program"),
                    surface=surface,
                    patch_intent=patch_intent,
                    diff_text=final_diff_text,
                )

    def add_patch_signature(
        self,
        *,
        program_id: str,
        surface: str,
        patch_intent: str,
        diff_text: str,
    ) -> None:
        signature_text = edit_signature_text(diff_text)
        shingles = patch_signature_shingles(signature_text)
        if not shingles:
            return
        self.patch_signatures_by_surface.setdefault(surface, []).append(
            PatchSignatureRecord(
                program_id=program_id,
                surface=surface,
                patch_intent=patch_intent,
                signature_text=signature_text,
                shingles=frozenset(shingles),
            )
        )

    def prompt_card_fitness(self, prompt_card_id: str) -> dict[str, float | str]:
        """Return controller-local prompt-card fitness from observed attempts."""

        attempts = int(self.prompt_card_attempt_counts[prompt_card_id])
        passes = int(self.prompt_card_pass_counts[prompt_card_id])
        duplicates = int(self.prompt_card_duplicate_counts[prompt_card_id])
        score_sum = float(self.prompt_card_score_sums[prompt_card_id])
        lazy_sum = float(self.prompt_card_lazy_penalty_sums[prompt_card_id])
        mean_score = score_sum / attempts if attempts else 0.0
        duplicate_rate = duplicates / attempts if attempts else 0.0
        nonduplicate_pass_rate = passes / attempts if attempts else 0.0
        hard_gate_risk = 1.0 - nonduplicate_pass_rate if attempts else 0.0
        best_score = self.prompt_card_best_scores.get(prompt_card_id, 0.0)
        fitness_score = mean_score + 0.50 * nonduplicate_pass_rate - 0.50 * duplicate_rate
        return {
            "prompt_fitness_policy_version": PROMPT_FITNESS_POLICY_VERSION,
            "prompt_card_fitness_score": float(fitness_score),
            "prompt_card_mean_search_score": float(mean_score),
            "prompt_card_best_search_score": float(best_score),
            "prompt_card_lazy_penalty_sum": float(lazy_sum),
            "prompt_card_nonduplicate_pass_rate": float(nonduplicate_pass_rate),
            "prompt_card_duplicate_rate": float(duplicate_rate),
            "prompt_card_hard_gate_risk": float(hard_gate_risk),
        }

    def prompt_card_reroute_policy(self, prompt_card_id: str) -> dict[str, Any]:
        """Return prompt-card de-saturation pressure for target selection."""

        attempts = int(self.prompt_card_attempt_counts[prompt_card_id])
        fitness = self.prompt_card_fitness(prompt_card_id)
        duplicate_rate = float(fitness["prompt_card_duplicate_rate"])
        nonduplicate_pass_rate = float(fitness["prompt_card_nonduplicate_pass_rate"])
        fitness_score = float(fitness["prompt_card_fitness_score"])
        penalty = 0.0
        reasons: list[str] = []
        if attempts >= PROMPT_CARD_REROUTE_MIN_ATTEMPTS and duplicate_rate >= PROMPT_CARD_REROUTE_DUPLICATE_RATE:
            penalty += 8.0
            reasons.append("duplicate_rate")
        if attempts >= PROMPT_CARD_REROUTE_MIN_ATTEMPTS and fitness_score <= PROMPT_CARD_REROUTE_LOW_FITNESS:
            penalty += 6.0
            reasons.append("low_fitness")
        if (
            attempts >= 3
            and nonduplicate_pass_rate <= PROMPT_CARD_REROUTE_LOW_PASS_RATE
            and fitness_score <= 0.50
        ):
            penalty += 4.0
            reasons.append("low_pass_rate")
        if attempts >= 3 and nonduplicate_pass_rate <= 0.0:
            penalty += 6.0
            reasons.append("no_nonduplicate_passes")
        return {
            "prompt_card_reroute_penalty": float(penalty),
            "prompt_card_reroute_reasons": ",".join(reasons),
        }

    def to_summary(self) -> dict[str, Any]:
        prompt_card_fitness = {
            prompt_card_id: self.prompt_card_fitness(prompt_card_id)
            for prompt_card_id in sorted(self.prompt_card_attempt_counts)
        }
        prompt_card_reroute_policy = {
            prompt_card_id: self.prompt_card_reroute_policy(prompt_card_id)
            for prompt_card_id in sorted(self.prompt_card_attempt_counts)
        }
        return {
            "version": self.version,
            "prompt_fitness_policy_version": PROMPT_FITNESS_POLICY_VERSION,
            "default_parent_id": self.default_parent_id,
            "parent_offspring_counts": dict(sorted(self.parent_offspring_counts.items())),
            "surface_attempt_counts": dict(sorted(self.surface_attempt_counts.items())),
            "surface_pass_counts": dict(sorted(self.surface_pass_counts.items())),
            "surface_duplicate_counts": dict(sorted(self.surface_duplicate_counts.items())),
            "intent_attempt_counts": dict(sorted(self.intent_attempt_counts.items())),
            "intent_pass_counts": dict(sorted(self.intent_pass_counts.items())),
            "intent_duplicate_counts": dict(sorted(self.intent_duplicate_counts.items())),
            "prompt_card_attempt_counts": dict(sorted(self.prompt_card_attempt_counts.items())),
            "prompt_card_pass_counts": dict(sorted(self.prompt_card_pass_counts.items())),
            "prompt_card_duplicate_counts": dict(sorted(self.prompt_card_duplicate_counts.items())),
            "prompt_card_score_sums": dict(sorted(self.prompt_card_score_sums.items())),
            "prompt_card_lazy_penalty_sums": dict(sorted(self.prompt_card_lazy_penalty_sums.items())),
            "prompt_card_best_scores": dict(sorted(self.prompt_card_best_scores.items())),
            "prompt_card_fitness": prompt_card_fitness,
            "prompt_card_reroute_policy": prompt_card_reroute_policy,
            "patch_signature_count_by_surface": {
                surface: len(records)
                for surface, records in sorted(self.patch_signatures_by_surface.items())
            },
            "duplicate_heavy_intents": duplicate_heavy_intents(self, limit=8),
        }


def target_intent_key(surface: str, intent: str) -> str:
    return f"{surface}:{intent}"


def prompt_card_id_for(surface: str, target_intent: str, *, policy_version: str = POPULATION_POLICY_VERSION) -> str:
    return f"controller_static:{surface}:{target_intent}:{policy_version}"


def is_duplicate_failure(failure_category: Any) -> bool:
    return str(failure_category or "") in {
        "duplicate_child",
        "duplicate_patch_fingerprint",
        NEAR_DUPLICATE_FAILURE_CATEGORY,
    }


def lazy_penalty_for_attempt(attempt_record: dict[str, Any]) -> float:
    """Return deterministic negative evidence for lazy or invalid outputs."""

    if attempt_record.get("decision") == "pass":
        if attempt_record.get("target_intent_match") is False:
            return TARGET_INTENT_MISMATCH_LAZY_PENALTY
        return 0.0
    failure_category = str(attempt_record.get("failure_category") or "")
    return float(LAZY_PENALTY_BY_FAILURE_CATEGORY.get(failure_category, DEFAULT_REJECT_LAZY_PENALTY))


def controller_search_score_for_attempt(attempt_record: dict[str, Any]) -> float:
    """Return the controller-stage score used for prompt-card fitness."""

    if attempt_record.get("decision") == "pass":
        if attempt_record.get("target_intent_match") is False:
            return TARGET_INTENT_MISMATCH_CONTROLLER_SCORE
        return PASS_CONTROLLER_SEARCH_SCORE
    return lazy_penalty_for_attempt(attempt_record)


def seed_population_policy_state(
    prior_attempts: Iterable[dict[str, Any]],
    *,
    default_parent_id: str = DEFAULT_PARENT_PROGRAM_ID,
    historical_missing_parent_id: str = DEFAULT_PARENT_PROGRAM_ID,
) -> PopulationPolicyState:
    """Build controller population state from prior summary attempts."""

    state = PopulationPolicyState(default_parent_id=default_parent_id)
    for idx, attempt in enumerate(prior_attempts):
        surface = str(attempt.get("target_surface") or "unknown")
        target_intent = str(attempt.get("target_intent") or attempt.get("patch_intent") or "unknown")
        patch_intent = str(attempt.get("patch_intent") or target_intent)
        prompt_card_id = str(attempt.get("prompt_card_id") or prompt_card_id_for(surface, target_intent))
        record = {
            **attempt,
            "parent_id": str(attempt.get("parent_id") or historical_missing_parent_id),
            "target_surface": surface,
            "target_intent": target_intent,
            "patch_intent": patch_intent,
            "prompt_card_id": prompt_card_id,
            "program_id": str(attempt.get("program_id") or f"prior_attempt_{idx:04d}"),
        }
        patch_text = _read_text_if_present(attempt.get("final_diff_path"))
        state.record_attempt(record, final_diff_text=patch_text)
    return state


def choose_population_diversity_target(
    state: PopulationPolicyState,
    surface: str,
    attempt_index: int,
    *,
    occupied_labels: set[str] | None = None,
) -> DiversityTarget:
    """Choose an underused, low-duplicate target intent for a surface."""

    targets = DIVERSITY_TARGETS.get(surface)
    if not targets:
        return choose_diversity_target(surface, attempt_index, occupied_labels=occupied_labels)

    occupied = occupied_labels or set()
    start = attempt_index % len(targets)
    scored: list[tuple[float, int, DiversityTarget]] = []
    for idx, target in enumerate(targets):
        intent_key = target_intent_key(surface, target.intent)
        pass_count = state.intent_pass_counts[intent_key]
        duplicate_count = state.intent_duplicate_counts[intent_key]
        attempt_count = state.intent_attempt_counts[intent_key]
        occupied_penalty = 3.0 if target.cell_label in occupied or pass_count else 0.0
        duplicate_penalty = 6.0 * duplicate_count
        attempt_penalty = 0.5 * attempt_count
        direction_flip_penalty = 4.0 if target.intent == "direction_flip" and duplicate_count else 0.0
        prompt_card_id = prompt_card_id_for(surface, target.intent)
        prompt_fitness = state.prompt_card_fitness(prompt_card_id)
        prompt_fitness_score = float(prompt_fitness["prompt_card_fitness_score"])
        prompt_duplicate_rate = float(prompt_fitness["prompt_card_duplicate_rate"])
        prompt_pass_rate = float(prompt_fitness["prompt_card_nonduplicate_pass_rate"])
        reroute_policy = state.prompt_card_reroute_policy(prompt_card_id)
        reroute_penalty = float(reroute_policy["prompt_card_reroute_penalty"])
        prompt_penalty = max(0.0, -prompt_fitness_score) * 2.0 + prompt_duplicate_rate * 2.0
        prompt_bonus = min(1.0, prompt_pass_rate)
        score = (
            occupied_penalty
            + duplicate_penalty
            + attempt_penalty
            + direction_flip_penalty
            + prompt_penalty
            + reroute_penalty
            - prompt_bonus
        )
        rotation_distance = (idx - start) % len(targets)
        scored.append((score, rotation_distance, target))
    scored.sort(key=lambda item: (item[0], item[1], item[2].cell_label))
    return scored[0][2]


def check_patch_novelty(
    state: PopulationPolicyState,
    *,
    surface: str,
    diff_text: str,
    threshold: float,
) -> NoveltyDecision:
    """Reject near-duplicate edit signatures within the same surface."""

    signature_text = edit_signature_text(diff_text)
    shingles = patch_signature_shingles(signature_text)
    if not shingles:
        return NoveltyDecision(
            decision="novel",
            reason="empty_signature_not_comparable",
            similarity=0.0,
            matched_program_id=None,
            matched_patch_intent=None,
            signature_token_count=0,
        )

    best_similarity = 0.0
    best_record: PatchSignatureRecord | None = None
    for record in state.patch_signatures_by_surface.get(surface, []):
        similarity = jaccard(shingles, set(record.shingles))
        if similarity > best_similarity:
            best_similarity = similarity
            best_record = record

    if best_record is not None and best_similarity >= threshold:
        return NoveltyDecision(
            decision=NEAR_DUPLICATE_FAILURE_CATEGORY,
            reason=(
                f"edit signature similarity {best_similarity:.3f} >= {threshold:.3f} "
                f"against {best_record.program_id}"
            ),
            similarity=best_similarity,
            matched_program_id=best_record.program_id,
            matched_patch_intent=best_record.patch_intent,
            signature_token_count=len(tokenize_signature(signature_text)),
        )
    return NoveltyDecision(
        decision="novel",
        reason=None,
        similarity=best_similarity,
        matched_program_id=best_record.program_id if best_record else None,
        matched_patch_intent=best_record.patch_intent if best_record else None,
        signature_token_count=len(tokenize_signature(signature_text)),
    )


def format_population_policy_context(
    state: PopulationPolicyState,
    *,
    parent_id: str,
    surface: str,
    target: DiversityTarget,
    prompt_card_id: str,
    near_duplicate_threshold: float,
) -> str:
    """Render compact prompt-facing population policy context."""

    snapshot = state.target_snapshot(
        parent_id=parent_id,
        surface=surface,
        target=target,
        prompt_card_id=prompt_card_id,
    )
    duplicate_intents = duplicate_heavy_intents(state, limit=5)
    duplicate_lines = ["None."]
    if duplicate_intents:
        duplicate_lines = [
            (
                f"- {item['intent_key']}: duplicates={item['duplicate_count']}, "
                f"passes={item['pass_count']}, attempts={item['attempt_count']}"
            )
            for item in duplicate_intents
        ]
    return "\n".join(
        [
            f"population_policy_version: {state.version}",
            f"parent_id: {parent_id}",
            f"parent_offspring_count: {snapshot['parent_offspring_count']}",
            f"target_surface: {surface}",
            f"target_intent: {target.intent}",
            f"target_cell_label: {target.cell_label}",
            f"target_intent_attempt_count: {snapshot['target_intent_attempt_count']}",
            f"target_intent_pass_count: {snapshot['target_intent_pass_count']}",
            f"target_intent_duplicate_count: {snapshot['target_intent_duplicate_count']}",
            f"prompt_card_id: {prompt_card_id}",
            f"prompt_card_attempt_count: {snapshot['prompt_card_attempt_count']}",
            f"prompt_card_pass_count: {snapshot['prompt_card_pass_count']}",
            f"prompt_card_duplicate_count: {snapshot['prompt_card_duplicate_count']}",
            f"prompt_fitness_policy_version: {snapshot['prompt_fitness_policy_version']}",
            f"prompt_card_fitness_score: {snapshot['prompt_card_fitness_score']:.3f}",
            f"prompt_card_mean_search_score: {snapshot['prompt_card_mean_search_score']:.3f}",
            f"prompt_card_best_search_score: {snapshot['prompt_card_best_search_score']:.3f}",
            f"prompt_card_lazy_penalty_sum: {snapshot['prompt_card_lazy_penalty_sum']:.3f}",
            f"prompt_card_nonduplicate_pass_rate: {snapshot['prompt_card_nonduplicate_pass_rate']:.3f}",
            f"prompt_card_duplicate_rate: {snapshot['prompt_card_duplicate_rate']:.3f}",
            f"prompt_card_hard_gate_risk: {snapshot['prompt_card_hard_gate_risk']:.3f}",
            f"prompt_card_reroute_penalty: {snapshot['prompt_card_reroute_penalty']:.3f}",
            f"prompt_card_reroute_reasons: {snapshot['prompt_card_reroute_reasons'] or 'none'}",
            f"near_duplicate_threshold: {near_duplicate_threshold:.3f}",
            "duplicate_heavy_intents:",
            *duplicate_lines,
            (
                "policy_instruction: avoid saturated or duplicate-heavy intent pockets; "
                "low prompt-card fitness means previous prompts with this card produced lazy, "
                "invalid, or duplicate patches, so make a more specific nonduplicate edit."
            ),
        ]
    )


def duplicate_heavy_intents(state: PopulationPolicyState, *, limit: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for intent_key, duplicate_count in state.intent_duplicate_counts.items():
        if duplicate_count <= 0:
            continue
        rows.append(
            {
                "intent_key": intent_key,
                "duplicate_count": int(duplicate_count),
                "pass_count": int(state.intent_pass_counts[intent_key]),
                "attempt_count": int(state.intent_attempt_counts[intent_key]),
            }
        )
    rows.sort(key=lambda item: (-item["duplicate_count"], item["intent_key"]))
    return rows[:limit]


def edit_signature_text(diff_text: str) -> str:
    """Return normalized changed replacement lines, not the whole replacement block."""

    try:
        blocks = parse_search_replace_blocks(diff_text)
    except DiffBlockError:
        return normalize_code_lines(diff_text)

    signature_lines: list[str] = []
    for block in blocks:
        search_counts = Counter(normalize_code_lines(block.search).splitlines())
        replacement_lines = normalize_code_lines(block.replace).splitlines()
        changed_lines: list[str] = []
        for line in replacement_lines:
            if search_counts[line] > 0:
                search_counts[line] -= 1
            else:
                changed_lines.append(line)
        signature_lines.extend(changed_lines or replacement_lines)
    return "\n".join(line for line in signature_lines if line)


def normalize_code_lines(text: str) -> str:
    lines: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if line:
            lines.append(re.sub(r"\s+", " ", line))
    return "\n".join(lines)


def tokenize_signature(text: str) -> list[str]:
    return re.findall(
        r"[a-zA-Z_][a-zA-Z0-9_]*|[0-9]+(?:\.[0-9]+)?|==|!=|<=|>=|[-+*/%<>=]",
        text.lower(),
    )


def patch_signature_shingles(signature_text: str, *, shingle_size: int = 5) -> set[str]:
    tokens = tokenize_signature(signature_text)
    if not tokens:
        return set()
    if len(tokens) <= shingle_size:
        return set(tokens)
    return {" ".join(tokens[idx : idx + shingle_size]) for idx in range(len(tokens) - shingle_size + 1)}


def jaccard(left: set[str], right: set[str]) -> float:
    if not left and not right:
        return 1.0
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def _read_text_if_present(raw_path: Any) -> str | None:
    if not raw_path:
        return None
    path = Path(str(raw_path))
    if not path.exists() or not path.is_file():
        return None
    return path.read_text(encoding="utf-8")


__all__ = [
    "DEFAULT_PARENT_PROGRAM_ID",
    "DEFAULT_REJECT_LAZY_PENALTY",
    "BEHAVIORAL_NOOP_FAILURE_CATEGORY",
    "LAZY_PENALTY_BY_FAILURE_CATEGORY",
    "NEAR_DUPLICATE_FAILURE_CATEGORY",
    "PASS_CONTROLLER_SEARCH_SCORE",
    "POPULATION_POLICY_VERSION",
    "PROMPT_FITNESS_POLICY_VERSION",
    "TARGET_INTENT_MISMATCH_CONTROLLER_SCORE",
    "TARGET_INTENT_MISMATCH_LAZY_PENALTY",
    "NoveltyDecision",
    "PopulationPolicyState",
    "check_patch_novelty",
    "choose_population_diversity_target",
    "controller_search_score_for_attempt",
    "edit_signature_text",
    "format_population_policy_context",
    "lazy_penalty_for_attempt",
    "prompt_card_id_for",
    "seed_population_policy_state",
]
