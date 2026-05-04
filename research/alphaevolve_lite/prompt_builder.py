"""Prompt construction for Phase 4 AlphaEvolve-lite child dry runs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .diversity import DiversityTarget, format_diversity_target
from .evolve_blocks import END_MARKER, START_MARKER


SURFACE_ORDER = ("signal", "ranking", "portfolio", "risk")

STRICT_SEARCH_REPLACE_SYSTEM_PROMPT = """You are a code patch generator for a quantitative research AlphaEvolve loop.

You must output only SEARCH/REPLACE blocks in exactly this format:

<<<<<<< SEARCH
exact original code
=======
replacement code
>>>>>>> REPLACE

Rules:
- No markdown fences.
- No explanation.
- No hidden reasoning, scratchpad, analysis, or thought process.
- The SEARCH text must be copied exactly from the current code.
- The output must contain the literal final line: >>>>>>> REPLACE.
- The SEARCH block must contain only lines strictly between # EVOLVE-BLOCK-START and # EVOLVE-BLOCK-END.
- Do not include function definitions in the SEARCH block.
- Do not include # EVOLVE-BLOCK-START or # EVOLVE-BLOCK-END in the SEARCH block.
- Do not introduce new imports, new global names, file I/O, data loading, or undeclared dependencies.
- Do not change train/validation/test split logic, universe logic, data paths, duplicate policy, cost accounting, or artifact writing.
- Do not add broker, IBKR, TWS, account, position, order, or credential logic.
- If no valid change is possible, output exactly: NO_VALID_PATCH.
"""


REPAIR_SYSTEM_PROMPT = """You repair unsafe or malformed AlphaEvolve SEARCH/REPLACE patches.

You must output exactly one SEARCH/REPLACE block using this literal format:

<<<<<<< SEARCH
exact original code
=======
replacement code
>>>>>>> REPLACE

Rules:
- No markdown fences.
- No explanation.
- No hidden reasoning, scratchpad, analysis, or thought process.
- The SEARCH text must be copied exactly from the editable code body supplied by the user.
- The SEARCH block must contain only code strictly inside the EVOLVE-BLOCK.
- Do not include function definitions.
- Do not include # EVOLVE-BLOCK-START or # EVOLVE-BLOCK-END.
- Preserve the intended semantic change when it can be expressed safely inside the target EVOLVE-BLOCK.
- Do not invent a new strategy idea during repair.
- If no valid safe repair is possible, output exactly: NO_VALID_PATCH.
"""


IMMUTABLE_RULES = """You may not change train/validation/test split dates or split proportions.
You may not change the rolling top-500-by-market-cap universe policy.
You may not change raw data paths.
You may not remove or weaken transaction costs.
You may not edit duplicate policy, return timing, artifact-writing logic, or evaluator gates.
You may not add broker, IBKR, TWS, account, position, order, or credential logic.
You may not add a non-primary dataset unless the prompt explicitly provides a dataset_admission_id.
You must keep SEARCH blocks strictly inside EVOLVE-BLOCK markers.
"""


DEFAULT_MUTATION_INSTRUCTION = """Improve the generation-zero Kalman innovation reversal seed for the next controller-static dry run.

The hardened sample evaluator showed:
- the seed passes infrastructure gates but loses money after costs;
- turnover is high;
- random matched long/short baselines are worse than the seed;
- the sign-flipped seed is better than the current seed.

Prefer bounded changes to signal direction, turnover dampening, ranking transform, or risk controls.
Do not edit loader, universe, split, cost, duplicate, artifact, or data-contract logic.
Return exactly one SEARCH/REPLACE patch.
"""


SURFACE_GUIDANCE = {
    "signal": (
        "Edit only the signal EVOLVE-BLOCK. Suitable changes include flipping the signal after volatility "
        "scaling, adding bounded nonlinear damping, changing causal smoothing inside the existing group loop, "
        "or attenuating noisy short-history observations. Avoid hard saturation such as tanh if it can create "
        "many tied signals and imbalanced long/short books."
    ),
    "ranking": (
        "Edit only the ranking EVOLVE-BLOCK. Suitable changes include flipping ranked direction, robust "
        "winsorization choices, monotone transforms, or stronger cross-sectional shrinkage."
    ),
    "portfolio": (
        "Edit only the portfolio EVOLVE-BLOCK. Suitable changes include tighter selection thresholds, "
        "or bounded gross exposure use through local logic. If you weight by signal strength, compute positive "
        "long-side magnitudes and positive short-side magnitudes separately, then assign negative weights to "
        "shorts; preserve both long and short exposure and keep net exposure near zero."
    ),
    "risk": (
        "Edit only the risk EVOLVE-BLOCK. Suitable changes include stricter concentration control, side-specific "
        "normalization, and conservative handling of small long or short books. Preserve both long and short "
        "books; avoid logic that can make the portfolio one-sided or materially net long/net short."
    ),
}


def load_json_if_exists(path: str | Path | None) -> dict[str, Any]:
    if not path:
        return {}
    file_path = Path(path)
    if not file_path.exists():
        return {}
    return json.loads(file_path.read_text(encoding="utf-8"))


def compact_evaluator_context(summary: dict[str, Any]) -> str:
    """Extract prompt-facing evaluator evidence from a hardened summary."""

    if not summary:
        return "No evaluator summary supplied."
    metrics = summary.get("metrics", {}).get("search_sample", {})
    baseline = summary.get("baseline_summary", {})
    fields = {
        "decision": summary.get("decision"),
        "search_sample_sharpe": metrics.get("sharpe"),
        "search_sample_annualized_return": metrics.get("annualized_return"),
        "search_sample_turnover": metrics.get("turnover"),
        "search_sample_turnover_aware_score": metrics.get("turnover_aware_score"),
        "max_weight": metrics.get("max_weight"),
        "max_missing_held_weight": metrics.get("max_missing_held_weight"),
        "random_sharpe_summary": baseline.get("random_search_sample_sharpe"),
        "random_turnover_aware_summary": baseline.get("random_search_sample_turnover_aware_score"),
        "sign_flip_search_sample": baseline.get("sign_flip_search_sample"),
    }
    return json.dumps(fields, indent=2, sort_keys=True)


def choose_target_surface(attempt_index: int) -> str:
    """Deterministically rotate target mutation surfaces across attempts."""

    return SURFACE_ORDER[attempt_index % len(SURFACE_ORDER)]


def extract_evolve_block_bodies(parent_code: str) -> dict[str, str]:
    """Return evolve-block bodies keyed by marker name.

    The seed uses markers such as ``# EVOLVE-BLOCK-START: signal``. Only the
    body between the markers is returned, which is the only valid SEARCH source.
    """

    blocks: dict[str, str] = {}
    lines = parent_code.splitlines(keepends=True)
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
            blocks[current_name] = "".join(current_body)
            current_name = None
            current_body = []
            continue
        if current_name is not None:
            current_body.append(line)
    return blocks


def editable_block_text(parent_code: str, target_surface: str) -> str:
    blocks = extract_evolve_block_bodies(parent_code)
    try:
        return blocks[target_surface]
    except KeyError as exc:
        allowed = ", ".join(sorted(blocks))
        raise ValueError(f"target surface {target_surface!r} not found; allowed: {allowed}") from exc


def build_child_generation_prompt(
    *,
    parent_code: str,
    evaluator_summary: dict[str, Any] | None = None,
    attempt_index: int = 0,
    target_surface: str | None = None,
    previous_accepted_patches: list[str] | None = None,
    diversity_target: DiversityTarget | None = None,
    occupied_map_cells: list[str] | None = None,
    forbidden_patches: list[str] | None = None,
    duplicate_retry_reason: str | None = None,
    reasoning_memory_text: str | None = None,
    mutation_instruction: str = DEFAULT_MUTATION_INSTRUCTION,
) -> dict[str, str]:
    """Build system/user messages for a child-generation attempt."""

    context = compact_evaluator_context(evaluator_summary or {})
    surface = target_surface or choose_target_surface(attempt_index)
    editable_body = editable_block_text(parent_code, surface)
    guidance = SURFACE_GUIDANCE.get(surface, "Edit only the target EVOLVE-BLOCK.")
    previous_patch_text = "None."
    if previous_accepted_patches:
        previous_patch_text = "\n\n".join(
            f"Previous accepted patch {idx + 1}:\n{patch.strip()}"
            for idx, patch in enumerate(previous_accepted_patches)
        )
    occupied_text = "None."
    if occupied_map_cells:
        occupied_text = "\n".join(f"- {cell}" for cell in occupied_map_cells[-12:])
    forbidden_patch_text = "None."
    if forbidden_patches:
        forbidden_patch_text = "\n\n".join(
            f"Forbidden duplicate patch {idx + 1}:\n{patch.strip()}"
            for idx, patch in enumerate(forbidden_patches[-3:])
        )
    retry_text = "This is an initial generation attempt."
    if duplicate_retry_reason:
        retry_text = (
            "This is a duplicate-retry generation attempt. The previous patch passed safety gates "
            f"but was rejected for diversity: {duplicate_retry_reason}"
        )
    memory_text = reasoning_memory_text.strip() if reasoning_memory_text and reasoning_memory_text.strip() else "None."
    user_prompt = f"""Task type: controller_static_child_dry_run
Attempt index: {attempt_index}
Target mutation surface: {surface}
Allowed mutation surface: {surface} only
Data scope: daily_stock_only
Universe policy: rolling_top500_market_cap_v1
Split policy: daily_stock_top500_chrono_70_15_15_v1
daily_stock contract: daily_stock_contract_v1

Relevant evaluator feedback:
{context}

Immutable rules:
{IMMUTABLE_RULES}

Relevant reasoning memory:
```text
{memory_text}
```

Use reasoning memory as evidence-grounded operating guidance. It is not proof of market alpha, and it must not override immutable rules or evaluator gates.

Editable code body for target surface `{surface}`:
```python
{editable_body}
```

Only copy SEARCH text from the editable code body above. Do not copy from helper functions, DEFAULT_PARAMS, function signatures, imports, loader code, or EVOLVE marker lines.

MAP-Elites controller diversity:
- MAP-Elites separates a program's performance from user-defined behavior descriptors.
- At this controller-static stage, the behavior cell is based on target surface, patch intent, and portfolio-shape smoke metrics.
- The goal of this attempt is to pass all deterministic gates while filling a distinct behavior cell.
- Do not use the same patch intent or same semantic change as an already occupied same-surface cell.

Group-relative sibling role:
- This attempt is one sibling in a matched batch from the same parent, evaluator context, data contract, and prompt policy.
- Future skill extraction compares siblings by controller validity, uniqueness, repair burden, and MAP-cell diversity.
- Make one focused semantic change with one clear intent; do not bundle unrelated ideas just to appear novel.

Target behavior cell:
```text
{format_diversity_target(diversity_target)}
```

Already occupied controller MAP cells:
```text
{occupied_text}
```

Previously accepted patches for target surface `{surface}`:
```text
{previous_patch_text}
```

Do not repeat the same SEARCH/REPLACE patch or the same semantic change as a previous accepted patch for this surface.

Forbidden duplicate patches:
```text
{forbidden_patch_text}
```

Retry context:
{retry_text}

Portfolio semantic constraints:
- active days must retain both positive and negative weights;
- short-side weights must remain negative and long-side weights must remain positive;
- net exposure must stay near zero after risk controls;
- avoid transforms that create many tied signals and unbalanced long/short counts.

Output format example:
<<<<<<< SEARCH
    old_line
=======
    new_line
>>>>>>> REPLACE

Task:
{mutation_instruction}

Target-surface guidance:
{guidance}

Output exactly one SEARCH/REPLACE block. Do not write commentary.
"""
    return {
        "system": STRICT_SEARCH_REPLACE_SYSTEM_PROMPT,
        "user": user_prompt,
    }


def build_patch_repair_prompt(
    *,
    parent_code: str,
    unsafe_patch: str,
    failure_reason: str,
    attempt_index: int = 0,
    target_surface: str | None = None,
) -> dict[str, str]:
    """Build a one-shot repair prompt for an unsafe child patch."""

    surface = target_surface or choose_target_surface(attempt_index)
    editable_body = editable_block_text(parent_code, surface)
    user_prompt = f"""Task type: controller_static_patch_repair
Target mutation surface: {surface}
Allowed mutation surface: {surface} only

Editable code body for target surface `{surface}`:
```python
{editable_body}
```

Unsafe patch:
```text
{unsafe_patch}
```

Reason rejected:
{failure_reason}

Repair instruction:
Shrink, retarget, or minimally correct the patch so the SEARCH text is copied exactly from the editable code body above and contains no EVOLVE marker lines, function definitions, helper code, or DEFAULT_PARAMS code. If the failure was a runtime/vector-smoke error, fix only the local API or expression mistake. If the failure was a portfolio semantic error, preserve both long and short exposure, keep short weights negative, keep long weights positive, and keep net exposure near zero. Preserve the original idea only if it can be expressed safely inside this target surface. Output exactly one safe SEARCH/REPLACE block, or output exactly NO_VALID_PATCH.
"""
    return {
        "system": REPAIR_SYSTEM_PROMPT,
        "user": user_prompt,
    }


def write_prompt_artifact(out_dir: str | Path, messages: dict[str, str]) -> dict[str, str]:
    path = Path(out_dir)
    path.mkdir(parents=True, exist_ok=True)
    json_path = path / "prompt.json"
    md_path = path / "prompt.md"
    json_path.write_text(json.dumps(messages, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(
        "\n".join(
            [
                "# Child Generation Prompt",
                "",
                "## System",
                "",
                "```text",
                messages["system"],
                "```",
                "",
                "## User",
                "",
                "```text",
                messages["user"],
                "```",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return {"json": str(json_path), "markdown": str(md_path)}


__all__ = [
    "DEFAULT_MUTATION_INSTRUCTION",
    "IMMUTABLE_RULES",
    "REPAIR_SYSTEM_PROMPT",
    "STRICT_SEARCH_REPLACE_SYSTEM_PROMPT",
    "build_child_generation_prompt",
    "build_patch_repair_prompt",
    "choose_target_surface",
    "editable_block_text",
    "extract_evolve_block_bodies",
    "load_json_if_exists",
    "write_prompt_artifact",
]
