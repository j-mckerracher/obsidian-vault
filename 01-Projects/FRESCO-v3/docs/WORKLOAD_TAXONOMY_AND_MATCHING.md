# Workload Taxonomy & Regime Matching (Required for Cross-Cluster Insights)

**Last Updated**: 2026-03-12

## Purpose
Enable **defensible cross-cluster insights** by ensuring we compare **like with like**.

## 1. Taxonomy
Define a shared taxonomy label `workload_regime`:
- `cpu_standard`
- `cpu_largemem`
- `gpu_standard`
- `gpu_largemem`
- `unknown`

Derivation signals:
- `gpu_count_per_node`, `gpus_allocated`, `gpu_model`
- `node_memory_gb`, `node_cores`
- `node_type`
- `partition` (cluster-specific → mapped into taxonomy)

## 2. Overlap-aware cohort builder
For any cross-cluster experiment comparing A vs B:

1. Choose feature set F.
2. Standardize continuous features.
3. Compute overlap score via domain classifier propensity:
   - train classifier to predict domain (A vs B) using F
   - define overlap as samples with P(domain=A|x) in [0.2, 0.8]
4. Evaluate models only within overlap region (primary) and outside (secondary).

## 3. Reporting requirements
Every cross-cluster claim must report:
- regime definition
- overlap coverage (% of target jobs)
- feature support diagnostics (KS stats, domain classifier AUC)
- residual bias and calibration

## 4. Non-negotiable constraint
No “global cross-cluster” claims without regime matching + overlap reporting.

## 5. Proxy-only authoritative baseline (historical)
- The authoritative v3 parquet still does **not** store `partition`, `node_type`, `node_memory_gb`, or `gpu_count_per_node`, so current regime labels remain **proxy-based** even on authoritative data.
- The current proxy is:
  - `cpu_standard := value_gpu_max <= 0` when available
  - otherwise `cpu_standard := (value_gpu_cnt <= 0) AND (value_gpu_sum <= 0)`
- Authoritative EXP-040 (alloc + perf counters) still produced severe domain separability:
  - domain AUC = `0.9962`
  - target overlap coverage = `25.94%`
- Authoritative EXP-041 then still showed very poor transfer on raw `value_memused_max`:
  - source-test `R^2 = 0.3103`
  - target `R^2 = -11.8921`

## 6. Safe-feature proxy baseline
Before hardware metadata was recovered at analysis time, the default authoritative overlap feature set used only the strict 0% missingness safe columns confirmed by Phase 1:

```text
ncores, nhosts, timelimit_sec, runtime_sec, queue_time_sec, runtime_fraction
```

Do **not** include raw performance counters or memory columns in the overlap feature set for primary transfer claims.

The authoritative safe-feature comparison pair is:
- `EXP-042_regime_matching_authoritative_v3_safe_features_band_02_08`
- `EXP-043_modeling_authoritative_v3_safe_features_band_02_08`

Results from that pair:
- EXP-042:
  - domain AUC = `0.9369`
  - target overlap coverage = `33.18%`
- EXP-043:
  - source-test `R^2 = 0.2282`
  - target `R^2 = -4.2053`

Interpretation:
- Restricting to safe overlap features helps, but it does **not** make raw `value_memused_max` transfer viable across Anvil -> Conte.
- Treat alloc+perf overlap runs such as EXP-040/041 as exploratory ablations, not the default publication path.
- Treat EXP-042/043 as the current best proxy-only baseline, not a publication-ready transfer result.

## 7. Recovered hardware-metadata path
We now recover hardware metadata at analysis time via `config/clusters.json`:
- `partition := queue`
- `node_type`, `node_cores`, `node_memory_gb`, `gpu_count_per_node`, `gpu_model` come from per-cluster defaults and known Anvil partition mappings
- Conte and Stampede queue identifiers remain anonymized, so those clusters use cluster-wide defaults
- `peak_memory_fraction := peak_memory_gb / (node_memory_gb * nhosts)`

This enables explicit hardware-based regime filters such as:
- `hardware_cpu_standard`
- `hardware_cpu_largemem`
- `hardware_gpu_standard`

## 8. Current best authoritative baseline
The first hardware-normalized comparison pair is:
- `EXP-044_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08`
- `EXP-045_modeling_authoritative_v3_hardware_cpu_standard_peakmem_band_02_08`

Results from that pair:
- EXP-044:
  - domain AUC = `0.9398`
  - target overlap coverage = `33.04%`
- EXP-045:
  - source-test `R^2 = 0.1414`
  - target `R^2 = 0.0878`
  - target bootstrap `R^2` 95% CI = `[0.0556, 0.1132]`

Interpretation:
- Recovering hardware metadata and switching to normalized `peak_memory_fraction` changed the Anvil -> Conte target result from clearly negative to modestly positive.
- This is the strongest authoritative transfer result so far, but it is still a baseline rather than a final claim because:
  - Conte and Stampede hardware metadata still rely on cluster-wide defaults,
  - Conte queue names remain anonymized,
  - memory measurement semantics still differ across clusters.

Repeated-seed validation runs then checked whether that positive split was stable:
- `EXP-046` / `EXP-047` (seed `2024`)
  - overlap AUC = `0.9394`
  - target overlap coverage = `26.92%`
  - target `R^2 = -0.0346`
  - bootstrap 95% CI = `[-0.0741, -0.0063]`
- `EXP-048` / `EXP-049` (seed `2025`)
  - overlap AUC = `0.9073`
  - target overlap coverage = `58.89%`
  - target `R^2 = -2.1030`
  - bootstrap 95% CI = `[-2.3111, -1.9280]`
- `EXP-050` / `EXP-051` (seed `2026`)
  - overlap AUC = `0.9271`
  - target overlap coverage = `40.37%`
  - target `R^2 = -0.2882`
  - bootstrap 95% CI = `[-0.3788, -0.2020]`

Updated interpretation before the frozen no-queue correction:
- EXP-045 is now best read as a promising single split, not a stable matched-regime result.
- Higher overlap coverage alone did not guarantee transfer: the seed-2025 repeat widened overlap substantially but still produced the worst target `R^2`.
- The normalized-label path remained the right direction, but the sampled authoritative baseline on its own was still too unstable for a publication claim.

Completed frozen no-queue-time follow-up (EXP-062..069):
- `EXP-062` (`experiments/EXP-062_regime_matching_authoritative_v3_hardware_cpu_standard_band_02_08_no_queuetime/results/overlap_report.json`) nearly reproduced the original EXP-044 geometry while dropping `queue_time_sec`: domain AUC = `0.9366`, target overlap coverage = `33.31%`, source overlap = `6995 / 12649`, target overlap = `2459 / 7383`.
- The frozen sampling artifact `experiments/ANALYSIS_seed_instability/frozen_sampling_plan_exp044_hwcpu_standard_300k_24_seed1337.json` fixed the EXP-044-equivalent `300k / 24` row-group universe as 24 Anvil row groups (`286,843` raw rows -> `13,260` jobs) and 24 Conte row groups (`131,122` raw rows -> `7,383` jobs), removing the raw sampling drift diagnosed in Workstream A.
- The meaningful repeated-split comparison is `EXP-063/065/067/069` on the shared `EXP-062` overlap cohort; `EXP-064/066/068` remain provenance placeholders because the frozen plan makes Phase 2 deterministic for this design.
- `EXP-063` (`.../EXP-063.../results/metrics.json`), `EXP-065` (`.../EXP-065.../results/metrics.json`), `EXP-067` (`.../EXP-067.../results/metrics.json`), and `EXP-069` (`.../EXP-069.../results/metrics.json`) all returned positive target `R^2`: `0.1070`, `0.1099`, `0.1089`, and `0.1108`, respectively.
- All four no-queue modeling repeats also kept their bootstrap 95% intervals strictly above zero (`[0.0788, 0.1291]`, `[0.0861, 0.1351]`, `[0.0812, 0.1354]`, `[0.0804, 0.1365]`) and target slopes near `1.0` (`0.9593` to `1.0498`), so the result is now stable across modeling split seeds on the frozen cohort.
- Updated interpretation: the earlier failure was not an unavoidable label-semantics collapse. It was largely driven by queue-time-driven overlap drift plus seed-dependent sampling drift. Once `queue_time_sec` is removed and the sampled universe is frozen, the authoritative Anvil -> Conte `hardware_cpu_standard` / `peak_memory_fraction` pathway yields a repeatable positive zero-shot result on that cohort.
- Remaining caveat: this is stability on a fixed frozen universe, not yet a claim about all possible overlap universes or all cluster pairs.
A denser-sampling stabilization attempt then tested whether the instability was mainly a row-group sampling artifact:
- `EXP-052` / `EXP-053` (seed `1337`, `max_rows=600000`, `sample_n_row_groups_per_file=128`)
  - overlap AUC = `0.9378`
  - target overlap coverage = `37.36%`
  - target `R^2 = -0.8817`
  - bootstrap 95% CI = `[-0.9372, -0.8255]`
- `EXP-054` / `EXP-055` (seed `2024`, same dense-sampling controls)
  - overlap AUC = `0.9536`
  - target overlap coverage = `24.25%`
  - target `R^2 = -0.1047`
  - bootstrap 95% CI = `[-0.1272, -0.0881]`

Dense-sampling interpretation:
- Increasing the sample depth alone did not stabilize the normalized baseline.
- On the original positive seed (`1337`), denser sampling actually pushed the target result decisively negative.
- That makes it unlikely that the earlier instability was only a 300k/24-row-group sampling artifact.

An alloc-only + Huber diagnosis then tested whether the remaining problem was still coming from timing-feature mismatch:
- `EXP-056` / `EXP-057` (seed `1337`, overlap/model features = `ncores`, `nhosts`, `timelimit_sec`)
  - overlap AUC = `0.8571`
  - target overlap coverage = `82.52%`
  - target `R^2 = -0.6492`
  - bootstrap 95% CI = `[-0.6831, -0.6182]`
- `EXP-058` / `EXP-059` (seed `2024`, same alloc-only + Huber design)
  - overlap AUC = `0.8607`
  - target overlap coverage = `83.03%`
  - target `R^2 = -1.4949`
  - bootstrap 95% CI = `[-1.5563, -1.4371]`

Alloc-only diagnosis interpretation:
- Simplifying the overlap feature set did reduce separability and dramatically widen target coverage, but it also collapsed source holdout signal (`source-test R^2` near `0`).
- Within-overlap `timelimit_sec` mismatch remained large (`KS ≈ 0.60`) even after removing queue and runtime-derived features.
- The tracked Huber runs therefore suggest the remaining failure is not just a queue-time artifact; the cross-cluster response relationship for normalized memory is still badly misspecified.

Post-hoc label-semantics diagnosis on the saved prediction artifacts then clarified the failure mode:
- On the dense alloc-only runs, the source-test median `peak_memory_fraction` stayed near `0.205`, while the true Conte target median was much lower (`0.074` for seed `1337`, `0.086` for seed `2024`).
- The alloc-only Huber model still predicted source-like target medians (`0.209` and `0.259`), so the transfer failure was dominated by source-centered prediction collapse rather than by overlap scarcity alone.
- A simple hidden-denominator correction did **not** explain the error: applying the expected `log(256 / 64) = log(4)` node-memory shift made target `R^2` dramatically worse.
- The positive single-split baseline (`EXP-045`) still showed some target calibration (`slope ≈ 0.90`) with the richer timing feature set, while the dense runs compressed target predictions into a narrow source-like band.

Label-semantics interpretation:
- Conte hardware CPU-standard jobs occupy a substantially lower normalized-memory median than the matched Anvil source jobs, even when they remain inside the overlap band.
- The current dense alloc-only model is too weak to learn that lower-median target regime, so it defaults toward a source-like prediction level.
- The next corrective experiment should therefore **decouple Phase 2 and Phase 3 feature sets**: keep safer overlap features if needed, but restore richer modeling features to test whether the low-median Conte label regime is actually predictable.

A decoupled-feature follow-up then tested that hypothesis directly:
- `EXP-060` (seed `1337`, alloc-only overlap from `EXP-056`, Phase 3 restored to the full safe timing feature set with Ridge)
  - source-test `R^2 = 0.0121`
  - target `R^2 = -1.5721`
  - bootstrap 95% CI = `[-1.6360, -1.5091]`
  - target slope = `-1.5997`
- `EXP-061` (seed `2024`, alloc-only overlap from `EXP-058`, same decoupled Phase 3 design)
  - source-test `R^2 = 0.0359`
  - target `R^2 = -0.8824`
  - bootstrap 95% CI = `[-0.9218, -0.8433]`
  - target slope = `-0.4331`

Decoupled-feature interpretation:
- Restoring the richer timing features did recover modest positive source holdout signal, so Phase 3 feature richness does matter.
- But both target slopes stayed negative and both target intervals remained fully below zero, so decoupling overlap and modeling features alone is still not enough.
- The remaining issue now looks more like unresolved domain shift inside the feature geometry than simple overlap scarcity or an underpowered source model.
## 9. Immediate next requirement
The immediate next requirement is no longer to decide whether to run the no-queue design; that family has now completed successfully on the frozen EXP-062 cohort:
- Record `EXP-062..069` as the current authoritative positive baseline for Anvil -> Conte transfer in the `hardware_cpu_standard` regime with `peak_memory_fraction`.
- Before making a publication-strength generalization claim, quantify sensitivity to frozen-universe choice (for example, a second frozen sampling plan) and/or extend the same queue-time-free recipe to additional cluster pairs.
- If alternate frozen universes or new cluster pairs fail, revisit either further timing-block simplification or explicit feature-space adaptation for those failing cases.
- Keep the measurement-semantics caveat explicit while extending the design.
