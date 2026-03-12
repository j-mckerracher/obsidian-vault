# EXP-049 Run Log  Modeling on authoritative v3 hardware CPU-standard overlap cohorts with normalized peak memory (repeat seed 2025)

**Run ID**: EXP-049_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_seed_2025  
**Date**: 2026-03-12

## Objective
Repeat the authoritative Anvil -> Conte transfer model under alternate random seed `2025` to test whether the positive `peak_memory_fraction` result persists.

## Inputs
- Dataset label: `chunks-v3-authoritative`
- Input manifest: `/depot/<group>/data/josh/FRESCO/chunks-v3/manifests/output_manifest.jsonl`
- Cohorts (from EXP-048):
  - `experiments/EXP-048_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_seed_2025/results/matched_source_indices.parquet`
  - `experiments/EXP-048_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_seed_2025/results/matched_target_indices.parquet`
- Label: `peak_memory_fraction` with `log1p` transform (`label_proxy=false`)
- Random seed: `2025`

## Code & Environment
- Script: `scripts/model_transfer.py`
- Config: `experiments/EXP-049_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_seed_2025/config/exp049_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_seed_2025.json`
- Hardware metadata source: `config/clusters.json`
- Model: `Ridge(alpha=1.0)`
- Adaptation: `none`
- Overlap feature set:
  - `ncores`
  - `nhosts`
  - `timelimit_sec`
  - `runtime_sec`
  - `queue_time_sec`
  - `runtime_fraction`

## Notes
- `peak_memory_fraction` is derived at analysis time as `peak_memory_gb / (node_memory_gb * nhosts)`.
- `peak_memory_gb` is inferred from `value_memused_max`; in the current authoritative parquet, that series is already GB-scale.
- The normalized label does not remove the cross-cluster measurement-semantic caveat (`memory_includes_cache=true` on anvil and `false` on conte/stampede).

## Execution
Planned repro command:
```powershell
python scripts/model_transfer.py --config experiments/EXP-049_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_seed_2025/config/exp049_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_seed_2025.json
```

Submitted on Gilbreth:
- Pending submission.

## Outputs
- Metrics: `experiments/EXP-049_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_seed_2025/results/metrics.json`
- Predictions:
  - `.../results/predictions_source_test.parquet`
  - `.../results/predictions_target.parquet`
- Provenance: `.../manifests/run_metadata.json`, `.../manifests/input_files_used.json`

## Results Summary
- Pending execution.
- Key checks after completion:
  - source-test `R^2`
  - target `R^2`
  - target bootstrap `R^2` interval
  - evaluation cohort sizes
