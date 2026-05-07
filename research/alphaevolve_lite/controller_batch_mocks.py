"""Deterministic mock patches for controller batch smoke tests."""

from __future__ import annotations


def mock_patch(parent_text: str, mode: str, target_surface: str = "signal") -> str:
    """Return a deterministic mock model patch for local smoke checks."""

    if mode == "no_valid_patch":
        return "NO_VALID_PATCH"
    if mode == "sign_flip":
        search = "        signal = signal / rolling_vol.clip(lower=1e-4)\n"
        if search not in parent_text:
            raise RuntimeError("mock sign_flip SEARCH text not found")
        return (
            "<<<<<<< SEARCH\n"
            f"{search}"
            "=======\n"
            "        signal = -signal / rolling_vol.clip(lower=1e-4)\n"
            ">>>>>>> REPLACE\n"
        )
    if mode == "marker_oversize":
        search = (
            "    # EVOLVE-BLOCK-START: signal\n"
            "    q = float(cfg[\"kalman_q\"])\n"
            "    r = float(cfg[\"kalman_r\"])\n"
            "    min_history = int(cfg[\"min_history\"])\n"
        )
        if search not in parent_text:
            raise RuntimeError("mock marker_oversize SEARCH text not found")
        replace = search + "    # mock oversized patch touched marker lines\n"
        return f"<<<<<<< SEARCH\n{search}=======\n{replace}>>>>>>> REPLACE\n"
    if mode == "portfolio_long_only":
        search = (
            "        weights.loc[longs] = 0.5 * gross / len(longs)\n"
            "        weights.loc[shorts] = -0.5 * gross / len(shorts)\n"
        )
        if search not in parent_text:
            raise RuntimeError("mock portfolio_long_only SEARCH text not found")
        return (
            "<<<<<<< SEARCH\n"
            f"{search}"
            "=======\n"
            "        weights.loc[longs] = 0.5 * gross * valid.loc[longs, \"signal\"] / valid.loc[longs, \"signal\"].sum()\n"
            "        weights.loc[shorts] = -0.5 * gross * valid.loc[shorts, \"signal\"] / valid.loc[shorts, \"signal\"].abs().sum()\n"
            ">>>>>>> REPLACE\n"
        )
    raise RuntimeError(f"unknown mock patch mode: {mode}")


def mock_repair_patch(parent_text: str, mode: str) -> str:
    """Return a deterministic mock repair patch for local smoke checks."""

    if mode == "marker_oversize":
        return mock_patch(parent_text, "sign_flip")
    return "NO_VALID_PATCH"


__all__ = ["mock_patch", "mock_repair_patch"]
