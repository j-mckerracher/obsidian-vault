# EXP-074 Run Log -- Planned second frozen-universe no-queue modeling (repeat split seed 2026)

**Run ID**: EXP-074_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_plan2024_seed_2026  
**Date**: 2026-03-12  
**Owner**: <username>

## Objective
Evaluate whether the stable positive target transfer from EXP-063/065/067/069 persists when the no-queue feature recipe is applied to a different frozen sampled universe.

## Hypothesis (if experiment)
If the stable positive result is genuinely robust to sampled-universe choice, then this run should retain target `R^2 > 0` on the second frozen plan while reusing the same no-queue feature set and modeling recipe.

## Inputs
- Dataset label: `chunks-v3-authoritative`
- Input manifest: `/depot/<group>/data/josh/FRESCO/chunks-v3/manifests/output_manifest.jsonl`
- Frozen sampling plan: `experiments/ANALYSIS_seed_instability/frozen_sampling_plan_exp070_hwcpu_standard_300k_24_seed2024.json`
- Clusters: anvil / conte / stampede
- Date range: 2015-01-01 to 2023-12-31
- Cohorts (planned from `EXP-070_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_no_queuetime_plan2024`):
  - `experiments/EXP-070_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_no_queuetime_plan2024/results/matched_source_indices.parquet`
  - `experiments/EXP-070_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_no_queuetime_plan2024/results/matched_target_indices.parquet`
- Label: `peak_memory_fraction` with `log1p` transform (`label_proxy=false`)
- Modeling split seed: `2026`

## Code & Environment
- Script: `scripts\model_transfer.py`
- Config: `experiments/EXP-074_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_plan2024_seed_2026/config/exp074_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_plan2024_seed_2026.json`
- Git commit (pipeline): `TBD before submission`
- Git commit (analysis): `TBD before submission`
- Conda env: `fresco_v2`
- Python: `TBD before submission`
- Package lock: `experiments/EXP-074_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_plan2024_seed_2026/validation/pip_freeze.txt`

## Execution
- Cluster: Gilbreth
- Submission command: `TBD before submission; expected wrapper will target the training partition`
- Job IDs: `Not assigned yet`
- Start / end time (UTC): `N/A / N/A`

## Outputs
- Output root: `experiments/EXP-074_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_plan2024_seed_2026/results/`
- Manifests: `experiments/EXP-074_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_plan2024_seed_2026/manifests/`
- Validation reports: `experiments/EXP-074_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_plan2024_seed_2026/validation/`

## Results Summary
- Planned run only; no job has been submitted yet.
- Success criterion: target `R^2` should remain positive on the second frozen universe, and repeated split seeds should stay directionally consistent.

## Validation Summary
- Not run yet. Validation artifacts will be written under `experiments/EXP-074_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_plan2024_seed_2026/validation/` after execution.

## Known Issues / Caveats
- These runs isolate frozen-universe choice; they do not broaden the claim to another cluster pair.
- The normalized label still carries the cross-cluster measurement-semantics caveat (`memory_includes_cache=true` on anvil and `false` on conte/stampede).
- If the positive result disappears here, the EXP-062..069 finding should be interpreted as conditional on the first frozen universe rather than a universal matched-regime claim.

## Repro Steps
1. `source ~/anaconda3/bin/activate fresco_v2`
2. `python scripts/model_transfer.py --config experiments/EXP-074_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_plan2024_seed_2026/config/exp074_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_plan2024_seed_2026.json`
