# PROD-20260203-v3 Run Log — FRESCO v3 Production Dataset Build

**Run ID**: PROD-20260203-v3  
**Date**: 2026-02-03 (submitted) / 2026-03-09 (executed) / 2026-03-11 (verified)

## Objective

Build the authoritative FRESCO v3 unified parquet dataset from raw FRESCO shards across all three clusters (anvil, conte, stampede) and write validation, manifest, and provenance artifacts required for publication.

## Inputs

- Dataset label: raw FRESCO shards
- Input root: `/depot/<group>/data/josh/FRESCO/chunks/`
- Clusters: **anvil**, **conte**, **stampede**
- Date range: 2013–2023 (full available range)
- Config: `config/production_v3.json` (local), `/home/<username>/Code/FRESCO-Pipeline/production_v3.json` (Gilbreth)

## Code & Environment

- Script: `scripts/build_production_v3.py`
- Config: `config/production_v3.json`
- Remote execution path: `/home/<username>/Code/FRESCO-Pipeline`
- Git commit (pipeline): **unknown** — the Gilbreth execution directory is not a git repository, so `run_metadata.json` could not pin a commit
- Conda env: `fresco_v2`
- SLURM job script: `scripts/production_v3.slurm`

## Execution

- Cluster: Gilbreth (Purdue RCAC)
- Partition: `a100-80gb` (only valid partition for `<group>` account)
- SLURM job IDs:
  - ~~10323059~~ — CANCELLED (wrong partition: `a10`)
  - **10387798** — COMPLETED ✅
- Job 10387798 start: 2026-03-09T10:47:11 EDT
- Job 10387798 end:   2026-03-09T13:20:23 EDT
- Elapsed: 2h 33m 12s

## Outputs

- Output file: `/depot/<group>/data/josh/FRESCO/chunks-v3/PROD-20260203-v3_v3.parquet`
- Row groups: 62,668
- Total rows: **655,327,086**
- Input manifest: `manifests/input_manifest.jsonl` (**62,668** entries)
- Output manifest: `manifests/output_manifest.jsonl` (**1** entry)
- Run metadata: `manifests/run_metadata.json`
- Validation present: `validation/schema_report.json`

## Results Summary

### Cluster distribution (from verify job 10393102)

| Cluster   | Rows         | Pct    |
|-----------|-------------|--------|
| anvil     | 63,220,257  | 9.65%  |
| conte     | 86,521,057  | 13.20% |
| stampede  | 505,585,772 | 77.15% |
| **Total** | **655,327,086** | 100% |

### Schema

All three clusters present. Timestamp fields (`time`, `submit_time`, `start_time`, `end_time`) confirmed as `timestamp[us]`. See `docs/SCHEMA_AND_PROVENANCE.md` for full column list.

**Note**: Actual output schema uses raw FRESCO column naming (`value_memused`, `value_cpuuser`, etc.), not the aspirational canonical names in the schema docs. See Known Issues.

## Validation Summary

- Level 0 (schema): ✅ All clusters present, required columns present
- Basic verification: ✅ `verify_v3_output.py` completed successfully in job **10393102**
- Validation artifacts actually present:
  - ✅ `validation/schema_report.json`
  - ❌ `validation/missingness_report.json`
  - ❌ `validation/dtype_report.json`
  - ❌ `validation/sanity_checks.json`
- Level 1/2/3 status: **not fully satisfied** because the current production script only writes `schema_report.json`

## Verification Status

| Job ID   | Status               | Notes |
|----------|----------------------|-------|
| 10387799 | **FAILED** (exit 1)  | `AttributeError: ParquetSchema has no .field()` — PyArrow API bug in script. Fixed in `scripts/verify_v3_output.py` (commit `af32734`). |
| **10393102** | **COMPLETED** (exit 0) | Resubmitted after fix; verified cluster counts and timestamp field types successfully. |

## Known Issues / Caveats

1. **Schema implementation gap**: The actual v3 parquet output uses raw FRESCO column names (`value_memused`, `value_gpu`, `value_cpuuser`, `value_nfs`, `value_block`, `queue`) rather than the normalized fields described in `docs/SCHEMA_AND_PROVENANCE.md` (`peak_memory_gb`, `partition`, etc.). Derived columns (`runtime_sec`, `queue_time_sec`, `runtime_fraction`, `peak_memory_fraction`) are not stored, so downstream analysis must either derive them post hoc or the production pipeline must be extended and rerun.

2. **Reproducibility gap**: `run_metadata.json` contains `"git_commit": "unknown"` because `/home/<username>/Code/FRESCO-Pipeline` is not a git repository on Gilbreth. The current metadata also lacks a recorded `completed_at`, host, and environment lock artifact paths.

3. **Validation artifact gap**: Although `write_validation_reports=true`, `build_production_v3.py` currently writes only `validation/schema_report.json`. The required `missingness_report.json`, `dtype_report.json`, and `sanity_checks.json` are not generated yet.

4. **Manifest completeness gap**: The manifests exist, but they record only paths, sizes, row counts, and timestamps — not checksums/hashes — so they do not yet meet the stronger provenance standard described in the docs and skills.

5. **Archive missing**: No archive folder exists yet under `/depot/<group>/data/josh/FRESCO-Research/runs/PROD-20260203-v3`.

6. **Research status**: All completed modeling and overlap experiments in `experiments/EXP-016` through `EXP-038` remain **proxy-only** (`local_job_partials_snapshot`, proxy label `value_memused_max`) and are not publication-grade.

## Next Actions

1. Bring `build_production_v3.py` up to the documented spec:
   - materialize the intended canonical/derived columns or define a post-processing step that does so,
   - emit the full validation artifact set,
   - capture reproducibility metadata from a git-tracked code checkout.
2. Archive `PROD-20260203-v3` only after those gaps are closed.
3. Then rerun Phase 1/2/3 experiments on authoritative v3 data instead of the proxy snapshot.

## Repro Steps

```bash
# On Gilbreth:
conda activate fresco_v2
cd /home/<username>/Code/FRESCO-Pipeline
sbatch --partition=a100-80gb --account=<group> production_v3.slurm
```
