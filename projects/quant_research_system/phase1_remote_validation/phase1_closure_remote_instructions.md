---
title: Phase 1 Closure Remote Instructions
type: project
status: active
updated: 2026-04-23
tags:
  - project
  - phase1
  - remote-validation
  - closure-run
  - ubuntu
---
# Phase 1 Closure Remote Instructions

## Purpose

These instructions are for the remote Ubuntu agent that will rerun Task 001 to determine whether Phase 1 can be closed.

The goal is not to improve the strategy. The goal is to produce a clean, reproducible remote-validation run whose artifacts can be trusted as evidence that the `remote_validation` pipeline works.

## Hard Rules

- Do not push raw warehouse data to GitHub.
- Do not commit `artifacts/remote_runs/` outputs; `artifacts/**` is intentionally ignored.
- Do not use or store any personal access token inside the repo.
- Do not run the final closure validation from a dirty Git tree.
- Do not patch code and then run before committing the patch.
- If code changes are required, commit them first, push if needed, pull the clean commit, and only then rerun.
- Prefer a fresh clone over trying to clean a previously dirty working tree.

## Required Data Path

The full daily stock file must exist here:

```bash
/home/b08303004/Desktop/WRDS/data/daily_stock/gago9dveytpx6922.csv
```

The runner should be invoked with:

```bash
--data-root /home/b08303004/Desktop/WRDS/data
```

## Closure Criteria

The run can be used to close Phase 1 only if all conditions hold:

- `git status --short` is empty immediately before the run.
- `run_manifest.yaml` records a real Git commit, not `unknown`.
- `run_manifest.yaml` records `dirty: false` for both `vault_snapshot` and `research_code_snapshot`.
- The remote run completes against the full warehouse file.
- The artifact bundle contains all required files.
- `metrics.json` status is `completed` or `completed_with_warnings`, not `failed_gates`.
- `diagnostics.csv` has no `status == fail` rows.
- A tracked closure decision note is committed and pushed to GitHub.
- The compact artifact bundle is packaged outside Git and made available for local import.

Warnings do not automatically block Phase 1 closure if they are explicitly recorded and the decision note explains why they are acceptable for a workflow-foundation phase.

## Recommended Fresh Clone

Use a fresh clone so the previous dirty remote run cannot contaminate this closure run.

```bash
set -euo pipefail

export REPO_URL="https://github.com/spurs7216/Quant_Knowledge_Base.git"
export RUN_ID="20260423_task001_daily_stock_short_reversal_closure_clean"
export WORK_PARENT="$HOME/Desktop/phase1_closure_runs"
export REPO_ROOT="$WORK_PARENT/quant_resource_$RUN_ID"
export DATA_ROOT="/home/b08303004/Desktop/WRDS/data"
export DATA_PATH="$DATA_ROOT/daily_stock/gago9dveytpx6922.csv"
export OUT_DIR="artifacts/remote_runs/$RUN_ID"
export RETURN_DIR="$HOME/Desktop/phase1_closure_returns"

mkdir -p "$WORK_PARENT" "$RETURN_DIR"
cd "$WORK_PARENT"
git clone "$REPO_URL" "quant_resource_$RUN_ID"
cd "$REPO_ROOT"
git checkout main
git pull --ff-only origin main
```

If clone authentication is required, use the remote machine's existing Git credential flow or GitHub CLI. Do not write a token into the repo, scripts, notes, shell history helpers, or config files that will be committed.

## Preflight Checks

Run these from `$REPO_ROOT`.

```bash
git status --short
git rev-parse --short HEAD
git remote -v
test -f "$DATA_PATH"
ls -lh "$DATA_PATH"
```

The output of `git status --short` must be empty. If it is not empty, stop and report the dirty paths. Do not continue to the closure run.

Check that the data has the expected header fields:

```bash
python3 - <<'PY'
import csv
from pathlib import Path

path = Path("/home/b08303004/Desktop/WRDS/data/daily_stock/gago9dveytpx6922.csv")
required = {
    "PERMNO",
    "DlyCalDt",
    "DlyRet",
    "DlyRetx",
    "DlyPrc",
    "DlyVol",
    "PrimaryExch",
    "SecurityType",
    "ShareType",
    "TradingStatusFlg",
    "vwretd",
    "sprtrn",
}
with path.open("r", newline="", encoding="utf-8", errors="replace") as f:
    header = next(csv.reader(f))
missing = sorted(required.difference(header))
print("column_count", len(header))
print("missing_required_columns", missing)
if missing:
    raise SystemExit(1)
PY
```

## Python Environment

Task 001 does not require GPU.

Preferred local virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r research/remote_validation/requirements.txt
python -m py_compile research/remote_validation/task001_daily_stock_short_reversal.py
```

Conda or micromamba is acceptable if the remote machine already standardizes on it, but record the Python version in the closure note.

## Final Clean-Tree Check

Immediately before running the validation:

```bash
git status --short
test -z "$(git status --short)"
export CLEAN_COMMIT="$(git rev-parse HEAD)"
export CLEAN_COMMIT_SHORT="$(git rev-parse --short HEAD)"
echo "clean_commit=$CLEAN_COMMIT"
```

If the `test -z` command fails, stop. Do not run the closure validation from a dirty tree.

## Run Task 001

Run from `$REPO_ROOT`:

```bash
python research/remote_validation/task001_daily_stock_short_reversal.py \
  --data-root "$DATA_ROOT" \
  --output-dir "$OUT_DIR"
```

Expected runtime depends on remote IO speed. Do not kill the job unless it is clearly stuck or exhausting memory.

## Required Artifact Files

After the run, this directory must exist:

```bash
$REPO_ROOT/artifacts/remote_runs/20260423_task001_daily_stock_short_reversal_closure_clean/
```

Required files:

- `run_manifest.yaml`
- `metrics.json`
- `scorecard.csv`
- `diagnostics.csv`
- `failure_report.md`
- `review.md`
- `subperiod_metrics.csv`
- `cost_sensitivity.csv`
- `exchange_split_metrics.csv`
- `liquidity_bucket_metrics.csv`
- `universe_counts_by_month.csv`
- `returns_train.csv`
- `returns_validation.csv`
- `returns_test.csv`

Check them:

```bash
for f in \
  run_manifest.yaml \
  metrics.json \
  scorecard.csv \
  diagnostics.csv \
  failure_report.md \
  review.md \
  subperiod_metrics.csv \
  cost_sensitivity.csv \
  exchange_split_metrics.csv \
  liquidity_bucket_metrics.csv \
  universe_counts_by_month.csv \
  returns_train.csv \
  returns_validation.csv \
  returns_test.csv
do
  test -s "$OUT_DIR/$f"
done
```

## Validate The Manifest And Gates

The file is named `run_manifest.yaml`, but the current runner writes JSON content. Validate it with Python JSON parsing.

```bash
python - <<'PY'
import csv
import json
from pathlib import Path

out = Path("artifacts/remote_runs/20260423_task001_daily_stock_short_reversal_closure_clean")

manifest = json.loads((out / "run_manifest.yaml").read_text())
metrics = json.loads((out / "metrics.json").read_text())

for key in ("vault_snapshot", "research_code_snapshot"):
    snap = manifest[key]
    print(key, snap)
    if snap.get("commit") in ("", "unknown", None):
        raise SystemExit(f"{key} commit is not recorded")
    if snap.get("dirty") is not False:
        raise SystemExit(f"{key} dirty flag is not false")

if metrics.get("status") == "failed_gates":
    raise SystemExit("metrics status is failed_gates")

failed = []
with (out / "diagnostics.csv").open(newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        if row.get("status") == "fail":
            failed.append(row)

print("metrics_status", metrics.get("status"))
print("failed_diagnostics_count", len(failed))
if failed:
    for row in failed[:20]:
        print(row)
    raise SystemExit("diagnostics contain failed rows")

print("validation_checks_passed")
PY
```

If this validation fails, package the failed artifact bundle anyway, but mark the closure decision as `not_closed` and explain why.

## Package The Artifact Bundle Outside Git

Artifacts are ignored by Git. This is intentional.

Create a portable archive outside the repo:

```bash
cd "$REPO_ROOT"
tar -czf "$RETURN_DIR/${RUN_ID}_${CLEAN_COMMIT_SHORT}_artifacts.tar.gz" "$OUT_DIR"
sha256sum "$RETURN_DIR/${RUN_ID}_${CLEAN_COMMIT_SHORT}_artifacts.tar.gz" \
  > "$RETURN_DIR/${RUN_ID}_${CLEAN_COMMIT_SHORT}_artifacts.tar.gz.sha256"
ls -lh "$RETURN_DIR"
cat "$RETURN_DIR/${RUN_ID}_${CLEAN_COMMIT_SHORT}_artifacts.tar.gz.sha256"
```

Do not commit the archive. Transfer it to the local machine by the available non-Git channel, for example `scp`, shared drive, or manual file download.

## Create The Tracked Closure Decision Note

Create:

```text
projects/quant_research_system/phase1_remote_validation/task_001_closure_decision.md
```

Use this structure and fill it with exact values from the artifact files:

```markdown
---
title: Task 001 Phase 1 Closure Decision
type: project
status: completed
updated: 2026-04-23
tags:
  - project
  - phase1
  - remote-validation
  - closure-run
sources:
  - "../../../artifacts/remote_runs/20260423_task001_daily_stock_short_reversal_closure_clean/run_manifest.yaml"
  - "../../../artifacts/remote_runs/20260423_task001_daily_stock_short_reversal_closure_clean/metrics.json"
  - "../../../artifacts/remote_runs/20260423_task001_daily_stock_short_reversal_closure_clean/diagnostics.csv"
  - "../../../artifacts/remote_runs/20260423_task001_daily_stock_short_reversal_closure_clean/failure_report.md"
---
# Task 001 Phase 1 Closure Decision

## Run Identity

- job_id: `20260423_task001_daily_stock_short_reversal`
- closure_run_id: `20260423_task001_daily_stock_short_reversal_closure_clean`
- remote repo path: `<fill>`
- data file: `/home/b08303004/Desktop/WRDS/data/daily_stock/gago9dveytpx6922.csv`
- git commit: `<full commit from run_manifest.yaml>`
- git dirty flag: `false`
- Python version: `<fill from run_manifest.yaml>`
- artifact archive: `<archive file name>`
- artifact archive sha256: `<sha256>`

## Artifact Completeness

- Required files present: `<yes/no>`
- `metrics.json` status: `<completed/completed_with_warnings/failed_gates>`
- failed diagnostics count: `<integer>`
- warning diagnostics count: `<integer>`
- raw warehouse data copied into repo: `no`

## Closure Assessment

Decision: `<phase1_closed / not_closed>`

Explain whether Phase 1 can close. The answer should be based on workflow trust, not whether the baseline is a good alpha.

## Strategy Result

Record train, validation, and test headline metrics:

| Split | Annualized return | Annualized vol | Sharpe | Max drawdown | Mean turnover | Beta to `vwretd` |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| train | `<fill>` | `<fill>` | `<fill>` | `<fill>` | `<fill>` | `<fill>` |
| validation | `<fill>` | `<fill>` | `<fill>` | `<fill>` | `<fill>` | `<fill>` |
| test | `<fill>` | `<fill>` | `<fill>` | `<fill>` | `<fill>` | `<fill>` |

## Remaining Research Follow-Up

List follow-up items that belong to Phase 2 or later. These should not block Phase 1 unless they undermine the workflow evidence.
```

The closure note must distinguish two questions:

- Can Phase 1 close as an engineering and evidence-pipeline milestone?
- Is the short-horizon reversal baseline promotable as alpha?

The likely acceptable outcome is: Phase 1 closes, but the strategy remains `revise` or `not_promoted`.

## Commit And Push Only Tracked Notes

Before committing, verify that artifacts are ignored and not staged:

```bash
git status --short --ignored artifacts
git status --short
```

Expected:

- `artifacts/remote_runs/...` appears as ignored with `!!`.
- Only the closure decision note, or other intentionally edited project notes, appear as tracked changes.

Commit only tracked project notes:

```bash
git add projects/quant_research_system/phase1_remote_validation/task_001_closure_decision.md
git commit -m "Record phase1 clean closure validation"
git push origin main
```

If you edited any code, do not include it in this closure commit unless the code change was intentional, reviewed, and the final run was executed after that code change was committed and the tree was clean.

## Final Message Back To Local Agent

Report these exact items:

- pushed commit hash
- clean run commit hash recorded in `run_manifest.yaml`
- artifact archive path on the remote machine
- artifact archive sha256
- `metrics.json` status
- failed diagnostics count
- warning diagnostics count
- Phase 1 closure decision
- whether the strategy itself remains `revise`, `reject`, or `promotable`

Do not paste secrets or credentials in the final message.
