# EXP-070 Run Log -- Planned second frozen-universe regime matching for authoritative v3 hardware CPU-standard cohorts without queue_time_sec

**Run ID**: EXP-070_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_no_queuetime_plan2024  
**Date**: 2026-03-12  
**Owner**: <username>

## Objective
Test whether the stable no-queue Anvil -> Conte overlap geometry holds on a second frozen `300k / 24` sampled universe built from a different sampling seed.

## Hypothesis (if experiment)
If the EXP-062 success is not specific to a single frozen universe, then a second frozen plan should still produce comparable overlap coverage and a similarly usable matched cohort after dropping `queue_time_sec`.

## Inputs
- Dataset label: `chunks-v3-authoritative`
- Input manifest: `/depot/<group>/data/josh/FRESCO/chunks-v3/manifests/output_manifest.jsonl`
- Frozen sampling plan: `experiments/ANALYSIS_seed_instability/frozen_sampling_plan_exp070_hwcpu_standard_300k_24_seed2024.json`
- Clusters: anvil / conte / stampede
- Date range: 2015-01-01 to 2023-12-31
- Source cluster: anvil
- Target cluster: conte
- Regime: `hardware_cpu_standard`

## Code & Environment
- Script: `scripts\regime_matching.py`
- Config: `experiments/EXP-070_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_no_queuetime_plan2024/config/exp070_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_no_queuetime_plan2024.json`
- Git commit (pipeline): `TBD before submission`
- Git commit (analysis): `TBD before submission`
- Conda env: `fresco_v2`
- Python: `TBD before submission`
- Package lock: `experiments/EXP-070_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_no_queuetime_plan2024/validation/pip_freeze.txt`

## Execution
- Cluster: Gilbreth
- Submission command: `TBD before submission; expected wrapper will target the training partition`
- Job IDs: `Not assigned yet`
- Start / end time (UTC): `N/A / N/A`

## Outputs
- Output root: `experiments/EXP-070_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_no_queuetime_plan2024/results/`
- Manifests: `experiments/EXP-070_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_no_queuetime_plan2024/manifests/`
- Validation reports: `experiments/EXP-070_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_no_queuetime_plan2024/validation/`

## Results Summary
- Planned run only; no job has been submitted yet.
- Success criterion: overlap geometry should remain near the EXP-062 baseline while using a different frozen sampling plan.

## Validation Summary
- Not run yet. Validation artifacts will be written under `experiments/EXP-070_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_no_queuetime_plan2024/validation/` after execution.

## Known Issues / Caveats
- This run is explicitly a frozen-universe sensitivity test, not a new feature-set ablation.
- The new plan uses base seed 2024 (target seed 2025), so any geometry shift should be interpreted as sampled-universe sensitivity rather than model-split noise.
- If overlap quality degrades materially, the stable EXP-062..069 claim should be restricted to the first frozen universe until broader evidence is gathered.

## Repro Steps
1. `source ~/anaconda3/bin/activate fresco_v2`
2. `python scripts/regime_matching.py --config experiments/EXP-070_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_no_queuetime_plan2024/config/exp070_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_no_queuetime_plan2024.json`
