"""Parent-zoo planning helpers for cost-aware Phase 4 controller batches."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from .artifact_io import write_json
from .mechanism_cards import normalize_mechanism_cards, render_mechanism_cards
from .paths import utc_now_iso, write_text
from .seed_zoo import SEED_ZOO_SCHEMA_VERSION, write_seed_zoo_programs


PARENT_ZOO_SCHEMA_VERSION = "phase4_parent_zoo_v1"
DEFAULT_ATTEMPT017_PROGRAM_ID = "PROG-20260430-CHILD-0017-ISOSREPAIR"
DEFAULT_ATTEMPT017_ROOT_ID = "attempt017_isos_repair"
DEFAULT_PARENT_ZOO_ROOT_IDS = (
    DEFAULT_ATTEMPT017_ROOT_ID,
    "five_day_excess_reversal",
    "vol_norm_five_day_reversal",
)


@dataclass(frozen=True)
class ParentZooRootSpec:
    """One root for a multi-parent controller-static batch."""

    root_id: str
    role: str
    program_id: str
    strategy_id: str
    strategy_family: str
    source_kind: str
    default_program_path: str
    default_evaluator_summary_path: str
    target_cell_schedule: tuple[str, ...]
    attempts: int
    thesis: str
    caveat: str


DEFAULT_ROOT_SPECS: tuple[ParentZooRootSpec, ...] = (
    ParentZooRootSpec(
        root_id=DEFAULT_ATTEMPT017_ROOT_ID,
        role="incumbent",
        program_id=DEFAULT_ATTEMPT017_PROGRAM_ID,
        strategy_id="attempt017_isos_repair",
        strategy_family="daily_stock_attempt017",
        source_kind="artifact_program_snapshot",
        default_program_path=(
            "artifacts/phase4_alphaevolve/"
            "remote_sample_eval_attempt017_is_os_forward_repair_20260519/program_snapshot.py"
        ),
        default_evaluator_summary_path=(
            "artifacts/phase4_alphaevolve/"
            "remote_sample_eval_attempt017_is_os_forward_repair_20260519/evaluator_summary.json"
        ),
        target_cell_schedule=(
            "portfolio/persistence_trade_gate",
            "portfolio/no_trade_band_or_sparsity",
            "portfolio/liquidity_weighted_sides",
            "risk/liquidity_scaled_cap",
            "signal/regime_aware_reversal",
            "signal/time_smoothing",
        ),
        attempts=6,
        thesis=(
            "Incumbent repaired attempt017 has the best costed sample evidence; mutate it only "
            "toward turnover and cost robustness without losing broad-book alpha."
        ),
        caveat="Do not optimize missing-held weight; that issue was largely repaired by evaluator contract fixes.",
    ),
    ParentZooRootSpec(
        root_id="five_day_excess_reversal",
        role="active_seed_root",
        program_id="PROG-20260521-SEEDZOO-0002",
        strategy_id="five_day_excess_reversal",
        strategy_family="daily_stock_seed_zoo",
        source_kind="rendered_seed_zoo_program",
        default_program_path="",
        default_evaluator_summary_path=(
            "artifacts/phase4_alphaevolve/seed_zoo_is_os_20260521/"
            "evaluations/five_day_excess_reversal/evaluator_summary.json"
        ),
        target_cell_schedule=(
            "portfolio/no_trade_band_or_sparsity",
            "portfolio/persistence_trade_gate",
            "signal/time_smoothing",
            "risk/liquidity_scaled_cap",
            "signal/regime_aware_reversal",
            "ranking/robust_center_scale",
        ),
        attempts=6,
        thesis=(
            "Best deterministic seed at 2.5 bps; it preserves simple five-day reversal structure "
            "but needs lower turnover and better OS behavior."
        ),
        caveat="Not promoted: it trails attempt017 and has weak OS Sharpe.",
    ),
    ParentZooRootSpec(
        root_id="vol_norm_five_day_reversal",
        role="active_seed_root",
        program_id="PROG-20260521-SEEDZOO-0003",
        strategy_id="vol_norm_five_day_reversal",
        strategy_family="daily_stock_seed_zoo",
        source_kind="rendered_seed_zoo_program",
        default_program_path="",
        default_evaluator_summary_path=(
            "artifacts/phase4_alphaevolve/seed_zoo_is_os_20260521/"
            "evaluations/vol_norm_five_day_reversal/evaluator_summary.json"
        ),
        target_cell_schedule=(
            "portfolio/no_trade_band_or_sparsity",
            "signal/regime_aware_reversal",
            "portfolio/persistence_trade_gate",
            "risk/liquidity_scaled_cap",
            "ranking/rank_transform",
            "signal/time_smoothing",
        ),
        attempts=6,
        thesis=(
            "Volatility-normalized reversal has useful gross and positive OS evidence, but the "
            "edge is cost-fragile."
        ),
        caveat="Use as a branch for cost-aware execution, not as a promoted candidate.",
    ),
    ParentZooRootSpec(
        root_id="momentum_reversal_blend",
        role="optional_diagnostic_root",
        program_id="PROG-20260521-SEEDZOO-0008",
        strategy_id="momentum_reversal_blend",
        strategy_family="daily_stock_seed_zoo",
        source_kind="rendered_seed_zoo_program",
        default_program_path="",
        default_evaluator_summary_path=(
            "artifacts/phase4_alphaevolve/seed_zoo_is_os_20260521/"
            "evaluations/momentum_reversal_blend/evaluator_summary.json"
        ),
        target_cell_schedule=(
            "portfolio/no_trade_band_or_sparsity",
            "portfolio/persistence_trade_gate",
            "risk/liquidity_scaled_cap",
            "ranking/robust_center_scale",
        ),
        attempts=4,
        thesis="Lowest-turnover broad deterministic seed; useful as a diagnostic branch if budget allows.",
        caveat="Not a lead because both IS and OS Sharpe are negative at the active cost setting.",
    ),
)


DEFAULT_PARENT_ZOO_MECHANISM_CARDS: tuple[dict[str, Any], ...] = (
    {
        "card_id": "pzoo_no_trade_band_cost_preserve",
        "surface": "portfolio",
        "intent": "no_trade_band_or_sparsity",
        "priority": 9.0,
        "status": "active",
        "thesis": (
            "Add a bounded no-trade or margin band so weak tail names are retained or skipped "
            "only when the side remains broad."
        ),
        "expected_effect": "Lower turnover without collapsing active portfolio-day coverage or one side of the book.",
        "required_data_fields": ["signal"],
        "implementation_hints": [
            "Use current ranked signal distance from the tail cutoff or prior same-sign support.",
            "Keep a fallback to the parent tails when a side becomes too thin.",
            "Preserve separate long and short exposure normalization.",
        ],
        "avoid": [
            "Do not use forward-return availability fields.",
            "Do not create a sparse few-day book.",
            "Do not use an unaligned boolean Series to assign weights.",
        ],
        "sample_eval_hypothesis": (
            "Search-sample turnover falls while Sharpe and active-day coverage remain parent-relative stable."
        ),
    },
    {
        "card_id": "pzoo_persistence_gate_turnover",
        "surface": "portfolio",
        "intent": "persistence_trade_gate",
        "priority": 8.5,
        "status": "active",
        "thesis": "Require prior-day same-sign support or a large current signal margin before replacing names.",
        "expected_effect": "Reduce daily churn while keeping the same reversal direction and balanced books.",
        "required_data_fields": ["signal", "CONTRACT.security_id"],
        "implementation_hints": [
            "Create prior_signal from data.groupby(CONTRACT.security_id)['signal'].shift(1).",
            "Use a side-specific fallback if persistence removes too many longs or shorts.",
        ],
        "avoid": [
            "Do not read panel.loc[..., 'signal']; signal is local data.",
            "Do not require persistence so strictly that one side disappears.",
        ],
        "sample_eval_hypothesis": "Turnover-aware score improves more than raw Sharpe changes.",
    },
    {
        "card_id": "pzoo_regime_aware_reversal",
        "surface": "signal",
        "intent": "regime_aware_reversal",
        "priority": 8.0,
        "status": "active",
        "thesis": (
            "Use a causal two-state or HMM-like market regime proxy to adjust reversal confidence "
            "instead of adding a full unrestricted hidden-state model."
        ),
        "expected_effect": "Preserve reversal in normal states and dampen or change horizon in stressed regimes.",
        "required_data_fields": ["CONTRACT.benchmark_return_primary", "CONTRACT.ex_dividend_return"],
        "implementation_hints": [
            "Use rolling or EWM benchmark volatility/return state known at date t.",
            "Name the state variable explicitly as a causal proxy, not a fitted full-sample HMM.",
            "Prefer bounded state weights that can change ranks but do not erase signal direction.",
        ],
        "avoid": [
            "Do not fit on the full timeline.",
            "Do not add sklearn, hmmlearn, file I/O, or global state.",
            "Do not use future returns or OS labels to define regimes.",
        ],
        "sample_eval_hypothesis": (
            "IS robustness improves and OS Sharpe does not depend only on the 2023-2025 regime."
        ),
    },
    {
        "card_id": "pzoo_causal_smoothing_horizon",
        "surface": "signal",
        "intent": "time_smoothing",
        "priority": 7.5,
        "status": "active",
        "thesis": "Use causal smoothing or horizon blending to reduce turnover while preserving reversal ranks.",
        "expected_effect": "Lower turnover and fewer rank flips without a generic magnitude compressor.",
        "required_data_fields": ["CONTRACT.security_id", "signal"],
        "implementation_hints": [
            "Use rolling or EWM logic with per-security grouping.",
            "Do not substitute tanh or clipping when the target is smoothing.",
        ],
        "avoid": ["Do not use centered windows.", "Do not hard-saturate all signals into ties."],
        "sample_eval_hypothesis": "Cost-grid degradation from 0 to 2.5 bps narrows.",
    },
    {
        "card_id": "pzoo_liquidity_cap_after_normalization",
        "surface": "risk",
        "intent": "liquidity_scaled_cap",
        "priority": 7.0,
        "status": "active",
        "thesis": "Scale effective single-name caps by ex-ante liquidity or market cap, then renormalize by side.",
        "expected_effect": "Reduce low-liquidity concentration without changing net exposure or max-weight safety.",
        "required_data_fields": ["CONTRACT.dollar_volume", "CONTRACT.market_cap", "weight"],
        "implementation_hints": [
            "Read daily_stock fields via panel.loc[group.index, ...].",
            "Clip caps at or below max_weight, side-renormalize, then clip again.",
        ],
        "avoid": ["Do not loosen max_weight.", "Do not make the book one-sided after caps."],
        "sample_eval_hypothesis": "Max weight stays safe while turnover-aware score improves after costs.",
    },
    {
        "card_id": "pzoo_robust_rank_cost_stability",
        "surface": "ranking",
        "intent": "robust_center_scale",
        "priority": 6.0,
        "status": "active",
        "thesis": "Use robust cross-sectional centering/scaling to reduce unstable marginal rank flips.",
        "expected_effect": "Fewer noisy boundary changes with preserved reversal order among strong signals.",
        "required_data_fields": ["signal"],
        "implementation_hints": [
            "Prefer median/MAD or quantile-stable scaling inside each date.",
            "Preserve monotone ordering for strong signals where possible.",
        ],
        "avoid": ["Do not direction-flip.", "Do not neutralize industries unless the target asks for it."],
        "sample_eval_hypothesis": "Turnover falls or Sharpe degradation narrows without losing broad coverage.",
    },
)


def default_parent_zoo_roots(root_ids: Iterable[str] | None = None) -> list[ParentZooRootSpec]:
    """Return selected parent roots in frozen parent-zoo order."""

    specs = list(DEFAULT_ROOT_SPECS)
    if root_ids is None:
        wanted = set(DEFAULT_PARENT_ZOO_ROOT_IDS)
    else:
        wanted = {root_id.strip() for root_id in root_ids if root_id.strip()}
        if not wanted or wanted == {"all"}:
            wanted = {spec.root_id for spec in specs}
    available = {spec.root_id for spec in specs}
    missing = sorted(wanted - available)
    if missing:
        raise ValueError(f"unknown parent-zoo roots: {missing}; available={sorted(available)}")
    return [spec for spec in specs if spec.root_id in wanted]


def default_parent_zoo_mechanism_cards() -> dict[str, Any]:
    """Return normalized default mechanism cards for the parent-zoo batch."""

    return normalize_mechanism_cards(
        {
            "schema_version": "phase4_mechanism_cards_v1",
            "source_model": "codex_hand_authored",
            "review_summary": (
                "Seed-zoo evidence shows gross reversal structure before costs, but daily churn "
                "consumes the edge. Use cards to target cost-aware preservation and causal regime logic."
            ),
            "cards": list(DEFAULT_PARENT_ZOO_MECHANISM_CARDS),
        }
    )


def write_parent_zoo_plan(
    out_dir: str | Path,
    *,
    root_ids: Iterable[str] | None = None,
    db_path: str,
    controller_script: str,
    program_id_prefix: str,
    attempts_per_root: int | None = None,
    mechanism_card_path: str | Path | None = None,
    prior_summary_paths: Iterable[str] = (),
    model_role: str = "fast_generator",
    temperature_grid: str = "0.0,0.2,0.5",
    max_tokens: int = 8192,
    incumbent_summary_path: str = "",
) -> dict[str, Any]:
    """Write parent-zoo roots, mechanism cards, and controller command artifacts."""

    root = Path(out_dir)
    root.mkdir(parents=True, exist_ok=True)
    selected_roots = default_parent_zoo_roots(root_ids)
    seed_roots = [spec.strategy_id for spec in selected_roots if spec.source_kind == "rendered_seed_zoo_program"]
    seed_manifest = None
    rendered_seed_paths: dict[str, str] = {}
    if seed_roots:
        seed_manifest = write_seed_zoo_programs(root / "seed_zoo_parents", seed_ids=seed_roots)
        rendered_seed_paths = {
            row["seed_id"]: row["program_path"] for row in seed_manifest.get("programs", [])
        }

    if mechanism_card_path:
        cards_path = Path(mechanism_card_path)
    else:
        card_payload = default_parent_zoo_mechanism_cards()
        cards_path = root / "parent_zoo_mechanism_cards.json"
        write_json(cards_path, card_payload)
        write_text(
            root / "parent_zoo_mechanism_cards.md",
            "# Parent Zoo Mechanism Cards\n\n" + render_mechanism_cards(card_payload["cards"]) + "\n",
        )

    root_rows = []
    for spec in selected_roots:
        program_path = rendered_seed_paths.get(spec.strategy_id, spec.default_program_path)
        root_rows.append(
            {
                "root_id": spec.root_id,
                "role": spec.role,
                "program_id": spec.program_id,
                "strategy_id": spec.strategy_id,
                "strategy_family": spec.strategy_family,
                "source_kind": spec.source_kind,
                "program_path": program_path,
                "evaluator_summary_path": spec.default_evaluator_summary_path,
                "target_cell_schedule": list(spec.target_cell_schedule),
                "attempts": int(attempts_per_root or spec.attempts),
                "thesis": spec.thesis,
                "caveat": spec.caveat,
            }
        )

    manifest = {
        "schema_version": PARENT_ZOO_SCHEMA_VERSION,
        "created_at": utc_now_iso(),
        "stage": "parent_zoo_cost_aware_controller_batch",
        "out_dir": str(root),
        "root_count": len(root_rows),
        "roots": root_rows,
        "seed_zoo_schema_version": SEED_ZOO_SCHEMA_VERSION,
        "seed_zoo_manifest_path": str(root / "seed_zoo_parents" / "seed_zoo_manifest.json")
        if seed_manifest
        else None,
        "mechanism_card_path": str(cards_path),
        "db_path": db_path,
        "controller_script": controller_script,
        "model_role": model_role,
        "max_tokens": max_tokens,
        "prior_summary_paths": list(prior_summary_paths),
        "incumbent_program_id": DEFAULT_ATTEMPT017_PROGRAM_ID,
        "incumbent_summary_path": incumbent_summary_path,
        "objective": (
            "Preserve reversal signal while reducing turnover and cost sensitivity. "
            "Reject sparse books, gross-only wins, and OS-only improvements with bad IS behavior."
        ),
    }
    write_json(root / "parent_zoo_manifest.json", manifest)
    _write_manifest_md(root / "parent_zoo_manifest.md", manifest)
    commands = build_parent_zoo_commands(
        manifest,
        db_path=db_path,
        controller_script=controller_script,
        program_id_prefix=program_id_prefix,
        mechanism_card_path=str(cards_path),
        prior_summary_paths=prior_summary_paths,
        model_role=model_role,
        temperature_grid=temperature_grid,
        max_tokens=max_tokens,
        incumbent_summary_path=incumbent_summary_path,
    )
    write_parent_zoo_command_artifacts(root, commands)
    return {"manifest": manifest, "commands": commands}


def build_parent_zoo_commands(
    manifest: dict[str, Any],
    *,
    db_path: str,
    controller_script: str,
    program_id_prefix: str,
    mechanism_card_path: str,
    prior_summary_paths: Iterable[str] = (),
    model_role: str = "fast_generator",
    temperature_grid: str = "0.0,0.2,0.5",
    max_tokens: int = 8192,
    incumbent_summary_path: str = "",
) -> list[dict[str, Any]]:
    """Build one controller command per parent root."""

    commands: list[dict[str, Any]] = []
    parent_prefix = Path(str(manifest.get("out_dir") or manifest.get("stage", "parent_zoo")))
    for idx, row in enumerate(manifest.get("roots", [])):
        root_id = row["root_id"]
        command_prefix = f"{program_id_prefix}-{idx:02d}"
        argv = [
            "python",
            controller_script,
            "--program-path",
            row["program_path"],
            "--parent-program-id",
            row["program_id"],
            "--parent-root-id",
            root_id,
            "--parent-strategy-id",
            row["strategy_id"],
            "--evaluator-summary",
            row["evaluator_summary_path"],
            "--out-dir",
            str(parent_prefix / "controller" / root_id),
            "--db-path",
            db_path,
            "--attempts",
            str(row["attempts"]),
            "--target-cell-schedule",
            ",".join(row["target_cell_schedule"]),
            "--mechanism-card-path",
            mechanism_card_path,
            "--model-role",
            model_role,
            "--temperature-grid",
            temperature_grid,
            "--max-tokens",
            str(max_tokens),
            "--program-id-prefix",
            command_prefix,
        ]
        if incumbent_summary_path:
            argv.extend(["--incumbent-program-id", DEFAULT_ATTEMPT017_PROGRAM_ID])
            argv.extend(["--incumbent-summary", incumbent_summary_path])
        for prior_summary in prior_summary_paths:
            argv.extend(["--prior-summary", prior_summary])
        commands.append(
            {
                "root_id": root_id,
                "program_id": row["program_id"],
                "strategy_id": row["strategy_id"],
                "out_dir": str(parent_prefix / "controller" / root_id),
                "argv": argv,
            }
        )
    return commands


def write_parent_zoo_command_artifacts(out_dir: str | Path, commands: list[dict[str, Any]]) -> None:
    """Write command artifacts for the remote operator."""

    root = Path(out_dir)
    # Fix command out_dir paths to the actual root after command construction.
    fixed_commands = []
    for command in commands:
        fixed = dict(command)
        fixed["out_dir"] = str(root / "controller" / command["root_id"])
        argv = list(command["argv"])
        for idx, value in enumerate(argv):
            if value == "--out-dir" and idx + 1 < len(argv):
                argv[idx + 1] = fixed["out_dir"]
        fixed["argv"] = argv
        fixed_commands.append(fixed)
    write_json(root / "parent_zoo_commands.json", fixed_commands)
    lines = ["#!/usr/bin/env bash", "set -euo pipefail", ""]
    for command in fixed_commands:
        lines.append(_shell_join(command["argv"]))
    write_text(root / "parent_zoo_commands.sh", "\n\n".join(lines) + "\n")
    _write_command_csv(root / "parent_zoo_commands.csv", fixed_commands)


def _write_manifest_md(path: Path, manifest: dict[str, Any]) -> None:
    lines = [
        "# Parent Zoo Manifest",
        "",
        f"- schema_version: `{manifest['schema_version']}`",
        f"- stage: `{manifest['stage']}`",
        f"- root_count: `{manifest['root_count']}`",
        f"- mechanism_card_path: `{manifest['mechanism_card_path']}`",
        "",
        "| Root | Role | Program | Strategy | Attempts | Target cells | Caveat |",
        "| --- | --- | --- | --- | ---: | --- | --- |",
    ]
    for row in manifest["roots"]:
        lines.append(
            "| `{root_id}` | {role} | `{program_id}` | `{strategy_id}` | {attempts} | `{cells}` | {caveat} |".format(
                root_id=row["root_id"],
                role=row["role"],
                program_id=row["program_id"],
                strategy_id=row["strategy_id"],
                attempts=row["attempts"],
                cells=",".join(row["target_cell_schedule"]),
                caveat=row["caveat"],
            )
        )
    write_text(path, "\n".join(lines) + "\n")


def _write_command_csv(path: Path, commands: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["root_id", "program_id", "strategy_id", "out_dir"])
        writer.writeheader()
        for command in commands:
            writer.writerow({key: command.get(key, "") for key in writer.fieldnames or []})


def _shell_join(parts: list[str]) -> str:
    return " ".join("'" + str(part).replace("'", "'\"'\"'") + "'" for part in parts)


__all__ = [
    "DEFAULT_PARENT_ZOO_MECHANISM_CARDS",
    "DEFAULT_PARENT_ZOO_ROOT_IDS",
    "DEFAULT_ROOT_SPECS",
    "PARENT_ZOO_SCHEMA_VERSION",
    "ParentZooRootSpec",
    "build_parent_zoo_commands",
    "default_parent_zoo_mechanism_cards",
    "default_parent_zoo_roots",
    "write_parent_zoo_command_artifacts",
    "write_parent_zoo_plan",
]
