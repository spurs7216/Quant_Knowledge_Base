"""
Prepare an artifact-local scored Phase 2 run folder.

Example:
    python research/research_falsification/prepare_phase2_scored_run.py \
        --run-id 20260424_task003_example
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def write_run_instructions(path: Path) -> None:
    text = """# Phase 2 Scored Run Instructions

Use this folder as the answering agent's working directory for the scored pass.

Rules:

- edit only `responses.csv` and optional files under `memos/`
- do not edit reusable project templates
- do not read any answer key or scoring file
- do not write score outputs here by hand

After the answering agent finishes:

1. complete `operator_handoff_record.md`
2. complete `independence_attestation.md`
3. run the scoring script locally
4. review the scored outputs locally
"""
    path.write_text(text, encoding="utf-8")


def write_operator_handoff_record(path: Path, run_id: str) -> None:
    text = f"""# Phase 2 Operator Handoff Record

## Run Identity

- run_id: `{run_id}`
- packet_file:
- responses_file:

## Operator Record

- local operator:
- answering agent session label:
- handoff timestamp:
- response received timestamp:

## Exact Prompt Used

Paste the exact prompt sent to the answering agent here.

## Allowed Files

- packet.md
- responses.csv
- files cited by packet.md
- optional memo writes under `memos/`

## Forbidden Files

- any `*answer_key*` file
- any scoring script
- any score report
- any local review note
- reusable project templates under `projects/`

## Deviations

- deviations from packet-only evidence access:
- notes:
"""
    path.write_text(text, encoding="utf-8")


def write_handoff_prompt(path: Path, run_dir: Path) -> None:
    run_dir_text = run_dir.as_posix()
    text = f"""Work only inside:
{run_dir_text}/

Read only:
- packet.md
- the evidence files cited by packet.md
- handoff_prompt.txt

Write only:
- responses.csv
- optional markdown memos under memos/

Do not open any answer key, scoring script, scored scorecard, score report, or phase-review note.
Do not edit anything under projects/.
Do not change task ids or task names.
Fill every row in responses.csv with:
- one of reject / revise / proceed
- a non-empty decision_summary
- a non-empty evidence_path
Leave memo_path blank unless you actually create a memo.
"""
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", required=True)
    parser.add_argument(
        "--output-root",
        type=Path,
        default=Path("artifacts/phase2_scored_falsification"),
    )
    parser.add_argument(
        "--packet",
        type=Path,
        default=Path("projects/quant_research_system/phase2_research_falsification/task_002_agent_packet.md"),
    )
    parser.add_argument(
        "--response-template",
        type=Path,
        default=Path("projects/quant_research_system/phase2_research_falsification/task_002_response_template.csv"),
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("projects/quant_research_system/phase2_research_falsification/task_002_manifest.yaml"),
    )
    parser.add_argument(
        "--attestation-template",
        type=Path,
        default=Path("projects/quant_research_system/phase2_research_falsification/independence_attestation_template.md"),
    )
    args = parser.parse_args()

    run_dir = args.output_root / args.run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    copy_file(args.packet, run_dir / "packet.md")
    copy_file(args.response_template, run_dir / "responses.csv")
    copy_file(args.manifest, run_dir / "task_manifest.yaml")
    copy_file(args.attestation_template, run_dir / "independence_attestation.md")
    (run_dir / "memos").mkdir(exist_ok=True)
    write_operator_handoff_record(run_dir / "operator_handoff_record.md", args.run_id)
    write_handoff_prompt(run_dir / "handoff_prompt.txt", run_dir)
    write_run_instructions(run_dir / "run_instructions.md")
    print(f"Prepared scored Phase 2 run folder at {run_dir}")


if __name__ == "__main__":
    main()
