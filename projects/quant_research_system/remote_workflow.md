---
title: Remote Data and GPU Workflow
type: project
status: active
updated: 2026-04-23
tags:
  - project
  - remote-compute
  - data
  - gpu
  - artifacts
---
# Remote Data and GPU Workflow

## Design principle

The local machine is the control plane. The remote Linux/GPU machine is the data and compute plane.

The local vault should know what exists, what was run, and what evidence came back. It should not mirror heavy warehouse files.

This workflow is not optimized for minimal machinery. It is optimized for reproducible research across two machines. If GitHub synchronization, manifests, artifact bundles, and manual review add complexity, that complexity is justified because it makes the system more robust, reusable, and learnable.

## Local responsibilities

Local vault responsibilities:

- inspect `catalog/` to select datasets
- define task and evaluator contract
- write job manifest
- review compact artifacts
- update project decisions
- promote durable lessons only after verification

## Remote responsibilities

Remote machine responsibilities:

- load full datasets
- run heavy backtests
- train models when needed
- run GPU jobs
- produce compact artifact bundles
- preserve reproducibility metadata

## Dataset references

Use physical mirror names from `catalog/` when referring to remote files.

Examples:

- `/home/b08303004/Desktop/WRDS/data/daily_stock/gago9dveytpx6922.csv`
- catalog-relative path: `data/daily_stock/gago9dveytpx6922.csv`
- `data/CCM/obvhttgmrtddf1tq.csv`
- `data/option_forward_price/albvtzgilyy7iwg5.csv`
- `data/option_volumne/ypbvvpsmuiv0jgxq.csv`

Do not silently rename misspelled mirror paths such as `option_volumne` or `Treasurey_Term_structure`.

## Job manifest

Every remote job should have a manifest before execution.

Suggested fields:

```yaml
job_id:
created:
owner:
objective:
environment:
candidate_artifact:
sync_channel: github
remote_os: ubuntu
vault_snapshot:
  repo:
  branch:
  commit:
  dirty:
research_code_snapshot:
  repo:
  branch:
  commit:
  dirty:
datasets:
  - logical_name:
    remote_path:
    catalog_sample:
    required_columns:
date_range:
universe:
split_plan:
cost_model:
benchmark:
random_seeds:
resource_request:
expected_outputs:
failure_gates:
artifact_import_policy: manual_review
notes:
```

## Artifact bundle

Every remote run should return a compact artifact bundle.

Minimum contents:

- `run_manifest.yaml`
- `metrics.json`
- `scorecard.csv`
- `diagnostics.csv`
- `failure_report.md`
- plots if useful
- logs trimmed to useful warnings and errors

Optional contents:

- sampled predictions
- factor coverage table
- turnover table
- regime-split metrics
- residual diagnostics
- feature-importance summary

## Artifact storage

Recommended local path pattern:

```text
artifacts/remote_runs/<YYYYMMDD>_<short_job_id>/
```

Large raw outputs should remain remote. The local artifact folder should contain only bounded evidence.

## Catalog refresh

Refresh `catalog/` when:

- new remote datasets are added
- dataset shape changes
- processed research outputs become reusable
- EDA summaries are regenerated

Do not refresh the catalog for every scratch run. Use `artifacts/` for bounded run outputs.

## Data integrity checks

Remote validation jobs should usually check:

- row counts after filters
- date coverage
- identifier coverage
- duplicate key rate
- missing key fields
- timestamp alignment
- survivorship-risk flags
- join path and join loss

## Synchronization modes

### Metadata sync

Use for:

- inventory
- EDA summaries
- run manifests
- scorecards

This is the default mode.

### Artifact sync

Use for:

- figures
- compact CSVs
- diagnostic tables
- result summaries

This is allowed when the files are small enough to inspect locally.

### Data sync

Use rarely.

Only copy data locally when:

- a small sample is needed for debugging
- the file is explicitly a catalog sample
- the user approves the transfer

## Remote job lifecycle

1. create project task
2. inspect `catalog/`
3. write job manifest
4. run local static checks on the manifest
5. submit to remote runner
6. monitor status
7. sync artifact bundle
8. inspect artifacts locally
9. record decision in `projects/`
10. crystallize stable lessons into `wiki/` only if reusable

## Security rules

- do not store SSH keys, passwords, tokens, or broker credentials in the vault
- redact paths or hostnames if they reveal sensitive infrastructure
- avoid copying proprietary raw data into tracked files
- artifacts should be compact and reviewable

## Remote synchronization choices

### Resolved choices

- Remote synchronization method: GitHub.
- Remote operating system: Ubuntu.
- Result import policy: manually reviewed before being pulled into `artifacts/` for now.

### GitHub workflow

Use GitHub as the synchronization and code-version channel, not as the heavy-data channel.

Recommended flow:

1. local vault defines the task, manifest, and candidate code changes
2. relevant code or manifest changes are committed to a GitHub branch
3. remote Ubuntu machine pulls the exact commit
4. remote machine runs the job against local warehouse data
5. remote machine writes a compact artifact bundle
6. artifact bundle is manually reviewed
7. approved compact artifacts are copied or pulled into local `artifacts/`
8. project notes record the decision and link the artifact bundle

Do not push raw warehouse data to GitHub. Do not push broker credentials or secrets to GitHub. Generated artifacts should remain outside tracked git unless a specific small metadata file is intentionally approved for tracking.

### Code snapshot meaning

Code snapshot pinning means recording the exact version of the code used for a run. In practice this should usually be:

- local vault git commit
- remote research repo git commit
- branch name if useful
- dirty-worktree flag if there were uncommitted changes

This matters because a metric without the exact code version is not reproducible evidence.

### Remote environment policy

Knowing the machine is Ubuntu answers the OS question, but not the environment-reproducibility question.

Recommended default for Phase 1:

- use a pinned environment file in the remote research repo
- prefer conda / micromamba for GPU-heavy Python stacks because CUDA, PyTorch, and numerical libraries are often easier to reproduce that way
- use `uv` or pinned `requirements.txt` for pure-Python research utilities inside that environment if useful
- add Docker later if environment drift, deployment, or cross-machine reproducibility becomes a real blocker

Rejected default:

- do not rely on unpinned system Python for serious benchmark or research runs

Remaining concrete choice:

- choose the exact remote environment file format once the remote research repo layout is known, likely `environment.yml` plus a lock file or `requirements.txt` for app-level packages
