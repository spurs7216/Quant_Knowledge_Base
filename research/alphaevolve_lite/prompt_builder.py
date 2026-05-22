"""Prompt construction for Phase 4 AlphaEvolve-lite child dry runs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .artifact_io import write_json
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
- Do not change fixed IS/OS split logic, universe logic, data paths, duplicate policy, cost accounting, or artifact writing.
- Do not use evaluator-only forward-return fields such as fwd_ret, fwd_date, fwd_vwretd, next_market_date, or one_day_forward.
- Do not add broker, IBKR, TWS, account, position, order, or credential logic.
- If the prompt provides a Target behavior cell, implement that intended patch intent. Do not substitute an easier patch intent.
- Do not use a sign or direction flip unless the intended patch intent is direction_flip.
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


IMMUTABLE_RULES = """You may not change fixed IS/OS split dates or split policy.
You may not change the rolling top-500-by-market-cap universe policy.
You may not change raw data paths.
You may not remove or weaken transaction costs.
You may not edit duplicate policy, return timing, artifact-writing logic, or evaluator gates.
You may not add broker, IBKR, TWS, account, position, order, or credential logic.
You may not add a non-primary dataset unless the prompt explicitly provides a dataset_admission_id.
You may not use evaluator-only forward-return fields such as fwd_ret, fwd_date, fwd_vwretd, next_market_date, or one_day_forward.
You must keep SEARCH blocks strictly inside EVOLVE-BLOCK markers.
"""


DEFAULT_MUTATION_INSTRUCTION = """Improve the generation-zero Kalman innovation reversal seed for the next controller-static dry run.

The hardened sample evaluator showed:
- the seed passes infrastructure gates but loses money after costs;
- turnover is high;
- random matched long/short baselines are worse than the seed;
- the sign-flipped seed is better than the current seed.
- sample pass requires broad active portfolio-day coverage; a sparse few-day book is review evidence, not alpha.
- code changes that are metric-equivalent to the seed are not useful children.
- repairing one caveat, such as missing held weight, is not enough if parent-relative performance or turnover-aware score gets worse.

Prefer bounded changes to signal direction, turnover dampening, ranking transform, or risk controls.
Do not edit loader, universe, split, cost, duplicate, artifact, or data-contract logic.
Return exactly one SEARCH/REPLACE patch.
"""

PARENT_RELATIVE_SEARCH_RULES = """Search-sample and controller metrics are evaluated relative to the current parent, not only in isolation.
Do not optimize a single diagnostic caveat while degrading parent-relative Sharpe, annualized return, turnover-aware score, broad active-day coverage, or max-weight discipline.
For sample_review repair parents, a missing-held-weight reduction is useful only when the child also preserves or improves parent-relative economics and does not create a sparse or metric-equivalent book.
Avoid generic signal compression such as bounded tanh or clipped magnitude dampening as a missing-held-weight repair unless it has a concrete mechanism that should preserve ranking economics after costs.
Repaired IS/OS evidence update: PROG-20260430-CHILD-0017-ISOSREPAIR is the active attempt017 parent lead after the forward-return source repair, but sample_pass is not promotion. Missing-held weight is no longer the main branch objective; preserve the attempt017 OS lead while improving IS robustness, turnover, and cost sensitivity.
Attempt017 mechanism-batch evidence: PROG-20260513-A017-MECH-0007 was a signal/liquidity_adjusted_reversal child with final-weight delta, but sample evaluation was worse than attempt017 on Sharpe, annualized return, turnover-aware score, drawdown, and missing-held exposure. Do not treat signal-side liquidity adjustment as a promoted repair for this branch.
If the target edit is likely to be absorbed by ranking, portfolio selection, or risk normalization so final weights are unchanged, output NO_VALID_PATCH instead of a cosmetic patch.
Controller execution-effect rule: a signal or ranking edit must change ranked signals or final weights; a portfolio or risk edit must change final weights or exposure shape after risk controls. Raw-signal-only rescaling that leaves ranks and final weights unchanged is not useful search progress.
Full validation remains forbidden inside child generation; these rules are search-control guidance for deterministic controller and sample gates.
"""

STAGE0_DAILY_STOCK_MECHANISM_GUIDANCE = """Stage-0 executable children may use only the supplied daily_stock panel and CONTRACT fields.
Useful ex-ante daily_stock fields include CONTRACT.price, CONTRACT.volume, CONTRACT.dollar_volume, CONTRACT.market_cap, CONTRACT.industry_primary, CONTRACT.exchange, and existing status/return-missing flags when present in the panel.
Do not use evaluator-only forward-return fields such as fwd_ret, fwd_date, fwd_vwretd, next_market_date, or one_day_forward.
For the repaired attempt017 branch, prefer mechanisms that change final weights through persistence/no-trade gates, liquidity-weighted side weights, or liquidity-scaled caps. Use industry-neutral ranking only when the target cell explicitly requests it; prior industry-neutral children were cleaner portfolio-shape evidence, not promoted alpha evidence.
Do not answer a liquidity, persistence, or industry-neutral target with generic tanh, clipped magnitude dampening, or raw signal shrinkage.
Do not use inverse raw dollar volume as a uniform signal shrinker. Use bounded relative liquidity, log liquidity, market-cap percentile, or rolling/liquidity confidence logic that can change cross-sectional ordering or selected final weights.
"""

SURFACE_LOCAL_DATA_ACCESS = {
    "signal": (
        "Local data scope: inside the signal block, group is a per-security slice of the full daily_stock "
        "panel, so group[CONTRACT.dollar_volume], group[CONTRACT.volume], group[CONTRACT.market_cap], "
        "and group[CONTRACT.price] are valid when present. Align any derived Series to group.index."
    ),
    "ranking": (
        "Local data scope: the ranking block's data/group frame contains only CONTRACT.date and signal. "
        "To use daily_stock fields, read them from panel with aligned index labels, for example "
        "industry = panel.loc[group.index, CONTRACT.industry_primary]. Do not use "
        "group[CONTRACT.industry_primary] unless the editable body already added that column."
    ),
    "portfolio": (
        "Local data scope: the portfolio block's data/group/valid frames contain CONTRACT.date, "
        "CONTRACT.security_id, and signal only. To use liquidity, price, market cap, exchange, or industry, "
        "read from panel with aligned labels, for example liq = panel.loc[valid.index, "
        "CONTRACT.dollar_volume]. For side-specific values use panel.loc[longs, CONTRACT.dollar_volume] "
        "or panel.loc[shorts, CONTRACT.dollar_volume]. Convert boolean masks to index labels before "
        "assigning weights."
    ),
    "risk": (
        "Local data scope: the risk block's data/group frame contains CONTRACT.date and weight only. "
        "To use liquidity, price, market cap, exchange, or industry, read from panel with aligned labels, "
        "for example liq = panel.loc[group.index, CONTRACT.dollar_volume]. If using a per-name cap Series, "
        "align it to w.index before clipping and renormalize long and short sides separately afterward."
    ),
}


SURFACE_GUIDANCE = {
    "signal": (
        "Edit only the signal EVOLVE-BLOCK. Follow the target behavior cell first. Direction flips are allowed "
        "only when the target intent requests direction_flip; otherwise use the requested bounded damping, "
        "history-confidence, volatility-scaling, or causal-smoothing family. Avoid hard saturation such as tanh "
        "if it can create many tied signals and imbalanced long/short books. For time_smoothing targets, use "
        "causal rolling, EWM, or lagged smoothing; do not substitute a nonlinear magnitude dampener. For "
        "regime_aware_reversal, use causal past benchmark, volatility, or cross-sectional state proxies; "
        "do not fit a hidden-state model on the full timeline or use future labels. Treat "
        "generic bounded or clipped signal dampening as negative evidence on attempt017-style missing-held "
        "repairs unless it preserves parent-relative economics after costs. For liquidity_adjusted_reversal, "
        "use daily_stock liquidity, price, or market-cap proxies as ex-ante confidence signals rather than "
        "a generic magnitude compressor. Avoid inverse raw dollar_volume clipped to a narrow range; it usually "
        "becomes a uniform rescale that leaves ranks and weights unchanged."
    ),
    "ranking": (
        "Edit only the ranking EVOLVE-BLOCK. Follow the target behavior cell first. Direction flips are allowed "
        "only when the target intent requests direction_flip; otherwise use the requested robust center/scale, "
        "rank/percentile transform, winsorization, monotone transform, or cross-sectional shrinkage family. "
        "For industry_neutral_rank, use native daily_stock industry fields such as CONTRACT.industry_primary "
        "with a fallback when a date-industry group is too small. In this seed, read industry from "
        "panel.loc[group.index, CONTRACT.industry_primary], not from group[CONTRACT.industry_primary]. "
        "For the attempt017 branch, repeated industry-neutral ranking is weak/replay evidence unless the patch "
        "beats the occupied-cell elite and preserves parent-relative economics."
    ),
    "portfolio": (
        "Edit only the portfolio EVOLVE-BLOCK. Suitable changes include tighter selection thresholds, "
        "or bounded gross exposure use through local logic. Keep the book active on most eligible sample dates; "
        "name sparsity is acceptable only if it does not collapse the portfolio to a few traded days. "
        "Do not filter names using forward-return availability fields. "
        "If you weight by signal strength, compute positive "
        "long-side magnitudes and positive short-side magnitudes separately, then assign negative weights to "
        "shorts; preserve both long and short exposure and keep net exposure near zero. If you use a boolean "
        "selection mask, convert it to index labels aligned to the target Series before assigning weights. Avoid "
        "threshold or sparsity edits that are absorbed downstream and leave final weights effectively unchanged. "
        "For liquidity_weighted_sides, use current-day liquidity or market-cap proxies only as positive side "
        "magnitudes and avoid formulas that downstream max-weight caps turn back into equal weights. For "
        "persistence_trade_gate, use prior-day signal or same-sign persistence and keep a fallback "
        "when a side becomes too thin. "
        "For no_trade_band_or_sparsity, use a bounded signal margin or persistence condition with a fallback "
        "that keeps both sides broad; do not turn the book into a few-day sparse artifact. "
        "In this seed, read daily_stock fields through panel.loc[valid.index, ...] "
        "or panel.loc[longs/shorts, ...], because valid does not include liquidity or market-cap columns. "
        "The signal column is local data, not a panel column: create data['prior_signal'] with "
        "data.groupby(CONTRACT.security_id)['signal'].shift(1) before the date loop, then use "
        "valid['prior_signal'] or data.loc[valid.index, 'prior_signal']; do not call panel.loc[..., 'signal']."
    ),
    "risk": (
        "Edit only the risk EVOLVE-BLOCK. Suitable changes include stricter concentration control, side-specific "
        "normalization, and conservative handling of small long or short books. Preserve both long and short "
        "books; avoid logic that can make the portfolio one-sided or materially net long/net short. Risk edits "
        "must produce an observable portfolio-shape change after normalization; otherwise output NO_VALID_PATCH. "
        "For liquidity_scaled_cap, the cap formula must bite below current weights for low-liquidity names and "
        "then renormalize long and short sides separately while preserving the max-weight cap. Use per-name "
        "cap values no larger than max_weight, clip, side-renormalize, and clip again. In this seed, read "
        "daily_stock fields through panel.loc[group.index, ...], because group does not include liquidity or "
        "market-cap columns."
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
    sample_coverage = summary.get("sample_coverage", {})
    reference_comparison = summary.get("reference_comparison", {})
    fields = {
        "decision": summary.get("decision"),
        "search_sample_sharpe": metrics.get("sharpe"),
        "search_sample_annualized_return": metrics.get("annualized_return"),
        "search_sample_turnover": metrics.get("turnover"),
        "search_sample_turnover_aware_score": metrics.get("turnover_aware_score"),
        "max_weight": metrics.get("max_weight"),
        "max_missing_held_weight": metrics.get("max_missing_held_weight"),
        "portfolio_days": sample_coverage.get("portfolio_days"),
        "visible_universe_days": sample_coverage.get("visible_universe_days"),
        "portfolio_day_coverage": sample_coverage.get("portfolio_day_coverage"),
        "metric_equivalent_to_reference": reference_comparison.get("metric_equivalent_to_reference"),
        "reference_max_abs_metric_delta": reference_comparison.get("max_abs_metric_delta"),
        "random_sharpe_summary": baseline.get("random_search_sample_sharpe"),
        "random_turnover_aware_summary": baseline.get("random_search_sample_turnover_aware_score"),
        "sign_flip_search_sample": baseline.get("sign_flip_search_sample"),
    }
    return json.dumps(fields, indent=2, sort_keys=True)


def choose_target_surface(
    attempt_index: int,
    *,
    surface_schedule: tuple[str, ...] | list[str] | None = None,
) -> str:
    """Deterministically choose the target mutation surface for an attempt."""

    schedule = tuple(surface_schedule or SURFACE_ORDER)
    if not schedule:
        raise ValueError("surface schedule must not be empty")
    return schedule[attempt_index % len(schedule)]


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
    parent_id: str | None = None,
    prompt_card_id: str | None = None,
    target_surface: str | None = None,
    previous_accepted_patches: list[str] | None = None,
    diversity_target: DiversityTarget | None = None,
    occupied_map_cells: list[str] | None = None,
    forbidden_patches: list[str] | None = None,
    duplicate_retry_reason: str | None = None,
    population_policy_text: str | None = None,
    reasoning_memory_text: str | None = None,
    diagnostic_text: str | None = None,
    skill_text: str | None = None,
    mechanism_card_text: str | None = None,
    mutation_instruction: str = DEFAULT_MUTATION_INSTRUCTION,
) -> dict[str, str]:
    """Build system/user messages for a child-generation attempt."""

    context = compact_evaluator_context(evaluator_summary or {})
    surface = target_surface or choose_target_surface(attempt_index)
    editable_body = editable_block_text(parent_code, surface)
    guidance = SURFACE_GUIDANCE.get(surface, "Edit only the target EVOLVE-BLOCK.")
    data_access_guidance = SURFACE_LOCAL_DATA_ACCESS.get(
        surface,
        "Use only variables available in the editable body and align any new Series to the target index.",
    )
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
    policy_text = (
        population_policy_text.strip()
        if population_policy_text and population_policy_text.strip()
        else "No population-policy context supplied."
    )
    memory_text = reasoning_memory_text.strip() if reasoning_memory_text and reasoning_memory_text.strip() else "None."
    diagnostics = diagnostic_text.strip() if diagnostic_text and diagnostic_text.strip() else "None."
    skills = skill_text.strip() if skill_text and skill_text.strip() else "None."
    mechanism_cards = (
        mechanism_card_text.strip() if mechanism_card_text and mechanism_card_text.strip() else "None."
    )
    user_prompt = f"""Task type: controller_static_child_dry_run
Attempt index: {attempt_index}
Parent program id: {parent_id or "PROG-20260430-000000"}
Prompt card id: {prompt_card_id or "controller_static:unknown"}
Target mutation surface: {surface}
Allowed mutation surface: {surface} only
Data scope: daily_stock_only
Universe policy: rolling_top500_market_cap_v1
Split policy: daily_stock_top500_is_2011_2022_os_2023_2025_v1
daily_stock contract: daily_stock_contract_v1

Relevant evaluator feedback:
{context}

Diagnostic analyzer cards:
```text
{diagnostics}
```

Use diagnostic cards as bottleneck localization, not as proof of market alpha.

Medium-model mechanism cards:
```text
{mechanism_cards}
```

Use mechanism cards as reviewed mechanism hypotheses for this target surface. They are not code, not immutable rules, and not promotion evidence. The target behavior cell remains binding.

Parent-relative search-control rules:
{PARENT_RELATIVE_SEARCH_RULES}

Stage-0 daily_stock mechanism guidance:
{STAGE0_DAILY_STOCK_MECHANISM_GUIDANCE}

Surface-local data access contract:
{data_access_guidance}

Immutable rules:
{IMMUTABLE_RULES}

Relevant reasoning memory:
```text
{memory_text}
```

Use reasoning memory as evidence-grounded operating guidance. It is not proof of market alpha, and it must not override immutable rules or evaluator gates.

Explicit skill library:
```text
{skills}
```

Use high-confidence and avoid skills as operating rules. Treat low-confidence skills as weak hypotheses, and never let any skill override immutable rules or evaluator gates.

Editable code body for target surface `{surface}`:
```python
{editable_body}
```

Only copy SEARCH text from the editable code body above. Do not copy from helper functions, DEFAULT_PARAMS, function signatures, imports, loader code, or EVOLVE marker lines.

MAP-Elites controller diversity:
- MAP-Elites separates a program's performance from user-defined behavior descriptors.
- At this controller-static stage, the behavior cell is based on target surface, patch intent, and portfolio-shape smoke metrics.
- The goal of this attempt is to pass all deterministic gates while filling a distinct behavior cell.
- The intended_patch_intent in the target behavior cell is mandatory; do not substitute a familiar easier intent.
- Do not use the same patch intent or same semantic change as an already occupied same-surface cell.
- Do not use a sign or direction flip unless the intended_patch_intent is direction_flip.
- A controller-safe off-target patch is still weak evidence for the sampled prompt card; implement the target intent directly.

Execution-effect gate:
- A signal/ranking edit that changes only raw signal magnitude but leaves ranked_signal and final weights unchanged will be rejected.
- A portfolio/risk edit that leaves final weights and exposure shape unchanged after risk controls will be rejected.
- If the target mechanism is likely to be fully absorbed by quantile selection, max-weight clipping, or side renormalization, output NO_VALID_PATCH.

Group-relative sibling role:
- This attempt is one sibling in a matched batch from the same parent, evaluator context, data contract, and prompt policy.
- Future skill extraction compares siblings by controller validity, uniqueness, repair burden, and MAP-cell diversity.
- Make one focused semantic change with one clear intent; do not bundle unrelated ideas just to appear novel.

Controller population policy:
```text
{policy_text}
```

Use the population policy as search-control evidence. Avoid duplicate-heavy target intents and near-duplicate edit signatures. The patch still must obey the target behavior cell below.

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
    data_access_guidance = SURFACE_LOCAL_DATA_ACCESS.get(
        surface,
        "Use only variables available in the editable body and align any new Series to the target index.",
    )
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

Surface-local data access contract:
{data_access_guidance}

Repair instruction:
Shrink, retarget, or minimally correct the patch so the SEARCH text is copied exactly from the editable code body above and contains no EVOLVE marker lines, function definitions, helper code, or DEFAULT_PARAMS code. If the failure was a runtime/vector-smoke error, fix only the local API or expression mistake; for daily_stock field KeyError failures, replace local-frame field access with panel.loc[...] access aligned to the same index. For portfolio persistence gates, remember that signal is local data, not a panel field; use data.groupby(CONTRACT.security_id)["signal"].shift(1) rather than panel.loc[..., "signal"]. For pandas boolean indexers, assign with index labels aligned to the target Series, not with a boolean Series from a different index. If the failure was a portfolio semantic error, preserve both long and short exposure, keep short weights negative, keep long weights positive, and keep net exposure near zero. If the failure was execution_effect_failed, make the original mechanism observable in ranked_signal, final weights, or exposure shape after downstream controls; otherwise output NO_VALID_PATCH. Preserve the original idea only if it can be expressed safely inside this target surface. Output exactly one safe SEARCH/REPLACE block, or output exactly NO_VALID_PATCH.
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
    write_json(json_path, messages)
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
    "PARENT_RELATIVE_SEARCH_RULES",
    "REPAIR_SYSTEM_PROMPT",
    "STAGE0_DAILY_STOCK_MECHANISM_GUIDANCE",
    "SURFACE_LOCAL_DATA_ACCESS",
    "STRICT_SEARCH_REPLACE_SYSTEM_PROMPT",
    "build_child_generation_prompt",
    "build_patch_repair_prompt",
    "choose_target_surface",
    "editable_block_text",
    "extract_evolve_block_bodies",
    "load_json_if_exists",
    "write_prompt_artifact",
]
