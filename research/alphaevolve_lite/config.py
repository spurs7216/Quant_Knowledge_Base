"""YAML config loading for the Phase 4 AlphaEvolve-lite controller."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .stage_names import ALLOWED_STAGE_NAMES, validate_stage_name


class ConfigError(ValueError):
    """Raised when a controller config is missing or invalid."""


@dataclass(frozen=True)
class AlphaEvolveConfig:
    """Parsed controller configuration."""

    path: Path
    raw: dict[str, Any]

    @property
    def artifact_root(self) -> Path:
        policy = self.raw.get("artifact_policy", {})
        if isinstance(policy, dict) and policy.get("root"):
            return Path(policy["root"])
        paths = self.raw.get("paths", {})
        if isinstance(paths, dict) and paths.get("project_artifact_root"):
            return Path(paths["project_artifact_root"])
        return Path("artifacts/phase4_alphaevolve")

    @property
    def sqlite_db_name(self) -> str:
        storage = self.raw.get("storage", {})
        if isinstance(storage, dict) and storage.get("sqlite_db_name"):
            return str(storage["sqlite_db_name"])
        paths = self.raw.get("paths", {})
        if isinstance(paths, dict) and paths.get("program_database_path"):
            return Path(paths["program_database_path"]).name
        return "program_database.sqlite"

    @property
    def audit_log_name(self) -> str:
        storage = self.raw.get("storage", {})
        if isinstance(storage, dict) and storage.get("audit_log_name"):
            return str(storage["audit_log_name"])
        paths = self.raw.get("paths", {})
        if isinstance(paths, dict) and paths.get("audit_log_path"):
            return Path(paths["audit_log_path"]).name
        return "audit_log.jsonl"

    @property
    def allowed_stages(self) -> set[str]:
        stage_config = self.raw.get("stage_names", {})
        if isinstance(stage_config, dict):
            allowed = stage_config.get("allowed") or stage_config.get("active")
            if isinstance(allowed, list):
                return {str(stage) for stage in allowed}
        return set(ALLOWED_STAGE_NAMES)

    def validate_stage(self, stage: str) -> str:
        """Validate a stage against canonical and config-level stage policy."""

        canonical = validate_stage_name(stage)
        if canonical not in self.allowed_stages:
            allowed = ", ".join(sorted(self.allowed_stages))
            raise ConfigError(f"stage {canonical!r} is not allowed by config; allowed: {allowed}")
        return canonical


def load_config(path: str | Path) -> AlphaEvolveConfig:
    """Load and minimally validate a YAML config."""

    config_path = Path(path)
    if not config_path.exists():
        raise ConfigError(f"config file does not exist: {config_path}")

    try:
        import yaml
    except Exception as exc:  # pragma: no cover - environment dependent
        raise ConfigError("PyYAML is required to parse Phase 4 YAML configs") from exc

    with config_path.open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle)
    if not isinstance(raw, dict):
        raise ConfigError(f"config must parse to a mapping: {config_path}")
    return AlphaEvolveConfig(path=config_path, raw=raw)
