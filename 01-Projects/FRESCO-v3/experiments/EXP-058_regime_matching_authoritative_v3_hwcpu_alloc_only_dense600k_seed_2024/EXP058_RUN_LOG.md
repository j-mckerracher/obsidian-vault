# EXP-058 Run Log  Dense alloc-only overlap diagnosis on authoritative v3 hardware CPU-standard cohorts

**Run ID**: EXP-058_regime_matching_authoritative_v3_hwcpu_alloc_only_dense600k_seed_2024  
**Date**: 2026-03-12

## Objective
Test whether removing scheduler/performance timing features from overlap matching reduces cross-cluster separability on the dense-sampled Anvil -> Conte hardware CPU-standard comparison.

## Inputs
- Dataset label: `chunks-v3-authoritative`
- Input manifest: `/depot/<group>/data/josh/FRESCO/chunks-v3/manifests/output_manifest.jsonl`
- Source cluster: anvil
- Target cluster: conte
- Regime: `hardware_cpu_standard`
- Random seed: `2024`

## Code & Environment
- Script: `scripts/regime_matching.py`
- Config: `experiments/EXP-058_regime_matching_authoritative_v3_hwcpu_alloc_only_dense600k_seed_2024/config/exp058_regime_matching_authoritative_v3_hwcpu_alloc_only_dense600k_seed_2024.json`
- Hardware metadata source: `config/clusters.json`
- Sampling controls:
  - `max_rows_per_cluster = 600000`
  - `sample_n_row_groups_per_file = 128`
- Overlap feature set:
  - `ncores`
  - `nhosts`
  - `timelimit_sec`

## Notes
- This run follows the dense-sampling diagnosis, which suggested `queue_time_sec` and `runtime_fraction` remain major mismatch drivers.
- `partition` is recovered from the raw `queue` field at analysis time.

## Execution
Planned repro command:
```bash
python scripts/regime_matching.py --config experiments/EXP-058_regime_matching_authoritative_v3_hwcpu_alloc_only_dense600k_seed_2024/config/exp058_regime_matching_authoritative_v3_hwcpu_alloc_only_dense600k_seed_2024.json
```

Submitted on Gilbreth:
- Pending submission.

## Outputs
- Overlap report: `experiments/EXP-058_regime_matching_authoritative_v3_hwcpu_alloc_only_dense600k_seed_2024/results/overlap_report.json`
- Matched indices:
  - `.../results/matched_source_indices.parquet`
  - `.../results/matched_target_indices.parquet`
- Provenance: `.../manifests/run_metadata.json`, `.../manifests/input_files_used.json`

## Results Summary
- Pending execution.
- Key checks after completion:
  - domain classifier AUC
  - target overlap coverage
  - whether alloc-only overlap lowers separability relative to the dense safe-feature runs
