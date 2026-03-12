# EXP-076 Run Log -- Planned runtime-sec-only frozen-universe follow-up

**Run ID**: EXP-076_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_runtime_sec_only
**Date**: 2026-03-12
**Owner**: <username>

## Objective
Measure whether the runtime-sec-only feature recipe can retain positive Anvil -> Conte `peak_memory_fraction` transfer on the first frozen universe.

## Hypothesis (if experiment)
If the first frozen-universe success only needed one duration-control variable, this reduced feature set should keep target transfer near or above zero without relying on the full timing trio.

## Inputs
- Dataset label: `chunks-v3-authoritative`
- Input manifest: `/depot/<group>/data/josh/FRESCO/chunks-v3/manifests/output_manifest.jsonl`
- Frozen sampling plan: `experiments/ANALYSIS_seed_instability/frozen_sampling_plan_exp044_hwcpu_standard_300k_24_seed1337.json`
- Clusters: anvil / conte / stampede
- Date range: 2015-01-01 to 2023-12-31
- Source cluster: anvil
- Target cluster: conte
- Regime: `hardware_cpu_standard`
- Cohorts: `experiments/EXP-075_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_runtime_sec_only/results/matched_source_indices.parquet` and `experiments/EXP-075_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_runtime_sec_only/results/matched_target_indices.parquet`
- Label: `peak_memory_fraction` with `log1p` transform (`label_proxy=false`)
- Modeling split seed: `1337`

## Code & Environment
- Script: `scripts\model_transfer.py`
- Config: `experiments/EXP-076_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_runtime_sec_only/config/exp076_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_runtime_sec_only.json`
- Git commit (pipeline): `TBD at execution time; stage and commit this scaffold before submission`
- Git commit (analysis): `TBD at execution time`
- Conda env: `TBD at execution time`
- Python: `TBD at execution time`
- Package lock: `experiments/EXP-076_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_runtime_sec_only/validation/pip_freeze.txt`

## Notes
- This model reuses the EXP-075 overlap cohort on the first frozen universe.
- `scripts\model_transfer.py` applies `log1p` to configured feature columns before scaling and fitting, so this design effectively tests `log1p(runtime_sec)` without a pipeline code change.
- A positive result here is not sufficient on its own; EXP-078 is the paired second-universe robustness check.
- This run has not been submitted yet; metrics and job IDs are intentionally blank until execution completes.

## Execution
- Cluster: Gilbreth
- Submission command: `Planned repro command: python scripts\model_transfer.py --config experiments\EXP-076_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_runtime_sec_only\config\exp076_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_runtime_sec_only.json`
- Job IDs: `Not assigned yet`
- Start / end time (UTC): `N/A / N/A`

## Outputs
- Output root: `experiments/EXP-076_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_runtime_sec_only/results/`
- Manifests: `experiments/EXP-076_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_runtime_sec_only/manifests/`
- Validation reports: `experiments/EXP-076_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_runtime_sec_only/validation/`

## Results Summary
- Planned run only; no job has been submitted yet, so no overlap or modeling metrics exist.
- Expected result artifacts, once executed, will be written under `experiments/EXP-076_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_runtime_sec_only/results/` and must be cited before making any claim.

## Validation Summary
- Not run yet. Validation artifacts will be produced under `experiments/EXP-076_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_runtime_sec_only/validation/` after execution.

## Known Issues / Caveats
- This log records a planned run only; nothing here should be interpreted as executed evidence until the job completes and the Results Summary is rewritten.
- The reduced timing design keeps only `runtime_sec` as the duration-control feature because the report recommends collapsing the redundant timing trio to one transformed feature and the current scripts already apply `log1p` to every configured feature.
- The design should be judged across both frozen universes together; a positive result on only one universe is not sufficient after EXP-070..074.

## Repro Steps
1. Commit this scaffold before submission so the config used at runtime is pinned in git.
2. Capture the execution environment into `experiments/EXP-076_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_runtime_sec_only/validation/` before or at job start.
3. Run `python scripts\model_transfer.py --config experiments\EXP-076_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_runtime_sec_only\config\exp076_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_runtime_sec_only.json`.
