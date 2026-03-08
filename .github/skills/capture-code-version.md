# Skill: Capture Code Version

Every run must be pinned to an exact git commit so results are reproducible from source.

## Commands (run on Gilbreth in the pipeline repo)

```bash
cd /home/<username>/Code/FRESCO-Pipeline

git rev-parse HEAD              > validation/git_commit.txt
git status --short              > validation/git_status.txt
git diff                        > validation/git_diff.patch   # save if non-empty
```

## Rules

1. **Prefer a clean working tree** — commit or stash all changes before submitting a production job.
2. **If uncommitted diffs exist**, save `git diff` as `validation/git_diff.patch` and note it in `manifests/run_metadata.json`.
3. **Never label a run "publication-ready"** if `git_status.txt` is non-empty and no diff artifact exists.

## What to record in run_metadata.json

```json
{
  "pipeline_git_commit": "<full SHA from git rev-parse HEAD>",
  "pipeline_git_dirty": false
}
```

See the `write-manifests` skill for the full `run_metadata.json` schema.
