# FRESCO v3: Master Index

**Last Updated**: 2026-02-03  

## Purpose
This folder contains the **required documentation** to (1) produce the FRESCO v3 dataset and (2) publish a paper describing the process.

## Core Docs (Required)

### Dataset Production
1. `docs/DATASET_PRODUCTION_SPEC.md` – what v3 is, outputs, guarantees, and invariants
2. `runbooks/PRODUCTION_RUNBOOK.md` – step-by-step operational procedure
3. `runbooks/REPRODUCIBILITY_CHECKLIST.md` – what must be logged + verified
4. `docs/SCHEMA_AND_PROVENANCE.md` – schema, dtype stability rules, provenance columns
5. `docs/DATA_QUALITY_AND_VALIDATION.md` – validation rules + known caveats
6. `docs/WORKLOAD_TAXONOMY_AND_MATCHING.md` – how cross-cluster comparisons are made defensible
7. `docs/CONFIGURATION.md` – config file formats, parameters, and defaults

### Paper-Ready Documentation
8. `paper/PAPER_OUTLINE.md` – section-by-section outline + claims we can defend
9. `paper/METHODS.md` – reproducible methods text (draftable into a paper)
10. `paper/EXPERIMENTS_AND_EVAL.md` – evaluation protocol, experiments, and reporting requirements
11. `paper/THREATS_TO_VALIDITY.md` – limitations (covariate shift, measurement equivalence)
12. `paper/ARTIFACTS_AND_REPRO_GUIDE.md` – how reviewers reproduce results

### Research Artifacts (Examples)
13. `docs/EXPERIMENT_LOG_TEMPLATE.md` – template for each experiment/production run
14. `experiments/EXP-015_baseline/` – frozen baseline reference + single-command replay reproducer
15. `experiments/EXP-016_feature_matrix/` – Phase 1 run folder (config/manifests/validation/logs/results)
16. `docs/feature_matrix.md` – Phase 1 feature availability matrix (EXP-016)
17. `experiments/EXP-017_regime_matching/` – Phase 2 overlap diagnostics + matched cohort indices (local proxy)
18. `experiments/EXP-018_regime_matching_alloc_only/` – Phase 2 sensitivity: allocations-only overlap
19. `docs/regime_matching.md` – Phase 2 summary (EXP-017)
20. `experiments/EXP-019_modeling_alloc_only/` – Phase 3 baseline transfer model (proxy label, allocations-only)
21. `experiments/EXP-020_regime_matching_alloc_perf_nomem/` – Phase 2 ablation: alloc+perf overlap (job-level, no memused)
22. `experiments/EXP-021_modeling_alloc_perf_nomem/` – Phase 3 ablation: alloc+perf transfer (job-level, no memused)
23. `experiments/EXP-022_regime_matching_alloc_only_joblevel/` – Phase 2 rerun: allocations-only overlap (job-level)
24. `experiments/EXP-023_modeling_alloc_only_joblevel/` – Phase 3 rerun: allocations-only transfer (job-level)
25. `experiments/EXP-024_regime_matching_alloc_perf_nomem_band_01_09/` – Phase 2 ablation: alloc+perf overlap (job-level, no memused, overlap band [0.1,0.9])
26. `experiments/EXP-025_modeling_alloc_perf_nomem_band_01_09/` – Phase 3 ablation: alloc+perf transfer (job-level, no memused, overlap band [0.1,0.9])

## Quick Links
- Planning: `../ZERO_SHOT_CROSS_CLUSTER_TRANSFER_PLAN.md`
