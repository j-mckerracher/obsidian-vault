# EXP-083 Run Log -- Staged quantile-output adaptation modeling on the frozen no-queue universe

**Run ID**: EXP-083_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_quantile_output
**Date**: 2026-03-13
**Owner**: <username>

## Objective
Test a zero-label post-prediction quantile-matching correction on the first frozen no-queue universe after both CORAL variants failed to preserve the previously positive result.

## Hypothesis (if experiment)
If the universe-1 adaptation failures are driven mainly by a small number of extreme target prediction errors rather than by a globally wrong median, then a monotone quantile-output correction should clip those outliers while preserving the otherwise good central fit seen in EXP-063.

## Inputs
- Dataset label: `chunks-v3-authoritative`
- Input manifest: `/depot/<group>/data/josh/FRESCO/chunks-v3/manifests/output_manifest.jsonl`
- Frozen sampling plan: `experiments/ANALYSIS_seed_instability/frozen_sampling_plan_exp044_hwcpu_standard_300k_24_seed1337.json`
- Clusters: anvil / conte / stampede
- Date range: 2015-01-01 to 2023-12-31
- Source cluster: anvil
- Target cluster: conte
- Regime: `hardware_cpu_standard`
- Cohorts: `experiments/EXP-062_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_no_queuetime/results/matched_source_indices.parquet and experiments/EXP-062_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_no_queuetime/results/matched_target_indices.parquet`
- Label: `peak_memory_fraction` with `log1p` transform (`label_proxy=false`)
- Modeling split seed: `1337`
- Adaptation: quantile-output matching with `n_quantiles = 100`

## Code & Environment
- Script: `scripts\model_transfer.py`
- Config: `experiments/EXP-083_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_quantile_output/config/exp083_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_quantile_output.json`
- Base config copied from: `EXP-063`
- Primary comparison targets after execution: `EXP-063, EXP-079, and EXP-081`
- Planned conda env: `fresco_v2`
- Planned Python: `/home/<username>/anaconda3/envs/fresco_v2/bin/python`

## Execution
- Cluster: Gilbreth
- Submission command: `Not submitted yet`
- Job IDs: `pending`
- Start / end time (UTC): `pending`

## Outputs
- Output root: `experiments/EXP-083_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_quantile_output/results/`
- Manifests: `experiments/EXP-083_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_quantile_output/manifests/`
- Validation reports: `experiments/EXP-083_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_quantile_output/validation/`

## Results Summary
- Not run yet; this staged experiment keeps the same frozen cohort and five-feature no-queue model space as `EXP-063` while changing only the post-prediction adaptation step.
- Primary question after execution: can a monotone output-space correction fix the target prediction shape mismatch without touching the input feature geometry?

## Validation Summary
- Config and run log staged locally only; manifests, validation artifacts, metrics, and predictions will be populated after a future Gilbreth run.
- No SLURM job has been submitted for this experiment yet.

## Known Issues / Caveats
- This staged run reuses the same frozen EXP-062 cohort and five-feature no-queue model space as EXP-063, changing only the adaptation step after prediction.
- `quantile_output` matches the target prediction distribution to the source-train prediction distribution without using target labels, but it can still distort semantics if the source prediction distribution is a poor reference.
- The run is staged only. No SLURM job has been submitted yet.

## Repro Steps
1. `source ~/anaconda3/bin/activate fresco_v2`
2. `cd /home/<username>/Code/FRESCO-Pipeline`
3. `python scripts/model_transfer.py --config experiments/EXP-083_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_quantile_output/config/exp083_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_quantile_output.json`
