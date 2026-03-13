# EXP-079 Run Log -- Staged CORAL adaptation modeling on the frozen no-queue universe

**Run ID**: EXP-079_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_coral
**Date**: 2026-03-13
**Owner**: <username>

## Objective
Test whether explicit CORAL feature adaptation on the stronger five-feature frozen no-queue design preserves or improves the positive universe-1 transfer result without relying on further feature pruning.

## Hypothesis (if experiment)
If the remaining failure mode is unresolved source/target covariance shift inside the matched cohort, then CORAL alignment in the existing log1p-transformed five-feature space should retain the positive universe-1 result and provide a fairer baseline before judging adaptation on harder universes.

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
- Adaptation: CORAL with `reg = 1e-6`

## Code & Environment
- Script: `scripts\model_transfer.py`
- Config: `experiments/EXP-079_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_coral/config/exp079_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_coral.json`
- Base config copied from: `EXP-063`
- Planned conda env: `fresco_v2`
- Planned Python: `/home/<username>/anaconda3/envs/fresco_v2/bin/python`
- Prior CORAL reference: `experiments/EXP-027_modeling_alloc_perf_nomem_band_01_09_coral/` (proxy-only and not directly comparable)

## Execution
- Cluster: Gilbreth
- Submission command: `Not submitted yet`
- Job IDs: `pending`
- Start / end time (UTC): `pending`

## Outputs
- Output root: `experiments/EXP-079_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_coral/results/`
- Manifests: `experiments/EXP-079_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_coral/manifests/`
- Validation reports: `experiments/EXP-079_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_coral/validation/`

## Results Summary
- Not run yet; this staged experiment will reuse the frozen EXP-062 overlap cohort and apply CORAL adaptation in the existing log1p-transformed five-feature space before ridge modeling.
- Primary comparison target after execution: EXP-063 through EXP-069, especially EXP-063 target R^2 = 0.1070.
- Acceptance focus after execution: preserve or improve the positive universe-1 transfer while keeping provenance directly comparable to the non-adapted no-queue baseline.

## Validation Summary
- Config and run log staged locally only; manifests, validation artifacts, metrics, and predictions will be populated after a future Gilbreth run.
- No SLURM job has been submitted for this experiment yet.

## Known Issues / Caveats
- CORAL support already exists in scripts\model_transfer.py, but the only prior tracked CORAL experiment (EXP-027) ran on the old proxy-label feature space and failed catastrophically, so this authoritative rerun is a fresh baseline rather than a validated adaptation recipe.
- This experiment intentionally keeps the stronger five-feature no-queue design from EXP-063 rather than the weaker runtime_sec-only ablation from EXP-076.
- The normalized label still carries the cross-cluster measurement-semantics caveat (memory_includes_cache=true on anvil and false on conte/stampede).

## Repro Steps
1. `source ~/anaconda3/bin/activate fresco_v2`
2. `cd /home/<username>/Code/FRESCO-Pipeline`
3. `python scripts/model_transfer.py --config experiments/EXP-079_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_coral/config/exp079_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_coral.json`
