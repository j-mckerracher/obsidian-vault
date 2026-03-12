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

## 5. Current authoritative status (2026-03-12)
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

## 6. Refined design decision
Until hardware metadata is restored, the default authoritative overlap feature set should use only the strict 0% missingness safe columns confirmed by Phase 1:

```text
ncores, nhosts, timelimit_sec, runtime_sec, queue_time_sec, runtime_fraction
```

Do **not** include raw performance counters or memory columns in the overlap feature set for primary transfer claims.

The next authoritative comparison pair is therefore:
- `EXP-042_regime_matching_authoritative_v3_safe_features_band_02_08`
- `EXP-043_modeling_authoritative_v3_safe_features_band_02_08`

Treat alloc+perf overlap runs such as EXP-040/041 as exploratory ablations, not the default publication path.
