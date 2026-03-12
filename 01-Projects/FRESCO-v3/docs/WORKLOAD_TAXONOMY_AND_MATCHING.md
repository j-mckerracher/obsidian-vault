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

Updated interpretation:
- EXP-045 is now best read as a promising single split, not a stable matched-regime result.
- Higher overlap coverage alone did not guarantee transfer: the seed-2025 repeat widened overlap substantially but still produced the worst target `R^2`.
- The normalized-label path remains the right direction, but the current sampled authoritative baseline is still too unstable for a publication claim.

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

## 9. Immediate next requirement
The next high-value task is now to diagnose why the normalized baseline remains unstable even after denser sampling:
- test whether the remaining failure is driven more by model specification / feature set than by cohort sampling depth,
- quantify how much `queue_time_sec` and `runtime_fraction` mismatch is still dominating the matched cohorts,
- decide whether to revise the overlap feature set or the Phase 3 model before extending to other cluster pairs,
- keep the measurement-semantics caveat explicit while doing that diagnosis.
