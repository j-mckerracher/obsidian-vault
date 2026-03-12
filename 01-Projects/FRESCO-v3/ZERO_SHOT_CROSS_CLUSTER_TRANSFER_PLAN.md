# FRESCO v3: Path to Zero‑Shot Cross‑Cluster Memory Prediction

**Last Updated**: 2026-03-12
**Owner**: <username>  
**Status**: Draft plan (ready to execute)

## Executive Summary

EXP-014/015 show that **v2.0 fixed schema + normalization**, but **zero‑shot transfer** (train on cluster A labels, predict on cluster B with *no labeled target*) still fails badly (R²  0) because the clusters are not i.i.d.:

- **Severe covariate shift** (e.g., partition/node_type completely non‑overlapping; KS up to 1.0)
- **Conditional shift** (the mapping \(E[y|x]\) differs by cluster)
- **Era / workload regime shift** (Conte 2015 CPU era vs Anvil 2022 GPU/AI era)

A path forward exists, but it requires **changing the problem definition** from “global transfer across all jobs” to one of the following:

1. **Zero‑shot transfer within *matched regimes*** (CPU‑only ↔ CPU‑only; comparable partitions; overlapping feature support)
2. **Domain adaptation using unlabeled target data** (still zero‑label, but not zero‑data): distribution alignment / calibration
3. **Learning invariant representations** using richer signals (time‑series/perf metrics) rather than allocations only

This document provides a concrete execution plan to deliver **the strongest defensible version of zero‑shot cross‑cluster prediction**.

## Authoritative status update (2026-03-12)

The authoritative `chunks-v3` reruns are now complete enough to sharpen the plan:

- EXP-039 confirmed the authoritative strict safe-feature path and supports using:
  - `ncores`
  - `nhosts`
  - `timelimit_sec`
  - `runtime_sec`
  - `queue_time_sec`
  - `runtime_fraction`
- EXP-040/041 (alloc + perf overlap features) remained too separable and transferred very poorly:
  - overlap AUC = `0.9962`
  - target overlap coverage = `25.94%`
  - target `R^2 = -11.8921`
- EXP-042/043 (strict safe-feature overlap) improved the situation, but not enough:
  - overlap AUC = `0.9369`
  - target overlap coverage = `33.18%`
  - target `R^2 = -4.2053`

Conclusion: narrowing to safer overlap features helps, but the current proxy regime + raw `value_memused_max` target still does not deliver a defensible zero-shot Anvil -> Conte transfer story.

---

## Definitions (to avoid ambiguity)

### What “zero‑shot” means here
- **Allowed**: 
  - Labeled source cluster data (train)
  - Unlabeled target cluster features (for adaptation/alignment)
  - Hardware metadata (node_memory_gb, node_type, gpu_count_per_node)
  - Non‑label target distribution summaries (e.g., feature histograms)
- **Not allowed**:
  - Using any labeled target jobs to fit parameters (no fine‑tuning, no calibration fit on target labels)

### Success Criteria
We should define tiered success metrics:

- **Tier A (realistic)**: R² > 0 on *matched* target regime (CPU↔CPU subset), stable across repeated splits, with uncertainty bounds.
- **Tier B (stretch)**: R² > 0 for broader target workloads but not necessarily the full distribution.
- **Tier C (unlikely)**: R² > 0 for the full Conte↔Anvil distribution without any regime matching.

---

## Root Cause Diagnosis (from EXP-015)

### Evidence of covariate shift
- partition KS = 1.00 (disjoint)
- node_type KS  0.999 (disjoint)
- log_ncores KS  0.88 (extreme)

**Implication**: models are extrapolating outside training support. Tree models in particular extrapolate poorly.

### Evidence of conditional / label shift
Transfer models show **large signed bias** in log space (e.g., +1.61, -2.31), and negative calibration slopes.

**Implication**: even within overlapping support, the mapping differs (measurement semantics and workload structure differ).

---

## Proposed v3 Strategy

We pursue three parallel tracks and merge outcomes:

### Track 1 — Regime‑Matched Zero‑Shot (high probability)
**Goal**: Make zero‑shot feasible by restricting evaluation to overlapping regimes.

Key idea: if Anvil contains CPU partitions and CPU‑like jobs comparable to Conte, transfer becomes an *inter‑site* problem rather than *inter‑era/architecture*.

Deliverables:
- A **workload taxonomy** shared across clusters (CPU, GPU, largemem, etc.)
- A **matched cohort builder** that constructs comparable train/test splits by *feature support overlap*.

### Track 2 — Unlabeled Domain Adaptation (medium probability)
**Goal**: Use unlabeled target features to align distributions (zero‑label).

Candidate methods:
- **CORAL** (covariance alignment) on standardized continuous features
- **MMD** minimization in latent space (kernel alignment)
- **Domain‑adversarial representation learning (DANN)** (requires NN)
- **Quantile mapping / distribution matching** of model outputs (unsupervised calibration)

### Track 3 — Richer Predictors (medium probability)
**Goal**: Use features that are more universal across clusters than scheduler metadata.

Candidate features (prefer those available in all clusters):
- value_cpuuser (and optionally nfs/block)
- runtime_fraction / runtime_efficiency
- failure/timed_out indicators

If available as time series/snapshots, derive robust aggregates:
- median/95p CPU usage
- I/O intensity bins
- “job signature” clusters via unsupervised embeddings

---

## Detailed Workplan

### Phase 0 — v3 Repo Structure & Baselines
- [x] Create `FRESCO-v3` workspace structure:
  - `experiments/`
  - `docs/`
  - `scripts/`
  - `results/`
- [x] Copy forward EXP-015 as baseline reference (frozen)
  - Snapshot copied to: `01-Projects/FRESCO-v3/experiments/EXP-015_baseline/source/`
  - Replay reproducer (single command): `python scripts\\reproduce_exp015_baseline.py --config experiments\\EXP-015_baseline\\config\\reproduce_exp015_baseline.json`
  - Limitations: this reproducer regenerates baseline *artifacts* from the frozen snapshot; it does not recompute EXP-015 from raw shards because the referenced scripts/logs are not present in the snapshot.
- [x] Define one canonical evaluation split protocol (seeded, reproducible)
  - Documented in: `paper/EXPERIMENTS_AND_EVAL.md` (“Canonical split protocol (v3 default)”).
- [x] Copied authoritative schema PDF from Gilbreth:
  - `docs/FRESCO_Repository_Description.pdf`
- [x] Sampled source data headers on Gilbreth (Action 2 in v2 quick start):
  - Anvil: JobAccounting + JobResourceUsage sample headers
  - Conte: `TACC_Stats/2015-03/cpu.csv` header
  - Stampede: `TACC_Stats/NODE1/cpu.csv` header

**Acceptance (Phase 0)**: EXP-015 baseline artifacts + summary can be regenerated from v3 with a single command, and the v3 evaluation split protocol is explicitly documented.

---

### Phase 1 — Feature Availability Matrix (All Clusters)
- [x] Build a script to compute:
  - intersection of columns across clusters
  - per‑cluster missingness rates for candidate features
  - type stability checks (parquet schema drift)
- [x] Produce `docs/feature_matrix.md` (run: `experiments\EXP-016_feature_matrix\`)

**Acceptance**: we have a vetted list of features safe for cross‑cluster modeling (see `docs\feature_matrix.md`).

---

### Phase 2 — Workload Taxonomy + Regime Matching
#### 2.1 Define a common taxonomy
- CPU vs GPU vs largemem vs unknown
- Derive from:
  - gpu_count_per_node, gpus_allocated, gpu_model
  - node_type
  - node_memory_gb / node_cores
  - partition (mapped per cluster into taxonomy)

#### 2.2 Overlap‑aware cohort construction
Implemented local-proxy overlap workflow:
- Script: `scripts\regime_matching.py`
- Run folder: `experiments\EXP-017_regime_matching\`
- Method: propensity (domain classifier) overlap with band **[0.2, 0.8]**
- Regime: `cpu_standard` (local proxy definition; see EXP-017 run log)

Key outputs:
- Overlap report: `experiments\EXP-017_regime_matching\results\overlap_report.json`
- Matched cohorts (indices):
  - `...\results\matched_source_indices.parquet`
  - `...\results\matched_target_indices.parquet`

**Acceptance**: cohort builder + overlap report exist and quantify coverage/shift (AUC, KS).

---

### Phase 3 — Modeling for Zero‑Shot
#### 3.1 Models to try (in order)
1. **Regularized linear / GAM** (better extrapolation than trees)
2. **Monotonic XGBoost** (constrain directions; improves stability)
3. **Quantile regression** (robust to heteroscedasticity)
4. **Neural net + DANN** (if Track 2 needed)

#### 3.2 Objective
Predict:
- \(y = \log(peak\_memory\_fraction)\)

#### 3.3 Report metrics
- R², MAE(log), MdAE(log), SMAPE
- Bias (mean residual)
- Calibration slope/intercept
- Uncertainty: bootstrap CI for R²

#### Phase 3 progress (local proxy)
- Baseline run (allocations-only, proxy label): `experiments\\EXP-019_modeling_alloc_only\\`
  - Repro: `python scripts\\model_transfer.py --config experiments\\EXP-019_modeling_alloc_only\\config\\exp019_modeling_alloc_only.json`
  - Result: Target (Conte) R² is strongly negative on proxy label; see `...\\results\\metrics.json`.

- Job-level rerun (allocations-only; fixes duplicate-jid weighting):
  - Phase 2 overlap: `experiments\\EXP-022_regime_matching_alloc_only_joblevel\\`
    - Key numbers: AUC≈0.8025, Conte overlap coverage=1.0.
  - Phase 3 modeling: `experiments\\EXP-023_modeling_alloc_only_joblevel\\`
    - Result: Target R²≈-30.21 on proxy label.

- Ablation run (alloc + perf aggregates, **exclude memused**; job-level aggregation):
  - Phase 2 overlap: `experiments\\EXP-020_regime_matching_alloc_perf_nomem\\`
    - Repro: `python scripts\\regime_matching.py --config experiments\\EXP-020_regime_matching_alloc_perf_nomem\\config\\exp020_regime_matching_alloc_perf_nomem.json`
    - Key numbers: AUC≈0.9895, Conte overlap coverage≈0.321 (see `...\\results\\overlap_report.json`).
  - Phase 3 modeling: `experiments\\EXP-021_modeling_alloc_perf_nomem\\`
    - Repro: `python scripts\\model_transfer.py --config experiments\\EXP-021_modeling_alloc_perf_nomem\\config\\exp021_modeling_alloc_perf_nomem.json`
    - Result: extremely negative target R² on proxy label (see `...\\results\\metrics.json`).

- Overlap-band sensitivity (alloc+perf, no memused; job-level):
  - Phase 2 overlap (band **[0.1,0.9]**): `experiments\\EXP-024_regime_matching_alloc_perf_nomem_band_01_09\\`
    - Key numbers: AUC≈0.9895, Conte overlap coverage≈0.416.
  - Phase 3 modeling (Ridge): `experiments\\EXP-025_modeling_alloc_perf_nomem_band_01_09\\`
    - Result: still catastrophic target R² on proxy label (~ -1.29e5).
  - Phase 3 modeling (HuberRegressor): `experiments\\EXP-026_modeling_alloc_perf_nomem_band_01_09_huber\\`
    - Result: target R²=-867.12 on proxy label (still negative, but far less extreme vs Ridge).

**Acceptance**: on regime‑matched cohorts, achieve Tier A success (R² > 0) with stable CI (requires rerun on true v3 shards and true label).

### Authoritative Phase 3 status
- [x] Rerun authoritative overlap/modeling on the raw `chunks-v3` parquet.
- [x] Confirm that alloc+perf overlap features are too separable for primary claims.
- [x] Confirm that the strict safe-feature overlap set improves transfer but still leaves target `R^2 < 0`.
- [ ] Recover authoritative hardware metadata needed to derive `peak_memory_fraction` and non-proxy workload regimes.
- [ ] Re-run Phase 2/3 on normalized memory targets after that metadata is restored.

---

### Phase 4 — Unlabeled Domain Adaptation (Zero‑Label)
#### 4.1 Domain classifier diagnostics
- Train a classifier to predict domain from features.
- If AUC  0.9, domains are highly separable → transfer will fail without matching/adaptation.

#### 4.2 CORAL baseline
- Align covariance of continuous features using unlabeled target.
- Train model on aligned source; evaluate on aligned target.
  - Proxy run: `experiments\\EXP-027_modeling_alloc_perf_nomem_band_01_09_coral\\`
    - Result: catastrophic negative target R² with severe numerical instability (proxy-only); see `...\\results\\metrics.json`.

#### 4.3 Output distribution matching (unsupervised)
- Fit a monotonic mapping on *predicted outputs* to match target’s predicted distribution to a reference distribution (careful: avoids using labels but can still distort semantics).

**Acceptance**: show measurable improvement over non‑adapted zero‑shot on matched cohorts; document failure modes clearly.

---

### Phase 5 — Rigor + Publication Readiness
- [ ] Repeat across multiple month pairs (not just one window; proxy single-month pairs EXP-033..EXP-038)
- [ ] Add ablations:
  - allocations only vs allocations+runtime vs allocations+perf metrics
  - with/without matching
  - with/without adaptation (proxy runs: EXP-027 CORAL vs EXP-028 no-adapt)
- [ ] Add sensitivity analysis to cohort overlap thresholds (proxy runs: EXP-029/030 [0.05,0.95], EXP-031/032 [0.2,0.8])

**Acceptance**: reproducible report with clear scope: “zero‑shot works for X% of target jobs under regime Y; fails elsewhere due to domain shift.”

---

## Risks & Mitigations

### Risk 1: True zero‑shot across full distributions is impossible
Mitigation: publish the **negative result** rigorously and pivot to *regime‑conditional transfer*.

### Risk 2: Feature semantics differ (measurement non‑equivalence)
Mitigation: stratify by `memory_includes_cache`, `memory_collection_method`; treat as separate domains.

### Risk 3: Partitions encode cluster identity
Mitigation: map partitions into a **shared taxonomy** and use only taxonomy labels (CPU/GPU/large) rather than raw partition strings.

---

## Concrete Next Steps (Immediate)

1. Implement `feature_matrix.py` to compute intersection + missingness.
2. Implement `workload_taxonomy.py` (mapping per cluster).
3. Implement `cohort_builder.py` with overlap diagnostics.
4. Run a first v3 experiment:
   - Source: Conte (CPU)
   - Target: Anvil CPU partitions only
   - Model: regularized linear / GAM
   - Evaluate Tier A success.

---

## Why this can work

Zero‑shot transfer fails today because we’re trying to transfer across:
- different **eras** (2015 vs 2022)
- different **hardware regimes** (CPU vs GPU/AI)
- disjoint **scheduler partitions**

By (1) restricting to overlapping regimes and (2) using unlabeled adaptation + more universal signals, we can create a **defensible and useful** zero‑shot story.

---

## References (internal)
- `../FRESCO-v2/PROGRESS_TRACKER.md` (Phase 7 summary)
- `../FRESCO-Research/Experiments/EXP-015_enhanced_validation/EXP015_FINAL_REPORT.md` (rigorous results)
