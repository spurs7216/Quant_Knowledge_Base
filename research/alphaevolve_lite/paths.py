"""Path and hashing helpers for AlphaEvolve-lite artifacts."""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path


def utc_now_iso() -> str:
    """Return an ISO-8601 UTC timestamp."""

    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def ensure_dir(path: Path) -> Path:
    """Create a directory if needed and return it."""

    path.mkdir(parents=True, exist_ok=True)
    return path


def sha256_file(path: Path) -> str:
    """Hash a file with SHA-256."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_text(path: Path, text: str) -> Path:
    """Write UTF-8 text, creating the parent directory."""

    ensure_dir(path.parent)
    path.write_text(text, encoding="utf-8")
    return path


def write_json_text(path: Path, text: str) -> Path:
    """Write JSON text with UTF-8 encoding."""

    return write_text(path, text)
