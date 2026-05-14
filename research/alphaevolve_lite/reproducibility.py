"""Reproducibility artifacts for remote controller and evaluator runs."""

from __future__ import annotations

import hashlib
import shutil
import subprocess
from pathlib import Path
from typing import Any


UNKNOWN_GIT_VALUE = "unknown"


def git_value(args: list[str]) -> str:
    """Return a git command value, or ``unknown`` when git is unavailable."""

    try:
        out = subprocess.check_output(["git", *args], stderr=subprocess.DEVNULL)
    except Exception:
        return UNKNOWN_GIT_VALUE
    return out.decode("utf-8", errors="replace").strip()


def capture_git_reproducibility(out_dir: Path) -> dict[str, Any]:
    """Write git hygiene artifacts and return prompt/evaluator metadata.

    Remote runs should be reproducible from a GitHub-fetchable commit. We do
    not fetch here because evaluators should not hide operator state changes;
    instead we record the local view of ``origin/main`` and whether ``HEAD``
    exactly matches it.
    """

    out_dir.mkdir(parents=True, exist_ok=True)
    status = git_value(["status", "--short"])
    diff_stat = git_value(["diff", "--stat"])
    branch = git_value(["rev-parse", "--abbrev-ref", "HEAD"]) or UNKNOWN_GIT_VALUE
    head_commit = git_value(["rev-parse", "HEAD"]) or UNKNOWN_GIT_VALUE
    origin_main_commit = git_value(["rev-parse", "origin/main"]) or UNKNOWN_GIT_VALUE
    head_matches_origin_main = (
        head_commit != UNKNOWN_GIT_VALUE
        and origin_main_commit != UNKNOWN_GIT_VALUE
        and head_commit == origin_main_commit
    )

    status_path = out_dir / "git_status.txt"
    diff_stat_path = out_dir / "git_diff_stat.txt"
    status_path.write_text(status + ("\n" if status else ""), encoding="utf-8")
    diff_stat_path.write_text(diff_stat + ("\n" if diff_stat else ""), encoding="utf-8")

    return {
        "git_commit": head_commit,
        "git_branch": branch,
        "git_dirty": bool(status and status != UNKNOWN_GIT_VALUE),
        "git_origin_main_commit": origin_main_commit,
        "git_head_matches_origin_main": head_matches_origin_main,
        "manifest_commit_fetchable_from_github": head_matches_origin_main,
        "git_status_path": status_path.name,
        "git_diff_stat_path": diff_stat_path.name,
    }


def file_sha256(path: Path) -> str:
    """Return the SHA-256 digest for a file."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def capture_program_snapshot(
    program_path: Path,
    out_dir: Path,
    *,
    snapshot_name: str = "program_snapshot.py",
) -> dict[str, Any]:
    """Copy an evaluated program into the artifact and record its hash."""

    out_dir.mkdir(parents=True, exist_ok=True)
    resolved = program_path.resolve()
    snapshot_path = out_dir / snapshot_name
    if resolved != snapshot_path.resolve():
        shutil.copyfile(resolved, snapshot_path)
    digest = file_sha256(snapshot_path)
    return {
        "program_snapshot_path": snapshot_path.name,
        "program_sha256": digest,
        "program_snapshot_bytes": snapshot_path.stat().st_size,
    }


__all__ = [
    "capture_git_reproducibility",
    "capture_program_snapshot",
    "file_sha256",
    "git_value",
]
