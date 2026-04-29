"""Controller entry points for the Phase 4 preparation milestone."""

from __future__ import annotations

import subprocess
import uuid
from pathlib import Path
from typing import Any

from .artifact_renderers import (
    render_controller_static_report,
    render_evaluator_summary,
    render_failure_report,
    render_prompt_card,
)
from .audit_log import append_audit_event
from .config import AlphaEvolveConfig, load_config
from .paths import ensure_dir, sha256_file, utc_now_iso
from .program_database import (
    finish_controller_run,
    init_db,
    insert_artifact_record,
    insert_controller_run,
)
from .stage_names import CONTROLLER_STATIC


class ControllerError(RuntimeError):
    """Raised when controller execution fails."""


def make_run_id(stage: str) -> str:
    """Create a compact run id."""

    timestamp = utc_now_iso().replace(":", "").replace("-", "")
    return f"{stage}-{timestamp}-{uuid.uuid4().hex[:8]}"


def get_git_commit() -> str | None:
    """Return current git commit if available."""

    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
    except Exception:
        return None
    return result.stdout.strip() or None


def _record_artifact(
    db_path: Path,
    *,
    run_id: str,
    artifact_type: str,
    path: Path,
    program_id: str | None = None,
) -> None:
    insert_artifact_record(
        db_path,
        {
            "artifact_id": f"ART-{uuid.uuid4().hex[:16]}",
            "run_id": run_id,
            "program_id": program_id,
            "artifact_type": artifact_type,
            "path": str(path),
            "sha256": sha256_file(path),
        },
    )


def run_controller_static(
    config: AlphaEvolveConfig,
    *,
    run_id: str | None = None,
) -> dict[str, Any]:
    """Run the controller_static preparation smoke stage.

    This stage does not call LLM endpoints and does not load CSV data.
    """

    stage = CONTROLLER_STATIC
    config.validate_stage(stage)
    actual_run_id = run_id or make_run_id(stage)
    artifact_root = ensure_dir(config.artifact_root)
    run_dir = ensure_dir(artifact_root / "runs" / actual_run_id)
    db_path = artifact_root / config.sqlite_db_name
    audit_path = artifact_root / config.audit_log_name

    started_at = utc_now_iso()
    append_audit_event(
        audit_path,
        "controller_started",
        actual_run_id,
        {"stage": stage, "config_path": str(config.path)},
    )

    checks: dict[str, bool] = {
        "config_file_exists": config.path.exists(),
        "config_parsed": True,
        "artifact_root_created": artifact_root.exists(),
        "no_llm_endpoint_called": True,
        "no_heavy_csv_loaded": True,
    }

    try:
        append_audit_event(
            audit_path,
            "config_loaded",
            actual_run_id,
            {"allowed_stages": sorted(config.allowed_stages)},
        )
        init_db(db_path)
        checks["database_initialized"] = True
        insert_controller_run(
            db_path,
            {
                "run_id": actual_run_id,
                "stage": stage,
                "config_path": str(config.path),
                "artifact_root": str(artifact_root),
                "git_commit": get_git_commit(),
                "status": "started",
                "started_at": started_at,
            },
        )
        append_audit_event(
            audit_path,
            "database_initialized",
            actual_run_id,
            {"db_path": str(db_path)},
        )

        prompt_paths = render_prompt_card(
            run_dir,
            program_id="EXAMPLE-PROGRAM",
            parent_id=None,
            generation=0,
            island="controller_static",
            mutation_surface="none",
            data_scope="daily_stock_only",
            allowed_surfaces=["signal", "ranking", "portfolio", "risk"],
            forbidden_changes=[
                "split_policy",
                "universe_policy",
                "cost_policy",
                "broker_logic",
                "non_daily_stock_dataset_features",
            ],
            evaluator_feedback_summary="Example controller_static prompt card; no data evaluation has run.",
            inspiration_programs=[],
            strict_output_contract="SEARCH/REPLACE only for child generation; not used in this smoke run.",
        )
        summary_paths = render_evaluator_summary(
            run_dir,
            program_id="EXAMPLE-PROGRAM",
            stage=stage,
            hard_gates={
                "config_parsed": True,
                "database_initialized": True,
                "audit_log_appended": True,
                "no_llm_endpoint_called": True,
                "no_heavy_csv_loaded": True,
            },
            metrics={},
            descriptors={"data_scope": "daily_stock_only", "stage": stage},
            decision="record_only",
            failure_reason=None,
            next_prompt_hint="Controller infrastructure is ready for remote schema/model evidence checks.",
            artifact_paths={},
        )
        failure_path = render_failure_report(
            run_dir,
            failure_category="none",
            exact_gate="none",
            minimal_reproduction="controller_static smoke run completed",
            repair_allowed=False,
            next_prompt_hint="No repair needed.",
            usable_as_inspiration=False,
        )
        checks["prompt_card_written"] = all(path.exists() for path in prompt_paths.values())
        checks["evaluator_summary_written"] = all(path.exists() for path in summary_paths.values())
        checks["failure_report_written"] = failure_path.exists()

        report_path = render_controller_static_report(
            run_dir,
            run_id=actual_run_id,
            config_path=str(config.path),
            db_path=str(db_path),
            audit_log_path=str(audit_path),
            checks=checks,
        )

        artifact_map = {
            "prompt_card_json": prompt_paths["json"],
            "prompt_card_markdown": prompt_paths["markdown"],
            "evaluator_summary_json": summary_paths["json"],
            "evaluator_summary_markdown": summary_paths["markdown"],
            "failure_report": failure_path,
            "controller_static_report": report_path,
        }
        for artifact_type, path in artifact_map.items():
            _record_artifact(db_path, run_id=actual_run_id, artifact_type=artifact_type, path=path)
            append_audit_event(
                audit_path,
                "artifact_written",
                actual_run_id,
                {"artifact_type": artifact_type, "path": str(path)},
            )

        finish_controller_run(db_path, actual_run_id, "finished")
        append_audit_event(
            audit_path,
            "controller_finished",
            actual_run_id,
            {"stage": stage, "status": "finished"},
        )
        return {
            "run_id": actual_run_id,
            "stage": stage,
            "run_dir": str(run_dir),
            "db_path": str(db_path),
            "audit_log_path": str(audit_path),
            "checks": checks,
        }
    except Exception as exc:
        try:
            finish_controller_run(db_path, actual_run_id, "error", str(exc))
        except Exception:
            pass
        try:
            append_audit_event(
                audit_path,
                "error",
                actual_run_id,
                {"stage": stage, "error": str(exc)},
            )
        except Exception:
            pass
        raise


def run_controller(config_path: str | Path, stage: str, run_id: str | None = None) -> dict[str, Any]:
    """Run a supported controller stage."""

    config = load_config(config_path)
    canonical_stage = config.validate_stage(stage)
    if canonical_stage != CONTROLLER_STATIC:
        raise ControllerError(f"stage {canonical_stage!r} is recognized but not implemented yet")
    return run_controller_static(config, run_id=run_id)
