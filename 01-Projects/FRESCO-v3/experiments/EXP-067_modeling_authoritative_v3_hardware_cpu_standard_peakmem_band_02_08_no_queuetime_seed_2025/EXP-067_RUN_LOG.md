# EXP-067 Run Log  Planned modeling repeat on authoritative v3 without queue_time_sec (seed 2025)

**Run ID**: EXP-067_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_seed_2025  
**Date**: 2026-03-12
**Owner**: <username>

## Objective
Repeat the normalized peak-memory transfer baseline with seed 2025 while dropping queue_time_sec from both overlap and modeling feature sets.

## Hypothesis (if experiment)
If queue_time_sec is forcing the model to learn scheduler-specific structure, removing it may produce a more defensible repeat than EXP-049 without otherwise changing the baseline recipe.

## Inputs
- Dataset label: `chunks-v3-authoritative`
- Input manifest: `/depot/<group>/data/josh/FRESCO/chunks-v3/manifests/output_manifest.jsonl`
- Frozen sampling plan: `experiments/ANALYSIS_seed_instability/frozen_sampling_plan_exp044_hwcpu_standard_300k_24_seed1337.json`
- Clusters: anvil / conte / stampede
- Date range: 2015-01-01 to 2023-12-31
- Cohorts (planned from EXP-062_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_no_queuetime):
  - `experiments/EXP-062_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_no_queuetime/results/matched_source_indices.parquet`
  - `experiments/EXP-062_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_no_queuetime/results/matched_target_indices.parquet`
- Label: `peak_memory_fraction` with `log1p` transform (`label_proxy=false`)

## Code & Environment
- Script: `scripts\model_transfer.py`
- Config: `experiments/EXP-067_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_seed_2025/config/exp067_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_seed_2025.json`
- Git commit (pipeline): `TBD at execution time; current local changes add sampling_plan_path support`
- Git commit (analysis): `TBD at execution time`
- Conda env: `TBD at execution time`
- Python: `TBD at execution time`
- Package lock: `experiments/EXP-067_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_seed_2025/validation/pip_freeze.txt`

## Notes
- Workstream B scaffolding only: this run has **not** been submitted yet.
- This modeling repeat now reuses the frozen EXP-062 overlap cohort, so only the train/test split seed changes across EXP-063/065/067/069.
- This config preserves the EXP-045/047/049/051 modeling design except for removing `queue_time_sec` from both the Phase 2 overlap reference and the Phase 3 `feature_columns` list.
- Renumbering rationale: the originally requested EXP-052..059 identifiers are already occupied by committed dense-sampling and alloc-only diagnosis runs, so this planned family is staged as EXP-062..069 instead.
- Rationale for the feature change: `queue_time_sec` appears to encode scheduler/cluster behavior more than workload similarity, and the tightened family tests whether removing it improves transfer stability without otherwise changing the baseline recipe.
- The normalized label still inherits the cross-cluster measurement-semantics caveat (`memory_includes_cache=true` on anvil and `false` on conte/stampede).

## Execution
- Cluster: Gilbreth
- Submission command: `Not submitted in Workstream B. Planned repro command: python scripts\model_transfer.py --config experiments\EXP-067_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_seed_2025\config\exp067_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_seed_2025.json`
- Job IDs: `Not assigned (job submission intentionally deferred)`
- Start / end time (UTC): `N/A / N/A`

## Outputs
- Output root: `experiments/EXP-067_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_seed_2025/results/`
- Manifests: `experiments/EXP-067_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_seed_2025/manifests/`
- Validation reports: `experiments/EXP-067_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_seed_2025/validation/`

## Results Summary
- Planned run only; no job has been submitted in Workstream B, so no metrics or overlap artifacts exist yet.
- Expected result artifacts, once executed, will be written under `experiments/EXP-067_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_seed_2025/results/` and should be cited there before making any claim.

## Validation Summary
- Not run yet. Validation artifacts will be produced under `experiments/EXP-067_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_seed_2025/validation/` after execution.

## Known Issues / Caveats
- This log records a **planned** run only; nothing in this folder should be interpreted as executed evidence.
- The experiment numbering was renumbered from the user-requested EXP-052..059 to EXP-062..069 because EXP-052..059 are already occupied by immutable committed historical runs.
- Final submission and any design adjustments should wait for Workstream A analysis of the current instability diagnosis.

## Repro Steps
1. Confirm the queue-time-free + frozen-sampling design is still the preferred next ablation after Workstream A review.
2. Capture the final execution environment into `experiments/EXP-067_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_seed_2025/validation/` before submission.
3. Run `python scripts\model_transfer.py --config experiments\EXP-067_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_seed_2025\config\exp067_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08_no_queuetime_seed_2025.json`.
