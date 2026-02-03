# Workload Taxonomy & Regime Matching (Required for Cross-Cluster Insights)

**Last Updated**: 2026-02-03

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
