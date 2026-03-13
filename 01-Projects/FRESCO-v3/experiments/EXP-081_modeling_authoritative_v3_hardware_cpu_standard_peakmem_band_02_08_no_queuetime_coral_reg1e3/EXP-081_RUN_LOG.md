# EXP-081 Run Log -- Staged higher-regularization CORAL adaptation modeling on the frozen no-queue universe

**Run ID**: EXP-081_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_coral_reg1e3
**Date**: 2026-03-13
**Owner**: <username>

## Objective
Test whether increasing CORAL regularization to `1e-3` removes the outlier-like universe-1 instability seen in EXP-079 while keeping the stronger five-feature no-queue design unchanged.

## Hypothesis (if experiment)
If the catastrophic EXP-079 failure was driven mainly by an unstable or over-aggressive CORAL transform at `reg = 1e-6`, then a higher-regularization variant should preserve the positive universe-1 signal instead of blowing up a small number of target predictions.

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
- Adaptation: CORAL with `reg = 1e-3`

## Code & Environment
- Script: `scripts\model_transfer.py`
- Config: `experiments/EXP-081_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_coral_reg1e3/config/exp081_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_coral_reg1e3.json`
- Base config copied from: `EXP-079`
- Primary comparison targets after execution: `EXP-063 and EXP-079`
- Planned conda env: `fresco_v2`
- Planned Python: `/home/<username>/anaconda3/envs/fresco_v2/bin/python`

## Execution
- Cluster: Gilbreth
- Submission command: `Not submitted yet`
- Job IDs: `pending`
- Start / end time (UTC): `pending`

## Outputs
- Output root: `experiments/EXP-081_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_coral_reg1e3/results/`
- Manifests: `experiments/EXP-081_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_coral_reg1e3/manifests/`
- Validation reports: `experiments/EXP-081_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_coral_reg1e3/validation/`

## Results Summary
- Not run yet; this staged experiment keeps the same frozen cohort and feature space as `EXP-079` while changing only CORAL regularization from `1e-6` to `1e-3`.
- Primary question after execution: does higher regularization preserve the previously positive universe-1 signal more cleanly than `EXP-079`?

## Validation Summary
- Config and run log staged locally only; manifests, validation artifacts, metrics, and predictions will be populated after a future Gilbreth run.
- No SLURM job has been submitted for this experiment yet.

## Known Issues / Caveats
- This run changes only the CORAL regularization strength relative to EXP-079; overlap cohorts, feature columns, random seed, and ridge model settings stay fixed.
- The run is staged only. No SLURM job has been submitted yet.
- The normalized label still carries the cross-cluster measurement-semantics caveat (`memory_includes_cache=true` on anvil and `false` on conte/stampede).

## Repro Steps
1. `source ~/anaconda3/bin/activate fresco_v2`
2. `cd /home/<username>/Code/FRESCO-Pipeline`
3. `python scripts/model_transfer.py --config experiments/EXP-081_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_coral_reg1e3/config/exp081_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_coral_reg1e3.json`
