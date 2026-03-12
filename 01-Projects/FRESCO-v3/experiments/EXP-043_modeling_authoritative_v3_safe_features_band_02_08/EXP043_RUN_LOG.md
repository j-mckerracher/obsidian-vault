# EXP-043 Run Log  Modeling on authoritative v3 safe-feature overlap cohorts

**Run ID**: EXP-043_modeling_authoritative_v3_safe_features_band_02_08  
**Date**: 2026-03-12

## Objective
Train and evaluate the authoritative Anvil -> Conte transfer model on overlap cohorts defined only by the strict safe features from Phase 1.

## Inputs
- Dataset label: `chunks-v3-authoritative`
- Input manifest: `/depot/<group>/data/josh/FRESCO/chunks-v3/manifests/output_manifest.jsonl`
- Cohorts (from EXP-042):
  - `experiments/EXP-042_regime_matching_authoritative_v3_safe_features_band_02_08/results/matched_source_indices.parquet`
  - `experiments/EXP-042_regime_matching_authoritative_v3_safe_features_band_02_08/results/matched_target_indices.parquet`
- Label: `value_memused_max` with `log1p` transform (`label_proxy=false`)

## Code & Environment
- Script: `scripts/model_transfer.py`
- Config: `experiments/EXP-043_modeling_authoritative_v3_safe_features_band_02_08/config/exp043_modeling_authoritative_v3_safe_features_band_02_08.json`
- Model: Ridge(alpha=1.0)
- Adaptation: none
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
python scripts\model_transfer.py --config experiments\EXP-043_modeling_authoritative_v3_safe_features_band_02_08\config\exp043_modeling_authoritative_v3_safe_features_band_02_08.json
```

## Outputs
- Metrics: `experiments/EXP-043_modeling_authoritative_v3_safe_features_band_02_08/results/metrics.json`
- Predictions:
  - `.../results/predictions_source_test.parquet`
  - `.../results/predictions_target.parquet`
- Provenance: `.../manifests/run_metadata.json`, `.../manifests/input_files_used.json`

## Results Summary
Pending run.

## Known Issues / Caveats
- The label remains raw peak `value_memused_max`, not normalized `peak_memory_fraction`.
- This run isolates the effect of switching to the strict safe overlap features; it does not solve the missing hardware metadata problem.
