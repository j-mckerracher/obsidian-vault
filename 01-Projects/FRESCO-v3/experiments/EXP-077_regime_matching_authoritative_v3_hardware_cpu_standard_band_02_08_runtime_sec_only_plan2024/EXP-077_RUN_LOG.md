# EXP-077 Run Log -- Planned runtime-sec-only frozen-universe follow-up

**Run ID**: EXP-077_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_runtime_sec_only_plan2024
**Date**: 2026-03-12
**Owner**: <username>

## Objective
Repeat the runtime-sec-only overlap test on the second frozen universe immediately, so the design is judged on cross-universe robustness rather than a single favorable cohort.

## Hypothesis (if experiment)
If the timing-trio redundancy was the main universe-sensitivity driver, the runtime-sec-only design should reduce the overlap mismatch spike seen in EXP-070 on the alternate frozen plan.

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
- Config: `experiments/EXP-077_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_runtime_sec_only_plan2024/config/exp077_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_runtime_sec_only_plan2024.json`
- Git commit (pipeline): `TBD at execution time; stage and commit this scaffold before submission`
- Git commit (analysis): `TBD at execution time`
- Conda env: `TBD at execution time`
- Python: `TBD at execution time`
- Package lock: `experiments/EXP-077_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_runtime_sec_only_plan2024/validation/pip_freeze.txt`

## Notes
- This run uses the second frozen sampling plan from EXP-070 so the reduced timing recipe is tested on both universes immediately.
- `runtime_fraction` was the single worst remaining overlap feature in both EXP-062 and EXP-070, so this design removes it entirely instead of merely dropping `queue_time_sec`.
- Interpret this run together with EXP-075; if the overlap still deteriorates materially here, the next fallback should be adaptation rather than another timing-only tweak.
- This run has not been submitted yet; metrics and job IDs are intentionally blank until execution completes.

## Execution
- Cluster: Gilbreth
- Submission command: `Planned repro command: python scripts\regime_matching.py --config experiments\EXP-077_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_runtime_sec_only_plan2024\config\exp077_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_runtime_sec_only_plan2024.json`
- Job IDs: `Not assigned yet`
- Start / end time (UTC): `N/A / N/A`

## Outputs
- Output root: `experiments/EXP-077_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_runtime_sec_only_plan2024/results/`
- Manifests: `experiments/EXP-077_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_runtime_sec_only_plan2024/manifests/`
- Validation reports: `experiments/EXP-077_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_runtime_sec_only_plan2024/validation/`

## Results Summary
- Planned run only; no job has been submitted yet, so no overlap or modeling metrics exist.
- Expected result artifacts, once executed, will be written under `experiments/EXP-077_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_runtime_sec_only_plan2024/results/` and must be cited before making any claim.

## Validation Summary
- Not run yet. Validation artifacts will be produced under `experiments/EXP-077_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_runtime_sec_only_plan2024/validation/` after execution.

## Known Issues / Caveats
- This log records a planned run only; nothing here should be interpreted as executed evidence until the job completes and the Results Summary is rewritten.
- The reduced timing design keeps only `runtime_sec` as the duration-control feature because the report recommends collapsing the redundant timing trio to one transformed feature and the current scripts already apply `log1p` to every configured feature.
- The design should be judged across both frozen universes together; a positive result on only one universe is not sufficient after EXP-070..074.

## Repro Steps
1. Commit this scaffold before submission so the config used at runtime is pinned in git.
2. Capture the execution environment into `experiments/EXP-077_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_runtime_sec_only_plan2024/validation/` before or at job start.
3. Run `python scripts\regime_matching.py --config experiments\EXP-077_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_runtime_sec_only_plan2024\config\exp077_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_runtime_sec_only_plan2024.json`.
