"""Shared JSON artifact I/O for AlphaEvolve-lite tooling."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


def clean_json(obj: Any) -> Any:
    """Convert common analysis objects into stable JSON-safe values."""

    try:
        import numpy as np
        import pandas as pd
    except Exception:  # pragma: no cover - optional runtime dependencies
        np = None
        pd = None

    if isinstance(obj, dict):
        return {str(key): clean_json(value) for key, value in obj.items()}
    if isinstance(obj, list):
        return [clean_json(value) for value in obj]
    if isinstance(obj, tuple):
        return [clean_json(value) for value in obj]
    if pd is not None and isinstance(obj, pd.Timestamp):
        return obj.isoformat()
    if np is not None and isinstance(obj, np.generic):
        return clean_json(obj.item())
    if isinstance(obj, float):
        return obj if math.isfinite(obj) else None
    return obj


def json_artifact_text(payload: Any, *, ensure_ascii: bool = True) -> str:
    """Render a deterministic JSON artifact body."""

    return json.dumps(clean_json(payload), indent=2, sort_keys=True, ensure_ascii=ensure_ascii) + "\n"


def write_json(path: Path, payload: Any, *, ensure_ascii: bool = True) -> Path:
    """Write a stable indented JSON artifact and return its path."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json_artifact_text(payload, ensure_ascii=ensure_ascii), encoding="utf-8")
    return path


__all__ = ["clean_json", "json_artifact_text", "write_json"]
