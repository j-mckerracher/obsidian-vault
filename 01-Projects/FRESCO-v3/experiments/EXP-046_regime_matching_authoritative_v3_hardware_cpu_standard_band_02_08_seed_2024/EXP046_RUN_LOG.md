# EXP-046 Run Log  Regime matching on authoritative v3 with recovered hardware CPU-standard regime (repeat seed 2024)

**Run ID**: EXP-046_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_seed_2024  
**Date**: 2026-03-12

## Objective
Repeat the authoritative Anvil -> Conte overlap analysis under alternate random seed `2024` to test whether the hardware-aware overlap cohort is stable.

## Inputs
- Dataset label: `chunks-v3-authoritative`
- Input manifest: `/depot/<group>/data/josh/FRESCO/chunks-v3/manifests/output_manifest.jsonl`
- Source cluster: anvil
- Target cluster: conte
- Regime: `hardware_cpu_standard`
- Random seed: `2024`

## Code & Environment
- Script: `scripts/regime_matching.py`
- Config: `experiments/EXP-046_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_seed_2024/config/exp046_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_seed_2024.json`
- Hardware metadata source: `config/clusters.json`
- Overlap feature set:
  - `ncores`
  - `nhosts`
  - `timelimit_sec`
  - `runtime_sec`
  - `queue_time_sec`
  - `runtime_fraction`

## Notes
- `partition` is recovered from the raw `queue` field at analysis time.
- `node_memory_gb`, `node_cores`, `gpu_count_per_node`, and `node_type` are recovered from `config/clusters.json`.
- Conte queue identifiers remain anonymized, so recovered hardware metadata uses cluster-wide defaults there.

## Execution
Planned repro command:
```powershell
python scripts
egime_matching.py --config experiments\EXP-046_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_seed_2024\config\exp046_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_seed_2024.json
```

Submitted on Gilbreth:
- Pending submission.

## Outputs
- Overlap report: `experiments/EXP-046_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_seed_2024/results/overlap_report.json`
- Matched indices:
  - `.../results/matched_source_indices.parquet`
  - `.../results/matched_target_indices.parquet`
- Provenance: `.../manifests/run_metadata.json`, `.../manifests/input_files_used.json`

## Results Summary
- Pending execution.
- Key checks after completion:
  - domain classifier AUC
  - target overlap coverage
  - source / target overlap cohort sizes
  - within-overlap KS statistics
