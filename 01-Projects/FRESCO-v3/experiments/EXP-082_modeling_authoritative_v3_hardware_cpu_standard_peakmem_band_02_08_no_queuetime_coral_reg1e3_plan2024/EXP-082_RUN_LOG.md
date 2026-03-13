# EXP-082 Run Log -- Staged higher-regularization CORAL adaptation modeling on the frozen no-queue universe

**Run ID**: EXP-082_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_coral_reg1e3_plan2024
**Date**: 2026-03-13
**Owner**: <username>

## Objective
Test whether increasing CORAL regularization to `1e-3` yields a cleaner second-universe comparison after EXP-080 showed that the naive `1e-6` setting barely changed the harder baseline.

## Hypothesis (if experiment)
If the second-universe CORAL result was damped by an unstable or poorly conditioned transform at `reg = 1e-6`, then a higher-regularization variant should provide a clearer signal about whether linear covariance adaptation can help at all on the harder frozen universe.

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
- Adaptation: CORAL with `reg = 1e-3`

## Code & Environment
- Script: `scripts\model_transfer.py`
- Config: `experiments/EXP-082_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_coral_reg1e3_plan2024/config/exp082_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_coral_reg1e3_plan2024.json`
- Base config copied from: `EXP-080`
- Primary comparison targets after execution: `EXP-071 and EXP-080`
- Planned conda env: `fresco_v2`
- Planned Python: `/home/<username>/anaconda3/envs/fresco_v2/bin/python`

## Execution
- Cluster: Gilbreth
- Submission command: `Not submitted yet`
- Job IDs: `pending`
- Start / end time (UTC): `pending`

## Outputs
- Output root: `experiments/EXP-082_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_coral_reg1e3_plan2024/results/`
- Manifests: `experiments/EXP-082_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_coral_reg1e3_plan2024/manifests/`
- Validation reports: `experiments/EXP-082_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_coral_reg1e3_plan2024/validation/`

## Results Summary
- Not run yet; this staged experiment keeps the same frozen cohort and feature space as `EXP-080` while changing only CORAL regularization from `1e-6` to `1e-3`.
- Primary question after execution: does higher regularization produce a more informative second-universe result than `EXP-080`?

## Validation Summary
- Config and run log staged locally only; manifests, validation artifacts, metrics, and predictions will be populated after a future Gilbreth run.
- No SLURM job has been submitted for this experiment yet.

## Known Issues / Caveats
- This run changes only the CORAL regularization strength relative to EXP-080; overlap cohorts, feature columns, random seed, and ridge model settings stay fixed.
- The run is staged only. No SLURM job has been submitted yet.
- The normalized label still carries the cross-cluster measurement-semantics caveat (`memory_includes_cache=true` on anvil and `false` on conte/stampede).

## Repro Steps
1. `source ~/anaconda3/bin/activate fresco_v2`
2. `cd /home/<username>/Code/FRESCO-Pipeline`
3. `python scripts/model_transfer.py --config experiments/EXP-082_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_coral_reg1e3_plan2024/config/exp082_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_coral_reg1e3_plan2024.json`
