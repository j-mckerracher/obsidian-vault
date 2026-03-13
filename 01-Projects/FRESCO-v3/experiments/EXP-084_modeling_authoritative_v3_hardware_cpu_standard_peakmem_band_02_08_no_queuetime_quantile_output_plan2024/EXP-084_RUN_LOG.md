# EXP-084 Run Log -- Staged quantile-output adaptation modeling on the frozen no-queue universe

**Run ID**: EXP-084_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_quantile_output_plan2024
**Date**: 2026-03-13
**Owner**: <username>

## Objective
Test the same zero-label post-prediction quantile-matching correction on the second frozen no-queue universe after both CORAL variants failed to improve the harder baseline.

## Hypothesis (if experiment)
If the remaining universe-2 error is mostly a prediction-distribution shape mismatch rather than an input-covariance problem, then a monotone quantile-output correction should give a more informative second-universe result than any of the CORAL runs.

## Inputs
- Dataset label: `chunks-v3-authoritative`
- Input manifest: `/depot/<group>/data/josh/FRESCO/chunks-v3/manifests/output_manifest.jsonl`
- Frozen sampling plan: `experiments/ANALYSIS_seed_instability/frozen_sampling_plan_exp070_hwcpu_standard_300k_24_seed2024.json`
- Clusters: anvil / conte / stampede
- Date range: 2015-01-01 to 2023-12-31
- Source cluster: anvil
- Target cluster: conte
- Regime: `hardware_cpu_standard`
- Cohorts: `experiments/EXP-070_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_no_queuetime_plan2024/results/matched_source_indices.parquet and experiments/EXP-070_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_no_queuetime_plan2024/results/matched_target_indices.parquet`
- Label: `peak_memory_fraction` with `log1p` transform (`label_proxy=false`)
- Modeling split seed: `1337`
- Adaptation: quantile-output matching with `n_quantiles = 100`

## Code & Environment
- Script: `scripts\model_transfer.py`
- Config: `experiments/EXP-084_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_quantile_output_plan2024/config/exp084_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_quantile_output_plan2024.json`
- Base config copied from: `EXP-071`
- Primary comparison targets after execution: `EXP-071, EXP-080, and EXP-082`
- Planned conda env: `fresco_v2`
- Planned Python: `/home/<username>/anaconda3/envs/fresco_v2/bin/python`

## Execution
- Cluster: Gilbreth
- Submission command: `Not submitted yet`
- Job IDs: `pending`
- Start / end time (UTC): `pending`

## Outputs
- Output root: `experiments/EXP-084_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_quantile_output_plan2024/results/`
- Manifests: `experiments/EXP-084_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_quantile_output_plan2024/manifests/`
- Validation reports: `experiments/EXP-084_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_quantile_output_plan2024/validation/`

## Results Summary
- Not run yet; this staged experiment keeps the same frozen cohort and five-feature no-queue model space as `EXP-071` while changing only the post-prediction adaptation step.
- Primary question after execution: can a monotone output-space correction fix the target prediction shape mismatch without touching the input feature geometry?

## Validation Summary
- Config and run log staged locally only; manifests, validation artifacts, metrics, and predictions will be populated after a future Gilbreth run.
- No SLURM job has been submitted for this experiment yet.

## Known Issues / Caveats
- This staged run reuses the same frozen EXP-070 cohort and five-feature no-queue model space as EXP-071, changing only the adaptation step after prediction.
- `quantile_output` matches the target prediction distribution to the source-train prediction distribution without using target labels, but it can still distort semantics if the source prediction distribution is a poor reference.
- The run is staged only. No SLURM job has been submitted yet.

## Repro Steps
1. `source ~/anaconda3/bin/activate fresco_v2`
2. `cd /home/<username>/Code/FRESCO-Pipeline`
3. `python scripts/model_transfer.py --config experiments/EXP-084_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_quantile_output_plan2024/config/exp084_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_quantile_output_plan2024.json`
