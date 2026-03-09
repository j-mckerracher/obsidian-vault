# PROD-20260203-v3 Run Log — FRESCO v3 Production Dataset Build

**Run ID**: PROD-20260203-v3  
**Date**: 2026-02-03 (submitted) / 2026-03-09 (executed)

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
- Git commit (pipeline): see SLURM job logs
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

## Results Summary

### Cluster distribution (from verify job 10387799 stdout before failure)

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
- Level 1 (sanity): Not yet formally verified — pending verify job completion
- Level 2/3: Not yet run

## Verification Status

| Job ID   | Status               | Notes |
|----------|----------------------|-------|
| 10387799 | **FAILED** (exit 1)  | `AttributeError: ParquetSchema has no .field()` — PyArrow API bug in script. Fixed in `scripts/verify_v3_output.py` (commit `af32734`). |
| **10393102** | **PENDING** (Priority) | Resubmitted 2026-03-09 after fix. |

## Known Issues / Caveats

1. **Schema naming discrepancy**: The actual v3 parquet output uses raw FRESCO column names (`value_memused`, `value_gpu`, `value_cpuuser`, `value_nfs`, `value_block`, `queue`) rather than the normalized names described in `docs/SCHEMA_AND_PROVENANCE.md` (`peak_memory_gb`, `partition`, etc.). Derived columns (`runtime_sec`, `queue_time_sec`, `runtime_fraction`, `peak_memory_fraction`) are not stored — they must be computed at analysis time. **The canonical schema skill and docs need updating to reflect this.**

2. **Verify job failure**: Job 10387799 failed on `parquet_file.schema.field()` — this method does not exist on `ParquetSchema`; use `schema_arrow.field()` instead. Fixed (commit `af32734`), resubmitted as job 10393102.

3. **Original submission delay**: Initial SLURM scripts targeted `--partition=a10` (zero quota). Corrected to `a100-80gb` on 2026-03-07, but the job queued until 2026-03-09 while other `<group>` users held both A100 slots.

4. **Manifests not confirmed**: Manifest files (`input_manifest.jsonl`, `output_manifest.jsonl`, `run_metadata.json`) have not been confirmed to exist in the output directory. Requires post-verify inspection.

## Repro Steps

```bash
# On Gilbreth:
conda activate fresco_v2
cd /home/<username>/Code/FRESCO-Pipeline
sbatch --partition=a100-80gb --account=<group> production_v3.slurm
```
