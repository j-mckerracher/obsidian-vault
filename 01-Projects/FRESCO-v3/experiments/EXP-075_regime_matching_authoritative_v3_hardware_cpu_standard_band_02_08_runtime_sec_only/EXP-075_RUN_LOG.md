# EXP-075 Run Log -- Planned runtime-sec-only frozen-universe follow-up

**Run ID**: EXP-075_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_runtime_sec_only
**Date**: 2026-03-12
**Owner**: <username>

## Objective
Test whether collapsing the remaining timing block to `runtime_sec` yields a cleaner authoritative Anvil -> Conte overlap on the first frozen universe.

## Hypothesis (if experiment)
If the residual instability comes from the redundant timing trio rather than `runtime_sec` alone, then keeping only `runtime_sec` alongside `ncores` and `nhosts` should preserve usable overlap while reducing within-overlap timing mismatch relative to EXP-062.

## Inputs
- Dataset label: `chunks-v3-authoritative`
- Input manifest: `/depot/<group>/data/josh/FRESCO/chunks-v3/manifests/output_manifest.jsonl`
- Frozen sampling plan: `experiments/ANALYSIS_seed_instability/frozen_sampling_plan_exp044_hwcpu_standard_300k_24_seed1337.json`
- Clusters: anvil / conte / stampede
- Date range: 2015-01-01 to 2023-12-31
- Source cluster: anvil
- Target cluster: conte
- Regime: `hardware_cpu_standard`

## Code & Environment
- Script: `scripts\regime_matching.py`
- Config: `experiments/EXP-075_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_runtime_sec_only/config/exp075_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_runtime_sec_only.json`
- Git commit (pipeline): `TBD at execution time; stage and commit this scaffold before submission`
- Git commit (analysis): `TBD at execution time`
- Conda env: `TBD at execution time`
- Python: `TBD at execution time`
- Package lock: `experiments/EXP-075_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_runtime_sec_only/validation/pip_freeze.txt`

## Notes
- This first reduced-timing pilot keeps the frozen EXP-044-equivalent sampling universe from EXP-062.
- `scripts\regime_matching.py` applies `log1p` to configured feature columns before fitting, so `runtime_sec` is already treated as the single transformed duration-control feature.
- This run should be interpreted jointly with EXP-077 so the design is tested on both frozen universes immediately rather than repeating the earlier single-universe false-positive cycle.
- This run has not been submitted yet; metrics and job IDs are intentionally blank until execution completes.

## Execution
- Cluster: Gilbreth
- Submission command: `Planned repro command: python scripts\regime_matching.py --config experiments\EXP-075_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_runtime_sec_only\config\exp075_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_runtime_sec_only.json`
- Job IDs: `Not assigned yet`
- Start / end time (UTC): `N/A / N/A`

## Outputs
- Output root: `experiments/EXP-075_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_runtime_sec_only/results/`
- Manifests: `experiments/EXP-075_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_runtime_sec_only/manifests/`
- Validation reports: `experiments/EXP-075_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_runtime_sec_only/validation/`

## Results Summary
- Planned run only; no job has been submitted yet, so no overlap or modeling metrics exist.
- Expected result artifacts, once executed, will be written under `experiments/EXP-075_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_runtime_sec_only/results/` and must be cited before making any claim.

## Validation Summary
- Not run yet. Validation artifacts will be produced under `experiments/EXP-075_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_runtime_sec_only/validation/` after execution.

## Known Issues / Caveats
- This log records a planned run only; nothing here should be interpreted as executed evidence until the job completes and the Results Summary is rewritten.
- The reduced timing design keeps only `runtime_sec` as the duration-control feature because the report recommends collapsing the redundant timing trio to one transformed feature and the current scripts already apply `log1p` to every configured feature.
- The design should be judged across both frozen universes together; a positive result on only one universe is not sufficient after EXP-070..074.

## Repro Steps
1. Commit this scaffold before submission so the config used at runtime is pinned in git.
2. Capture the execution environment into `experiments/EXP-075_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_runtime_sec_only/validation/` before or at job start.
3. Run `python scripts\regime_matching.py --config experiments\EXP-075_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_runtime_sec_only\config\exp075_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_runtime_sec_only.json`.
