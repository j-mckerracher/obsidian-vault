# EXP-042 Run Log  Regime matching on authoritative v3 with safe features

**Run ID**: EXP-042_regime_matching_authoritative_v3_safe_features_band_02_08  
**Date**: 2026-03-12

## Objective
Re-run the authoritative Anvil -> Conte overlap analysis using only the strict 0% missingness safe features from Phase 1.

## Inputs
- Dataset label: `chunks-v3-authoritative`
- Input manifest: `/depot/<group>/data/josh/FRESCO/chunks-v3/manifests/output_manifest.jsonl`
- Source cluster: anvil
- Target cluster: conte
- Regime: `cpu_standard`

## Code & Environment
- Script: `scripts/regime_matching.py`
- Config: `experiments/EXP-042_regime_matching_authoritative_v3_safe_features_band_02_08/config/exp042_regime_matching_authoritative_v3_safe_features_band_02_08.json`
- Safe feature set:
  - `ncores`
  - `nhosts`
  - `timelimit_sec`
  - `runtime_sec`
  - `queue_time_sec`
  - `runtime_fraction`

## Execution
Planned repro command:
```powershell
python scripts\regime_matching.py --config experiments\EXP-042_regime_matching_authoritative_v3_safe_features_band_02_08\config\exp042_regime_matching_authoritative_v3_safe_features_band_02_08.json
```

## Outputs
- Overlap report: `experiments/EXP-042_regime_matching_authoritative_v3_safe_features_band_02_08/results/overlap_report.json`
- Matched indices:
  - `.../results/matched_source_indices.parquet`
  - `.../results/matched_target_indices.parquet`
- Provenance: `.../manifests/run_metadata.json`, `.../manifests/input_files_used.json`

## Results Summary
Pending run.

## Known Issues / Caveats
- Regime is still proxy-based because the authoritative parquet still does not materialize `partition`, `node_type`, `node_memory_gb`, or `gpu_count_per_node`.
- This run is intended to test whether removing raw performance counters from the overlap feature set reduces domain separability relative to EXP-040.
