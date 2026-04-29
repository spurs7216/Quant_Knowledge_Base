"""Record remote Qwen/vLLM model-test logs as formal artifacts."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import uuid
from pathlib import Path
from statistics import mean, median
from typing import Any


def _ensure_repo_import() -> None:
    repo_root = Path(__file__).resolve().parents[3]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Record a remote model-test log as artifacts and SQLite metadata.")
    parser.add_argument("--model-role", required=True)
    parser.add_argument("--model-id", required=True)
    parser.add_argument("--served-model-name", required=True)
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--log-path", required=True)
    parser.add_argument("--db-path", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--max-model-len", type=int)
    parser.add_argument("--decision", default="pending_review")
    parser.add_argument("--command-summary", default="")
    return parser.parse_args()


def _count_bool_pattern(text: str, names: list[str]) -> int | None:
    total = 0
    found = False
    for name in names:
        pattern = re.compile(rf"{re.escape(name)}\s*[:=]\s*(true|pass|passed|1)", re.IGNORECASE)
        matches = pattern.findall(text)
        if matches:
            found = True
            total += len(matches)
    return total if found else None


def parse_log(text: str) -> dict[str, Any]:
    """Best-effort parser; unknown fields remain null."""

    latencies = [float(match) for match in re.findall(r"latency[^0-9]*(\d+(?:\.\d+)?)", text, re.IGNORECASE)]
    return {
        "health_pass": bool(re.search(r"\bhealth\b.*\b(pass|ok|200)\b", text, re.IGNORECASE)) or None,
        "model_list_pass": bool(re.search(r"\bmodels?\b.*\b(pass|ok|200)\b", text, re.IGNORECASE)) or None,
        "latency": {
            "mean_sec": mean(latencies) if latencies else None,
            "median_sec": median(latencies) if latencies else None,
            "min_sec": min(latencies) if latencies else None,
            "max_sec": max(latencies) if latencies else None,
        },
        "parse_pass_count": _count_bool_pattern(text, ["parse_pass", "strict_patch_parse"]),
        "apply_pass_count": _count_bool_pattern(text, ["apply_pass", "strict_patch_apply"]),
        "compile_pass_count": _count_bool_pattern(text, ["compile_pass", "strict_patch_compile"]),
        "vector_smoke_pass_count": _count_bool_pattern(text, ["vector_smoke_pass", "pandas_smoke", "numpy_smoke"]),
        "critic_json_pass": bool(re.search(r"critic_json[^\n]*(pass|true|1)", text, re.IGNORECASE)) or None,
        "medium_context_json_pass": bool(re.search(r"medium_context_json[^\n]*(pass|true|1)", text, re.IGNORECASE)) or None,
    }


def write_artifacts(out_dir: Path, record: dict[str, Any], raw_log_source: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    copied_log = out_dir / "raw_terminal_log.txt"
    if raw_log_source.resolve() != copied_log.resolve():
        shutil.copyfile(raw_log_source, copied_log)
    record["result_log_path"] = str(copied_log)
    (out_dir / "model_test_record.json").write_text(
        json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    md = [
        f"# Model Test Record: {record['test_id']}",
        "",
        f"- model role: {record['model_role']}",
        f"- model id: {record['model_id']}",
        f"- served model name: {record['served_model_name']}",
        f"- port: {record['port']}",
        f"- decision: {record['decision']}",
        f"- raw log: {record['result_log_path']}",
        "",
        "## Parsed Metrics",
        "",
    ]
    for key, value in sorted(record["parsed_metrics"].items()):
        md.append(f"- {key}: {value}")
    md.append("")
    (out_dir / "model_test_record.md").write_text("\n".join(md), encoding="utf-8")
    return copied_log


def main() -> int:
    _ensure_repo_import()
    from research.alphaevolve_lite.program_database import init_db, insert_model_test_record

    args = parse_args()
    log_path = Path(args.log_path)
    if not log_path.exists():
        print(f"ERROR: log path does not exist: {log_path}", file=sys.stderr)
        return 1
    text = log_path.read_text(encoding="utf-8", errors="replace")
    test_id = f"MODELTEST-{uuid.uuid4().hex[:12]}"
    record = {
        "test_id": test_id,
        "model_role": args.model_role,
        "model_id": args.model_id,
        "served_model_name": args.served_model_name,
        "port": args.port,
        "max_model_len": args.max_model_len,
        "gpu_config": {},
        "command_summary": args.command_summary,
        "result_log_path": str(log_path),
        "parsed_metrics": parse_log(text),
        "decision": args.decision,
    }
    copied_log = write_artifacts(Path(args.out_dir), record, log_path)
    record["result_log_path"] = str(copied_log)
    init_db(args.db_path)
    insert_model_test_record(args.db_path, record)
    print(json.dumps({"status": "ok", "test_id": test_id, "out_dir": args.out_dir}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
